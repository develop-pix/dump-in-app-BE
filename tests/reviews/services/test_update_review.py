import uuid

import pytest

from dump_in.common.exception.exceptions import (
    NotFoundException,
    PermissionDeniedException,
)
from dump_in.reviews.enums import CameraShot, FrameColor
from dump_in.reviews.services import ReviewService

pytestmark = pytest.mark.django_db


class TestUpdateReview:
    def setup_method(self):
        self.review_service = ReviewService()

    def test_update_review_success(self, concept, photo_booth, valid_review):
        main_thumbnail_image_url = "https://test.com/test.jpg"
        image_urls = ["https://test.com/test.jpg", "https://test.com/test.jpg"]
        content = "test"
        photo_booth_id = photo_booth.id
        date = "2023-01-01"
        frame_color = FrameColor.BLACK.value
        participants = 1
        camera_shot = CameraShot.CLOSEUP.value
        concept_names = [concept.name]
        goods_amount = True
        curl_amount = True
        is_public = True

        review = self.review_service.update_review(
            review_id=valid_review.id,
            main_thumbnail_image_url=main_thumbnail_image_url,
            image_urls=image_urls,
            content=content,
            photo_booth_id=photo_booth_id,
            date=date,
            frame_color=frame_color,
            participants=participants,
            camera_shot=camera_shot,
            concept_names=concept_names,
            goods_amount=goods_amount,
            curl_amount=curl_amount,
            is_public=is_public,
            user_id=valid_review.user.id,
        )

        assert review.content == content
        assert review.main_thumbnail_image_url == main_thumbnail_image_url
        assert str(review.photo_booth.id) == photo_booth_id
        assert review.date == date
        assert review.frame_color == frame_color
        assert review.participants == participants
        assert review.camera_shot == camera_shot
        assert review.goods_amount == goods_amount
        assert review.curl_amount == curl_amount
        assert review.is_public == is_public
        assert review.user == valid_review.user
        assert review.concept.all()[0] == concept
        assert review.review_image.count() == len(image_urls)
        assert review.review_image.all()[0].review_image_url == image_urls[0]
        assert review.review_image.all()[1].review_image_url == image_urls[1]

    def test_update_review_fail_photo_booth_does_not_exist(self, concept, valid_review):
        main_thumbnail_image_url = "https://test.com/test.jpg"
        image_urls = ["https://test.com/test.jpg", "https://test.com/test.jpg"]
        content = "test"
        photo_booth_id = str(uuid.uuid4())
        date = "2023-01-01"
        frame_color = FrameColor.BLACK.value
        participants = 1
        camera_shot = CameraShot.CLOSEUP.value
        concept_names = [concept.name]
        goods_amount = True
        curl_amount = True
        is_public = True

        with pytest.raises(NotFoundException) as e:
            self.review_service.update_review(
                review_id=valid_review.id,
                main_thumbnail_image_url=main_thumbnail_image_url,
                image_urls=image_urls,
                content=content,
                photo_booth_id=photo_booth_id,
                date=date,
                frame_color=frame_color,
                participants=participants,
                camera_shot=camera_shot,
                concept_names=concept_names,
                goods_amount=goods_amount,
                curl_amount=curl_amount,
                is_public=is_public,
                user_id=valid_review.user.id,
            )

        assert e.value.detail == "PhotoBooth does not exist"
        assert e.value.status_code == 404

    def test_update_review_fail_review_does_not_exist(self, concept, valid_review):
        main_thumbnail_image_url = "https://test.com/test.jpg"
        image_urls = ["https://test.com/test.jpg", "https://test.com/test.jpg"]
        content = "test"
        photo_booth_id = valid_review.photo_booth.id
        date = "2023-01-01"
        frame_color = FrameColor.BLACK.value
        participants = 1
        camera_shot = CameraShot.CLOSEUP.value
        concept_names = [concept.name]
        goods_amount = True
        curl_amount = True
        is_public = True

        with pytest.raises(NotFoundException) as e:
            self.review_service.update_review(
                review_id=999999999,
                main_thumbnail_image_url=main_thumbnail_image_url,
                image_urls=image_urls,
                content=content,
                photo_booth_id=photo_booth_id,
                date=date,
                frame_color=frame_color,
                participants=participants,
                camera_shot=camera_shot,
                concept_names=concept_names,
                goods_amount=goods_amount,
                curl_amount=curl_amount,
                is_public=is_public,
                user_id=valid_review.user.id,
            )

        assert e.value.detail == "Review does not exist"
        assert e.value.status_code == 404

    def test_update_review_fail_permission_denied(self, concept, valid_review, valid_user):
        main_thumbnail_image_url = "https://test.com/test.jpg"
        image_urls = ["https://test.com/test.jpg", "https://test.com/test.jpg"]
        content = "test"
        photo_booth_id = valid_review.photo_booth.id
        date = "2023-01-01"
        frame_color = FrameColor.BLACK.value
        participants = 1
        camera_shot = CameraShot.CLOSEUP.value
        concept_names = [concept.name]
        goods_amount = True
        curl_amount = True
        is_public = True

        with pytest.raises(PermissionDeniedException) as e:
            self.review_service.update_review(
                review_id=valid_review.id,
                main_thumbnail_image_url=main_thumbnail_image_url,
                image_urls=image_urls,
                content=content,
                photo_booth_id=photo_booth_id,
                date=date,
                frame_color=frame_color,
                participants=participants,
                camera_shot=camera_shot,
                concept_names=concept_names,
                goods_amount=goods_amount,
                curl_amount=curl_amount,
                is_public=is_public,
                user_id=valid_user.id,
            )

        assert e.value.detail == "You do not have permission to perform this action."
        assert e.value.status_code == 403
