from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import View
from Apps.Index.models import IndexPageViewKeyBenfitsModel
# Create your views here.


class DashboardIndexView(View):
    def get(self,request):
        return render(request,'index/static_index.html')
        # return render(request,'index/index_test.html')

class DashboardZhHansPrivacyView(View):
    def get(self,request):
        return render(request,'index/static_ZhHansprivacy.html')

class DashboardEnUsPrivacyView(View):
    def get(self,request):
        return render(request,'index/static_EnUsprivacy.html')