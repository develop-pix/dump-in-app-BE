import pytest

from dump_in.events.selectors.events import EventSelector

pytestmark = pytest.mark.django_db


class TestGetEventWithUserInfoById:
    def setup_method(self):
        self.event_selector = EventSelector()

    def test_get_event_with_user_info_by_id_success(self, valid_event, valid_user):
        event = self.event_selector.get_event_with_user_info_by_id(valid_event.id, valid_user.id)

        assert event == valid_event

    def test_get_event_with_user_info_by_id_success_is_liked_true(self, valid_event, valid_user):
        valid_event.user_event_like_logs.add(valid_user)

        event = self.event_selector.get_event_with_user_info_by_id(valid_event.id, valid_user.id)

        assert event.is_liked is True

    def test_get_event_with_user_info_by_id_success_is_liked_false(self, valid_event, valid_user):
        event = self.event_selector.get_event_with_user_info_by_id(valid_event.id, valid_user.id)

        assert event.is_liked is False

    def test_get_event_with_user_info_by_id_fail_does_not_exist(self, valid_event, valid_user):
        event = self.event_selector.get_event_with_user_info_by_id(valid_event.id + 1, valid_user.id)

        assert event is None

    def test_get_event_with_user_info_by_id_fail_private_event(self, private_event, valid_user):
        event = self.event_selector.get_event_with_user_info_by_id(private_event.id, valid_user.id)

        assert event is None

    def test_get_event_with_user_info_by_id_fail_not_event_photo_booth_brand(self, invalid_event, valid_user):
        event = self.event_selector.get_event_with_user_info_by_id(invalid_event.id, valid_user.id)

        assert event is None
