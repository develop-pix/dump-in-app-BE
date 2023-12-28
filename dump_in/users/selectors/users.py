from datetime import timedelta
from typing import Optional

from django.db.models.query import QuerySet
from django.utils import timezone

from dump_in.users.models import User


class UserSelector:
    def get_user_by_id(self, user_id) -> Optional[User]:
        try:
            return User.objects.filter(id=user_id, is_deleted=False, deleted_at__isnull=True, is_active=True).get()
        except User.DoesNotExist:
            return None

    def get_user_by_username_for_auth(self, username: str) -> Optional[User]:
        try:
            return User.objects.filter(username=username).get()
        except User.DoesNotExist:
            return None

    def get_user_queryset_by_delated_at_lte_days(self, days: int) -> QuerySet[User]:
        return User.objects.filter(deleted_at__lte=timezone.now() - timedelta(days=days), is_deleted=True)

    def check_is_exists_user_by_nickname(self, nickname: str) -> bool:
        return User.objects.filter(nickname=nickname).exists()
