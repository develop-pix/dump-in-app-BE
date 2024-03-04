from dump_in.reviews.selectors.reviews import ReviewSelector


class TestGetReviewWithPhotoBoothQuerysetByUserLike:
    def setup_method(self):
        self.review_selector = ReviewSelector()

    def test_get_review_with_photo_booth_queryset_by_user_like_success_single_review(self, valid_review, valid_user):
        valid_review.user_review_like_logs.add(valid_user)

        review_with_photo_booth_queryset = self.review_selector.get_review_with_photo_booth_queryset_by_user_like(valid_user.id)

        assert review_with_photo_booth_queryset.first() == valid_review

    def test_get_review_with_photo_booth_queryset_by_user_like_success_multiple_review(self, valid_review_list, valid_user):
        for valid_review in valid_review_list:
            valid_review.user_review_like_logs.add(valid_user)

        review_queryset_with_photo_booth = self.review_selector.get_review_with_photo_booth_queryset_by_user_like(valid_user.id)

        assert review_queryset_with_photo_booth.count() == len(valid_review_list)

    def test_get_review_with_photo_booth_queryset_by_user_like_fail_does_not_exist(self, valid_user):
        review_queryset_with_photo_booth = self.review_selector.get_review_with_photo_booth_queryset_by_user_like(valid_user.id)

        assert review_queryset_with_photo_booth.count() == 0

    def test_get_review_with_photo_booth_queryset_by_user_like_fail_deleted_review(self, deleted_review, valid_user):
        deleted_review.user_review_like_logs.add(valid_user)

        review_queryset_with_photo_booth = self.review_selector.get_review_with_photo_booth_queryset_by_user_like(valid_user.id)

        assert review_queryset_with_photo_booth.count() == 0

    def test_get_review_with_photo_booth_queryset_by_user_like_fail_private_review(self, private_review, valid_user):
        private_review.user_review_like_logs.add(valid_user)

        review_queryset_with_photo_booth = self.review_selector.get_review_with_photo_booth_queryset_by_user_like(valid_user.id)

        assert review_queryset_with_photo_booth.count() == 0
