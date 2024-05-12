from django.contrib.auth.models import User
from django_filters import rest_framework as filters

from advertisements.models import Advertisement


class AdvertisementFilter(filters.FilterSet):
    """Фильтры для объявлений."""

    # TODO: задайте требуемые фильтры
    created_at = filters.DateFromToRangeFilter()
    creator = filters.ModelChoiceFilter(queryset=User.objects.all())

    class Meta:
        model = Advertisement
        fields = ['creator', 'status', 'description', 'created_at']
