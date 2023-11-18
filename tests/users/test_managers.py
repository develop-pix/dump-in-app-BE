import pytest

from dump_in.users.enums import AuthGroup, UserProvider
from dump_in.users.models import User

pytestmark = pytest.mark.django_db


class TestUserManager:
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
        assert user.user_social_provider_id == UserProvider.EMAIL.value
        assert user.groups.first().id == AuthGroup.SUPER_USER.value

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
        assert user.user_social_provider_id == UserProvider.EMAIL.value
        assert user.groups.first().id == AuthGroup.ADMIN.value
