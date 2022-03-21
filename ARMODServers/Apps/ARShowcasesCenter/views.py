import os
import json
from django.shortcuts import render
from django.template.loader import render_to_string
from django.conf import settings
from django.core.cache import cache
from django.views.generic import View
from utils.mixin import LoginRequiredMixin
from .models import ARShowcasesCenterModel, ARShowcasesAndTagsLinkModel, ARShowcasesTagsModel
from django.http import JsonResponse
from Apps.ARExperiences.models import ARExperienceModel
from Apps.Applications.models import ApplicationsModel
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage
from django.conf import settings
import logging
from utils.create_md5 import create_md5
# Create your views here.


class ARShowcasesCenterView(LoginRequiredMixin, View):
    def get(self, request, app_uid):
        user = request.user
        query_key = f"{user.user_uid}_{app_uid}_get_showcaseList"
        arshowcase_list = cache.get(query_key)
        if arshowcase_list is None:
            arshowcase_list = ARShowcasesCenterModel.objects.filter(
                app_uid=app_uid).order_by('id')
            cache.set(query_key, arshowcase_list, settings.API_CACHE_EXPIRED)

        page = int(request.GET.get("page", 1))
        paginator = Paginator(arshowcase_list, 10)
        arshowcase_pages = paginator.get_page(page)

        all_preset_tags = ARShowcasesTagsModel.objects.filter(
            app_uid=app_uid, user_uid=user.user_uid)
        return render(request,  'dashboard/arshowcasecenter.html', {'arshowcase_list': arshowcase_pages,
                                                                    'user': user,
                                                                    'app_uid': app_uid,
                                                                    'all_preset_tags': all_preset_tags})


class ARShowcasesCenterProjectPostView(LoginRequiredMixin, View):
    def post(self, request):
        """创建Case"""
        action = request.POST.get('action')
        app_uid = request.POST.get('app_uid')
        showcase_uid = request.POST.get('showcase_uid')

        showcase_name = request.POST.get('showcase_name')
        showcase_description = request.POST.get('showcase_description')
        showcase_permission = request.POST.get('showcase_permission')
        showcase_status = request.POST.get('showcase_status')
        showcase_recommend = request.POST.get('showcase_recommend')

        query_key = f"{request.user.user_uid}_{app_uid}_get_showcaseList"
        query_showcase_detail_key = f"{request.user.user_uid}_{app_uid}_{showcase_uid}_get_detail"

        if 'create_showcase' in action:
            try:
                arexperience_uid = request.POST.get('arexperience_uid')
                showcase_tags = json.loads(request.POST.get('showcase_tags'))
                showcase_brief = request.POST.get('showcase_brief')

                try:
                    arexperience_uid = int(arexperience_uid)
                except Exception as e:
                    logging.exception(e)
                    return JsonResponse({'code': 201, 'message': 'Incomplete data'})

                if not all([showcase_name, app_uid]) or type(arexperience_uid) is str:
                    return JsonResponse({'code': 201, 'message': 'Incomplete data'})

                from utils.generate_random_pid import generate_unique_id
                unique_pid = generate_unique_id(showcase_name)
                try:
                    app = ARShowcasesCenterModel.objects.get(
                        showcase_uid=unique_pid)
                except ARShowcasesCenterModel.DoesNotExist:
                    app = None

                if app is not None:
                    return JsonResponse({'code': 201, 'message': 'The Showcase Name was used'})

                try:
                    arexperience = ARExperienceModel.objects.get(
                        app_uid=app_uid, arexperience_uid=arexperience_uid)
                except ARExperienceModel.DoesNotExist:
                    arexperience = None

                if arexperience is None:
                    return JsonResponse({'code': 201, 'message': 'Incorrect ARExperience UID!'})

                ARShowcasesCenterModel.objects.create(app_uid=app_uid,
                                                      arexperience_uid=arexperience_uid,
                                                      showcase_name=showcase_name,
                                                      user_uid=self.request.user.user_uid,
                                                      showcase_uid=unique_pid,
                                                      showcase_description=showcase_description,
                                                      showcase_status=0,
                                                      showcase_brief=showcase_brief,
                                                      showcase_permission=showcase_permission,
                                                      showcase_recommend = showcase_recommend,
                                                      showcase_not_index_tags=showcase_tags['showcase_tags'])
                for tag in showcase_tags['showcase_tags']:
                    try:
                        ARShowcasesAndTagsLinkModel.objects.update_or_create(
                            showcase_uid=unique_pid, user_uid=request.user.user_uid, app_uid=app_uid, tag_name=tag)
                    except BaseException as e:
                        print(repr(e))
                        continue

                # modify child project count
                app_QuerySet = ApplicationsModel.objects.filter(
                    app_uid=app_uid).first()
                app_child_project_count = app_QuerySet.child_project + 1
                app_QuerySet.child_project = app_child_project_count
                app_QuerySet.save()
                cache.delete(query_key)
            except Exception as e:
                logging.exception(e)
                return JsonResponse({'code': 201, 'message':'Create failed'})
        elif 'get_showcase' in action:
            showcase_dict = cache.get(query_showcase_detail_key)
            if showcase_dict is None:
                showcase = ARShowcasesCenterModel.objects.get(
                    app_uid=app_uid, showcase_uid=showcase_uid)
                showcase_tags_filter_queryset = ARShowcasesAndTagsLinkModel.objects.filter(
                    showcase_uid=showcase_uid)
                showcase_dict = {
                    'arexperience_uid': showcase.arexperience_uid,
                    'showcase_uid': showcase.showcase_uid,
                    'showcase_name': showcase.showcase_name,
                    'showcase_status': showcase.showcase_status,
                    'showcase_permission': showcase.showcase_permission,
                    'showcase_icon': showcase.showcase_icon,
                    'showcase_header': showcase.showcase_header,
                    'showcase_description': showcase.showcase_description,
                    'showcase_brief': showcase.showcase_brief,
                    'showcase_recommend':showcase.showcase_recommend,
                  
                }

                showcase_tags = []
                for tag_quertset in showcase_tags_filter_queryset:
                    showcase_tags.append(tag_quertset.tag_name)
                showcase_dict['showcase_tags'] = showcase_tags
                cache.set(query_showcase_detail_key, showcase_dict,
                          settings.API_CACHE_EXPIRED)

            return JsonResponse({'code': 200, 'message': 'success', 'data': {"showcase": showcase_dict}})
        elif 'save_change' in action:
            showcase_arexperience_uid = request.POST.get('showcase_arexperience_uid')
            showcase_permission = request.POST.get('showcase_permission')
            try:
                arexperience = ARExperienceModel.objects.get(arexperience_uid=showcase_arexperience_uid)
            except ARExperienceModel.DoesNotExist:
                return JsonResponse({'code': 201, 'message': 'ARExperience Does Not Exist'})
            
            showcase_brief = request.POST.get('showcase_brief')
            showcase_tags = json.loads(request.POST.get('showcase_tags'))
            showcase = ARShowcasesCenterModel.objects.get(
                app_uid=app_uid, showcase_uid=showcase_uid)
            from utils.aliyun_utility import AliyunObjectStorage
            aliyunStorage = AliyunObjectStorage()

            assets_save_folder = os.path.join(
                str(self.request.user.user_uid), app_uid, 'Showcases', showcase_uid)
            assets_save_folder = assets_save_folder.replace('\\', '/')
            showcase_icon = request.FILES.get('showcase_icon_img')
            if showcase_icon is not None:
                oss_path = "%s/%s" % (assets_save_folder, f"{create_md5(showcase_icon.name).replace('.jpg', '')}.jpg")                                
                aliyunStorage._save(
                    name=oss_path, content=showcase_icon.read(), progress_callback=None)
                showcase.showcase_icon = aliyunStorage.url(oss_path)

            showcase_header = request.FILES.get('showcase_header_img')
            if showcase_header is not None:
                oss_path = "%s/%s" % (assets_save_folder, showcase_header.name)
                showcase.showcase_header = aliyunStorage.url(oss_path)
                aliyunStorage._save(
                    name=oss_path, content=showcase_header.read(), progress_callback=None)

            showcase.showcase_name = showcase_name
            showcase.showcase_status = showcase_status
            showcase.showcase_permission = showcase_permission
            showcase.showcase_description = showcase_description
            showcase.showcase_brief = showcase_brief
            showcase.arexperience_uid = showcase_arexperience_uid
            showcase.showcase_recommend = showcase_recommend
            

            if showcase_tags['tags_has_changed'] == True:
                ARShowcasesAndTagsLinkModel.objects.filter(
                    user_uid=request.user.user_uid, app_uid=app_uid, showcase_uid=showcase_uid).delete()
                for tag in showcase_tags['showcase_tags']:
                    try:
                        ARShowcasesAndTagsLinkModel.objects.update_or_create(
                            user_uid=request.user.user_uid, app_uid=app_uid, showcase_uid=showcase_uid, tag_name=tag)
                    except BaseException as e:
                        print(e)
                        continue
                
                showcase.showcase_not_index_tags =showcase_tags['showcase_tags']
          
            showcase.save()

            cache.delete(query_showcase_detail_key)
            cache.delete(query_key)
        elif 'delete_showcase' in action:
            showcase = ARShowcasesCenterModel.objects.get(
                showcase_uid=showcase_uid, app_uid=app_uid)
            from utils.aliyun_utility import AliyunObjectStorage
            aliyunStorage = AliyunObjectStorage()

            assets_save_folder = os.path.join(
                str(self.request.user.user_uid), app_uid, 'Showcases', showcase_uid)
            assets_save_folder = assets_save_folder.replace('\\', '/')
            if showcase.showcase_icon is not '':
                oss_file_path = showcase.showcase_icon[len(
                    settings.OSS_BASE_URL)+1:]
                aliyunStorage.delete(oss_file_path)

            if showcase.showcase_header is not '':
                oss_file_path = showcase.showcase_header[len(
                    settings.OSS_BASE_URL)+1:]
                aliyunStorage.delete(oss_file_path)

            ARShowcasesAndTagsLinkModel.objects.filter(
                showcase_uid=showcase_uid).delete()

            # modify child project count
            app_QuerySet = ApplicationsModel.objects.filter(
                app_uid=app_uid).first()
            app_child_project_count = app_QuerySet.child_project - 1
            app_QuerySet.child_project = app_child_project_count
            app_QuerySet.save()

            showcase.delete()
            cache.delete(query_key)

        return JsonResponse({'code': 200, 'message': 'success'})


class ARShowcaseTagsView(LoginRequiredMixin, View):
    def get(self, request):
        app_uid = request.GET.get('app_uid')
        query_tag_key = f"{request.user.user_uid}_{app_uid}_get_tagList"
        all_preset_tags = cache.get(query_tag_key)
        if all_preset_tags is None:
            all_query_set_tags = ARShowcasesTagsModel.objects.filter(
                app_uid=app_uid, user_uid=request.user.user_uid)
            all_preset_tags = (all_query_set_tags.values(
                'tag_reference_weight', 'tag_sort_weight', 'tag_name'))
        return JsonResponse({'code': 200, 'message': 'success', 'data': list(all_preset_tags)})

    def post(self, request):
        action = request.POST.get('action')
        app_uid = request.POST.get('app_uid')
        tag_name = request.POST.get('tag_name')
        query_tag_key = f"{request.user.user_uid}_{app_uid}_get_tagList"
        cache.delete(query_tag_key)

        if 'create_tag' in action:
            showcase_tag_weight = request.POST.get('showcase_tag_weight')
            try:
                tag_query_set = ARShowcasesTagsModel.objects.get(
                    user_uid=request.user.user_uid, app_uid=app_uid, tag_name=tag_name)
            except ARShowcasesTagsModel.DoesNotExist:
                tag_query_set = None

            if tag_query_set is None:
                tag_query_set = ARShowcasesTagsModel.objects.create(
                    user_uid=request.user.user_uid,
                    app_uid=app_uid,
                    tag_name=tag_name,
                    tag_sort_weight=showcase_tag_weight)
                all_preset_tags = ARShowcasesTagsModel.objects.filter(
                    app_uid=app_uid, user_uid=request.user.user_uid).order_by('tag_sort_weight')
                modal_html_txt = render_to_string(
                    'dashboard/showcase_tags_modal_table.html', {'all_preset_tags': all_preset_tags})
                all_preset_tags_cacge = all_preset_tags.values(
                    'tag_sort_weight', 'tag_name')
                return JsonResponse({'code': 200, 'message': 'success', 'data': {'modal': modal_html_txt}})

            return JsonResponse({'code': 201, 'message': 'The tag name was exist!'})
        elif 'delete_tag' in action:
            try:
                tag_query_set = ARShowcasesTagsModel.objects.get(
                    user_uid=request.user.user_uid, app_uid=app_uid, tag_name=tag_name)
                tag_query_set.delete()
                ARShowcasesAndTagsLinkModel.objects.filter(
                    app_uid=app_uid, user_uid=request.user.user_uid, tag_name=tag_name).delete()
                all_preset_tags = ARShowcasesTagsModel.objects.filter(
                    app_uid=app_uid, user_uid=request.user.user_uid)
                modal_html_txt = render_to_string(
                    'dashboard/showcase_tags_modal_table.html', {'all_preset_tags': all_preset_tags})
                return JsonResponse({'code': 200, 'message': 'success', 'data': {'modal': modal_html_txt}})
            except ARShowcasesTagsModel.DoesNotExist:
                tag_query_set = None
            return JsonResponse({'code': 201, 'message': 'The tag name was not exist!'})
