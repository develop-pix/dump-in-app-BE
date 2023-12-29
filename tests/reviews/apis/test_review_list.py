from django.urls import reverse
from rest_framework.exceptions import ErrorDetail

from dump_in.reviews.enums import CameraShot, FrameColor
from dump_in.reviews.models import Review
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

    def test_review_list_get_fail_not_authenticated(self):
        response = self.client.get(self.url)

        assert response.status_code == 401
        assert response.data["code"] == "not_authenticated"
        assert response.data["message"] == "Authentication credentials were not provided."

    def test_review_list_get_fail_photo_booth_location_choice(self, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            self.url,
            data={"photo_booth_location": "test"},
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"photo_booth_location": ['"test" is not a valid choice.']}

    def test_review_list_get_fail_frame_color_choice(self, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            self.url,
            data={"frame_color": "test"},
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"frame_color": ['"test" is not a valid choice.']}

    def test_review_list_get_fail_participants_choice(self, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            self.url,
            data={"participants": "test"},
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"participants": ['"test" is not a valid choice.']}

    def test_review_list_get_fail_camera_shot_choice(self, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            self.url,
            data={"camera_shot": "test"},
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"camera_shot": ['"test" is not a valid choice.']}

    def test_review_list_get_fail_concept_choice(self, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(
            self.url,
            data={"concept": "test"},
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"concept": ['"test" is not a valid choice.']}

    def test_review_list_get_fail_limit_min_value(self, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(self.url, data={"limit": -1})

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"limit": ["Ensure this value is greater than or equal to 1."]}

    def test_review_list_get_fail_limit_max_value(self, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(self.url, data={"limit": 51})

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"limit": ["Ensure this value is less than or equal to 50."]}

    def test_review_list_get_fail_offset_min_value(self, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(self.url, data={"offset": -1})

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"offset": ["Ensure this value is greater than or equal to 0."]}

    def test_review_list_get_fail_limit_invalid_format(self, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(self.url, data={"limit": "invalid"})

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"limit": ["A valid integer is required."]}

    def test_review_list_get_fail_offset_invalid_format(self, valid_user):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(self.url, data={"offset": "invalid"})

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"offset": ["A valid integer is required."]}

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

    def test_review_list_post_success_goods_amout_allow_null(self, valid_user, photo_booth, concept):
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
                "curl_amount": True,
                "goods_amount": None,
                "is_public": True,
            },
            format="json",
        )

        assert response.status_code == 201
        assert response.data["data"]["id"] is not None
        assert response.data["data"]["main_thumbnail_image_url"] == "https://test.com"
        assert response.data["data"]["photo_booth_name"] == photo_booth.name
        Review.objects.get(id=response.data["data"]["id"]).goods_amount is None

    def test_review_list_post_success_curl_amout_allow_null(self, valid_user, photo_booth, concept):
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
                "curl_amount": None,
                "goods_amount": True,
                "is_public": True,
            },
            format="json",
        )

        assert response.status_code == 201
        assert response.data["data"]["id"] is not None
        assert response.data["data"]["main_thumbnail_image_url"] == "https://test.com"
        assert response.data["data"]["photo_booth_name"] == photo_booth.name
        Review.objects.get(id=response.data["data"]["id"]).curl_amount is None

    def test_review_list_post_fail_not_authenticated(self):
        response = self.client.post(self.url)

        assert response.status_code == 401
        assert response.data["code"] == "not_authenticated"
        assert response.data["message"] == "Authentication credentials were not provided."

    def test_review_list_post_fail_main_thumbnail_image_url_required(self, valid_user, photo_booth, concept):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.post(
            self.url,
            data={
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

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"main_thumbnail_image_url": ["This field is required."]}

    def test_review_list_post_fail_content_required(self, valid_user, photo_booth, concept):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.post(
            self.url,
            data={
                "main_thumbnail_image_url": "https://test.com",
                "image_urls": ["https://test.com"],
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

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"content": ["This field is required."]}

    def test_review_list_post_fail_photo_booth_id_required(self, valid_user, photo_booth, concept):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.post(
            self.url,
            data={
                "main_thumbnail_image_url": "https://test.com",
                "image_urls": ["https://test.com"],
                "content": "string",
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

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"photo_booth_id": ["This field is required."]}

    def test_review_list_post_fail_date_required(self, valid_user, photo_booth, concept):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.post(
            self.url,
            data={
                "main_thumbnail_image_url": "https://test.com",
                "image_urls": ["https://test.com"],
                "content": "string",
                "photo_booth_id": photo_booth.id,
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
        assert response.data["message"] == {"date": ["This field is required."]}

    def test_review_list_post_fail_frame_color_required(self, valid_user, photo_booth, concept):
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
        assert response.data["message"] == {"frame_color": ["This field is required."]}

    def test_review_list_post_fail_participants_required(self, valid_user, photo_booth, concept):
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
        assert response.data["message"] == {"participants": ["This field is required."]}

    def test_review_list_post_fail_camera_shot_required(self, valid_user, photo_booth, concept):
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
                "concept": [concept.name],
                "goods_amount": True,
                "curl_amount": True,
                "is_public": True,
            },
            format="json",
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"camera_shot": ["This field is required."]}

    def test_review_list_post_fail_concept_required(self, valid_user, photo_booth, concept):
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
                "goods_amount": True,
                "curl_amount": True,
                "is_public": True,
            },
            format="json",
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"concept": ["This field is required."]}

    def test_review_list_post_fail_is_public_required(self, valid_user, photo_booth, concept):
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
            },
            format="json",
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"is_public": ["This field is required."]}

    def test_review_list_post_fail_main_thumbnail_image_url_invalid_format(self, valid_user, photo_booth, concept):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.post(
            self.url,
            data={
                "main_thumbnail_image_url": "test",
                "image_urls": ["https://test.com"],
                "content": "string",
                "photo_booth_id": photo_booth.id,
                "date": "2022-01-01",
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
        assert response.data["message"] == {"main_thumbnail_image_url": ["Enter a valid URL."]}

    def test_review_list_post_fail_image_urls_child_invalid_format(self, valid_user, photo_booth, concept):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.post(
            self.url,
            data={
                "main_thumbnail_image_url": "https://test.com",
                "image_urls": ["test"],
                "content": "string",
                "photo_booth_id": photo_booth.id,
                "date": "2022-01-01",
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
        assert response.data["message"] == {"image_urls": {0: [ErrorDetail(string="Enter a valid URL.", code="invalid")]}}

    def test_review_list_post_fail_image_urls_invalid_format(self, valid_user, photo_booth, concept):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.post(
            self.url,
            data={
                "main_thumbnail_image_url": "https://test.com",
                "image_urls": "test",
                "content": "string",
                "photo_booth_id": photo_booth.id,
                "date": "2022-01-01",
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
        assert response.data["message"] == {"image_urls": ['Expected a list of items but got type "str".']}

    def test_review_list_post_fail_content_invalid_format(self, valid_user, photo_booth, concept):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.post(
            self.url,
            data={
                "main_thumbnail_image_url": "https://test.com",
                "image_urls": ["https://test.com"],
                "content": [1234],
                "photo_booth_id": photo_booth.id,
                "date": "2022-01-01",
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
        assert response.data["message"] == {"content": ["Not a valid string."]}

    def test_review_list_post_fail_photo_booth_id_invalid_format(self, valid_user, photo_booth, concept):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.post(
            self.url,
            data={
                "main_thumbnail_image_url": "https://test.com",
                "image_urls": ["https://test.com"],
                "content": "string",
                "photo_booth_id": "test",
                "date": "2022-01-01",
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
        assert response.data["message"] == {"photo_booth_id": ["Must be a valid UUID."]}

    def test_review_list_post_fail_date_invalid_format(self, valid_user, photo_booth, concept):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.post(
            self.url,
            data={
                "main_thumbnail_image_url": "https://test.com",
                "image_urls": ["https://test.com"],
                "content": "string",
                "photo_booth_id": photo_booth.id,
                "date": "test",
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
        assert response.data["message"] == {"date": ["Date has wrong format. Use one of these formats instead: YYYY-MM-DD."]}

    def test_review_list_post_fail_participants_invalid_format(self, valid_user, photo_booth, concept):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.post(
            self.url,
            data={
                "main_thumbnail_image_url": "https://test.com",
                "image_urls": ["https://test.com"],
                "content": "string",
                "photo_booth_id": photo_booth.id,
                "date": "2022-01-01",
                "frame_color": FrameColor.BLACK.value,
                "participants": "test",
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
        assert response.data["message"] == {"participants": ["A valid integer is required."]}

    def test_review_list_post_fail_goods_amount_invalid_format(self, valid_user, photo_booth, concept):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.post(
            self.url,
            data={
                "main_thumbnail_image_url": "https://test.com",
                "image_urls": ["https://test.com"],
                "content": "string",
                "photo_booth_id": photo_booth.id,
                "date": "2022-01-01",
                "frame_color": FrameColor.BLACK.value,
                "participants": 1,
                "camera_shot": CameraShot.CLOSEUP.value,
                "concept": [concept.name],
                "goods_amount": "test",
                "curl_amount": True,
                "is_public": True,
            },
            format="json",
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"goods_amount": ["Must be a valid boolean."]}

    def test_review_list_post_fail_curl_amount_invalid_format(self, valid_user, photo_booth, concept):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.post(
            self.url,
            data={
                "main_thumbnail_image_url": "https://test.com",
                "image_urls": ["https://test.com"],
                "content": "string",
                "photo_booth_id": photo_booth.id,
                "date": "2022-01-01",
                "frame_color": FrameColor.BLACK.value,
                "participants": 1,
                "camera_shot": CameraShot.CLOSEUP.value,
                "concept": [concept.name],
                "goods_amount": True,
                "curl_amount": "test",
                "is_public": True,
            },
            format="json",
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"curl_amount": ["Must be a valid boolean."]}

    def test_review_list_post_fail_is_public_invalid_format(self, valid_user, photo_booth, concept):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        response = self.client.post(
            self.url,
            data={
                "main_thumbnail_image_url": "https://test.com",
                "image_urls": ["https://test.com"],
                "content": "string",
                "photo_booth_id": photo_booth.id,
                "date": "2022-01-01",
                "frame_color": FrameColor.BLACK.value,
                "participants": 1,
                "camera_shot": CameraShot.CLOSEUP.value,
                "concept": [concept.name],
                "goods_amount": True,
                "curl_amount": True,
                "is_public": "test",
            },
            format="json",
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"is_public": ["Must be a valid boolean."]}

    def test_review_post_put_fail_concept_allow_empty(self, valid_user, photo_booth, concept):
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
                "concept": [],
                "goods_amount": True,
                "curl_amount": True,
                "is_public": True,
            },
            format="json",
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"concept": ["This selection may not be empty."]}

    def test_review_list_post_fail_image_urls_max_value(self, valid_user, photo_booth, concept):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        image_urls = ["https://test.com"] * 6
        response = self.client.post(
            self.url,
            data={
                "main_thumbnail_image_url": "https://test.com",
                "image_urls": image_urls,
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

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"image_urls": ["Ensure this field has no more than 4 elements."]}

    def test_review_list_post_fail_content_max_value(self, valid_user, photo_booth, concept):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        content = "string" * 1000
        response = self.client.post(
            self.url,
            data={
                "main_thumbnail_image_url": "https://test.com",
                "image_urls": ["https://test.com"],
                "content": content,
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

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"content": ["Ensure this field has no more than 100 characters."]}

    def test_review_list_post_fail_date_max_value(self, valid_user, photo_booth, concept):
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

    def test_review_list_post_fail_participants_min_value(self, valid_user, photo_booth, concept):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        participants = 0
        response = self.client.post(
            self.url,
            data={
                "main_thumbnail_image_url": "https://test.com",
                "image_urls": ["https://test.com"],
                "content": "string",
                "photo_booth_id": photo_booth.id,
                "date": "2023-01-01",
                "frame_color": FrameColor.BLACK.value,
                "participants": participants,
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
        assert response.data["message"] == {"participants": ["Ensure this value is greater than or equal to 1."]}

    def test_review_list_post_fail_participants_max_value(self, valid_user, photo_booth, concept):
        access_token = self.obtain_token(valid_user)
        self.authenticate_with_token(access_token)
        participants = 100
        response = self.client.post(
            self.url,
            data={
                "main_thumbnail_image_url": "https://test.com",
                "image_urls": ["https://test.com"],
                "content": "string",
                "photo_booth_id": photo_booth.id,
                "date": "2023-01-01",
                "frame_color": FrameColor.BLACK.value,
                "participants": participants,
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
        assert response.data["message"] == {"participants": ["Ensure this value is less than or equal to 5."]}

    def test_review_list_post_fail_concept_max_choices(self, valid_user, photo_booth, concept):
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
                "concept": ["일상", "커플", "우정샷", "가족", "콜라보", "이달의 프레임"],
                "goods_amount": True,
                "curl_amount": True,
                "is_public": True,
            },
            format="json",
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {
            "concept": [ErrorDetail(string="Ensure this field has no more than 5 items.", code="max_choices")]
        }

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

    def test_review_list_post_fail_frame_color_choice(self, valid_user, photo_booth, concept):
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

    def test_review_list_post_fail_camera_shot_choice(self, valid_user, photo_booth, concept):
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

    def test_review_list_post_fail_concept_choices(self, valid_user, photo_booth, concept):
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
