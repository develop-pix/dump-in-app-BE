import pytest
from rest_framework_simplejwt.tokens import RefreshToken


class IsAuthenticateTestCase:
    @pytest.fixture(autouse=True)
    def set_up(self, api_client):
        self.client = api_client

    def obtain_token(self, new_users):
        access_token = RefreshToken.for_user(new_users).access_token
        return str(access_token)

    def authenticate_with_token(self, access_token):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + access_token)
