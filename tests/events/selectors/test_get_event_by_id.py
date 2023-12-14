import pytest

from dump_in.events.selectors.events import EventSelector

pytestmark = pytest.mark.django_db


class TestGetEventById:
    def setup_method(self):
        self.event_selector = EventSelector()

    def test_get_event_by_id_success(self, valid_event):
        event = self.event_selector.get_event_by_id(valid_event.id)

        assert event == valid_event

    def test_get_event_by_id_fail_does_not_exist(self, valid_event):
        event = self.event_selector.get_event_by_id(valid_event.id + 1)

        assert event is None

    def test_get_event_by_id_fail_private_event(self, private_event):
        event = self.event_selector.get_event_by_id(private_event.id)

        assert event is None

    def test_get_event_by_id_fail_not_event_photo_booth_brand(self, invalid_event):
        event = self.event_selector.get_event_by_id(invalid_event.id)

        assert event is None
