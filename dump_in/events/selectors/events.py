from typing import Optional, Union

from django.contrib.auth.models import AnonymousUser
from django.db.models import BooleanField, Case, When
from django.db.models.query import QuerySet

from dump_in.events.filters import EventFilter
from dump_in.events.models import Event
from dump_in.users.models import User


class EventSelector:
    def get_event_by_id(self, event_id: int) -> Optional[Event]:
        try:
            return Event.objects.filter(id=event_id, is_public=True, photo_booth_brand__is_event=True).get()
        except Event.DoesNotExist:
            return None

    def get_event_queryset_order_by_created_at_desc(self) -> QuerySet[Event]:
        return Event.objects.filter(is_public=True, photo_booth_brand__is_event=True).order_by("-created_at")

    def get_event_with_user_info_by_id(self, event_id: int, user: Union[User, AnonymousUser]) -> Optional[Event]:
        try:
            qs = Event.objects.filter(id=event_id, is_public=True, photo_booth_brand__is_event=True)

            if user.is_authenticated:
                like_id_list = user.usereventlikelog_set.values_list("event_id", flat=True)

                qs = qs.annotate(
                    is_liked=Case(
                        When(id__in=like_id_list, then=True),
                        default=False,
                        output_field=BooleanField(),
                    ),
                )

            return qs.get()
        except Event.DoesNotExist:
            return None

    def get_event_queryset_by_photo_booth_brand_id_order_by_created_at_desc(
        self, photo_booth_brand_id: int, user: Union[User, AnonymousUser]
    ) -> QuerySet[Event]:
        qs = Event.objects.filter(photo_booth_brand_id=photo_booth_brand_id, is_public=True, photo_booth_brand__is_event=True).order_by(
            "-created_at"
        )

        if user.is_authenticated:
            like_id_list = user.usereventlikelog_set.values_list("event_id", flat=True)

            qs = qs.annotate(
                is_liked=Case(
                    When(id__in=like_id_list, then=True),
                    default=False,
                    output_field=BooleanField(),
                ),
            )
        return qs

    def get_event_queryset_by_user_like(self, user_id) -> QuerySet[Event]:
        return Event.objects.filter(usereventlikelog__user_id=user_id, is_public=True, photo_booth_brand__is_event=True)

    def get_event_list(self, filters: Optional[dict], user: Union[User, AnonymousUser]) -> QuerySet[Event]:
        filters = filters or {}

        qs = Event.objects.select_related("photo_booth_brand").filter(is_public=True, photo_booth_brand__is_event=True)

        if user.is_authenticated:
            like_id_list = user.usereventlikelog_set.values_list("event_id", flat=True)

            qs = qs.annotate(
                is_liked=Case(
                    When(id__in=like_id_list, then=True),
                    default=False,
                    output_field=BooleanField(),
                )
            )

        return EventFilter(data=filters, queryset=qs).qs
