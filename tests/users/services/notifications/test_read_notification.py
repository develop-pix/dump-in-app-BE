import pytest

from dump_in.common.exception.exceptions import (
    NotFoundException,
    PermissionDeniedException,
)
from dump_in.users.services.notifications import NotificationService

pytestmark = pytest.mark.django_db


class TestReadNotification:
    def setup_method(self):
        self.service = NotificationService()

    def test_read_notification_success(self, valid_notification):
        notification = self.service.read_notification(notification_id=valid_notification.id, user_id=valid_notification.user_id)

        assert notification.is_read is True

    def test_read_notification_fail_does_not_exist(self, valid_user):
        with pytest.raises(NotFoundException) as e:
            self.service.read_notification(notification_id=999, user_id=valid_user.id)

        assert str(e.value) == "Notification does not exist"

    def test_read_notification_fail_permission_denied(self, valid_notification):
        with pytest.raises(PermissionDeniedException) as e:
            self.service.read_notification(notification_id=valid_notification.id, user_id=999)

        assert str(e.value) == "You do not have permission to perform this action."
