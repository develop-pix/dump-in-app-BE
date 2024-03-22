import pytest

from dump_in.reviews.selectors.reviews import ReviewSelector

pytestmark = pytest.mark.django_db


class TestGetReviewByIdAndUserId:
    def setup_method(self):
        self.review_selector = ReviewSelector()

    def test_get_review_by_id_and_user_id_success(self, valid_review):
        review = self.review_selector.get_review_by_id_and_user_id(valid_review.id, valid_review.user_id)

        assert review == valid_review

    def test_get_review_by_id_and_user_id_fail_does_not_exist(self):
        review = self.review_selector.get_review_by_id_and_user_id(999, 999)

        assert review is None
