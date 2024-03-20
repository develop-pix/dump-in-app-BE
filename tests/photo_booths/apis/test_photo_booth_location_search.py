import pytest
from django.urls import reverse

from tests.utils import IsAuthenticateTestCase

pytestmark = pytest.mark.django_db


class TestPhotoBoothLocationSearch(IsAuthenticateTestCase):
    url = reverse("api-photo-booths:photo-booth-location-search")

    def test_photo_booth_location_search_get_success(self, photo_booth, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            path=self.url,
            data={
                "photo_booth_brand_name": photo_booth.photo_booth_brand.name,
                "longitude": 126.97151987127677,
                "latitude": 37.55558726825372,
                "radius": 1.5,
            },
        )

        assert response.status_code == 200
        assert len(response.data["data"]) == 1
        assert response.data["data"][0]["id"] == photo_booth.id
        assert response.data["data"][0]["name"] == photo_booth.name

    def test_photo_booth_location_search_get_success_anonymous_user(self, photo_booth):
        response = self.client.get(
            path=self.url,
            data={
                "photo_booth_brand_name": photo_booth.photo_booth_brand.name,
                "longitude": 126.97151987127677,
                "latitude": 37.55558726825372,
                "radius": 1.5,
            },
        )

        assert response.status_code == 200
        assert len(response.data["data"]) == 1
        assert response.data["data"][0]["id"] == photo_booth.id
        assert response.data["data"][0]["name"] == photo_booth.name
