import uuid

from django.urls import reverse

from tests.utils import IsAuthenticateTestCase


class TestPhotoBoothDetail(IsAuthenticateTestCase):
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
                "longitude": 126.97151987127677,
                "latitude": 37.55558726825372,
            },
        )

        assert response.status_code == 200
        assert response.data["data"]["id"] == photo_booth.id
        assert response.data["data"]["location"] == photo_booth.location
        assert response.data["data"]["latitude"] == float(photo_booth.latitude)
        assert response.data["data"]["longitude"] == float(photo_booth.longitude)
        assert response.data["data"]["street_address"] == photo_booth.street_address
        assert response.data["data"]["road_address"] == photo_booth.road_address
        assert response.data["data"]["operation_time"] == photo_booth.operation_time
        assert not response.data["data"]["is_liked"]
        assert response.data["data"]["photo_booth_brand"]["name"] == photo_booth.photo_booth_brand.name
        assert (
            response.data["data"]["photo_booth_brand"]["image"][0]["id"]
            == photo_booth.photo_booth_brand.photo_booth_brand_image.all()[0].id
        )
        assert (
            response.data["data"]["photo_booth_brand"]["image"][0]["image_url"]
            == photo_booth.photo_booth_brand.photo_booth_brand_image.all()[0].photo_booth_brand_image_url
        )
        assert response.data["data"]["photo_booth_brand"]["hashtag"][0]["id"] == photo_booth.photo_booth_brand.hashtag.all()[0].id
        assert response.data["data"]["photo_booth_brand"]["hashtag"][0]["name"] == photo_booth.photo_booth_brand.hashtag.all()[0].name

    def test_photo_booth_detail_get_success_anoymous_user(self, photo_booth):
        response = self.client.get(
            path=reverse(
                "api-photo-booths:photo-booth-detail",
                kwargs={
                    "photo_booth_id": photo_booth.id,
                },
            ),
            data={
                "longitude": 126.97151987127677,
                "latitude": 37.55558726825372,
            },
        )

        assert response.status_code == 200
        assert response.data["data"]["id"] == photo_booth.id
        assert response.data["data"]["location"] == photo_booth.location
        assert response.data["data"]["latitude"] == float(photo_booth.latitude)
        assert response.data["data"]["longitude"] == float(photo_booth.longitude)
        assert response.data["data"]["street_address"] == photo_booth.street_address
        assert response.data["data"]["road_address"] == photo_booth.road_address
        assert response.data["data"]["operation_time"] == photo_booth.operation_time
        assert response.data["data"]["is_liked"] is None
        assert response.data["data"]["photo_booth_brand"]["name"] == photo_booth.photo_booth_brand.name
        assert (
            response.data["data"]["photo_booth_brand"]["image"][0]["id"]
            == photo_booth.photo_booth_brand.photo_booth_brand_image.all()[0].id
        )
        assert (
            response.data["data"]["photo_booth_brand"]["image"][0]["image_url"]
            == photo_booth.photo_booth_brand.photo_booth_brand_image.all()[0].photo_booth_brand_image_url
        )
        assert response.data["data"]["photo_booth_brand"]["hashtag"][0]["id"] == photo_booth.photo_booth_brand.hashtag.all()[0].id
        assert response.data["data"]["photo_booth_brand"]["hashtag"][0]["name"] == photo_booth.photo_booth_brand.hashtag.all()[0].name

    def test_photo_Booth_detail_get_success_location_is_none(self, photo_booth, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            path=reverse(
                "api-photo-booths:photo-booth-detail",
                kwargs={
                    "photo_booth_id": photo_booth.id,
                },
            ),
        )

        assert response.status_code == 200
        assert response.data["data"]["id"] == photo_booth.id
        assert response.data["data"]["location"] == photo_booth.location
        assert response.data["data"]["latitude"] == float(photo_booth.latitude)
        assert response.data["data"]["longitude"] == float(photo_booth.longitude)
        assert response.data["data"]["street_address"] == photo_booth.street_address
        assert response.data["data"]["road_address"] == photo_booth.road_address
        assert response.data["data"]["operation_time"] == photo_booth.operation_time
        assert not response.data["data"]["is_liked"]
        assert response.data["data"]["photo_booth_brand"]["name"] == photo_booth.photo_booth_brand.name
        assert (
            response.data["data"]["photo_booth_brand"]["image"][0]["id"]
            == photo_booth.photo_booth_brand.photo_booth_brand_image.all()[0].id
        )
        assert (
            response.data["data"]["photo_booth_brand"]["image"][0]["image_url"]
            == photo_booth.photo_booth_brand.photo_booth_brand_image.all()[0].photo_booth_brand_image_url
        )
        assert response.data["data"]["photo_booth_brand"]["hashtag"][0]["id"] == photo_booth.photo_booth_brand.hashtag.all()[0].id
        assert response.data["data"]["photo_booth_brand"]["hashtag"][0]["name"] == photo_booth.photo_booth_brand.hashtag.all()[0].name
        assert response.data["data"]["distance"] is None

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
                "longitude": 126.97151987127677,
                "latitude": 37.55558726825372,
            },
        )

        assert response.status_code == 404
        assert response.data["code"] == "not_found"
        assert response.data["message"] == "Photo Booth does not exist"
