from django.urls import path

from dump_in.photo_booths.apis import (
    PhotoBoothBrandDetailAPI,
    PhotoBoothBrandEventListAPI,
    PhotoBoothBrandListAPI,
    PhotoBoothBrandReviewListAPI,
    PhotoBoothDetailAPI,
    PhotoBoothLikeAPI,
    PhotoBoothLocationListAPI,
    PhotoBoothLocationSearchAPI,
    PhotoBoothReviewListAPI,
)

urlpatterns = [
    path("/brands", PhotoBoothBrandListAPI.as_view(), name="photo-booth-brand-list"),
    path("/brands/<int:photo_booth_brand_id>", PhotoBoothBrandDetailAPI.as_view(), name="photo-booth-brand-detail"),
    path("/brands/<int:photo_booth_brand_id>/events", PhotoBoothBrandEventListAPI.as_view(), name="photo-booth-brand-event-list"),
    path("/brands/<int:photo_booth_brand_id>/reviews", PhotoBoothBrandReviewListAPI.as_view(), name="photo-booth-brand-review-list"),
    path("/locations/search", PhotoBoothLocationSearchAPI.as_view(), name="photo-booth-location-search"),
    path("/locations", PhotoBoothLocationListAPI.as_view(), name="photo-booth-location-list"),
    path("/<str:photo_booth_id>", PhotoBoothDetailAPI.as_view(), name="photo-booth-detail"),
    path("/<str:photo_booth_id>/likes", PhotoBoothLikeAPI.as_view(), name="photo-booth-like"),
    path("/<str:photo_booth_id>/reviews", PhotoBoothReviewListAPI.as_view(), name="photo-booth-review-list"),
]
