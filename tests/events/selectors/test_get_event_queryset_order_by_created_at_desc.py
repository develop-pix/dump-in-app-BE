import pytest

from dump_in.events.selectors.events import EventSelector

pytestmark = pytest.mark.django_db


class TestGetEventQuerysetOrderByCreatedAtDesc:
    def setup_method(self):
        self.event_selector = EventSelector()

    def test_get_event_queryset_order_by_created_at_desc_success(self, valid_event_list):
        event_queryset = self.event_selector.get_event_queryset_order_by_created_at_desc()

        sorted_event_list = sorted(valid_event_list, key=lambda x: x.created_at, reverse=True)

        assert event_queryset.count() == len(sorted_event_list)
        assert event_queryset[0].created_at == sorted_event_list[0].created_at
        assert event_queryset[1].created_at == sorted_event_list[1].created_at
        assert event_queryset[2].created_at == sorted_event_list[2].created_at

    def test_get_event_queryset_order_by_created_at_desc_fail_does_not_exist(self):
        event_queryset = self.event_selector.get_event_queryset_order_by_created_at_desc()

        assert event_queryset.count() == 0
