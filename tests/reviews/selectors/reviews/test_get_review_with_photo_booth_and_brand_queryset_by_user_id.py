import pytest

from dump_in.reviews.selectors.reviews import ReviewSelector

pytestmark = pytest.mark.django_db


class TestGetReviewWithPhotoBoothAndBrandQuerysetByUserId:
    def setup_method(self):
        self.review_selector = ReviewSelector()

    def test_get_review_with_photo_booth_and_brand_queryset_by_user_id_success_single_review(self, valid_review):
        review_with_photo_booth_and_brand_queryset = self.review_selector.get_review_with_photo_booth_and_brand_queryset_by_user_id(
            valid_review.user_id
        )

        assert review_with_photo_booth_and_brand_queryset.first() == valid_review

    def test_get_review_with_photo_booth_and_brand_queryset_by_user_id_success_multiple_review(
        self, valid_review_list_by_valid_user, valid_user
    ):
        review_queryset_with_photo_booth_and_brand = self.review_selector.get_review_with_photo_booth_and_brand_queryset_by_user_id(
            valid_user.id
        )

        assert review_queryset_with_photo_booth_and_brand.count() == len(valid_review_list_by_valid_user)

    def test_get_review_with_photo_booth_and_brand_queryset_by_user_id_fail_does_not_exist(self, valid_user):
        review_queryset_with_photo_booth_and_brand = self.review_selector.get_review_with_photo_booth_and_brand_queryset_by_user_id(
            valid_user.id
        )

        assert review_queryset_with_photo_booth_and_brand.count() == 0
