import pytest

from dump_in.photo_booths.selectors.photo_booth_brands import PhotoBoothBrandSelector

pytestmark = pytest.mark.django_db


class TestGetPhotoBoothBrandQueryset:
    def setup_method(self):
        self.photo_booth_brand_selector = PhotoBoothBrandSelector()

    def test_get_photo_booth_brand_queryset_success(self, photo_booth_brand_list):
        photo_booth_brands = self.photo_booth_brand_selector.get_photo_booth_brand_queryset()

        assert photo_booth_brands.count() == 3

    def test_get_photo_booth_brand_queryset_fail_does_not_exist(self):
        photo_booth_brands = self.photo_booth_brand_selector.get_photo_booth_brand_queryset()

        assert photo_booth_brands.count() == 0
