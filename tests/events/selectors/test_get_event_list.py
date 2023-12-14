import time

import pytest
from django.db.models import BooleanField, Case, When

from dump_in.events.models import Event
from dump_in.events.selectors.events import EventSelector

pytestmark = pytest.mark.django_db


class TestGetEventList:
    def setup_method(self):
        self.event_selector = EventSelector()

    def test_get_event_list_success(self, valid_event_list, valid_user):
        event_list = self.event_selector.get_event_list({}, valid_user)

        assert event_list.count() == 100

    def test_get_event_list_success_is_liked_true(self, valid_event, valid_user):
        valid_event.user_event_like_logs.add(valid_user)

        event_list = self.event_selector.get_event_list({}, valid_user)

        assert event_list.count() == 1
        assert event_list.first().is_liked is True

    def test_get_event_list_success_is_liked_false(self, valid_event, valid_user):
        event_list = self.event_selector.get_event_list({}, valid_user)

        assert event_list.count() == 1
        assert event_list.first().is_liked is False

    def test_get_event_list_success_with_hashtag(self, valid_event, valid_user):
        hashtag = valid_event.hashtag.first()

        event_list = self.event_selector.get_event_list({"hashtag": str(hashtag.id)}, valid_user)

        assert event_list.count() == 1

    def test_get_event_list_fail_does_not_exist(self, valid_user):
        event_list = self.event_selector.get_event_list({}, valid_user)

        assert list(event_list) == []

    def test_get_event_list_fail_private_event(self, private_event, valid_user):
        event_list = self.event_selector.get_event_list({}, valid_user)

        assert list(event_list) == []

    def test_get_event_list_fail_not_event_photo_booth_brand(self, invalid_event, valid_user):
        event_list = self.event_selector.get_event_list({}, valid_user)

        assert list(event_list) == []

    def test_get_event_list_fail_invalid_hashtag(self, valid_event, valid_user):
        event_list = self.event_selector.get_event_list({"hashtag": "99999"}, valid_user)

        assert list(event_list) == []

    def test_get_event_list_select_related_performance(self, valid_event_list, valid_user):
        start_time = time.time()

        event_list = Event.objects.annotate(
            is_liked=Case(
                When(usereventlikelog__user=valid_user, then=True),
                default=False,
                output_field=BooleanField(),
            ),
        ).filter(is_public=True, photo_booth_brand__is_event=True)

        for event in event_list:
            event.photo_booth_brand.name
            event.photo_booth_brand.description
            event.photo_booth_brand.photo_booth_url
            event.photo_booth_brand.logo_image_url
            event.photo_booth_brand.main_thumbnail_image_url
            event.photo_booth_brand.is_event

        end_time = time.time()

        time_with_filter = end_time - start_time

        start_time = time.time()

        event_list = self.event_selector.get_event_list({}, valid_user)

        for event in event_list:
            event.photo_booth_brand.name
            event.photo_booth_brand.description
            event.photo_booth_brand.photo_booth_url
            event.photo_booth_brand.logo_image_url
            event.photo_booth_brand.main_thumbnail_image_url
            event.photo_booth_brand.is_event

        end_time = time.time()

        time_with_select_related = end_time - start_time

        assert time_with_filter > time_with_select_related
