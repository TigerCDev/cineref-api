from rest_framework import serializers
from .models import (
    Cinematographer,
    Film,
    Lens,
    Shot,
    LightingSetup,
    Reference
)


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


class LensSerializer(serializers.ModelSerializer):
    notable_films = FilmBasicSerializer(many=True, read_only=True)

    class Meta:
        model = Lens
        fields = '__all__'


class ShotSerializer(serializers.ModelSerializer):
    film = FilmSerializer(read_only=True)
    film_id = serializers.PrimaryKeyRelatedField(
        queryset=Film.objects.all(),
        source='film',
        write_only=True,
    )
    lens_used = LensSerializer(read_only=True)
    lens_used_id = serializers.PrimaryKeyRelatedField(
        queryset=Lens.objects.all(),
        source='lens_used',
        write_only=True,
        allow_null=True,
        required=False,
    )
    created_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Shot
        fields = '__all__'


class LightingSetupSerializer(serializers.ModelSerializer):
    shot = ShotSerializer(read_only=True)
    shot_id = serializers.PrimaryKeyRelatedField(
        queryset=Shot.objects.all(),
        source='shot',
        write_only=True,
    )

    class Meta:
        model = LightingSetup
        fields = '__all__'


class ReferenceSerializer(serializers.ModelSerializer):
    linked_films = FilmBasicSerializer(many=True, read_only=True)
    linked_film_ids = serializers.PrimaryKeyRelatedField(
        queryset=Film.objects.all(),
        source='linked_films',
        many=True,
        write_only=True,
        required=False,
    )
    linked_shots = ShotSerializer(many=True, read_only=True)
    linked_shot_ids = serializers.PrimaryKeyRelatedField(
        queryset=Shot.objects.all(),
        source='linked_shots',
        many=True,
        write_only=True,
        required=False,
    )

    class Meta:
        model = Reference
        fields = '__all__'
