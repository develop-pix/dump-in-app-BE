import pytest

from dump_in.events.selectors.events import EventSelector

pytestmark = pytest.mark.django_db


class TestGetEventList:
    def setup_method(self):
        self.event_selector = EventSelector()

    def test_get_event_list_success_single_event(self, valid_event, valid_user):
        event_list = self.event_selector.get_event_list({}, valid_user)

        assert event_list.first() == valid_event

    def test_get_event_list_success_multiple_event(self, valid_event_list, valid_user):
        event_list = self.event_selector.get_event_list({}, valid_user)

        assert event_list.count() == len(valid_event_list)

    def test_get_event_list_success_is_liked_true(self, valid_event, valid_user):
        valid_event.user_event_like_logs.add(valid_user)

        event_list = self.event_selector.get_event_list({}, valid_user)

        assert event_list.first() == valid_event
        assert event_list.first().is_liked is True

    def test_get_event_list_success_is_liked_false(self, valid_event, valid_user):
        event_list = self.event_selector.get_event_list({}, valid_user)

        assert event_list.first() == valid_event
        assert event_list.first().is_liked is False

    def test_get_event_list_success_with_hashtag(self, valid_event, valid_user):
        hashtag_name = [valid_event.hashtag.first().name]

        event_list = self.event_selector.get_event_list({"hashtag": hashtag_name}, valid_user)

        assert event_list.first() == valid_event

    def test_get_event_list_success_anonymous_user(self, valid_event, inactive_user):
        event_list = self.event_selector.get_event_list({}, inactive_user)

        assert event_list.first() == valid_event

    def test_get_event_list_fail_does_not_exist(self, valid_user):
        event_list = self.event_selector.get_event_list({}, valid_user)

        assert event_list.count() == 0

    def test_get_event_list_fail_private_event(self, private_event, valid_user):
        event_list = self.event_selector.get_event_list({}, valid_user)

        assert event_list.count() == 0

    def test_get_event_list_fail_not_event_photo_booth_brand(self, invalid_event, valid_user):
        event_list = self.event_selector.get_event_list({}, valid_user)

        assert event_list.count() == 0

    def test_get_event_list_fail_invalid_hashtag(self, valid_event, valid_user):
        event_list = self.event_selector.get_event_list({"hashtag": "string"}, valid_user)

        assert event_list.count() == 0
