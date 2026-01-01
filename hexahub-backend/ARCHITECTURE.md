# HexaHub Backend Architecture

## Table of Contents
- [System Overview](#system-overview)
- [Architecture Diagram](#architecture-diagram)
- [Core Components](#core-components)
- [Technology Stack](#technology-stack)
- [Data Flow](#data-flow)
- [Security Architecture](#security-architecture)
- [Monitoring & Observability](#monitoring--observability)
- [Deployment Architecture](#deployment-architecture)
- [Development Workflow](#development-workflow)
- [Scaling Considerations](#scaling-considerations)

## System Overview

HexaHub Backend is a FastAPI-based microservice that provides authentication, user management, and observability for the HexaHub platform. The system is designed with production-grade monitoring, CI/CD automation, and containerized deployment.

### Design Principles

1. **API-First**: RESTful API design with OpenAPI documentation
2. **Observability**: Comprehensive metrics, logging, and alerting
3. **Security**: JWT authentication with OAuth2 integration path
4. **Scalability**: Stateless design with horizontal scaling capability
5. **DevOps**: Automated CI/CD with security scanning
6. **Reliability**: Health checks, graceful degradation, automated rollback

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         Load Balancer                            │
│                     (Future: Traefik/Nginx)                      │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      FastAPI Backend                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   Health     │  │     Auth     │  │    Users     │          │
│  │  Endpoints   │  │  (JWT/OAuth) │  │  Management  │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│         │                  │                   │                 │
│         └──────────────────┴───────────────────┘                │
│                            │                                     │
│                  ┌─────────▼─────────┐                          │
│                  │   SQLAlchemy ORM  │                          │
│                  └─────────┬─────────┘                          │
└────────────────────────────┼─────────────────────────────────────┘
                             │
              ┌──────────────┴──────────────┐
              │                             │
              ▼                             ▼
    ┌──────────────────┐        ┌──────────────────┐
    │   PostgreSQL 15  │        │  Prometheus      │
    │                  │        │  (Metrics)       │
    │  - Users         │        └────────┬─────────┘
    │  - Sessions      │                 │
    └──────────────────┘                 │
              │                           │
              ▼                           ▼
    ┌──────────────────┐        ┌──────────────────┐
    │ Postgres Exporter│        │     Grafana      │
    │  (DB Metrics)    │        │  (Dashboards)    │
    └──────────────────┘        └──────────────────┘
              │
              └─────────────────────┐
                                    ▼
                          ┌──────────────────┐
                          │    cAdvisor      │
                          │(Container Metrics)│
                          └──────────────────┘
```

## Core Components

### 1. FastAPI Application (`app/`)

**Main Application** (`main.py`)
- FastAPI application instance
- CORS middleware configuration
- Router registration
- Prometheus metrics instrumentation
- Startup/shutdown lifecycle management

**Configuration** (`config.py`)
- Pydantic Settings for environment-based configuration
- Database connection settings
- JWT/OAuth configuration
- CORS origins management
- Feature flags

**Database Layer** (`database.py`)
- SQLAlchemy engine initialization
- Session management with dependency injection
- Connection pooling configuration
- Automatic table creation

### 2. API Routes (`app/routes/`)

**Health Check** (`health.py`)
```python
GET /health         # Application health status
GET /health/db      # Database connectivity check
```

**Authentication** (`auth.py`)
```python
POST /auth/login    # JWT token generation
POST /auth/refresh  # Token refresh (future)
GET /auth/me        # Current user info
```

**User Management** (`users.py`)
```python
GET /users          # List users (paginated)
GET /users/{id}     # Get user by ID
POST /users         # Create user
PUT /users/{id}     # Update user
DELETE /users/{id}  # Delete user
```

### 3. Data Models (`app/models/`)

**User Model** (`user.py`)
```python
User:
  - id: Integer (PK)
  - email: String (unique, indexed)
  - username: String (unique, indexed)
  - full_name: String (nullable)
  - is_active: Boolean (default: True)
  - oauth_provider: String (nullable)
  - created_at: DateTime (auto)
  - updated_at: DateTime (auto)
```

### 4. Schemas (`app/schemas/`)

Pydantic models for request/response validation:
- `UserBase`: Base user fields
- `UserCreate`: User creation payload
- `UserUpdate`: User update payload
- `UserResponse`: User response model
- `Token`: JWT token response

### 5. Database (`PostgreSQL 15`)

**Configuration:**
- Connection pooling: 20 max connections
- Alpine-based container for minimal footprint
- Persistent volume for data durability
- Health check: `pg_isready -U hexahub`

**Migrations:**
- Alembic for schema migrations
- Auto-generated from SQLAlchemy models
- Version controlled migration history

## Technology Stack

### Backend Framework
- **FastAPI 0.109.0**: Modern async Python web framework
- **Uvicorn 0.27.0**: ASGI server with hot reload
- **Python 3.11**: Latest stable Python with performance improvements

### Database
- **PostgreSQL 15**: Primary data store
- **SQLAlchemy 2.0.25**: ORM and query builder
- **Alembic 1.13.1**: Database migration tool
- **psycopg2-binary 2.9.9**: PostgreSQL adapter

### Authentication
- **python-jose 3.3.0**: JWT token handling
- **passlib 1.7.4**: Password hashing (bcrypt)
- **OAuth2PasswordBearer**: FastAPI OAuth2 integration

### Validation
- **Pydantic 2.5.3**: Data validation and settings
- **email-validator 2.1.0**: Email validation

### Testing
- **pytest 7.4.4**: Testing framework
- **pytest-asyncio 0.23.3**: Async test support
- **pytest-cov 4.1.0**: Coverage reporting
- **httpx 0.26.0**: Test client for FastAPI

### Monitoring
- **prometheus-client 0.19.0**: Metrics collection
- **prometheus-fastapi-instrumentator 6.1.0**: Auto-instrumentation
- **Prometheus**: Metrics aggregation and alerting
- **Grafana**: Metrics visualization
- **cAdvisor**: Container metrics
- **postgres-exporter**: Database metrics

### DevOps
- **Docker**: Containerization
- **Docker Compose**: Local orchestration
- **GitHub Actions**: CI/CD automation
- **Trivy**: Security vulnerability scanning

## Data Flow

### Authentication Flow

```
1. Client Request
   └─> POST /auth/login
       └─> username + password

2. Backend Processing
   ├─> Validate credentials
   ├─> Query user from database
   │   └─> CREATE user if not exists (demo mode)
   ├─> Generate JWT token
   │   └─> Sign with SECRET_KEY
   │   └─> Set expiration (30 min default)
   └─> Return token

3. Client Storage
   └─> Store token (localStorage/cookie)

4. Subsequent Requests
   └─> Include: Authorization: Bearer {token}
       └─> Backend validates JWT
           ├─> Decode token
           ├─> Verify signature
           ├─> Check expiration
           └─> Extract user ID
               └─> Fetch user from DB
                   └─> Return user context
```

### Request Lifecycle

```
1. HTTP Request
   └─> Uvicorn (ASGI Server)

2. Middleware Chain
   ├─> CORS Middleware
   │   └─> Validate origin
   │   └─> Add CORS headers
   └─> Prometheus Middleware
       └─> Record request metrics
           - Request count
           - Request duration
           - Request size

3. Route Handler
   ├─> Path matching
   ├─> Request validation (Pydantic)
   ├─> Dependency injection
   │   └─> Database session
   │   └─> Current user (if authenticated)
   └─> Business logic

4. Database Operations
   ├─> SQLAlchemy query
   ├─> Connection pool
   └─> PostgreSQL execution

5. Response
   ├─> Pydantic serialization
   ├─> JSON encoding
   └─> HTTP response
       └─> Prometheus metrics update
```

## Security Architecture

### Authentication Strategy

**Current: JWT-based Authentication**
- HS256 signing algorithm
- 30-minute token expiration
- Bearer token scheme
- Automatic user creation (demo mode)

**Future: OAuth2 with Authentik**
- Integration with Authentik SSO
- OpenID Connect (OIDC) flow
- Multi-factor authentication (MFA)
- Session management

### Security Measures

1. **Input Validation**
   - Pydantic models for all inputs
   - Email format validation
   - SQL injection prevention (SQLAlchemy ORM)

2. **Password Security**
   - bcrypt hashing (passlib)
   - Configurable hash rounds
   - No plaintext password storage

3. **CORS Configuration**
   - Configurable allowed origins
   - Credentials support
   - Preflight request handling

4. **Environment Security**
   - `.env` file for secrets
   - No hardcoded credentials
   - SECRET_KEY rotation capability

5. **Container Security**
   - Non-root user execution
   - Minimal base images (Alpine)
   - Security scanning (Trivy)
   - Regular dependency updates

## Monitoring & Observability

### Metrics Collection

**Application Metrics** (via prometheus-fastapi-instrumentator)
- `http_requests_total`: Total HTTP requests by method, endpoint, status
- `http_request_duration_seconds`: Request latency histogram
- `http_request_size_bytes`: Request body size
- `http_response_size_bytes`: Response body size

**Python Runtime Metrics**
- `python_gc_*`: Garbage collection statistics
- `process_*`: Process CPU, memory, file descriptors
- `python_info`: Python version information

**Database Metrics** (via postgres-exporter)
- `pg_stat_database_*`: Database activity statistics
- `pg_stat_user_tables_*`: Table-level statistics
- `pg_locks_*`: Lock information
- `pg_stat_database_numbackends`: Active connections

**Container Metrics** (via cAdvisor)
- `container_cpu_usage_seconds_total`: CPU usage
- `container_memory_usage_bytes`: Memory usage
- `container_network_*`: Network I/O
- `container_fs_*`: Filesystem metrics

### Alerting Rules

**Critical Alerts**
- Backend down (> 1 minute)
- High error rate (> 5% 5xx responses)
- High latency (p95 > 1 second)
- Database connection failures
- High memory usage (> 80%)

**Warning Alerts**
- Database connection pool saturation
- High CPU usage (> 70%)
- Slow database queries

### Grafana Dashboards

**HexaHub Backend Overview**
- Backend status indicator
- Request rate graph (by endpoint)
- Response time percentiles (p50, p95)
- CPU and memory usage
- Database connection count

Access: http://localhost:3000 (admin/admin)

## Deployment Architecture

### Container Strategy

**Multi-stage Docker Build**
```dockerfile
# Stage 1: Builder
- Install system dependencies (gcc, postgresql-client)
- Install Python dependencies
- Create user packages

# Stage 2: Runtime
- Minimal base image
- Copy user packages from builder
- Set up non-root user
- Configure entrypoint
```

**Benefits:**
- Smaller final image size
- Faster deployment
- Reduced attack surface
- Layer caching optimization

### Docker Compose Services

```yaml
services:
  postgres:      # Database
  backend:       # FastAPI application
  prometheus:    # Metrics aggregation
  grafana:       # Visualization
  cadvisor:      # Container metrics
  postgres-exporter: # Database metrics
```

**Networks:**
- `hexahub-network`: Bridge network for inter-service communication

**Volumes:**
- `postgres_data`: Database persistence
- `prometheus_data`: Metrics storage
- `grafana_data`: Dashboard persistence

### CI/CD Pipeline

**GitHub Actions Workflow** (`.github/workflows/backend-ci-cd.yml`)

**Stages:**
1. **Build & Test**
   - Docker build with caching
   - Push to GHCR
   - Run pytest with coverage

2. **Security Scan**
   - Trivy vulnerability scanning
   - Dependency audit
   - Fail on HIGH/CRITICAL vulnerabilities

3. **Deploy Staging**
   - SSH to staging server
   - Pull latest image
   - Run database migrations
   - Deploy with Docker Compose
   - Health check validation

4. **Deploy Production**
   - Manual approval required
   - Blue-green deployment strategy
   - Automated rollback on failure

**Deployment Triggers:**
- Push to `main`: Deploy to staging
- Tag `v*`: Deploy to production
- Pull request: Build and test only

## Development Workflow

### Local Development Setup

```bash
# 1. Clone repository
git clone <repo-url>
cd hexahub-backend

# 2. Create environment file
cp .env.example .env
# Edit .env with local settings

# 3. Start services
docker compose up -d

# 4. Run migrations
docker compose exec backend alembic upgrade head

# 5. Access application
curl http://localhost:8000/health
```

### Testing

```bash
# Run all tests
docker compose exec backend pytest

# Run with coverage
docker compose exec backend pytest --cov=app --cov-report=html

# Run specific test file
docker compose exec backend pytest tests/test_health.py -v
```

### Database Migrations

```bash
# Create new migration
docker compose exec backend alembic revision --autogenerate -m "description"

# Apply migrations
docker compose exec backend alembic upgrade head

# Rollback one version
docker compose exec backend alembic downgrade -1

# Show migration history
docker compose exec backend alembic history
```

### Code Quality

```bash
# Format code
docker compose exec backend black app/

# Lint code
docker compose exec backend ruff check app/

# Type checking (future)
docker compose exec backend mypy app/
```

## Scaling Considerations

### Horizontal Scaling

**Stateless Design:**
- No in-memory session storage
- JWT tokens (client-side state)
- Database for all persistent state

**Load Balancing:**
- Round-robin distribution
- Health check endpoint for LB
- Graceful shutdown handling

**Scaling Strategy:**
```bash
docker compose up -d --scale backend=3
```

### Database Scaling

**Read Replicas:**
- PostgreSQL streaming replication
- Read-only queries to replicas
- Write queries to primary

**Connection Pooling:**
- SQLAlchemy pool size: 20
- Connection recycling
- Pool overflow handling

**Query Optimization:**
- Indexed columns: email, username
- Query analysis with EXPLAIN
- N+1 query prevention

### Caching Strategy (Future)

**Redis Integration:**
- Session storage
- API response caching
- Rate limiting counters
- Pub/sub for events

**Cache Invalidation:**
- Time-based expiration
- Event-driven invalidation
- Cache warming on deployment

### Performance Targets

- **Response Time:** p95 < 100ms, p99 < 500ms
- **Throughput:** > 1000 req/sec per instance
- **Availability:** 99.9% uptime
- **Database:** < 10ms query latency (p95)

### Monitoring for Scale

**Key Metrics:**
- Request rate and latency
- Error rate (5xx responses)
- Database connection pool usage
- Memory and CPU utilization
- Network I/O

**Autoscaling Triggers:**
- CPU > 70% for 5 minutes
- Memory > 80% for 5 minutes
- Request queue depth > 100

## Future Architecture Enhancements

### Planned Improvements

1. **Authentication**
   - Authentik OAuth2/OIDC integration
   - Multi-factor authentication (MFA)
   - Social login providers

2. **Caching Layer**
   - Redis for session storage
   - API response caching
   - Cache invalidation strategy

3. **Message Queue**
   - RabbitMQ/Redis for async tasks
   - Email notifications
   - Background job processing

4. **API Gateway**
   - Traefik reverse proxy
   - Rate limiting
   - Request routing
   - SSL termination

5. **Service Mesh**
   - Microservices architecture
   - Service discovery
   - Circuit breakers
   - Distributed tracing

6. **Advanced Monitoring**
   - Distributed tracing (Jaeger/Tempo)
   - Log aggregation (Loki)
   - Error tracking (Sentry)
   - APM (Application Performance Monitoring)

### Migration Path

```
Phase 1: Foundation (Current)
├─ FastAPI backend
├─ PostgreSQL database
├─ Basic monitoring
└─ CI/CD pipeline

Phase 2: Authentication & Caching
├─ Authentik integration
├─ Redis caching
└─ Session management

Phase 3: Scalability
├─ Load balancer
├─ Database replicas
├─ Horizontal scaling
└─ Advanced monitoring

Phase 4: Microservices
├─ Service decomposition
├─ Message queue
├─ API gateway
└─ Service mesh
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines, coding standards, and pull request process.

## License

See [LICENSE](LICENSE) file for details.

## Support

- **Documentation**: [docs/](docs/)
- **API Docs**: http://localhost:8000/docs
- **Issues**: GitHub Issues
- **Monitoring**: http://localhost:3000
