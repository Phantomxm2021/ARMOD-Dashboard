"""ARMODServers URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('Apps.Users.urls', namespace='auth')),
    path('dashboard/', include('Apps.Applications.urls', namespace='applications')),
    path('dashboard/', include('Apps.ARExperiences.urls', namespace='arexperiences')),
    path('dashboard/', include('Apps.TagManager.urls', namespace='tagmanager')),  

    path('api/v1/',include('Apps.Api.urls', namespace='api')),
    path('api/v2/',include('Apps.Apiv2.urls', namespace='apiv2')),

    #last 
    path('',include('Apps.Index.urls', namespace='index')),

    ]
