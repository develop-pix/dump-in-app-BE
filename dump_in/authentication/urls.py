from django.urls import path

from dump_in.authentication.apis import (
    AppleLoginAPI,
    AppleLoginRedirectAPI,
    KakaoLoginAPI,
    NaverLoginAPI,
    UserJWTRefreshAPI,
)

urlpatterns = [
    # auth
    path("jwt/refresh", UserJWTRefreshAPI.as_view(), name="jwt-refresh"),
    # oauth
    path("kakao/login", KakaoLoginAPI.as_view(), name="kakao-login"),
    path("naver/login", NaverLoginAPI.as_view(), name="naver-login"),
    path("apple/callback", AppleLoginAPI.as_view(), name="apple-login-callback"),
    path("apple/redirect", AppleLoginRedirectAPI.as_view(), name="apple-login-redirect"),
]
