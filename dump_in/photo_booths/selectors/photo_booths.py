from typing import Optional

from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance
from django.db.models import QuerySet

from dump_in.photo_booths.models import PhotoBooth


class PhotoBoothSelector:
    def get_photo_booth_by_id(self, photo_booth_id: str) -> Optional[PhotoBooth]:
        try:
            return PhotoBooth.objects.filter(id=photo_booth_id).get()
        except PhotoBooth.DoesNotExist:
            return None

    def get_nearby_photo_booth_queryset_by_photo_booth_brand_name(
        self, center_point: Point, radius: int, photo_booth_brand_name: str
    ) -> QuerySet[PhotoBooth]:
        return PhotoBooth.objects.select_related("photo_booth_brand").filter(
            point__distance_lte=(center_point, Distance(km=radius)),
            photo_booth_brand__name__icontains=photo_booth_brand_name,
        )
