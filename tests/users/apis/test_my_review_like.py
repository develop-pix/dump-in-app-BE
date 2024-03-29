import pytest
from django.urls import reverse

from tests.utils import IsAuthenticateTestCase

pytestmark = pytest.mark.django_db


class TestMyReviewLike(IsAuthenticateTestCase):
    url = reverse("api-users:user-review-like-list")

    def test_my_review_like_get_success_single_review(self, valid_user, valid_review):
        valid_review.user_review_like_logs.add(valid_user)

        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            path=self.url,
            data={
                "limit": 1,
                "offset": 0,
            },
        )

        assert response.status_code == 200
        assert response.data["data"]["count"] == 1
        assert response.data["data"]["results"][0]["id"] == valid_review.id
        assert response.data["data"]["results"][0]["photo_booth_name"] == valid_review.photo_booth.name
        assert response.data["data"]["results"][0]["main_thumbnail_image_url"] == valid_review.main_thumbnail_image_url
        assert response.data["data"]["results"][0]["is_liked"]

    def test_my_review_like_get_success_pagination(self, valid_user, valid_review_list):
        for valid_review in valid_review_list:
            valid_review.user_review_like_logs.add(valid_user)

        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(self.url)

        assert response.status_code == 200
        assert response.data["data"]["count"] == len(valid_review_list)

    def test_my_review_like_get_fail_not_authenticated(self):
        response = self.client.get(self.url)

        assert response.status_code == 401
        assert response.data["code"] == "not_authenticated"
        assert response.data["message"] == "Authentication credentials were not provided."
