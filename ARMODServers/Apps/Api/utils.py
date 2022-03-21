from rest_framework import exceptions, HTTP_HEADER_ENCODING
from rest_framework.authentication import BasicAuthentication
from rest_framework.throttling import SimpleRateThrottle
from django.core import serializers
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired
from django.conf import settings
from Apps.Users.models import User
from Apps.Applications.models import ApplicationsModel
import time
from django.core.cache import cache
import logging
serializer = Serializer(settings.SECRET_KEY, 8640000000)

# Create your views here.


def get_authorization_header(request):
    """
    Return request's 'Authorization:' header, as a bytestring.
    Hide some test client ickyness where the header can be unicode.
    """
    auth = request.META.get('HTTP_AUTHORIZATION', b'')
    if isinstance(auth, str):
        # Work around django test client oddness
        auth = auth.encode(HTTP_HEADER_ENCODING)
    return auth


def get_package_id(request):
    try:
        package_id = request.POST.get('package_id', None)
        return package_id
    except Exception as e:
        logging.exception(e)


class Authtication(BasicAuthentication):
    """API Authentication"""
    keyword = 'Token'
    model = None
    loaded_token = None

    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.keyword.lower().encode():
            raise exceptions.AuthenticationFailed(
                'Invalid token header. No credentials provided.')

        if len(auth) == 1:
            msg = 'Invalid token header. No credentials provided.'
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = 'Invalid token header. Token string should not contain spaces.'
            raise exceptions.AuthenticationFailed(msg)
        try:
            token = auth[1].decode()
        except UnicodeError:
            msg = 'Invalid token header. Token string should not contain invalid characters.'
            raise exceptions.AuthenticationFailed(msg)

        try:
            info = serializer.loads(token)
            package_id = info['packageid']
            user_uid = info['user_uid']
            get_app_cache_key = f"api_{user_uid}_{package_id}_get_app"
            app = cache.get(get_app_cache_key)
            if app is None:
                try:
                    app = ApplicationsModel.objects.get(user_uid=user_uid, packageid=package_id)                
                    cache.set(get_app_cache_key, app,settings.API_CACHE_EXPIRED)
                except ApplicationsModel.DoesNotExist:
                    msg = 'Permission denied.'
                    raise exceptions.AuthenticationFailed(msg)

               

            get_user_cache_key = f"{user_uid}_get_user"
            user = cache.get(get_user_cache_key)
            if user is None:
                user = User.objects.get(user_uid=user_uid)
                if user:
                    cache.set(get_user_cache_key, user,
                              settings.API_CACHE_EXPIRED)

            if user is None:
                msg = 'Invalid token.'
                raise exceptions.AuthenticationFailed(msg)

            if package_id == get_package_id(request):
                return (user, [app.app_uid, app.packageid])

            raise exceptions.AuthenticationFailed('Package id not matched')
        except SignatureExpired as e:
            raise exceptions.AuthenticationFailed('App does not exist')
        except Exception as e:
            logging.exception(e)
            raise exceptions.AuthenticationFailed(e)


class AuthticationWithoutPackageId(BasicAuthentication):
    """API Authentication"""
    keyword = 'Token'
    model = None
    loaded_token = None

    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.keyword.lower().encode():
            raise exceptions.AuthenticationFailed(
                'Invalid token header. No credentials provided.')

        if len(auth) == 1:
            msg = 'Invalid token header. No credentials provided.'
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = 'Invalid token header. Token string should not contain spaces.'
            raise exceptions.AuthenticationFailed(msg)
        try:
            token = auth[1].decode()
        except UnicodeError:
            msg = 'Invalid token header. Token string should not contain invalid characters.'
            raise exceptions.AuthenticationFailed(msg)

        try:
            info = serializer.loads(token)
            package_id = info['packageid']
            user_uid = info['user_uid']
            get_app_cache_key = f"api_{user_uid}_{package_id}_get_app"
            app = cache.get(get_app_cache_key)
            if app is None:
                try:
                    app = ApplicationsModel.objects.get(
                        user_uid=user_uid, packageid=package_id)
                    cache.set(get_app_cache_key, app,
                              settings.API_CACHE_EXPIRED)
                except ApplicationsModel.DoesNotExist:
                    msg = 'Permission denied.'
                    raise exceptions.AuthenticationFailed(msg)

            get_user_cache_key = f"{user_uid}_get_user"
            user = cache.get(get_user_cache_key)
            if user is None:
                user = User.objects.get(user_uid=user_uid)
                if user:
                    cache.set(get_user_cache_key, user,
                              settings.API_CACHE_EXPIRED)

            if user is None:
                msg = 'Invalid token.'
                raise exceptions.AuthenticationFailed(msg)

            return (user, [app.app_uid, app.packageid])

            raise exceptions.AuthenticationFailed('Package id not matched')
        except SignatureExpired as e:
            logging.exception(e)

            raise exceptions.AuthenticationFailed('App does not exist')
        except Exception as e:
            logging.exception(e)
            raise exceptions.AuthenticationFailed(e)


class VisitThrottle(SimpleRateThrottle):
    scope = 'api'
    keyword = 'Token'
    model = None
    loaded_token = None

    def get_cache_key(self, request, view):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.keyword.lower().encode():
            raise exceptions.AuthenticationFailed(
                'Invalid token header. No credentials provided.')

        if len(auth) == 1:
            msg = 'Invalid token header. No credentials provided.'
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = 'Invalid token header. Token string should not contain spaces.'
            raise exceptions.AuthenticationFailed(msg)
        try:
            token = auth[1].decode()
        except UnicodeError:
            msg = 'Invalid token header. Token string should not contain invalid characters.'
            raise exceptions.AuthenticationFailed(msg)
        package_id = serializer.loads(token)['packageid']
        return package_id
