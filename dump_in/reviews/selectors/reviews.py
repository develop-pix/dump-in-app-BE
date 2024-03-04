from typing import Optional

from django.db.models import BooleanField, Case, QuerySet, When

from dump_in.reviews.filters import ReviewFilter
from dump_in.reviews.models import Review


class ReviewSelector:
    def get_review_with_concept_queryset_by_photo_booth_id_order_by_created_at_desc(self, photo_booth_id: str) -> QuerySet[Review]:
        return (
            Review.objects.prefetch_related("concept")
            .filter(photo_booth_id=photo_booth_id, is_deleted=False, is_public=True)
            .order_by("-created_at")
        )

    def get_review_with_concept_queryset_by_photo_booth_brand_id_order_by_created_at_desc(
        self, photo_booth_brand_id: int
    ) -> QuerySet[Review]:
        return (
            Review.objects.prefetch_related("concept")
            .filter(photo_booth__photo_booth_brand_id=photo_booth_brand_id, is_deleted=False, is_public=True)
            .order_by("-created_at")
        )

    def get_review_by_id(self, review_id: int) -> Optional[Review]:
        try:
            return Review.objects.filter(id=review_id, is_deleted=False).get()
        except Review.DoesNotExist:
            return None

    def get_review_with_user_info_by_id_and_user_id(self, review_id: int, user_id) -> Optional[Review]:
        try:
            qs = Review.objects.filter(id=review_id, is_deleted=False)

            if user_id:
                qs = qs.annotate(
                    is_liked=Case(
                        When(userreviewlikelog__user_id=user_id, then=True),
                        default=False,
                        output_field=BooleanField(),
                    ),
                    is_mine=Case(
                        When(user_id=user_id, then=True),
                        default=False,
                        output_field=BooleanField(),
                    ),
                )

            return qs.get()
        except Review.DoesNotExist:
            return None

    def get_public_review_by_id(self, review_id: int) -> Optional[Review]:
        try:
            return Review.objects.filter(id=review_id, is_deleted=False, is_public=True).get()
        except Review.DoesNotExist:
            return None

    def get_review_with_photo_booth_and_brand_queryset_by_user_id(self, user_id) -> QuerySet[Review]:
        return (
            Review.objects.select_related("photo_booth")
            .prefetch_related("photo_booth__photo_booth_brand")
            .filter(user_id=user_id, is_deleted=False)
        )

    def get_review_with_photo_booth_queryset_by_user_like(self, user_id) -> QuerySet[Review]:
        return Review.objects.select_related("photo_booth").filter(userreviewlikelog__user_id=user_id, is_deleted=False, is_public=True)

    def get_review_count(self, filters: Optional[dict]) -> int:
        filters = filters or {}
        qs = Review.objects.filter(is_deleted=False, is_public=True)
        return ReviewFilter(filters, qs).qs.count()

    def get_review_list(self, filters: Optional[dict]) -> QuerySet[Review]:
        filters = filters or {}
        qs = Review.objects.select_related("photo_booth").filter(is_deleted=False, is_public=True)
        return ReviewFilter(filters, qs).qs
