import pytest
from django.urls import reverse

from tests.utils import IsAuthenticateTestCase

pytestmark = pytest.mark.django_db


class TestPhotoBoothBrandEventList(IsAuthenticateTestCase):
    def test_photo_booth_brand_event_list_get_success_single_event(self, valid_event, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            path=reverse(
                "api-photo-booths:photo-booth-brand-event-list",
                kwargs={
                    "photo_booth_brand_id": valid_event.photo_booth_brand.id,
                },
            ),
            data={
                "limit": 1,
                "offset": 0,
            },
        )

        assert response.status_code == 200
        assert len(response.data["data"]["results"]) == 1
        assert response.data["data"]["results"][0]["id"] == valid_event.id
        assert response.data["data"]["results"][0]["title"] == valid_event.title
        assert response.data["data"]["results"][0]["main_thumbnail_image_url"] == valid_event.main_thumbnail_image_url
        assert not response.data["data"]["results"][0]["is_liked"]

    def test_photo_booth_brand_event_list_get_success_pagination(self, valid_event_list, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            path=reverse(
                "api-photo-booths:photo-booth-brand-event-list",
                kwargs={
                    "photo_booth_brand_id": valid_event_list[0].photo_booth_brand.id,
                },
            ),
            data={"limit": 3, "offset": 0},
        )

        assert response.status_code == 200
        assert len(response.data["data"]["results"]) == 3

    def test_photo_booth_brand_event_list_get_success_anonymous_user(self, valid_event):
        response = self.client.get(
            path=reverse(
                "api-photo-booths:photo-booth-brand-event-list",
                kwargs={
                    "photo_booth_brand_id": valid_event.photo_booth_brand.id,
                },
            ),
        )

        assert response.status_code == 200
        assert len(response.data["data"]["results"]) == 1
        assert response.data["data"]["results"][0]["id"] == valid_event.id
        assert response.data["data"]["results"][0]["title"] == valid_event.title
        assert response.data["data"]["results"][0]["main_thumbnail_image_url"] == valid_event.main_thumbnail_image_url
        assert response.data["data"]["results"][0]["is_liked"] is None

    def test_photo_booth_brand_event_list_get_fail_not_exist_photo_booth_brand(self, valid_event, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            path=reverse(
                "api-photo-booths:photo-booth-brand-event-list",
                kwargs={
                    "photo_booth_brand_id": 9999,
                },
            ),
        )

        assert response.status_code == 404
        assert response.data["code"] == "not_found"
        assert response.data["message"] == "Photo Booth Brand does not exist"
