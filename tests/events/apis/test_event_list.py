import pytest
from django.urls import reverse

from tests.utils import IsAuthenticateTestCase

pytestmark = pytest.mark.django_db


class TestEventList(IsAuthenticateTestCase):
    url = reverse("api-events:event-list")

    def test_event_list_get_success_single_event(self, valid_user, valid_event):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            path=self.url,
            data={
                "limit": 1,
                "offset": 0,
            },
        )

        assert response.status_code == 200
        assert response.data["data"]["results"][0]["id"] == valid_event.id
        assert response.data["data"]["results"][0]["title"] == valid_event.title
        assert response.data["data"]["results"][0]["main_thumbnail_image_url"] == valid_event.main_thumbnail_image_url
        assert not response.data["data"]["results"][0]["is_liked"]
        assert response.data["data"]["results"][0]["photo_booth_brand_name"] == valid_event.photo_booth_brand.name

    def test_event_list_get_success_pagination(self, valid_user, valid_event_list):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            path=self.url,
            data={
                "limit": 10,
                "offset": 0,
            },
        )

        assert response.status_code == 200
        assert response.data["data"]["count"] == len(valid_event_list)
        assert len(response.data["data"]["results"]) == 10

    def test_event_list_get_success_with_filter(self, valid_event, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            path=self.url,
            data={"hashtag": valid_event.hashtag.first().name},
        )

        assert response.status_code == 200
        assert response.data["data"]["results"][0]["id"] == valid_event.id
        assert response.data["data"]["results"][0]["title"] == valid_event.title
        assert response.data["data"]["results"][0]["main_thumbnail_image_url"] == valid_event.main_thumbnail_image_url
        assert not response.data["data"]["results"][0]["is_liked"]
        assert response.data["data"]["results"][0]["photo_booth_brand_name"] == valid_event.photo_booth_brand.name

    def test_event_list_get_success_anonymous_user(self, valid_event):
        response = self.client.get(
            path=self.url,
            data={
                "limit": 1,
                "offset": 0,
            },
        )

        assert response.status_code == 200
        assert response.data["data"]["results"][0]["id"] == valid_event.id
        assert response.data["data"]["results"][0]["title"] == valid_event.title
        assert response.data["data"]["results"][0]["main_thumbnail_image_url"] == valid_event.main_thumbnail_image_url
        assert response.data["data"]["results"][0]["is_liked"] is None
        assert response.data["data"]["results"][0]["photo_booth_brand_name"] == valid_event.photo_booth_brand.name
