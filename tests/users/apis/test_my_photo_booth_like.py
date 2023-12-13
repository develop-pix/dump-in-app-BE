import pytest
from django.urls import reverse

from tests.utils import IsAuthenticateTestCase

pytestmark = pytest.mark.django_db


class TestMyPhotoBoothLikeAPI(IsAuthenticateTestCase):
    url = reverse("api-users:user-photo-booth-like")

    def test_my_photo_booth_like_get_success_single_photo_booth(self, photo_booth, valid_user):
        photo_booth.user_photo_booth_like_logs.add(valid_user)

        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(self.url)

        assert response.status_code == 200
        assert response.data["data"].get("count") == 1

    def test_my_photo_booth_like_get_success_pagination(self, photo_booth_list, valid_user):
        for photo_booth in photo_booth_list:
            photo_booth.user_photo_booth_like_logs.add(valid_user)

        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(self.url)

        assert response.status_code == 200
        assert response.data["data"].get("count") == 100

    def test_my_photo_booth_like_get_not_authenticated(self):
        response = self.client.get(self.url)

        assert response.status_code == 401
        assert response.data["message"] == "Authentication credentials were not provided."
