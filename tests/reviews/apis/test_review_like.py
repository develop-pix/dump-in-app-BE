from django.urls import reverse

from tests.utils import IsAuthenticateTestCase


class TestReviewLike(IsAuthenticateTestCase):
    def test_review_like_post_success(self, valid_review, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.post(reverse("api-reviews:review-like", kwargs={"review_id": valid_review.id}))

        assert response.status_code == 200
        assert response.data["data"]["id"] == valid_review.id
        assert response.data["data"]["is_liked"] is True

    def test_review_like_post_success_already_liked(self, valid_review, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        valid_review.user_review_like_logs.add(valid_user)
        response = self.client.post(reverse("api-reviews:review-like", kwargs={"review_id": valid_review.id}))

        assert response.status_code == 200
        assert response.data["data"]["id"] == valid_review.id
        assert response.data["data"]["is_liked"] is False

    def test_review_like_post_fail_not_authenticated(self, valid_review):
        response = self.client.post(reverse("api-reviews:review-like", kwargs={"review_id": valid_review.id}))

        assert response.status_code == 401
        assert response.data["code"] == "not_authenticated"
        assert response.data["message"] == "Authentication credentials were not provided."
