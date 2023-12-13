from django.urls import reverse

from tests.utils import IsAuthenticateTestCase


class TestReviewDetailAPI(IsAuthenticateTestCase):
    def test_review_detail_get_success(self, valid_review, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(reverse("api-reviews:review-detail", kwargs={"review_id": valid_review.id}))

        assert response.status_code == 200
        assert response.data["data"] is not None

    def test_review_detail_get_fail_not_authenticated(self, valid_review):
        response = self.client.get(reverse("api-reviews:review-detail", kwargs={"review_id": valid_review.id}))

        assert response.status_code == 401
        assert response.data["message"] == "Authentication credentials were not provided."

    def test_review_detail_put_success(self, valid_review, photo_booth, concept):
        access_token = self.obtain_token(valid_review.user)
        self.authenticate_with_token(access_token)
        response = self.client.put(
            reverse("api-reviews:review-detail", kwargs={"review_id": valid_review.id}),
            data={
                "main_thumbnail_image_url": "https://test.com",
                "image_urls": ["https://test.com"],
                "content": "string",
                "photo_booth_id": photo_booth.id,
                "date": "2023-01-01",
                "frame_color": "string",
                "participants": 1,
                "camera_shot": "string",
                "concept_ids": [1],
                "goods_amount": True,
                "curl_amount": True,
                "is_public": True,
            },
            format="json",
        )
        assert response.status_code == 200
        assert response.data["data"].get("id") == valid_review.id
        assert response.data["data"].get("main_thumbnail_image_url") == "https://test.com"
        assert response.data["data"].get("review_image")[0].get("image_url") == "https://test.com"
        assert response.data["data"].get("content") == "string"
        assert response.data["data"].get("date") == "2023-01-01"
        assert response.data["data"].get("frame_color") == "string"
        assert response.data["data"].get("participants") == 1
        assert response.data["data"].get("camera_shot") == "string"
        assert response.data["data"].get("concept")[0].get("id") == 1
        assert response.data["data"].get("goods_amount") is True
        assert response.data["data"].get("curl_amount") is True

    def test_review_detail_put_fail_not_authenticated(self, valid_review):
        response = self.client.put(
            reverse("api-reviews:review-detail", kwargs={"review_id": valid_review.id}),
        )

        assert response.status_code == 401
        assert response.data["message"] == "Authentication credentials were not provided."

    def test_review_detail_put_fail_main_thumbnail_image_url_required(self, valid_review, photo_booth, concept):
        access_token = self.obtain_token(valid_review.user)
        self.authenticate_with_token(access_token)
        response = self.client.put(
            reverse("api-reviews:review-detail", kwargs={"review_id": valid_review.id}),
            data={
                "image_urls": ["https://test.com"],
                "content": "string",
                "photo_booth_id": photo_booth.id,
                "date": "2023-01-01",
                "frame_color": "string",
                "participants": 1,
                "camera_shot": "string",
                "concept_ids": [1],
                "goods_amount": True,
                "curl_amount": True,
                "is_public": True,
            },
            format="json",
        )

        assert response.status_code == 400
        assert response.data["message"] == "Invalid parameter format"

    def test_review_detail_put_fail_image_urls_required(self, valid_review, photo_booth, concept):
        access_token = self.obtain_token(valid_review.user)
        self.authenticate_with_token(access_token)
        response = self.client.put(
            reverse("api-reviews:review-detail", kwargs={"review_id": valid_review.id}),
            data={
                "main_thumbnail_image_url": "https://test.com",
                "content": "string",
                "photo_booth_id": photo_booth.id,
                "date": "2023-01-01",
                "frame_color": "string",
                "participants": 1,
                "camera_shot": "string",
                "concept_ids": [1],
                "goods_amount": True,
                "curl_amount": True,
                "is_public": True,
            },
            format="json",
        )

        assert response.status_code == 400
        assert response.data["message"] == "Invalid parameter format"

    def test_review_detail_put_fail_content_required(self, valid_review, photo_booth, concept):
        access_token = self.obtain_token(valid_review.user)
        self.authenticate_with_token(access_token)
        response = self.client.put(
            reverse("api-reviews:review-detail", kwargs={"review_id": valid_review.id}),
            data={
                "main_thumbnail_image_url": "https://test.com",
                "image_urls": ["https://test.com"],
                "photo_booth_id": photo_booth.id,
                "date": "2023-01-01",
                "frame_color": "string",
                "participants": 1,
                "camera_shot": "string",
                "concept_ids": [1],
                "goods_amount": True,
                "curl_amount": True,
                "is_public": True,
            },
            format="json",
        )

        assert response.status_code == 400
        assert response.data["message"] == "Invalid parameter format"

    def test_review_detail_put_fail_photo_booth_id_required(self, valid_review, photo_booth, concept):
        access_token = self.obtain_token(valid_review.user)
        self.authenticate_with_token(access_token)
        response = self.client.put(
            reverse("api-reviews:review-detail", kwargs={"review_id": valid_review.id}),
            data={
                "main_thumbnail_image_url": "https://test.com",
                "image_urls": ["https://test.com"],
                "content": "string",
                "date": "2023-01-01",
                "frame_color": "string",
                "participants": 1,
                "camera_shot": "string",
                "concept_ids": [1],
                "goods_amount": True,
                "curl_amount": True,
                "is_public": True,
            },
            format="json",
        )

        assert response.status_code == 400
        assert response.data["message"] == "Invalid parameter format"

    def test_review_detail_put_fail_date_required(self, valid_review, photo_booth, concept):
        access_token = self.obtain_token(valid_review.user)
        self.authenticate_with_token(access_token)
        response = self.client.put(
            reverse("api-reviews:review-detail", kwargs={"review_id": valid_review.id}),
            data={
                "main_thumbnail_image_url": "https://test.com",
                "image_urls": ["https://test.com"],
                "content": "string",
                "photo_booth_id": photo_booth.id,
                "frame_color": "string",
                "participants": 1,
                "camera_shot": "string",
                "concept_ids": [1],
                "goods_amount": True,
                "curl_amount": True,
                "is_public": True,
            },
            format="json",
        )

        assert response.status_code == 400
        assert response.data["message"] == "Invalid parameter format"

    def test_review_detail_put_fail_frame_color_required(self, valid_review, photo_booth, concept):
        access_token = self.obtain_token(valid_review.user)
        self.authenticate_with_token(access_token)
        response = self.client.put(
            reverse("api-reviews:review-detail", kwargs={"review_id": valid_review.id}),
            data={
                "main_thumbnail_image_url": "https://test.com",
                "image_urls": ["https://test.com"],
                "content": "string",
                "photo_booth_id": photo_booth.id,
                "date": "2023-01-01",
                "participants": 1,
                "camera_shot": "string",
                "concept_ids": [1],
                "goods_amount": True,
                "curl_amount": True,
                "is_public": True,
            },
            format="json",
        )

        assert response.status_code == 400
        assert response.data["message"] == "Invalid parameter format"

    def test_review_detail_put_fail_participants_required(self, valid_review, photo_booth, concept):
        access_token = self.obtain_token(valid_review.user)
        self.authenticate_with_token(access_token)
        response = self.client.put(
            reverse("api-reviews:review-detail", kwargs={"review_id": valid_review.id}),
            data={
                "main_thumbnail_image_url": "https://test.com",
                "image_urls": ["https://test.com"],
                "content": "string",
                "photo_booth_id": photo_booth.id,
                "date": "2023-01-01",
                "frame_color": "string",
                "camera_shot": "string",
                "concept_ids": [1],
                "goods_amount": True,
                "curl_amount": True,
                "is_public": True,
            },
            format="json",
        )

        assert response.status_code == 400
        assert response.data["message"] == "Invalid parameter format"

    def test_review_detail_put_fail_camera_shot_required(self, valid_review, photo_booth, concept):
        access_token = self.obtain_token(valid_review.user)
        self.authenticate_with_token(access_token)
        response = self.client.put(
            reverse("api-reviews:review-detail", kwargs={"review_id": valid_review.id}),
            data={
                "main_thumbnail_image_url": "https://test.com",
                "image_urls": ["https://test.com"],
                "content": "string",
                "photo_booth_id": photo_booth.id,
                "date": "2023-01-01",
                "frame_color": "string",
                "participants": 1,
                "concept_ids": [1],
                "goods_amount": True,
                "curl_amount": True,
                "is_public": True,
            },
            format="json",
        )

        assert response.status_code == 400
        assert response.data["message"] == "Invalid parameter format"

    def test_review_detail_put_fail_concept_ids_required(self, valid_review, photo_booth, concept):
        access_token = self.obtain_token(valid_review.user)
        self.authenticate_with_token(access_token)
        response = self.client.put(
            reverse("api-reviews:review-detail", kwargs={"review_id": valid_review.id}),
            data={
                "main_thumbnail_image_url": "https://test.com",
                "image_urls": ["https://test.com"],
                "content": "string",
                "photo_booth_id": photo_booth.id,
                "date": "2023-01-01",
                "frame_color": "string",
                "participants": 1,
                "camera_shot": "string",
                "goods_amount": True,
                "curl_amount": True,
                "is_public": True,
            },
            format="json",
        )

        assert response.status_code == 400
        assert response.data["message"] == "Invalid parameter format"

    def test_review_detail_put_fail_image_urls_min_length(self, valid_review, photo_booth, concept):
        access_token = self.obtain_token(valid_review.user)
        self.authenticate_with_token(access_token)
        response = self.client.put(
            reverse("api-reviews:review-detail", kwargs={"review_id": valid_review.id}),
            data={
                "main_thumbnail_image_url": "https://test.com",
                "image_urls": [],
                "content": "string",
                "photo_booth_id": photo_booth.id,
                "date": "2023-01-01",
                "frame_color": "string",
                "participants": 1,
                "camera_shot": "string",
                "concept_ids": [1],
                "goods_amount": True,
                "curl_amount": True,
                "is_public": True,
            },
            format="json",
        )

        assert response.status_code == 400
        assert response.data["message"] == "Invalid parameter format"

    def test_review_detail_put_fail_image_urls_max_length(self, valid_review, photo_booth, concept):
        access_token = self.obtain_token(valid_review.user)
        self.authenticate_with_token(access_token)
        response = self.client.put(
            reverse("api-reviews:review-detail", kwargs={"review_id": valid_review.id}),
            data={
                "main_thumbnail_image_url": "https://test.com",
                "image_urls": ["https://test.com", "https://test.com", "https://test.com", "https://test.com", "https://test.com"],
                "content": "string",
                "photo_booth_id": photo_booth.id,
                "date": "2023-01-01",
                "frame_color": "string",
                "participants": 1,
                "camera_shot": "string",
                "concept_ids": [1],
                "goods_amount": True,
                "curl_amount": True,
                "is_public": True,
            },
            format="json",
        )

        assert response.status_code == 400
        assert response.data["message"] == "Invalid parameter format"

    def test_review_detail_delete_success(self, valid_review):
        access_token = self.obtain_token(valid_review.user)
        self.authenticate_with_token(access_token)
        response = self.client.delete(reverse("api-reviews:review-detail", kwargs={"review_id": valid_review.id}))

        assert response.status_code == 204

    def test_review_detail_delete_fail_not_authenticated(self, valid_review):
        response = self.client.delete(reverse("api-reviews:review-detail", kwargs={"review_id": valid_review.id}))

        assert response.status_code == 401
        assert response.data["message"] == "Authentication credentials were not provided."
