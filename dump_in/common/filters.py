import django_filters


class ListFilter(django_filters.Filter):
    def filter(self, qs, value):
        if value not in (None, ""):
            values = value.split(",")
            return qs.filter(**{"{}__{}".format(self.field_name, self.lookup_expr): values})
        return qs
