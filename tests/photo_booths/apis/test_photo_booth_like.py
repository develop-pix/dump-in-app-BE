import pytest
from django.urls import reverse

from tests.utils import IsAuthenticateTestCase

pytestmark = pytest.mark.django_db


class TestPhotoBoothLikeAPI(IsAuthenticateTestCase):
    def test_photo_booth_like_post_success(self, photo_booth, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.post(reverse("api-photo-booths:photo-booth-like", kwargs={"photo_booth_id": photo_booth.id}))

        assert response.status_code == 200
        assert response.data["data"] is not None

    def test_photo_booth_like_post_success_already_liked(self, photo_booth, valid_user):
        photo_booth.user_photo_booth_like_logs.add(valid_user)

        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.post(reverse("api-photo-booths:photo-booth-like", kwargs={"photo_booth_id": photo_booth.id}))

        assert response.status_code == 200
        assert response.data["data"] is not None

    def test_photo_booth_like_post_fail_not_authenticated(self, photo_booth):
        response = self.client.post(reverse("api-photo-booths:photo-booth-like", kwargs={"photo_booth_id": photo_booth.id}))

        assert response.status_code == 401
        assert response.data["message"] == "Authentication credentials were not provided."
