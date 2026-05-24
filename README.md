# CineRef API

> A production-grade cinematography reference REST API — Django · DRF · PostgreSQL · Docker

## Stack

**Backend:** Python · Django · Django REST Framework
**Database:** PostgreSQL
**Auth:** JWT via djangorestframework-simplejwt
**Infra:** Docker · Docker Compose
**Testing:** pytest · pytest-django
**External:** TMDB API

## Features

- Full CRUD for Films, Cinematographers, Shots, and Lenses
- JWT authentication — read endpoints open, write endpoints protected
- Nested serializers — films show cinematographer details, shots show full film and lens data
- TMDB API integration — fetch real film metadata by title and year
- Automated test suite with pytest-django

## Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | /api/v1/films/ | No | List all films |
| POST | /api/v1/films/ | Yes | Create a film |
| GET | /api/v1/films/{id}/ | No | Get a film |
| GET | /api/v1/cinematographers/ | No | List cinematographers with nested films |
| GET | /api/v1/shots/ | No | List shots |
| POST | /api/v1/shots/ | Yes | Create a shot |
| GET | /api/v1/lenses/ | No | List lenses |
| POST | /api/v1/token/ | No | Obtain JWT token |
| POST | /api/v1/token/refresh/ | No | Refresh JWT token |

## Run locally

```bash
git clone https://github.com/TigerCDev/cineref-api.git
cd cineref-api
cp .env.example .env  # add your TMDB_API_KEY
docker compose up --build
```

Visit http://localhost:8000/api/v1/

## Run tests

```bash
docker compose exec web pytest -v
```

## Why this exists

Built to bridge my background in film production and software
engineering. The domain exposes interesting technical problems —
relational data modeling, external API integration, async task
processing — that general CRUD projects don't. Every line of code
is mine.
