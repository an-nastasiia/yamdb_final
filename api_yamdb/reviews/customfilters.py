import django_filters

from .models import Title


class TitleFilter(django_filters.FilterSet):
    """Filter for Title by fields: name, year, category and genre."""

    category = django_filters.CharFilter(
        field_name="category__slug", lookup_expr='icontains')
    genre = django_filters.CharFilter(
        field_name="genre__slug", lookup_expr='icontains')
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Title
        fields = ('category', 'genre', 'name', 'year')
