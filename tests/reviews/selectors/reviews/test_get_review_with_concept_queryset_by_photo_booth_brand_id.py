import time

import pytest

from dump_in.reviews.models import Review
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

    def test_get_review_with_concept_queryset_by_photo_booth_brand_id_brand_id_success_multiple_review(self, valid_review_bulk):
        review_with_concept_queryset = self.review_selector.get_review_with_concept_queryset_by_photo_booth_brand_id(
            valid_review_bulk[0].photo_booth.photo_booth_brand.id
        )

        assert review_with_concept_queryset.count() == len(valid_review_bulk)

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

    def test_get_review_with_concept_queryset_by_photo_booth_brand_id_prefetch_related_performance(self, valid_review_bulk):
        start_time = time.time()

        review_list = Review.objects.filter(
            photo_booth__photo_booth_brand_id=valid_review_bulk[0].photo_booth.photo_booth_brand.id, is_deleted=False, is_public=True
        )

        for review in review_list:
            for concept in review.concept.all():
                concept.name

        end_time = time.time()
        time_with_filter = end_time - start_time

        start_time = time.time()

        review_with_concept_queryset = self.review_selector.get_review_with_concept_queryset_by_photo_booth_brand_id(
            valid_review_bulk[0].photo_booth.photo_booth_brand.id
        )

        for review in review_with_concept_queryset:
            for concept in review.concept.all():
                concept.name

        end_time = time.time()
        time_with_prefetch_related = end_time - start_time

        assert time_with_filter > time_with_prefetch_related
