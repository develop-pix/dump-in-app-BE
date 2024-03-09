from typing import Tuple

from django.db import transaction
from django.db.models import F

from dump_in.common.exception.exceptions import NotFoundException
from dump_in.events.models import Event
from dump_in.events.selectors.events import EventSelector


class EventService:
    def __init__(self):
        self.event_selector = EventSelector()

    @transaction.atomic
    def like_event(self, event_id: int, user) -> Tuple[Event, bool]:
        event = self.event_selector.get_event_by_id(event_id=event_id)

        if event is None:
            raise NotFoundException("Event does not exist")

        if event.user_event_like_logs.filter(id=user.id).exists():
            event.user_event_like_logs.remove(user)
            event.like_count = F("like_count") - 1
            is_liked = False

        else:
            event.user_event_like_logs.add(user)
            event.like_count = F("like_count") + 1
            is_liked = True

        event.save(update_fields=["like_count"])

        return event, is_liked
