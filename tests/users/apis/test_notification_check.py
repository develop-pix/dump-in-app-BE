import pytest
from django.urls import reverse

from tests.utils import IsAuthenticateTestCase

pytestmark = pytest.mark.django_db


class TestNotificaitonCheck(IsAuthenticateTestCase):
    url = reverse("api-users:user-notification-check")

    def test_notification_check_get_success(self, valid_notification):
        access_token = self.obtain_token(valid_notification.user)
        self.authenticate_with_token(access_token)
        response = self.client.get(self.url)

        assert response.status_code == 200
        assert response.data["data"]["is_unread"]
        assert response.data["data"]["count"] == 1

    def test_notification_check_get_fail_not_authenticated(self):
        response = self.client.get(self.url)

        assert response.status_code == 401
        assert response.data["code"] == "not_authenticated"
        assert response.data["message"] == "Authentication credentials were not provided."
