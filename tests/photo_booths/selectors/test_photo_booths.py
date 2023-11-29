import pytest

from dump_in.photo_booths.selectors.photo_booths import PhotoBoothSelector

pytestmark = pytest.mark.django_db


class TestPhotoBoothSelector:
    def setup_method(self):
        self.photo_booth_selector = PhotoBoothSelector()

    def test_get_photo_booth_by_id_success(self, photo_booth):
        photo_booth_id = 1
        photo_booth = self.photo_booth_selector.get_photo_booth_by_id(photo_booth_id)
        assert photo_booth.id == photo_booth_id

    def test_get_photo_booth_by_id_fail_does_not_exist(self):
        photo_booth_id = 1
        photo_booth = self.photo_booth_selector.get_photo_booth_by_id(photo_booth_id)
        assert photo_booth is None