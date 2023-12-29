import pytest

from dump_in.common.exception.exceptions import NotFoundException
from dump_in.users.services.user_mobile_tokens import UserMobileTokenService

pytestmark = pytest.mark.django_db


class TestUpdateUserMobileToken:
    def setup_method(self):
        self.user_mobile_token_service = UserMobileTokenService()

    def test_update_user_mobile_token_success(self, valid_user_mobile_token, valid_user):
        user_mobile_token = self.user_mobile_token_service.update_user_mobile_token(
            user_id=valid_user.id, token=valid_user_mobile_token.token
        )

        assert user_mobile_token.id == valid_user_mobile_token.id
        assert user_mobile_token.token == valid_user_mobile_token.token
        assert user_mobile_token.user_id == valid_user.id

    def test_update_user_mobile_token_fail_does_not_exist(self):
        with pytest.raises(NotFoundException) as e:
            self.user_mobile_token_service.update_user_mobile_token(user_id=1, token="test_token")

        assert str(e.value) == "Token does not exist"
        assert isinstance(e.value, NotFoundException)
