import pytest

from dump_in.reviews.selectors.reviews import ReviewSelector

pytestmark = pytest.mark.django_db


class TestGetPublicReviewById:
    def setup_method(self):
        self.review_selector = ReviewSelector()

    def test_get_public_review_by_id_success(self, valid_review):
        public_review = self.review_selector.get_public_review_by_id(valid_review.id)

        assert public_review == valid_review

    def test_get_public_review_by_id_fail_does_not_exist(self):
        public_review = self.review_selector.get_public_review_by_id(999)

        assert public_review is None

    def test_get_public_review_by_id_fail_private_review(self, private_review):
        public_review = self.review_selector.get_public_review_by_id(private_review.id)

        assert public_review is None
