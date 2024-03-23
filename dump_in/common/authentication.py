from rest_framework_simplejwt.authentication import AuthUser, JWTAuthentication
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import Token
from rest_framework_simplejwt.utils import get_md5_hash_password

from dump_in.common.exception.exceptions import (
    AuthenticationFailedException,
    InvalidTokenException,
)


class CustomJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token: Token) -> AuthUser:
        try:
            user_id = validated_token[api_settings.USER_ID_CLAIM]
        except KeyError:
            raise InvalidTokenException("Token contained no recognizable user identification")

        try:
            user = self.user_model.objects.get(**{api_settings.USER_ID_FIELD: user_id})
        except self.user_model.DoesNotExist:
            raise AuthenticationFailedException("User not found")

        if user.is_active is False:
            raise AuthenticationFailedException("User is inactive")

        if api_settings.CHECK_REVOKE_TOKEN:
            if validated_token.get(api_settings.REVOKE_TOKEN_CLAIM) != get_md5_hash_password(user.password):
                raise AuthenticationFailedException("The user's password has been changed.")

        if user.is_deleted is True and user.deleted_at is not None:
            raise AuthenticationFailedException("User is deleted")

        return user

    def get_validated_token(self, raw_token: bytes) -> Token:
        messages = []

        for AuthToken in api_settings.AUTH_TOKEN_CLASSES:
            try:
                return AuthToken(raw_token)
            except TokenError:
                messages.append(AuthToken.token_type)

        raise InvalidTokenException(f"{messages} Token is invalid or expired")
