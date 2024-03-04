import pytest

from dump_in.users.selectors.notifications import NotificationSelector

pytestmark = pytest.mark.django_db


class TestGetUnreadNotificationCountByUserId:
    def setup_method(self):
        self.notification_selector = NotificationSelector()

    def test_get_unread_notification_count_by_user_id_success_single_notification(self, valid_notification):
        count = self.notification_selector.get_unread_notification_count_by_user_id(user_id=valid_notification.user_id)

        assert count == 1

    def test_get_unread_notification_count_by_user_id_success_multiple_notification(self, valid_notification_list):
        count = self.notification_selector.get_unread_notification_count_by_user_id(user_id=valid_notification_list[0].user_id)

        assert count == 10

    def test_get_unread_notification_count_by_user_id_fail_does_not_exist(self):
        count = self.notification_selector.get_unread_notification_count_by_user_id(user_id=999)

        assert count == 0

    def test_get_unread_notification_count_by_user_id_fail_is_deleted(self, deleted_notification):
        count = self.notification_selector.get_unread_notification_count_by_user_id(user_id=deleted_notification.user_id)

        assert count == 0

    def test_get_unread_notification_count_by_user_id_fail_is_read(self, read_notification):
        count = self.notification_selector.get_unread_notification_count_by_user_id(user_id=read_notification.user_id)

        assert count == 0
