import django_filters

from reviews.models import Titles

class TitlesFilters(django_filters.FilterSet):
    genre = django_filters.CharFilter(field_name='genre', lookup_expr='slug')
    category = django_filters.CharFilter(field_name='category', lookup_expr='slug')
    name = django_filters.CharFilter(field_name='name')
    year = django_filters.CharFilter(field_name='year')
    class Meta:
        model = Titles
        fields = ['genre', 'category', 'name', 'year']