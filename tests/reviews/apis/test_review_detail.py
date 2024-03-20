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
        assert str(response.data["data"]["photo_booth_id"]) == str(valid_review.photo_booth.id)
        assert response.data["data"]["photo_booth_name"] == valid_review.photo_booth.name
        assert response.data["data"]["photo_booth_brand_name"] == valid_review.photo_booth.photo_booth_brand.name
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

    def test_review_detail_get_success_anonymous_user(self, valid_review):
        response = self.client.get(reverse("api-reviews:review-detail", kwargs={"review_id": valid_review.id}))

        assert response.status_code == 200
        assert response.data["data"]["id"] == valid_review.id
        assert str(response.data["data"]["photo_booth_id"]) == str(valid_review.photo_booth.id)
        assert response.data["data"]["photo_booth_name"] == valid_review.photo_booth.name
        assert response.data["data"]["photo_booth_brand_name"] == valid_review.photo_booth.photo_booth_brand.name
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
        assert response.data["data"]["is_liked"] is None
        assert response.data["data"]["is_mine"] is None
        assert response.data["data"]["is_public"] == valid_review.is_public
        assert response.data["data"]["user_nickname"] == valid_review.user.nickname

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
                "concept": [concept.name],
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
        assert response.data["data"]["concept"][0]["name"] == concept.name
        assert response.data["data"]["user_nickname"] == valid_review.user.nickname
        assert response.data["data"]["is_public"] == valid_review.is_public
        assert str(response.data["data"]["photo_booth_id"]) == str(photo_booth.id)

    def test_review_detail_put_fail_not_authenticated(self, valid_review):
        response = self.client.put(
            reverse("api-reviews:review-detail", kwargs={"review_id": valid_review.id}),
        )

        assert response.status_code == 401
        assert response.data["code"] == "not_authenticated"
        assert response.data["message"] == "Authentication credentials were not provided."

    def test_review_detail_put_fail_date_validate(self, valid_review, photo_booth, concept):
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
                "concept": [concept.name],
                "goods_amount": True,
                "curl_amount": True,
                "is_public": True,
            },
            format="json",
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"

    def test_review_detail_put_fail_concept_duplicate(self, valid_review, photo_booth, concept):
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
                "concept": [concept.name, concept.name],
                "goods_amount": True,
                "curl_amount": True,
                "is_public": True,
            },
            format="json",
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {
            "concept": [ErrorDetail(string="This list may not contain the same item twice.", code="duplicate_values")]
        }

    def test_review_detail_put_fail_frame_color_invalid_choices(self, valid_review, photo_booth, concept):
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
                "concept": [concept.name],
                "goods_amount": True,
                "curl_amount": True,
                "is_public": True,
            },
            format="json",
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"frame_color": ['"invalid" is not a valid choice.']}

    def test_review_detail_put_fail_camera_shot_invalid_choices(self, valid_review, photo_booth, concept):
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
                "concept": [concept.name],
                "goods_amount": True,
                "curl_amount": True,
                "is_public": True,
            },
            format="json",
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"camera_shot": ['"invalid" is not a valid choice.']}

    def test_review_detail_put_fail_concept_invalid_choices(self, valid_review, photo_booth, concept):
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
                "concept": ["invalid"],
                "goods_amount": True,
                "curl_amount": True,
                "is_public": True,
            },
            format="json",
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"concept": ['"invalid" is not a valid choice.']}

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
