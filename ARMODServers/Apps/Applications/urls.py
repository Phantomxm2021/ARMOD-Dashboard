from django.conf.urls import url
from Apps.Applications.views import DashboardApplicationListView,DashboardApplicationProjectListView
app_name = 'Apps.Users'
urlpatterns = [
    url(r'^apps/$', DashboardApplicationListView.as_view(), name='apps'),
    url(r'^apps/appdetails/$', DashboardApplicationProjectListView.as_view(), name='appdetails'),
    url(r'^apps/appdetails/(?P<app_uid>\d+)/$', DashboardApplicationProjectListView.as_view(), name='appdetails'),
]