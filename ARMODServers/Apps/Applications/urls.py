from django.conf.urls import url
from Apps.Applications.views import DashboardApplicationListView,DashboardApplicationDeleteView,DashboardApplicationProjectListView,DashboardApplicationProjectDeleteView
app_name = 'Apps.Users'
urlpatterns = [
    url(r'^apps/$', DashboardApplicationListView.as_view(), name='apps'),
    url(r'^apps/appdelete/$', DashboardApplicationDeleteView.as_view(), name='appdelete'),
    url(r'^apps/appdetails/(?P<app_uid>\d+)/$', DashboardApplicationProjectListView.as_view(), name='appdetails'),
    url(r'^apps/projectdelete/$', DashboardApplicationProjectDeleteView.as_view(), name='projectdelete'),
]