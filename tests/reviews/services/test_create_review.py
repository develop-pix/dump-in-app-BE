import uuid

import pytest

from dump_in.common.exception.exceptions import NotFoundException
from dump_in.reviews.models import Review
from dump_in.reviews.services import ReviewService

pytestmark = pytest.mark.django_db


class TestCreateReview:
    def setup_method(self):
        self.review_service = ReviewService()

    def test_create_review_success(self, valid_user, concept, photo_booth):
        main_thumbnail_image_url = "https://test.com/test.jpg"
        image_urls = ["https://test.com/test.jpg", "https://test.com/test.jpg"]
        content = "test"
        photo_booth_id = photo_booth.id
        date = "2023-01-01"
        frame_color = "test"
        participants = 1
        camera_shot = "test"
        concept_ids = [concept.id]
        goods_amount = True
        curl_amount = True
        is_public = True

        review = self.review_service.create_review(
            main_thumbnail_image_url=main_thumbnail_image_url,
            image_urls=image_urls,
            content=content,
            photo_booth_id=photo_booth_id,
            date=date,
            frame_color=frame_color,
            participants=participants,
            camera_shot=camera_shot,
            concept_ids=concept_ids,
            goods_amount=goods_amount,
            curl_amount=curl_amount,
            is_public=is_public,
            user=valid_user,
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
        assert review.user == valid_user
        assert review.concept.all()[0] == concept
        assert review.review_image.count() == len(image_urls)
        assert review.review_image.all()[0].review_image_url == image_urls[0]
        assert review.review_image.all()[1].review_image_url == image_urls[1]

    def test_create_review_fail_photo_booth_does_not_exist(self, valid_user, concept):
        main_thumbnail_image_url = "https://test.com/test.jpg"
        image_urls = ["https://test.com/test.jpg", "https://test.com/test.jpg"]
        content = "test"
        photo_booth_id = str(uuid.uuid4())
        date = "2023-01-01"
        frame_color = "test"
        participants = 1
        camera_shot = "test"
        concept_ids = [concept.id]
        goods_amount = True
        curl_amount = True
        is_public = True

        with pytest.raises(NotFoundException) as e:
            self.review_service.create_review(
                main_thumbnail_image_url=main_thumbnail_image_url,
                image_urls=image_urls,
                content=content,
                photo_booth_id=photo_booth_id,
                date=date,
                frame_color=frame_color,
                participants=participants,
                camera_shot=camera_shot,
                concept_ids=concept_ids,
                goods_amount=goods_amount,
                curl_amount=curl_amount,
                is_public=is_public,
                user=valid_user,
            )

        assert e.value.detail == "PhotoBooth does not exist"
        assert e.value.status_code == 404

    def test_create_review_fail_concept_does_not_exist(self, valid_user, concept, photo_booth):
        main_thumbnail_image_url = "https://test.com/test.jpg"
        image_urls = ["https://test.com/test.jpg", "https://test.com/test.jpg"]
        content = "test"
        photo_booth_id = photo_booth.id
        date = "2023-01-01"
        frame_color = "test"
        participants = 1
        camera_shot = "test"
        concept_ids = [2, 3, 4]
        goods_amount = True
        curl_amount = True
        is_public = True

        with pytest.raises(NotFoundException) as e:
            self.review_service.create_review(
                main_thumbnail_image_url=main_thumbnail_image_url,
                image_urls=image_urls,
                content=content,
                photo_booth_id=photo_booth_id,
                date=date,
                frame_color=frame_color,
                participants=participants,
                camera_shot=camera_shot,
                concept_ids=concept_ids,
                goods_amount=goods_amount,
                curl_amount=curl_amount,
                is_public=is_public,
                user=valid_user,
            )

        assert e.value.detail == "Concept does not exist"
        assert e.value.status_code == 404

    def test_create_review_transaction(self, concept, photo_booth, valid_user):
        main_thumbnail_image_url = "https://test.com/test.jpg"
        image_urls = ["https://test.com/test.jpg", "https://test.com/test.jpg"]
        content = "test"
        photo_booth_id = photo_booth.id
        date = "2023-01-01"
        frame_color = "test"
        participants = 1
        camera_shot = "test"
        concept_ids = [2, 3, 4]
        goods_amount = True
        curl_amount = True
        is_public = True

        with pytest.raises(NotFoundException):
            self.review_service.create_review(
                main_thumbnail_image_url=main_thumbnail_image_url,
                image_urls=image_urls,
                content=content,
                photo_booth_id=photo_booth_id,
                date=date,
                frame_color=frame_color,
                participants=participants,
                camera_shot=camera_shot,
                concept_ids=concept_ids,
                goods_amount=goods_amount,
                curl_amount=curl_amount,
                is_public=is_public,
                user=valid_user,
            )

        assert Review.objects.count() == 0
