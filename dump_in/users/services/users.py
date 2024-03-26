from datetime import datetime
from typing import Optional, Union

import requests
from django.db import transaction
from django.utils import timezone

from dump_in.common.exception.exceptions import ValidationException
from dump_in.users.models import User
from dump_in.users.selectors.users import UserSelector
from dump_in.users.services.user_mobile_tokens import UserMobileTokenService


class UserService:
    def __init__(self):
        self.user_selector = UserSelector()

    @transaction.atomic
    def create_social_user(
        self,
        email: str,
        nickname: Optional[str],
        social_id: str,
        birth: Union[str, datetime, None],
        gender: Optional[str],
        social_provider: int,
        mobile_token: Optional[str],
    ) -> User:
        user = self.user_selector.get_user_by_username_for_auth(username=social_id)

        if user is None:
            # Nickname exists check and Generate random nickname
            while nickname is None or self.user_selector.check_is_exists_user_by_nickname(nickname=nickname):
                response = requests.get(
                    "https://nickname.hwanmoo.kr",
                    params={
                        "format": "json",
                        "count": "1",
                        "max_length": "10",
                    },
                )
                nickname = response.json()["words"][0]

            user = User.objects.create_social_user(
                email=email,
                nickname=nickname,
                social_id=social_id,
                social_provider=social_provider,
                birth=birth,
                gender=gender,
            )

            if mobile_token is not None:
                user_mobile_token_service = UserMobileTokenService()
                user_mobile_token_service.update_user_mobile_token(user_id=user.id, token=mobile_token)

        return user

    @transaction.atomic
    def update_user(self, user_id, nickname: str) -> User:
        if self.user_selector.check_is_exists_user_by_nickname(nickname=nickname):
            raise ValidationException("Nickname already exists")

        user = self.user_selector.get_user_by_id(user_id=user_id)

        user.nickname = nickname
        user.save()
        return user

    @transaction.atomic
    def soft_delete_user(self, user_id) -> User:
        user = self.user_selector.get_user_by_id(user_id=user_id)

        user.deleted_at = timezone.now()
        user.is_deleted = True
        user.save()
        return user

    @transaction.atomic()
    def hard_bulk_delete_users(self, days: int):
        users = self.user_selector.get_user_queryset_by_delated_at_lte_days(days=days)
        users.delete()
