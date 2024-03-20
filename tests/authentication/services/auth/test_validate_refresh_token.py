from datetime import timedelta

import pytest
from rest_framework_simplejwt.tokens import RefreshToken

from dump_in.authentication.services.auth import AuthService
from dump_in.common.exception.exceptions import AuthenticationFailedException

pytestmark = pytest.mark.django_db


class TestValidateRefreshToken:
    def setup_method(self):
        self.auth_service = AuthService()

    def test_validate_refresh_token_success_access_token(self, valid_user):
        refresh = RefreshToken.for_user(user=valid_user)
        refresh_token, access_token = self.auth_service.validate_refresh_token(refresh=str(refresh))

        assert refresh_token is None
        assert access_token is not None

    def test_validate_refresh_token_success_refresh_token(self, valid_user):
        refresh = RefreshToken.for_user(user=valid_user)
        refresh.set_exp(lifetime=timedelta(seconds=300))
        refresh_token, access_token = self.auth_service.validate_refresh_token(refresh=str(refresh))

        assert refresh_token is not None
        assert access_token is not None

    def test_validate_refresh_token_fail_invalid_token(self):
        with pytest.raises(AuthenticationFailedException) as e:
            self.auth_service.validate_refresh_token("invalid_token")

        assert str(e.value) == "Token is invalid or expired"
        assert isinstance(e.value, AuthenticationFailedException)
