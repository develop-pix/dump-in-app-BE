import pytest

from dump_in.common.exception.exceptions import ValidationException
from dump_in.users.enums import UserProvider
from dump_in.users.services.users import UserService

pytestmark = pytest.mark.django_db


class TestUserService:
    def setup_method(self):
        self.service = UserService()

    def test_get_or_create_social_user_success(self, group, user_social_provider):
        user = self.service.get_and_create_social_user(
            email="test@test.com",
            nickname="test_nickname",
            social_id="test_social_id",
            birth="2023-01-01",
            gender="F",
            social_provider=UserProvider.KAKAO.value,
        )
        assert user.email == "test@test.com"
        assert user.nickname == "test_nickname"
        assert user.username == "test_social_id"
        assert user.gender == "F"
        assert user.birth == "2023-01-01"

    def test_get_and_update_user_success(self, group, user_social_provider, new_users):
        user = self.service.get_and_update_user(
            user_id=11,
            nickname="test_nickname",
        )
        assert user.id == 11
        assert user.nickname == "test_nickname"

    def test_get_and_update_user_fail_exist_nickname(self, group, user_social_provider, new_users):
        with pytest.raises(ValidationException) as e:
            self.service.get_and_update_user(
                user_id=12,
                nickname="test11",
            )
        assert e.value.detail == "Nickname already exists"
        assert e.value.status_code == 400

    def test_soft_delete_user_success(self, group, user_social_provider, new_users):
        user = self.service.soft_delete_user(
            user_id=11,
        )
        assert user.is_deleted is True
        assert user.deleted_at is not None

    def test_hard_delete_user_success(self, group, user_social_provider, deleted_users):
        user = self.service.hard_bulk_delete_users(
            days=10,
        )
        assert user is None
