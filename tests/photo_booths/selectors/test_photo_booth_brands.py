import pytest

from dump_in.photo_booths.selectors.photo_booth_brands import PhotoBoothBrandSelector

pytestmark = pytest.mark.django_db


class TestPhotoBoothBrandSelector:
    def setup_method(self):
        self.photo_booth_brand_selector = PhotoBoothBrandSelector()

    def test_get_photo_booth_queryset_success(self, photo_booth_brand):
        photo_booth_queryset = self.photo_booth_brand_selector.get_photo_booth_queryset()

        assert photo_booth_queryset.count() == 3
