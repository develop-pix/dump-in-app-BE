import pytest
from django.urls import reverse

from tests.utils import IsAuthenticateTestCase

pytestmark = pytest.mark.django_db


class TestPhotoBoothBrandDetailAPI(IsAuthenticateTestCase):
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

    def test_photo_booth_brand_detail_get_fail_not_authenticated(self, photo_booth_brand):
        response = self.client.get(
            path=reverse(
                "api-photo-booths:photo-booth-brand-detail",
                kwargs={
                    "photo_booth_brand_id": photo_booth_brand.id,
                },
            ),
        )

        assert response.status_code == 401
        assert response.data["message"] == "Authentication credentials were not provided."
