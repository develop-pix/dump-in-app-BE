import pytest
from django.urls import reverse

from tests.utils import IsAuthenticateTestCase

pytestmark = pytest.mark.django_db


class TestPhotoBoothBrandEventList(IsAuthenticateTestCase):
    def test_photo_booth_brand_event_list_get_success(self, valid_event, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            path=reverse(
                "api-photo-booths:photo-booth-brand-event-list",
                kwargs={
                    "photo_booth_brand_id": valid_event.photo_booth_brand.id,
                },
            ),
        )

        assert response.status_code == 200
        assert response.data["data"][0]["id"] == valid_event.id
        assert response.data["data"][0]["title"] == valid_event.title

    def test_photo_booth_brand_event_list_get_success_limit(self, valid_event_list, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            path=reverse(
                "api-photo-booths:photo-booth-brand-event-list",
                kwargs={
                    "photo_booth_brand_id": valid_event_list[0].photo_booth_brand.id,
                },
            ),
            data={"limit": 3},
        )

        assert response.status_code == 200
        assert len(response.data["data"]) == 3

    def test_photo_booth_brand_event_list_get_fail_not_authenticated(self, valid_event):
        response = self.client.get(
            path=reverse(
                "api-photo-booths:photo-booth-brand-event-list",
                kwargs={
                    "photo_booth_brand_id": valid_event.photo_booth_brand.id,
                },
            ),
        )

        assert response.status_code == 401
        assert response.data["message"] == "Authentication credentials were not provided."
