from datetime import datetime
from typing import Optional

from attrs import define
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from dump_in.common.exception.exceptions import (
    AuthenticationFailedException,
    InvalidTokenException,
)
from dump_in.users.models import User
from dump_in.users.selectors.users import UserSelector


@define
class Token:
    token: str
    expired_at: datetime


class AuthService:
    def _get_expired_at_by_token(self, token: RefreshToken) -> datetime:
        return datetime.fromtimestamp(token.get("exp"))

    def generate_token(self, user: User) -> dict[str, Token]:
        refresh_token = RefreshToken.for_user(user=user)
        access_token = Token(token=str(refresh_token.access_token), expired_at=self._get_expired_at_by_token(refresh_token.access_token))
        refresh_token = Token(token=str(refresh_token), expired_at=self._get_expired_at_by_token(refresh_token))
        return {"access_token": access_token, "refresh_token": refresh_token}

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

    def validate_refresh_token(self, refresh: RefreshToken, is_refresh_generated: bool) -> dict[str, Optional[Token]]:
        try:
            refresh_token = RefreshToken(refresh)
            access_token = Token(
                token=str(refresh_token.access_token), expired_at=self._get_expired_at_by_token(refresh_token.access_token)
            )
            data = {"access_token": access_token, "refresh_token": None}

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

            refresh_token = Token(token=str(refresh_token), expired_at=self._get_expired_at_by_token(refresh_token))
            data["refresh_token"] = refresh_token
        return data
