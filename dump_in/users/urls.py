from django.urls import path

from dump_in.users.apis import (
    MyEventLikeAPI,
    MyPhotoBoothLikeAPI,
    MyReviewAPI,
    MyReviewLikeAPI,
    NotificationCheckAPI,
    NotificationDetailAPI,
    NotificationListAPI,
    UserDetailAPI,
    UserMobileTokenAPI,
)

urlpatterns = [
    path("detail", UserDetailAPI.as_view(), name="user-detail"),
    path("reviews", MyReviewAPI.as_view(), name="user-review-list"),
    path("reviews/likes", MyReviewLikeAPI.as_view(), name="user-review-like-list"),
    path("photo-booths/likes", MyPhotoBoothLikeAPI.as_view(), name="user-photo-booth-like-list"),
    path("events/likes", MyEventLikeAPI.as_view(), name="user-event-like-list"),
    path("notifications", NotificationListAPI.as_view(), name="user-notification-list"),
    path("notifications/check", NotificationCheckAPI.as_view(), name="user-notification-check"),
    path("notifications/<int:notification_id>", NotificationDetailAPI.as_view(), name="user-notification-detail"),
    path("mobile-token", UserMobileTokenAPI.as_view(), name="user-mobile-token"),
]
