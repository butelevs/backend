from django.contrib.auth import get_user_model
from django_filters.rest_framework import DateFromToRangeFilter, FilterSet

from advertisements.models import Advertisement, AdvertisementStatusChoices


class AdvertisementFilter(FilterSet):
    """Фильтры для объявлений."""

    created_at = DateFromToRangeFilter()

    class Meta:
        model = Advertisement
        fields = ['status', 'creator', 'created_at',]
