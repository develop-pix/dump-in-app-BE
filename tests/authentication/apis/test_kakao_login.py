import pytest
from django.urls import reverse

from dump_in.common.exception.exceptions import AuthenticationFailedException

pytestmark = pytest.mark.django_db


class TestKakaoLoginRedirectAPI:
    url = reverse("api-auth:kakao-login-redirect")

    def test_kakao_login_redirect_api_success(self, api_client, mocker):
        mock_response = mocker.Mock()
        mock_response.status_code = 200
        mock_response.url = "https://kauth.kakao.com/oauth/authorize"

        mocker.patch("dump_in.authentication.services.kakao_oauth.requests.get", return_value=mock_response)

        response = api_client.get(path=self.url)

        assert response.status_code == 302
        assert response.url == "https://kauth.kakao.com/oauth/authorize"


class TestKakaoLoginAPI:
    url = reverse("api-auth:kakao-login-callback")

    def test_kakao_login_api_success(self, api_client, mocker, user_social_provider, group):
        user_info_response = {
            "id": 123456789,
            "kakao_account": {
                "profile": {"nickname": "test"},
                "email": "test@test.com",
            },
        }

        mocker.patch("dump_in.authentication.services.kakao_oauth.KakaoLoginFlowService.get_token", return_value=mocker.Mock())
        mocker.patch("dump_in.authentication.services.kakao_oauth.KakaoLoginFlowService.get_user_info", return_value=user_info_response)

        response = api_client.get(
            path=self.url,
            data={
                "code": "code",
            },
        )

        assert response.status_code == 200
        assert response.data["code"] == 0
        assert response.data["success"] is True
        assert response.data["message"] == "Request was successful."
        assert response.data["data"]["access_token"] is not None
        assert response.cookies["refresh_token"] is not None

    def test_kakao_login_api_fail_not_code(self, api_client):
        response = api_client.get(path=self.url)
        assert response.status_code == 401
        assert response.data["code"] == AuthenticationFailedException.code
        assert response.data["message"] == "Code is not provided"

    def test_kakao_login_api_fail_is_error(self, api_client):
        response = api_client.get(
            path=self.url,
            data={
                "error": "error",
            },
        )
        assert response.status_code == 401
        assert response.data["code"] == AuthenticationFailedException.code
        assert response.data["message"] == "error"
