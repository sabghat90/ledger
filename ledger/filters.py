import django_filters
from .models import Order
from django_filters import DateFilter, CharFilter


class OrderFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name="created_at", lookup_expr='gte')
    end_date = DateFilter(field_name="created_at", lookup_expr='lte')
    name = CharFilter(field_name='name', lookup_expr='icontains')
    class Meta:
        model = Order
        fields = ['order_type', 'created_at', 'agent']
