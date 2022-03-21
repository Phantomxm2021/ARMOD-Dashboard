import json
import logging
from django.conf import settings
from django.core.cache import cache
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from Apps.Apiv2.utils import Authtication, VisitThrottle, AuthticationWithoutPackageId
from Apps.ARExperiences.models import ARExperienceModelV2,ARExperienceResourceV2
from Apps.Apiv2.serializer import GetARExperienceSerializer,GetARResourceSerializer,GetARExperienceDetailSerializer
from Apps.Apiv2.serializer import GetRecommendARExperienceSerializer
from Apps.TagManager.models import TagsModel
from Apps.TagManager.serializer import GetTagSerializer


class GetARResourcesView(APIView):
    authentication_classes = [AuthticationWithoutPackageId, ]
    throttle_classes = [VisitThrottle, ]
    def post(self, request, *args, **kwargs):
        ret = {'code':200,'msg':'Not data'}
        try:
            project_id = request._request.POST.get('project_id')
            cache_key = f"api_{project_id}_get_arresources"
            project_cache_key = f"api_{project_id}_get_arproject"

            project_data = cache.get(project_cache_key)
            if project_data is None:
                # arexperience_queryset = ARExperienceModelV2.objects.get(project_id=project_id,project_status=1)
                # Ignore project online state
                arexperience_queryset = ARExperienceModelV2.objects.get(project_id=project_id)
                cache.set(project_cache_key,arexperience_queryset,settings.API_CACHE_EXPIRED)
                project_data = arexperience_queryset
            
            data = cache.get(cache_key)
            if data is None:
                if (project_data is None or project_data.project_permission != 1) and project_data.user_uid != request.user.user_uid:
                    ret['msg'] = "You do'ot have permission."
                    data = {}
                else:
                    resource_quersets= ARExperienceResourceV2.objects.filter(project_id=project_id)
                    resource_serializer=   GetARResourceSerializer(data=resource_quersets,many=True)
                    resource_serializer.is_valid()
                    data = resource_serializer.data
                    cache.set(cache_key, data, settings.API_CACHE_EXPIRED)
            else:
                ret['msg'] = ''
            ret['data'] = data
            return JsonResponse(ret, status=200,safe=False)
        except Exception as e:
            logging.exception(e)
        return JsonResponse(ret)

class GetARExperienceDetailView(APIView):
    authentication_classes = [AuthticationWithoutPackageId, ]
    throttle_classes = [VisitThrottle, ]

    def post(self, request, *args, **kwargs):
        ret = {'code': 200, 'msg': '', 'data':{}}
        try:
            project_id = request._request.POST.get('project_id')
            cache_key = f"api_{project_id}_get_arexperience_detail"
            data = cache.get(cache_key)
            
            if data is None:
                arexperience_queryset = ARExperienceModelV2.objects.get(project_id=project_id,project_status=1)
                cache.set(cache_key, arexperience_queryset, settings.API_CACHE_EXPIRED)
                data = arexperience_queryset

            if data is None:
                pass
            else:
                if data.project_permission != 1 and data.user_uid != request.user.user_uid:
                    ret['msg'] = "You do'ot have permission."
                    data = {}
                else:
                    serializer = GetARExperienceDetailSerializer(data)
                    data = serializer.data
                    ret['msg'] = ''
                ret['data'] = data
            
            return JsonResponse(ret, status=200,safe=False)
        except Exception as e:
            logging.exception(e)
        return JsonResponse(ret)

# http://IP:PORT/api/v2/getarexperiencelist?page_size=2&page_num=1
class GetARExperiencesView(APIView):
    authentication_classes = [Authtication, ]
    throttle_classes = [VisitThrottle, ]
    def get(self,request,*args,**kwargs):
        ret = {'code': 200, 'msg': '', 'data':[]}
        try:
            user_uid = request.user.user_uid
            cache_key = f"api_{user_uid}_get_arexperience_page"
            data = cache.get(cache_key)
            if data is None:
                arexperience_queryset = ARExperienceModelV2.objects.filter(user_uid=user_uid,project_status=1,app_uid=self.request.auth[0]).order_by('-id')
                cache.set(cache_key, arexperience_queryset, settings.API_CACHE_EXPIRED)
                data = arexperience_queryset

            page_obj = ARExperiencesViewPageNumber()
            page_items = page_obj.paginate_queryset(queryset=data, request=request, view=self)
            serializer = GetARExperienceSerializer(data=page_items,many=True)
            serializer.is_valid()
            data = serializer.data
            ret['msg'] = ''
            ret['data'] = data
            return JsonResponse(ret, status=200,safe=False)
        except Exception as e:
            logging.exception(e)
        return JsonResponse(ret)

class ARExperiencesViewPageNumber(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size' 
    page_query_param = 'page_num'  
    max_page_size = None

class GetTagListView(APIView):
    authentication_classes = [AuthticationWithoutPackageId, ]
    throttle_classes = [VisitThrottle, ]

    def post(self, request, *args, **kwargs):
        ret = {'code': 200, 'msg': '', 'data':{}}
        query_project_tags_key = f"api_{request.user.user_uid}_{request.auth[0]}_get_tagList"
        tags = cache.get(query_project_tags_key)
        if tags is None:
            taglist_querysets = TagsModel.objects.filter(app_uid=request.auth[0],user_uid=request.user.user_uid).order_by('-tag_sort_weight')
            cache.set(query_project_tags_key, taglist_querysets,settings.API_CACHE_EXPIRED)
            tags = taglist_querysets

        serializer = GetTagSerializer(data=tags,many=True)
        serializer.is_valid()
        tags = serializer.data
        ret['data'] = tags
        return JsonResponse(ret)

class GetARExperienceRecommendList(APIView):
    authentication_classes = [AuthticationWithoutPackageId, ]
    throttle_classes = [VisitThrottle, ]

    def post(self, request, *args, **kwargs):
        ret = {'code': 200, 'msg': '', 'data': {}}
        try:
            query_project_recommend_key = f"api_{request.user.user_uid}_{request.auth[0]}_get_recommendList"
            recommends = cache.get(query_project_recommend_key)
            if recommends is None or len(recommends) == 0:
                recommend_querysets = ARExperienceModelV2.objects.filter(app_uid=request.auth[0],user_uid=request.user.user_uid,project_recommend=1,project_status=1).order_by('-project_weight')
                cache.set(query_project_recommend_key,recommend_querysets, settings.API_CACHE_EXPIRED)
                recommends = recommend_querysets
            serializer = GetRecommendARExperienceSerializer(data=recommends,many=True)
            serializer.is_valid()
            ret['data'] = serializer.data
            return JsonResponse(ret, safe=False)
        except Exception as e:
            logging.exception(e)
        return JsonResponse(ret)

# http://IP:PORT/api/v2/getarexperiencelist?page_size=2&page_num=1
class GetARExperiencePublicListView(APIView):
    authentication_classes = [AuthticationWithoutPackageId, ]
    throttle_classes = [VisitThrottle, ]

    def get(self, request, *args, **kwargs):
        ret = {'code': 200, 'msg': '', 'data':[]}
        query_by_app_uid_cache_key = f"api_{request.user.user_uid}_{request.auth[0]}_get_arexperiencepubliclist"
        public_project = cache.get(query_by_app_uid_cache_key)
        if public_project is None:
            public_project_querysets = ARExperienceModelV2.objects.filter(project_permission=1,project_status=1).order_by("-id")
            cache.set(query_by_app_uid_cache_key,public_project_querysets, settings.API_CACHE_EXPIRED)
            public_project = public_project_querysets
        try:
            page_obj = ARExperiencesViewPageNumber()
            page_items = page_obj.paginate_queryset(queryset=public_project, request=request, view=self)
            serializer = GetARExperienceSerializer(data=page_items,many=True)
            serializer.is_valid()
            public_project = serializer.data
            ret['data'] = public_project
        except:
            ret['data'] = []
       
        return JsonResponse(ret)

class GetARexperienceByTagsListView(APIView):
    authentication_classes = [AuthticationWithoutPackageId, ]
    throttle_classes = [VisitThrottle, ]
    def post(self, request, *args, **kwargs):
        ret = {'code': 200, 'msg': '', 'data':{}}
        project_tags =json.loads(request._request.POST.get('project_tags'))

        query_by_app_uid_cache_key = f"api_{request.user.user_uid}_{request.auth[0]}_get_arexperiencebytagslist"
        projects = cache.get(query_by_app_uid_cache_key)
        if projects is None:
            project_querysets = ARExperienceModelV2.objects.filter(user_uid=request.user.user_uid,app_uid=request.auth[0],project_status=1,project_tags__contains=project_tags).order_by("-id")
            cache.set(query_by_app_uid_cache_key,project_querysets,settings.API_CACHE_EXPIRED)
            projects = project_querysets
        serializer = GetARExperienceSerializer(data=projects,many=True)
        serializer.is_valid()
        ret['data'] = serializer.data
        return JsonResponse(ret)