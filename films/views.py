from rest_framework import viewsets
from .models import Cinematographer, Film
from .serializers import CinematographerSerializer, FilmSerializer


class CinematographerViewSet(viewsets.ModelViewSet):
    queryset = Cinematographer.objects.all()
    serializer_class = CinematographerSerializer


class FilmViewSet(viewsets.ModelViewSet):
    queryset = Film.objects.all()
    serializer_class = FilmSerializer