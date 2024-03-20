import pytest
from django.urls import reverse

from tests.utils import IsAuthenticateTestCase

pytestmark = pytest.mark.django_db


class TestPhotoBoothReviewList(IsAuthenticateTestCase):
    def test_photo_booth_review_list_get_success(self, valid_user, valid_review):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            path=reverse("api-photo-booths:photo-booth-review-list", kwargs={"photo_booth_id": valid_review.photo_booth.id}),
        )

        assert response.status_code == 200
        assert response.data["data"][0]["id"] == valid_review.id
        assert response.data["data"][0]["main_thumbnail_image_url"] == valid_review.main_thumbnail_image_url
        assert response.data["data"][0]["content"] == valid_review.content
        assert response.data["data"][0]["frame_color"] == valid_review.frame_color
        assert response.data["data"][0]["participants"] == valid_review.participants
        assert response.data["data"][0]["camera_shot"] == valid_review.camera_shot
        assert response.data["data"][0]["goods_amount"] == valid_review.goods_amount
        assert response.data["data"][0]["curl_amount"] == valid_review.curl_amount

    def test_photo_booth_review_list_get_success_limit(self, valid_user, valid_review_list):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            path=reverse(
                "api-photo-booths:photo-booth-review-list",
                kwargs={"photo_booth_id": valid_review_list[0].photo_booth.id},
            ),
            data={"limit": 3},
        )

        assert response.status_code == 200
        assert len(response.data["data"]) == 3

    def test_photo_booth_review_list_get_success_anonymous_user(self, valid_review):
        response = self.client.get(
            path=reverse("api-photo-booths:photo-booth-review-list", kwargs={"photo_booth_id": valid_review.photo_booth.id}),
        )

        assert response.status_code == 200
        assert response.data["data"][0]["id"] == valid_review.id
        assert response.data["data"][0]["main_thumbnail_image_url"] == valid_review.main_thumbnail_image_url
        assert response.data["data"][0]["content"] == valid_review.content
        assert response.data["data"][0]["frame_color"] == valid_review.frame_color
        assert response.data["data"][0]["participants"] == valid_review.participants
        assert response.data["data"][0]["camera_shot"] == valid_review.camera_shot
        assert response.data["data"][0]["goods_amount"] == valid_review.goods_amount
        assert response.data["data"][0]["curl_amount"] == valid_review.curl_amount
