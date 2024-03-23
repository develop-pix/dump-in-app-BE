from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken


class TestUserJWTRefresh:
    url = reverse("api-auth:jwt-refresh")

    def test_user_jwt_refresh_api_success(self, api_client, valid_user):
        refresh = RefreshToken.for_user(valid_user)

        response = api_client.post(
            path=self.url,
            data={"refresh": str(refresh), "is_refresh_generated": False},
            format="json",
        )

        assert response.status_code == 200
        assert response.data["code"] == "request_success"
        assert response.data["success"] is True
        assert response.data["message"] == "Request was successful."
        assert response.data["data"]["access_token"] is not None
        assert response.data["data"]["refresh_token"] is None
