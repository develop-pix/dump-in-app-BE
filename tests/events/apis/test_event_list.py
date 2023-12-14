import pytest
from django.urls import reverse

from tests.utils import IsAuthenticateTestCase

pytestmark = pytest.mark.django_db


class TestEventLike(IsAuthenticateTestCase):
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
        assert response.data["data"].get("count") == 1

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
        assert response.data["data"].get("count") == 100

    def test_event_list_get_success_with_filter(self, valid_event, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            path=self.url,
            data={"hashtag": valid_event.hashtag.first().id},
        )

        assert response.status_code == 200
        assert response.data["data"].get("count") == 1

    def test_event_list_get_fail_not_authenticated(self):
        response = self.client.get(path=self.url)

        assert response.status_code == 401
        assert response.data["message"] == "Authentication credentials were not provided."
