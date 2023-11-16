from django.urls import path

from dump_in.authentication.apis import (
    KakaoLoginAPI,
    KakaoLoginRedirectAPI,
    NaverLoginApi,
    NaverLoginRedirectApi,
    UserJWTRefreshAPI,
)

urlpatterns = [
    # auth
    path("jwt/refresh", UserJWTRefreshAPI.as_view(), name="jwt-refresh"),
    # oauth
    path("kakao/callback", KakaoLoginAPI.as_view(), name="kakao-login-callback"),
    path("kakao/redirect", KakaoLoginRedirectAPI.as_view(), name="kakao-login-redirect"),
    path("naver/callback", NaverLoginApi.as_view(), name="naver-login-callback"),
    path("naver/redirect", NaverLoginRedirectApi.as_view(), name="naver-login-redirect"),
]
