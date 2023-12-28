import pytest

from dump_in.users.selectors.notifications import NotificationSelector

pytestmark = pytest.mark.django_db


class TestCheckUnreadNotifiactionByUserId:
    def setup_method(self):
        self.notification_selector = NotificationSelector()

    def test_check_unread_notification_by_user_id_success(self, valid_notification):
        is_unread = self.notification_selector.check_unread_notification_by_user_id(user_id=valid_notification.user_id)

        assert is_unread is True

    def test_check_unread_notification_by_user_id_fail_does_not_exist(self):
        is_unread = self.notification_selector.check_unread_notification_by_user_id(user_id=999)

        assert is_unread is False

    def test_check_unread_notification_by_user_id_fail_is_deleted(self, deleted_notification):
        is_unread = self.notification_selector.check_unread_notification_by_user_id(user_id=deleted_notification.user_id)

        assert is_unread is False

    def test_check_unread_notification_by_user_id_fail_is_read(self, read_notification):
        is_unread = self.notification_selector.check_unread_notification_by_user_id(user_id=read_notification.user_id)

        assert is_unread is False
