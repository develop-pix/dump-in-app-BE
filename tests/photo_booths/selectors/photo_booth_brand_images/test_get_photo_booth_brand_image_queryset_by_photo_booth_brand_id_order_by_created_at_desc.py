import pytest

from dump_in.photo_booths.selectors.photo_booth_brand_images import (
    PhotoBoothBrandImageSelector,
)

pytestmark = pytest.mark.django_db


class TestGetPhotoBoothBrandImageQuerySetByPhotoBoothBrandIdOrderByCreatedAtDesc:
    def setup_method(self):
        self.photo_booth_brand_image_selector = PhotoBoothBrandImageSelector()

    def test_get_photo_booth_brand_image_queryset_by_photo_booth_brand_id_order_by_created_at_desc_success_multiple_photo_booth_brand_image(
        self, photo_booth_brand_image_list
    ):
        photo_booth_brand_image_queryset = (
            self.photo_booth_brand_image_selector.get_photo_booth_brand_image_queryset_by_photo_booth_brand_id_order_by_created_at_desc(
                photo_booth_brand_image_list[0].photo_booth_brand_id
            )
        )

        sorted_photo_booth_brand_image_list = sorted(
            photo_booth_brand_image_list, key=lambda photo_booth_brand_image: photo_booth_brand_image.created_at, reverse=True
        )

        assert photo_booth_brand_image_queryset.count() == len(photo_booth_brand_image_list)
        assert photo_booth_brand_image_queryset[0] == sorted_photo_booth_brand_image_list[0]
        assert photo_booth_brand_image_queryset[1] == sorted_photo_booth_brand_image_list[1]
        assert photo_booth_brand_image_queryset[2] == sorted_photo_booth_brand_image_list[2]

    def test_get_photo_booth_brand_image_queryset_by_photo_booth_brand_id_order_by_created_at_desc_success_single_photo_booth_brand_image(
        self, photo_booth_brand_image
    ):
        photo_booth_brand_image_queryset = (
            self.photo_booth_brand_image_selector.get_photo_booth_brand_image_queryset_by_photo_booth_brand_id_order_by_created_at_desc(
                photo_booth_brand_image.photo_booth_brand_id
            )
        )

        assert photo_booth_brand_image_queryset.first() == photo_booth_brand_image

    def test_get_photo_booth_brand_image_queryset_by_photo_booth_brand_id_order_by_created_at_desc_fail_does_not_exist(self):
        photo_booth_brand_image_queryset = (
            self.photo_booth_brand_image_selector.get_photo_booth_brand_image_queryset_by_photo_booth_brand_id_order_by_created_at_desc(
                99999
            )
        )

        assert photo_booth_brand_image_queryset.count() == 0
