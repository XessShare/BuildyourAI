# HexaHub Backend API

Self-hosted AI workspace backend built with FastAPI and PostgreSQL.

[![CI/CD Pipeline](https://github.com/XessShare/BuildyourAI/actions/workflows/backend-ci-cd.yml/badge.svg)](https://github.com/XessShare/BuildyourAI/actions/workflows/backend-ci-cd.yml)
[![codecov](https://codecov.io/gh/XessShare/BuildyourAI/branch/main/graph/badge.svg)](https://codecov.io/gh/XessShare/BuildyourAI)

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.11+ (for local development)

### Run with Docker Compose

1. **Clone and navigate:**
   ```bash
   cd hexahub-backend
   ```

2. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

3. **Start services:**
   ```bash
   docker-compose up -d
   ```

4. **Check health:**
   ```bash
   curl http://localhost:8000/health
   ```

5. **Access API docs:**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Local Development (without Docker)

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start PostgreSQL:**
   ```bash
   docker-compose up -d postgres
   ```

3. **Run API:**
   ```bash
   python -m uvicorn app.main:app --reload
   ```

## API Endpoints

### Health
- `GET /health` - Basic health check
- `GET /health/db` - Database health check

### Authentication
- `POST /auth/login` - Login (MVP: demo mode, no password required)
- `GET /auth/callback` - OAuth callback (placeholder for Authentik)

### Users
- `GET /users/me` - Get current user info (requires auth)
- `GET /users/{user_id}` - Get user by ID (requires auth)
- `GET /users/` - List all users (requires auth)
- `POST /users/` - Create new user
- `PATCH /users/me` - Update current user (requires auth)

## Testing

Run tests:
```bash
pytest tests/ -v
```

With coverage:
```bash
pytest tests/ -v --cov=app --cov-report=html
```

## Project Structure

```
hexahub-backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration (Pydantic Settings)
│   ├── database.py          # Database connection
│   ├── models/              # SQLAlchemy models
│   │   ├── __init__.py
│   │   └── user.py
│   ├── schemas/             # Pydantic schemas
│   │   ├── __init__.py
│   │   └── user.py
│   ├── routes/              # API endpoints
│   │   ├── __init__.py
│   │   ├── health.py
│   │   ├── auth.py
│   │   └── users.py
│   └── services/            # Business logic
├── tests/                   # Test suite
├── migrations/              # Database migrations
├── requirements.txt         # Python dependencies
├── Dockerfile               # Docker image
├── docker-compose.yml       # Docker Compose config
├── .env.example             # Environment variables template
└── README.md                # This file
```

## Environment Variables

See `.env.example` for all configuration options.

Key variables:
- `DATABASE_URL` - PostgreSQL connection string
- `SECRET_KEY` - JWT secret (change in production!)
- `AUTHENTIK_URL` - Authentik SSO server URL
- `CORS_ORIGINS` - Allowed CORS origins

## Development

### Code Style
- Black for formatting
- Ruff for linting

```bash
black app/
ruff check app/
```

### Database Migrations
```bash
# Create migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head
```

## Production Deployment

1. Update `.env` with production values
2. Set strong `SECRET_KEY`
3. Configure Authentik OAuth credentials
4. Use PostgreSQL with SSL
5. Enable HTTPS (reverse proxy)
6. Set `DEBUG=false`

## License

MIT License - See LICENSE file

## CI/CD Pipeline

**Status:** ✅ Configured
**Workflow:** `.github/workflows/backend-ci-cd.yml`
**Staging:** http://rtx1080.local:8000

### Automatic Deployment

Pushes to `main`, `master`, or `sprint-26/*` branches automatically:
1. Build Docker image
2. Run tests (pytest)
3. Security scan (Trivy)
4. Deploy to staging
5. Run health checks

### Manual Deployment

```bash
# Deploy to staging
./scripts/deploy.sh staging

# Run health checks
./scripts/health-check.sh staging

# Rollback if needed
./scripts/rollback.sh
```

See [CICD_SETUP.md](./CICD_SETUP.md) for detailed pipeline documentation.

---

## Sprint 26 Notes

**Status:** MVP Backend + CI/CD Complete (13 SP)
**Goal:** Automated deployment pipeline with testing
**Tech Stack:** FastAPI 0.109, PostgreSQL 15, Docker, GitHub Actions
**Authentication:** JWT (demo mode), Authentik OAuth (placeholder)
**Deployment:** Automated to RTX1080 staging ✓
