import uuid

import pytest

from dump_in.photo_booths.selectors.photo_booths import PhotoBoothSelector

pytestmark = pytest.mark.django_db


class TestGetPhotoBoothById:
    def setup_method(self):
        self.photo_booth_selector = PhotoBoothSelector()

    def test_get_photo_booth_by_id_success(self, photo_booth):
        photo_booth_data = self.photo_booth_selector.get_photo_booth_by_id(photo_booth.id)

        assert str(photo_booth_data.id) == photo_booth.id

    def test_get_photo_booth_by_id_success_user_id_none(self, photo_booth):
        photo_booth_data = self.photo_booth_selector.get_photo_booth_by_id(photo_booth.id)

        assert str(photo_booth_data.id) == photo_booth.id

    def test_get_photo_booth_by_id_fail_does_not_exist(self):
        photo_booth_data = self.photo_booth_selector.get_photo_booth_by_id(uuid.uuid4())

        assert photo_booth_data is None
