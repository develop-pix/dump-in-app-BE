import time

from dump_in.reviews.models import Review
from dump_in.reviews.selectors.reviews import ReviewSelector


class TestGetReviewQuerysetWithPhotoBoothByUserLike:
    def setup_method(self):
        self.review_selector = ReviewSelector()

    def test_get_review_queryset_with_photo_booth_by_user_like_success(self, valid_review_list, valid_user):
        for valid_review in valid_review_list:
            valid_review.user_review_like_logs.add(valid_user)

        review_queryset_with_photo_booth = self.review_selector.get_review_queryset_with_photo_booth_by_user_like(valid_user)

        assert review_queryset_with_photo_booth.count() == len(valid_review_list)

    def test_get_review_queryset_with_photo_booth_by_user_like_fail_does_not_exist(self, valid_user):
        review_queryset_with_photo_booth = self.review_selector.get_review_queryset_with_photo_booth_by_user_like(valid_user)

        assert list(review_queryset_with_photo_booth) == []

    def test_get_review_queryset_with_photo_booth_by_user_like_fail_deleted_review(self, deleted_review, valid_user):
        deleted_review.user_review_like_logs.add(valid_user)

        review_queryset_with_photo_booth = self.review_selector.get_review_queryset_with_photo_booth_by_user_like(valid_user)

        assert list(review_queryset_with_photo_booth) == []

    def test_get_review_queryset_with_photo_booth_by_user_like_fail_private_review(self, private_review, valid_user):
        private_review.user_review_like_logs.add(valid_user)

        review_queryset_with_photo_booth = self.review_selector.get_review_queryset_with_photo_booth_by_user_like(valid_user)

        assert list(review_queryset_with_photo_booth) == []

    def test_get_review_queryset_with_photo_booth_by_user_like_select_related_performance(self, valid_review_list):
        start_time = time.time()

        review_list = Review.objects.filter(is_deleted=False, is_public=True)

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

        review_queryset_with_photo_booth = self.review_selector.get_review_queryset_with_photo_booth_by_user_like(valid_review_list[0].user)

        for review in review_queryset_with_photo_booth:
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
