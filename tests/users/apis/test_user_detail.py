import pytest
from django.urls import reverse

from tests.utils import IsAuthenticateTestCase

pytestmark = pytest.mark.django_db


class TestUserDetail(IsAuthenticateTestCase):
    url = reverse("api-users:user-detail")

    def test_user_detail_get_success(self, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(self.url)

        assert response.status_code == 200
        assert response.data["data"]["id"] == valid_user.id
        assert response.data["data"]["email"] == valid_user.email
        assert response.data["data"]["nickname"] == valid_user.nickname

    def test_user_detail_get_fail_not_authenticated(self):
        response = self.client.get(self.url)

        assert response.status_code == 401
        assert response.data["code"] == "not_authenticated"
        assert response.data["message"] == "Authentication credentials were not provided."

    def test_user_detail_put_success(self, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.put(
            self.url,
            data={"nickname": "nickname"},
            format="json",
        )

        assert response.status_code == 200
        assert response.data["data"]["id"] == valid_user.id
        assert response.data["data"]["email"] == valid_user.email
        assert response.data["data"]["nickname"] == "nickname"

    def test_user_detail_put_fail_not_authenticated(self):
        response = self.client.put(
            self.url,
            data={"nickname": "nickname"},
            format="json",
        )

        assert response.status_code == 401
        assert response.data["code"] == "not_authenticated"
        assert response.data["message"] == "Authentication credentials were not provided."

    def test_user_detail_delete_success(self, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.delete(self.url)

        assert response.status_code == 204

    def test_user_detail_delete_fail_not_authenticated(self):
        response = self.client.delete(self.url)

        assert response.status_code == 401
        assert response.data["code"] == "not_authenticated"
        assert response.data["message"] == "Authentication credentials were not provided."
