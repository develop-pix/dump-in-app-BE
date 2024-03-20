from django.urls import reverse
from rest_framework.exceptions import ErrorDetail

from dump_in.reviews.enums import CameraShot, FrameColor
from tests.utils import IsAuthenticateTestCase


class TestReviewList(IsAuthenticateTestCase):
    url = reverse("api-reviews:review-list")

    def test_review_list_get_success_single_review(self, valid_review, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            self.url,
            data={"limit": 1, "offset": 0},
        )

        assert response.status_code == 200
        assert response.data["data"]["count"] == 1
        assert response.data["data"]["results"][0]["id"] == valid_review.id
        assert response.data["data"]["results"][0]["main_thumbnail_image_url"] == valid_review.main_thumbnail_image_url
        assert response.data["data"]["results"][0]["photo_booth_name"] == valid_review.photo_booth.name

    def test_review_list_get_success_pagination(self, valid_review_list, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            self.url,
            data={"limit": 5, "offset": 0},
        )

        assert response.status_code == 200
        assert response.data["data"]["count"] == 10
        assert len(response.data["data"]["results"]) == 5

    def test_review_list_get_success_with_filter(self, valid_review_list_frame_color, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            self.url,
            data={"limit": 1, "offset": 0, "frame_color": valid_review_list_frame_color[0].frame_color},
        )

        assert response.status_code == 200
        assert response.data["data"]["count"] == len(valid_review_list_frame_color)

    def test_review_list_get_success_with_anonymous_user(self, valid_review_list):
        response = self.client.get(
            self.url,
            data={"limit": 1, "offset": 0},
        )

        assert response.status_code == 200
        assert response.data["data"]["count"] == len(valid_review_list)

    def test_review_list_get_fail_photo_booth_location_invalid_choice(self, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            self.url,
            data={"photo_booth_location": "test"},
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"photo_booth_location": ['"test" is not a valid choice.']}

    def test_review_list_get_fail_frame_color_invalid_choice(self, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            self.url,
            data={"frame_color": "test"},
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"frame_color": ['"test" is not a valid choice.']}

    def test_review_list_get_fail_participants_invalid_choice(self, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            self.url,
            data={"participants": "test"},
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"participants": ['"test" is not a valid choice.']}

    def test_review_list_get_fail_camera_shot_invalid_choice(self, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            self.url,
            data={"camera_shot": "test"},
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"camera_shot": ['"test" is not a valid choice.']}

    def test_review_list_get_fail_concept_invalid_choice(self, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            self.url,
            data={"concept": "test"},
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"concept": ['"test" is not a valid choice.']}

    def test_review_list_get_fail_photo_booth_location_duplicate(self, valid_review_list, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            self.url,
            data={
                "photo_booth_location": [valid_review_list[0].photo_booth.location, valid_review_list[0].photo_booth.location],
            },
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {
            "photo_booth_location": [ErrorDetail(string="This list may not contain the same item twice.", code="duplicate_values")]
        }

    def test_review_list_get_fail_frame_color_duplicate(self, valid_review_list, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            self.url,
            data={
                "frame_color": [valid_review_list[0].frame_color, valid_review_list[0].frame_color],
            },
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {
            "frame_color": [ErrorDetail(string="This list may not contain the same item twice.", code="duplicate_values")]
        }

    def test_review_list_get_fail_participants_duplicate(self, valid_review_list, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            self.url,
            data={
                "participants": [valid_review_list[0].participants, valid_review_list[0].participants],
            },
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {
            "participants": [ErrorDetail(string="This list may not contain the same item twice.", code="duplicate_values")]
        }

    def test_review_list_get_fail_camera_shot_duplicate(self, valid_review_list, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            self.url,
            data={
                "camera_shot": [valid_review_list[0].camera_shot, valid_review_list[0].camera_shot],
            },
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {
            "camera_shot": [ErrorDetail(string="This list may not contain the same item twice.", code="duplicate_values")]
        }

    def test_review_list_get_fail_concept_duplicate(self, valid_review_list, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            self.url,
            data={
                "concept": ["일상", "일상"],
            },
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {
            "concept": [ErrorDetail(string="This list may not contain the same item twice.", code="duplicate_values")]
        }

    def test_review_list_post_success(self, valid_user, photo_booth, concept):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.post(
            self.url,
            data={
                "main_thumbnail_image_url": "https://test.com",
                "image_urls": ["https://test.com"],
                "content": "string",
                "photo_booth_id": photo_booth.id,
                "date": "2023-01-01",
                "frame_color": FrameColor.BLACK.value,
                "participants": 1,
                "camera_shot": CameraShot.CLOSEUP.value,
                "concept": [concept.name],
                "goods_amount": True,
                "curl_amount": True,
                "is_public": True,
            },
            format="json",
        )

        assert response.status_code == 201
        assert response.data["data"]["id"] is not None
        assert response.data["data"]["main_thumbnail_image_url"] == "https://test.com"
        assert response.data["data"]["photo_booth_name"] == photo_booth.name

    def test_review_list_post_fail_not_authenticated(self):
        response = self.client.post(self.url)

        assert response.status_code == 401
        assert response.data["code"] == "not_authenticated"
        assert response.data["message"] == "Authentication credentials were not provided."

    def test_review_list_post_fail_date_validate(self, valid_user, photo_booth, concept):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.post(
            self.url,
            data={
                "main_thumbnail_image_url": "https://test.com",
                "image_urls": ["https://test.com"],
                "content": "string",
                "photo_booth_id": photo_booth.id,
                "date": "2030-01-01",
                "frame_color": FrameColor.BLACK.value,
                "participants": 1,
                "camera_shot": CameraShot.CLOSEUP.value,
                "concept": [concept.name],
                "goods_amount": True,
                "curl_amount": True,
                "is_public": True,
            },
            format="json",
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"

    def test_review_detail_put_fail_concept_duplicate(self, valid_user, photo_booth, concept):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.post(
            self.url,
            data={
                "main_thumbnail_image_url": "https://test.com",
                "image_urls": ["https://test.com"],
                "content": "string",
                "photo_booth_id": photo_booth.id,
                "date": "2023-01-01",
                "frame_color": FrameColor.BLACK.value,
                "participants": 1,
                "camera_shot": CameraShot.CLOSEUP.value,
                "concept": [concept.name, concept.name],
                "goods_amount": True,
                "curl_amount": True,
                "is_public": True,
            },
            format="json",
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {
            "concept": [ErrorDetail(string="This list may not contain the same item twice.", code="duplicate_values")]
        }

    def test_review_list_post_fail_frame_color_invalid_choice(self, valid_user, photo_booth, concept):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.post(
            self.url,
            data={
                "main_thumbnail_image_url": "https://test.com",
                "image_urls": ["https://test.com"],
                "content": "string",
                "photo_booth_id": photo_booth.id,
                "date": "2023-01-01",
                "frame_color": "test",
                "participants": 1,
                "camera_shot": CameraShot.CLOSEUP.value,
                "concept": [concept.name],
                "goods_amount": True,
                "curl_amount": True,
                "is_public": True,
            },
            format="json",
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"frame_color": ['"test" is not a valid choice.']}

    def test_review_list_post_fail_camera_shot_invalid_choice(self, valid_user, photo_booth, concept):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.post(
            self.url,
            data={
                "main_thumbnail_image_url": "https://test.com",
                "image_urls": ["https://test.com"],
                "content": "string",
                "photo_booth_id": photo_booth.id,
                "date": "2023-01-01",
                "frame_color": FrameColor.BLACK.value,
                "participants": 1,
                "camera_shot": "test",
                "concept": [concept.name],
                "goods_amount": True,
                "curl_amount": True,
                "is_public": True,
            },
            format="json",
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"camera_shot": ['"test" is not a valid choice.']}

    def test_review_list_post_fail_concept_invalid_choices(self, valid_user, photo_booth, concept):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.post(
            self.url,
            data={
                "main_thumbnail_image_url": "https://test.com",
                "image_urls": ["https://test.com"],
                "content": "string",
                "photo_booth_id": photo_booth.id,
                "date": "2023-01-01",
                "frame_color": FrameColor.BLACK.value,
                "participants": 1,
                "camera_shot": CameraShot.CLOSEUP.value,
                "concept": ["test"],
                "goods_amount": True,
                "curl_amount": True,
                "is_public": True,
            },
            format="json",
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"concept": [ErrorDetail(string='"test" is not a valid choice.', code="invalid_choice")]}
