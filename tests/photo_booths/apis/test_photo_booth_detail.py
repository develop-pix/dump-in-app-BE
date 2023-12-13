import uuid

from django.urls import reverse

from tests.utils import IsAuthenticateTestCase


class TestPhotoBoothDetailAPI(IsAuthenticateTestCase):
    def test_photo_booth_detail_get_success(self, photo_booth, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            path=reverse(
                "api-photo-booths:photo-booth-detail",
                kwargs={
                    "photo_booth_id": photo_booth.id,
                },
            ),
            data={
                "latitude": 126.97151987127677,
                "longitude": 37.55558726825372,
            },
        )

        assert response.status_code == 200
        assert response.data["data"].get("id") == photo_booth.id
        assert response.data["data"].get("photo_booth_name") == photo_booth.name
        assert response.data["data"].get("photo_booth_brand_name") == photo_booth.photo_booth_brand.name
        assert response.data["data"].get("latitude") == float(photo_booth.latitude)
        assert response.data["data"].get("longitude") == float(photo_booth.longitude)
        assert response.data["data"].get("street_address") == photo_booth.street_address
        assert response.data["data"].get("road_address") == photo_booth.road_address

    def test_photo_booth_detail_get_fail_not_authenticated(self, photo_booth):
        response = self.client.get(
            path=reverse(
                "api-photo-booths:photo-booth-detail",
                kwargs={
                    "photo_booth_id": photo_booth.id,
                },
            ),
        )

        assert response.status_code == 401
        assert response.data["message"] == "Authentication credentials were not provided."

    def test_photo_booth_detail_get_fail_latitude_required(self, photo_booth, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            path=reverse(
                "api-photo-booths:photo-booth-detail",
                kwargs={
                    "photo_booth_id": photo_booth.id,
                },
            ),
            data={
                "longitude": 126.97151987127677,
            },
        )

        assert response.status_code == 400
        assert response.data["message"] == "Invalid parameter format"

    def test_photo_booth_detail_get_fail_longitude_required(self, photo_booth, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            path=reverse(
                "api-photo-booths:photo-booth-detail",
                kwargs={
                    "photo_booth_id": photo_booth.id,
                },
            ),
            data={
                "latitude": 126.97151987127677,
            },
        )

        assert response.status_code == 400
        assert response.data["message"] == "Invalid parameter format"

    def test_photo_booth_detail_get_fail_does_not_exist(self, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            path=reverse(
                "api-photo-booths:photo-booth-detail",
                kwargs={
                    "photo_booth_id": uuid.uuid4(),
                },
            ),
            data={
                "latitude": 126.97151987127677,
                "longitude": 37.55558726825372,
            },
        )

        assert response.status_code == 404
        assert response.data["message"] == "Photo Booth does not exist"
