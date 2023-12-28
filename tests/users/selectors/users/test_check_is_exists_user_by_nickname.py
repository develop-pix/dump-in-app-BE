import pytest

from dump_in.users.selectors.users import UserSelector

pytestmark = pytest.mark.django_db


class TestCheckIsExistsUserByNickname:
    def setup_method(self):
        self.user_selector = UserSelector()

    def test_check_is_exists_user_by_nickname_success(self, valid_user):
        is_check = self.user_selector.check_is_exists_user_by_nickname(valid_user.nickname)

        assert is_check is True

    def test_check_is_exists_user_by_nickname_fail_not_exists(self):
        is_check = self.user_selector.check_is_exists_user_by_nickname("test")

        assert is_check is False
