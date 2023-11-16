from typing import Any, Optional

import requests
from django.db import transaction
from django.db.models import BigAutoField
from django.utils import timezone

from dump_in.common.exception.exceptions import ValidationException
from dump_in.users.models import User
from dump_in.users.models import GenderChoices, User
from dump_in.users.selectors.users import UserSelector


class UserService:
    @transaction.atomic
    def get_or_create_social_user(self, email: str, nickname: str, social_id: str, birth: Any, gender: Optional[str], social_provider: int):
        user_selector = UserSelector()
        user = user_selector.get_user_by_username_for_auth(social_id)

        if not user:
            # Nickname exists check and Generate random nickname
            while user_selector.check_is_exists_user_by_nickname(nickname):
                response = requests.get(
                    "https://nickname.hwanmoo.kr",
                    params={
                        "format": "json",
                        "count": "1",
                        "max_length": "16",
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
        return user

    @transaction.atomic
    def get_and_update_user(self, user_id: BigAutoField, nickname: str) -> Optional[User]:
        user_selector = UserSelector()

        if user_selector.check_is_exists_user_by_nickname(nickname):
            raise ValidationException("Nickname already exists")

        user = user_selector.get_user_by_id(user_id)
        user.nickname = nickname
        user.save()
        return user

    @transaction.atomic
    def delete_user(self, user_id: BigAutoField):
        user_selector = UserSelector()
        user = user_selector.get_user_by_id(user_id)
        user.deleted_at = timezone.now()
        user.is_deleted = True
        user.save()
        return user
     