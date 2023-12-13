import pytest

from dump_in.reviews.selectors.reviews import ReviewSelector

pytestmark = pytest.mark.django_db


class TestGetReviewById:
    def setup_method(self):
        self.review_selector = ReviewSelector()

    def test_get_review_by_id_success(self, valid_review):
        review = self.review_selector.get_review_by_id(valid_review.id)

        assert review == valid_review

    def test_get_review_by_id_fail_does_not_exist(self):
        review = self.review_selector.get_review_by_id(999)

        assert review is None

    def test_get_review_by_id_fail_deleted_review(self, deleted_review):
        review = self.review_selector.get_review_by_id(deleted_review.id)

        assert review is None
