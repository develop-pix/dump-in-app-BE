from typing import Optional

from django.db.models import QuerySet

from dump_in.reviews.filters import ReviewFilter
from dump_in.reviews.models import Review


class ReviewSelector:
    def get_review_with_review_images_and_hashtags_by_id(self, review_id: int) -> Optional[Review]:
        try:
            return Review.objects.filter(id=review_id, is_deleted=False).get()
        except Review.DoesNotExist:
            return None

    def get_review_by_id(self, review_id: int) -> Optional[Review]:
        try:
            return Review.objects.filter(id=review_id, is_deleted=False).get()
        except Review.DoesNotExist:
            return None

    def get_public_review_by_id(self, review_id: int) -> Optional[Review]:
        try:
            return Review.objects.filter(id=review_id, is_deleted=False, is_public=True).get()
        except Review.DoesNotExist:
            return None

    def get_review_queryset_with_photo_booth_by_user_id(self, user) -> QuerySet[Review]:
        return Review.objects.select_related("photo_booth").filter(user_id=user.id, is_deleted=False)

    def get_review_queryset_by_user_like(self, user) -> QuerySet[Review]:
        return user.review_like_logs.all()

    def get_review_count(self, filters: Optional[dict]) -> int:
        filters = filters or {}
        qs = (
            Review.objects.select_related("photo_booth")
            .prefetch_related("review_images", "hashtags")
            .filter(is_deleted=False, is_public=True)
        )
        return ReviewFilter(filters, qs).qs.count()

    def get_review_list(self, filters: Optional[dict]) -> QuerySet[Review]:
        filters = filters or {}
        qs = (
            Review.objects.select_related("photo_booth")
            .prefetch_related("review_images", "hashtags")
            .filter(is_deleted=False, is_public=True)
        )
        return ReviewFilter(filters, qs).qs
