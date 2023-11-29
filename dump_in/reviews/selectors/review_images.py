from django.db.models import QuerySet

from dump_in.reviews.models import ReviewImage


class ReviewImageSelector:
    def get_review_queryset_by_review_id(self, review_id: int) -> QuerySet[ReviewImage]:
        return ReviewImage.objects.filter(review_id=review_id)
