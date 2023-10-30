from django_filters import rest_framework as filters
from .models import Title


class TitleFilter(filters.FilterSet):
    """Фильтр для Произведений."""
    category = filters.CharFilter(field_name='category__slug')
    genre = filters.CharFilter(field_name='genre__slug')
    name = filters.CharFilter()
    year = filters.CharFilter()

    class Meta:
        model = Title
        fields = (
            'genre',
            'year',
            'category',
            'name'
        )
