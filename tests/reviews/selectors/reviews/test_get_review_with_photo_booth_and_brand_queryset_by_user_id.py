import time

import pytest

from dump_in.reviews.models import Review
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

    def test_get_review_with_photo_booth_and_brand_queryset_by_user_id_fail_deleted_review(self, deleted_review):
        review_queryset_with_photo_booth_and_brand = self.review_selector.get_review_with_photo_booth_and_brand_queryset_by_user_id(
            deleted_review.user.id
        )

        assert review_queryset_with_photo_booth_and_brand.count() == 0

    def test_get_review_with_photo_booth_and_brand_queryset_by_user_id_select_related_performance(self, valid_review_list_by_valid_user):
        start_time = time.time()

        review_list = Review.objects.filter(user_id=valid_review_list_by_valid_user[0].user_id, is_deleted=False)

        for review in review_list:
            review.photo_booth.location
            review.photo_booth.name
            review.photo_booth.latitude
            review.photo_booth.longitude
            review.photo_booth.point
            review.photo_booth.street_address
            review.photo_booth.road_address
            review.photo_booth.operation_time
            review.photo_booth.like_count
            review.photo_booth.view_count

        end_time = time.time()
        time_with_filter = end_time - start_time

        start_time = time.time()

        review_queryset_with_photo_booth_and_brand = self.review_selector.get_review_with_photo_booth_and_brand_queryset_by_user_id(
            valid_review_list_by_valid_user[0].user.id
        )

        for review in review_queryset_with_photo_booth_and_brand:
            review.photo_booth.location
            review.photo_booth.name
            review.photo_booth.latitude
            review.photo_booth.longitude
            review.photo_booth.point
            review.photo_booth.street_address
            review.photo_booth.road_address
            review.photo_booth.operation_time
            review.photo_booth.like_count
            review.photo_booth.view_count

        end_time = time.time()
        time_with_select_related = end_time - start_time

        assert time_with_filter > time_with_select_related

    def test_get_review_with_photo_booth_and_brand_queryset_by_user_id_prefetch_related_performance(self, valid_review_list_by_valid_user):
        start_time = time.time()

        review_list = Review.objects.filter(user_id=valid_review_list_by_valid_user[0].user_id, is_deleted=False)

        for review in review_list:
            review.photo_booth.photo_booth_brand.photo_booth_url
            review.photo_booth.photo_booth_brand.main_thumbnail_image_url
            review.photo_booth.photo_booth_brand.logo_image_url
            review.photo_booth.photo_booth_brand.is_event

        end_time = time.time()
        time_with_filter = end_time - start_time

        start_time = time.time()

        review_queryset_with_photo_booth_and_brand = self.review_selector.get_review_with_photo_booth_and_brand_queryset_by_user_id(
            valid_review_list_by_valid_user[0].user.id
        )

        for review in review_queryset_with_photo_booth_and_brand:
            review.photo_booth.photo_booth_brand.photo_booth_url
            review.photo_booth.photo_booth_brand.main_thumbnail_image_url
            review.photo_booth.photo_booth_brand.logo_image_url
            review.photo_booth.photo_booth_brand.is_event

        end_time = time.time()
        time_with_prefetch_related = end_time - start_time

        assert time_with_filter > time_with_prefetch_related

    def test_get_review_with_photo_booth_and_brand_queryset_by_user_id_selected_and_prefetch_related_performance(
        self, valid_review_list_by_valid_user
    ):
        start_time = time.time()

        review_list = Review.objects.filter(user_id=valid_review_list_by_valid_user[0].user_id, is_deleted=False)

        for review in review_list:
            review.photo_booth.location
            review.photo_booth.name
            review.photo_booth.latitude
            review.photo_booth.longitude
            review.photo_booth.point
            review.photo_booth.street_address
            review.photo_booth.road_address
            review.photo_booth.operation_time
            review.photo_booth.like_count
            review.photo_booth.view_count

            review.photo_booth.location
            review.photo_booth.name
            review.photo_booth.latitude
            review.photo_booth.longitude
            review.photo_booth.point
            review.photo_booth.street_address
            review.photo_booth.road_address
            review.photo_booth.operation_time
            review.photo_booth.like_count
            review.photo_booth.view_count

        end_time = time.time()
        time_with_filter = end_time - start_time

        start_time = time.time()

        review_queryset_with_photo_booth_and_brand = self.review_selector.get_review_with_photo_booth_and_brand_queryset_by_user_id(
            valid_review_list_by_valid_user[0].user.id
        )

        for review in review_queryset_with_photo_booth_and_brand:
            review.photo_booth.location
            review.photo_booth.name
            review.photo_booth.latitude
            review.photo_booth.longitude
            review.photo_booth.point
            review.photo_booth.street_address
            review.photo_booth.road_address
            review.photo_booth.operation_time
            review.photo_booth.like_count
            review.photo_booth.view_count

            review.photo_booth.location
            review.photo_booth.name
            review.photo_booth.latitude
            review.photo_booth.longitude
            review.photo_booth.point
            review.photo_booth.street_address
            review.photo_booth.road_address
            review.photo_booth.operation_time
            review.photo_booth.like_count
            review.photo_booth.view_count

        end_time = time.time()
        time_with_selected_and_prefetch_related = end_time - start_time

        assert time_with_filter > time_with_selected_and_prefetch_related
