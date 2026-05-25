from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

from .models import (
    Cinematographer,
    Film,
    Lens,
    Shot,
)
from .serializers import (
    CinematographerSerializer,
    FilmSerializer,
    LensSerializer,
    ShotSerializer,
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


class LensViewSet(viewsets.ModelViewSet):
    queryset = Lens.objects.all()
    serializer_class = LensSerializer


class ShotViewSet(viewsets.ModelViewSet):
    queryset = Shot.objects.all()
    serializer_class = ShotSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ShotFilter
