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



class CinematographerViewSet(viewsets.ModelViewSet):
    queryset = Cinematographer.objects.all()
    serializer_class = CinematographerSerializer


class FilmViewSet(viewsets.ModelViewSet):
    queryset = Film.objects.all()
    serializer_class = FilmSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = FilmFilter

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
    queryset = Lens.objects.all()
    serializer_class = LensSerializer


class ShotViewSet(viewsets.ModelViewSet):
    queryset = Shot.objects.all()
    serializer_class = ShotSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ShotFilter


class LightingSetupViewSet(viewsets.ModelViewSet):
    queryset = LightingSetup.objects.all()
    serializer_class = LightingSetupSerializer


class ReferencesViewSet(viewsets.ModelViewSet):
    queryset = Reference.objects.all()
    serializer_class = ReferenceSerializer
