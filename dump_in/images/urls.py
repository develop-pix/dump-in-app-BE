from django.urls import path

from dump_in.images.apis import ImageUploadAPI

urlpatterns = [
    path("upload", ImageUploadAPI.as_view(), name="upload"),
]
