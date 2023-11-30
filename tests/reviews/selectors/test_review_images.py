from dump_in.reviews.selectors.review_images import ReviewImageSelector


class TestReviewImageSelector:
    def setup_method(self):
        self.review_image_selector = ReviewImageSelector()

    def test_get_review_queryset_by_review_id_success(self, review_image):
        review_id = review_image.review_id
        review_image_queryset = self.review_image_selector.get_review_queryset_by_review_id(review_id)
        assert review_image_queryset.count() == 1
