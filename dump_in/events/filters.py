import django_filters

from dump_in.events.models import Event


class EventFilter(django_filters.FilterSet):
    hashtag_ids = django_filters.CharFilter(method="filter_hashtag_ids")

    def filter_hashtag_ids(self, queryset, name, value):
        if value not in (None, ""):
            values = value.split(",")
            return queryset.filter(hashtag__id__in=values)

    class Meta:
        model = Event
        fields = [
            "hashtag_ids",
        ]
