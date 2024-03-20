from django.urls import reverse
from rest_framework.exceptions import ErrorDetail

from tests.utils import IsAuthenticateTestCase


class TestReviewListCount(IsAuthenticateTestCase):
    url = reverse("api-reviews:review-list-count")

    def test_review_list_count_get_success(self, valid_review_list, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(self.url)

        assert response.status_code == 200
        assert response.data["data"]["count"] == 10

    def test_review_list_count_get_success_with_filter(self, valid_review_list_frame_color, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            self.url,
            data={"frame_color": valid_review_list_frame_color[0].frame_color},
        )

        assert response.status_code == 200
        assert response.data["data"]["count"] == len(valid_review_list_frame_color)

    def test_review_list_count_get_success_anonymous_user(self, valid_review_list, valid_user):
        response = self.client.get(self.url)

        assert response.status_code == 200
        assert response.data["data"]["count"] == 10

    def test_review_list_count_get_fail_photo_booth_location_duplicate(self, valid_review_list_photo_booth_location, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            self.url,
            data={"photo_booth_location": ["강남", "강남"]},
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {
            "photo_booth_location": [ErrorDetail(string="This list may not contain the same item twice.", code="duplicate_values")]
        }

    def test_review_list_count_get_fail_frame_color_duplicate(self, valid_review_list_frame_color, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            self.url,
            data={"frame_color": [valid_review_list_frame_color[0].frame_color, valid_review_list_frame_color[0].frame_color]},
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {
            "frame_color": [ErrorDetail(string="This list may not contain the same item twice.", code="duplicate_values")]
        }

    def test_review_list_count_get_fail_participants_duplicate(self, valid_review_list_participants, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            self.url,
            data={"participants": [valid_review_list_participants[0].participants, valid_review_list_participants[0].participants]},
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {
            "participants": [ErrorDetail(string="This list may not contain the same item twice.", code="duplicate_values")]
        }

    def test_review_list_count_get_fail_camera_shot_duplicate(self, valid_review_list_camera_shot, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            self.url,
            data={"camera_shot": [valid_review_list_camera_shot[0].camera_shot, valid_review_list_camera_shot[0].camera_shot]},
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {
            "camera_shot": [ErrorDetail(string="This list may not contain the same item twice.", code="duplicate_values")]
        }

    def test_review_list_count_get_fail_concept_duplicate(self, valid_review_list_concept, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            self.url,
            data={"concept": ["일상", "일상"]},
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {
            "concept": [ErrorDetail(string="This list may not contain the same item twice.", code="duplicate_values")]
        }

    def test_review_list_count_get_fail_photo_booth_location_invalid_choice(self, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            self.url,
            data={"photo_booth_location": "test"},
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"photo_booth_location": ['"test" is not a valid choice.']}

    def test_review_list_count_get_fail_frame_color_invalid_choice(self, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            self.url,
            data={"frame_color": "test"},
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"frame_color": ['"test" is not a valid choice.']}

    def test_review_list_count_get_fail_participants_invalid_choice(self, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            self.url,
            data={"participants": "test"},
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"participants": ['"test" is not a valid choice.']}

    def test_review_list_count_get_fail_camera_shot_invalid_choice(self, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            self.url,
            data={"camera_shot": "test"},
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"camera_shot": ['"test" is not a valid choice.']}

    def test_review_list_count_get_fail_concept_invalid_choice(self, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            self.url,
            data={"concept": "test"},
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"concept": ['"test" is not a valid choice.']}
