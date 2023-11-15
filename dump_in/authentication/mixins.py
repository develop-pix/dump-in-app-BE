from typing import Type

from rest_framework.authentication import BaseAuthentication
from rest_framework.permissions import AllowAny, BasePermission, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from dump_in.authentication.services.auth import RefreshTokenAuthentication


class RefreshTokenAPIAuthMixin:
    authentication_classes: Type[BaseAuthentication] = (RefreshTokenAuthentication,)
    permission_classes: Type[BasePermission] = (IsAuthenticated,)


class JWTAPTAuthMixin:
    authentication_classes: Type[BaseAuthentication] = (JWTAuthentication,)
    permission_classes: Type[BasePermission] = (IsAuthenticated,)


class PublicAPIMixin:
    authentication_classes: Type[BaseAuthentication] = ()
    permission_classes: Type[BasePermission] = (AllowAny,)
