from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from authentication.views import *

urlpatterns = [
    path('api/v1/auth/token/refresh', TokenRefreshView.as_view(), name='refresh_token'),
    path('api/v1/auth/login/generate', LoginGenerateAPI.as_view(), name='api_auth_login_generate'),
    path('api/v1/auth/login/verify', LoginVerifyAPI.as_view(), name='api_auth_login_verify'),
    path('api/v1/auth/login/regenerate', RegenerateLoginVerificationCode.as_view(), name='api_auth_login_regenerate'),
    path('api/v1/auth/register', RegisterAPI.as_view(), name='api_auth_register'),
    path('api/v1/auth/register/verify', VerifyRegistrationAPI.as_view(), name='api_auth_verify_registration'),
    path('api/v1/auth/register/regenerate', RegenerateRegisterVerificationCode.as_view(),
         name='api_auth_register_regenerate'),
    path('api/v1/auth/forget-password/generate', ForgetPasswordGenerateAPI.as_view(),
         name='api_auth_forget_password_generate'),
    path('api/v1/auth/forget-password/verify', ForgetPasswordVerifyAPI.as_view(),
         name='api_auth_forget_password_verify'),
    path('api/v1/auth/users/me', UpdateProfileAPI.as_view(), name='api_update_profile'),
]
