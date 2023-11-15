import pytest

from dump_in.common.constants import (
    AUTH_GROUP_ADMIN,
    AUTH_GROUP_NOMAL_USER,
    AUTH_GROUP_SUPER_USER,
    USER_SOCIAL_PROVIDER_EMAIL,
    USER_SOCIAL_PROVIDER_KAKAO,
)
from dump_in.users.models import User

pytestmark = pytest.mark.django_db


class TestUserManager:
    def test_create_social_user_success(self, user_social_provider, group):
        email = "test1234@test.com"
        nickname = "test1234"
        social_id = "test1234"
        social_provider = USER_SOCIAL_PROVIDER_KAKAO

        user = User.objects.create_social_user(
            email=email,
            nickname=nickname,
            social_id=social_id,
            social_provider=social_provider,
        )

        assert user.email == email
        assert user.nickname == nickname
        assert user.username == social_id
        assert user.user_social_provider_id == USER_SOCIAL_PROVIDER_KAKAO
        assert user.groups.first().id == AUTH_GROUP_NOMAL_USER

    def test_create_superuser_success(self, user_social_provider, group):
        email = "test1234@test.com"
        nickname = "test1234"
        username = "test1234"
        password = "test1234"

        user = User.objects.create_superuser(
            email=email,
            nickname=nickname,
            username=username,
            password=password,
        )

        assert user.email == email
        assert user.nickname == nickname
        assert user.username == username
        assert user.user_social_provider_id == USER_SOCIAL_PROVIDER_EMAIL
        assert user.groups.first().id == AUTH_GROUP_SUPER_USER

    def test_create_admin_success(self, user_social_provider, group):
        email = "test1234@test.com"
        nickname = "test1234"
        username = "test1234"
        password = "test1234"

        user = User.objects.create_admin(
            email=email,
            nickname=nickname,
            username=username,
            password=password,
        )

        assert user.email == email
        assert user.nickname == nickname
        assert user.username == username
        assert user.user_social_provider_id == USER_SOCIAL_PROVIDER_EMAIL
        assert user.groups.first().id == AUTH_GROUP_ADMIN