from django_filters import rest_framework as filters
from .models import Title


class TitleFilter(filters.FilterSet):
    """Фильтр для Произведений."""
    category = filters.CharFilter(
        field_name='category__slug',
        lookup_expr='icontains'
    )
    genre = filters.CharFilter(
        field_name='genre__slug',
        lookup_expr='icontains'
    )
    name = filters.CharFilter(
        lookup_expr='icontains'
    )
    year = filters.NumberFilter()

    class Meta:
        model = Title
        fields = (
            'genre',
            'year',
            'category',
            'name'
        )
