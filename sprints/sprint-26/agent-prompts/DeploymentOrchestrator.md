# DeploymentOrchestrator - Sprint 26 Tasks

**Priority:** HIGH
**Owner:** DeploymentOrchestrator (Automated + Human oversight)
**Output Directory:** `/home/fitna/homelab/infrastructure/`
**Deadline:** Tag 5 (2025-12-31)

---

## 🎯 Mission

Setup production-ready infrastructure for HexaHub MVP: CI/CD pipeline, staging environment on RTX1080, monitoring stack, and K3s readiness check.

---

## 📋 Tasks

### 1. CI/CD Pipeline für HexaHub MVP
**Story Points:** 2
**Platform:** GitHub Actions

**Requirements:**

**Workflow Steps:**
```yaml
name: HexaHub CI/CD

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    - Run pytest (backend tests)
    - Run ESLint (frontend)
    - Check code coverage (>80%)

  build:
    - Build Docker images (backend, frontend)
    - Tag with commit SHA
    - Push to GitHub Container Registry

  deploy-staging:
    - Deploy to RTX1080 via SSH
    - Run health checks
    - Notify on Slack/Discord (success/failure)
    - Rollback on failure

  deploy-production:
    - Manual approval required
    - Deploy to VPS
    - Health checks
    - Notify team
```

**Deliverables:**
- `.github/workflows/hexahub-ci-cd.yml`
- Deployment script: `infrastructure/scripts/deploy-staging.sh`
- Rollback script: `infrastructure/scripts/rollback.sh`
- README: `infrastructure/CI-CD-SETUP.md`

**Testing:**
- Trigger test deployment
- Verify auto-rollback works
- Test manual production deployment

**Output:** Working CI/CD pipeline with 3 successful test runs

---

### 2. Staging Environment (RTX1080 - Docker Compose)
**Story Points:** 2
**Target:** RTX1080 homelab server

**Stack Setup:**

```yaml
# docker-compose.staging.yml
services:
  hexahub-backend:
    image: ghcr.io/xessshare/hexahub-backend:staging
    ports: ["8000:8000"]
    environment:
      - DATABASE_URL=postgresql://...
      - REDIS_URL=redis://...
      - AUTHENTIK_URL=http://authentik:9000
    depends_on: [postgres, redis]

  hexahub-frontend:
    image: ghcr.io/xessshare/hexahub-frontend:staging
    ports: ["3000:3000"]
    environment:
      - NEXT_PUBLIC_API_URL=http://backend:8000

  postgres:
    image: postgres:16-alpine
    volumes: ["./data/postgres:/var/lib/postgresql/data"]

  redis:
    image: redis:7-alpine

  nginx:
    image: nginx:alpine
    ports: ["80:80", "443:443"]
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./certs:/etc/nginx/certs
```

**Tasks:**
1. Create `docker-compose.staging.yml`
2. Configure nginx reverse proxy
3. Setup SSL certificates (Let's Encrypt)
4. Configure Authentik integration
5. Setup PostgreSQL with backups
6. Test full stack deployment

**Deliverables:**
- `infrastructure/docker-compose.staging.yml`
- `infrastructure/nginx/hexahub.conf`
- `infrastructure/scripts/setup-staging.sh`
- `infrastructure/STAGING-SETUP.md`

**Success Criteria:**
- HexaHub accessible via https://staging.hexahub.local
- Auth flow works (Authentik integration)
- API responds to health checks
- Database persists data after restart

---

### 3. Monitoring Setup (Grafana/Prometheus for HexaHub)
**Story Points:** 1.5
**Stack:** Prometheus + Grafana + Loki

**Metrics to Track:**

**Application Metrics:**
```python
# Backend (FastAPI)
- API request latency (p50, p95, p99)
- Request rate (req/sec)
- Error rate (4xx, 5xx)
- Active users (concurrent)
- Database query duration
- Redis cache hit rate
```

**Infrastructure Metrics:**
```
- CPU usage (per container)
- Memory usage
- Disk I/O
- Network throughput
- Container health status
```

**Business Metrics:**
```
- User signups (daily)
- API calls per user
- Feature usage stats
- Session duration
```

**Grafana Dashboards:**
1. HexaHub Overview (high-level KPIs)
2. API Performance (latency, errors)
3. Infrastructure Health (CPU, mem, disk)
4. User Activity (signups, sessions)

**Alerting Rules:**
```yaml
Alerts:
  - name: API Down
    condition: up{job="hexahub-backend"} == 0
    duration: 2m
    severity: critical

  - name: High Error Rate
    condition: rate(http_errors_total[5m]) > 0.05
    duration: 5m
    severity: warning

  - name: Slow Response Time
    condition: http_request_duration_p95 > 2s
    duration: 10m
    severity: warning
```

**Deliverables:**
- `infrastructure/monitoring/prometheus.yml`
- `infrastructure/monitoring/grafana-dashboards/` (4 dashboards)
- `infrastructure/monitoring/alertmanager.yml`
- `infrastructure/MONITORING-SETUP.md`

**Output:** Working monitoring stack with dashboards accessible

---

### 4. Infrastructure Scaling Preparation (K3s Readiness Check)
**Story Points:** 0.5
**Goal:** Prepare for Phase 3 cloud migration

**Tasks:**

1. **K3s Installation (Homelab)**
   - Install K3s on RTX1080
   - Configure kubectl access
   - Setup Helm

2. **Namespace Structure**
   ```
   - hexahub-staging
   - hexahub-production
   - monitoring
   - infra
   ```

3. **Helm Charts Preparation**
   - Create Helm chart skeleton for HexaHub
   - Values files for staging/production
   - Document deployment process

4. **Migration Path Documentation**
   ```markdown
   Phase 1-2: Docker Compose (current)
   Phase 3: K3s (homelab) → EKS/GKE (cloud)

   Migration steps:
   1. Convert docker-compose to K8s manifests
   2. Test on K3s locally
   3. Deploy to cloud K8s (EKS/GKE)
   4. Cut over DNS
   ```

**Deliverables:**
- K3s installed and tested
- `infrastructure/k8s/hexahub-chart/` (Helm chart)
- `infrastructure/SCALING-PLAN.md`

---

## 🛠️ Tech Stack

**CI/CD:**
- GitHub Actions
- Docker
- SSH deployment

**Infrastructure:**
- Docker Compose (staging)
- Nginx (reverse proxy)
- Let's Encrypt (SSL)
- Authentik (SSO)

**Monitoring:**
- Prometheus (metrics)
- Grafana (visualization)
- Loki (logs)
- Alertmanager (alerts)

**Future:**
- K3s (local K8s)
- Helm (package management)
- Terraform (IaC for cloud)

---

## 📊 Success Metrics

- CI/CD: <5min deployment time, 100% automated
- Staging: 99%+ uptime, <100ms API latency
- Monitoring: 100% metric coverage, <2min alert response
- K3s: Ready for Q2 migration

---

## 🚀 Execution Instructions

**Agent Prompt:**
```
You are DeploymentOrchestrator working on Sprint 26 infrastructure setup.

Your mission: Build production-ready deployment pipeline and staging environment for HexaHub MVP.

Context:
- Current: No CI/CD, manual deployments
- Target: Automated staging deployments, monitoring, K3s prep
- Timeline: Tag 5 (2025-12-31)
- Infrastructure: RTX1080 homelab server (staging)

Tasks (execute in order):
1. CI/CD Pipeline (GitHub Actions) → .github/workflows/hexahub-ci-cd.yml
2. Staging Environment (Docker Compose) → infrastructure/docker-compose.staging.yml
3. Monitoring Stack (Prometheus + Grafana) → infrastructure/monitoring/
4. K3s Readiness (installation + prep) → infrastructure/k8s/

Output directory: /home/fitna/homelab/infrastructure/

Principles:
- Automate everything
- Fail fast, rollback faster
- Monitor all the things
- Document for future scaling

Begin with Task 1. Test thoroughly before moving to next task.
```

---

**Created:** 2025-12-28
**Last Updated:** 2025-12-28
