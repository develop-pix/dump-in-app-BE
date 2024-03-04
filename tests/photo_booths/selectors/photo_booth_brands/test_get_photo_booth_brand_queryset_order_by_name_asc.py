import pytest

from dump_in.photo_booths.selectors.photo_booth_brands import PhotoBoothBrandSelector

pytestmark = pytest.mark.django_db


class TestGetPhotoBoothBrandQuerysetOrderByNameAsc:
    def setup_method(self):
        self.photo_booth_brand_selector = PhotoBoothBrandSelector()

    def test_get_photo_booth_brand_queryset_order_by_name_asc_success(self, photo_booth_brand_list):
        photo_booth_brand_queryset = self.photo_booth_brand_selector.get_photo_booth_brand_queryset_order_by_name_asc()

        sorted_photo_booth_brand_list = sorted(photo_booth_brand_list, key=lambda x: x.name)

        assert photo_booth_brand_queryset.count() == len(sorted_photo_booth_brand_list)
        assert photo_booth_brand_queryset[0].name == sorted_photo_booth_brand_list[0].name
        assert photo_booth_brand_queryset[1].name == sorted_photo_booth_brand_list[1].name
        assert photo_booth_brand_queryset[2].name == sorted_photo_booth_brand_list[2].name

    def test_get_photo_booth_brand_queryset_order_by_name_asc_fail_does_not_exist(self):
        photo_booth_brand_queryset = self.photo_booth_brand_selector.get_photo_booth_brand_queryset_order_by_name_asc()

        assert photo_booth_brand_queryset.count() == 0
