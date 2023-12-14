import pytest
from django.urls import reverse

from tests.utils import IsAuthenticateTestCase

pytestmark = pytest.mark.django_db


class TestMyEventLikeAPI(IsAuthenticateTestCase):
    url = reverse("api-users:user-event-like")

    def test_my_event_like_get_success_single_event(self, valid_user, valid_event):
        valid_event.user_event_like_logs.add(valid_user)

        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(self.url)

        assert response.status_code == 200
        assert response.data["data"].get("count") == 1

    def test_my_event_like_get_success_pagination(self, valid_user, valid_event_list):
        for valid_event in valid_event_list:
            valid_event.user_event_like_logs.add(valid_user)

        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(self.url)

        assert response.status_code == 200
        assert response.data["data"].get("count") == 100

    def test_my_event_like_get_fail_not_authenticated(self):
        response = self.client.get(self.url)

        assert response.status_code == 401
        assert response.data["message"] == "Authentication credentials were not provided."
