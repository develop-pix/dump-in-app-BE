import pytest

from dump_in.reviews.selectors.reviews import ReviewSelector

pytestmark = pytest.mark.django_db


class TestGetReviewList:
    def setup_method(self):
        self.review_selector = ReviewSelector()

    def test_get_review_list_order_by_created_at_desc_success_single_review(self, valid_review):
        review_list = self.review_selector.get_review_list_order_by_created_at_desc({})

        assert review_list.first() == valid_review

    def test_get_review_list_order_by_created_at_desc_success_multiple_review(self, valid_review_list):
        review_list = self.review_selector.get_review_list_order_by_created_at_desc({})

        assert review_list.count() == len(valid_review_list)

    def test_get_review_list_order_by_created_at_desc_success_with_frame_color(self, valid_review_list_frame_color):
        frame_color = [valid_review_list_frame_color[0].frame_color]

        review_list = self.review_selector.get_review_list_order_by_created_at_desc({"frame_color": frame_color})

        assert review_list.count() == len(valid_review_list_frame_color)

    def test_get_review_list_order_by_created_at_desc_success_with_participants(self, valid_review_list_participants):
        participants = valid_review_list_participants[0].participants

        review_list = self.review_selector.get_review_list_order_by_created_at_desc({"participants": str(participants)})

        assert review_list.count() == len(valid_review_list_participants)

    def test_get_review_list_order_by_created_at_desc_success_with_camera_shot(self, valid_review_list_camera_shot):
        camera_shot = [valid_review_list_camera_shot[0].camera_shot]

        review_list = self.review_selector.get_review_list_order_by_created_at_desc({"camera_shot": camera_shot})

        assert review_list.count() == len(valid_review_list_camera_shot)

    def test_get_review_list_order_by_created_at_desc_success_with_concept(self, valid_review_list_concept):
        concept_name = [valid_review_list_concept[0].concept.all()[0].name]

        review_list = self.review_selector.get_review_list_order_by_created_at_desc({"concept": concept_name})

        assert review_list.count() == len(valid_review_list_concept)

    def test_get_review_list_order_by_created_at_desc_success_with_photo_booth_location(self, valid_review_list_photo_booth_location):
        photo_booth_location = [valid_review_list_photo_booth_location[0].photo_booth.location]

        review_list = self.review_selector.get_review_list_order_by_created_at_desc({"photo_booth_location": photo_booth_location})

        assert review_list.count() == len(valid_review_list_photo_booth_location)

    def test_get_review_list_order_by_created_at_desc_fail_invalid_frame_color(self, valid_review_list_frame_color):
        review_list = self.review_selector.get_review_list_order_by_created_at_desc({"frame_color": ["invalid"]})

        assert review_list.count() == 0

    def test_get_review_list_order_by_created_at_desc_fail_invalid_participants(self, valid_review_list_participants):
        review_list = self.review_selector.get_review_list_order_by_created_at_desc({"participants": "9999"})

        assert review_list.count() == 0

    def test_get_review_list_order_by_created_at_desc_fail_invalid_camera_shot(self, valid_review_list_camera_shot):
        review_list = self.review_selector.get_review_list_order_by_created_at_desc({"camera_shot": ["invalid"]})

        assert review_list.count() == 0

    def test_get_review_list_order_by_created_at_desc_fail_invalid_concept(self, valid_review_list_concept):
        review_list = self.review_selector.get_review_list_order_by_created_at_desc({"concept": ["9999"]})

        assert review_list.count() == 0

    def test_get_review_list_order_by_created_at_desc_fail_invalid_photo_booth_location(self, valid_review_list_photo_booth_location):
        review_list = self.review_selector.get_review_list_order_by_created_at_desc({"photo_booth_location": ["invalid"]})

        assert review_list.count() == 0

    def test_get_review_list_order_by_created_at_desc_fail_does_not_exist(self):
        review_list = self.review_selector.get_review_list_order_by_created_at_desc({})

        assert review_list.count() == 0

    def test_get_review_list_order_by_created_at_desc_fail_deleted_review(self, deleted_review):
        review_list = self.review_selector.get_review_list_order_by_created_at_desc({})

        assert review_list.count() == 0

    def test_get_review_list_order_by_created_at_desc_fail_private_review(self, private_review):
        review_list = self.review_selector.get_review_list_order_by_created_at_desc({})

        assert review_list.count() == 0
