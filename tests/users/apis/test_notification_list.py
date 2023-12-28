import pytest
from django.urls import reverse

from tests.utils import IsAuthenticateTestCase

pytestmark = pytest.mark.django_db


class TestNotificaitonList(IsAuthenticateTestCase):
    url = reverse("api-users:user-notification-list")

    def test_notification_list_get_success(self, valid_notification_list):
        access_token = self.obtain_token(valid_notification_list[0].user)
        self.authenticate_with_token(access_token)
        response = self.client.get(self.url)

        assert response.status_code == 200
        assert len(response.data["data"]) == 100

    def test_notification_list_get_fail_not_authenticated(self):
        response = self.client.get(self.url)

        assert response.status_code == 401
        assert response.data["code"] == "not_authenticated"
        assert response.data["message"] == "Authentication credentials were not provided."

    def test_notification_list_delete_success(self, valid_notification_list):
        access_token = self.obtain_token(valid_notification_list[0].user)
        self.authenticate_with_token(access_token)
        response = self.client.delete(self.url)

        assert response.status_code == 204
        valid_notification_list[0].refresh_from_db()
        assert valid_notification_list[0].is_deleted

    def test_notification_list_delete_fail_not_authenticated(self):
        response = self.client.delete(self.url)

        assert response.status_code == 401
        assert response.data["code"] == "not_authenticated"
        assert response.data["message"] == "Authentication credentials were not provided."
