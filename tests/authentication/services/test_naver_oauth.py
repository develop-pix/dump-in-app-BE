import pytest
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.test import override_settings

from dump_in.authentication.services.naver_oauth import (
    NaverAccessToken,
    NaverLoginFlowService,
    naver_login_get_credentials,
)
from dump_in.common.exception.exceptions import AuthenticationFailedException


class TestNaverLoginFlowService:
    def setup_method(self):
        self.service = NaverLoginFlowService()

    def test_get_authorization_url_success(self, mocker):
        mock_response = mocker.Mock()
        mock_response.status_code = 200
        mock_response.url = "https://nid.naver.com/oauth2.0/authorize"

        mocker.patch("dump_in.authentication.services.naver_oauth.requests.get", return_value=mock_response)

        authorization_url = self.service.get_authorization_url()
        assert authorization_url == "https://nid.naver.com/oauth2.0/authorize"

    def test_get_authorization_url_fail_response_not_200(self, mocker):
        mock_response = mocker.Mock()
        mock_response.status_code = 401
        mock_response.url = "https://nid.naver.com/oauth2.0/authorize"

        mocker.patch("dump_in.authentication.services.naver_oauth.requests.get", return_value=mock_response)

        with pytest.raises(AuthenticationFailedException) as e:
            self.service.get_authorization_url()

        assert e.value.detail == "Failed to get authorization url from Naver."
        assert e.value.status_code == 401

    def test_get_token_success(self, mocker):
        mock_response = mocker.Mock()
        mock_response.status_code = 200
        mock_response.text = '{"access_token": "test_access_token"}'

        mocker.patch("dump_in.authentication.services.naver_oauth.requests.post", return_value=mock_response)

        token = self.service.get_token("test_code", "test_state")
        assert token.access_token == "test_access_token"

    def test_get_token_fail_response_not_200(self, mocker):
        mock_response = mocker.Mock()
        mock_response.status_code = 401
        mock_response.text = '{"access_token": "test_access_token"}'

        mocker.patch("dump_in.authentication.services.naver_oauth.requests.post", return_value=mock_response)

        with pytest.raises(AuthenticationFailedException) as e:
            self.service.get_token("test_code", "test_state")

        assert e.value.detail == "Failed to get access token from Naver."
        assert e.value.status_code == 401

    def test_get_user_info_success(self, mocker):
        mock_response = mocker.Mock()
        mock_response.status_code = 200
        mock_response.text = """
        {
            "response": {
                "id": 123456789,
                "nickname": "test_nickname",
                "email": "test_email@test.com",
                "gender": "F",
                "birthyear": "2023",
                "birthday": "01-01"
                }
        }
        """
        mocker.patch("dump_in.authentication.services.naver_oauth.requests.get", return_value=mock_response)
        naver_token = NaverAccessToken(access_token="test_access_token")
        user_info = self.service.get_user_info(naver_token)
        assert user_info["id"] == 123456789
        assert user_info["nickname"] == "test_nickname"
        assert user_info["email"] == "test_email@test.com"
        assert user_info["gender"] == "F"
        assert user_info["birthyear"] == "2023"
        assert user_info["birthday"] == "01-01"

    def test_get_user_info_fail_response_not_200(self, mocker):
        mock_response = mocker.Mock()
        mock_response.status_code = 401

        mocker.patch("dump_in.authentication.services.naver_oauth.requests.get", return_value=mock_response)
        naver_token = NaverAccessToken(access_token="test_access_token")
        with pytest.raises(AuthenticationFailedException) as e:
            self.service.get_user_info(naver_token)

        assert e.value.detail == "Failed to get user info from Naver."
        assert e.value.status_code == 401

    def test_naver_login_get_credentials_success(self):
        credentials = naver_login_get_credentials()
        assert credentials.client_id == settings.NAVER_CLIENT_ID
        assert credentials.client_secret == settings.NAVER_CLIENT_SECRET

    @override_settings(NAVER_CLIENT_ID=None)
    def test_naver_login_get_credentials_fail_client_id_missing(self):
        with pytest.raises(ImproperlyConfigured) as e:
            naver_login_get_credentials()

        assert str(e.value) == "NAVER_CLIENT_ID missing in env."

    @override_settings(NAVER_CLIENT_SECRET=None)
    def test_naver_login_get_credentials_fail_client_secret_missing(self):
        with pytest.raises(ImproperlyConfigured) as e:
            naver_login_get_credentials()

        assert str(e.value) == "NAVER_CLIENT_SECRET missing in env."
