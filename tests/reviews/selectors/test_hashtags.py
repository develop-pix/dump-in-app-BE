from dump_in.reviews.selectors.concepts import ConceptSelector


class TestConceptSelector:
    def setup_method(self):
        self.concept_selector = ConceptSelector()

    def test_get_concept_queryset_by_ids_success(self, concept):
        concept_id = concept.id
        concept_queryset = self.concept_selector.get_concept_queryset_by_ids([concept_id])
        assert concept_queryset.count() == 1
