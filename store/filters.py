import django_filters
from django_filters import RangeFilter
from .models import *


class ProductFilter(django_filters.FilterSet):
    price = RangeFilter()
    class Meta:
        model = Product
        fields = ['name', 'price']

    name = django_filters.CharFilter(field_name='name', lookup_expr="icontains")
