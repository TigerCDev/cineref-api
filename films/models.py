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
    Cinematographer = models.ForeignKey(
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
