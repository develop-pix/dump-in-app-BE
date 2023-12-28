import pytest
from django.urls import reverse

from tests.utils import IsAuthenticateTestCase

pytestmark = pytest.mark.django_db


class TestMyPhotoBoothLike(IsAuthenticateTestCase):
    url = reverse("api-users:user-photo-booth-like-list")

    def test_my_photo_booth_like_get_success_single_photo_booth(self, photo_booth, valid_user):
        photo_booth.user_photo_booth_like_logs.add(valid_user)

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
        assert response.data["data"]["count"] == 1
        assert response.data["data"]["results"][0]["id"] == photo_booth.id
        assert response.data["data"]["results"][0]["photo_booth_name"] == photo_booth.name
        assert response.data["data"]["results"][0]["photo_booth_brand_name"] == photo_booth.photo_booth_brand.name
        assert response.data["data"]["results"][0]["photo_booth_brand_logo_image_url"] == photo_booth.photo_booth_brand.logo_image_url
        assert response.data["data"]["results"][0]["hashtag"][0]["id"] == photo_booth.photo_booth_brand.hashtag.all()[0].id
        assert response.data["data"]["results"][0]["hashtag"][0]["name"] == photo_booth.photo_booth_brand.hashtag.all()[0].name
        assert response.data["data"]["results"][0]["is_liked"] == True

    def test_my_photo_booth_like_get_success_pagination(self, photo_booth_list, valid_user):
        for photo_booth in photo_booth_list:
            photo_booth.user_photo_booth_like_logs.add(valid_user)

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
        assert response.data["data"]["count"] == 100
        assert len(response.data["data"]["results"]) == 10

    def test_my_photo_booth_like_get_not_authenticated(self):
        response = self.client.get(self.url)

        assert response.status_code == 401
        assert response.data["code"] == "not_authenticated"
        assert response.data["message"] == "Authentication credentials were not provided."

    def test_my_photo_booth_like_get_fail_limit_min_value(self, photo_booth, valid_user):
        photo_booth.user_photo_booth_like_logs.add(valid_user)

        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            path=self.url,
            data={
                "limit": 0,
                "offset": 0,
            },
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"limit": ["Ensure this value is greater than or equal to 1."]}

    def test_my_photo_booth_like_get_fail_limit_max_value(self, photo_booth, valid_user):
        photo_booth.user_photo_booth_like_logs.add(valid_user)

        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            path=self.url,
            data={
                "limit": 51,
                "offset": 0,
            },
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"limit": ["Ensure this value is less than or equal to 50."]}

    def test_my_photo_booth_like_get_fail_offset_min_value(self, photo_booth, valid_user):
        photo_booth.user_photo_booth_like_logs.add(valid_user)

        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            path=self.url,
            data={
                "limit": 1,
                "offset": -1,
            },
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"offset": ["Ensure this value is greater than or equal to 0."]}

    def test_my_photo_booth_like_get_fail_limit_invalid_format(self, photo_booth, valid_user):
        photo_booth.user_photo_booth_like_logs.add(valid_user)

        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            path=self.url,
            data={
                "limit": "invalid",
                "offset": 0,
            },
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"limit": ["A valid integer is required."]}

    def test_my_photo_booth_like_get_fail_offset_invalid_format(self, photo_booth, valid_user):
        photo_booth.user_photo_booth_like_logs.add(valid_user)

        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            path=self.url,
            data={
                "limit": 1,
                "offset": "invalid",
            },
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"offset": ["A valid integer is required."]}
