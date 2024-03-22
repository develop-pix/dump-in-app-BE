import django_filters

from dump_in.events.models import Event


class EventFilter(django_filters.FilterSet):
    hashtag = django_filters.Filter(method="filter_hashtag")

    def filter_hashtag(self, queryset, name, value):
        if value:
            values = list(value)
            return queryset.filter(hashtag__name__in=values)
        return queryset

    class Meta:
        model = Event
        fields = [
            "hashtag",
        ]
