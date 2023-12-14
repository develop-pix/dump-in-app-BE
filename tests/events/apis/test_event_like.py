import pytest
from django.urls import reverse

from tests.utils import IsAuthenticateTestCase

pytestmark = pytest.mark.django_db


class TestEventLike(IsAuthenticateTestCase):
    def test_event_like_post_success(self, valid_event, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.post(
            path=reverse(
                "api-events:event-like",
                kwargs={
                    "event_id": valid_event.id,
                },
            ),
        )

        assert response.status_code == 200
        assert response.data["data"]["is_liked"] is True
        assert response.data["data"]["event_id"] == valid_event.id

    def test_event_like_post_suceess_already_liked(self, valid_event, valid_user):
        valid_event.user_event_like_logs.add(valid_user)

        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.post(
            path=reverse(
                "api-events:event-like",
                kwargs={
                    "event_id": valid_event.id,
                },
            ),
        )

        assert response.status_code == 200
        assert response.data["data"]["is_liked"] is False
        assert response.data["data"]["event_id"] == valid_event.id

    def test_event_like_post_fail_not_authenticated(self):
        response = self.client.post(
            path=reverse(
                "api-events:event-like",
                kwargs={
                    "event_id": 1,
                },
            ),
        )

        assert response.status_code == 401
        assert response.data["message"] == "Authentication credentials were not provided."
