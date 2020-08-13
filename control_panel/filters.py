import django_filters
from django_filters import NumberFilter, CharFilter
from .models import *


class ProductFilter(django_filters.FilterSet):
    start_price = NumberFilter(field_name='price', lookup_expr='gte')
    end_price = NumberFilter(field_name='price', lookup_expr='lte')
    search_name = CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Product
        fields = '__all__'
        exclude = ['tags', 'description', 'date_created', 'price', 'name', 'buying_price']
