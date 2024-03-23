import pytest

from dump_in.authentication.services.auth import AuthService

pytestmark = pytest.mark.django_db


class TestGenerateToken:
    def setup_method(self):
        self.auth_service = AuthService()

    def test_generate_token_success(self, valid_user):
        token_data = self.auth_service.generate_token(user=valid_user)

        assert token_data["access_token"] is not None
        assert token_data["refresh_token"] is not None
