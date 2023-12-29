import pytest

from dump_in.users.selectors.user_mobile_tokens import UserMobileTokenSelector

pytestmark = pytest.mark.django_db


class TestCheckIsExistsUserMobileTokenByToken:
    def setup_method(self):
        self.user_mobile_token_selector = UserMobileTokenSelector()

    def test_check_is_exists_user_mobile_token_by_token_success(self, valid_user_mobile_token):
        result = self.user_mobile_token_selector.check_is_exists_user_mobile_token_by_token(token=valid_user_mobile_token.token)

        assert result is True

    def test_check_is_exists_user_mobile_token_by_token_fail_does_not_exist(self):
        result = self.user_mobile_token_selector.check_is_exists_user_mobile_token_by_token(token="test_token")

        assert result is False
