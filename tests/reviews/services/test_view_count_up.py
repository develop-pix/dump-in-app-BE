import pytest

from dump_in.common.exception.exceptions import (
    NotFoundException,
    PermissionDeniedException,
)
from dump_in.reviews.services import ReviewService

pytestmark = pytest.mark.django_db


class TestViewCountUp:
    def setup_method(self):
        self.review_service = ReviewService()

    def test_view_count_up_success(self, valid_review):
        before_view_count = valid_review.view_count

        review = self.review_service.view_count_up(review_id=valid_review.id, user=valid_review.user)

        assert review.view_count == before_view_count + 1

    def test_view_count_up_fail_review_does_not_exist(self, inactive_user):
        with pytest.raises(NotFoundException) as e:
            self.review_service.view_count_up(review_id=999, user=inactive_user)

        assert e.value.detail == "Review does not exist"
        assert e.value.status_code == 404

    def test_view_count_up_fail_permission_denied(self, private_review, valid_user):
        with pytest.raises(PermissionDeniedException) as e:
            self.review_service.view_count_up(review_id=private_review.id, user=valid_user)

        assert e.value.detail == "You do not have permission to perform this action."
        assert e.value.status_code == 403
