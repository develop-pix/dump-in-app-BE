import pytest
from django.urls import reverse

from tests.utils import IsAuthenticateTestCase

pytestmark = pytest.mark.django_db


class TestMyReviewAPI(IsAuthenticateTestCase):
    url = reverse("api-users:user-review")

    def test_my_review_get_success_single_review(self, valid_review):
        access_token = self.obtain_token(valid_review.user)
        self.authenticate_with_token(access_token)
        response = self.client.get(self.url)

        assert response.status_code == 200
        assert response.data["data"].get("count") == 1

    def test_my_review_get_success_pagination(self, valid_review_list):
        access_token = self.obtain_token(valid_review_list[0].user)
        self.authenticate_with_token(access_token)
        response = self.client.get(self.url)

        assert response.status_code == 200
        assert response.data["data"].get("count") == 1

    def test_my_review_get_fail_not_authenticated(self):
        response = self.client.get(self.url)

        assert response.status_code == 401
        assert response.data["message"] == "Authentication credentials were not provided."
