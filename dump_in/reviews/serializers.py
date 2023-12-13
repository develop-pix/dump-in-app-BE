from rest_framework import serializers

from dump_in.reviews.models import Concept, ReviewImage


class ReviewImageSerializer(serializers.ModelSerializer):
    image_url = serializers.URLField(source="review_image_url")

    class Meta:
        model = ReviewImage
        fields = (
            "id",
            "image_url",
        )


class ConceptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Concept
        fields = (
            "id",
            "name",
        )
