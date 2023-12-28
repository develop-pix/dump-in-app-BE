import django_filters

from dump_in.reviews.models import Review


class ReviewFilter(django_filters.FilterSet):
    photo_booth_location = django_filters.Filter(method="filter_photo_booth_location")
    frame_color = django_filters.Filter(method="filter_frame_color")
    participants = django_filters.Filter(method="filter_participants")
    camera_shot = django_filters.Filter(method="filter_camera_shot")
    concept = django_filters.Filter(method="filter_concept")

    def filter_photo_booth_location(self, queryset, name, value):
        if value:
            values = list(value)
            return queryset.filter(photo_booth__location__in=values)
        return queryset

    def filter_frame_color(self, queryset, name, value):
        if value:
            values = list(value)
            return queryset.filter(frame_color__in=values)
        return queryset

    def filter_participants(self, queryset, name, value):
        if value:
            values = list(value)
            return queryset.filter(participants__in=values)
        return queryset

    def filter_camera_shot(self, queryset, name, value):
        if value:
            values = list(value)
            return queryset.filter(camera_shot__in=values)
        return queryset

    def filter_concept(self, queryset, name, value):
        if value:
            values = list(value)
            return queryset.filter(concept__name__in=values)
        return queryset

    class Meta:
        model = Review
        fields = [
            "photo_booth_location",
            "frame_color",
            "participants",
            "camera_shot",
            "concept",
        ]
