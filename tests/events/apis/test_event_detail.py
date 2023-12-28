import pytest
from django.urls import reverse

from tests.utils import IsAuthenticateTestCase

pytestmark = pytest.mark.django_db


class TestEventDetail(IsAuthenticateTestCase):
    def test_event_detail_get_success(self, valid_event, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            path=reverse(
                "api-events:event-detail",
                kwargs={
                    "event_id": valid_event.id,
                },
            ),
        )

        assert response.status_code == 200
        assert response.data["data"]["id"] == valid_event.id
        assert response.data["data"]["title"] == valid_event.title
        assert response.data["data"]["content"] == valid_event.content
        assert response.data["data"]["main_thumbnail_image_url"] == valid_event.main_thumbnail_image_url
        assert not response.data["data"]["is_liked"]
        assert response.data["data"]["hashtag"][0]["id"] == valid_event.hashtag.all()[0].id
        assert response.data["data"]["hashtag"][0]["name"] == valid_event.hashtag.all()[0].name
        assert response.data["data"]["image"][0]["id"] == valid_event.event_image.all()[0].id
        assert response.data["data"]["image"][0]["image_url"] == valid_event.event_image.all()[0].event_image_url

    def test_event_detail_get_fail_not_authenticated(self):
        response = self.client.get(
            path=reverse(
                "api-events:event-detail",
                kwargs={
                    "event_id": 1,
                },
            ),
        )

        assert response.status_code == 401
        assert response.data["code"] == "not_authenticated"
        assert response.data["message"] == "Authentication credentials were not provided."

    def test_event_detail_get_fail_does_not_exist(self, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            path=reverse(
                "api-events:event-detail",
                kwargs={
                    "event_id": 99999,
                },
            ),
        )

        assert response.status_code == 404
        assert response.data["code"] == "not_found"
        assert response.data["message"] == "Event does not exist."
