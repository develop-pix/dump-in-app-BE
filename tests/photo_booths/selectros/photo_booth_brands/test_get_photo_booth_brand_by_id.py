import pytest

from dump_in.photo_booths.selectors.photo_booth_brands import PhotoBoothBrandSelector

pytestmark = pytest.mark.django_db


class TestGetPhotoBoothBrandById:
    def setup_method(self):
        self.photo_booth_brand_selector = PhotoBoothBrandSelector()

    def test_get_photo_booth_brand_by_id_success(self, photo_booth_brand):
        photo_booth_brand_data = self.photo_booth_brand_selector.get_photo_booth_brand_by_id(photo_booth_brand.id)

        assert photo_booth_brand_data == photo_booth_brand

    def test_get_photo_booth_brand_by_id_fail_does_not_exist(self, photo_booth_brand):
        photo_booth_brand = self.photo_booth_brand_selector.get_photo_booth_brand_by_id(99999)

        assert photo_booth_brand is None
