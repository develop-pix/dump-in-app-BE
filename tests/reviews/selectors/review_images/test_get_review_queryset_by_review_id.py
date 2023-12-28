import pytest

from dump_in.reviews.selectors.review_images import ReviewImageSelector

pytestmark = pytest.mark.django_db


class TestGetReviewQuerysetByReviewId:
    def setup_method(self):
        self.review_image_selector = ReviewImageSelector()

    def test_get_review_image_queryset_by_review_id_success_single_review_image(self, review_image):
        review_image_queryset = self.review_image_selector.get_review_image_queryset_by_review_id(review_image.review_id)

        assert review_image_queryset.first() == review_image

    def test_get_review_image_queryset_by_review_id_success_multiple_review_image(self, review_image_list):
        review_image_queryset = self.review_image_selector.get_review_image_queryset_by_review_id(review_image_list[0].review_id)

        assert review_image_queryset.count() == len(review_image_list)

    def test_get_review_image_queryset_by_review_id_fail_does_not_exist(self):
        review_image_queryset = self.review_image_selector.get_review_image_queryset_by_review_id(999)

        assert review_image_queryset.count() == 0
