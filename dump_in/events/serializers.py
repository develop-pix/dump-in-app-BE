from rest_framework import serializers

from dump_in.events.models import EventImage


class EventImageSerializer(serializers.ModelSerializer):
    image_url = serializers.CharField(source="event_image_url")

    class Meta:
        model = EventImage
        fields = (
            "id",
            "image_url",
        )
