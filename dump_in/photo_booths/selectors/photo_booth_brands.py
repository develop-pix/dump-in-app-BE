from typing import Optional, Tuple

from django.db.models import QuerySet

from dump_in.photo_booths.models import PhotoBoothBrand


class PhotoBoothBrandSelector:
    def get_photo_booth_brand_queryset(self) -> QuerySet[PhotoBoothBrand]:
        return PhotoBoothBrand.objects.all()

    def get_photo_booth_brand_with_by_id(self, photo_booth_brand_id: int) -> Tuple[Optional[PhotoBoothBrand], Optional[list]]:
        try:
            photo_booth_brand = PhotoBoothBrand.objects.filter(id=photo_booth_brand_id).get()

            if photo_booth_brand:
                photo_booth_brand_image = list(photo_booth_brand.photo_booth_brand_image.order_by("-created_at")[:4])

            return photo_booth_brand, photo_booth_brand_image

        except PhotoBoothBrand.DoesNotExist:
            return None, None
