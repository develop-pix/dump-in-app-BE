from datetime import datetime

import requests
from django.db import transaction

from dump_in.users.models import GenderChoices, User
from dump_in.users.selectors.users import UserSelector


class UserService:
    @transaction.atomic
    def get_or_create_social_user(
        self, email: str | None, nickname: str, social_id: str, birth: str | None, gender: str | None, social_provider: str
    ) -> User:
        user_selector = UserSelector()
        user = user_selector.get_user_by_username(social_id)

        if not user:
            # Nickname exists check and Generate random nickname
            while user_selector.check_is_exists_user_by_nickname(nickname):
                response = requests.get(
                    "https://nickname.hwanmoo.kr",
                    params={
                        "format": "json",
                        "count": 1,
                        "max_length": 10,
                    },
                )
                nickname = response.json()["words"][0]

            # gender (F, M)
            if gender == "female":
                gender = GenderChoices.FEMALE
            elif gender == "male":
                gender = GenderChoices.MALE

            # birth datetime Convert
            if birth:
                birth = datetime.strptime(birth, "%Y%m%d")

            user = User.objects.create_social_user(
                email=email,
                nickname=nickname,
                social_id=social_id,
                social_provider=social_provider,
                birth=birth,
                gender=gender,
            )
        return user
