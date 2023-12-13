import pytest

from dump_in.reviews.selectors.concepts import ConceptSelector

pytestmark = pytest.mark.django_db


class TestGetConceptQuerysetByIds:
    def setup_method(self):
        self.concept_selector = ConceptSelector()

    def test_get_concept_queryset_by_ids_success_single_concept_id(self, concept):
        concept_queryset = self.concept_selector.get_concept_queryset_by_ids([concept.id])

        assert list(concept_queryset) == [concept]

    def test_get_concept_queryset_by_ids_success_multiple_concept_ids(self, concept_list):
        concept_list_id = [concept.id for concept in concept_list]
        concept_queryset = self.concept_selector.get_concept_queryset_by_ids(concept_list_id)

        assert list(concept_queryset) == concept_list

    def test_get_concept_queryset_by_ids_fail_does_not_exist(self):
        concept_queryset = self.concept_selector.get_concept_queryset_by_ids([999])

        assert list(concept_queryset) == []
