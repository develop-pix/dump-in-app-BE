import pytest

from dump_in.common.exception.exceptions import (
    NotFoundException,
    PermissionDeniedException,
    ValidationException,
)
from dump_in.reviews.services.reviews import ReviewService


class TestReviewService:
    def setup_method(self):
        self.review_service = ReviewService()

    def test_create_review_success(self, new_users, photo_booth, concept):
        review = self.review_service.create_review(
            image_urls=["test1", "test2", "test3"],
            content="test_content",
            photo_booth_id=photo_booth.id,
            date="2021-01-01",
            frame_color="test",
            participants=2,
            camera_shot="test",
            concept_ids=[concept.id],
            goods_amount=True,
            curl_amount=True,
            is_public=True,
            user=new_users,
        )

        assert review.content == "test_content"
        assert str(review.photo_booth_id) == photo_booth.id
        assert review.date == "2021-01-01"
        assert review.frame_color == "test"
        assert review.participants == 2
        assert review.camera_shot == "test"
        assert review.goods_amount is True
        assert review.curl_amount is True
        assert review.is_public is True
        assert review.user_id == new_users.id
        assert review.concepts.all().count() == 1
        assert review.review_images.all().count() == 3

    def test_create_review_fail_image_urls_list_many(self, new_users, photo_booth, concept):
        with pytest.raises(ValidationException) as e:
            self.review_service.create_review(
                image_urls=["test1", "test2", "test3", "test4", "test5", "test6"],
                content="test_content",
                photo_booth_id=photo_booth.id,
                date="2021-01-01",
                frame_color="test",
                participants=2,
                camera_shot="test",
                concept_ids=[concept.id],
                goods_amount=True,
                curl_amount=True,
                is_public=True,
                user=new_users,
            )

        assert e.value.status_code == 400
        assert e.value.detail == "Image urls must be less than 5"

    def test_create_review_fail_photo_booth_does_not_exist(self, new_users, concept):
        with pytest.raises(NotFoundException) as e:
            self.review_service.create_review(
                image_urls=["test1", "test2", "test3"],
                content="test_content",
                photo_booth_id=999,
                date="2021-01-01",
                frame_color="test",
                participants=2,
                camera_shot="test",
                concept_ids=[concept.id],
                goods_amount=True,
                curl_amount=True,
                is_public=True,
                user=new_users,
            )

        assert e.value.status_code == 404
        assert e.value.detail == "PhotoBooth does not exist"

    def test_update_review_success(self, photo_booth, concept, review):
        review = self.review_service.update_review(
            review_id=review.id,
            image_urls=["test1", "test2", "test3"],
            content="test_content",
            photo_booth_id=photo_booth.id,
            date="2021-01-01",
            frame_color="test",
            participants=2,
            camera_shot="test",
            concept_ids=[concept.id],
            goods_amount=True,
            curl_amount=True,
            is_public=True,
            user=review.user,
        )
        assert review.content == "test_content"
        assert str(review.photo_booth_id) == photo_booth.id
        assert review.date == "2021-01-01"
        assert review.frame_color == "test"
        assert review.participants == 2
        assert review.camera_shot == "test"
        assert review.goods_amount is True
        assert review.curl_amount is True
        assert review.is_public is True
        assert review.user_id == review.user.id
        assert review.concepts.all().count() == 1

    def test_update_review_fail_image_urls_list_many(self, photo_booth, concept, review):
        with pytest.raises(ValidationException) as e:
            review = self.review_service.update_review(
                review_id=review.id,
                image_urls=["test1", "test2", "test3", "test4", "test5", "test6"],
                content="test_content",
                photo_booth_id=photo_booth.id,
                date="2021-01-01",
                frame_color="test",
                participants=2,
                camera_shot="test",
                concept_ids=[concept.id],
                goods_amount=True,
                curl_amount=True,
                is_public=True,
                user=review.user,
            )

        assert e.value.status_code == 400
        assert e.value.detail == "Image urls must be less than 5"

    def test_update_review_fail_photo_booth_does_not_exist(self, concept, review):
        with pytest.raises(NotFoundException) as e:
            review = self.review_service.update_review(
                review_id=review.id,
                image_urls=["test1", "test2", "test3"],
                content="test_content",
                photo_booth_id=999,
                date="2021-01-01",
                frame_color="test",
                participants=2,
                camera_shot="test",
                concept_ids=[concept.id],
                goods_amount=True,
                curl_amount=True,
                is_public=True,
                user=review.user,
            )

        assert e.value.status_code == 404
        assert e.value.detail == "PhotoBooth does not exist"

    def test_update_review_fail_review_does_not_exist(self, photo_booth, review, concept):
        with pytest.raises(NotFoundException) as e:
            review = self.review_service.update_review(
                review_id=100,
                image_urls=["test1", "test2", "test3"],
                content="test_content",
                photo_booth_id=photo_booth.id,
                date="2021-01-01",
                frame_color="test",
                participants=2,
                camera_shot="test",
                concept_ids=[concept.id],
                goods_amount=True,
                curl_amount=True,
                is_public=True,
                user=review.user,
            )

        assert e.value.status_code == 404
        assert e.value.detail == "Review does not exist"

    def test_update_review_fail_user_permission_denied(self, photo_booth, concept, review, new_users):
        with pytest.raises(PermissionDeniedException) as e:
            review = self.review_service.update_review(
                review_id=review.id,
                image_urls=["test1", "test2", "test3"],
                content="test_content",
                photo_booth_id=photo_booth.id,
                date="2021-01-01",
                frame_color="test",
                participants=2,
                camera_shot="test",
                concept_ids=[concept.id],
                goods_amount=True,
                curl_amount=True,
                is_public=True,
                user=new_users,
            )

        assert e.value.status_code == 403
        assert e.value.detail == "Permission denied"

    def test_soft_delete_review_success(self, review):
        review = self.review_service.soft_delete_review(
            review_id=review.id,
            user=review.user,
        )

        assert review.is_deleted is True

    def test_soft_delete_review_fail_review_does_not_exist(self, review):
        with pytest.raises(NotFoundException) as e:
            review = self.review_service.soft_delete_review(
                review_id=100,
                user=review.user,
            )

        assert e.value.status_code == 404
        assert e.value.detail == "Review does not exist"

    def test_soft_delete_review_fail_user_permission_denied(self, review, new_users):
        with pytest.raises(PermissionDeniedException) as e:
            review = self.review_service.soft_delete_review(
                review_id=review.id,
                user=new_users,
            )

        assert e.value.status_code == 403
        assert e.value.detail == "Permission denied"

    def test_like_review_success(self, review, new_users):
        review, is_like = self.review_service.like_review(
            review_id=review.id,
            user=new_users,
        )

        assert is_like is True

    def test_like_review_success_already_like(self, review, new_users):
        review.user_review_like_logs.add(new_users)
        review, is_like = self.review_service.like_review(
            review_id=review.id,
            user=new_users,
        )

        assert is_like is False

    def test_like_review_fail_review_does_not_exist(self, review):
        with pytest.raises(NotFoundException) as e:
            review, is_like = self.review_service.like_review(
                review_id=100,
                user=review.user,
            )

        assert e.value.status_code == 404
        assert e.value.detail == "Review does not exist"

    def test_view_count_up_success(self, review):
        review = self.review_service.view_count_up(
            review_id=review.id,
            user=review.user,
        )

        assert review.view_count != 0

    def test_view_count_up_fail_review_does_not_exist(self, review):
        with pytest.raises(NotFoundException) as e:
            review = self.review_service.view_count_up(
                review_id=100,
                user=review.user,
            )

        assert e.value.status_code == 404
        assert e.value.detail == "Review does not exist"

    def test_view_count_up_fail_user_permission_denied(self, review, new_users):
        review.is_public = False
        review.save()

        with pytest.raises(PermissionDeniedException) as e:
            review = self.review_service.view_count_up(
                review_id=review.id,
                user=new_users,
            )

        assert e.value.status_code == 403
        assert e.value.detail == "Permission denied"
