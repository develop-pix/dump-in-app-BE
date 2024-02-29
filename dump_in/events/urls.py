from django.urls import path

from dump_in.events.apis import EventDetailAPI, EventLikeAPI, EventListAPI

urlpatterns = [
    path("", EventListAPI.as_view(), name="event-list"),
    path("/<int:event_id>", EventDetailAPI.as_view(), name="event-detail"),
    path("/<int:event_id>/likes", EventLikeAPI.as_view(), name="event-like"),
]
