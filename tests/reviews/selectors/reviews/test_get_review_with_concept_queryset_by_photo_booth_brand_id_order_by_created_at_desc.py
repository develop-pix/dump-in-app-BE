import pytest

from dump_in.reviews.selectors.reviews import ReviewSelector

pytestmark = pytest.mark.django_db


class TestGetReviewWithConceptQuerysetByPhotoBoothBrandIdOrderByCreatedAtDesc:
    def setup_method(self):
        self.review_selector = ReviewSelector()

    def test_get_review_with_concept_queryset_by_photo_booth_brand_id_order_by_created_at_desc_brand_id_success_single_review(
        self, valid_review
    ):
        review_with_concept_queryset = (
            self.review_selector.get_review_with_concept_queryset_by_photo_booth_brand_id_order_by_created_at_desc(
                valid_review.photo_booth.photo_booth_brand.id
            )
        )

        assert review_with_concept_queryset.first() == valid_review

    def test_get_review_with_concept_queryset_by_photo_booth_brand_id_order_by_created_at_desc_brand_id_success_multiple_review(
        self, valid_review_list
    ):
        review_with_concept_queryset = (
            self.review_selector.get_review_with_concept_queryset_by_photo_booth_brand_id_order_by_created_at_desc(
                valid_review_list[0].photo_booth.photo_booth_brand.id
            )
        )

        sorted_valid_review_list = sorted(valid_review_list, key=lambda review: review.created_at, reverse=True)

        assert review_with_concept_queryset.count() == len(valid_review_list)
        assert review_with_concept_queryset[0] == sorted_valid_review_list[0]
        assert review_with_concept_queryset[1] == sorted_valid_review_list[1]
        assert review_with_concept_queryset[2] == sorted_valid_review_list[2]

    def test_get_review_with_concept_queryset_by_photo_booth_brand_id_order_by_created_at_desc_fail_does_not_exist(self):
        review_with_concept_queryset = (
            self.review_selector.get_review_with_concept_queryset_by_photo_booth_brand_id_order_by_created_at_desc(1234)
        )

        assert review_with_concept_queryset.count() == 0

    def test_get_review_with_concept_queryset_by_photo_booth_brand_id_order_by_created_at_desc_fail_deleted_review(self, deleted_review):
        review_with_concept_queryset = (
            self.review_selector.get_review_with_concept_queryset_by_photo_booth_brand_id_order_by_created_at_desc(
                deleted_review.photo_booth.photo_booth_brand.id
            )
        )

        assert review_with_concept_queryset.count() == 0

    def test_get_review_with_concept_queryset_by_photo_booth_brand_id_order_by_created_at_desc_fail_private_review(self, private_review):
        review_with_concept_queryset = (
            self.review_selector.get_review_with_concept_queryset_by_photo_booth_brand_id_order_by_created_at_desc(
                private_review.photo_booth.photo_booth_brand.id
            )
        )

        assert review_with_concept_queryset.count() == 0
