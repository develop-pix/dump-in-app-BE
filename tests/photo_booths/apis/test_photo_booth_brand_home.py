import pytest
from django.urls import reverse

from tests.utils import IsAuthenticateTestCase

pytestmark = pytest.mark.django_db


class TestPhotoBoothBrandHome(IsAuthenticateTestCase):
    url = reverse("api-photo-booths:photo-booth-brand-home")

    def test_photo_booth_brand_home_get_success_single_photo_booth_brand(self, valid_user, photo_booth_brand):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            path=self.url,
            data={
                "limit": 1,
                "offset": 0,
            },
        )

        assert response.status_code == 200
        assert response.data["data"]["results"][0]["name"] == photo_booth_brand.name
        assert response.data["data"]["results"][0]["main_thumbnail_image_url"] == photo_booth_brand.main_thumbnail_image_url

    def test_photo_booth_brand_home_get_success_pagination(self, valid_user, photo_booth_brand_list):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            path=self.url,
            data={
                "limit": 3,
                "offset": 0,
            },
        )

        assert response.status_code == 200
        assert response.data["data"]["count"] == len(photo_booth_brand_list)
        assert len(response.data["data"]["results"]) == 3
