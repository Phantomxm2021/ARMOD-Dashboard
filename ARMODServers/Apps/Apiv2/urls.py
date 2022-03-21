from django.conf.urls import url
from Apps.Apiv2.views import GetARResourcesView, GetARExperienceDetailView
from Apps.Apiv2.views import GetTagListView,GetARExperienceRecommendList,GetARExperiencePublicListView,GetARExperiencesView
from Apps.Apiv2.views import GetARexperienceByTagsListView 
app_name = 'Apps.Users'
urlpatterns = [
    url(r'^getarresources$', GetARResourcesView.as_view(), name='getarresources'),
    url(r'^getarexperience$', GetARExperienceDetailView.as_view(), name='getarexperience'),
    url(r'^getarexperiencelist$', GetARExperiencesView.as_view(), name='getarexperience'),
    url(r'^gettaglist$', GetTagListView.as_view(), name='getshowcasetags'),
    url(r'^getrecommendslist$', GetARExperienceRecommendList.as_view(), name='getshowcaserecommends'),
    url(r'^getarexperiencepubliclist$', GetARExperiencePublicListView.as_view(), name='getarexperiencepubliclist'),
    url(r'^getarexperiencebytagslist$', GetARexperienceByTagsListView.as_view(), name='getarexperiencebytagslist'),

    
    # api/v2/
]