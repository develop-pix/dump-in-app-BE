from django.urls import reverse


class TestKakaoLogin:
    url = reverse("api-auth:kakao-login")

    def test_kakao_login_api_post_success(self, api_client, mocker, user_social_provider, group, valid_user_mobile_token):
        user_info_response = {
            "id": 123456789,
            "kakao_account": {
                "profile": {"nickname": "test"},
                "email": "test@test.com",
            },
        }

        mocker.patch("dump_in.authentication.services.kakao_oauth.KakaoLoginFlowService.get_user_info", return_value=user_info_response)

        response = api_client.post(
            path=self.url,
            data={
                "access_token": "access_token",
                "mobile_token": valid_user_mobile_token.token,
            },
            format="json",
        )

        assert response.status_code == 200
        assert response.data["code"] == "request_success"
        assert response.data["success"] is True
        assert response.data["message"] == "Request was successful."
        assert response.data["data"]["access_token"] is not None
        assert response.data["data"]["refresh_token"] is not None

    def test_kakao_login_api_post_success_mobile_token_none(self, api_client, mocker, user_social_provider, group):
        user_info_response = {
            "id": 123456789,
            "kakao_account": {
                "profile": {"nickname": "test"},
                "email": "test@test.com",
            },
        }

        mocker.patch("dump_in.authentication.services.kakao_oauth.KakaoLoginFlowService.get_user_info", return_value=user_info_response)

        response = api_client.post(
            path=self.url,
            data={
                "access_token": "access_token",
                "mobile_token": None,
            },
            format="json",
        )

        assert response.status_code == 200
        assert response.data["code"] == "request_success"
        assert response.data["success"] is True
        assert response.data["message"] == "Request was successful."
        assert response.data["data"]["access_token"] is not None
        assert response.data["data"]["refresh_token"] is not None
