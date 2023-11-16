import pytest

from dump_in.authentication.services.kakao_oauth import (
    KakaoAccessToken,
    KakaoLoginFlowService,
)
from dump_in.common.exception.exceptions import AuthenticationFailedException


class TestKakaoLoginFlowService:
    def setup_method(self):
        self.service = KakaoLoginFlowService()

    def test_get_authorization_url_success(self, mocker):
        mock_response = mocker.Mock()
        mock_response.status_code = 200
        mock_response.url = "https://kauth.kakao.com/oauth/authorize"

        mocker.patch("dump_in.authentication.services.kakao_oauth.requests.get", return_value=mock_response)

        authorization_url = self.service.get_authorization_url()
        assert authorization_url == "https://kauth.kakao.com/oauth/authorize"

    def test_get_authorization_url_fail(self, mocker):
        mock_response = mocker.Mock()
        mock_response.status_code = 401
        mock_response.url = "https://kauth.kakao.com/oauth/authorize"

        mocker.patch("dump_in.authentication.services.kakao_oauth.requests.get", return_value=mock_response)

        with pytest.raises(AuthenticationFailedException) as e:
            self.service.get_authorization_url()

        assert e.value.detail == "Failed to get authorization url from Kakao."
        assert e.value.status_code == 401

    def test_get_token_success(self, mocker):
        mock_response = mocker.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"access_token": "test_access_token"}

        mocker.patch("dump_in.authentication.services.kakao_oauth.requests.post", return_value=mock_response)

        token = self.service.get_token("test_code")
        assert token.access_token == "test_access_token"

    def test_get_token_fail(self, mocker):
        mock_response = mocker.Mock()
        mock_response.status_code = 401
        mock_response.json.return_value = {"access_token": "test_access_token"}

        mocker.patch("dump_in.authentication.services.kakao_oauth.requests.post", return_value=mock_response)

        with pytest.raises(AuthenticationFailedException) as e:
            self.service.get_token("test_code")

        assert e.value.detail == "Failed to get access token from Kakao."
        assert e.value.status_code == 401

    def test_get_user_info_success(self, mocker):
        mock_response = mocker.Mock()
        mock_response.status_code = 200
        # @TODO 생년월일, 성별 추가 필요
        mock_response.text = """
        {
            "id": 123456789,
            "kakao_account": {
                "profile": {
                    "nickname": "test_nickname"
                },
                "email": "test_email"
            }
        }
        """
        mocker.patch("dump_in.authentication.services.kakao_oauth.requests.get", return_value=mock_response)
        kakao_token = KakaoAccessToken(access_token="test_access_token")
        user_info = self.service.get_user_info(kakao_token)
        assert user_info["id"] == 123456789
        assert user_info["kakao_account"]["profile"]["nickname"] == "test_nickname"
        assert user_info["kakao_account"]["email"] == "test_email"

    def test_get_user_info_fail(self, mocker):
        mock_response = mocker.Mock()
        mock_response.status_code = 401

        mocker.patch("dump_in.authentication.services.kakao_oauth.requests.get", return_value=mock_response)
        kakao_token = KakaoAccessToken(access_token="test_access_token")
        with pytest.raises(AuthenticationFailedException) as e:
            self.service.get_user_info(kakao_token)

        assert e.value.detail == "Failed to get user info from Kakao."
        assert e.value.status_code == 401
