import pytest

from dump_in.users.selectors.notifications import NotificationSelector

pytestmark = pytest.mark.django_db


class TestGetNotificationById:
    def setup_method(self):
        self.notification_selector = NotificationSelector()

    def test_get_notification_by_id_success(self, valid_notification):
        notification = self.notification_selector.get_notification_by_id(notification_id=valid_notification.id)

        assert notification == valid_notification

    def test_get_notification_by_id_fail_does_not_exist(self):
        notification = self.notification_selector.get_notification_by_id(notification_id=999)

        assert notification is None

    def test_get_notification_by_id_fail_is_deleted(self, deleted_notification):
        notification = self.notification_selector.get_notification_by_id(notification_id=deleted_notification.id)

        assert notification is None
