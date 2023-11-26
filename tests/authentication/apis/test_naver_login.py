import pytest
from django.urls import reverse

from dump_in.common.exception.exceptions import AuthenticationFailedException

pytestmark = pytest.mark.django_db


class TestNaverLoginRedirectAPI:
    url = reverse("api-auth:naver-login-redirect")

    def test_naver_login_redirect_api_success(self, api_client, mocker):
        mock_response = mocker.Mock()
        mock_response.status_code = 200
        mock_response.url = "https://nid.naver.com/oauth2.0/authorize"

        mocker.patch("dump_in.authentication.services.naver_oauth.requests.get", return_value=mock_response)

        response = api_client.get(path=self.url)

        assert response.status_code == 302
        assert response.url == "https://nid.naver.com/oauth2.0/authorize"


class TestNaverLoginAPI:
    url = reverse("api-auth:naver-login-callback")

    def test_kakao_login_api_success(self, api_client, mocker, user_social_provider, group):
        user_info_response = {
            "id": 123456789,
            "nickname": "test_nickname",
            "email": "test@test.com",
            "gender": "F",
            "birthyear": "2023",
            "birthday": "01-01",
        }

        mocker.patch("dump_in.authentication.services.naver_oauth.NaverLoginFlowService.get_token", return_value=mocker.Mock())
        mocker.patch("dump_in.authentication.services.naver_oauth.NaverLoginFlowService.get_user_info", return_value=user_info_response)

        response = api_client.get(
            path=self.url,
            data={
                "code": "code",
                "state": "state",
            },
        )

        assert response.status_code == 200
        assert response.data["code"] == 0
        assert response.data["success"] is True
        assert response.data["message"] == "Request was successful."
        assert response.data["data"]["access_token"] is not None
        assert response.data["data"]["refresh_token"] is not None

    def test_kakao_login_api_fail_not_code_and_state(self, api_client):
        response = api_client.get(path=self.url)
        assert response.status_code == 401
        assert response.data["code"] == AuthenticationFailedException.code
        assert response.data["message"] == "Code and State is not provided"

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
