from django.urls import reverse


class TestAppleLogin:
    url = reverse("api-auth:apple-login")

    def test_apple_login_api_post_success(self, api_client, mocker, user_social_provider, group, valid_user_mobile_token):
        user_info_response = {
            "sub": "001",
            "email": "test_email",
        }

        mocker.patch("dump_in.authentication.services.apple_oauth.AppleLoginFlowService.get_user_info", return_value=user_info_response)

        response = api_client.post(
            path=self.url,
            data={
                "identify_token": "test_token",
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

    def test_apple_login_api_post_fail_identify_token_required(self, api_client):
        response = api_client.post(path=self.url)

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"identify_token": ["This field is required."]}

    def test_apple_login_api_post_fail_identify_token_invalid_format(self, api_client):
        response = api_client.post(
            path=self.url,
            data={"identify_token": [1234]},
            format="json",
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"identify_token": ["Not a valid string."]}

    def test_apple_login_api_post_fail_mobile_token_invalid_format(self, api_client):
        response = api_client.post(
            path=self.url,
            data={"identify_token": "string", "mobile_token": [1234]},
            format="json",
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"mobile_token": ["Not a valid string."]}
