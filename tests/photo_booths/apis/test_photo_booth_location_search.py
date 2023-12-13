import pytest
from django.urls import reverse

from tests.utils import IsAuthenticateTestCase

pytestmark = pytest.mark.django_db


class TestPhotoBoothLocationSearchAPI(IsAuthenticateTestCase):
    url = reverse("api-photo-booths:photo-booth-location-search")

    def test_photo_booth_location_search_get_success(self, photo_booth, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            path=self.url,
            data={
                "photo_booth_brand_name": photo_booth.photo_booth_brand.name,
                "latitude": 126.97151987127677,
                "longitude": 37.55558726825372,
                "radius": 1.5,
            },
        )

        assert response.status_code == 200
        assert len(response.data["data"]) == 1

    def test_photo_booth_location_search_get_fail_not_authenticated(self):
        response = self.client.get(self.url)

        assert response.status_code == 401
        assert response.data["message"] == "Authentication credentials were not provided."

    def test_photo_booth_location_search_get_fail_radius_required(self, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            path=self.url,
            data={
                "photo_booth_brand_name": "invalid",
                "latitude": 126.97151987127677,
                "longitude": 37.55558726825372,
            },
        )

        assert response.status_code == 400
        assert response.data["message"] == "Invalid parameter format"

    def test_photo_booth_location_search_get_fail_latitude_required(self, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            path=self.url,
            data={
                "photo_booth_brand_name": "invalid",
                "longitude": 126.97151987127677,
                "radius": 1.5,
            },
        )

        assert response.status_code == 400
        assert response.data["message"] == "Invalid parameter format"

    def test_photo_booth_location_search_get_fail_longitude_required(self, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            path=self.url,
            data={
                "photo_booth_brand_name": "invalid",
                "latitude": 126.97151987127677,
                "radius": 1.5,
            },
        )

        assert response.status_code == 400
        assert response.data["message"] == "Invalid parameter format"

    def test_photo_booth_location_search_get_fail_photo_booth_brand_name_required(self, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            path=self.url,
            data={
                "latitude": 126.97151987127677,
                "longitude": 37.55558726825372,
                "radius": 1.5,
            },
        )

        assert response.status_code == 400
        assert response.data["message"] == "Invalid parameter format"

    def test_photo_booth_location_search_get_fail_radius_max_value(self, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            path=self.url,
            data={
                "photo_booth_brand_name": "invalid",
                "latitude": 126.97151987127677,
                "longitude": 37.55558726825372,
                "radius": 100000,
            },
        )

        assert response.status_code == 400
        assert response.data["message"] == "Invalid parameter format"
