import pytest
from django.urls import reverse

from tests.utils import IsAuthenticateTestCase

pytestmark = pytest.mark.django_db


class TestPhotoBoothLocationList(IsAuthenticateTestCase):
    url = reverse("api-photo-booths:photo-booth-location-list")

    def test_photo_booth_location_list_get_success(self, photo_booth_list, valid_user):
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

        assert response.status_code == 200
        assert len(response.data["data"]) == len(photo_booth_list)

    def test_photo_booth_location_list_get_success_single(self, photo_booth, valid_user):
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

        assert response.status_code == 200
        assert len(response.data["data"]) == 1
        assert response.data["data"][0]["id"] == str(photo_booth.id)
        assert response.data["data"][0]["name"] == photo_booth.name
        assert response.data["data"][0]["latitude"] == float(photo_booth.latitude)
        assert response.data["data"][0]["longitude"] == float(photo_booth.longitude)
        assert not response.data["data"][0]["is_liked"]
        assert response.data["data"][0]["photo_booth_brand"]["name"] == photo_booth.photo_booth_brand.name
        assert response.data["data"][0]["photo_booth_brand"]["logo_image_url"] == photo_booth.photo_booth_brand.logo_image_url
        assert response.data["data"][0]["photo_booth_brand"]["hashtag"][0]["id"] == photo_booth.photo_booth_brand.hashtag.all()[0].id
        assert response.data["data"][0]["photo_booth_brand"]["hashtag"][0]["name"] == photo_booth.photo_booth_brand.hashtag.all()[0].name

    def test_photo_booth_location_list_get_fail_not_authenticated(self):
        response = self.client.get(self.url)

        assert response.status_code == 401
        assert response.data["code"] == "not_authenticated"
        assert response.data["message"] == "Authentication credentials were not provided."

    def test_photo_booth_location_list_get_fail_radis_required(self, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            path=self.url,
            data={
                "longitude": 126.97151987127677,
                "latitude": 37.55558726825372,
            },
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"radius": ["This field is required."]}

    def test_photo_booth_location_list_get_fail_latitude_required(self, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            path=self.url,
            data={
                "longitude": 126.97151987127677,
                "radius": 1.5,
            },
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"latitude": ["This field is required."]}

    def test_photo_booth_location_list_get_fail_longitude_required(self, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            path=self.url,
            data={
                "latitude": 37.55558726825372,
                "radius": 1.5,
            },
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"longitude": ["This field is required."]}

    def test_photo_booth_location_list_get_fail_latitude_max_value(self, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            path=self.url,
            data={
                "longitude": 126.97151987127677,
                "latitude": 91,
                "radius": 1.5,
            },
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"latitude": ["Ensure this value is less than or equal to 90."]}

    def test_photo_booth_location_list_get_fail_latitude_min_value(self, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            path=self.url,
            data={
                "longitude": 126.97151987127677,
                "latitude": -91,
                "radius": 1.5,
            },
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"latitude": ["Ensure this value is greater than or equal to -90."]}

    def test_photo_booth_location_list_get_fail_longitude_max_value(self, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(self.url, data={"longitude": 181, "latitude": 37.55558726825372, "radius": 1.5})

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"longitude": ["Ensure this value is less than or equal to 180."]}

    def test_photo_booth_location_list_get_fail_longitude_min_value(self, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(self.url, data={"longitude": -181, "latitude": 37.55558726825372, "radius": 1.5})

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"longitude": ["Ensure this value is greater than or equal to -180."]}

    def test_photo_booth_location_list_get_fail_radius_max_value(self, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            path=self.url,
            data={
                "longitude": 126.97151987127677,
                "latitude": 37.55558726825372,
                "radius": 100000,
            },
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"radius": ["Ensure this value is less than or equal to 1.5."]}

    def test_photo_booth_location_list_get_fail_radius_min_value(self, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            path=self.url,
            data={
                "longitude": 126.97151987127677,
                "latitude": 37.55558726825372,
                "radius": -1,
            },
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"radius": ["Ensure this value is greater than or equal to 0."]}

    def test_photo_booth_location_list_get_fail_latitude_invalid_format(self, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(self.url, data={"longitude": 126.97151987127677, "latitude": "a", "radius": 1.5})

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"latitude": ["A valid number is required."]}

    def test_photo_booth_location_list_get_fail_longitude_invalid_format(self, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(self.url, data={"longitude": "a", "latitude": 37.55558726825372, "radius": 1.5})

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"longitude": ["A valid number is required."]}

    def test_photo_booth_location_list_get_fail_radius_invalid_format(self, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(self.url, data={"longitude": 126.97151987127677, "latitude": 37.55558726825372, "radius": "a"})

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"radius": ["A valid number is required."]}
