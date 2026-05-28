# CineRef API

> A production-grade cinematography reference REST API built with Django, DRF, PostgreSQL, and Docker.

**Live:** https://cineref-api.fly.dev · **Docs:** https://cineref-api.fly.dev/api/schema/swagger-ui/

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Django](https://img.shields.io/badge/Django-6.0-green)
![DRF](https://img.shields.io/badge/DRF-3.17-red)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue)
![Docker](https://img.shields.io/badge/Docker-compose-blue)
![Coverage](https://img.shields.io/badge/coverage-92%25-brightgreen)

## What this is

A REST API for cataloging and querying cinematography reference data — films, shots, lenses, lighting setups, cinematographers, and cross-linked references. Built as a production portfolio project demonstrating Django/DRF fundamentals alongside asynchronous task processing, external API integration, and full-text search.

## Why it's interesting (technical)

- **TMDB API integration** — auto-fetches film metadata on creation via async Celery task
- **Celery + Redis** — async task queue so API responses are never blocked by external calls
- **Postgres full-text search** — SearchVector ranking across title, director, and synopsis
- **JWT authentication** — read endpoints open, write endpoints protected
- **drf-spectacular** — auto-generated OpenAPI 3.0 docs + Swagger UI
- **pytest-django** with 92% coverage including mocked external API tests
- **Dockerized** — Django + PostgreSQL + Redis + Celery in one `docker compose up`
- **Rate limiting** — anonymous 100/day, authenticated 1000/day

## Architecture

[Add architecture diagram here]

## Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | /api/v1/films/ | No | List films (paginated, filterable) |
| POST | /api/v1/films/ | Yes | Create film (triggers async TMDB sync) |
| GET | /api/v1/films/search/?q=... | No | Full-text search across title, director, synopsis |
| GET | /api/v1/cinematographers/ | No | List cinematographers with nested films |
| GET | /api/v1/shots/ | No | List shots (filterable by film, lens type) |
| POST | /api/v1/shots/ | Yes | Create shot |
| GET | /api/v1/lenses/ | No | List lenses with notable films |
| GET | /api/v1/lightingsetups/ | No | List lighting setups |
| GET | /api/v1/references/ | No | List references |
| POST | /api/v1/token/ | No | Obtain JWT token |
| POST | /api/v1/token/refresh/ | No | Refresh JWT token |
| GET | /api/schema/swagger-ui/ | No | Interactive API docs |

## Run locally

```bash
git clone https://github.com/TigerCDev/cineref-api.git
cd cineref-api
cp .env.example .env  # add your TMDB_API_KEY
docker compose up --build
```

Visit http://localhost:8000/api/schema/swagger-ui/

## Run tests

```bash
docker compose exec web pytest -v
docker compose exec web pytest --cov=. --cov-report=term-missing
```

## Key technical decisions

**Why Celery instead of calling TMDB synchronously?** External API calls average 800ms. Blocking the request thread for that long would make every film creation feel slow. Celery drops the task into Redis and returns 201 immediately — the enrichment happens in the background.

**Why Postgres full-text search instead of simple icontains filtering?** Full-text search with SearchVector handles stemming, ranking, and multi-field search in one query. A search for "blade runner" ranks title matches higher than synopsis matches automatically.

**Why drf-spectacular?** Auto-generated docs that stay in sync with the code. No manual maintenance. A hiring manager can click the Swagger UI URL and explore the entire API without reading the source.

## Why this exists

Built to bridge my background in film production and software engineering. The domain exposes interesting technical problems — relational data modeling, external API reliability, async task processing — that general CRUD projects don't. Every line of code is mine.
