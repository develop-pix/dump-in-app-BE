from django.urls import reverse

from tests.utils import IsAuthenticateTestCase


class TestReviewListAPI(IsAuthenticateTestCase):
    url = reverse("api-reviews:review-list")

    def test_review_list_get_success(self, review_list, new_users):
        access_token = self.obtain_token(new_users)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            self.url,
            data={"limit": 1, "offset": 0},
        )

        assert response.status_code == 200
        assert response.data["data"] is not None

    def test_review_list_get_success_with_filter(self, review_list, new_users):
        access_token = self.obtain_token(new_users)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            self.url,
            data={"limit": 1, "offset": 0, "frame_color": "red"},
        )

        assert response.status_code == 200
        assert response.data["data"] is not None

    def test_review_list_get_fail_not_authenticated(self):
        response = self.client.get(self.url)

        assert response.status_code == 401
        assert response.data["message"] == "자격 인증데이터(authentication credentials)가 제공되지 않았습니다."

    def test_review_list_post_success(self, new_users, photo_booth, hashtag):
        access_token = self.obtain_token(new_users)
        self.authenticate_with_token(access_token)
        response = self.client.post(
            self.url,
            data={
                "image_urls": ["string"],
                "content": "string",
                "photo_booth_id": 1,
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

        assert response.status_code == 201
        assert response.data["data"] is not None

    def test_review_list_post_fail_not_authenticated(self):
        response = self.client.post(self.url)

        assert response.status_code == 401
        assert response.data["message"] == "자격 인증데이터(authentication credentials)가 제공되지 않았습니다."

    def test_review_list_post_fail_invalid_parameter(self, new_users):
        access_token = self.obtain_token(new_users)
        self.authenticate_with_token(access_token)
        response = self.client.post(
            self.url,
            data={
                "image_urls": ["string"],
            },
            format="json",
        )

        assert response.status_code == 400
        assert response.data["message"] == "Invalid parameter format"
