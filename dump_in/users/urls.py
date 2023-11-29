from django.urls import path

from dump_in.users.apis import MyReviewAPI, MyReviewLikeAPI, UserDetailAPI

urlpatterns = [
    path("detail", UserDetailAPI.as_view(), name="user-detail"),
    path("reviews", MyReviewAPI.as_view(), name="user-review"),
    path("reviews/likes", MyReviewLikeAPI.as_view(), name="user-review-like"),
]
