from django.db.models import QuerySet

from dump_in.photo_booths.models import PhotoBoothBrandImage


class PhotoBoothBrandImageSelector:
    def get_photo_booth_brand_image_queryset_by_photo_booth_brand_id_order_by_created_at_desc(
        self, photo_booth_brand_id: int
    ) -> QuerySet[PhotoBoothBrandImage]:
        return PhotoBoothBrandImage.objects.filter(photo_booth_brand_id=photo_booth_brand_id).order_by("-created_at")
