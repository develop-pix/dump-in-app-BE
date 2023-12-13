import pytest

from dump_in.users.selectors.users import UserSelector

pytestmark = pytest.mark.django_db


class TestGetUserByUsernameForAuth:
    def setup_method(self):
        self.user_selector = UserSelector()

    def test_get_user_by_username_for_auth_success(self, valid_user):
        user = self.user_selector.get_user_by_username_for_auth(valid_user.username)
        assert user.username == valid_user.username

    def test_get_user_by_username_for_auth_fail_does_not_exist(self):
        user = self.user_selector.get_user_by_username_for_auth("test")
        assert user is None
