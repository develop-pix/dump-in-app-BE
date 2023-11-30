from django.urls import reverse

from tests.utils import IsAuthenticateTestCase


class TestReviewDetailAPI(IsAuthenticateTestCase):
    def test_review_detail_get_success(self, review, new_users):
        access_token = self.obtain_token(new_users)
        self.authenticate_with_token(access_token)
        response = self.client.get(reverse("api-reviews:review-detail", kwargs={"review_id": review.id}))

        assert response.status_code == 200
        assert response.data["data"] is not None

    def test_review_detail_get_fail_not_authenticated(self, review):
        response = self.client.get(reverse("api-reviews:review-detail", kwargs={"review_id": review.id}))

        assert response.status_code == 401
        assert response.data["message"] == "자격 인증데이터(authentication credentials)가 제공되지 않았습니다."

    def test_review_detail_put_success(self, review, photo_booth, hashtag):
        access_token = self.obtain_token(review.user)
        self.authenticate_with_token(access_token)
        response = self.client.put(
            reverse("api-reviews:review-detail", kwargs={"review_id": review.id}),
            data={
                "image_urls": ["string"],
                "content": "string",
                "photo_booth_id": photo_booth.id,
                "date": "2023-01-01",
                "frame_color": "string",
                "participants": 1,
                "camera_shot": "string",
                "hashtag_ids": [1],
                "goods_amount": True,
                "curl_amount": True,
                "is_public": True,
            },
            format="json",
        )

        assert response.status_code == 200
        assert response.data["data"] is not None

    def test_review_detail_put_fail_not_authenticated(self, review):
        response = self.client.put(
            reverse("api-reviews:review-detail", kwargs={"review_id": review.id}),
        )

        assert response.status_code == 401
        assert response.data["message"] == "자격 인증데이터(authentication credentials)가 제공되지 않았습니다."

    def test_review_detail_delete_success(self, review):
        access_token = self.obtain_token(review.user)
        self.authenticate_with_token(access_token)
        response = self.client.delete(reverse("api-reviews:review-detail", kwargs={"review_id": review.id}))

        assert response.status_code == 204

    def test_review_detail_delete_fail_not_authenticated(self, review):
        response = self.client.delete(reverse("api-reviews:review-detail", kwargs={"review_id": review.id}))

        assert response.status_code == 401
        assert response.data["message"] == "자격 인증데이터(authentication credentials)가 제공되지 않았습니다."
