import pytest

from dump_in.users.selectors.user_mobile_tokens import UserMobileTokenSelector

pytestmark = pytest.mark.django_db


class TestGetUserMobileTokenByToken:
    def setup_method(self):
        self.user_mobile_token_selector = UserMobileTokenSelector()

    def test_get_user_mobile_token_by_token_success(self, valid_user_mobile_token):
        user_mobile_token = self.user_mobile_token_selector.get_user_mobile_token_by_token(token=valid_user_mobile_token.token)

        assert user_mobile_token.id == valid_user_mobile_token.id
        assert user_mobile_token.token == valid_user_mobile_token.token
        assert user_mobile_token.user_id == valid_user_mobile_token.user_id

    def test_get_user_mobile_token_by_token_fail_does_not_exist(self):
        user_mobile_token = self.user_mobile_token_selector.get_user_mobile_token_by_token(token="test_token")

        assert user_mobile_token is None
