import json
from django.conf import settings
from django.core.cache import cache
from django.http import JsonResponse
from django.core import serializers
from rest_framework.views import APIView
from Apps.Api.utils import Authtication, VisitThrottle, AuthticationWithoutPackageId
from Apps.ARExperiences.models import ARExperienceModel, ARExperienceAsset
from Apps.ARShowcasesCenter.models import ARShowcasesCenterModel, ARShowcasesAndTagsLinkModel, ARShowcasesTagsModel
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.forms.models import model_to_dict
import logging

ar_showcase_detail_fields = ['app_uid', 'user_uid', 'arexperience_uid', 'showcase_uid',
                             'showcase_name', 'showcase_brief', 'showcase_icon', 'showcase_header', 'showcase_description']
ar_experience_detail_fields = ['name', 'arexperience_uid']
ar_experience_asset_detail_fields = ['android_json', 'android_bundle',
                                     'android_bundle_size', 'ios_json', 'ios_bundle', 'ios_bundle_size']


class ARExperienceView(APIView):
    authentication_classes = [AuthticationWithoutPackageId, ]
    throttle_classes = [VisitThrottle, ]

    def post(self, request, *args, **kwargs):
        ret = {'code': 200, 'msg': '', 'data': None}
        try:
            arexperience_uid = request._request.POST.get('arexperience_uid')
            cache_key = f"api_{arexperience_uid}_get_arexperience"
            data = cache.get(cache_key)
            if data is None:
                try:
                    arexperience_queryset = ARExperienceModel.objects.get(
                        arexperience_uid=arexperience_uid)
                    arexperience = model_to_dict(
                        arexperience_queryset, ar_experience_detail_fields)
                    arexperience_asset= ARExperienceAsset.objects.get(
                        arexperience_uid=arexperience_uid)
                    arexperience_asset = model_to_dict(
                        arexperience_asset, ar_experience_asset_detail_fields)
                    arexperience['arexperience_asset'] = arexperience_asset                    
                    data = arexperience                   
                    

                except ARExperienceModel.DoesNotExist or ARExperienceAsset.DoesNotExist:
                    arexperience = None
                    arexperience_asset = None 
            cache.set(cache_key, data, settings.API_CACHE_EXPIRED)
            ret['data'] = data
            return JsonResponse(ret, status=200)
        except Exception as e:
            logging.exception(e)
        return JsonResponse(ret)


class ARShowcaseView(APIView):
    authentication_classes = [Authtication, ]
    throttle_classes = [VisitThrottle, ]

    def post(self, request, *args, **kwargs):
        # respone dict
        ret = {'code': 200, 'msg': '', 'data': None}
        try:
            showcase_tag = request._request.POST.get('showcase_tag')
            showcase_status = request._request.POST.get('showcase_status', 1)

            showcase_uids = []
            if showcase_tag is not None:
                # get from cache when it is exsit. api_useruid_appuid_tag
                query_by_tag_cache_key = f"api_{request.user.user_uid}_{request.auth[0]}_{showcase_tag}_get_showcaseList"
                showcases = cache.get(query_by_tag_cache_key)
                if showcases is None:
                    all_tags_queryset = ARShowcasesAndTagsLinkModel.objects.filter(
                        app_uid=request.auth[0], user_uid=request.user.user_uid, tag_name=showcase_tag)
                    for showcase_uid in all_tags_queryset:
                        showcase_uids.append(showcase_uid.showcase_uid)
                    showcases = list(ARShowcasesCenterModel.objects.filter(app_uid=request.auth[0], user_uid=request.user.user_uid, showcase_uid__in=showcase_uids, showcase_status=showcase_status)
                                     .values('app_uid', 'user_uid', 'arexperience_uid',
                                             'showcase_uid', 'showcase_name', 'showcase_brief',
                                             'showcase_icon', 'showcase_not_index_tags'))
                    cache.set(query_by_tag_cache_key, showcases,
                              settings.API_CACHE_EXPIRED)
            else:
                # get from cache when it is exsit. api_useruid_appuid
                query_by_app_uid_cache_key = f"api_{request.user.user_uid}_{request.auth[0]}_get_showcaseList"
                showcases = cache.get(query_by_app_uid_cache_key)

                if showcases is None:
                    showcaseQuerysetList = ARShowcasesCenterModel.objects.filter(
                        app_uid=request.auth[0], user_uid=request.user.user_uid, showcase_status=showcase_status).values('app_uid', 'user_uid', 'arexperience_uid',
                                                                                                                         'showcase_uid', 'showcase_name', 'showcase_brief',
                                                                                                                         'showcase_icon',  'showcase_not_index_tags')
                    showcases = list(showcaseQuerysetList)
                    cache.set(query_by_app_uid_cache_key,
                              showcases, settings.API_CACHE_EXPIRED)
            ret['data'] = showcases

            return JsonResponse(ret, safe=False)
        except Exception as e:
            logging.exception(e)
        return JsonResponse(ret)


class ARShowcaseDetailView(APIView):
    authentication_classes = [Authtication, ]
    throttle_classes = [VisitThrottle, ]

    def post(self, request, *args, **kwargs):
        # respone dict
        ret = {'code': 200, 'msg': '', 'data': None}
        if 'showcase_uid' in request._request.POST:
            showcase_uid = request._request.POST.get('showcase_uid', None)
            query_showcase_detail_key = f"api_{request.user.user_uid}_{request.auth[0]}_{showcase_uid}_get_detail"
            showcase = cache.get(query_showcase_detail_key)
            if showcase is None:
                try:
                    showcase_queryset = ARShowcasesCenterModel.objects.get(
                        user_uid=request.user.user_uid, app_uid=request.auth[0], showcase_uid=showcase_uid,showcase_status=1)
                    showcase = model_to_dict(
                        showcase_queryset, ar_showcase_detail_fields)
                    arexperience_asset = ARExperienceAsset.objects.get(
                        arexperience_uid=showcase_queryset.arexperience_uid)
                    showcase['android_size'] = arexperience_asset.android_bundle_size
                    showcase['ios_size'] = arexperience_asset.ios_bundle_size

                    cache.set(query_showcase_detail_key, showcase,
                              settings.API_CACHE_EXPIRED)
                except ARShowcasesCenterModel.DoesNotExist:
                    showcase = None
            ret['data'] = showcase
            return JsonResponse(ret)
        ret['msg'] = 'Invalid showcase_uid'
        return JsonResponse(ret)


class ARShowcaseTagsView(APIView):
    authentication_classes = [Authtication, ]
    throttle_classes = [VisitThrottle, ]

    def post(self, request, *args, **kwargs):
        ret = {'code': 200, 'msg': '', 'data': None}
        query_showcase_tags_key = f"api_{request.user.user_uid}_{request.auth[0]}_get_tags"
        tags = cache.get(query_showcase_tags_key)
        if tags is None:
            tags = (list(ARShowcasesTagsModel.objects.filter(app_uid=request.auth[0], user_uid=request.user.user_uid).order_by('tag_sort_weight')
                         .values('tag_sort_weight', 'tag_name')))
            cache.set(query_showcase_tags_key, tags,
                      settings.API_CACHE_EXPIRED)

        ret['data'] = tags
        return JsonResponse(ret)


class ARShowcaseRecommends(APIView):
    authentication_classes = [Authtication, ]
    throttle_classes = [VisitThrottle, ]

    def post(self, request, *args, **kwargs):
        ret = {'code': 200, 'msg': '', 'data': None}
        try:
            query_showcase_recommend_key = f"api_{request.user.user_uid}_{request.auth[0]}_get_recommendList"
            recommends = cache.get(query_showcase_recommend_key)
            if recommends is None:
                recommends = list(ARShowcasesCenterModel.objects.filter(app_uid=request.auth[0], user_uid=request.user.user_uid, showcase_recommend=True, showcase_status=1)
                                  .values('app_uid', 'user_uid', 'arexperience_uid',
                                          'showcase_uid', 'showcase_name', 'showcase_brief',
                                          'showcase_icon', 'showcase_header', 'showcase_not_index_tags'))
                cache.set(query_showcase_recommend_key,
                          recommends, settings.API_CACHE_EXPIRED)
            ret['data'] = recommends
            return JsonResponse(ret, safe=False)
        except Exception as e:
            logging.exception(e)
        return JsonResponse(ret)


class ARShowcasePublicView(APIView):
    authentication_classes = [AuthticationWithoutPackageId, ]
    throttle_classes = [VisitThrottle, ]

    def post(self, request, *args, **kwargs):
        ret = {'code': 200, 'msg': '', 'data': None}
        query_by_app_uid_cache_key = f"api_{request.user.user_uid}_{request.auth[0]}_1_1_get_showcaseList"
        showcases = cache.get(query_by_app_uid_cache_key)
        if showcases is None:
            showcaseQuerysetList = ARShowcasesCenterModel.objects.filter(showcase_permission=1,
                                                                         showcase_status=1).values('app_uid', 'user_uid', 'arexperience_uid',
                                                                                                   'showcase_uid', 'showcase_name', 'showcase_brief',
                                                                                                   'showcase_icon',  'showcase_not_index_tags')
            showcases = list(showcaseQuerysetList)
            cache.set(query_by_app_uid_cache_key,
                      showcases, settings.API_CACHE_EXPIRED)
        ret['data'] = showcases
        return JsonResponse(ret)
