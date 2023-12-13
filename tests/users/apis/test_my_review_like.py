import pytest
from django.urls import reverse

from tests.utils import IsAuthenticateTestCase

pytestmark = pytest.mark.django_db


class TestMyReviewLikeAPI(IsAuthenticateTestCase):
    url = reverse("api-users:user-review-like")

    def test_my_review_like_get_success_single_review(self, valid_user, valid_review):
        valid_review.user_review_like_logs.add(valid_user)

        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(self.url)

        assert response.status_code == 200
        assert response.data["data"].get("count") == 1

    def test_my_review_like_get_success_pagination(self, valid_user, valid_review_list):
        for valid_review in valid_review_list:
            valid_review.user_review_like_logs.add(valid_user)

        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(self.url)

        assert response.status_code == 200
        assert response.data["data"].get("count") == 10

    def test_my_review_like_get_fail_not_authenticated(self):
        response = self.client.get(self.url)

        assert response.status_code == 401
        assert response.data["message"] == "Authentication credentials were not provided."
