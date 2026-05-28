from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
import pytest
from .models import (
    Film,
    Cinematographer,
    Shot,
    LightingSetup,
    Reference,
)

from unittest.mock import patch, MagicMock
from tmdb_client import fetch_film_details
from .tasks import sync_tmdb_for_film
import requests


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticated_client(db):
    user = User.objects.create_user(
        username='testuser',
        password='testpass123'
    )
    client = APIClient()
    response = client.post('/api/v1/token/', {
        'username': 'testuser',
        'password': 'testpass123'
    }, format='json')
    token = response.data['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    return client


@pytest.mark.django_db
def test_list_films(api_client, db):
    response = api_client.get('/api/v1/films/')
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_create_film_unauthenticated(api_client, db):
    response = api_client.post('/api/v1/films/', {
        'title': 'Test Film',
        'release_year': 2004,
        'director': 'Test director'
    }, format='json')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_create_film_authenticated(authenticated_client):
    response = authenticated_client.post('/api/v1/films/', {
        'title': 'Test Film',
        'release_year': 2024,
        'director': 'Test Director'
    }, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['title'] == 'Test Film'


@pytest.mark.django_db
def test_list_shots(api_client, db):
    response = api_client.get('/api/v1/shots/')
    assert response.status_code == status.HTTP_200_OK



@pytest.mark.django_db
def test_create_shot_unauthenticated(api_client, db):
    film = Film.objects.create(
        title='Test Film',
        release_year=2024,
        director='Test Director',
    )
    response = api_client.post('/api/v1/shots/', {
        'film_id': film.id,
        'description': 'Test Shot',
    }, format='json')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_create_shot_authenticated(authenticated_client):
    film = Film.objects.create(
        title='Test Film',
        release_year=2024,
        director='Test Director',
    )
    response = authenticated_client.post('/api/v1/shots/', {
        'film_id': film.id,
        'description': 'Test Shot',
    }, format='json')
    assert response.status_code == status.HTTP_201_CREATED, response.data
    assert response.data['description'] == 'Test Shot'


@pytest.mark.django_db
def test_filter_films_by_year(api_client, db):
    Film.objects.create(title='Film A', release_year=2017, director='Director A')
    Film.objects.create(title='Film B', release_year=2020, director='Director B')

    response = api_client.get('/api/v1/films/?release_year=2017')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data['results']) == 1
    assert response.data['results'][0]['title'] == 'Film A'


@pytest.mark.django_db
def test_filter_film_by_director(api_client, db):
    Film.objects.create(title='Film A', release_year=2017, director='Denis Villeneuve')
    Film.objects.create(title='Film B', release_year=2020, director='Christopher Nolan')

    response = api_client.get('/api/v1/films/?director=villeneuve')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data['results']) == 1
    assert response.data['results'][0]['title'] == 'Film A'


@pytest.mark.django_db
def test_filter_shots_by_film(api_client, db):
    film_a = Film.objects.create(title='Film A', release_year=2017, director='Director A')
    film_b = Film.objects.create(title='Film B', release_year=2020, director='Director B')
    Shot.objects.create(film=film_a, description='Shot 1')
    Shot.objects.create(film=film_b, description='Shot 2')

    response = api_client.get(f'/api/v1/shots/?film={film_a.id}')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data['results']) == 1
    assert response.data['results'][0]['description'] == 'Shot 1'


@pytest.mark.django_db
def test_search_film(api_client, db):
    Film.objects.create(title='Blade Runner 2049', release_year=2017, director='Denis Villeneuve')
    Film.objects.create(title='Oppenheimer', release_year=2023, director='Chirstopher Nolan')

    response = api_client.get('/api/v1/films/search/?q=blade+runner')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) >= 1
    assert response.data[0]['title'] == 'Blade Runner 2049'


@pytest.mark.django_db
def test_list_lighting_setups(api_client, db):
    response = api_client.get('/api/v1/lightingsetups/')
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_create_lighting_setup_authenticated(authenticated_client):
    film = Film.objects.create(
        title='Test Film',
        release_year=2026,
        director='Test Director',
    )
    shot = Shot.objects.create(film=film, description='Test Shot')
    response = authenticated_client.post('/api/v1/lightingsetups/', {
        'shot_id': shot.id,
    }, format='json')
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_listing_references(api_client, db):
    Reference.objects.create(title='Test Reference', type='inspiration')

    response = api_client.get('/api/v1/references/')
    assert response.status_code == status.HTTP_200_OK
    assert response.data['count'] == 1
    assert response.data['results'][0]['title'] == 'Test Reference'


@pytest.mark.django_db
def test_create_reference_authenticated(authenticated_client):
    response = authenticated_client.post('/api/v1/references/', {
        'title': 'Test Reference',
        'type': 'inspiration',
    }, format='json')

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['title'] == 'Test Reference'


@pytest.mark.django_db
def test_sync_tmdb_for_film_task(db):
    film = Film.objects.create(
        title='Blade Runner 2049',
        release_year=2017,
        director='Denis Villeneuve',
    )

    with patch('films.tasks.fetch_film_details') as mock_fetch:
        mock_fetch.return_value = {
            'tmdb_id': 335984,
            'title': 'Blade Runner 2049',
            'release_year': '2017',
            'synopsis': 'A new blade runner unearths a secret.',
            'poster_path': '/some/path.jpg',
        }
        result = sync_tmdb_for_film(film.id)

    film.refresh_from_db()
    assert result == f"Updated film {film.title} with TMDB data"
    assert film.synopsis == 'A new blade runner unearths a secret.'


@pytest.mark.django_db
def test_sync_tmdb_film_not_found(db):
    film = Film.objects.create(
        title='Nonexistent Film XYZ',
        release_year=2024,
        director='Nobody'
    )
    with patch('films.tasks.fetch_film_details') as mock_fetch:
        mock_fetch.return_value = None
        result = sync_tmdb_for_film(film.id)
    assert result == f'No TMDB data found for {film.title}'


def test_fetch_film_details_film_not_found():
    with patch('tmdb_client.requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {'results': []}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = fetch_film_details('Nonexistent Film XYZ', 2024)
        assert result is None


def test_fetch_film_details_timeout():
    with patch('tmdb_client.requests.get') as mock_get:
        mock_get.side_effect = requests.exceptions.Timeout()
        with pytest.raises(Exception, match='timed out'):
            fetch_film_details('Blade Runner 2049', 2017)


@pytest.mark.django_db
def test_get_nonexistent_film(api_client, db):
    response = api_client.get('/api/v1/films/99999/')
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_invalid_jwt_token(api_client, db):
    api_client.credentials(HTTP_AUTHORIZATION='Bearer invalidtoken123')
    response = api_client.post('/api/v1/films/', {
        'title': 'Test Film',
        'release_year': 2024,
        'director': 'Test Director',
    }, format='json')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db()
def test_malformed_filter_params(api_client, db):
    response = api_client.get('/api/v1/films/?release_year=notanumber')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
