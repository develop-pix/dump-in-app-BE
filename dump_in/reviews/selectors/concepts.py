from typing import List

from django.db.models.query import QuerySet

from dump_in.reviews.models import Concept


class ConceptSelector:
    def get_concept_queryset_by_ids(self, concept_ids: List[int]) -> QuerySet[Concept]:
        return Concept.objects.filter(id__in=concept_ids)
