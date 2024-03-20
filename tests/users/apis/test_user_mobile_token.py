import pytest
from django.urls import reverse

from tests.utils import IsAuthenticateTestCase

pytestmark = pytest.mark.django_db


class TestUserMobileToken(IsAuthenticateTestCase):
    url = reverse("api-users:user-mobile-token")

    def test_user_mobile_token_post_success(self):
        response = self.client.post(
            path=self.url,
            data={"mobile_token": "string"},
            format="json",
        )

        assert response.status_code == 201
        assert response.data["data"]["id"] is not None
        assert response.data["data"]["mobile_token"] == "string"
