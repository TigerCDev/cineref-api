from celery import shared_task
from .models import Film
from tmdb_client import fetch_film_details



@shared_task
def sync_tmdb_for_film(film_id):
    """
    Fetch TMDB dta for a film and update its fields.
    Triggered asynchronously after film creation.
    """
    try:
        film = Film.objects.get(id=film_id)
    except Film.DoesNotExist:
        return f"Film {film_id} not found"

    data = fetch_film_details(film.title, film.release_year)

    if not data:
        return f"No TMDB data found for {film.title}"

    if data.get('synopsis'):
        film.synopsis = data['synopsis']

    film.save()
    return f"Updated film {film.title} with TMDB data"
