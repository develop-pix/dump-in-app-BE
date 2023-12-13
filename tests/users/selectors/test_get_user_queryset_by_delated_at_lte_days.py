import pytest

from dump_in.users.selectors.users import UserSelector

pytestmark = pytest.mark.django_db


class TestGetUserQuerysetByDelatedAtLteDays:
    def setup_method(self):
        self.user_selector = UserSelector()

    def test_get_user_queryset_by_delated_at_lte_days_success(self, deleted_user):
        users = self.user_selector.get_user_queryset_by_delated_at_lte_days(14)
        assert users.count() == 1
        assert users[0].id == deleted_user.id

    def test_get_user_queryset_by_delated_at_lte_days_fail_not_deleted(self, valid_user):
        users = self.user_selector.get_user_queryset_by_delated_at_lte_days(30)
        assert users.count() == 0
