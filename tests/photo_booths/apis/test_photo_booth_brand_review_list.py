import pytest
import pytz
from django.urls import reverse

from tests.utils import IsAuthenticateTestCase

pytestmark = pytest.mark.django_db


class TestPhotoBoothBrandReviewtList(IsAuthenticateTestCase):
    def test_photo_booth_brand_review_list_get_success(self, valid_review, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            path=reverse(
                "api-photo-booths:photo-booth-brand-review-list",
                kwargs={
                    "photo_booth_brand_id": valid_review.photo_booth.photo_booth_brand.id,
                },
            ),
        )

        assert response.status_code == 200
        assert len(response.data["data"]) == 1
        assert response.data["data"][0]["id"] == valid_review.id
        assert response.data["data"][0]["main_thumbnail_image_url"] == valid_review.main_thumbnail_image_url
        assert response.data["data"][0]["content"] == valid_review.content
        assert response.data["data"][0]["frame_color"] == valid_review.frame_color
        assert response.data["data"][0]["participants"] == valid_review.participants
        assert response.data["data"][0]["camera_shot"] == valid_review.camera_shot
        assert response.data["data"][0]["goods_amount"] == valid_review.goods_amount
        assert response.data["data"][0]["curl_amount"] == valid_review.curl_amount
        assert response.data["data"][0]["concept"][0]["id"] == valid_review.concept.all()[0].id
        assert response.data["data"][0]["concept"][0]["name"] == valid_review.concept.all()[0].name
        assert response.data["data"][0]["created_at"] == valid_review.created_at.astimezone(pytz.timezone("Asia/Seoul")).isoformat()
        assert response.data["data"][0]["updated_at"] == valid_review.updated_at.astimezone(pytz.timezone("Asia/Seoul")).isoformat()

    def test_photo_booth_brand_review_list_get_success_limit(self, valid_review_list, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            path=reverse(
                "api-photo-booths:photo-booth-brand-review-list",
                kwargs={
                    "photo_booth_brand_id": valid_review_list[0].photo_booth.photo_booth_brand.id,
                },
            ),
            data={"limit": 3},
        )

        assert response.status_code == 200
        assert len(response.data["data"]) == 3

    def test_photo_booth_brand_review_list_get_success_anonymous_user(self, valid_review):
        response = self.client.get(
            path=reverse(
                "api-photo-booths:photo-booth-brand-review-list",
                kwargs={
                    "photo_booth_brand_id": valid_review.photo_booth.photo_booth_brand.id,
                },
            ),
        )

        assert response.status_code == 200
        assert len(response.data["data"]) == 1
        assert response.data["data"][0]["id"] == valid_review.id
        assert response.data["data"][0]["main_thumbnail_image_url"] == valid_review.main_thumbnail_image_url
        assert response.data["data"][0]["content"] == valid_review.content
        assert response.data["data"][0]["frame_color"] == valid_review.frame_color
        assert response.data["data"][0]["participants"] == valid_review.participants
        assert response.data["data"][0]["camera_shot"] == valid_review.camera_shot
        assert response.data["data"][0]["goods_amount"] == valid_review.goods_amount
        assert response.data["data"][0]["curl_amount"] == valid_review.curl_amount
        assert response.data["data"][0]["concept"][0]["id"] == valid_review.concept.all()[0].id
        assert response.data["data"][0]["concept"][0]["name"] == valid_review.concept.all()[0].name
        assert response.data["data"][0]["created_at"] == valid_review.created_at.astimezone(pytz.timezone("Asia/Seoul")).isoformat()
        assert response.data["data"][0]["updated_at"] == valid_review.updated_at.astimezone(pytz.timezone("Asia/Seoul")).isoformat()

    def test_photo_booth_brand_review_list_get_fail_limit_min_value(self, valid_review, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            path=reverse(
                "api-photo-booths:photo-booth-brand-review-list",
                kwargs={
                    "photo_booth_brand_id": valid_review.photo_booth.photo_booth_brand.id,
                },
            ),
            data={"limit": 0},
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"limit": ["Ensure this value is greater than or equal to 1."]}

    def test_photo_booth_brand_review_list_get_fail_limit_max_value(self, valid_review, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            path=reverse(
                "api-photo-booths:photo-booth-brand-review-list",
                kwargs={
                    "photo_booth_brand_id": valid_review.photo_booth.photo_booth_brand.id,
                },
            ),
            data={"limit": 51},
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"limit": ["Ensure this value is less than or equal to 50."]}

    def test_photo_booth_brand_review_list_get_fail_limit_invalid_format(self, valid_review, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            path=reverse(
                "api-photo-booths:photo-booth-brand-review-list",
                kwargs={
                    "photo_booth_brand_id": valid_review.photo_booth.photo_booth_brand.id,
                },
            ),
            data={"limit": "invalid"},
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"limit": ["A valid integer is required."]}

    def test_photo_booth_brand_e_list_get_fail_not_exist_photo_booth_brand(self, valid_event, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            path=reverse(
                "api-photo-booths:photo-booth-brand-review-list",
                kwargs={
                    "photo_booth_brand_id": 99999,
                },
            ),
            data={"limit": 10},
        )

        assert response.status_code == 404
        assert response.data["code"] == "not_found"
        assert response.data["message"] == "Photo Booth Brand does not exist"
