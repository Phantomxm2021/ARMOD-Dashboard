from django.conf.urls import url
from Apps.TagManager.views import DashboardTagManagerView

app_name = 'Apps.TagManager'
urlpatterns = [
    url(r'^apps/appdetails/(?P<app_uid>\d+)/tagmanager/$', DashboardTagManagerView.as_view(), name='tagmanager'),   
]