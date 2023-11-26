import pytest
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken

pytestmark = pytest.mark.django_db


class TestUserJWTRefreshAPI:
    url = reverse("api-auth:jwt-refresh")

    def test_user_jwt_refresh_api_success(self, api_client, new_users):
        refresh = RefreshToken.for_user(new_users)

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
