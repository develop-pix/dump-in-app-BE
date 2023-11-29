import pytest
from django.urls import reverse

from tests.utils import IsAuthenticateTestCase

pytestmark = pytest.mark.django_db


class TestMyReviewLikeAPI(IsAuthenticateTestCase):
    url = reverse("api-users:user-review-like")

    def test_my_review_get_like_success(self, review, new_users):
        review.user_review_like_logs.add(new_users)

        access_token = self.obtain_token(new_users)
        self.authenticate_with_token(access_token)
        response = self.client.get(self.url)

        assert response.status_code == 200
        assert response.data["data"] is not None

    def test_my_review_get_like_fail_not_authenticated(self):
        response = self.client.get(self.url)

        assert response.status_code == 401
        assert response.data["message"] == "자격 인증데이터(authentication credentials)가 제공되지 않았습니다."
