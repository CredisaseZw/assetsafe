# To Do Is To Be

[![CI](https://github.com/CredisaseZw/assetsafe/actions/workflows/ci.yml/badge.svg)](https://github.com/CredisaseZw/assetsafe/actions/workflows/ci.yml)

*Esse est posse*

> "To do is to be" is a Latin philosophical expression often interpreted as
> "to be is to have the power to be" or "to be is to be able to be."

It has been attributed to several Greek and Roman thinkers, including Aristotle,
Seneca, and Cicero. The phrase is commonly used to express the idea that
existence is fundamental to reality, and that the ability to be is a necessary
condition for existence.

---

## Running the System

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/) (v2+)
- Git

### 1. Clone and configure environment

```bash
git clone https://github.com/CredisaseZw/assetsafe.git
cd assetsafe

# Backend environment
cp .env.example .env.docker
# Edit .env.docker and fill in SECRET_KEY, DB credentials, Redis URLs, etc.
```

For the frontend, set the API base URL if it differs from the default:

```bash
# frontend/.env.local
VITE_API_BASE_URL=http://localhost:8081/api
```

### 2. Build and start all services

```bash
docker compose up --build
```

This starts:

| Service | URL |
|---------|-----|
| Nginx (reverse proxy) | <http://localhost:8080> |
| Django / Gunicorn | <http://localhost:8081> |
| React / Vite frontend | <http://localhost:5173> |
| Redis | `localhost:6380` |

Celery worker and beat scheduler start automatically alongside the app.

### 3. Create a superuser (first run only)

```bash
docker compose exec app python manage.py createsuperuser
```

### 4. Stop the system

```bash
docker compose down          # stop containers, keep volumes
docker compose down -v       # stop and remove all volumes (resets database)
```

---

### Running locally (without Docker)

**Requirements:** Python 3.12+, [uv](https://github.com/astral-sh/uv), Node.js 20+, a running PostgreSQL instance, and Redis.

```bash
# Install Python dependencies
uv sync

# Configure environment
cp .env.example .env
# Edit .env with your local DB and Redis settings

# Apply migrations and start Django
python manage.py migrate
python manage.py runserver

# In a separate terminal — Celery worker
celery -A core worker -l info

# In a separate terminal — Celery beat
celery -A core beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler

# In a separate terminal — React frontend
cd frontend
npm install
npm run dev
```

The frontend dev server will be available at <http://localhost:5173> and the Django API at <http://localhost:8000>.