from django.urls import path
from .views import (RegisterCustomUser, GetTokensView, ActivateAccountView,
                    ProfileView, RefreshTokenView)


urlpatterns = [
    path('register', RegisterCustomUser.as_view(), name='accounts-register'),
    path('activate/<slug:token>', ActivateAccountView.as_view(), name='accounts-activate'),
    path('profile', ProfileView.as_view(), name='accounts-profile'),
    path('get-tokens', GetTokensView.as_view(), name='accounts-get-token'),
    path('refresh-token', RefreshTokenView.as_view(), name='accounts-refresh-token'),
    path('profile-update', ProfileView.as_view(), name='accounts-profile-update'),
]
