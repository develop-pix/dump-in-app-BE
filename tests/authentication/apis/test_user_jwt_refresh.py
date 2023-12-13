from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken


class TestUserJWTRefreshAPI:
    url = reverse("api-auth:jwt-refresh")

    def test_user_jwt_refresh_api_success(self, api_client, valid_review):
        refresh = RefreshToken.for_user(valid_review)

        response = api_client.post(
            path=self.url,
            data={"refresh": str(refresh)},
            format="json",
        )

        assert response.status_code == 200
        assert response.data["code"] == 0
        assert response.data["success"] is True
        assert response.data["message"] == "Request was successful."
        assert response.data["data"]["access_token"] is not None

    def test_user_jwt_refresh_api_fail_required_refresh(self, api_client):
        response = api_client.post(
            path=self.url,
            data={},
            format="json",
        )

        assert response.status_code == 400
        assert response.data["code"] == 1000
        assert response.data["success"] is False
        assert response.data["message"]["refresh"][0] == "This field is required."

    def test_user_jwt_refresh_api_fail_invalid_or_expired_token(self, api_client):
        response = api_client.post(
            path=self.url,
            data={"refresh": "invalid_or_expired_refresh"},
            format="json",
        )

        assert response.status_code == 401
        assert response.data["code"] == 1000
        assert response.data["success"] is False
        assert response.data["message"]["detail"] == "Token is invalid or expired"
