import os
from datetime import datetime
from django.db.models import Q
from django.urls import reverse
from django.conf import settings
from django.shortcuts import render
from django.core.cache import cache
from django.views.generic import View
from utils.mixin import LoginRequiredMixin
from utils.aliyun_utility import AliyunObjectStorage
from django.http import JsonResponse, HttpResponse, FileResponse
from Apps.ARExperiences.models import ARExperienceModel, ARExperienceAsset
from django.forms.models import model_to_dict

# Create your views here.
aliyunStorage = AliyunObjectStorage()

<<<<<<< HEAD
dashboard_project_detail_field = ['project_id','project_name','app_uid','project_brief','project_status',
                                  'project_permission','project_description','project_recommend','project_tags',
                                  'project_weight','project_icon','create_time','update_time',
                                  'project_header','project_preview']

dashboard_project_asset_detail_field =['project_id','json_url','bundle_url','bundle_size','platform_type',
                                       'create_time','update_time']

=======
dashboard_project_detail_field = ['di','name','app_uid','status','description','create_time','update_time']
dashboard_project_asset_detail_field =['android_json','android_bundle','android_bundle_size','ios_json','ios_bundle','ios_bundle_size','create_time','update_time']
>>>>>>> parent of 7df37a3 (upgrade to 1.0-alpha.2)
class DashboardProjectListView(LoginRequiredMixin, View):
    def get(self, request, app_uid, arexperience_uid):
        """Show ARExperiences project detail"""
        query_key = f"{request.user.user_uid}_{app_uid}_{arexperience_uid}"
        data = cache.get(query_key)
        if data is None:
            arexperience = ARExperienceModel.objects.get(app_uid=app_uid, arexperience_uid=arexperience_uid)           
            data = model_to_dict(arexperience,dashboard_project_detail_field)     
            data['create_time']=arexperience.create_time
            data['update_time']=arexperience.update_time
            try:
                assets = ARExperienceAsset.objects.get(arexperience_uid=arexperience.arexperience_uid)               
                data['assets'] =  model_to_dict(assets,dashboard_project_asset_detail_field)
            except:
                assets = None
            cache.set(query_key,data,settings.API_CACHE_EXPIRED)      
        return JsonResponse({'code': 200, 'message': 'Success', 'data': data})

<<<<<<< HEAD
    def post(self, request):
        response = {}
        method_type = request.POST.get('method_type')
        if method_type == 'UpdateProject':
            response = self.update_project(request)
        elif method_type == 'UploadARResources':
            response = self.upload_ar_resources(request)

        return JsonResponse(response)

    def update_project(self,request):
        ret = {'code':200,'message':None,'data':None}
        project_name = request.POST.get('project_name')   
        project_id = request.POST.get('project_id')   
        app_uid = request.POST.get('app_uid')   
        if not all([app_uid,project_id,project_name]):
            ret['code'] = 201
            ret['message'] = 'Incomplete data'
            return ret
        try:
            arexperience = ARExperienceModelV2.objects.get(app_uid=app_uid,project_id=project_id)
        except ARExperienceModelV2.DoesNotExist:
            arexperience = None
            ret['code'] = 201
            ret['message'] = 'The ARExperience is not exsit!'
            return ret
        if arexperience.project_name != project_name:
            arexperience.project_name = project_name

       
        project_description = request.POST.get('project_description')
        project_support_url = request.POST.get('project_support_url')
        project_brief = request.POST.get('project_brief')
        project_weight = request.POST.get('project_weight')
        project_permission = request.POST.get('project_permission')
        project_status = request.POST.get('project_status')
        project_recommend = request.POST.get('project_recommend')
        project_header= request.FILES.get("project_header")
        project_icon= request.FILES.get("project_icon")
        project_preview_will_delete_id = json.loads(request.POST.get('project_preview_delete_id'))
        project_preview_count = int(request.POST.get("project_preview_count"))
        project_tags = json.loads(request.POST.get('project_tags'))


        if project_description is not None:
            arexperience.project_description = project_description
        if project_support_url is not None:
            arexperience.project_support_url = project_support_url
        if project_brief is not None:
            arexperience.project_brief = project_brief
        if project_weight is not None:
            arexperience.project_weight = project_weight
        if project_permission is not None:
            arexperience.project_permission = project_permission
        if project_status is not None:
            arexperience.project_status = project_status
        if project_recommend is not None:
            arexperience.project_recommend = project_recommend

        arexperience.project_tags = project_tags
            

        if project_header is not None:
            delete_img_from_oss(request.user.user_uid,app_uid,arexperience.project_id,arexperience.project_header)
            project_header_image_url = save_image_to_oss(request.user.user_uid,app_uid,arexperience.project_id,project_header,custom_name="%s_banner" %(project_name))
            arexperience.project_header  = project_header_image_url

        if project_icon is not None:
            delete_img_from_oss(request.user.user_uid,app_uid,arexperience.project_id,arexperience.project_icon)
            project_icon_image_url = save_image_to_oss(request.user.user_uid,app_uid,arexperience.project_id,project_icon,custom_name="%s_icon"%(project_name))
            arexperience.project_icon  = project_icon_image_url

        if project_preview_will_delete_id is not None and len(project_preview_will_delete_id)>0:
            imgs = json.loads(arexperience.project_preview)
            duplicate_imgs = json.loads(arexperience.project_preview)
            for img_idx in range(0,len(project_preview_will_delete_id)):
                idx = project_preview_will_delete_id[img_idx]
                will_remove_img = imgs[idx]
                delete_img_from_oss(request.user.user_uid,app_uid,project_id,will_remove_img)
                duplicate_imgs.remove(will_remove_img)
           
            arexperience.project_preview = json.dumps(duplicate_imgs)


        if project_preview_count > 0:
            if len(arexperience.project_preview)>0:
                preview_img_url = json.loads(arexperience.project_preview)
            else:
                preview_img_url = []
            for idx in range(0,project_preview_count):
                preview_img = request.FILES.get('project_preview_%s' % (idx))
                project_preview_image_url = save_image_to_oss(request.user.user_uid,app_uid,arexperience.project_id,preview_img)
                preview_img_url.append(project_preview_image_url)
            
            arexperience.project_preview  = json.dumps(preview_img_url)


        try:
            arexperience.save()
        except:
            ret['code'] = 201
            ret['message'] = 'Duplicate project name'
            return ret 
        query_key = f"{request.user.user_uid}_{app_uid}_{project_id}"
        query_app_uid_key = f"{request.user.user_uid}_{app_uid}"
        cache.delete(query_app_uid_key)
        cache.delete(query_key)       

        cache.delete(f"api_{project_id}_get_arexperience_detail")
        cache.delete(f"api_{request.user.user_uid}_get_arexperience_page")
        cache.delete(f"api_{request.user.user_uid}_{app_uid}_get_arexperiencepubliclist")
        cache.delete(f"api_{request.user.user_uid}_{app_uid}_get_recommendList")
        query_by_app_uid_cache_key = f"api_{request.user.user_uid}_{app_uid}_get_arexperiencebytagslist"
        cache.delete(query_by_app_uid_cache_key)

        ret['code'] = 200
        ret['message'] = 'Success'
        return ret

    def upload_ar_resources(self,request):
        """Upload ARExperiences"""
        try:
            app_uid = request.POST.get('app_uid')
            project_id = request.POST.get('project_id')
            platform = request.POST.get('platform')
            filesIndex = ['arexperience', 'json'] 
=======
    def post(self, request, app_uid, arexperience_uid):
        """Upload AR experience resources"""
        try:
            projectname = request.POST.get('projectname')
            platform = request.POST.get('platform')
            filesIndex = ['arexperience', 'json']

>>>>>>> parent of 7df37a3 (upgrade to 1.0-alpha.2)
            files = []
            file_size = 0
            upload_response = ''

            for fileidx in filesIndex:
                files.append(request.FILES.get(fileidx))
            user_uid = request.user.user_uid
            assets_save_folder = os.path.join(
                str(user_uid), settings.AREXPERIENCE_URL, app_uid, arexperience_uid, platform)

            assets_save_folder = assets_save_folder.replace('\\', '/')
            arexperience_assets = ARExperienceAsset.objects.get(
                arexperience_uid=arexperience_uid)

            for file in files:
                oss_path = "%s/%s" % (assets_save_folder, file.name)
                if 'iOS' in platform and 'json' in file.name:
                    arexperience_assets.ios_json = os.path.join(
                        settings.OSS_BASE_URL, oss_path)
                elif 'iOS' in platform and 'arexperience' in file.name:
                    arexperience_assets.ios_bundle = os.path.join(
                        settings.OSS_BASE_URL, oss_path)
                elif 'Android' in platform and 'json' in file.name:
                    arexperience_assets.android_json = os.path.join(
                        settings.OSS_BASE_URL, oss_path)
                elif 'Android' in platform and 'arexperience' in file.name:
                    arexperience_assets.android_bundle = os.path.join(
                        settings.OSS_BASE_URL, oss_path)

                file_size += file.size

                data_bytes = file.read()
                upload_response = aliyunStorage._save(
                    name=oss_path, content=data_bytes, progress_callback=percentage)

            if 'iOS' in platform:
                arexperience_assets.ios_bundle_size = round(file_size/1048576,2)
            elif 'Android' in platform:
                arexperience_assets.android_bundle_size = round(file_size/1048576,2)

            arexperience_assets.save()

            arexperience = ARExperienceModel.objects.get(
                app_uid=app_uid, arexperience_uid=arexperience_uid)
            arexperience.save()

            data = {
                'ios_json': arexperience_assets.ios_json,
                'ios_bundle': arexperience_assets.ios_bundle,
                'android_json': arexperience_assets.android_json,
                'android_bundle': arexperience_assets.android_bundle,
                'create_time': arexperience.create_time,
                'update_time': arexperience.update_time,
            }
            query_key = f"{user_uid}_{app_uid}_{arexperience_uid}"
            query_app_uid_key = f"{user_uid}_{app_uid}"
            api_query_by_app_uid_cache_key = f"api_{request.user.user_uid}_{app_uid}_get_showcaseList"
            api_query_arexperience=f"api_{request.user.user_uid}_{app_uid}_{arexperience_uid}_get_arexperience"
            cache.delete(api_query_by_app_uid_cache_key)
            cache.delete(api_query_arexperience)
            cache.delete(query_app_uid_key)
            cache.delete(query_key)
<<<<<<< HEAD
            
            query_by_app_uid_cache_key = f"api_{request.user.user_uid}_{app_uid}_get_arexperiencebytagslist"
            cache.delete(query_by_app_uid_cache_key)
            cache.delete(f"api_{project_id}_get_arexperience_detail")
            cache.delete(f"api_{request.user.user_uid}_get_arexperience_page")
            cache.delete(f"api_{project_id}_get_arresources")
            public_project_list_cache_key = f"api_{request.user.user_uid}_{app_uid}_get_arexperiencepubliclist"
            cache.delete(public_project_list_cache_key)
            
            return  {'code': upload_response.status, 'message': 'The ARExperience Project is edited successfully!', 'data': data}
=======
            cache.delete(f"api_{arexperience_uid}_get_arexperience")
            return JsonResponse({'code': upload_response.status, 'message': 'The ARExperience Project is edited successfully!', 'data': data})
>>>>>>> parent of 7df37a3 (upgrade to 1.0-alpha.2)
        except Exception as e:
            print(e)
            return JsonResponse({'code': 201, 'message': e.__str__()})


class DashbaordARExperienceUpdateView(LoginRequiredMixin,View):
    def post(self, request, app_uid, arexperience_uid):
        """Update ARExperience project"""
        ret = {'code':200,'message':None,'data':None}
        projectname = request.POST.get('projectname')                 
        if not all([app_uid,arexperience_uid,projectname]):
            ret['code'] = 201
            ret['message'] = 'Incomplete data'
            return JsonResponse(ret)


        try:
            arexperience = ARExperienceModel.objects.get(app_uid=app_uid,arexperience_uid=arexperience_uid)
        except ARExperienceModel.DoesNotExist:
            arexperience = None
            ret['code'] = 201
            ret['message'] = 'The ARExperience is not exsit!'
            return JsonResponse(ret)
        
        arexperience.name = projectname
        arexperience.save()

        ret['code'] = 200
        ret['message'] = 'Success!!!'
        ret['data'] = model_to_dict(arexperience,dashboard_project_detail_field)
        ret['data']['create_time'] = arexperience.create_time
        ret['data']['update_time'] = arexperience.update_time
        query_key = f"{request.user.user_uid}_{app_uid}_{arexperience_uid}"
        query_app_uid_key = f"{request.user.user_uid}_{app_uid}"
        api_query_by_app_uid_cache_key = f"api_{request.user.user_uid}_{app_uid}_get_showcaseList"
        api_query_arexperience=f"api_{request.user.user_uid}_{app_uid}_{arexperience_uid}_get_arexperience"
        cache.delete(api_query_by_app_uid_cache_key)
        cache.delete(api_query_arexperience)
        cache.delete(query_app_uid_key)
        cache.delete(query_key)       
        cache.delete(f"api_{arexperience_uid}_get_arexperience")
        return JsonResponse(ret)
        

def percentage(consumed_bytes, total_bytes):
    if total_bytes:
        rate = int(100 * (float(consumed_bytes) / float(total_bytes)))
        print('\r{0}% '.format(rate), end='')
