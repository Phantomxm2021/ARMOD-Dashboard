from django.conf import settings
from django.conf import settings
from django.core.cache import cache
from django.http import JsonResponse
from django.views.generic import View
from utils.mixin import LoginRequiredMixin
from django.shortcuts import render, redirect
from Apps.Applications.models import ApplicationsModel
from Apps.ARExperiences.models import ARExperienceModel, ARExperienceAsset
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage
# Create your views here.


class DashboardApplicationListView(LoginRequiredMixin, View):
    def get(self, request):
        """Get Application list"""
        user = request.user
        app_list = cache.get(f"{user.user_uid}_get_applist")
        if app_list is None:
            app_list = ApplicationsModel.objects.filter(user_uid=user.user_uid)
            cache.set(f"{user.user_uid}_get_applist",app_list,settings.API_CACHE_EXPIRED)
        page = int(request.GET.get("page", 1))
        paginator = Paginator(app_list, 10)
        page = request.GET.get('page')
        apps = paginator.get_page(page)
        return render(request, 'dashboard/application_list.html', {'applist': apps,'user':user})

    def post(self, request):
        """Create Application"""
<<<<<<< HEAD
        method = request.POST.get('method_type')
        response = {}
        if method == 'CreateApp':
            response=self.create(request)
        return JsonResponse(response)

    def create(self,request):
        """Create APP"""
        name = request.POST.get('app_name')
    
=======
        name = request.POST.get('appname')
>>>>>>> parent of 7df37a3 (upgrade to 1.0-alpha.2)
        packageid = request.POST.get('packageid')
          
        description = request.POST.get('description')
        if not all([name, packageid]):
            return JsonResponse({'code': 201, 'message': 'Incomplete data'})

        apps = ApplicationsModel.objects.filter(packageid=packageid)
        if len(apps) > 0:
            return JsonResponse({'code': 201, 'message': 'The Package Name was used'})

<<<<<<< HEAD
        # Use Packageid to generate a Token for the application for verification
        serializer = Serializer(settings.SECRET_KEY, 8640000000)
        token = {'packageid': packageid,'user_uid':request.user.user_uid}
        token = serializer.dumps(token)  
        token = token.decode('utf8')
=======
        # Use Packageid to generate Token for the application for verification
        serializer = Serializer(settings.SECRET_KEY, 8640000000)
        token = {'packageid': packageid,'user_uid':request.user.user_uid}
        token = serializer.dumps(token)
        token = token.decode('utf8') 
>>>>>>> parent of 7df37a3 (upgrade to 1.0-alpha.2)
        
        from utils.generate_random_pid import generate_unique_id
        app_uid = generate_unique_id(packageid)
        ApplicationsModel.objects.create(app_uid=app_uid,
                                         name=name,
                                         packageid=packageid,
                                         user_uid=request.user.user_uid,
                                         token=token,
                                         description=description)        
        cache.delete(f"{request.user.user_uid}_get_applist")
        return JsonResponse({'code': 200, 'message': 'success'})


class DashboardApplicationDeleteView(LoginRequiredMixin, View):
    def post(self, request):
        """Delete Application"""
        app_uid = request.POST.get('app_uid')
        apps = ApplicationsModel.objects.filter(app_uid=app_uid)
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
        """AR experience project list"""        
<<<<<<< HEAD
        arexperience_project = cache.get(f"{request.user.user_uid}_{app_uid}_get_arexperienceList")
        if arexperience_project is None:
            arexperience_project = ARExperienceModelV2.objects.filter(app_uid=app_uid).order_by('-create_time')
            cache.set(f"{request.user.user_uid}_get_projectList",arexperience_project,settings.API_CACHE_EXPIRED)
        paginator = Paginator(arexperience_project, 24)
        page = int(request.GET.get("page", 1))
        arexperience_project_pages = paginator.get_page(page)
        appinfo = ApplicationsModelV2.objects.get(app_uid=app_uid)
        return render(request, 'dashboard/arexperience_list.html', {'arexperience_projects': arexperience_project_pages, 'appinfo': appinfo})

    def post(self, request, app_uid):
        """Create new AR experience project"""
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
        """Create proejct"""
=======
        arshowcase_list = cache.get(f"{request.user.user_uid}_{app_uid}_get_arexperienceList")
        if arshowcase_list is None:
            arshowcase_list = ARExperienceModel.objects.filter(app_uid=app_uid).order_by('create_time')
            cache.set(f"{request.user.user_uid}_get_projectList",arshowcase_list,settings.API_CACHE_EXPIRED)
        paginator = Paginator(arshowcase_list, 10)
        page = int(request.GET.get("page", 1))
        arshowcase_pages = paginator.get_page(page)
        appinfo = ApplicationsModel.objects.get(app_uid=app_uid)
        return render(request, 'dashboard/arexperience_list.html', {'arshowcase_list': arshowcase_pages, 'appinfo': appinfo})

    def post(self, request, app_uid):
        """Create new AR experience project"""
>>>>>>> parent of 7df37a3 (upgrade to 1.0-alpha.2)
        try:
            app_uid = request.POST.get('app_uid')
            projectname = request.POST.get('projectname')
            description = request.POST.get('projectdescription',"")

            if not all([app_uid,projectname]):
                return JsonResponse({'code': 201, 'message': 'Incomplete data'})

            projects = ARExperienceModel.objects.filter(name=projectname, app_uid=app_uid)
            if len(projects) > 0:
                return JsonResponse({'code': 201, 'message': 'The Package Name was used'})

            from utils.generate_random_pid import generate_unique_id
            arexperience = ARExperienceModel.objects.create(arexperience_uid=generate_unique_id(projectname),
                                                            name=projectname,
                                                            app_uid=app_uid,
                                                            description=description)
            arexperience.save()

            arexperienceAsset = ARExperienceAsset.objects.create(
                arexperience_uid=arexperience.arexperience_uid)
            arexperienceAsset.save()

            app = ApplicationsModel.objects.get(app_uid=app_uid)
            app.child_project = app.child_project + 1
            app.save()

            cache.delete(f"{request.user.user_uid}_{app_uid}_get_arexperienceList")
            return JsonResponse({'code': 200, 'message': 'success'})
        except Exception as e:
            return JsonResponse({'code': 201, 'message': 'Unknow Error'})


<<<<<<< HEAD
    def delete_app(self,request):
        """Del App"""
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
        """Del project"""
        project_id = request.POST.get('project_id')
=======
class DashboardApplicationProjectDeleteView(LoginRequiredMixin, View):

    def post(self, request):
        """Delete the AR experience"""
        arexperience_uid = request.POST.get('arexperience_uid')
>>>>>>> parent of 7df37a3 (upgrade to 1.0-alpha.2)
        app_uid = request.POST.get('app_uid')
        project = ARExperienceModel.objects.get(app_uid=app_uid, arexperience_uid=arexperience_uid)
        asset = ARExperienceAsset.objects.get(arexperience_uid=arexperience_uid)
        if project is None:
            return JsonResponse({'code': 201, 'message': 'Incorrect projecet id'})

<<<<<<< HEAD
        # 1. Del assets
=======
        # 1.Delete resources
>>>>>>> parent of 7df37a3 (upgrade to 1.0-alpha.2)
        from utils.aliyun_utility import AliyunObjectStorage

        aliyun_oss = AliyunObjectStorage()

        sub_url_start_index = len(settings.OSS_BASE_URL)
        if asset.android_json is not '':
            if aliyun_oss.exists(asset.android_json[len(settings.OSS_BASE_URL):]):
                aliyun_oss.batch_delete_objects(
                    [asset.android_json[sub_url_start_index:], asset.android_bundle[sub_url_start_index:]])

        if asset.ios_json is not '':             
            if aliyun_oss.exists(asset.ios_json[len(settings.OSS_BASE_URL):]):
                print(type([asset.android_json[sub_url_start_index:],asset.android_bundle[sub_url_start_index:]]))
                aliyun_oss.batch_delete_objects(
                    [asset.ios_json[sub_url_start_index:], asset.ios_bundle[sub_url_start_index:]])

<<<<<<< HEAD
        if "https" in project.project_header:
            if aliyun_oss.exists(project.project_header[sub_url_start_index:]):
                aliyun_oss.delete(project.project_header[sub_url_start_index:])
        
        # 2.Del project
=======
        # 2.Delete AR experience project
>>>>>>> parent of 7df37a3 (upgrade to 1.0-alpha.2)
        project.delete()
        asset.delete()

        child_projecet_count = ApplicationsModel.objects.get(
            app_uid=app_uid).child_project - 1
        ApplicationsModel.objects.update(child_project=child_projecet_count)
        cache.delete(f"{request.user.user_uid}_{app_uid}_get_arexperienceList")
        return JsonResponse({'code': 200, 'message': 'Success'})
