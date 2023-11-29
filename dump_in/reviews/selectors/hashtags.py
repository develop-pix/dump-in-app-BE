from typing import List

from django.db.models.query import QuerySet

from dump_in.reviews.models import HashTag


class HashTagSelector:
    def get_hash_tag_queryset_by_ids(self, hashtag_ids: List[int]) -> QuerySet[HashTag]:
        return HashTag.objects.filter(id__in=hashtag_ids)
