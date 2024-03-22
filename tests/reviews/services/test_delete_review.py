import pytest

from dump_in.common.exception.exceptions import NotFoundException
from dump_in.reviews.models import Review
from dump_in.reviews.services import ReviewService

pytestmark = pytest.mark.django_db


class TestDeleteReview:
    def setup_method(self):
        self.review_service = ReviewService()

    def test_delete_review_success(self, valid_review):
        self.review_service.delete_review(review_id=valid_review.id, user_id=valid_review.user_id)

        assert Review.objects.filter(id=valid_review.id).first() is None

    def test_delete_review_fail_review_does_not_exist(self, valid_user):
        with pytest.raises(NotFoundException) as e:
            self.review_service.delete_review(review_id=1, user_id=valid_user.id)

        assert e.value.detail == "Review does not exist"
        assert e.value.status_code == 404
