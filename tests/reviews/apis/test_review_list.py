from django.urls import reverse

from tests.utils import IsAuthenticateTestCase


class TestReviewListAPI(IsAuthenticateTestCase):
    url = reverse("api-reviews:review-list")

    def test_review_list_get_success_single_review(self, valid_review, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            self.url,
            data={"limit": 1, "offset": 0},
        )

        assert response.status_code == 200
        assert response.data["data"].get("count") == 1

    def test_review_list_get_success_pagination(self, valid_review_list, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            self.url,
            data={"limit": 10, "offset": 0},
        )

        assert response.status_code == 200
        assert response.data["data"].get("count") == 10

    def test_review_list_get_success_with_filter(self, valid_review_list_frame_color, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            self.url,
            data={"limit": 1, "offset": 0, "frame_color": "red"},
        )

        assert response.status_code == 200
        assert response.data["data"].get("count") == 3

    def test_review_list_get_fail_not_authenticated(self):
        response = self.client.get(self.url)

        assert response.status_code == 401
        assert response.data["message"] == "Authentication credentials were not provided."

    def test_review_list_post_success(self, valid_user, photo_booth, concept):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.post(
            self.url,
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
        assert response.status_code == 201
        assert response.data["data"].get("review_id") is not None
        assert response.data["data"].get("main_thumbnail_image_url") == "https://test.com"
        assert response.data["data"].get("photo_booth_name") == photo_booth.name

    def test_review_list_post_fail_not_authenticated(self):
        response = self.client.post(self.url)

        assert response.status_code == 401
        assert response.data["message"] == "Authentication credentials were not provided."

    def test_review_list_post_fail_main_thumbnail_image_url_required(self, valid_user, photo_booth, concept):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.post(
            self.url,
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

    def test_review_list_post_fail_image_urls_required(self, valid_user, photo_booth, concept):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.post(
            self.url,
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

    def test_review_list_post_fail_content_required(self, valid_user, photo_booth, concept):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.post(
            self.url,
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

    def test_review_list_post_fail_photo_booth_id_required(self, valid_user, photo_booth, concept):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.post(
            self.url,
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

    def test_review_list_post_fail_date_required(self, valid_user, photo_booth, concept):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.post(
            self.url,
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

    def test_review_list_post_fail_frame_color_required(self, valid_user, photo_booth, concept):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.post(
            self.url,
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

    def test_review_list_post_fail_participants_required(self, valid_user, photo_booth, concept):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.post(
            self.url,
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

    def test_review_list_post_fail_camera_shot_required(self, valid_user, photo_booth, concept):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.post(
            self.url,
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

    def test_review_list_post_fail_concept_ids_required(self, valid_user, photo_booth, concept):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.post(
            self.url,
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

    def test_review_list_post_fail_image_urls_min_length(self, valid_user, photo_booth, concept):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.post(
            self.url,
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

    def test_review_list_post_fail_image_urls_max_length(self, valid_user, photo_booth, concept):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        image_urls = ["https://test.com" for _ in range(11)]
        response = self.client.post(
            self.url,
            data={
                "main_thumbnail_image_url": "https://test.com",
                "image_urls": image_urls,
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
