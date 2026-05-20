from rest_framework import serializers
from .models import Cinematographer, Film


class FilmBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Film
        fields =['id', 'title', 'release_year', 'director', 'aspect_ratio']


class CinematographerSerializer(serializers.ModelSerializer):
    films = FilmBasicSerializer(many=True, read_only=True)

    class Meta:
        model = Cinematographer
        fields = '__all__'


class FilmSerializer(serializers.ModelSerializer):
    cinematographer = CinematographerSerializer(read_only=True)
    cinematographer_id = serializers.PrimaryKeyRelatedField(
        queryset=Cinematographer.objects.all(),
        source='cinematographer',
        write_only=True,
        allow_null=True,
        required=False
    )

    class Meta:
        model = Film
        fields = '__all__'
