import pytest

from dump_in.users.models import Notification
from dump_in.users.services.notifications import NotificationService

pytestmark = pytest.mark.django_db


class TestDeleteNotifications:
    def setup_method(self):
        self.notification_service = NotificationService()

    def test_delete_notifications_success(self, valid_notification):
        self.notification_service.delete_notifications(user_id=valid_notification.user_id)

        assert Notification.objects.filter(id=valid_notification.id).first() is None
