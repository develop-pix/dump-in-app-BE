from dump_in.events.selectors.events import EventSelector


class TestGetEventQuerysetByUserLike:
    def setup_method(self):
        self.event_selector = EventSelector()

    def test_get_event_queryset_by_user_like_success_single_event(self, valid_event, valid_user):
        valid_event.user_event_like_logs.add(valid_user)

        event_queryset_by_user_like = self.event_selector.get_event_queryset_by_user_like(valid_user.id)

        assert event_queryset_by_user_like.first() == valid_event

    def test_get_event_queryset_by_user_like_success_multiple_event(self, valid_event_list, valid_user):
        for valid_event in valid_event_list:
            valid_event.user_event_like_logs.add(valid_user)

        event_queryset_by_user_like = self.event_selector.get_event_queryset_by_user_like(valid_user.id)

        assert event_queryset_by_user_like.count() == len(valid_event_list)

    def test_get_event_queryset_by_user_like_fail_does_not_exist(self, valid_user):
        event_queryset_by_user_like = self.event_selector.get_event_queryset_by_user_like(valid_user.id)

        assert event_queryset_by_user_like.count() == 0

    def test_get_event_queryset_by_user_like_fail_private_event(self, private_event, valid_user):
        private_event.user_event_like_logs.add(valid_user)

        event_queryset_by_user_like = self.event_selector.get_event_queryset_by_user_like(valid_user.id)

        assert event_queryset_by_user_like.count() == 0

    def test_get_event_queryset_by_user_like_fail_not_event_photo_booth_brand(self, invalid_event, valid_user):
        invalid_event.user_event_like_logs.add(valid_user)

        event_queryset_by_user_like = self.event_selector.get_event_queryset_by_user_like(valid_user.id)

        assert event_queryset_by_user_like.count() == 0
