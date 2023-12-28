import pytest

from dump_in.reviews.selectors.concepts import ConceptSelector

pytestmark = pytest.mark.django_db


class TestGetConceptQuerysetByNames:
    def setup_method(self):
        self.concept_selector = ConceptSelector()

    def test_get_concept_queryset_by_names_success_single_concept_name(self, concept):
        concept_queryset = self.concept_selector.get_concept_queryset_by_names([concept.name])

        assert concept_queryset.first() == concept

    def test_get_concept_queryset_by_names_success_multiple_concept_name(self, concept_list):
        concept_list_name = [concept.name for concept in concept_list]
        concept_queryset = self.concept_selector.get_concept_queryset_by_names(concept_list_name)

        assert concept_queryset.count() == len(concept_list)

    def test_get_concept_queryset_by_names_fail_does_not_exist(self):
        concept_queryset = self.concept_selector.get_concept_queryset_by_names(["string"])

        assert concept_queryset.count() == 0
