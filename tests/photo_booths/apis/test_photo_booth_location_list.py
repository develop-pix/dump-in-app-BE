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

    def test_photo_booth_location_list_get_success_anonymous_user(self, photo_booth_list, valid_user):
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
