from django.db import transaction

from dump_in.common.exception.exceptions import NotFoundException, ValidationException
from dump_in.users.models import UserMobileToken
from dump_in.users.selectors.user_mobile_tokens import UserMobileTokenSelector


class UserMobileTokenService:
    def __init__(self):
        self.user_mobile_token_selector = UserMobileTokenSelector()

    @transaction.atomic
    def create_user_mobile_token(self, token: str) -> UserMobileToken:
        if self.user_mobile_token_selector.check_is_exists_user_mobile_token_by_token(token=token):
            raise ValidationException("Token already exists")

        user_mobile_token = UserMobileToken.objects.create(token=token)

        return user_mobile_token

    @transaction.atomic
    def update_user_mobile_token(self, user_id, token: str) -> UserMobileToken:
        user_mobile_token = self.user_mobile_token_selector.get_user_mobile_token_by_token(token=token)

        if user_mobile_token is None:
            raise NotFoundException("Token does not exist")

        user_mobile_token.user_id = user_id
        user_mobile_token.save()

        return user_mobile_token
