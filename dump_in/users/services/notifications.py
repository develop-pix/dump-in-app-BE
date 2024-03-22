from django.db import transaction

from dump_in.common.exception.exceptions import (
    NotFoundException,
    PermissionDeniedException,
)
from dump_in.users.models import Notification
from dump_in.users.selectors.notifications import NotificationSelector


class NotificationService:
    def __init__(self):
        self.notification_selector = NotificationSelector()

    @transaction.atomic
    def read_notification(self, notification_id: int, user_id) -> Notification:
        notification = self.notification_selector.get_notification_by_id(notification_id=notification_id)

        if notification is None:
            raise NotFoundException("Notification does not exist")

        if notification.user_id != user_id:
            raise PermissionDeniedException()

        notification.is_read = True
        notification.save()
        return notification

    @transaction.atomic
    def delete_notifications(self, user_id):
        notifications = self.notification_selector.get_notification_queryset_by_user_id(user_id=user_id)
        notifications.delete()
