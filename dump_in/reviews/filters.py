import django_filters

from dump_in.common.filters import ListFilter
from dump_in.reviews.models import Review


class ReviewFilter(django_filters.FilterSet):
    photo_booth_location = django_filters.CharFilter(method="filter_photo_booth_location")
    frame_color = ListFilter(field_name="frame_color", lookup_expr="in")
    participants = ListFilter(field_name="participants", lookup_expr="in")
    camera_shot = ListFilter(field_name="camera_shot", lookup_expr="in")
    concept = django_filters.CharFilter(method="filter_concept")

    def filter_photo_booth_location(self, queryset, name, value):
        if value not in (None, ""):
            values = value.split(",")
            return queryset.filter(photo_booth__location__in=values)

    def filter_concept(self, queryset, name, value):
        if value not in (None, ""):
            values = value.split(",")
            return queryset.filter(concept__id__in=values)

    class Meta:
        model = Review
        fields = [
            "photo_booth_location",
            "frame_color",
            "participants",
            "camera_shot",
            "concept",
        ]
