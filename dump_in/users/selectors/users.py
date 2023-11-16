from typing import Optional, Union

from django.db.models import BigAutoField

from dump_in.users.models import User


class UserSelector:
    def get_user_by_id(self, user_id: Union[BigAutoField, str, int]) -> Optional[User]:
        try:
            return User.objects.filter(id=user_id, is_deleted=False, deleted_at__isnull=True).get()
        except User.DoesNotExist:
            return None

    def get_user_by_username_for_auth(self, username: str) -> Optional[User]:
        try:
            return User.objects.filter(username=username).get()
        except User.DoesNotExist:
            return None

    def get_user_by_username(self, username: str) -> Optional[User]:
        try:
            return User.objects.filter(username=username, is_deleted=False, deleted_at__isnull=True).get()
        except User.DoesNotExist:
            return None

    def check_is_exists_user_by_nickname(self, nickname: str) -> bool:
        return User.objects.filter(nickname=nickname, is_deleted=False, deleted_at__isnull=True).exists()
