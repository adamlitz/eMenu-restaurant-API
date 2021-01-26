import django_filters.rest_framework as filters
from .models import Menu


class DateFilter(filters.FilterSet):
    """
    Allows filtering by date
    """
    created = filters.IsoDateTimeFromToRangeFilter()
    updated = filters.IsoDateTimeFromToRangeFilter()

    class Meta:
        model = Menu
        fields = ['created', 'updated']
