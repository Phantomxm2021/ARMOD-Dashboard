from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.views.generic import View
from Apps.Users.models import User
import re
from django.db.models import Q
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.backends import ModelBackend
from celery_tasks.tasks import send_register_active_email
from django.contrib.auth import authenticate, login, logout
from itsdangerous import SignatureExpired
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from django.contrib.sites.models import Site
from django.template.loader import render_to_string

# Create your views here.


class RegisterView(View):
    """Register user"""

    def get(self, request):
        return render(request, 'auth/register.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        allow = request.POST.get('privacypolicychecker')

        if not all([username, password, email]):
            # 数据不完整incomplete data
            return JsonResponse({'code': 201, 'message': {'title': 'ERROR', 'body': 'incomplete data'}})

         # Check e-mail
        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return JsonResponse({'code': 201, 'message': {'title': 'ERROR', 'body': 'Email address is incorrect'}})

        if allow != 'on':
            return JsonResponse({'code': 201, 'message': {'title': 'ERROR', 'body': 'Please agree to the Privacy Policy first'}})

        # Check for duplicate users
        try:
            user = User.objects.filter(
                Q(username=username) | Q(email=email)).first()
        except:
            user = None
        if user is not None:
            return JsonResponse({'code': 201, 'message':  {'title': 'ERROR', 'body': 'user already exists'}})

        # Perform business processing: perform user registration
        from utils.generate_random_pid import generate_unique_id
        user = User.objects.create_user(user_uid=generate_unique_id(
            email), username=username, email=email, password=password)
        user.is_active = 0
        user.save()

        # Send activation link, including activation link: http://127.0.0.1:8000/user/active/5
        # The activation link needs to contain the user's identity information, and the identity information should be encrypted
        # Activation link format: /user/active/user identity encrypted information /user/active/token

        # Encrypt the user's identity information and generate an activation token
        serializer = Serializer(settings.SECRET_KEY, 900)
        info = {'confirm': user.user_uid}
        token = serializer.dumps(info)
        token = token.decode('utf8') 

        # Send email asynchronously
        full_url = 'https://%s/%s/%s' % (
            Site.objects.get_current().domain, 'auth/activation', token)

        message = '我们已收到您注册 XRMOD 的请求。如果邮箱是自用的，请点击下方按钮进行验证。如果不是你，请忽略。'
        html_message = render_to_string('activate_email_template.html', {
                                        'username': username, 'url': full_url, 'title': '感谢您注册XRMOD', 'content': message})
        send_register_active_email.delay(email, html_message)

        # Return to response, jump to home page
        return JsonResponse({'code': 200, 'message': {'title': 'Success', 'body': '账户注册成功，请前往邮箱激活'}, 'url': reverse('auth:login')})


# /user/active/token
class ActiveView(View):
    """User active"""

    def get(self, request, token):
        # do user activation
        # Decrypt to get the user information to be activated
        serializer = Serializer(settings.SECRET_KEY, 900)
        try:
            info = serializer.loads(token)
            # Get the id of the user to be activated
            user_uid = info['confirm']

            # Get user information by id
            user = User.objects.get(user_uid=user_uid)
            user.is_active = 1
            user.save()

            # Jump to login page
            return redirect(reverse('auth:login'))
        except SignatureExpired as e:
            # Activation link has expired
            return HttpResponse('The activation link has expired')


# /user/login
class LoginView(View):
    """Login"""

    def get(self, request):
        # show login page
        # Determine whether to remember the password
        if 'email' in request.COOKIES:
            email = request.COOKIES.get('email')
            checked = 'checked'
        else:
            email = ''
            checked = ''

        return render(request, 'auth/login.html', {'email': email, 'checked': checked})

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        if not all([email, password]):
            return JsonResponse({'code': 201, 'message': 'Incomplete data'})

        user = authenticate(request, email=email, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return JsonResponse({'code': 200, 'message': 'Success', 'data': reverse('applications:apps')})
            else:
                return JsonResponse({'code': 202, 'message': 'Account is not verified'})
        else:
            return JsonResponse({'code': 203, 'message': 'Incorrect email or password'})


class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, email=None, password=None, **kwargs):
        try:
            if username is not None:
                user = User.objects.get(username=username)
            else:
                user = User.objects.get(email=email)
            if user.check_password(password):
                return user
        except Exception as e:
            print(e)
        return None


# /user/logout
class LogoutView(View):
    """Logout"""
    def get(self, request):
        logout(request)
        return redirect(reverse('auth:login'))


class ForgotPasswordView(View):
    def get(self, request):
        return render(request, 'auth/forgotpassword.html')

    def post(self, request):
        email = request.POST.get("email")
        ret = {'code': 200, 'message': None}
        if not all([email]):
            ret['code'] = 201
            ret['message'] = {'title': 'ERROR', 'body': 'Incomplete data'}
            return JsonResponse(ret)
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None

        if user is None:
            ret['code'] = 201
            ret['message'] =  {'title': 'ERROR', 'body': 'User is not exists'}
            return JsonResponse(ret)

        serializer = Serializer(settings.SECRET_KEY, 900)
        info = {'reset': email}
        token = serializer.dumps(info) 
        token = token.decode('utf8')  

        # Send email asynchronously
        full_url = 'https://%s/%s/%s' % (
            Site.objects.get_current().domain, 'auth/resetpassword', token)
        message = 'We have received your request to reset password for ARMOD. If the email is for your own use,please click the button below to verify it. If it is not you, please ignore it.'
        html_message = render_to_string('reset_password_email_template.html', {
                                        'username': '', 'url': full_url, 'title': 'Reset your account password for ARMOD', 'content': message})
        send_register_active_email.delay(email, html_message)
        return JsonResponse({'code': 200, 'message': {'title': 'Success', 'body': 'Password reset email sent!'}})


class ResetPassworView(View):
    def get(self, request, token):
        try:
            if not all([token]):
                return HttpResponse('The link is no valid')

            serializer = Serializer(settings.SECRET_KEY, 900)
            info = serializer.loads(token)
            email = info['reset']

            try:
                user = User.objects.get(email=email)
            except user.DoesNotExist:
                user = None     
                return HttpResponse('The email is no valid')
            
            return render(request, 'auth/changepwd.html', {'user_uid': user.user_uid, 'token': token})
        except SignatureExpired as e:            
            return HttpResponse('The link to reset the password is no longer valid')

    def post(self, request, token):
        ret = {'code': 200, 'message': None, 'data': None}
        serializer = Serializer(settings.SECRET_KEY, 900)
        info = serializer.loads(token)
        email = info['reset']
        new_password = request.POST.get('new_password')
        if not all([email, new_password]):
            ret['code'] = 201
            ret['message'] = {'title': 'ERROR', 'body': 'Incomplete data'}
            return JsonResponse(ret)
        try:
            user = User.objects.get(email=email)
        except user.DoesNotExist:
            user = None
        if user is None:
            ret['code'] = 201
            ret['message'] = {'title': 'ERROR', 'body': 'User is not exists'}
            return JsonResponse(ret)

        user.set_password(new_password)
        user.save()

        ret['code'] = 200
        ret['message'] = {'title': 'Success',
                          'body': 'Password has been reset'}
        return JsonResponse(ret)
