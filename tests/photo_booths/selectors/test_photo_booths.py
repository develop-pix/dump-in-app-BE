import uuid

import pytest

from dump_in.photo_booths.selectors.photo_booths import PhotoBoothSelector

pytestmark = pytest.mark.django_db


class TestPhotoBoothSelector:
    def setup_method(self):
        self.photo_booth_selector = PhotoBoothSelector()

    def test_get_photo_booth_by_id_success(self, photo_booth):
        photo_booth = self.photo_booth_selector.get_photo_booth_by_id(photo_booth.id)
        assert photo_booth.id is not None

    def test_get_photo_booth_by_id_fail_does_not_exist(self):
        photo_booth_id = uuid.uuid4().hex
        photo_booth = self.photo_booth_selector.get_photo_booth_by_id(photo_booth_id)
        assert photo_booth is None
