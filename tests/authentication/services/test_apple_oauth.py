import json

import jwt
import pytest

from dump_in.authentication.services.apple_oauth import AppleLoginFlowService
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

    def test_get_authorization_url_fail(self, mocker):
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

    def test_get_id_token_fail(self, mocker):
        mock_response = mocker.Mock()
        mock_response.status_code = 401
        mock_response.side_effect = AuthenticationFailedException("Failed to get id token from Apple.")

        mocker.patch("dump_in.authentication.services.apple_oauth.requests.post", return_value=mock_response)

        with pytest.raises(AuthenticationFailedException) as e:
            self.service.get_id_token("test_code")

        assert e.value.status_code == 401
