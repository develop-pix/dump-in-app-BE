from datetime import datetime, timedelta

from django.urls import reverse
from rest_framework.exceptions import ErrorDetail

from tests.utils import IsAuthenticateTestCase


class TestReviewDetail(IsAuthenticateTestCase):
    def test_review_detail_get_success(self, valid_review, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(reverse("api-reviews:review-detail", kwargs={"review_id": valid_review.id}))

        assert response.status_code == 200
        assert response.data["data"]["id"] == valid_review.id
        assert response.data["data"]["main_thumbnail_image_url"] == valid_review.main_thumbnail_image_url
        assert response.data["data"]["content"] == valid_review.content
        assert response.data["data"]["date"] == valid_review.date
        assert response.data["data"]["frame_color"] == valid_review.frame_color
        assert response.data["data"]["participants"] == valid_review.participants
        assert response.data["data"]["camera_shot"] == valid_review.camera_shot
        assert response.data["data"]["concept"][0]["id"] == valid_review.concept.all()[0].id
        assert response.data["data"]["concept"][0]["name"] == valid_review.concept.all()[0].name
        assert response.data["data"]["goods_amount"] == valid_review.goods_amount
        assert response.data["data"]["curl_amount"] == valid_review.curl_amount
        assert response.data["data"]["is_liked"] is False
        assert response.data["data"]["is_public"] == valid_review.is_public
        assert response.data["data"]["user_nickname"] == valid_review.user.nickname
        assert str(response.data["data"]["photo_booth_id"]) == str(valid_review.photo_booth.id)

    def test_review_detail_get_fail_not_authenticated(self, valid_review):
        response = self.client.get(reverse("api-reviews:review-detail", kwargs={"review_id": valid_review.id}))

        assert response.status_code == 401
        assert response.data["code"] == "not_authenticated"
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
                "frame_color": valid_review.frame_color,
                "participants": 1,
                "camera_shot": valid_review.camera_shot,
                "concept_names": [concept.name],
                "goods_amount": True,
                "curl_amount": True,
                "is_public": True,
            },
            format="json",
        )

        assert response.status_code == 200
        assert response.data["data"]["id"] == valid_review.id
        assert response.data["data"]["main_thumbnail_image_url"] == "https://test.com"
        assert response.data["data"]["image"][0]["image_url"] == "https://test.com"
        assert response.data["data"]["content"] == "string"
        assert response.data["data"]["date"] == "2023-01-01"
        assert response.data["data"]["frame_color"] == valid_review.frame_color
        assert response.data["data"]["participants"] == 1
        assert response.data["data"]["camera_shot"] == valid_review.camera_shot
        assert response.data["data"]["goods_amount"] is True
        assert response.data["data"]["curl_amount"] is True
        assert response.data["data"]["concept"][0]["id"] == 1
        assert response.data["data"]["concept"][0]["name"] == concept.name
        assert response.data["data"]["user_nickname"] == valid_review.user.nickname
        assert response.data["data"]["is_public"] == valid_review.is_public
        assert str(response.data["data"]["photo_booth_id"]) == str(photo_booth.id)

    def test_review_detail_put_success_goods_amount_allow_null(self, valid_review, photo_booth, concept):
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
                "frame_color": valid_review.frame_color,
                "participants": 1,
                "camera_shot": valid_review.camera_shot,
                "concept_names": [concept.name],
                "goods_amount": None,
                "curl_amount": True,
                "is_public": True,
            },
            format="json",
        )

        assert response.status_code == 200
        assert response.data["data"]["goods_amount"] is None

    def test_review_detail_put_success_curl_amount_allow_null(self, valid_review, photo_booth, concept):
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
                "frame_color": valid_review.frame_color,
                "participants": 1,
                "camera_shot": valid_review.camera_shot,
                "concept_names": [concept.name],
                "goods_amount": True,
                "curl_amount": None,
                "is_public": True,
            },
            format="json",
        )

        assert response.status_code == 200
        assert response.data["data"]["curl_amount"] is None

    def test_review_detail_put_fail_not_authenticated(self, valid_review):
        response = self.client.put(
            reverse("api-reviews:review-detail", kwargs={"review_id": valid_review.id}),
        )

        assert response.status_code == 401
        assert response.data["code"] == "not_authenticated"
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
                "frame_color": valid_review.frame_color,
                "participants": 1,
                "camera_shot": valid_review.camera_shot,
                "concept_names": [concept.name],
                "goods_amount": True,
                "curl_amount": True,
                "is_public": True,
            },
            format="json",
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"main_thumbnail_image_url": ["This field is required."]}

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
                "frame_color": valid_review.frame_color,
                "participants": 1,
                "camera_shot": valid_review.camera_shot,
                "concept_names": [concept.name],
                "goods_amount": True,
                "curl_amount": True,
                "is_public": True,
            },
            format="json",
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"content": ["This field is required."]}

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
                "frame_color": valid_review.frame_color,
                "participants": 1,
                "camera_shot": valid_review.camera_shot,
                "concept_names": [concept.name],
                "goods_amount": True,
                "curl_amount": True,
                "is_public": True,
            },
            format="json",
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"photo_booth_id": ["This field is required."]}

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
                "frame_color": valid_review.frame_color,
                "participants": 1,
                "camera_shot": valid_review.camera_shot,
                "concept_names": [concept.name],
                "goods_amount": True,
                "curl_amount": True,
                "is_public": True,
            },
            format="json",
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"date": ["This field is required."]}

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
                "camera_shot": valid_review.camera_shot,
                "concept_names": [concept.name],
                "goods_amount": True,
                "curl_amount": True,
                "is_public": True,
            },
            format="json",
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"frame_color": ["This field is required."]}

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
                "frame_color": valid_review.frame_color,
                "camera_shot": valid_review.camera_shot,
                "concept_names": [concept.name],
                "goods_amount": True,
                "curl_amount": True,
                "is_public": True,
            },
            format="json",
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"participants": ["This field is required."]}

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
                "frame_color": valid_review.frame_color,
                "participants": 1,
                "concept_names": [concept.name],
                "goods_amount": True,
                "curl_amount": True,
                "is_public": True,
            },
            format="json",
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"camera_shot": ["This field is required."]}

    def test_review_detail_put_fail_concept_names_required(self, valid_review, photo_booth, concept):
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
                "frame_color": valid_review.frame_color,
                "participants": 1,
                "camera_shot": valid_review.camera_shot,
                "goods_amount": True,
                "curl_amount": True,
                "is_public": True,
            },
            format="json",
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert sorted(response.data["message"]) == sorted({"concept_names": ["This field is required."]})

    def test_review_detail_put_fail_main_thumbnail_image_url_invalid_format(self, valid_review, photo_booth, concept):
        access_token = self.obtain_token(valid_review.user)
        self.authenticate_with_token(access_token)
        response = self.client.put(
            reverse("api-reviews:review-detail", kwargs={"review_id": valid_review.id}),
            data={
                "main_thumbnail_image_url": "invalid",
                "image_urls": ["https://test.com"],
                "content": "string",
                "photo_booth_id": photo_booth.id,
                "date": "2023-01-01",
                "frame_color": valid_review.frame_color,
                "participants": 1,
                "camera_shot": valid_review.camera_shot,
                "concept_names": [concept.name],
                "goods_amount": True,
                "curl_amount": True,
                "is_public": True,
            },
            format="json",
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"main_thumbnail_image_url": ["Enter a valid URL."]}

    def test_review_detail_put_fail_image_urls_child_invalid_format(self, valid_review, photo_booth, concept):
        access_token = self.obtain_token(valid_review.user)
        self.authenticate_with_token(access_token)
        response = self.client.put(
            reverse("api-reviews:review-detail", kwargs={"review_id": valid_review.id}),
            data={
                "main_thumbnail_image_url": "https://test.com",
                "image_urls": ["invalid"],
                "content": "string",
                "photo_booth_id": photo_booth.id,
                "date": "2023-01-01",
                "frame_color": valid_review.frame_color,
                "participants": 1,
                "camera_shot": valid_review.camera_shot,
                "concept_names": [concept.name],
                "goods_amount": True,
                "curl_amount": True,
                "is_public": True,
            },
            format="json",
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"image_urls": {0: [ErrorDetail(string="Enter a valid URL.", code="invalid")]}}

    def test_review_detail_put_fail_image_urls_invalid_format(self, valid_review, photo_booth, concept):
        access_token = self.obtain_token(valid_review.user)
        self.authenticate_with_token(access_token)
        response = self.client.put(
            reverse("api-reviews:review-detail", kwargs={"review_id": valid_review.id}),
            data={
                "main_thumbnail_image_url": "https://test.com",
                "image_urls": "invalid",
                "content": "string",
                "photo_booth_id": photo_booth.id,
                "date": "2023-01-01",
                "frame_color": valid_review.frame_color,
                "participants": 1,
                "camera_shot": valid_review.camera_shot,
                "concept_names": [concept.name],
                "goods_amount": True,
                "curl_amount": True,
                "is_public": True,
            },
            format="json",
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"image_urls": ['Expected a list of items but got type "str".']}

    def test_review_detail_put_fail_content_invalid_format(self, valid_review, photo_booth, concept):
        access_token = self.obtain_token(valid_review.user)
        self.authenticate_with_token(access_token)
        response = self.client.put(
            reverse("api-reviews:review-detail", kwargs={"review_id": valid_review.id}),
            data={
                "main_thumbnail_image_url": "https://test.com",
                "image_urls": ["https://test.com"],
                "content": [1234],
                "photo_booth_id": photo_booth.id,
                "date": "2023-01-01",
                "frame_color": valid_review.frame_color,
                "participants": 1,
                "camera_shot": valid_review.camera_shot,
                "concept_names": [concept.name],
                "goods_amount": True,
                "curl_amount": True,
                "is_public": True,
            },
            format="json",
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"content": ["Not a valid string."]}

    def test_review_detail_put_fail_photo_booth_id_invalid_format(self, valid_review, photo_booth, concept):
        access_token = self.obtain_token(valid_review.user)
        self.authenticate_with_token(access_token)
        response = self.client.put(
            reverse("api-reviews:review-detail", kwargs={"review_id": valid_review.id}),
            data={
                "main_thumbnail_image_url": "https://test.com",
                "image_urls": ["https://test.com"],
                "content": "string",
                "photo_booth_id": "string",
                "date": "2023-01-01",
                "frame_color": valid_review.frame_color,
                "participants": 1,
                "camera_shot": valid_review.camera_shot,
                "concept_names": [concept.name],
                "goods_amount": True,
                "curl_amount": True,
                "is_public": True,
            },
            format="json",
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"photo_booth_id": ["Must be a valid UUID."]}

    def test_review_detail_put_fail_date_invalid_format(self, valid_review, photo_booth, concept):
        access_token = self.obtain_token(valid_review.user)
        self.authenticate_with_token(access_token)
        response = self.client.put(
            reverse("api-reviews:review-detail", kwargs={"review_id": valid_review.id}),
            data={
                "main_thumbnail_image_url": "https://test.com",
                "image_urls": ["https://test.com"],
                "content": "string",
                "photo_booth_id": photo_booth.id,
                "date": "1234",
                "frame_color": valid_review.frame_color,
                "participants": 1,
                "camera_shot": valid_review.camera_shot,
                "concept_names": [concept.name],
                "goods_amount": True,
                "curl_amount": True,
                "is_public": True,
            },
            format="json",
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"date": ["Date has wrong format. Use one of these formats instead: YYYY-MM-DD."]}

    def test_review_detail_put_fail_participants_invalid_format(self, valid_review, photo_booth, concept):
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
                "frame_color": valid_review.frame_color,
                "participants": "string",
                "camera_shot": valid_review.camera_shot,
                "concept_names": [concept.name],
                "goods_amount": True,
                "curl_amount": True,
                "is_public": True,
            },
            format="json",
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"participants": ["A valid integer is required."]}

    def test_review_detail_put_fail_goods_amount_invalid_format(self, valid_review, photo_booth, concept):
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
                "frame_color": valid_review.frame_color,
                "participants": 1,
                "camera_shot": valid_review.camera_shot,
                "concept_names": [concept.name],
                "goods_amount": "string",
                "curl_amount": True,
                "is_public": True,
            },
            format="json",
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"goods_amount": ["Must be a valid boolean."]}

    def test_review_detail_put_fail_curl_amount_invalid_format(self, valid_review, photo_booth, concept):
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
                "frame_color": valid_review.frame_color,
                "participants": 1,
                "camera_shot": valid_review.camera_shot,
                "concept_names": [concept.name],
                "goods_amount": True,
                "curl_amount": "string",
                "is_public": True,
            },
            format="json",
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"curl_amount": ["Must be a valid boolean."]}

    def test_review_detail_put_fail_is_public_invalid_format(self, valid_review, photo_booth, concept):
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
                "frame_color": valid_review.frame_color,
                "participants": 1,
                "camera_shot": valid_review.camera_shot,
                "concept_names": [concept.name],
                "goods_amount": True,
                "curl_amount": True,
                "is_public": "string",
            },
            format="json",
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"is_public": ["Must be a valid boolean."]}

    def test_review_detail_put_fail_concept_names_allow_empty(self, valid_review, photo_booth, concept):
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
                "frame_color": valid_review.frame_color,
                "participants": 1,
                "camera_shot": valid_review.camera_shot,
                "concept_names": [],
                "goods_amount": True,
                "curl_amount": True,
                "is_public": True,
            },
            format="json",
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"concept_names": ["This selection may not be empty."]}

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
                "frame_color": valid_review.frame_color,
                "participants": 1,
                "camera_shot": valid_review.camera_shot,
                "concept_names": [concept.name],
                "goods_amount": True,
                "curl_amount": True,
                "is_public": True,
            },
            format="json",
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"image_urls": ["Ensure this field has no more than 4 elements."]}

    def test_review_detail_put_fail_content_max_value(self, valid_review, photo_booth, concept):
        access_token = self.obtain_token(valid_review.user)
        self.authenticate_with_token(access_token)
        content = "string" * 1000
        response = self.client.put(
            reverse("api-reviews:review-detail", kwargs={"review_id": valid_review.id}),
            data={
                "main_thumbnail_image_url": "https://test.com",
                "image_urls": ["https://test.com"],
                "content": content,
                "photo_booth_id": photo_booth.id,
                "date": "2023-01-01",
                "frame_color": valid_review.frame_color,
                "participants": 1,
                "camera_shot": valid_review.camera_shot,
                "concept_names": [concept.name],
                "goods_amount": True,
                "curl_amount": True,
                "is_public": True,
            },
            format="json",
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"content": ["Ensure this field has no more than 100 characters."]}

    def test_review_detail_put_fail_date_max_value(self, valid_review, photo_booth, concept):
        access_token = self.obtain_token(valid_review.user)
        self.authenticate_with_token(access_token)
        date = datetime.now().date() + timedelta(days=2)
        response = self.client.put(
            reverse("api-reviews:review-detail", kwargs={"review_id": valid_review.id}),
            data={
                "main_thumbnail_image_url": "https://test.com",
                "image_urls": ["https://test.com", "https://test.com", "https://test.com", "https://test.com"],
                "content": "string",
                "photo_booth_id": photo_booth.id,
                "date": date,
                "frame_color": valid_review.frame_color,
                "participants": 1,
                "camera_shot": valid_review.camera_shot,
                "concept_names": [concept.name],
                "goods_amount": True,
                "curl_amount": True,
                "is_public": True,
            },
            format="json",
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"

    def test_review_detail_put_fail_participants_min_value(self, valid_review, photo_booth, concept):
        access_token = self.obtain_token(valid_review.user)
        self.authenticate_with_token(access_token)
        response = self.client.put(
            reverse("api-reviews:review-detail", kwargs={"review_id": valid_review.id}),
            data={
                "main_thumbnail_image_url": "https://test.com",
                "image_urls": ["https://test.com", "https://test.com", "https://test.com", "https://test.com"],
                "content": "string",
                "photo_booth_id": photo_booth.id,
                "date": "2023-01-01",
                "frame_color": valid_review.frame_color,
                "participants": 0,
                "camera_shot": valid_review.camera_shot,
                "concept_names": [concept.name],
                "goods_amount": True,
                "curl_amount": True,
                "is_public": True,
            },
            format="json",
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"participants": ["Ensure this value is greater than or equal to 1."]}

    def test_review_detail_put_fail_participants_max_value(self, valid_review, photo_booth, concept):
        access_token = self.obtain_token(valid_review.user)
        self.authenticate_with_token(access_token)
        response = self.client.put(
            reverse("api-reviews:review-detail", kwargs={"review_id": valid_review.id}),
            data={
                "main_thumbnail_image_url": "https://test.com",
                "image_urls": ["https://test.com", "https://test.com", "https://test.com", "https://test.com"],
                "content": "string",
                "photo_booth_id": photo_booth.id,
                "date": "2023-01-01",
                "frame_color": valid_review.frame_color,
                "participants": 6,
                "camera_shot": valid_review.camera_shot,
                "concept_names": [concept.name],
                "goods_amount": True,
                "curl_amount": True,
                "is_public": True,
            },
            format="json",
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"participants": ["Ensure this value is less than or equal to 5."]}

    def test_review_detail_put_fail_concept_names_max_choices(self, valid_review, photo_booth, concept):
        access_token = self.obtain_token(valid_review.user)
        self.authenticate_with_token(access_token)
        response = self.client.put(
            reverse("api-reviews:review-detail", kwargs={"review_id": valid_review.id}),
            data={
                "main_thumbnail_image_url": "https://test.com",
                "image_urls": ["https://test.com", "https://test.com", "https://test.com", "https://test.com"],
                "content": "string",
                "photo_booth_id": photo_booth.id,
                "date": "2023-01-01",
                "frame_color": valid_review.frame_color,
                "participants": 5,
                "camera_shot": valid_review.camera_shot,
                "concept_names": ["일상", "커플", "우정샷", "가족", "콜라보", "이달의 프레임"],
                "goods_amount": True,
                "curl_amount": True,
                "is_public": True,
            },
            format="json",
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {
            "concept_names": [ErrorDetail(string="Ensure this field has no more than 5 items.", code="max_choices")]
        }

    def test_review_detail_put_fail_concept_names_duplicate(self, valid_review, photo_booth, concept):
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
                "frame_color": valid_review.frame_color,
                "participants": 1,
                "camera_shot": valid_review.camera_shot,
                "concept_names": [concept.name, concept.name],
                "goods_amount": True,
                "curl_amount": True,
                "is_public": True,
            },
            format="json",
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {
            "concept_names": [ErrorDetail(string="This list may not contain the same item twice.", code="duplicate_values")]
        }

    def test_review_detail_put_fail_frame_color_choices(self, valid_review, photo_booth, concept):
        access_token = self.obtain_token(valid_review.user)
        self.authenticate_with_token(access_token)
        response = self.client.put(
            reverse("api-reviews:review-detail", kwargs={"review_id": valid_review.id}),
            data={
                "main_thumbnail_image_url": "https://test.com",
                "image_urls": ["https://test.com", "https://test.com", "https://test.com", "https://test.com"],
                "content": "string",
                "photo_booth_id": photo_booth.id,
                "date": "2023-01-01",
                "frame_color": "invalid",
                "participants": 1,
                "camera_shot": valid_review.camera_shot,
                "concept_names": [concept.name],
                "goods_amount": True,
                "curl_amount": True,
                "is_public": True,
            },
            format="json",
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"frame_color": ['"invalid" is not a valid choice.']}

    def test_review_detail_put_fail_camera_shot_choices(self, valid_review, photo_booth, concept):
        access_token = self.obtain_token(valid_review.user)
        self.authenticate_with_token(access_token)
        response = self.client.put(
            reverse("api-reviews:review-detail", kwargs={"review_id": valid_review.id}),
            data={
                "main_thumbnail_image_url": "https://test.com",
                "image_urls": ["https://test.com", "https://test.com", "https://test.com", "https://test.com"],
                "content": "string",
                "photo_booth_id": photo_booth.id,
                "date": "2023-01-01",
                "frame_color": valid_review.frame_color,
                "participants": 1,
                "camera_shot": "invalid",
                "concept_names": [concept.name],
                "goods_amount": True,
                "curl_amount": True,
                "is_public": True,
            },
            format="json",
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"camera_shot": ['"invalid" is not a valid choice.']}

    def test_review_detail_put_fail_concept_names_choices(self, valid_review, photo_booth, concept):
        access_token = self.obtain_token(valid_review.user)
        self.authenticate_with_token(access_token)
        concept.delete()
        response = self.client.put(
            reverse("api-reviews:review-detail", kwargs={"review_id": valid_review.id}),
            data={
                "main_thumbnail_image_url": "https://test.com",
                "image_urls": ["https://test.com", "https://test.com", "https://test.com", "https://test.com"],
                "content": "string",
                "photo_booth_id": photo_booth.id,
                "date": "2023-01-01",
                "frame_color": valid_review.frame_color,
                "participants": 1,
                "camera_shot": valid_review.camera_shot,
                "concept_names": ["invalid"],
                "goods_amount": True,
                "curl_amount": True,
                "is_public": True,
            },
            format="json",
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"concept_names": ['"invalid" is not a valid choice.']}

    def test_review_detail_delete_success(self, valid_review):
        access_token = self.obtain_token(valid_review.user)
        self.authenticate_with_token(access_token)
        response = self.client.delete(reverse("api-reviews:review-detail", kwargs={"review_id": valid_review.id}))

        assert response.status_code == 204

    def test_review_detail_delete_fail_not_authenticated(self, valid_review):
        response = self.client.delete(reverse("api-reviews:review-detail", kwargs={"review_id": valid_review.id}))

        assert response.status_code == 401
        assert response.data["code"] == "not_authenticated"
        assert response.data["message"] == "Authentication credentials were not provided."
