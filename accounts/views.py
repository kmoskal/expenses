from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, exceptions
from rest_framework.permissions import AllowAny
from .serializers import (RegisterSerializer, CustomUserSerializer,
                          CustomUserProfileUpdateSerializer)
from .utils import (generate_access_token,
                    generate_refresh_token,
                    generate_activation_token)
from .models import ActivateAccount, CustomUser
import jwt


class RegisterCustomUser(APIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            activate_account = ActivateAccount(
                email=serializer.data['email'],
                token=generate_activation_token()
            )
            activate_account.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ActivateAccountView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, token=None):
        account = ActivateAccount.objects.filter(token=token).first()
        if account is None:
            raise exceptions.NotFound('No account to activate')
        user = CustomUser.objects.filter(email=account.email).first()
        user.is_active = True
        user.save()
        account.delete()
        return Response({'detail': 'Account successfully activated'})


@method_decorator(csrf_protect, name='put')
class ProfileView(APIView):
    def get(self, request):
        user = request.user
        serialized_user = CustomUserSerializer(user).data
        return Response({'user': serialized_user})

    def put(self, request):
        serialized_user = CustomUserProfileUpdateSerializer(
            request.user, data=request.data
        )
        if serialized_user.is_valid():
            serialized_user.save()
            return Response(serialized_user.data)
        return Response(
            serialized_user.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


@method_decorator(csrf_protect, name='post')
class RefreshTokenView(APIView):
    '''
        Need cookie with valid refresh_token and header
        X-CSRFTOKEN with valid csrf token.
    '''
    def post(self, request):
        refresh_token = request.COOKIES.get('refreshtoken')
        if refresh_token is None:
            raise exceptions.AuthenticationFailed(
                'Authentication credentials were not provided.')
        try:
            payload = jwt.decode(
                refresh_token,
                settings.SECRET_KEY,
                algorithms='HS256'
            )
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed(
                'Expired refresh token, please login again.')
        user = CustomUser.objects.filter(id=payload.get('user_id')).first()
        if user is None:
            raise exceptions.AuthenticationFailed('User is inactive')

        access_token = generate_access_token(user)
        return Response({'access_token': access_token})


@method_decorator(ensure_csrf_cookie, name='post')
class GetTokensView(APIView):
    permission_classes = [AllowAny]
    serializers = CustomUserSerializer

    def post(self, request):
        CustomUser = get_user_model()
        email = request.data.get('email')
        password = request.data.get('password')
        response = Response()
        if (email is None) or (password is None):
            raise exceptions.AuthenticationFailed('Email/password required')

        user = CustomUser.objects.filter(email=email).first()
        if user is None:
            raise exceptions.AuthenticationFailed('Invalid email or password')
        if not user.check_password(password):
            raise exceptions.AuthenticationFailed('Invalid email or password')
        if not user.is_active:
            raise exceptions.AuthenticationFailed('User is not active')

        serialized_user = self.serializers(user).data

        access_token = generate_access_token(user)
        refresh_token = generate_refresh_token(user)

        response.set_cookie(
            key='refreshtoken', value=refresh_token,
            samesite='None', secure=False, httponly=False
        )
        response.data = {
            'access_token': access_token,
            'user': serialized_user,
        }

        return response
