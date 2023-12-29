from django.urls import reverse


class TestNaverLogin:
    url = reverse("api-auth:naver-login")

    def test_naver_login_api_success(self, api_client, mocker, user_social_provider, group, valid_user_mobile_token):
        user_info_response = {
            "id": 123456789,
            "nickname": "test_nickname",
            "email": "test@test.com",
            "gender": "F",
            "birthyear": "2023",
            "birthday": "01-01",
        }

        mocker.patch("dump_in.authentication.services.naver_oauth.NaverLoginFlowService.get_user_info", return_value=user_info_response)

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

    def test_naver_login_api_fail_access_token_required(self, api_client):
        response = api_client.post(path=self.url)

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"access_token": ["This field is required."]}

    def test_naver_login_api_fail_access_token_invalid_format(self, api_client):
        response = api_client.post(
            path=self.url,
            data={"access_token": [1234]},
            format="json",
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"access_token": ["Not a valid string."]}

    def test_naver_login_api_fail_mobile_token_invalid_format(self, api_client):
        response = api_client.post(
            path=self.url,
            data={"access_token": "string", "mobile_token": [1234]},
            format="json",
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"mobile_token": ["Not a valid string."]}
