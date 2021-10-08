from django.conf.urls import url
from Apps.Api.views import ARExperienceView,ARShowcaseView,ARShowcaseDetailView,ARShowcaseTagsView,ARShowcaseRecommends,ARShowcasePublicView
app_name = 'Apps.Users'
urlpatterns = [
    url(r'^getarexperience$', ARExperienceView.as_view(), name='getarexperience'),
    url(r'^getshowcaselist$', ARShowcaseView.as_view(), name='getshowcaselist'),
    url(r'^getshowcase$', ARShowcaseDetailView.as_view(), name='getshowcase'),
    url(r'^getshowcasetags$', ARShowcaseTagsView.as_view(), name='getshowcasetags'),
    url(r'^getshowcaserecommends$', ARShowcaseRecommends.as_view(), name='getshowcaserecommends'),
    url(r'^getshowcasepublic$', ARShowcasePublicView.as_view(), name='getshowcasepublic'),

    
    # api/v1/
]