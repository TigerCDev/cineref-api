import django_filters
from .models import Film, Shot


class FilmFilter(django_filters.FilterSet):
    release_year = django_filters.NumberFilter()
    director = django_filters.CharFilter(lookup_expr='icontains')
    aspect_ratio = django_filters.CharFilter(lookup_expr='icontains')
    cinematographer = django_filters.NumberFilter(
        field_name='cinematographer__id'
    )

    class Meta:
        model = Film
        fields = ['release_year', 'director', 'aspect_ratio', 'cinematographer']


class ShotFilter(django_filters.FilterSet):
    film = django_filters.NumberFilter(
        field_name='film__id'
    )
    lens_type = django_filters.CharFilter(
        field_name='lens_used__lens_type',
        lookup_expr='icontains'
    )
    lighting_notes = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Shot
        fields = ['film', 'lens_type', 'lighting_notes']
