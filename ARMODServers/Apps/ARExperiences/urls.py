from django.conf.urls import url,include
from Apps.ARExperiences.views import DashboardProjectListView,DashbaordARExperienceUpdateView
from django.conf import settings
from django.conf.urls.static import static

app_name = 'Apps.ARExperiences'
urlpatterns = [
    url(r'^apps/appdetails/(?P<app_uid>\d+)/projectdetails/(?P<arexperience_uid>\d+)$', DashboardProjectListView.as_view(), name='projectdetails'),    
    url(r'^apps/appdetails/(?P<app_uid>\d+)/projectdetails/(?P<arexperience_uid>\d+)/update$', DashbaordARExperienceUpdateView.as_view(), name='update'),    
]

urlpatterns += static(settings.IMAGE_URL,document_root = settings.IMAGE_ROOT)
urlpatterns += static("/arexperiences/",document_root = settings.AREXPERIENCE_ROOT)