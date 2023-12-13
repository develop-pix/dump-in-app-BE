import uuid

import pytest

from dump_in.photo_booths.selectors.photo_booths import PhotoBoothSelector

pytestmark = pytest.mark.django_db


class TestGetPhotoBoothWithdUserInfoById:
    def setup_method(self):
        self.photo_booth_selector = PhotoBoothSelector()

    def test_get_photo_booth_with_user_info_by_id_success(self, photo_booth, valid_user):
        photo_booth_data = self.photo_booth_selector.get_photo_booth_with_user_info_by_id(photo_booth.id, valid_user)

        assert str(photo_booth_data.id) == photo_booth.id

    def test_get_photo_booth_with_user_info_by_id_success_is_like_true(self, photo_booth, valid_user):
        photo_booth.user_photo_booth_like_logs.add(valid_user)

        photo_booth_data = self.photo_booth_selector.get_photo_booth_with_user_info_by_id(photo_booth.id, valid_user)

        assert photo_booth_data.is_liked is True

    def test_get_photo_booth_with_user_info_by_id_success_is_like_false(self, photo_booth, valid_user):
        photo_booth_data = self.photo_booth_selector.get_photo_booth_with_user_info_by_id(photo_booth.id, valid_user)

        assert photo_booth_data.is_liked is False

    def test_get_photo_booth_with_user_info_by_id_fail_does_not_exist(self, valid_user):
        photo_booth_data = self.photo_booth_selector.get_photo_booth_with_user_info_by_id(uuid.uuid4(), valid_user)

        assert photo_booth_data == None
