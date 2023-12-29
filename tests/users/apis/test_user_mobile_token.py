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

    def test_user_mobile_token_post_fail_mobile_token_required(self):
        response = self.client.post(path=self.url)

        assert response.status_code == 400
        assert response.data["message"] == {"mobile_token": ["This field is required."]}

    def test_user_mobile_token_post_fail_mobile_token_max_length(self):
        response = self.client.post(
            path=self.url,
            data={"mobile_token": "a" * 517},
            format="json",
        )

        assert response.status_code == 400
        assert response.data["message"] == {"mobile_token": ["Ensure this field has no more than 512 characters."]}

    def test_user_mobile_token_post_mobile_token_invalid_format(self):
        response = self.client.post(
            path=self.url,
            data={"mobile_token": [1234]},
            format="json",
        )

        assert response.status_code == 400
        assert response.data["message"] == {"mobile_token": ["Not a valid string."]}
