from typing import Optional

from django.db.models import BooleanField, Case, QuerySet, When

from dump_in.reviews.filters import ReviewFilter
from dump_in.reviews.models import Review


class ReviewSelector:
    def get_review_queryset_with_review_image_and_concept_by_photo_booth_id(self, photo_booth_id: str) -> QuerySet[Review]:
        return Review.objects.prefetch_related("review_image", "concept").filter(
            photo_booth_id=photo_booth_id, is_deleted=False, is_public=True
        )

    def get_review_by_id(self, review_id: int) -> Optional[Review]:
        try:
            return Review.objects.filter(id=review_id, is_deleted=False).get()
        except Review.DoesNotExist:
            return None

    def get_review_with_user_info_by_id(self, review_id: int, user) -> Optional[Review]:
        try:
            return (
                Review.objects.annotate(
                    is_liked=Case(
                        When(userreviewlikelog__user=user, then=True),
                        default=False,
                        output_field=BooleanField(),
                    ),
                    is_mine=Case(
                        When(user=user, then=True),
                        default=False,
                        output_field=BooleanField(),
                    ),
                )
                .filter(id=review_id, is_deleted=False)
                .get()
            )
        except Review.DoesNotExist:
            return None

    def get_public_review_by_id(self, review_id: int) -> Optional[Review]:
        try:
            return Review.objects.filter(id=review_id, is_deleted=False, is_public=True).get()
        except Review.DoesNotExist:
            return None

    def get_review_queryset_with_photo_booth_and_brand_by_user_id(self, user) -> QuerySet[Review]:
        return (
            Review.objects.select_related("photo_booth")
            .prefetch_related("photo_booth__photo_booth_brand")
            .filter(user_id=user.id, is_deleted=False)
        )

    def get_review_queryset_with_photo_booth_by_user_like(self, user) -> QuerySet[Review]:
        return Review.objects.select_related("photo_booth").filter(userreviewlikelog__user=user, is_deleted=False, is_public=True)

    def get_review_count(self, filters: Optional[dict]) -> int:
        filters = filters or {}
        qs = Review.objects.filter(is_deleted=False, is_public=True)

        return ReviewFilter(filters, qs).qs.count()

    def get_review_list(self, filters: Optional[dict]) -> QuerySet[Review]:
        filters = filters or {}
        qs = Review.objects.select_related("photo_booth").filter(is_deleted=False, is_public=True)
        return ReviewFilter(filters, qs).qs
