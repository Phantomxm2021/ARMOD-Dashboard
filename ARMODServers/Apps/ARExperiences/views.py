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

dashboard_project_detail_field = ['di','name','app_uid','status','description','create_time','update_time']
dashboard_project_asset_detail_field =['android_json','android_bundle','android_bundle_size','ios_json','ios_bundle','ios_bundle_size','create_time','update_time']
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

    def post(self, request, app_uid, arexperience_uid):
        """Upload AR experience resources"""
        try:
            projectname = request.POST.get('projectname')
            platform = request.POST.get('platform')
            filesIndex = ['arexperience', 'json']

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
            cache.delete(f"api_{arexperience_uid}_get_arexperience")
            return JsonResponse({'code': upload_response.status, 'message': 'The ARExperience Project is edited successfully!', 'data': data})
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
