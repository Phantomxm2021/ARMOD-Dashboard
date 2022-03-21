from struct import pack
from django.conf import settings
from django.core.cache import cache
from django.http import JsonResponse
from django.views.generic import View
from utils.mixin import LoginRequiredMixin
from django.shortcuts import render
from Apps.Applications.models import ApplicationsModelV2
from Apps.ARExperiences.models import ARExperienceModelV2, ARExperienceResourceV2
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from django.core.paginator import Paginator
import os
import json
from utils.create_md5 import create_md5
from django.db.models import Q
# Create your views here.

default_image_url ='/static/img/theme/logo.jpg'

class DashboardApplicationListView(LoginRequiredMixin, View):
    def get(self, request):
        """获取APP列表"""
        user = request.user
        app_list = cache.get(f"{user.user_uid}_get_applist")
        if app_list is None:
            app_list = ApplicationsModelV2.objects.filter(user_uid=user.user_uid).order_by('-create_time')
            cache.set(f"{user.user_uid}_get_applist",app_list,settings.API_CACHE_EXPIRED)
        page = int(request.GET.get("page", 1))
        paginator = Paginator(app_list, 12)
        page = request.GET.get('page')
        apps = paginator.get_page(page)
        render_page = request.GET.get("render", True)
        if render_page:
            return render(request, 'dashboard/application_list.html', {'applist': apps,'user':user})
        else:
            return JsonResponse(apps,status=200)

    def post(self, request):
        method = request.POST.get('method_type')
        response = {}
        if method == 'CreateApp':
            response=self.create(request)
        return JsonResponse(response)
    
    def create(self,request):
        """创建APP"""
        name = request.POST.get('app_name')
    
        packageid = request.POST.get('packageid')
          
        description = request.POST.get('project_description')
        if not all([name, packageid]):
            return {'code': 201, 'message': 'Incomplete data'}

        apps = ApplicationsModelV2.objects.filter(Q(packageid=packageid)|Q(name=name))
        if len(apps) > 0:
            return {'code': 201, 'message': 'The Package Name was used'}

        # 使用Packageid为该应用生成Token用于验证
        serializer = Serializer(settings.SECRET_KEY, 8640000000)
        token = {'packageid': packageid,'user_uid':request.user.user_uid}
        token = serializer.dumps(token)  # bytes
        token = token.decode('utf8')  # 解码, str
        
        from utils.generate_random_pid import generate_unique_id
        app_uid = str(generate_unique_id(packageid))
        
        app_icon_image = request.FILES.get('app_icon_image')
        if app_icon_image is not None:
            assets_save_folder = os.path.join(
                str(self.request.user.user_uid), app_uid, 'Showcases', name)
            assets_save_folder = assets_save_folder.replace('\\', '/')
            oss_path = "%s/%s" % (assets_save_folder, f"{create_md5(app_icon_image.name).replace('.jpg', '')}.jpg")
            from utils.aliyun_utility import AliyunObjectStorage
            aliyunStorage = AliyunObjectStorage()
            aliyunStorage._save(name=oss_path, content=app_icon_image.read(), progress_callback=None)
            app_icon_image_url = aliyunStorage.url(oss_path)
        else:
            app_icon_image_url = "%s%s"%(settings.BASE_WEBSITE_URL,default_image_url)
        ApplicationsModelV2.objects.create(app_uid=app_uid,
                                         name=name,
                                         app_icon_image=app_icon_image_url,
                                         packageid=packageid,
                                         user_uid=request.user.user_uid,
                                         token=token,
                                         description=description)        
        cache.delete(f"{request.user.user_uid}_get_applist")
        return {'code': 200, 'message': 'success'}
   
class DashboardApplicationDeleteView(LoginRequiredMixin, View):
    def post(self, request):
        """删除App"""
        app_uid = request.POST.get('app_uid')
        apps = ApplicationsModelV2.objects.filter(app_uid=app_uid)
        if len(apps) == 0:
            return JsonResponse({'code': 201, 'message': 'Incorrect package name'})
        for app in apps:
            if app.child_project != 0:
                return JsonResponse({'code': 201, 'message': 'You cannot delete Application. Because the application is not an empty application.'})
            app.delete()        
        cache.delete(f"{request.user.user_uid}_get_applist")
        return JsonResponse({'code': 200, 'message': 'Success'})

class DashboardApplicationProjectListView(LoginRequiredMixin, View):
    def get(self, request, app_uid):
        """用于显示App内的项目列表"""        
        arexperience_project = cache.get(f"{request.user.user_uid}_{app_uid}_get_arexperienceList")
        if arexperience_project is None:
            arexperience_project = ARExperienceModelV2.objects.filter(app_uid=app_uid).order_by('-create_time')
            cache.set(f"{request.user.user_uid}_get_projectList",arexperience_project,settings.API_CACHE_EXPIRED)
        paginator = Paginator(arexperience_project, 24)
        page = int(request.GET.get("page", 1))
        arexperience_project_pages = paginator.get_page(page)
        appinfo = ApplicationsModelV2.objects.get(app_uid=app_uid)
        return render(request, 'dashboard/arexperience_list.html', {'arexperience_projects': arexperience_project_pages, 'appinfo': appinfo})

    def post(self, request,app_uid):
        method = request.POST.get('method_type')
        response = {}
        if method == 'CreateProject':
            response = self.create_project(request)
        elif method == 'UpdateApp':
            response = self.update_app(request)
        elif method == "DeleteApp":
            response = self.delete_app(request)
        elif method == 'DeleteProject':
            response = self.delete_project(request)

        return JsonResponse(response)

    def create_project(self,request):
        """创建项目"""
        try:
            app_uid = request.POST.get('app_uid')
            project_name = request.POST.get('project_name')
            project_description = request.POST.get('project_description',"")
            
            if not all([app_uid,project_name]):
                return {'code': 201, 'message': 'Incomplete data'}

            projects = ARExperienceModelV2.objects.filter(project_name=project_name, app_uid=app_uid)
            if len(projects) > 0:
                return {'code': 201, 'message': 'The Package Name was used'}

            from utils.generate_random_pid import generate_unique_id
            arexperience = ARExperienceModelV2.objects.create(project_id=generate_unique_id(project_name),
                                                            project_name=project_name,
                                                            app_uid=app_uid,
                                                            user_uid=self.request.user.user_uid,
                                                            project_description=project_description,
                                                            project_header ="%s%s"%(settings.BASE_WEBSITE_URL,default_image_url),
                                                            project_icon="%s%s"%(settings.BASE_WEBSITE_URL,default_image_url))
            arexperience.save()

            arexperienceAsset_iOS = ARExperienceResourceV2.objects.create(project_id=arexperience.project_id,
                                                                        platform_type="iOS")
            arexperienceAsset_iOS.save()

            arexperienceAsset_Android = ARExperienceResourceV2.objects.create(project_id=arexperience.project_id,
                                                                        platform_type="Android")
            arexperienceAsset_Android.save()
            
            arexperienceAsset_WSA = ARExperienceResourceV2.objects.create(project_id=arexperience.project_id,
                                                                        platform_type="WSA")
            arexperienceAsset_WSA.save()

            app = ApplicationsModelV2.objects.get(app_uid=app_uid)
            app.child_project = app.child_project + 1
            app.save()

            cache.delete(f"{request.user.user_uid}_{app_uid}_get_arexperienceList")

            public_project_list_cache_key = f"api_{request.user.user_uid}_{app_uid}_get_arexperiencepubliclist"
            cache.delete(public_project_list_cache_key)
            
            return {'code': 200, 'message': 'success'}
        except Exception as e:
            print(repr(e))
            return {'code': 201, 'message': repr(e)}

    def update_app(self,request):
        app_uid = request.POST.get('app_uid')
        app_icon_image = request.FILES.get('app_icon_image')
        if app_icon_image is not None:
            assets_save_folder = os.path.join(str(self.request.user.user_uid), app_uid)
            assets_save_folder = assets_save_folder.replace('\\', '/')
            oss_path = "%s/%s" % (assets_save_folder, f"{create_md5(app_icon_image.name).replace('.jpg', '')}.jpg")
            from utils.aliyun_utility import AliyunObjectStorage
            aliyunStorage = AliyunObjectStorage()
            aliyunStorage._save(name=oss_path, content=app_icon_image.read(), progress_callback=None)
            app_icon_image_url = aliyunStorage.url(oss_path)
        else:
            app_icon_image_url = "%s%s"%(settings.BASE_WEBSITE_URL,default_image_url)
        app = ApplicationsModelV2.objects.get(app_uid=app_uid)
        app.app_icon_image = app_icon_image_url
        app.save()
        
        cache.delete(f"{request.user.user_uid}_get_applist")
        return {'code': 200, 'message': 'success'}

    def delete_app(self,request):
        """删除App"""
        app_uid = request.POST.get('app_uid')
        apps = ApplicationsModelV2.objects.filter(app_uid=app_uid)
        if len(apps) == 0:
            return {'code': 201, 'message': 'Incorrect package name'}
        for app in apps:
            if app.child_project != 0:
                return {'code': 201, 'message': 'You cannot delete Application. Because the application is not an empty application.'}
            app.delete()        
        cache.delete(f"{request.user.user_uid}_get_applist")
        return {'code': 200, 'message': 'Success'}
   
    def delete_project(self,request):
        """删除项目"""
        project_id = request.POST.get('project_id')
        app_uid = request.POST.get('app_uid')
        project = ARExperienceModelV2.objects.get(app_uid=app_uid, project_id=project_id)
        assets = ARExperienceResourceV2.objects.filter(project_id=project_id)
        if project is None:
            return {'code': 201, 'message': 'Incorrect projecet id'}

        # 1. 删除资源
        from utils.aliyun_utility import AliyunObjectStorage

        aliyun_oss = AliyunObjectStorage()
        sub_url_start_index = len(settings.OSS_BASE_URL+"/")
        for asset in assets:
            if asset.json_url != '' and aliyun_oss.exists(asset.json_url[sub_url_start_index:]):
                aliyun_oss.batch_delete_objects([asset.json_url[sub_url_start_index:], asset.bundle_url[sub_url_start_index:]])
            asset.delete()

        if project.project_preview != "":
            for preview in json.loads(project.project_preview):
                if aliyun_oss.exists(preview[sub_url_start_index:]):
                    aliyun_oss.delete(preview[sub_url_start_index:])

        if "https" in project.project_icon:
            if aliyun_oss.exists(project.project_icon[sub_url_start_index:]):
                aliyun_oss.delete(project.project_icon[sub_url_start_index:])

        if "https" in project.project_header:
            if aliyun_oss.exists(project.project_header[sub_url_start_index:]):
                aliyun_oss.delete(project.project_header[sub_url_start_index:])
        
        # 2.删除项目
        project.delete()

        app = ApplicationsModelV2.objects.get(user_uid=request.user.user_uid,app_uid=app_uid)
        app.child_project = app.child_project - 1
        app.save()
        
        cache.delete(f"{request.user.user_uid}_{app_uid}_get_arexperienceList")

        query_by_app_uid_cache_key = f"api_{request.user.user_uid}_{app_uid}_get_arexperiencebytagslist"
        cache.delete(query_by_app_uid_cache_key)

        query_project_recommend_key = f"api_{request.user.user_uid}_{app_uid}_get_recommendList"
        cache.delete(query_project_recommend_key)

        page_cache_key = f"api_{request.user.user_uid}_get_arexperience_page"
        cache.delete(page_cache_key)

        detail_cache_key = f"api_{project_id}_get_arexperience_detail"
        cache.delete(detail_cache_key)

        public_project_list_cache_key = f"api_{request.user.user_uid}_{app_uid}_get_arexperiencepubliclist"
        cache.delete(public_project_list_cache_key)

        return {'code': 200, 'message': 'Success'}