import json

import jwt
import pytest
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.test import override_settings

from dump_in.authentication.services.apple_oauth import (
    AppleLoginFlowService,
    apple_login_get_credentials,
)
from dump_in.common.exception.exceptions import AuthenticationFailedException


class TestAppleLoginFlowService:
    def setup_method(self):
        self.service = AppleLoginFlowService()

    def test_get_authorization_url_success(self, mocker):
        mock_response = mocker.Mock()
        mock_response.status_code = 200
        mock_response.url = "https://appleid.apple.com/auth/authorize"

        mocker.patch("dump_in.authentication.services.apple_oauth.requests.get", return_value=mock_response)

        authorization_url = self.service.get_authorization_url()
        assert authorization_url == "https://appleid.apple.com/auth/authorize"

    def test_get_authorization_url_fail_response_not_200(self, mocker):
        mock_response = mocker.Mock()
        mock_response.status_code = 401
        mock_response.url = "https://appleid.apple.com/auth/authorize"

        mocker.patch("dump_in.authentication.services.apple_oauth.requests.get", return_value=mock_response)

        with pytest.raises(AuthenticationFailedException) as e:
            self.service.get_authorization_url()

        assert e.value.detail == "Failed to get authorization url from Apple."
        assert e.value.status_code == 401

    def test_get_id_token_success(self, mocker):
        id_token = """
        {
            "sub": "001",
            "email": "email"
        }
        """
        id_token_encoded = jwt.encode(json.loads(id_token), "", algorithm="HS256")

        mock_response = mocker.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"id_token": id_token_encoded}

        mocker.patch("dump_in.authentication.services.apple_oauth.requests.post", return_value=mock_response)

        token = self.service.get_id_token("test_code")

        assert token is not None

    def test_get_id_token_fail_response_not_200(self, mocker):
        mock_response = mocker.Mock()
        mock_response.status_code = 401
        mock_response.side_effect = AuthenticationFailedException("Failed to get access token from Apple.")

        mocker.patch("dump_in.authentication.services.apple_oauth.requests.post", return_value=mock_response)

        with pytest.raises(AuthenticationFailedException) as e:
            self.service.get_id_token("test_code")

        assert e.value.status_code == 401
        assert e.value.detail == "Failed to get access token from Apple."

    def test_apple_login_get_credentials_success(self):
        credentials = apple_login_get_credentials()

        assert credentials.team_id == settings.APPLE_TEAM_ID
        assert credentials.client_id == settings.APPLE_CLIENT_ID
        assert credentials.key_id == settings.APPLE_KEY_ID
        assert credentials.private_key == settings.APPLE_PRIVATE_KEY

    @override_settings(APPLE_TEAM_ID=None)
    def test_apple_login_get_credentials_fail_team_id_missing(self):
        with pytest.raises(ImproperlyConfigured) as e:
            apple_login_get_credentials()

        assert str(e.value) == "APPLE_TEAM_ID missing in env."

    @override_settings(APPLE_CLIENT_ID=None)
    def test_apple_login_get_credentials_fail_client_id_missing(self):
        with pytest.raises(ImproperlyConfigured) as e:
            apple_login_get_credentials()

        assert str(e.value) == "APPLE_API_KEY missing in env."

    @override_settings(APPLE_KEY_ID=None)
    def test_apple_login_get_credentials_fail_key_id_missing(self):
        with pytest.raises(ImproperlyConfigured) as e:
            apple_login_get_credentials()

        assert str(e.value) == "APPLE_KEY_ID missing in env."

    @override_settings(APPLE_PRIVATE_KEY=None)
    def test_apple_login_get_credentials_fail_private_key_missing(self):
        with pytest.raises(ImproperlyConfigured) as e:
            apple_login_get_credentials()

        assert str(e.value) == "APPLE_PRIVATE_KEY missing in env."
