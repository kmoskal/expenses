from django.conf import settings
from django.contrib.auth import get_user_model
from django.middleware.csrf import CsrfViewMiddleware
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication
import jwt


class CSRFCheck(CsrfViewMiddleware):
    def _reject(self, request, reason):
        return reason


class SafeJWTAuthentication(BaseAuthentication):
    '''
        custom authentication class for DRF and JWT
        https://github.com/encode/django-rest-framework/blob/master/rest_framework/authentication.py
    '''

    def authenticate(self, request):
        CustomUser = get_user_model()
        authorization_header = request.headers.get('Authorization')

        if not authorization_header:
            return None
        try:
            access_token = authorization_header.split(' ')[1]
            payload = jwt.decode(access_token, settings.SECRET_KEY,
                                 algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('access_token expired')
        except IndexError:
            raise exceptions.AuthenticationFailed('Token prefix missing')

        custom_user = CustomUser.objects.filter(id=payload['user_id']).first()
        if custom_user is None:
            raise exceptions.AuthenticationFailed('User not found')

        if not custom_user.is_active:
            raise exceptions.AuthenticationFailed('User is not active')

        self.enforce_csrf(request)
        return (custom_user, None)

    def enforce_csrf(self, request):
        '''
            Enforce CSRF validation
        '''
        check = CSRFCheck()
        # populates request.META['CSRF_COOKIE'],which is used in process_view()
        check.process_request(request)
        reason = check.process_view(request, None, (), {})
        if reason:
            raise exceptions.PermissionDenied(f'CSRF Failed: {reason}')
