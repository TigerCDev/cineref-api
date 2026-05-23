from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
import pytest
from .models import Film, Cinematographer



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
