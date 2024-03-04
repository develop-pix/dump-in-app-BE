from django.urls import path

from dump_in.events.apis import EventDetailAPI, EventHomeAPI, EventLikeAPI, EventListAPI

urlpatterns = [
    path("", EventListAPI.as_view(), name="event-list"),
    path("/home", EventHomeAPI.as_view(), name="event-home"),
    path("/<int:event_id>", EventDetailAPI.as_view(), name="event-detail"),
    path("/<int:event_id>/likes", EventLikeAPI.as_view(), name="event-like"),
]
