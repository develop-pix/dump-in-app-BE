import concurrent.futures

import pytest

from dump_in.common.exception.exceptions import NotFoundException
from dump_in.events.services import EventService

pytestmark = pytest.mark.django_db


class TestLikeEvent:
    def setup_method(self):
        self.event_service = EventService()

    def test_like_event_success(self, valid_event, valid_user):
        event, is_liked = self.event_service.like_event(event_id=valid_event.id, user=valid_user)

        assert is_liked is True
        assert event.user_event_like_logs.count() == 1
        assert event == valid_event

    def test_like_event_success_already_like(self, valid_event, valid_user):
        valid_event.user_event_like_logs.add(valid_user)
        event, is_like = self.event_service.like_event(event_id=valid_event.id, user=valid_user)

        assert is_like is False
        assert event.user_event_like_logs.count() == 0
        assert event == valid_event

    def test_like_event_fail_event_does_not_exist(self, valid_user):
        with pytest.raises(NotFoundException) as e:
            self.event_service.like_event(event_id=999, user=valid_user)

        assert e.value.detail == "Event does not exist"
        assert e.value.status_code == 404

    @pytest.mark.django_db(transaction=True)
    def test_like_event_success_concurrency(self, valid_event, valid_user, inactive_user):
        before_event_like_count = valid_event.like_count

        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            future1 = executor.submit(self.event_service.like_event, valid_event.id, valid_user)
            future2 = executor.submit(self.event_service.like_event, valid_event.id, inactive_user)

            result1 = future1.result()
            result2 = future2.result()

        result1_event, result1_is_like = result1
        result2_event, result2_is_like = result2

        assert result1_is_like is True
        assert result2_is_like is True

        valid_event.refresh_from_db()
        assert before_event_like_count + 2 == valid_event.like_count

        self.event_service.like_event(valid_event.id, valid_user)
        valid_event.refresh_from_db()
        assert before_event_like_count + 1 == valid_event.like_count
