import pytest
from django.urls import reverse

from tests.utils import IsAuthenticateTestCase

pytestmark = pytest.mark.django_db


class TestMyReview(IsAuthenticateTestCase):
    url = reverse("api-users:user-review-list")

    def test_my_review_get_success_single_review(self, valid_review):
        access_token = self.obtain_token(valid_review.user)
        self.authenticate_with_token(access_token)
        response = self.client.get(self.url)

        assert response.status_code == 200
        assert response.data["data"]["count"] == 1
        assert response.data["data"]["results"][0]["id"] == valid_review.id
        assert response.data["data"]["results"][0]["main_thumbnail_image_url"] == valid_review.main_thumbnail_image_url
        assert response.data["data"]["results"][0]["photo_booth_name"] == valid_review.photo_booth.name
        assert response.data["data"]["results"][0]["photo_booth_brand_name"] == valid_review.photo_booth.photo_booth_brand.name

    def test_my_review_get_success_pagination(self, valid_review_list):
        access_token = self.obtain_token(valid_review_list[0].user)
        self.authenticate_with_token(access_token)
        response = self.client.get(self.url)

        assert response.status_code == 200
        assert response.data["data"]["count"] == 1

    def test_my_review_get_fail_not_authenticated(self):
        response = self.client.get(self.url)

        assert response.status_code == 401
        assert response.data["code"] == "not_authenticated"
        assert response.data["message"] == "Authentication credentials were not provided."

    def test_my_review_get_fail_limit_min_value(self, valid_review):
        access_token = self.obtain_token(valid_review.user)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            path=self.url,
            data={
                "limit": 0,
                "offset": 0,
            },
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"limit": ["Ensure this value is greater than or equal to 1."]}

    def test_my_review_get_fail_limit_max_value(self, valid_review):
        access_token = self.obtain_token(valid_review.user)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            path=self.url,
            data={
                "limit": 51,
                "offset": 0,
            },
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"limit": ["Ensure this value is less than or equal to 50."]}

    def test_my_review_get_fail_offset_min_value(self, valid_review):
        access_token = self.obtain_token(valid_review.user)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            path=self.url,
            data={
                "limit": 1,
                "offset": -1,
            },
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"offset": ["Ensure this value is greater than or equal to 0."]}

    def test_my_review_get_fail_limit_invalid_format(self, valid_review):
        access_token = self.obtain_token(valid_review.user)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            path=self.url,
            data={
                "limit": "invalid",
                "offset": 0,
            },
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"limit": ["A valid integer is required."]}

    def test_my_review_get_fail_offset_invalid_format(self, valid_review):
        access_token = self.obtain_token(valid_review.user)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            path=self.url,
            data={
                "limit": 1,
                "offset": "invalid",
            },
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"offset": ["A valid integer is required."]}
