from django_filters import filterset, filters
from zs_utils.api.models import APIRequestLog


__all__ = [
    "APIRequestLogFilter",
]


class APIRequestLogFilter(filterset.FilterSet):
    created = filters.DateTimeFromToRangeFilter()
    is_success = filters.BooleanFilter(method="get_is_success")
    response_time = filters.NumberFilter(lookup_expr="gte")
    url = filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = APIRequestLog
        fields = [
            "user",
        ]

    def get_is_success(self, queryset, name, value):
        if value:
            return queryset.filter(status_code__startswith="2")
        else:
            return queryset.exclude(status_code__startswith="2")
