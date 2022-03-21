from django.shortcuts import render
from Apps.TagManager.models import TagsModel
from Apps.Applications.models import ApplicationsModelV2
from django.views.generic import View
from utils.mixin import LoginRequiredMixin
from django.core.cache import cache
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.conf import settings
import time

# Create your views here.
dashboard_tag_fields =['tag_name']
class DashboardTagManagerView(LoginRequiredMixin,View):
    
    def get(self,request,app_uid):
        query_tag_key = f"{request.user.user_uid}_{app_uid}_get_tagList"
        all_preset_tags = cache.get(query_tag_key)
        if all_preset_tags is None:
            all_query_set_tags = TagsModel.objects.filter(
                app_uid=app_uid, user_uid=request.user.user_uid)
            
            all_preset_tags = (all_query_set_tags.values(
                'tag_reference_weight', 'tag_sort_weight', 'tag_name','create_time'))
            cache.set(query_tag_key,all_preset_tags,settings.API_CACHE_EXPIRED)
            
        modal_html_txt = render_to_string(
                    'dashboard/showcase_tags_modal_table.html', {'all_preset_tags': all_preset_tags})
        return JsonResponse({'code': 200, 'message': 'success', 'data': modal_html_txt})


    def post(self, request,app_uid):
        method_type = request.POST.get('method_type')
        app_uid = request.POST.get('app_uid')
        tag_name = request.POST.get('tag_name')
        response={}
        if method_type == 'CreateTag':
            response = self.create_tag(request=request,app_uid=app_uid,tag_name=tag_name)
        elif method_type == 'DeleteTag':
            response = self.delete_tag(request=request,app_uid=app_uid,tag_name=tag_name)
        elif method_type == 'GetTags':
            response = self.get_tags(request=request,app_uid=app_uid)

        return JsonResponse(response)

    def create_tag(self,request,app_uid,tag_name):
        showcase_tag_weight = request.POST.get('tag_weight')

        query_tag_key = f"{request.user.user_uid}_{app_uid}_get_tagList"
        query_api_tag_key = f"api_{request.user.user_uid}_{app_uid}_get_tagList"

        try:
            tag_query_set = TagsModel.objects.get(
                user_uid=request.user.user_uid, app_uid=app_uid,tag_key = "%s-%s-%s"%(request.user.user_uid,app_uid,tag_name), tag_name=tag_name)
        except TagsModel.DoesNotExist:
            tag_query_set = None

        if tag_query_set is None:
            tag_query_set = TagsModel.objects.create(
                user_uid=request.user.user_uid,
                app_uid=app_uid,
                tag_name=tag_name,
                tag_key = "%s-%s-%s"%(request.user.user_uid,app_uid,tag_name),
                tag_sort_weight=showcase_tag_weight)
            all_preset_tags = TagsModel.objects.filter(
                app_uid=app_uid, user_uid=request.user.user_uid).order_by('tag_sort_weight')
            
            cache.set(query_tag_key,all_preset_tags,settings.API_CACHE_EXPIRED)
            cache.set(query_api_tag_key,all_preset_tags,settings.API_CACHE_EXPIRED)
            modal_html_txt = render_to_string(
                'dashboard/showcase_tags_modal_table.html', {'all_preset_tags': all_preset_tags})
            # all_preset_tags_cache = all_preset_tags.values('tag_sort_weight', 'tag_name')
            return {'code': 200, 'message': 'success', 'data': modal_html_txt}

        return {'code': 201, 'message': 'The tag name was exist!'}

    def delete_tag(self,request,app_uid,tag_name):

        query_tag_key = f"{request.user.user_uid}_{app_uid}_get_tagList"
        query_api_tag_key = f"api_{request.user.user_uid}_{app_uid}_get_tagList"

        try:
            tag_query_set = TagsModel.objects.get(
                user_uid=request.user.user_uid, app_uid=app_uid, tag_name=tag_name)
            tag_query_set.delete()
            all_preset_tags = TagsModel.objects.filter(
                app_uid=app_uid, user_uid=request.user.user_uid).order_by('tag_sort_weight')
           
            cache.set(query_tag_key,all_preset_tags,settings.API_CACHE_EXPIRED)
            cache.set(query_api_tag_key,all_preset_tags,settings.API_CACHE_EXPIRED)
            modal_html_txt = render_to_string(
                'dashboard/showcase_tags_modal_table.html', {'all_preset_tags': all_preset_tags})
            return {'code': 200, 'message': 'success', 'data': modal_html_txt}
        except TagsModel.DoesNotExist:
            tag_query_set = None
        return {'code': 201, 'message': 'The tag name was not exist!'}
   
    def get_tags(self,request,app_uid):
        
        query_tag_key = f"{request.user.user_uid}_{app_uid}_get_tagList"
        all_preset_tags = cache.get(query_tag_key)
        all_tags=[]

        if all_preset_tags is None:
            all_query_set_tags = TagsModel.objects.filter(app_uid=app_uid, user_uid=request.user.user_uid).order_by('tag_sort_weight')
            all_preset_tags = all_query_set_tags

        for tag in all_preset_tags:
            all_tags.append(model_to_dict(tag,dashboard_tag_fields))
        

        return {'code': 200, 'message': 'success', 'data': all_tags}