# accounts/urls.py
from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    # 회원가입/로그인/로그아웃
    # path("join/", RegisterView.as_view()),
    # path("login/", AuthView.as_view()),
    # path("logout/", LogoutView.as_view()),
    # path("delete/", DeleteView.as_view()),
    # path("restore/", RestoreView.as_view()),
    
    # 구글 소셜로그인
    path("google/login/", google_login, name="google_login"),
    path("google/callback/", google_callback, name="google_callback"),

    # 토큰
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
]