from django.urls import path

from dump_in.authentication.apis import (
    AppleLoginAPI,
    AppleLoginRedirectAPI,
    KakaoLoginAPI,
    KakaoLoginRedirectAPI,
    NaverLoginAPI,
    NaverLoginRedirectAPI,
    UserJWTRefreshAPI,
)

urlpatterns = [
    # auth
    path("jwt/refresh", UserJWTRefreshAPI.as_view(), name="jwt-refresh"),
    # oauth
    path("kakao/callback", KakaoLoginAPI.as_view(), name="kakao-login-callback"),
    path("kakao/redirect", KakaoLoginRedirectAPI.as_view(), name="kakao-login-redirect"),
    path("naver/callback", NaverLoginAPI.as_view(), name="naver-login-callback"),
    path("naver/redirect", NaverLoginRedirectAPI.as_view(), name="naver-login-redirect"),
    path("apple/callback", AppleLoginAPI.as_view(), name="apple-login-callback"),
    path("apple/redirect", AppleLoginRedirectAPI.as_view(), name="apple-login-redirect"),
]
