import pytest

from dump_in.reviews.selectors.reviews import ReviewSelector

pytestmark = pytest.mark.django_db


class TestReviewSelector:
    def setup_method(self):
        self.review_selector = ReviewSelector()

    def test_get_review_with_review_images_and_hashtags_by_id_success(self, review):
        review = self.review_selector.get_review_with_review_images_and_hashtags_by_id(review.id)
        assert review is not None

    def test_get_review_with_review_images_and_hashtags_by_id_fail_does_not_exist(self):
        review_id = 1
        review = self.review_selector.get_review_with_review_images_and_hashtags_by_id(review_id)
        assert review is None

    def test_get_review_by_id_success(self, review):
        review = self.review_selector.get_review_by_id(review.id)
        assert review is not None

    def test_get_review_by_id_fail_does_not_exist(self):
        review_id = 1
        review = self.review_selector.get_review_by_id(review_id)
        assert review is None

    def test_get_public_review_by_id_success(self, review):
        review = self.review_selector.get_public_review_by_id(review.id)
        assert review is not None

    def test_get_public_review_by_id_fail_does_not_exist(self):
        review_id = 1
        review = self.review_selector.get_public_review_by_id(review_id)
        assert review is None

    def test_get_review_queryset_with_photo_booth_by_user_id_success(self, review):
        user = review.user
        review_queryset = self.review_selector.get_review_queryset_with_photo_booth_by_user_id(user)
        assert review_queryset.count() == 1

    def test_get_review_queryset_with_photo_booth_by_user_id_fail_does_not_exist(self, review, new_users):
        review_queryset = self.review_selector.get_review_queryset_with_photo_booth_by_user_id(new_users)
        assert review_queryset.count() == 0

    def test_get_review_queryset_by_user_like_success(self, review):
        user = review.user
        review.user_review_like_logs.add(user)
        review_queryset = self.review_selector.get_review_queryset_by_user_like(user)
        assert review_queryset.count() == 1

    def test_get_review_count_success_all(self, review_list):
        review_count = self.review_selector.get_review_count({})
        assert review_count == 7

    def test_get_review_count_success_with_frame_coloer(self, review_list):
        review_count = self.review_selector.get_review_count({"frame_color": "red"})
        assert review_count == 3

    def test_get_review_count_success_with_participants(self, review_list):
        review_count = self.review_selector.get_review_count({"participants": "1"})
        assert review_count == 3

    def test_get_review_count_success_with_camera_shot(self, review_list):
        review_count = self.review_selector.get_review_count({"camera_shot": "red1"})
        assert review_count == 3

    def test_get_review_count_success_with_hashtags(self, review_list):
        review_count = self.review_selector.get_review_count({"hashtags": "1"})
        assert review_count == 3

    def test_get_review_list_success_all(self, review_list):
        review_queryset = self.review_selector.get_review_list({})
        assert review_queryset.count() == 7

    def test_get_review_list_success_with_frame_coloer(self, review_list):
        review_queryset = self.review_selector.get_review_list({"frame_color": "red"})
        assert review_queryset.count() == 3

    def test_get_review_list_success_with_participants(self, review_list):
        review_queryset = self.review_selector.get_review_list({"participants": "1"})
        assert review_queryset.count() == 3

    def test_get_review_list_success_with_camera_shot(self, review_list):
        review_queryset = self.review_selector.get_review_list({"camera_shot": "red1"})
        assert review_queryset.count() == 3

    def test_get_review_list_success_with_hashtags(self, review_list):
        review_queryset = self.review_selector.get_review_list({"hashtags": "1"})
        assert review_queryset.count() == 3
