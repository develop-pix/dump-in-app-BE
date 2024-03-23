from typing import Optional

from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from dump_in.common.exception.exceptions import (
    AuthenticationFailedException,
    InvalidTokenException,
)
from dump_in.users.models import User
from dump_in.users.selectors.users import UserSelector


class AuthService:
    def generate_token(self, user: User) -> tuple[str, str]:
        refresh_token = RefreshToken.for_user(user=user)
        return str(refresh_token), str(refresh_token.access_token)

    def authenticate_user(self, username: str) -> User:
        user_selector = UserSelector()
        user = user_selector.get_user_by_username_for_auth(username=username)

        if user is None:
            raise AuthenticationFailedException("User is not found")

        if user.is_active is False:
            raise AuthenticationFailedException("User is not active")

        if user.is_deleted is True:
            user.is_deleted = False
            user.deleted_at = None
            user.save()

        return user

    def validate_refresh_token(self, refresh: str, is_refresh_generated: bool) -> tuple[Optional[str], str]:
        try:
            refresh_token = RefreshToken(refresh)
            access_token = str(refresh_token.access_token)

        except TokenError:
            raise InvalidTokenException("Token is invalid or expired")

        if is_refresh_generated is True:
            try:
                refresh.blacklist()
            except AttributeError:
                pass

            refresh_token.set_jti()
            refresh_token.set_exp()
            refresh_token.set_iat()

            refresh_token = str(refresh_token)
            return refresh_token, access_token
        return None, access_token
