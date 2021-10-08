from django.conf.urls import url
from Apps.Users.views import RegisterView,LoginView,LogoutView,ActiveView,ForgotPasswordView,ResetPassworView
app_name = 'Apps.Users'
urlpatterns = [
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^activation/(?P<token>.*)$', ActiveView.as_view(), name='activation'),
    url(r'^forgotpassword/$', ForgotPasswordView.as_view(), name='forgotpassword'),
    url(r'^resetpassword/(?P<token>.*)$', ResetPassworView.as_view(), name='resetpassword'),
]