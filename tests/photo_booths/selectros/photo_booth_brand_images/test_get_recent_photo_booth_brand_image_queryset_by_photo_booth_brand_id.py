import pytest

from dump_in.photo_booths.selectors.photo_booth_brand_images import (
    PhotoBoothBrandImageSelector,
)

pytestmark = pytest.mark.django_db


class TestGetRecentPhotoBoothBrandImageQuerysetByPhotoBoothBrandId:
    def setup_method(self):
        self.photo_booth_brand_image_selector = PhotoBoothBrandImageSelector()

    def test_get_recent_photo_booth_brand_image_queryset_by_photo_booth_brand_id_success_multiple_photo_booth_brand_image(
        self, photo_booth_brand_image_list
    ):
        photo_booth_brand_image_queryset = (
            self.photo_booth_brand_image_selector.get_recent_photo_booth_brand_image_queryset_by_photo_booth_brand_id(
                photo_booth_brand_image_list[0].photo_booth_brand_id
            )
        )

        assert photo_booth_brand_image_queryset.count() == 4

    def test_get_recent_photo_booth_brand_image_queryset_by_photo_booth_brand_id_success_single_photo_booth_brand_image(
        self, photo_booth_brand_image
    ):
        photo_booth_brand_image_queryset = (
            self.photo_booth_brand_image_selector.get_recent_photo_booth_brand_image_queryset_by_photo_booth_brand_id(
                photo_booth_brand_image.photo_booth_brand_id
            )
        )

        assert photo_booth_brand_image_queryset.first() == photo_booth_brand_image

    def test_get_recent_photo_booth_brand_image_queryset_by_photo_booth_brand_id_fail_does_not_exist(self):
        photo_booth_brand_image_queryset = (
            self.photo_booth_brand_image_selector.get_recent_photo_booth_brand_image_queryset_by_photo_booth_brand_id(99999)
        )

        assert photo_booth_brand_image_queryset.count() == 0
