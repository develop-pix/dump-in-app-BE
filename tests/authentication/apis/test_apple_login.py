from django.urls import reverse


class TestAppleLoginRedirect:
    url = reverse("api-auth:apple-login-redirect")

    def test_apple_login_redirect_api_success(self, api_client, mocker):
        mock_response = mocker.Mock()
        mock_response.status_code = 200
        mock_response.url = "https://appleid.apple.com/auth/authorize"

        mocker.patch("dump_in.authentication.services.apple_oauth.requests.get", return_value=mock_response)

        response = api_client.get(path=self.url)

        assert response.status_code == 302
        assert response.url == "https://appleid.apple.com/auth/authorize"

    def test_apple_login_redirect_api_fail(self, api_client, mocker):
        mock_response = mocker.Mock()
        mock_response.status_code = 400

        mocker.patch("dump_in.authentication.services.apple_oauth.requests.get", return_value=mock_response)

        response = api_client.get(path=self.url)

        assert response.status_code == 401
        assert response.data["code"] == "authentication_failed"
        assert response.data["message"] == "Failed to get authorization url from Apple."


class TestAppleLogin:
    url = reverse("api-auth:apple-login-callback")

    def test_apple_login_api_success(self, api_client, mocker, user_social_provider, group):
        user_info_response = {
            "sub": "001",
            "email": "test_email",
        }

        mocker.patch("dump_in.authentication.services.apple_oauth.AppleLoginFlowService.get_id_token", return_value=user_info_response)

        response = api_client.post(
            path=self.url,
            content_type="application/x-www-form-urlencoded",
            data="code=code",
        )

        assert response.status_code == 200
        assert response.data["code"] == "request_success"
        assert response.data["success"] is True
        assert response.data["message"] == "Request was successful."
        assert response.data["data"]["access_token"] is not None
        assert response.data["data"]["refresh_token"] is not None

    def test_apple_login_api_fail_not_code(self, api_client):
        response = api_client.post(path=self.url)

        assert response.status_code == 401
        assert response.data["code"] == "authentication_failed"
        assert response.data["message"] == "Code is not provided"
