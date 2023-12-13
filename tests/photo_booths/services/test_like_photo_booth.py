import concurrent.futures
import uuid

import pytest

from dump_in.common.exception.exceptions import NotFoundException
from dump_in.photo_booths.services.photo_booths import PhotoBoothService


class TestLikePhotoBooth:
    def setup_method(self):
        self.photo_booth_service = PhotoBoothService()

    def test_like_photo_booth_success(self, photo_booth, valid_user):
        photo_booth, is_like = self.photo_booth_service.like_photo_booth(
            photo_booth_id=photo_booth.id,
            user=valid_user,
        )

        assert is_like is True

    def test_like_photo_booth_success_already_like(self, photo_booth, valid_user):
        photo_booth.user_photo_booth_like_logs.add(valid_user)
        photo_booth, is_like = self.photo_booth_service.like_photo_booth(
            photo_booth_id=photo_booth.id,
            user=valid_user,
        )

        assert is_like is False

    @pytest.mark.django_db(transaction=True)
    def test_like_photo_booth_success_concurrency(self, photo_booth, inactive_user, valid_user):
        before_photo_booth_like_count = photo_booth.like_count
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            future1 = executor.submit(self.photo_booth_service.like_photo_booth, photo_booth.id, valid_user)
            future2 = executor.submit(self.photo_booth_service.like_photo_booth, photo_booth.id, inactive_user)

            result1 = future1.result()
            result2 = future2.result()

        result1_photo_booth, result1_is_like = result1
        result2_photo_booth, result2_is_like = result2

        assert result1_is_like is True
        assert result2_is_like is True

        photo_booth.refresh_from_db()
        assert before_photo_booth_like_count + 2 == photo_booth.like_count

        self.photo_booth_service.like_photo_booth(photo_booth.id, valid_user)
        photo_booth.refresh_from_db()
        assert before_photo_booth_like_count + 1 == photo_booth.like_count

    def test_like_photo_booth_fail_photo_booth_does_not_exist(self, photo_booth, valid_user):
        with pytest.raises(NotFoundException) as e:
            self.photo_booth_service.like_photo_booth(
                photo_booth_id=uuid.uuid4(),
                user=valid_user,
            )

        assert e.value.status_code == 404
        assert e.value.detail == "Photo Booth does not exist"
