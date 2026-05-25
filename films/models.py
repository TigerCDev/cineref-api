from django.contrib.auth.models import User
from django.db import models


class Cinematographer(models.Model):
    name = models.CharField(max_length=255)
    birth_year = models.IntegerField(null=True, blank=True)
    nationality = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name


class Film(models.Model):
    title = models.CharField(max_length=255)
    release_year = models.IntegerField()
    director = models.CharField(max_length=255)
    cinematographer = models.ForeignKey(
        Cinematographer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='films',
    )
    aspect_ratio = models.CharField(max_length=20, null=True, blank=True)
    runtime = models.IntegerField(null=True, blank=True)
    synopsis = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering =['-created_at']


class Lens(models.Model):
    LENS_TYPE_CHOICES= [
        ('anamorphic', 'Anamorphic'),
        ('spherical', 'Spherical'),
        ('other', 'Other'),
    ]

    manufacturer = models.CharField(max_length=255)
    model_name = models.CharField(max_length=255)
    focal_length_min = models.IntegerField(null=True, blank=True)
    focal_length_max = models.IntegerField(null=True, blank=True)
    lens_type = models.CharField(
        max_length=255,
        choices=LENS_TYPE_CHOICES,
        default='spherical',
    )
    notable_films = models.ManyToManyField(
        Film,
        blank=True,
        related_name='lenses',
    )

    def __str__(self):
        return f'{self.manufacturer} {self.model_name}'


class Shot(models.Model):
    film = models.ForeignKey(
        Film,
        on_delete=models.CASCADE,
        related_name='shots',
    )
    timestamp = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    lens_used = models.ForeignKey(
        Lens,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='shots',
    )
    lighting_notes = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='shots',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Shot from {self.film.title} at {self.timestamp}'

    class Meta:
        ordering = ['-created_at']


class LightingSetup(models.Model):
    SETUP_TYPE_CHOICES = [
        ('three_point', 'Three Point'),
        ('motivated', 'Motivated'),
        ('natural', 'Natural'),
        ('high_key', 'High Key'),
        ('low_key', 'Low Key'),
        ('other', 'Other'),
    ]

    shot = models.ForeignKey(
        Shot,
        on_delete=models.CASCADE,
        related_name='lighting_setups',
    )
    setup_type = models.CharField(
        max_length=50,
        choices=SETUP_TYPE_CHOICES,
        default='other'
    )
    key_light_notes = models.TextField(null=True, blank=True)
    fill_notes = models.TextField(null=True, blank=True)
    equipment_list = models.JSONField(default=list, blank=True)

    def __str__(self):
        return f'{self.setup_type} for shot {self.shot.id}'

    class Meta:
        ordering = ['id']


class Reference(models.Model):
    TYPE_CHOICES = [
        ('inspiration', 'Inspiration'),
        ('technique', 'Technique'),
        ('director_study', 'Director Study'),
    ]

    title = models.CharField(max_length=255)
    type = models.CharField(
        max_length=50,
        choices=TYPE_CHOICES,
        default='inspiration',
    )
    linked_film = models.ManyToManyField(
        Film,
        blank=True,
        related_name='references',
    )
    linked_shot = models.ManyToManyField(
        Shot,
        blank=True,
        related_name='references'
    )
    notes = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='references'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
