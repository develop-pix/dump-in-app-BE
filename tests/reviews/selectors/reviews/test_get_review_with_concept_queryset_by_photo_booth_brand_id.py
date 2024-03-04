import pytest

from dump_in.reviews.selectors.reviews import ReviewSelector

pytestmark = pytest.mark.django_db


class TestGetReviewWithConceptQuerysetByPhotoBoothBrandId:
    def setup_method(self):
        self.review_selector = ReviewSelector()

    def test_get_review_with_concept_queryset_by_photo_booth_brand_id_brand_id_success_single_review(self, valid_review):
        review_with_concept_queryset = self.review_selector.get_review_with_concept_queryset_by_photo_booth_brand_id(
            valid_review.photo_booth.photo_booth_brand.id
        )

        assert review_with_concept_queryset.first() == valid_review

    def test_get_review_with_concept_queryset_by_photo_booth_brand_id_brand_id_success_multiple_review(self, valid_review_list):
        review_with_concept_queryset = self.review_selector.get_review_with_concept_queryset_by_photo_booth_brand_id(
            valid_review_list[0].photo_booth.photo_booth_brand.id
        )

        assert review_with_concept_queryset.count() == len(valid_review_list)

    def test_get_review_with_concept_queryset_by_photo_booth_brand_id_fail_does_not_exist(self):
        review_with_concept_queryset = self.review_selector.get_review_with_concept_queryset_by_photo_booth_brand_id(1234)

        assert review_with_concept_queryset.count() == 0

    def test_get_review_with_concept_queryset_by_photo_booth_brand_id_fail_deleted_review(self, deleted_review):
        review_with_concept_queryset = self.review_selector.get_review_with_concept_queryset_by_photo_booth_brand_id(
            deleted_review.photo_booth.photo_booth_brand.id
        )

        assert review_with_concept_queryset.count() == 0

    def test_get_review_with_concept_queryset_by_photo_booth_brand_id_fail_private_review(self, private_review):
        review_with_concept_queryset = self.review_selector.get_review_with_concept_queryset_by_photo_booth_brand_id(
            private_review.photo_booth.photo_booth_brand.id
        )

        assert review_with_concept_queryset.count() == 0
