import pytest

from dump_in.users.selectors.users import UserSelector

pytestmark = pytest.mark.django_db


class TestGetUserById:
    def setup_method(self):
        self.user_selector = UserSelector()

    def test_get_user_by_id_success(self, valid_user):
        user = self.user_selector.get_user_by_id(valid_user.id)

        assert user == valid_user

    def test_get_user_by_id_fail_does_not_exist(self):
        user = self.user_selector.get_user_by_id(9999)

        assert user is None

    def test_get_user_by_id_fail_deleted(self, deleted_user):
        user = self.user_selector.get_user_by_id(deleted_user.id)

        assert user is None

    def test_get_user_by_id_fail_inactive(self, inactive_user):
        user = self.user_selector.get_user_by_id(inactive_user.id)

        assert user is None
