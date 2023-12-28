from typing import Optional

from django.db.models import QuerySet

from dump_in.users.models import Notification


class NotificationSelector:
    def get_notification_by_id(self, notification_id: int) -> Optional[Notification]:
        try:
            return Notification.objects.filter(id=notification_id, is_deleted=False).get()
        except Notification.DoesNotExist:
            return None

    def get_notification_with_category_queryset_by_user_id(self, user_id) -> QuerySet[Notification]:
        return Notification.objects.select_related("category").filter(user_id=user_id, is_deleted=False)

    def get_notification_queryset_by_user_id(self, user_id) -> QuerySet[Notification]:
        return Notification.objects.filter(user_id=user_id, is_deleted=False)

    def get_unread_notification_count_by_user_id(self, user_id) -> int:
        return Notification.objects.filter(user_id=user_id, is_read=False, is_deleted=False).count()

    def check_unread_notification_by_user_id(self, user_id) -> bool:
        return Notification.objects.filter(user_id=user_id, is_read=False, is_deleted=False).exists()
