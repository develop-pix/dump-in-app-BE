import pytest

from dump_in.authentication.services.auth import AuthService
from dump_in.common.exception.exceptions import AuthenticationFailedException


class TestAuthenticateUser:
    def setup_method(self):
        self.auth_service = AuthService()

    def test_authenticate_user_success(self, valid_user):
        user = self.auth_service.authenticate_user(valid_user.username)

        assert valid_user.username == user.username

    def test_authenticate_user_success_deleted_user(self, deleted_user):
        user = self.auth_service.authenticate_user(deleted_user.username)

        assert deleted_user.username == user.username
        assert not user.is_deleted
        assert user.deleted_at is None

    def test_authenticate_user_fail_user_is_not_active(self, inactive_user):
        with pytest.raises(AuthenticationFailedException) as e:
            self.auth_service.authenticate_user(inactive_user.username)

        assert str(e.value) == "User is not active"
        assert isinstance(e.value, AuthenticationFailedException)
