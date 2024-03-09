import pytest

from dump_in.reviews.selectors.reviews import ReviewSelector

pytestmark = pytest.mark.django_db


class TestGetReviewWithUserInfoById:
    def setup_method(self):
        self.review_selector = ReviewSelector()

    def test_get_review_with_user_info_by_id_and_user_id_success(self, valid_review, valid_user):
        review_with_user_info = self.review_selector.get_review_with_user_info_by_id_and_user_id(valid_review.id, valid_user)

        assert review_with_user_info == valid_review

    def test_get_review_with_user_info_by_id_and_user_id_success_is_mine_true(self, valid_review):
        review_with_user_info = self.review_selector.get_review_with_user_info_by_id_and_user_id(valid_review.id, valid_review.user)

        assert review_with_user_info.is_mine is True

    def test_get_review_with_user_info_by_id_and_user_id_success_is_mine_false(self, valid_review, valid_user):
        review_with_user_info = self.review_selector.get_review_with_user_info_by_id_and_user_id(valid_review.id, valid_user)

        assert review_with_user_info.is_mine is False

    def test_get_review_with_user_info_by_id_and_user_id_success_is_liked_true(self, valid_review, valid_user):
        valid_review.user_review_like_logs.add(valid_user)

        review_with_user_info = self.review_selector.get_review_with_user_info_by_id_and_user_id(valid_review.id, valid_user)

        assert review_with_user_info.is_liked is True

    def test_get_review_with_user_info_by_id_and_user_id_success_is_liked_false(self, valid_review, valid_user):
        review_with_user_info = self.review_selector.get_review_with_user_info_by_id_and_user_id(valid_review.id, valid_user)

        assert review_with_user_info.is_liked is False

    def test_get_review_with_user_info_by_id_and_user_id_success_anonymous_user(self, valid_review, inactive_user):
        review_with_user_info = self.review_selector.get_review_with_user_info_by_id_and_user_id(valid_review.id, inactive_user)

        assert review_with_user_info == valid_review

    def test_get_review_with_user_info_by_id_and_user_id_fail_does_not_exist(self, valid_user):
        review_with_user_info = self.review_selector.get_review_with_user_info_by_id_and_user_id(999, valid_user)

        assert review_with_user_info is None

    def test_get_review_with_user_info_by_id_and_user_id_fail_deleted_review(self, deleted_review, valid_user):
        review_with_user_info = self.review_selector.get_review_with_user_info_by_id_and_user_id(deleted_review.id, valid_user)

        assert review_with_user_info is None
