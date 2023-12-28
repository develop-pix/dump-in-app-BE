from typing import Optional

from django.db.models import QuerySet

from dump_in.photo_booths.models import PhotoBoothBrand


class PhotoBoothBrandSelector:
    def get_photo_booth_brand_queryset(self) -> QuerySet[PhotoBoothBrand]:
        return PhotoBoothBrand.objects.all()

    def get_photo_booth_brand_by_id(self, photo_booth_brand_id: int) -> Optional[PhotoBoothBrand]:
        try:
            return PhotoBoothBrand.objects.filter(id=photo_booth_brand_id).get()

        except PhotoBoothBrand.DoesNotExist:
            return None
