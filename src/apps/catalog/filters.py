import django_filters
from django.db.models import Q

from apps.catalog.models import Product


class ProductFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method="filter_search")

    class Meta:
        model = Product
        fields = ("category", "badge", "family")

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(name__ru__icontains=value)
            | Q(name__en__icontains=value)
            | Q(description__ru__icontains=value)
            | Q(description__en__icontains=value)
        )
