from django.urls import reverse

from tests.utils import IsAuthenticateTestCase


class TestReviewLikeAPI(IsAuthenticateTestCase):
    def test_review_like_post_success(self, review, new_users):
        access_token = self.obtain_token(new_users)
        self.authenticate_with_token(access_token)
        response = self.client.post(reverse("api-reviews:review-like", kwargs={"review_id": review.id}))

        assert response.status_code == 200
        assert response.data["data"] is not None

    def test_review_like_post_fail_not_authenticated(self, review):
        response = self.client.post(reverse("api-reviews:review-like", kwargs={"review_id": review.id}))

        assert response.status_code == 401
        assert response.data["message"] == "자격 인증데이터(authentication credentials)가 제공되지 않았습니다."
