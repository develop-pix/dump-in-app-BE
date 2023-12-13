from django.db.models import QuerySet

from dump_in.photo_booths.models import PhotoBoothBrand


class PhotoBoothBrandSelector:
    def get_photo_booth_brand_queryset(self) -> QuerySet[PhotoBoothBrand]:
        return PhotoBoothBrand.objects.all()
