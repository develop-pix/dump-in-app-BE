from typing import List, Optional, Tuple

from django.db import transaction
from django.db.models import F

from dump_in.common.exception.exceptions import (
    NotFoundException,
    PermissionDeniedException,
)
from dump_in.photo_booths.selectors.photo_booths import PhotoBoothSelector
from dump_in.reviews.models import Review, ReviewImage
from dump_in.reviews.selectors.concepts import ConceptSelector
from dump_in.reviews.selectors.reviews import ReviewSelector


class ReviewService:
    @transaction.atomic
    def create_review(
        self,
        main_thumbnail_image_url: str,
        image_urls: Optional[List[str]],
        content: str,
        photo_booth_id: str,
        date: str,
        frame_color: str,
        participants: int,
        camera_shot: str,
        concept: List[str],
        goods_amount: Optional[bool],
        curl_amount: Optional[bool],
        is_public: bool,
        user_id,
    ) -> Review:
        photo_booth_selector = PhotoBoothSelector()
        photo_booth = photo_booth_selector.get_photo_booth_by_id(photo_booth_id=photo_booth_id)

        if photo_booth is None:
            raise NotFoundException("PhotoBooth does not exist")

        review = Review.objects.create(
            content=content,
            main_thumbnail_image_url=main_thumbnail_image_url,
            photo_booth=photo_booth,
            date=date,
            frame_color=frame_color,
            participants=participants,
            camera_shot=camera_shot,
            goods_amount=goods_amount,
            curl_amount=curl_amount,
            is_public=is_public,
            user_id=user_id,
        )

        if image_urls is not None:
            review.review_image.bulk_create(
                [
                    ReviewImage(
                        review=review,
                        review_image_url=image_url,
                    )
                    for image_url in image_urls
                ],
            )

        concept_selector = ConceptSelector()
        concepts = concept_selector.get_concept_queryset_by_names(concept=concept)
        review.concept.set(concepts)

        return review

    @transaction.atomic
    def update_review(
        self,
        review_id: int,
        main_thumbnail_image_url: str,
        image_urls: Optional[List[str]],
        content: str,
        photo_booth_id: str,
        date: str,
        frame_color: str,
        participants: int,
        camera_shot: str,
        concept: List[str],
        goods_amount: Optional[bool],
        curl_amount: Optional[bool],
        is_public: bool,
        user_id,
    ) -> Review:
        photo_booth_selector = PhotoBoothSelector()
        photo_booth = photo_booth_selector.get_photo_booth_by_id(photo_booth_id=photo_booth_id)

        if photo_booth is None:
            raise NotFoundException("PhotoBooth does not exist")

        review_selector = ReviewSelector()
        review = review_selector.get_review_by_id(review_id=review_id)

        if review is None:
            raise NotFoundException("Review does not exist")

        if review.user_id != user_id:
            raise PermissionDeniedException()

        review.content = content
        review.main_thumbnail_image_url = main_thumbnail_image_url
        review.photo_booth = photo_booth
        review.date = date
        review.frame_color = frame_color
        review.participants = participants
        review.camera_shot = camera_shot
        review.goods_amount = goods_amount
        review.curl_amount = curl_amount
        review.is_public = is_public
        review.save()

        if image_urls is not None:
            review.review_image.all().delete()
            review.review_image.bulk_create(
                [
                    ReviewImage(
                        review=review,
                        review_image_url=image_url,
                    )
                    for image_url in image_urls
                ],
            )

        concept_selector = ConceptSelector()
        concepts = concept_selector.get_concept_queryset_by_names(concept=concept)

        review.concept.clear()
        review.concept.set(concepts)

        return review

    @transaction.atomic
    def soft_delete_review(self, review_id: int, user_id):
        review_selector = ReviewSelector()
        review = review_selector.get_review_by_id(review_id=review_id)

        if review is None:
            raise NotFoundException("Review does not exist")

        if review.user_id != user_id:
            raise PermissionDeniedException()

        review.is_deleted = True
        review.save()

    @transaction.atomic
    def like_review(self, review_id: int, user) -> Tuple[Review, bool]:
        review_selector = ReviewSelector()
        review = review_selector.get_public_review_by_id(review_id=review_id)

        if review is None:
            raise NotFoundException("Review does not exist")

        if review.user_review_like_logs.filter(id=user.id).exists():
            review.user_review_like_logs.remove(user)
            review.like_count = F("like_count") - 1
            is_liked = False

        else:
            review.user_review_like_logs.add(user)
            review.like_count = F("like_count") + 1
            is_liked = True

        review.save(update_fields=["like_count"])

        return review, is_liked

    @transaction.atomic
    def view_count_up(self, review_id: int, user_id) -> Review:
        review_selector = ReviewSelector()
        review = review_selector.get_review_with_user_info_by_id_and_user_id(
            review_id=review_id,
            user_id=user_id,
        )

        if review is None:
            raise NotFoundException("Review does not exist")

        if review.is_public is False and review.user_id != user_id:
            raise PermissionDeniedException()

        review.view_count += 1
        review.save(update_fields=["view_count"])

        return review
