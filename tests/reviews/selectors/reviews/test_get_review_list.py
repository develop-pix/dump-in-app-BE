import time

import pytest

from dump_in.reviews.models import Review
from dump_in.reviews.selectors.reviews import ReviewSelector

pytestmark = pytest.mark.django_db


class TestGetReviewList:
    def setup_method(self):
        self.review_selector = ReviewSelector()

    def test_get_review_list_success_all(self, valid_review_list):
        review_list = self.review_selector.get_review_list({})

        assert review_list.count() == len(valid_review_list)

    def test_get_review_list_success_with_frame_color(self, valid_review_list_frame_color):
        frame_color = valid_review_list_frame_color[0].frame_color

        review_list = self.review_selector.get_review_list({"frame_color": frame_color})

        assert review_list.count() == len(valid_review_list_frame_color)

    def test_get_review_list_success_with_participants(self, valid_review_list_participants):
        participants = valid_review_list_participants[0].participants

        review_list = self.review_selector.get_review_list({"participants": str(participants)})

        assert review_list.count() == len(valid_review_list_participants)

    def test_get_review_list_success_with_camera_shot(self, valid_review_list_camera_shot):
        camera_shot = valid_review_list_camera_shot[0].camera_shot

        review_list = self.review_selector.get_review_list({"camera_shot": camera_shot})

        assert review_list.count() == len(valid_review_list_camera_shot)

    def test_get_review_list_success_with_concept(self, valid_review_list_concept):
        concept = valid_review_list_concept[0].concept.all()[0]

        review_list = self.review_selector.get_review_list({"concept": str(concept.id)})

        assert review_list.count() == len(valid_review_list_concept)

    def test_get_review_list_success_with_photo_booth_location(self, valid_review_list_photo_booth_location):
        photo_booth_location = valid_review_list_photo_booth_location[0].photo_booth.location

        review_list = self.review_selector.get_review_list({"photo_booth_location": photo_booth_location})

        assert review_list.count() == len(valid_review_list_photo_booth_location)

    def test_get_review_list_fail_does_not_exist(self):
        review_list = self.review_selector.get_review_list({})

        assert list(review_list) == []

    def test_get_review_list_fail_deleted_review(self, deleted_review):
        review_list = self.review_selector.get_review_list({})

        assert list(review_list) == []

    def test_get_review_list_fail_private_review(self, private_review):
        review_list = self.review_selector.get_review_list({})

        assert list(review_list) == []

    def test_get_review_list_select_related_performance(self, valid_review_list):
        start_time = time.time()

        review_list = Review.objects.filter(is_deleted=False, is_public=True)

        for review in review_list:
            review.photo_booth

        end_time = time.time()
        time_with_filter = end_time - start_time

        start_time = time.time()

        review_list = self.review_selector.get_review_list({})

        for review in review_list:
            review.photo_booth

        end_time = time.time()
        time_with_select_related = end_time - start_time

        assert time_with_filter > time_with_select_related
