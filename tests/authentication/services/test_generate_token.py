import pytest

from dump_in.authentication.services.auth import AuthService

pytestmark = pytest.mark.django_db


class TestGenerateToken:
    def setup_method(self):
        self.auth_service = AuthService()

    def test_generate_token_success(self, valid_review):
        refresh_token, access_token = self.auth_service.generate_token(valid_review)

        assert refresh_token is not None
        assert access_token is not None
