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

    def test_photo_booth_location_search_get_fail_not_authenticated(self):
        response = self.client.get(self.url)

        assert response.status_code == 401
        assert response.data["code"] == "not_authenticated"
        assert response.data["message"] == "Authentication credentials were not provided."

    def test_photo_booth_location_search_get_fail_radius_required(self, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            path=self.url,
            data={
                "photo_booth_brand_name": "invalid",
                "longitude": 126.97151987127677,
                "latitude": 37.55558726825372,
            },
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"radius": ["This field is required."]}

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
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"latitude": ["This field is required."]}

    def test_photo_booth_location_search_get_fail_longitude_required(self, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            path=self.url,
            data={
                "photo_booth_brand_name": "invalid",
                "latitude": 37.55558726825372,
                "radius": 1.5,
            },
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"longitude": ["This field is required."]}

    def test_photo_booth_location_search_get_fail_photo_booth_brand_name_required(self, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            path=self.url,
            data={
                "longitude": 126.97151987127677,
                "latitude": 37.55558726825372,
                "radius": 1.5,
            },
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"photo_booth_brand_name": ["This field is required."]}

    def test_photo_booth_location_search_get_fail_photo_booth_brand_name_max_length(self, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            path=self.url,
            data={
                "photo_booth_brand_name": "a" * 65,
                "longitude": 126.97151987127677,
                "latitude": 37.55558726825372,
                "radius": 1.5,
            },
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"photo_booth_brand_name": ["Ensure this field has no more than 64 characters."]}

    def test_photo_booth_location_search_get_fail_longitude_max_value(self, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            path=self.url,
            data={
                "photo_booth_brand_name": "invalid",
                "longitude": 181,
                "latitude": 37.55558726825372,
                "radius": 1.5,
            },
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"longitude": ["Ensure this value is less than or equal to 180."]}

    def test_photo_booth_location_search_get_fail_longitude_min_value(self, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            path=self.url,
            data={
                "photo_booth_brand_name": "invalid",
                "longitude": -181,
                "latitude": 37.55558726825372,
                "radius": 1.5,
            },
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"longitude": ["Ensure this value is greater than or equal to -180."]}

    def test_photo_booth_location_search_get_fail_latitude_min_value(self, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            path=self.url,
            data={
                "photo_booth_brand_name": "invalid",
                "longitude": 126.97151987127677,
                "latitude": -91,
                "radius": 1.5,
            },
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"latitude": ["Ensure this value is greater than or equal to -90."]}

    def test_photo_booth_location_search_get_fail_latitude_max_value(self, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            path=self.url,
            data={
                "photo_booth_brand_name": "invalid",
                "longitude": 126.97151987127677,
                "latitude": 91,
                "radius": 1.5,
            },
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"latitude": ["Ensure this value is less than or equal to 90."]}

    def test_photo_booth_location_search_get_fail_radius_min_value(self, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            path=self.url,
            data={
                "photo_booth_brand_name": "invalid",
                "longitude": 126.97151987127677,
                "latitude": 37.55558726825372,
                "radius": -1,
            },
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"radius": ["Ensure this value is greater than or equal to 0."]}

    def test_photo_booth_location_search_get_fail_radius_max_value(self, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            path=self.url,
            data={
                "photo_booth_brand_name": "invalid",
                "longitude": 126.97151987127677,
                "latitude": 37.55558726825372,
                "radius": 100000,
            },
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"radius": ["Ensure this value is less than or equal to 1.5."]}

    def test_photo_booth_location_search_get_fail_longitude_invalid_format(self, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            path=self.url,
            data={
                "photo_booth_brand_name": "invalid",
                "longitude": "invalid",
                "latitude": 37.55558726825372,
                "radius": 1,
            },
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"longitude": ["A valid number is required."]}

    def test_photo_booth_location_search_get_fail_latitude_invalid_format(self, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            path=self.url,
            data={
                "photo_booth_brand_name": "invalid",
                "longitude": 126.97151987127677,
                "latitude": "invalid",
                "radius": 1,
            },
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"latitude": ["A valid number is required."]}

    def test_photo_booth_location_search_get_fail_radius_invalid_format(self, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            path=self.url,
            data={
                "photo_booth_brand_name": "invalid",
                "longitude": 126.97151987127677,
                "latitude": 37.55558726825372,
                "radius": "invalid",
            },
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"radius": ["A valid number is required."]}
