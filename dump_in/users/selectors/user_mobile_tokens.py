from typing import Optional

from dump_in.users.models import UserMobileToken


class UserMobileTokenSelector:
    def get_user_mobile_token_by_token(self, token: str) -> Optional[UserMobileToken]:
        try:
            return UserMobileToken.objects.filter(token=token).get()
        except UserMobileToken.DoesNotExist:
            return None

    def check_is_exists_user_mobile_token_by_token(self, token: str) -> bool:
        return UserMobileToken.objects.filter(token=token).exists()
