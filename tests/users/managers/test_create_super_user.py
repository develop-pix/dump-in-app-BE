import pytest
from django.db import transaction
from django.db.utils import IntegrityError

from dump_in.users.enums import AuthGroup, UserProvider
from dump_in.users.models import User

pytestmark = pytest.mark.django_db


class TestCreateSuperUser:
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

    def test_create_superuser_fail_duplicate_nickname(self, user_social_provider, group, valid_user):
        email = "test1234@test.com"
        nickname = valid_user.nickname
        username = "test1234"
        password = "test1234"

        with transaction.atomic():
            with pytest.raises(IntegrityError):
                User.objects.create_superuser(
                    email=email,
                    nickname=nickname,
                    username=username,
                    password=password,
                )
        assert User.objects.count() == 1

    def test_create_superuser_fail_duplicate_username(self, user_social_provider, group, valid_user):
        email = "test1234@test.com"
        nickname = "test1234"
        username = valid_user.username
        password = "test1234"

        with transaction.atomic():
            with pytest.raises(IntegrityError):
                User.objects.create_superuser(
                    email=email,
                    nickname=nickname,
                    username=username,
                    password=password,
                )
        assert User.objects.count() == 1
