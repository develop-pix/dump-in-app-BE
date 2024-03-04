import pytest

from dump_in.users.selectors.notifications import NotificationSelector

pytestmark = pytest.mark.django_db


class TestGetNotificationWithCategoryQuerysetByUserId:
    def setup_method(self):
        self.notification_selector = NotificationSelector()

    def test_get_notification_with_category_queryset_by_user_id_success_single_notification(self, valid_notification):
        notification_list = self.notification_selector.get_notification_with_category_queryset_by_user_id(
            user_id=valid_notification.user_id
        )

        assert notification_list[0] == valid_notification

    def test_get_notification_with_category_queryset_by_user_id_success_multiple_notification(self, valid_notification_list):
        notification_list = self.notification_selector.get_notification_with_category_queryset_by_user_id(
            user_id=valid_notification_list[0].user_id
        )

        assert notification_list.count() == len(valid_notification_list)

    def test_get_notification_with_category_queryset_by_user_id_fail_does_not_exist(self):
        notification_list = self.notification_selector.get_notification_with_category_queryset_by_user_id(user_id=999)

        assert notification_list.count() == 0

    def test_get_notification_with_category_queryset_by_user_id_fail_is_deleted(self, deleted_notification):
        notification_list = self.notification_selector.get_notification_with_category_queryset_by_user_id(
            user_id=deleted_notification.user_id
        )

        assert notification_list.count() == 0
