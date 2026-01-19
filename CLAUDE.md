# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## Repository Overview

This is a **production homelab infrastructure** combining:
- **Homelab OSS Stack**: 30+ self-hosted services (Docker Compose)
- **J-Jeco AI Platform**: Multi-agent AI system with LangChain + ChromaDB
- **HexaHub Backend**: FastAPI SaaS application with CI/CD
- **3-System Architecture**: VPS (public), ThinkPad (dev), RTX1080 (production/GPU)

**Key Context:**
- Production environment serving real users
- Multi-agent AI system with model routing (Claude 3.5, GPT-4o-mini, Perplexity)
- Distributed deployment across 3 physical systems
- Sprint-driven development (2-week cycles, story point tracking)

---

## Essential Commands

### Infrastructure (Docker Compose Stacks)

```bash
# Navigate to stacks directory
cd /home/fitna/homelab/infrastructure/docker/stacks

# Deploy specific stack
docker compose -f core.yml up -d              # Traefik + Authentik + PostgreSQL
docker compose -f homeassistant.yml up -d     # Smart home stack
docker compose -f media.yml up -d             # Jellyfin + *arr suite
docker compose -f monitoring.yml up -d        # Prometheus + Grafana + Loki

# View logs (real-time)
docker compose -f <stack>.yml logs -f [service-name]

# Check service status
docker compose -f <stack>.yml ps

# Restart service
docker compose -f <stack>.yml restart [service-name]

# Stop and remove
docker compose -f <stack>.yml down

# Create required network (if missing)
docker network create homelab_network
```

### Ansible (Infrastructure Automation)

```bash
# Test connectivity to all hosts
ansible all -i infrastructure/ansible/inventory/hosts.yml -m ping

# Bootstrap new hosts (initial setup)
ansible-playbook -i infrastructure/ansible/inventory/hosts.yml \
  infrastructure/ansible/playbooks/00-bootstrap.yml

# Check UFW firewall status
ansible all -i infrastructure/ansible/inventory/hosts.yml \
  -m shell -a "ufw status verbose"
```

### AI Platform (Python Agents)

```bash
# Navigate to AI platform
cd /home/fitna/homelab/ai-platform/1-first-agent

# Activate virtual environment
source ../ai-agents-masterclass/bin/activate

# Install/update dependencies
pip install -r requirements.txt

# Test all configured LLM models
python test_all_models.py

# Test individual agents
python test_content_creator.py
python test_researcher.py
python test_verifier.py
python test_analyst.py

# Run main orchestrator
python main.py                              # Interactive mode
python main.py optimize-prompt "text"       # Optimize prompt
python main.py plan-project "description"   # Create action plan
python main.py moonshot-check               # Check progress

# Run agent workflows
python run_agents.py
```

### HexaHub Backend (FastAPI)

```bash
# Navigate to backend
cd /home/fitna/homelab/hexahub-backend

# Start all services (Docker Compose)
docker-compose up -d

# Run tests
docker-compose exec backend pytest tests/ -v

# Run tests with coverage
docker-compose exec backend pytest --cov=app --cov-report=html

# Check health
curl http://localhost:8000/health
curl http://localhost:8000/health/db

# View API docs
# Swagger: http://localhost:8000/docs
# ReDoc: http://localhost:8000/redoc

# Database migrations
docker-compose exec backend alembic upgrade head
docker-compose exec backend alembic revision --autogenerate -m "description"

# Code quality
docker-compose exec backend black app/
docker-compose exec backend ruff check app/
```

### Sprint Management (Automation Scripts)

```bash
# Start new sprint
/home/fitna/homelab/shared/scripts/sprint-manager.sh start

# Check sprint status
/home/fitna/homelab/shared/scripts/sprint-manager.sh status

# Complete sprint (generate report)
/home/fitna/homelab/shared/scripts/sprint-manager.sh end

# Daily progress tracking
/home/fitna/homelab/shared/scripts/create-daily-sheet-enhanced.sh
/home/fitna/homelab/shared/scripts/create-evening-report.sh
```

### Secrets Management

```bash
# Sync API keys across all 3 systems (VPS, ThinkPad, RTX1080)
/home/fitna/homelab/shared/scripts/sync-secrets.sh

# Master secrets location:
# /home/fitna/homelab/shared/secrets/.env.master (NOT in Git)
```

---

## Architecture

### Three-System Distributed Architecture

```
┌─────────────────────────────────────────────────────────┐
│ VPS (91.107.198.37) - "The Field Agent"                 │
│ Role: Public-facing, lightweight agents                 │
│ Services: Ghost/Listmonk, Webhook handler               │
│ Agents: Communicator, Project Manager                   │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ ThinkPad (192.168.16.7) - "Development Workshop"        │
│ Role: Development, testing, CI/CD staging               │
│ Specs: 4 cores, 8GB RAM                                 │
│ Agents: All agents (testing & debugging)                │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ RTX1080 (192.168.17.1) - "Production Powerhouse"        │
│ Role: GPU compute, heavy AI workloads, production       │
│ Specs: 8 cores, 32GB RAM, RTX 1080 GPU                  │
│ Services: All major stacks (monitoring, media, etc.)    │
│ Agents: Research, Content Creator, Verification         │
└─────────────────────────────────────────────────────────┘

Connection: WireGuard VPN + Direct LAN (ThinkPad ↔ RTX1080)
```

### Docker Compose Stack Organization

All services use `homelab_network` for inter-container communication. Traefik acts as reverse proxy with automatic SSL (Let's Encrypt) and Authentik SSO protection.

**Key Stacks** (`infrastructure/docker/stacks/`):
- `core.yml` - Traefik + Authentik + PostgreSQL + Redis
- `homeassistant.yml` - Home Assistant + MQTT + Zigbee2MQTT + Node-RED
- `media.yml` - Jellyfin + Sonarr + Radarr + Prowlarr + qBittorrent
- `monitoring.yml` - Prometheus + Grafana + Loki + Uptime Kuma
- `automation.yml` - n8n + Node-RED + Pi-hole + Ollama

### AI Agent Architecture

**Multi-Agent System** (`ai-platform/1-first-agent/agents/`):

All agents inherit from `BaseAgent` (base_agent.py) and use model routing:
- **Claude 3.5 Sonnet** - Strategic/architectural tasks (ProjectManager, Communicator)
- **GPT-4o-mini** - Content creation, analysis (ContentCreator, Analyst, Verifier)
- **Perplexity** - Real-time research with online sources (Researcher)

**Key Components:**
- `main.py` - JJecoOrchestrator (CLI entry point)
- `run_agents.py` - Workflow runner (video, newsletter, research workflows)
- `knowledge_base.py` - ChromaDB vector database (cross-agent knowledge sharing)
- `config.py` - Central configuration (API keys, model routing, agent specializations)

**Agent Roles:**
- **ProjectManagerAgent** - Orchestrates workflows, breaks down tasks
- **CommunicatorAgent** - Optimizes prompts and messaging
- **ContentCreatorAgent** - Generates video scripts, newsletters, blog posts
- **ResearcherAgent** - Online research with Perplexity API
- **VerifierAgent** - Fact-checking and QA
- **AnalystAgent** - KPI tracking and data analysis
- **CodeGenerationAgent** - Code generation with fallbacks
- **DeploymentOrchestrator** - CI/CD orchestration

### HexaHub Backend Architecture

FastAPI application with:
- **PostgreSQL 15** - Database (SQLAlchemy ORM)
- **Prometheus + Grafana** - Metrics and visualization
- **cAdvisor** - Container metrics
- **Alembic** - Database migrations
- **pytest** - Testing framework

**API Structure** (`hexahub-backend/app/`):
- `main.py` - FastAPI app
- `config.py` - Pydantic Settings
- `database.py` - Database connection
- `models/` - SQLAlchemy models
- `schemas/` - Pydantic schemas
- `routes/` - API endpoints (health, auth, users)

---

## Important Patterns & Conventions

### Docker Compose Patterns

**Network:** All services must use `homelab_network` (external)

**Traefik Labels Pattern:**
```yaml
labels:
  - "traefik.enable=true"
  - "traefik.http.routers.SERVICE.rule=Host(`SERVICE.${DOMAIN}`)"
  - "traefik.http.routers.SERVICE.entrypoints=websecure"
  - "traefik.http.routers.SERVICE.tls.certresolver=cloudflare"
  - "traefik.http.routers.SERVICE.middlewares=authentik@file"
```

**Environment Variables:** Always loaded from `.env` files (never hardcoded)

### Git Workflow

**Branch Strategy:**
- Main branch: `master`
- Feature branches: `sprint-XX/<feature-name>`
- Current: `sprint-26/multi-agent-prompt-optimization`

**Commit Convention:**
```
<type>(<scope>): <description> (<story-points> SP)

Types: feat, fix, docs, chore, refactor
Example: feat(cicd): Complete CI/CD Pipeline Setup (5 SP)
```

### Naming Conventions

- **Containers:** `service-name` (lowercase, hyphenated)
- **Networks:** `homelab_network`
- **Volumes:** `service-name_data`
- **Hosts:** `pve-<description>` (e.g., pve-thinkpad, pve-ryzen)

### File Organization

```
infrastructure/  → Homelab services (Docker, Ansible, configs)
ai-platform/     → J-Jeco multi-agent system
hexahub-backend/ → FastAPI SaaS application
shared/          → Cross-system resources (scripts, docs, secrets)
sprints/         → Sprint planning and tracking
```

**Critical Rule:** Do NOT mix concerns between these directories.

---

## Security & Deployment

### Required Before Making Changes

1. **Read documentation first:**
   - `AGENTS.md` - Repository overview
   - `infrastructure/README.md` - Infrastructure details
   - `.cursorrules` - Critical safety rules

2. **Check git status** to understand current state

3. **Verify target system:**
   - VPS: Lightweight agents, public-facing
   - ThinkPad: Development and testing
   - RTX1080: Production and GPU workloads

4. **ALWAYS test on ThinkPad (dev) before RTX1080 (production)**

### Secrets Management

**Master secrets location:** `/home/fitna/homelab/shared/secrets/.env.master`

**NEVER commit to Git:**
- `.env` files
- API keys (OPENAI_API_KEY, ANTHROPIC_API_KEY, etc.)
- Passwords
- Tokens
- Private keys

**Required API keys:**
- Infrastructure: CLOUDFLARE_API_KEY, AUTHENTIK_SECRET_KEY, POSTGRES_PASSWORD
- AI Platform: OPENAI_API_KEY, ANTHROPIC_API_KEY, GOOGLE_API_KEY, PERPLEXITY_API_KEY

### Deployment Safety Rules

- **NEVER deploy to all hosts simultaneously** - deploy sequentially
- **ALWAYS verify health checks** after deployment
- **CREATE snapshots** before major infrastructure changes
- **STOP after 2 failed attempts** - ask for human intervention
- **DO NOT restart services in loops** - fix root cause first

### Firewall (UFW)

**Open ports:**
- 22 (SSH)
- 80/443 (HTTP/S)
- 8006 (Proxmox Web UI)
- 2377, 7946, 4789 (Docker Swarm)

### Authentication

- **Authentik SSO** protects all services with 2FA
- **JWT tokens** for API authentication (HexaHub)
- **SSH key-only** authentication (passwords disabled)

---

## CI/CD Pipeline

**GitHub Actions workflows:**
- `.github/workflows/backend-ci-cd.yml` - HexaHub backend
- `.github/workflows/deploy.yml` - Infrastructure deployment

**Pipeline stages:**
1. Build Docker image
2. Run tests (pytest)
3. Security scan (Trivy)
4. Deploy to staging (RTX1080)
5. Health check validation

**Trigger events:**
- Push to `main`, `master`, or `sprint-26/*` branches
- Manual dispatch with environment selection

**Required GitHub Secrets:**
- VPS_WEBHOOK_URL
- DEPLOY_TOKEN
- HEALTH_CHECK_URL
- Database credentials
- API keys

---

## Sprint-Driven Development

**Sprint Cycle:** 2 weeks (starting 2025-01-01)

**Sprint Structure** (`sprints/sprint-XX/`):
- `SPRINT_PLAN.md` - Goals, backlog, timeline
- `SPRINT_BOARD.md` - Kanban board (TODO/IN PROGRESS/DONE)
- `SPRINT_STATUS.md` - Real-time progress tracking
- `prompt-library/` - Reusable agent prompts

**Story Points:**
- High Priority: 5-8 SP
- Medium Priority: 2-3 SP
- Low Priority: 1 SP

**Agent Task Allocation Pattern:**
Each sprint allocates tasks to 6 agent types (ContentCreator, Researcher, Analyst, ProjectManager, DeploymentOrchestrator, Verifier)

---

## Troubleshooting

### Container Won't Start

```bash
# Check logs
docker logs <container-name>

# Force recreate
docker compose -f <stack>.yml down
docker compose -f <stack>.yml up -d --force-recreate
```

### Traefik Not Routing

```bash
# Check Traefik logs
docker logs traefik

# Verify container labels
docker inspect <container-name> | grep traefik

# Access dashboard: https://traefik.${DOMAIN}
```

### Service Health Checks

```bash
# PostgreSQL
docker exec postgresql pg_isready

# Redis
docker exec redis redis-cli ping

# Check unhealthy containers
docker ps --filter "health=unhealthy"
```

### AI Agent Issues

```bash
# Verify .env file exists
ls -la /home/fitna/homelab/ai-platform/1-first-agent/.env

# Test API connectivity
python test_all_models.py

# Check API key sync status
/home/fitna/homelab/shared/scripts/sync-secrets.sh
```

---

## Key Documentation Files

**Must-read before making changes:**
- `AGENTS.md` - Comprehensive repository guide
- `infrastructure/README.md` - Complete stack documentation
- `ai-platform/ARCHITECTURE.md` - AI system architecture (500+ lines)
- `.cursorrules` - Critical safety rules (loop prevention, duplicate prevention)
- `SCHLACHTPLAN_2025.md` - Strategic roadmap

**HexaHub specific:**
- `hexahub-backend/README.md` - API documentation
- `hexahub-backend/CICD_SETUP.md` - CI/CD pipeline details

**Sprint specific:**
- `sprints/sprint-26/SPRINT_PLAN.md` - Current sprint goals
- `sprints/sprint-26/QUICK_START_GUIDE.md` - Agent onboarding

---

## Common Gotchas

1. **Docker networks:** Services must use `homelab_network` (external) to communicate
2. **API keys:** Sync across systems with `sync-secrets.sh` before running agents
3. **Virtual environment:** Always activate (`source ../ai-agents-masterclass/bin/activate`) before running Python agents
4. **System roles:** VPS=lightweight, ThinkPad=dev, RTX1080=production/GPU
5. **Firewall:** UFW is active on all hosts - check rules before troubleshooting connectivity
6. **Git commits:** Include story points in commit message for velocity tracking
7. **Docker Compose files:** Multiple stack files exist - use correct one for your target
8. **Ansible inventory:** Uses `hosts.yml` not `hosts.ini`
9. **Health checks:** Verify after every deployment - don't assume success
10. **Loop prevention:** `.cursorrules` contains explicit warnings about recursive operations

---

**Production Environment:** This is a live homelab serving real users. Always test on ThinkPad (dev) before deploying to RTX1080 (production). When in doubt, ask for clarification.
