from django.urls import path

from dump_in.users.apis import UserDetailAPI

urlpatterns = [
    path("detail", UserDetailAPI.as_view(), name="user-detail"),
]

