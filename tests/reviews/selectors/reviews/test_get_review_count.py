import pytest

from dump_in.reviews.selectors.reviews import ReviewSelector

pytestmark = pytest.mark.django_db


class TestGetReviewCount:
    def setup_method(self):
        self.review_selector = ReviewSelector()

    def test_get_review_count_success_all(self, valid_review_list):
        review_count = self.review_selector.get_review_count({})

        assert review_count == len(valid_review_list)

    def test_get_review_count_success_with_frame_color(self, valid_review_list_frame_color):
        frame_color = valid_review_list_frame_color[0].frame_color

        review_count = self.review_selector.get_review_count({"frame_color": frame_color})

        assert review_count == len(valid_review_list_frame_color)

    def test_get_review_count_success_with_participants(self, valid_review_list_participants):
        participants = valid_review_list_participants[0].participants

        review_count = self.review_selector.get_review_count({"participants": str(participants)})

        assert review_count == len(valid_review_list_participants)

    def test_get_review_count_success_with_camera_shot(self, valid_review_list_camera_shot):
        camera_shot = valid_review_list_camera_shot[0].camera_shot

        review_count = self.review_selector.get_review_count({"camera_shot": camera_shot})

        assert review_count == len(valid_review_list_camera_shot)

    def test_get_review_count_success_with_concept(self, valid_review_list_concept):
        concept = valid_review_list_concept[0].concept.all()[0]

        review_count = self.review_selector.get_review_count({"concept": str(concept.id)})

        assert review_count == len(valid_review_list_concept)

    def test_get_review_count_success_with_photo_booth_location(self, valid_review_list_photo_booth_location):
        photo_booth_location = valid_review_list_photo_booth_location[0].photo_booth.location

        review_count = self.review_selector.get_review_count({"photo_booth_location": photo_booth_location})

        assert review_count == len(valid_review_list_photo_booth_location)

    def test_get_review_count_fail_does_not_exist(self):
        review_count = self.review_selector.get_review_count({})

        assert review_count == 0

    def test_get_review_count_fail_deleted_review(self, deleted_review):
        review_count = self.review_selector.get_review_count({})

        assert review_count == 0

    def test_get_review_count_fail_private_review(self, private_review):
        review_count = self.review_selector.get_review_count({})

        assert review_count == 0
