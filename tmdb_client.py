import requests
import os
from dotenv import load_dotenv

load_dotenv()

TMDB_API_KEY = os.getenv('TMDB_API_KEY')
TMDB_BASE_URL = 'https://api.themoviedb.org/3'


def fetch_film_details(title, year=None):
    """
    Fetch film details from TMDB API by title and optional year.
    Returns a dict with film data or None if not found.
    """
    if not TMDB_API_KEY:
        raise ValueError("TMBD_API_KEY not set in environment")

    # Step 1 - search for the film
    search_url = f"{TMDB_BASE_URL}/search/movie"
    params = {
        'api_key': TMDB_API_KEY,
        'query': title,
        'year': year,
    }

    try:
        response = requests.get(search_url, params=params, timeout=5)
        response.raise_for_status()
    except requests.exceptions.Timeout:
        raise Exception("TMDB request timed out")
    except requests.exceptions.ConnectionError:
        raise Exception("Could not connect to TMDB")
    except requests.exceptions.HTTPError as e:
        if response.status_code == 429:
            raise Exception("TMDB rate limit exceeded")
        raise Exception(f"TMDB HTTP error: {e}")

    data = response.json()

    if not data['results']:
        return None

    # Step 2 - get the first result
    film = data['results'][0]

    return {
        'tmdb_id': film.get('id'),
        'title': film.get('title'),
        'release_year': film.get('release_date', '')[:4],
        'synopsis': film.get('overview'),
        'poster_path': film.get('poster_path'),
    }
