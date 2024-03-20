import pytest

from dump_in.authentication.services.auth import AuthService
from dump_in.common.exception.exceptions import AuthenticationFailedException

pytestmark = pytest.mark.django_db


class TestAuthenticateUser:
    def setup_method(self):
        self.auth_service = AuthService()

    def test_authenticate_user_success(self, deleted_user):
        user = self.auth_service.authenticate_user(username=deleted_user.username)

        assert user.is_deleted is False
        assert not user.deleted_at

    def test_authenticate_user_fail_does_not_exist(self):
        with pytest.raises(AuthenticationFailedException) as e:
            self.auth_service.authenticate_user(username=None)

        assert str(e.value) == "User is not found"
        assert isinstance(e.value, AuthenticationFailedException)

    def test_authenticate_user_fail_user_inactive(self, inactive_user):
        with pytest.raises(AuthenticationFailedException) as e:
            self.auth_service.authenticate_user(username=inactive_user.username)

        assert str(e.value) == "User is not active"
        assert isinstance(e.value, AuthenticationFailedException)
