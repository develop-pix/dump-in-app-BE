import django_filters

from dump_in.common.filters import ListFilter
from dump_in.reviews.models import Review


class ReviewFilter(django_filters.FilterSet):
    photo_booth_name = django_filters.CharFilter(method="filter_photo_booth_name")
    frame_color = ListFilter(field_name="frame_color", lookup_expr="in")
    participants = ListFilter(field_name="participants", lookup_expr="in")
    camera_shot = ListFilter(field_name="camera_shot", lookup_expr="in")
    concepts = django_filters.CharFilter(method="filter_concepts")

    def filter_photo_booth_name(self, queryset, name, value):
        if value not in (None, ""):
            values = value.split(",")
            return queryset.filter(potho_booths__name__in=values)

    def filter_concepts(self, queryset, name, value):
        if value not in (None, ""):
            values = value.split(",")
            return queryset.filter(concepts__id__in=values)

    class Meta:
        model = Review
        fields = [
            "frame_color",
            "participants",
            "camera_shot",
            "concepts",
        ]
