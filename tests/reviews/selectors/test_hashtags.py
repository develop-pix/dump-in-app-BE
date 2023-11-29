import pytest

from dump_in.reviews.selectors.hashtags import HashTagSelector

pytestmark = pytest.mark.django_db


class TestHashTagSelector:
    def setup_method(self):
        self.hashtag_selector = HashTagSelector()

    def test_get_hash_tag_queryset_by_ids_success(self, hashtag):
        hashtag_id = hashtag.id
        hashtag_queryset = self.hashtag_selector.get_hash_tag_queryset_by_ids([hashtag_id])
        assert hashtag_queryset.count() == 1
