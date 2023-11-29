import pytest
from django.urls import reverse

from tests.utils import IsAuthenticateTestCase

pytestmark = pytest.mark.django_db


class TestUserDetailAPI(IsAuthenticateTestCase):
    url = reverse("api-users:user-detail")

    def test_user_detail_get_success(self, new_users):
        access_token = self.obtain_token(new_users)
        self.authenticate_with_token(access_token)
        response = self.client.get(self.url)

        assert response.status_code == 200
        assert response.data["data"] == {
            "id": 11,
            "email": "test11@test.com",
            "nickname": "test11",
        }

    def test_user_detail_get_fail_not_authenticated(self):
        response = self.client.get(self.url)

        assert response.status_code == 401
        assert response.data["message"] == "자격 인증데이터(authentication credentials)가 제공되지 않았습니다."

    def test_user_detail_put_success(self, new_users):
        access_token = self.obtain_token(new_users)
        self.authenticate_with_token(access_token)
        response = self.client.put(
            self.url,
            data={"nickname": "test_nickname"},
            format="json",
        )

        assert response.status_code == 200
        assert response.data["data"] == {
            "id": 11,
            "email": "test11@test.com",
            "nickname": "test_nickname",
        }

    def test_user_detail_put_fail_not_authenticated(self):
        response = self.client.put(
            self.url,
            data={"nickname": "test_nickname"},
            format="json",
        )

        assert response.status_code == 401
        assert response.data["message"] == "자격 인증데이터(authentication credentials)가 제공되지 않았습니다."

    def test_user_detail_delete_success(self, new_users):
        access_token = self.obtain_token(new_users)
        self.authenticate_with_token(access_token)
        response = self.client.delete(self.url)

        assert response.status_code == 204

    def test_user_detail_delete_fail_not_authenticated(self):
        response = self.client.delete(self.url)

        assert response.status_code == 401
        assert response.data["message"] == "자격 인증데이터(authentication credentials)가 제공되지 않았습니다."
