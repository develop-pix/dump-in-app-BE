import django_filters

from dump_in.common.filters import ListFilter
from dump_in.reviews.models import Review


class ReviewFilter(django_filters.FilterSet):
    location = django_filters.CharFilter(method="filter_location")
    frame_color = ListFilter(field_name="frame_color", lookup_expr="in")
    participants = ListFilter(field_name="participants", lookup_expr="in")
    camera_shot = ListFilter(field_name="camera_shot", lookup_expr="in")
    hashtags = django_filters.CharFilter(method="filter_hashtags")

    def filter_location(self, queryset, name, value):
        if value not in (None, ""):
            values = value.split(",")
            return queryset.filter(potho_booths__location__in=values)

    def filter_hashtags(self, queryset, name, value):
        if value not in (None, ""):
            values = value.split(",")
            return queryset.filter(hashtags__id__in=values)

    class Meta:
        model = Review
        fields = [
            "frame_color",
            "participants",
            "camera_shot",
            "hashtags",
        ]
