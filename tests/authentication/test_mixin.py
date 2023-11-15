from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from dump_in.authentication.mixins import (
    JWTAPTAuthMixin,
    PublicAPIMixin,
    RefreshTokenAPIAuthMixin,
)


class RefreshTokenAPIAuthTestView(RefreshTokenAPIAuthMixin, APIView):
    def get(self, request):
        return Response({"message": "Test Success!"})


class JWTAPTAuthTestView(JWTAPTAuthMixin, APIView):
    def get(self, request):
        return Response({"message": "Test Success!"})


class PublicAPITestView(PublicAPIMixin, APIView):
    def get(self, request):
        return Response({"message": "Hello World!"})


def test_refresh_token_auth_mixin_unauthenticated(api_factory):
    view = RefreshTokenAPIAuthTestView.as_view()

    request = api_factory.get("/api/test")
    response = view(request)

    assert response.status_code == 401


def test_jwt_auth_mixin_unauthenticated(api_factory):
    view = JWTAPTAuthTestView.as_view()

    request = api_factory.get("/api/test")
    response = view(request)

    assert response.status_code == 401


def test_jwt_auth_mixin_authenticated(api_factory, new_users):
    view = JWTAPTAuthTestView.as_view()
    access_token = RefreshToken.for_user(new_users).access_token

    request = api_factory.get("/api/test")
    request.META["HTTP_AUTHORIZATION"] = f"Bearer {access_token}"
    response = view(request)

    assert response.status_code == 200


def test_public_api_mixin_unauthenticated(api_factory):
    view = PublicAPITestView.as_view()

    request = api_factory.get("/api/test")
    response = view(request)

    assert response.status_code == 200
