import pytest

from dump_in.common.exception.exceptions import (
    NotFoundException,
    PermissionDeniedException,
)
from dump_in.reviews.services.reviews import ReviewService

pytestmark = pytest.mark.django_db


class TestSoftDeleteReview:
    def setup_method(self):
        self.review_service = ReviewService()

    def test_soft_delete_review_success(self, valid_review):
        review = self.review_service.soft_delete_review(review_id=valid_review.id, user=valid_review.user)

        assert review.is_deleted == True

    def test_soft_delete_review_fail_review_does_not_exist(self, valid_user):
        with pytest.raises(NotFoundException) as e:
            self.review_service.soft_delete_review(review_id=1, user=valid_user)

        assert e.value.detail == "Review does not exist"
        assert e.value.status_code == 404

    def test_soft_delete_review_fail_permission_denied(self, valid_review, valid_user):
        with pytest.raises(PermissionDeniedException) as e:
            self.review_service.soft_delete_review(review_id=valid_review.id, user=valid_user)

        assert e.value.detail == "Permission denied"
        assert e.value.status_code == 403
