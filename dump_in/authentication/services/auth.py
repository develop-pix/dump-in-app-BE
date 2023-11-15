import jwt
from django.conf import settings
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken, Token

from dump_in.common.exception.exceptions import AuthenticationFailedException
from dump_in.users.models import User
from dump_in.users.selectors.users import UserSelector


class AuthServices:
    def generate_token(self, user: User) -> Token:
        refresh_token = RefreshToken.for_user(user)
        return str(refresh_token), str(refresh_token.access_token)

    def generate_access_token(self, refresh_token: Token) -> Token:
        refresh_token = RefreshToken(refresh_token)
        return str(refresh_token.access_token)

    def authenticate_user(self, username: str) -> User:
        user_selector = UserSelector()
        user = user_selector.get_user_by_username_for_auth(username)

        if user is None:
            raise AuthenticationFailedException("User is not found")

        if user.is_active is False:
            raise AuthenticationFailedException("User is not active")

        if user.is_deleted is True:
            user.is_deleted = False
            user.deleted_at = None
            user.save()

        return user

    def set_refresh_token_cookie(self, response: Response, refresh_token: Token) -> Response:
        response.set_cookie(
            key=settings.SIMPLE_JWT["AUTH_COOKIE"],
            value=refresh_token,
            max_age=settings.SIMPLE_JWT["AUTH_COOKIE_EXPIRES"],
            httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
            samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
            secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
        )

    def delete_refresh_token(self, refresh_token: Token, response: Response) -> Response:
        refresh_token = RefreshToken(refresh_token)
        refresh_token.blacklist()
        response.delete_cookie("refresh_token")


class RefreshTokenAuthentication(JWTAuthentication):
    def authenticate(self, request: Request):
        refresh_token = request.COOKIES.get(settings.SIMPLE_JWT["AUTH_COOKIE"]) or None

        if refresh_token is None:
            raise AuthenticationFailedException("Refresh token is not in cookie")

        self.get_validated_refresh_token(refresh_token)

        decoded_jwt = jwt.decode(
            jwt=refresh_token,
            key=settings.SIMPLE_JWT["SIGNING_KEY"],
            algorithms=["HS256"],
        )
        user = self.get_user(decoded_jwt)

        return user, refresh_token

    def get_validated_refresh_token(self, refresh_token: bytes):
        try:
            token_obj = RefreshToken(refresh_token)
            token_obj.check_blacklist()
        except TokenError as e:
            raise AuthenticationFailedException(str(e))

    def get_user(self, decoded_jwt: dict) -> User:
        try:
            user = self.user_model.objects.get(**{settings.SIMPLE_JWT["USER_ID_FIELD"]: decoded_jwt.get("user_id")})
        except self.user_model.DoesNotExist:
            raise AuthenticationFailedException("User is not found")

        if not user.is_active:
            raise AuthenticationFailedException("User is not active")

        return user
