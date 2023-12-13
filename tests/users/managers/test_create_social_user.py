import pytest
from django.db import transaction
from django.db.utils import IntegrityError

from dump_in.users.enums import AuthGroup, UserProvider
from dump_in.users.models import User

pytestmark = pytest.mark.django_db


class TestCreateSocialUser:
    def test_create_social_user_success(self, user_social_provider, group):
        email = "test1234@test.com"
        nickname = "test1234"
        social_id = "test1234"
        social_provider = UserProvider.KAKAO.value

        user = User.objects.create_social_user(
            email=email,
            nickname=nickname,
            social_id=social_id,
            social_provider=social_provider,
        )

        assert user.email == email
        assert user.nickname == nickname
        assert user.username == social_id
        assert user.user_social_provider_id == UserProvider.KAKAO.value
        assert user.groups.first().id == AuthGroup.NORMAL_USER.value

    def test_create_social_user_fail_duplicate_nickname(self, user_social_provider, group, valid_user):
        email = "test1234@test.com"
        nickname = valid_user.nickname
        social_id = "test1234"
        social_provider = UserProvider.KAKAO.value

        with transaction.atomic():
            with pytest.raises(IntegrityError):
                User.objects.create_social_user(
                    email=email,
                    nickname=nickname,
                    social_id=social_id,
                    social_provider=social_provider,
                )

        assert User.objects.count() == 1

    def test_create_social_user_fail_duplicate_social_id(self, user_social_provider, group, valid_user):
        email = "test1234@test.com"
        nickname = valid_user.nickname
        social_id = valid_user.username
        social_provider = UserProvider.KAKAO.value

        with transaction.atomic():
            with pytest.raises(IntegrityError):
                User.objects.create_social_user(
                    email=email,
                    nickname=nickname,
                    social_id=social_id,
                    social_provider=social_provider,
                )
        assert User.objects.count() == 1
