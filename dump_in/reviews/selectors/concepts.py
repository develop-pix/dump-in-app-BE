from typing import List

from django.db.models.query import QuerySet

from dump_in.reviews.models import Concept


class ConceptSelector:
    def get_concept_queryset_by_names(self, concept_names: List[str]) -> QuerySet[Concept]:
        return Concept.objects.filter(name__in=concept_names)
