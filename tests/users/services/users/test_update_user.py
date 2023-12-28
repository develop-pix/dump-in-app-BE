import pytest

from dump_in.common.exception.exceptions import ValidationException
from dump_in.users.services.users import UserService

pytestmark = pytest.mark.django_db


class TestUpdateUser:
    def setup_method(self):
        self.service = UserService()

    def test_update_user_success(self, group, user_social_provider, valid_user):
        user = self.service.update_user(
            user_id=valid_user.id,
            nickname="test_nickname",
        )

        assert user.id == valid_user.id
        assert user.nickname == "test_nickname"

    def test_update_user_fail_exist_nickname(self, group, user_social_provider, valid_user):
        with pytest.raises(ValidationException) as e:
            self.service.update_user(
                user_id=valid_user.id,
                nickname=valid_user.nickname,
            )

        assert e.value.detail == "Nickname already exists"
        assert e.value.status_code == 400
