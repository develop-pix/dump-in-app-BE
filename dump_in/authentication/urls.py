from django.urls import path

from dump_in.authentication.apis import (
    KakaoLoginAPI,
    KakaoLoginRedirectAPI,
    UserJWTRefreshAPI,
)

urlpatterns = [
    # auth
    path("jwt/refresh", UserJWTRefreshAPI.as_view(), name="jwt-refresh"),
    # oauth
    path("kakao/callback", KakaoLoginAPI.as_view(), name="kakao-login-callback"),
    path("kakao/redirect", KakaoLoginRedirectAPI.as_view(), name="kakao-login-redirect"),
]
