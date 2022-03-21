from django.conf.urls import url
from Apps.Index.views import DashboardIndexView,DashboardZhHansPrivacyView,DashboardEnUsPrivacyView
app_name = 'Apps.Index'
urlpatterns = [
    url(r'^$', DashboardIndexView.as_view(), name='index'),    
    url(r'^zh-hans/privacy/$', DashboardZhHansPrivacyView.as_view(), name='privacy'),    
    url(r'^en-us/privacy/$', DashboardEnUsPrivacyView.as_view(), name='privacy'),    
]