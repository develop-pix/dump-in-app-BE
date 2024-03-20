import pytest
from django.urls import reverse

from tests.utils import IsAuthenticateTestCase

pytestmark = pytest.mark.django_db


class TestMyEventLike(IsAuthenticateTestCase):
    url = reverse("api-users:user-event-like-list")

    def test_my_event_like_get_success_single_event(self, valid_user, valid_event):
        valid_event.user_event_like_logs.add(valid_user)

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
        assert response.data["data"]["count"] == 1
        assert response.data["data"]["results"][0]["id"] == valid_event.id
        assert response.data["data"]["results"][0]["title"] == valid_event.title
        assert response.data["data"]["results"][0]["main_thumbnail_image_url"] == valid_event.main_thumbnail_image_url
        assert response.data["data"]["results"][0]["is_liked"]

    def test_my_event_like_get_success_pagination(self, valid_user, valid_event_list):
        for valid_event in valid_event_list:
            valid_event.user_event_like_logs.add(valid_user)

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
        assert response.data["data"]["count"] == 10
        assert len(response.data["data"]["results"]) == 10

    def test_my_event_like_get_fail_not_authenticated(self):
        response = self.client.get(self.url)

        assert response.status_code == 401
        assert response.data["code"] == "not_authenticated"
        assert response.data["message"] == "Authentication credentials were not provided."
