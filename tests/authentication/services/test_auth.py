import pytest

from dump_in.authentication.services.auth import AuthService
from dump_in.common.exception.exceptions import AuthenticationFailedException


class TestAuthService:
    def setup_method(self):
        self.auth_service = AuthService()

    def test_generate_token_success(self, new_users):
        refresh_token, access_token = self.auth_service.generate_token(new_users)

        assert refresh_token is not None
        assert access_token is not None

    def test_authenticate_user_success(self, new_users):
        username = "test11"
        user = self.auth_service.authenticate_user(username)

        assert new_users.username == user.username

    def test_authenticate_user_success_deleted_user(self, deleted_users):
        username = "test12"
        user = self.auth_service.authenticate_user(username)

        assert deleted_users.username == user.username
        assert not user.is_deleted
        assert user.deleted_at is None

    def test_authenticate_user_fail_user_is_not_active(self, not_active_users):
        username = "test13"

        with pytest.raises(AuthenticationFailedException) as e:
            self.auth_service.authenticate_user(username)

        assert str(e.value) == "User is not active"
        assert isinstance(e.value, AuthenticationFailedException)
