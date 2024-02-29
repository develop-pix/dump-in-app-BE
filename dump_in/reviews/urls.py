from django.urls import path

from dump_in.reviews.apis import (
    ReviewDetailAPI,
    ReviewLikeAPI,
    ReviewListAPI,
    ReviewListCountAPI,
    ReviewPhotoBoothLocationSearchAPI,
)

urlpatterns = [
    path("", ReviewListAPI.as_view(), name="review-list"),
    path("/count", ReviewListCountAPI.as_view(), name="review-list-count"),
    path("/<int:review_id>", ReviewDetailAPI.as_view(), name="review-detail"),
    path("/<int:review_id>/likes", ReviewLikeAPI.as_view(), name="review-like"),
    path("/photo-booths/locations/search", ReviewPhotoBoothLocationSearchAPI.as_view(), name="review-photo-booth-location-search"),
]
