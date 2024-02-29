from django.urls import reverse

from tests.utils import IsAuthenticateTestCase


class TestReviewPhotoBoothLocationSearch(IsAuthenticateTestCase):
    url = reverse("api-reviews:review-photo-booth-location-search")

    def test_review_photo_booth_location_search_get_success(self, valid_user, photo_booth):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            self.url,
            data={"limit": 1, "offset": 0, "photo_booth_name": photo_booth.name},
        )

        assert response.status_code == 200
        assert response.data["data"]["count"] == 1
        assert response.data["data"]["results"][0]["id"] == str(photo_booth.id)
        assert response.data["data"]["results"][0]["name"] == photo_booth.name

    def test_review_photo_booth_location_search_get_fail_not_authenticated(self, photo_booth):
        response = self.client.get(
            self.url,
            data={"limit": 1, "offset": 0, "photo_booth_name": photo_booth.name},
        )

        assert response.status_code == 401
        assert response.data["code"] == "not_authenticated"
        assert response.data["message"] == "Authentication credentials were not provided."

    def test_review_photo_booth_location_search_get_fail_photo_booth_name_required(self, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            self.url,
            data={"limit": 1, "offset": 0},
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"photo_booth_name": ["This field is required."]}

    def test_review_photo_booth_location_search_get_fail_limit_min_value(self, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(self.url, data={"limit": -1, "photo_booth_name": "test"})

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"limit": ["Ensure this value is greater than or equal to 1."]}

    def test_review_photo_booth_location_search_get_fail_limit_max_value(self, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(self.url, data={"limit": 51, "photo_booth_name": "test"})

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"limit": ["Ensure this value is less than or equal to 50."]}

    def test_review_photo_booth_location_search_get_fail_offset_min_value(self, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(self.url, data={"offset": -1, "photo_booth_name": "test"})

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"offset": ["Ensure this value is greater than or equal to 0."]}

    def test_review_photo_booth_location_search_get_fail_limit_invalid_format(self, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(self.url, data={"limit": "invalid", "photo_booth_name": "test"})

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"limit": ["A valid integer is required."]}

    def test_review_photo_booth_location_search_get_fail_offset_invalid_format(self, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(self.url, data={"offset": "invalid", "photo_booth_name": "test"})

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"offset": ["A valid integer is required."]}
