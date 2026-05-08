from rest_framework import serializers
from .models import Cinematographer, Film

class CinematographerSerializer(serializers.ModelSerializer):
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