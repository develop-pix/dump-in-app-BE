import pytest
from django.urls import reverse

from tests.utils import IsAuthenticateTestCase

pytestmark = pytest.mark.django_db


class TestPhotoBoothBrandDetail(IsAuthenticateTestCase):
    def test_photo_booth_brand_detail_get_success(self, photo_booth_brand, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            path=reverse(
                "api-photo-booths:photo-booth-brand-detail",
                kwargs={
                    "photo_booth_brand_id": photo_booth_brand.id,
                },
            ),
        )

        assert response.status_code == 200
        assert response.data["data"]["id"] == photo_booth_brand.id
        assert response.data["data"]["name"] == photo_booth_brand.name
        assert response.data["data"]["hashtag"][0]["id"] == photo_booth_brand.hashtag.all()[0].id
        assert response.data["data"]["hashtag"][0]["name"] == photo_booth_brand.hashtag.all()[0].name
        assert response.data["data"]["image"][0]["id"] == photo_booth_brand.photo_booth_brand_image.all()[0].id
        assert (
            response.data["data"]["image"][0]["image_url"] == photo_booth_brand.photo_booth_brand_image.all()[0].photo_booth_brand_image_url
        )

    def test_photo_booth_brand_detail_get_success_anonymous_user(self, photo_booth_brand):
        response = self.client.get(
            path=reverse(
                "api-photo-booths:photo-booth-brand-detail",
                kwargs={
                    "photo_booth_brand_id": photo_booth_brand.id,
                },
            ),
        )

        assert response.status_code == 200
        assert response.data["data"]["id"] == photo_booth_brand.id
        assert response.data["data"]["name"] == photo_booth_brand.name
        assert response.data["data"]["hashtag"][0]["id"] == photo_booth_brand.hashtag.all()[0].id
        assert response.data["data"]["hashtag"][0]["name"] == photo_booth_brand.hashtag.all()[0].name
        assert response.data["data"]["image"][0]["id"] == photo_booth_brand.photo_booth_brand_image.all()[0].id
        assert (
            response.data["data"]["image"][0]["image_url"] == photo_booth_brand.photo_booth_brand_image.all()[0].photo_booth_brand_image_url
        )

    def test_photo_booth_brand_detail_get_fail_does_not_exist(self, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            path=reverse(
                "api-photo-booths:photo-booth-brand-detail",
                kwargs={
                    "photo_booth_brand_id": 99999,
                },
            ),
        )

        assert response.status_code == 404
        assert response.data["code"] == "not_found"
        assert response.data["message"] == "Photo Booth Brand does not exist"
