import pytest

from dump_in.authentication.services.auth import AuthServices
from dump_in.common.exception.exceptions import AuthenticationFailedException
from dump_in.common.response import create_response


class TestAuthService:
    def setup_method(self):
        self.auth_service = AuthServices()

    def test_generate_token_success(self, new_users):
        refresh_token, access_token = self.auth_service.generate_token(new_users)

        assert refresh_token is not None
        assert access_token is not None

    def test_generate_access_token_success(self, new_users):
        refresh_token, access_token = self.auth_service.generate_token(new_users)
        access_token = self.auth_service.generate_access_token(refresh_token)

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

    def test_set_refresh_token_cookie_success(self, new_users):
        response = create_response(data="test", status_code=200)
        refresh_token, access_token = self.auth_service.generate_token(new_users)

        self.auth_service.set_refresh_token_cookie(response, refresh_token)

        assert response.cookies.get("refresh_token").value == refresh_token

    def test_delete_refresh_token_success(self, new_users):
        response = create_response(data="test", status_code=200)
        refresh_token, access_token = self.auth_service.generate_token(new_users)
        self.auth_service.set_refresh_token_cookie(response, refresh_token)
        assert response.cookies.get("refresh_token").value == refresh_token

        self.auth_service.delete_refresh_token(refresh_token, response)
        assert response.cookies.get("refresh_token").value == ""
