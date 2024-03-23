import pytest
from rest_framework_simplejwt.tokens import RefreshToken

from dump_in.authentication.services.auth import AuthService

pytestmark = pytest.mark.django_db


# @TODO: Blacklist refresh token Test
class TestValidateRefreshToken:
    def setup_method(self):
        self.auth_service = AuthService()

    def test_validate_refresh_token_success_access_token(self, valid_user):
        refresh = RefreshToken.for_user(user=valid_user)
        token_data = self.auth_service.validate_refresh_token(
            refresh=str(refresh),
            is_refresh_generated=False,
        )

        assert token_data["access_token"] is not None
        assert token_data["refresh_token"] is None

    def test_validate_refresh_token_success_refresh_token(self, valid_user):
        refresh = RefreshToken.for_user(user=valid_user)
        token_data = self.auth_service.validate_refresh_token(
            refresh=str(refresh),
            is_refresh_generated=True,
        )

        assert token_data["access_token"] is not None
        assert token_data["refresh_token"] is not None
