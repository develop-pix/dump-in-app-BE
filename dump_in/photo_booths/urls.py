from django.urls import path

from dump_in.photo_booths.apis import (  # PhotoBoothDetailAPI,
    PhotoBoothBrandListAPI,
    PhotoBoothLocationSearchAPI,
)

urlpatterns = [
    path("brands", PhotoBoothBrandListAPI.as_view(), name="photo-booth-brand-list"),
    path("locations/search", PhotoBoothLocationSearchAPI.as_view(), name="photo-booth-location-search")
    # path("<str:photo_booth_id>", PhotoBoothDetailAPI.as_view(), name="photo-booth-detail"),
]
