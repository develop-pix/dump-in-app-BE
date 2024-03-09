import pytest

from dump_in.events.selectors.events import EventSelector

pytestmark = pytest.mark.django_db


class TestGetEventQuerysetByPhotoBoothBrandIdOrderbyCreatedAtDesc:
    def setup_method(self):
        self.event_selector = EventSelector()

    def test_get_event_queryset_by_photo_booth_brand_id_order_by_created_at_desc_success_single_event(self, valid_event, valid_user):
        event_queryset = self.event_selector.get_event_queryset_by_photo_booth_brand_id_order_by_created_at_desc(
            valid_event.photo_booth_brand_id, valid_user
        )

        assert event_queryset.first() == valid_event

    def test_get_event_queryset_by_photo_booth_brand_id_order_by_created_at_desc_success_multiple_event(self, valid_event_list, valid_user):
        event_queryset = self.event_selector.get_event_queryset_by_photo_booth_brand_id_order_by_created_at_desc(
            valid_event_list[0].photo_booth_brand_id, valid_user
        )

        sorted_valid_event_list = sorted(valid_event_list, key=lambda event: event.created_at, reverse=True)

        assert event_queryset.count() == len(valid_event_list)
        assert event_queryset[0] == sorted_valid_event_list[0]
        assert event_queryset[1] == sorted_valid_event_list[1]
        assert event_queryset[2] == sorted_valid_event_list[2]

    def test_get_event_queryset_by_photo_booth_brand_id_order_by_created_at_desc_success_is_liked_true(self, valid_event, valid_user):
        valid_event.user_event_like_logs.add(valid_user)

        event_queryset = self.event_selector.get_event_queryset_by_photo_booth_brand_id_order_by_created_at_desc(
            valid_event.photo_booth_brand_id, valid_user
        )

        assert event_queryset.first() == valid_event
        assert event_queryset.first().is_liked is True

    def test_get_event_queryset_by_photo_booth_brand_id_order_by_created_at_desc_success_is_liked_false(self, valid_event, valid_user):
        event_queryset = self.event_selector.get_event_queryset_by_photo_booth_brand_id_order_by_created_at_desc(
            valid_event.photo_booth_brand_id, valid_user
        )

        assert event_queryset.first() == valid_event
        assert event_queryset.first().is_liked is False

    def test_get_event_queryset_by_photo_booth_brand_id_order_by_created_at_desc_success_anonymous_user(self, valid_event, inactive_user):
        event_queryset = self.event_selector.get_event_queryset_by_photo_booth_brand_id_order_by_created_at_desc(
            valid_event.photo_booth_brand_id, inactive_user
        )

        assert event_queryset.first() == valid_event

    def test_get_event_queryset_by_photo_booth_brand_id_order_by_created_at_desc_fail_does_not_exist(self, valid_event, valid_user):
        event_queryset = self.event_selector.get_event_queryset_by_photo_booth_brand_id_order_by_created_at_desc(
            valid_event.photo_booth_brand_id + 1, valid_user
        )

        assert event_queryset.count() == 0

    def test_get_event_queryset_by_photo_booth_brand_id_order_by_created_at_desc_fail_private_event(self, private_event, valid_user):
        event_queryset = self.event_selector.get_event_queryset_by_photo_booth_brand_id_order_by_created_at_desc(
            private_event.photo_booth_brand_id, valid_user
        )

        assert event_queryset.count() == 0

    def test_get_event_queryset_by_photo_booth_brand_id_order_by_created_at_desc_fail_not_event_photo_booth_brand(
        self, invalid_event, valid_user
    ):
        event_queryset = self.event_selector.get_event_queryset_by_photo_booth_brand_id_order_by_created_at_desc(
            invalid_event.photo_booth_brand_id, valid_user
        )

        assert event_queryset.count() == 0
