import pytest
from django.urls import reverse

from tests.utils import IsAuthenticateTestCase

pytestmark = pytest.mark.django_db


class TestNotificaitonDetail(IsAuthenticateTestCase):
    def test_notification_detail_get_success(self, valid_notification):
        access_token = self.obtain_token(valid_notification.user)
        self.authenticate_with_token(access_token)
        response = self.client.put(path=reverse("api-users:user-notification-detail", kwargs={"notification_id": valid_notification.id}))

        assert response.status_code == 200
        assert response.data["data"]["id"] == valid_notification.id
        assert response.data["data"]["title"] == valid_notification.title
        assert response.data["data"]["content"] == valid_notification.content
        assert response.data["data"]["is_read"] == True
        assert response.data["data"]["parameter_data"] == valid_notification.parameter_data
        assert response.data["data"]["category"] == valid_notification.category.name

    def test_notification_detail_get_fail_not_authenticated(self):
        response = self.client.get(path=reverse("api-users:user-notification-detail", kwargs={"notification_id": 1}))

        assert response.status_code == 401
        assert response.data["code"] == "not_authenticated"
        assert response.data["message"] == "Authentication credentials were not provided."
