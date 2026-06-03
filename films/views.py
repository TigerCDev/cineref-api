from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import (
    Cinematographer,
    Film,
    Lens,
    Shot,
    LightingSetup,
    Reference
)
from .serializers import (
    CinematographerSerializer,
    FilmSerializer,
    LensSerializer,
    ShotSerializer,
    LightingSetupSerializer,
    ReferenceSerializer
)
from .filters import FilmFilter, ShotFilter
from .tasks import sync_tmdb_for_film



class CinematographerViewSet(viewsets.ModelViewSet):
    queryset = Cinematographer.objects.all()
    serializer_class = CinematographerSerializer


class FilmViewSet(viewsets.ModelViewSet):
    queryset = Film.objects.select_related('cinematographer')
    serializer_class = FilmSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = FilmFilter

    def perform_create(self, serializer):
        film = serializer.save()
        sync_tmdb_for_film.delay(film.id)

    @action(detail=False, methods=['get'], url_path='search')
    def search(self, request):
        query = request.query_params.get('q', '')
        if not query:
            return Response([])

        search_vector = SearchVector('title', weight='A') + \
                        SearchVector('director', weight='B') + \
                        SearchVector('synopsis', weight='C')
        search_query = SearchQuery(query)

        results = Film.objects.annotate(
            rank=SearchRank(search_vector, search_query)
        ).filter(rank__gte=0.001).order_by('-rank')

        serializer = self.get_serializer(results, many=True)
        return Response(serializer.data)


class LensViewSet(viewsets.ModelViewSet):
    queryset = Lens.objects.prefetch_related('notable_films')
    serializer_class = LensSerializer


class ShotViewSet(viewsets.ModelViewSet):
    queryset = Shot.objects.select_related('film', 'lens_used', 'created_by')
    serializer_class = ShotSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ShotFilter


class LightingSetupViewSet(viewsets.ModelViewSet):
    queryset = LightingSetup.objects.select_related('shot')
    serializer_class = LightingSetupSerializer


class ReferencesViewSet(viewsets.ModelViewSet):
    queryset = Reference.objects.select_related('created_by').prefetch_related('linked_film', 'linked_shot')
    serializer_class = ReferenceSerializer
