import concurrent.futures

import pytest

from dump_in.common.exception.exceptions import NotFoundException
from dump_in.reviews.services import ReviewService

pytestmark = pytest.mark.django_db


class TestLikeReview:
    def setup_method(self):
        self.review_service = ReviewService()

    def test_like_review_success(self, valid_review, valid_user):
        review, is_liked = self.review_service.like_review(review_id=valid_review.id, user=valid_user)

        assert is_liked is True
        assert review.user_review_like_logs.count() == 1

    def test_like_review_success_already_like(self, valid_review, valid_user):
        valid_review.user_review_like_logs.add(valid_user)
        review, is_like = self.review_service.like_review(review_id=valid_review.id, user=valid_user)

        assert is_like is False
        assert review.user_review_like_logs.count() == 0

    def test_like_review_fail_review_does_not_exist(self, valid_user):
        with pytest.raises(NotFoundException) as e:
            self.review_service.like_review(review_id=999, user=valid_user)

        assert e.value.detail == "Review does not exist"
        assert e.value.status_code == 404

    @pytest.mark.django_db(transaction=True)
    def test_like_review_success_concurrency(self, valid_review, valid_user, inactive_user):
        before_review_like_count = valid_review.like_count

        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            future1 = executor.submit(self.review_service.like_review, valid_review.id, valid_user)
            future2 = executor.submit(self.review_service.like_review, valid_review.id, inactive_user)

            result1 = future1.result()
            result2 = future2.result()

        result1_review, result1_is_like = result1
        result2_review, result2_is_like = result2

        assert result1_is_like is True
        assert result2_is_like is True

        valid_review.refresh_from_db()
        assert before_review_like_count + 2 == valid_review.like_count

        self.review_service.like_review(valid_review.id, valid_user)
        valid_review.refresh_from_db()
        assert before_review_like_count + 1 == valid_review.like_count
