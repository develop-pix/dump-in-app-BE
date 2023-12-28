import pytest

from dump_in.users.services.notifications import NotificationService

pytestmark = pytest.mark.django_db


class TestSoftDeleteNotifications:
    def setup_method(self):
        self.service = NotificationService()

    def test_soft_delete_notifications_success(self, valid_notification):
        self.service.soft_delete_notifications(user_id=valid_notification.user_id)

        valid_notification.refresh_from_db()
        assert valid_notification.is_deleted
