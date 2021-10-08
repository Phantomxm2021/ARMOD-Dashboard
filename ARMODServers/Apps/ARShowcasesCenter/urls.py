from django.conf.urls import url
from Apps.ARShowcasesCenter.views import ARShowcasesCenterView,ARShowcasesCenterProjectPostView,ARShowcaseTagsView

app_name = 'Apps.ARShowcasesCenter'
urlpatterns = [
    url(r'^apps/arshowcasescenter/(?P<app_uid>\d+)/$', ARShowcasesCenterView.as_view(), name='arshowcasescenter'),   
    url(r'^apps/arshowcasescenter/arshowcasesprojectpost', ARShowcasesCenterProjectPostView.as_view(), name='arshowcasesprojectpost'),      
    url(r'^apps/arshowcasescenter/arshowcasetag', ARShowcaseTagsView.as_view(), name='arshowcasetag'),
]