from django.urls import path

from dump_in.photo_booths.apis import PhotoBoothBrandListAPI

urlpatterns = [
    path("brands", PhotoBoothBrandListAPI.as_view(), name="photo-booth-brand-list"),
]
