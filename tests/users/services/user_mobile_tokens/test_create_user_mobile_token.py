import pytest

from dump_in.common.exception.exceptions import ValidationException
from dump_in.users.services.user_mobile_tokens import UserMobileTokenService

pytestmark = pytest.mark.django_db


class TestCreateUserMobileToken:
    def setup_method(self):
        self.user_mobile_token_service = UserMobileTokenService()

    def test_create_user_mobile_token_success(self):
        user_mobile_token = self.user_mobile_token_service.create_user_mobile_token(token="test_token")

        assert user_mobile_token.id is not None
        assert user_mobile_token.token == "test_token"
        assert user_mobile_token.user_id is None

    def test_create_user_mobile_token_fail_already_exists(self, valid_user_mobile_token):
        with pytest.raises(ValidationException) as e:
            self.user_mobile_token_service.create_user_mobile_token(token=valid_user_mobile_token.token)

        assert str(e.value) == "Token already exists"
        assert isinstance(e.value, ValidationException)
