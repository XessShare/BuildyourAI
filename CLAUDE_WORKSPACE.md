# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## Quick Start - First Time Here?

**This is a workspace directory, not a single project.** `/home/fitna` contains five independent projects, each with its own documentation.

**What to do first:**
1. **Clarify the scope** - Ask which project the user wants to work on
2. **Navigate to project** - `cd /home/fitna/<project-name>`
3. **Read project docs** - See [Project-Specific Documentation](#project-specific-documentation) below
4. **Use project CLAUDE.md** - Each project has detailed setup/architecture docs

**This file provides:** Cross-project overview, common commands, and system architecture.

**System Environment:**
- OS: Arch Linux (Kernel 6.18.3-arch1-1)
- Platform: x86_64
- Working Directory: `/home/fitna`
- Current System: RTX1080 (192.168.17.1) - Production machine

---

## Environment Overview

Multi-project development environment (`/home/fitna`) with five distinct projects:

| Project | Path | Type | Status |
|---------|------|------|--------|
| **homelab/** | `/home/fitna/homelab` | Infrastructure + AI Platform | Production (30+ services) |
| **J-Jeco/** | `/home/fitna/J-Jeco` | AI Agent Platform | Production (multi-agent content) |
| **FItnaai/** | `/home/fitna/FItnaai` | Agent Framework | MVP1 complete (24/24 tests) |
| **content-pipeline/** | `/home/fitna/content-pipeline` | Content Pipeline | Forked from FItnaai MVP1 |
| **Documents/** | `/home/fitna/Documents` | Planning Repository | Documentation only |

**When asked to "work on the codebase" without context, clarify which project.**

Each project has its own detailed CLAUDE.md - see [Project-Specific Docs](#project-specific-documentation) below.

---

## Quick Reference

| Task | Command |
|------|:--------|
| Deploy homelab stack | `cd /home/fitna/homelab/infrastructure/docker/stacks && docker compose -f <stack>.yml up -d` |
| Run homelab AI agents | `cd /home/fitna/homelab/ai-platform/1-first-agent && source ../ai-agents-masterclass/bin/activate && python main.py` |
| Run J-Jeco agents | `cd /home/fitna/J-Jeco/1-first-agent && source ../ai-agents-masterclass/bin/activate && python main.py` |
| Run FItnaai pipeline | `cd /home/fitna/FItnaai && source .venv/bin/activate && fitnaai run -t "Topic" -a "Audience" -g "Newsletter"` |
| Run content-pipeline | `cd /home/fitna/content-pipeline && source .venv/bin/activate && fitnaai run -t "Topic" -a "Audience" -g "Newsletter"` |
| Test FItnaai/content-pipeline | `cd /home/fitna/{project} && source .venv/bin/activate && pytest tests/ -v` |
| Test AI connectivity | `python test_all_models.py` (from any ai-platform dir) |
| Sync secrets | `/home/fitna/homelab/shared/scripts/sync-secrets.sh` |
| Check container health | `docker ps --filter "health=unhealthy"` |

---

## 3-System Architecture

```
VPS (91.107.198.37)       → Public-facing, lightweight agents, webhooks
ThinkPad (192.168.16.7)   → Development/testing (ALWAYS test here first)
RTX1080 (192.168.17.1)    → Production, GPU workloads (8 cores, 32GB, RTX 1080)
```

**Connectivity:** WireGuard VPN + Direct LAN (ThinkPad ↔ RTX1080)

**Docker:** All services use `homelab_network` (external). Traefik handles reverse proxy with SSL. Authentik SSO protects services.

---

## AI Model Strategy

| Model | Role | Use For |
|-------|------|---------|
| **Claude 3.5 Sonnet** | Primary Builder | Code generation, architecture, strategic tasks |
| **GPT-4o-mini** | Verifier/Reviewer | Content review, analysis, edge case checks |
| **Perplexity** | Research Only | Real-time research with online sources (never writes code) |

**Golden Rules:**
1. Tests must be green before and after any change
2. Contracts are truth (`docs/contracts/*`) - agents must comply
3. LLMs enhance, they do not silently change structures

---

## Critical Rules

### Safety (from `.cursorrules`)

1. **Check docs first** - Read AGENTS.md, infrastructure/README.md before creating files
2. **Never duplicate** - No duplicate compose files, playbooks, or scripts
3. **Stop after 2 failures** - Ask for human intervention
4. **Test on ThinkPad first** - Always before RTX1080 production
5. **Never commit secrets** - No .env, API keys, passwords, tokens
6. **Avoid loops** - No recursive operations without explicit path limits
7. **Sequential deployment** - Never deploy to all hosts simultaneously

### Secrets

**Master location:** `/home/fitna/homelab/shared/secrets/.env.master` (not in git)

```bash
/home/fitna/homelab/shared/scripts/sync-secrets.sh  # Sync across all 3 systems
```

### Git Workflow

**Branch:** `sprint-XX/<feature-name>` → `master`

**Commit:** `<type>(<scope>): <description> (<story-points> SP)` where type is feat|fix|docs|chore|refactor

---

## Project-Specific Documentation

**IMPORTANT:** Always read the project-specific CLAUDE.md file before working on that project. This file provides cross-project overview only.

**When to use which file:**
- **Use THIS file (`/home/fitna/CLAUDE.md`)** when:
  - User hasn't specified a project yet
  - Working across multiple projects
  - Need system-wide architecture context
  - Managing secrets or sprint tracking

- **Use PROJECT file (e.g., `/home/fitna/homelab/CLAUDE.md`)** when:
  - Working within a specific project directory
  - Need detailed architecture for that project
  - Running project-specific commands
  - Understanding project-specific patterns

**Project Documentation Matrix:**

| Project | Primary Doc | Also Read | Key Focus |
|---------|-------------|-----------|-----------|
| homelab | `/home/fitna/homelab/CLAUDE.md` | `AGENTS.md`, `.cursorrules`, `infrastructure/README.md` | Docker stacks, Ansible, AI agents |
| J-Jeco | `/home/fitna/J-Jeco/AGENTS.md` | `ARCHITECTURE.md`, `BETRIEBSANLEITUNG.md` | Multi-agent content generation |
| FItnaai | `/home/fitna/FItnaai/CLAUDE.md` | `docs/contracts/*`, `README.md` | Agent framework, contracts, CLI |
| content-pipeline | `/home/fitna/content-pipeline/CLAUDE.md` | `docs/contracts/*` | Forked from FItnaai, content workflows |
| Documents | `/home/fitna/Documents/CLAUDE.md` | `docs/runbook.md`, `docs/model_strategy.md` | Planning, documentation, runbooks |

---

## Directory Structure Overview

```
/home/fitna/
├── homelab/                    # Infrastructure + AI Platform (Production)
│   ├── infrastructure/         # Docker Compose stacks, Ansible playbooks
│   ├── ai-platform/           # J-Jeco AI agents (async, LangChain)
│   ├── shared/                # Cross-system scripts, secrets, docs
│   └── CLAUDE.md              # Homelab-specific guidance (500+ lines)
│
├── J-Jeco/                    # AI Agent Platform (Production)
│   ├── 1-first-agent/         # Main agent code
│   ├── ai-agents-masterclass/ # Shared venv for homelab + J-Jeco
│   └── AGENTS.md              # J-Jeco-specific guidance
│
├── FItnaai/                   # Agent Framework (MVP1 complete)
│   ├── agents/                # Agent implementations
│   ├── docs/contracts/        # Agent contracts (source of truth)
│   ├── .venv/                 # Isolated venv
│   └── CLAUDE.md              # FItnaai-specific guidance
│
├── content-pipeline/          # Content Pipeline (Forked from FItnaai)
│   ├── agents/                # Agent implementations
│   ├── docs/contracts/        # Agent contracts
│   ├── .venv/                 # Isolated venv
│   └── CLAUDE.md              # Content-pipeline-specific guidance
│
├── Documents/                 # Planning & Documentation
│   ├── docs/                  # Runbooks, strategies, guides
│   └── CLAUDE.md              # Documentation-specific guidance
│
└── 2026 Coding/               # Experimental/snapshots (NOT active dev)
```

**Key Distinctions:**
- **homelab/** & **J-Jeco/** share venv (`ai-agents-masterclass/`), use async agents
- **FItnaai/** & **content-pipeline/** have isolated `.venv/`, use sync agents
- **Documents/** is documentation-only, no code execution
- **2026 Coding/** is archived experiments, avoid for active work

---

## Common Commands by Project

### homelab

```bash
cd /home/fitna/homelab/infrastructure/docker/stacks

# Deploy stacks
docker compose -f core.yml up -d              # Traefik + Authentik + PostgreSQL
docker compose -f monitoring.yml up -d        # Prometheus + Grafana + Loki
docker compose -f media.yml up -d             # Jellyfin + *arr suite
docker compose -f homeassistant.yml up -d     # Smart home stack

# Logs
docker compose -f <stack>.yml logs -f [service]

# Ansible
ansible-playbook -i infrastructure/ansible/inventory/hosts.yml \
  infrastructure/ansible/playbooks/00-bootstrap.yml

# AI Platform
cd /home/fitna/homelab/ai-platform/1-first-agent
source ../ai-agents-masterclass/bin/activate
python main.py                                # Interactive mode
python test_all_models.py                     # Test API connectivity
```

### FItnaai

```bash
cd /home/fitna/FItnaai
source .venv/bin/activate

# Run pipeline
fitnaai run -t "Topic" -a "Audience" -g "Newsletter"
fitnaai run -t "Topic" -a "Audience" -g "Newsletter" --dry-run  # Preview plan

# Or via script
python scripts/run_pipeline.py --topic "X" --audience "Y" --goal "Z"

# Tests
pytest tests/ -v                    # All 24 tests
pytest tests/test_happy_path.py -v  # CLI + plan tests
pytest -k "test_review" -v          # By name pattern

# Quality
pre-commit run --all-files
```

### J-Jeco

```bash
cd /home/fitna/J-Jeco/1-first-agent
source ../ai-agents-masterclass/bin/activate

python main.py                    # Interactive mode
python run_agents.py              # Multi-agent workflows
./deploy.sh                       # Deploy full stack
```

### content-pipeline

```bash
cd /home/fitna/content-pipeline
source .venv/bin/activate

# Run pipeline (CLI)
fitnaai run -t "Topic" -a "Audience" -g "Newsletter"
fitnaai run -t "Topic" -a "Audience" -g "Newsletter" --dry-run  # Preview plan

# Run pipeline (script)
python scripts/run_pipeline.py --topic "X" --audience "Y" --goal "Z"

# Tests
pytest tests/ -v                           # All tests
pytest tests/test_happy_path.py -v         # CLI + plan tests
pytest tests/test_agent_integration.py -v  # Full pipeline
pytest -k "test_review" -v                 # By name pattern

# Code quality
pre-commit run --all-files
```

---

## Troubleshooting

```bash
# Container issues
docker ps --filter "health=unhealthy"
docker logs <container-name>
docker compose -f <stack>.yml down && docker compose -f <stack>.yml up -d --force-recreate

# Health checks
docker exec postgresql pg_isready
docker exec redis redis-cli ping

# AI API
python test_all_models.py

# Network
docker network create homelab_network  # If missing
```

---

## Common Gotchas

1. **Virtual environments differ** - homelab/J-Jeco use `ai-agents-masterclass/`, FItnaai/content-pipeline use `.venv/` (see [Directory Structure](#directory-structure-overview))
2. **Async patterns vary** - homelab agents are async (`await`), FItnaai/content-pipeline agents are synchronous
3. **This is a workspace, not a repo** - Always clarify which project before working (see [Quick Start](#quick-start---first-time-here))
4. **Each project has its own CLAUDE.md** - Use project-specific docs, not just this file (see [Project-Specific Documentation](#project-specific-documentation))
5. **Multiple compose files** - Use correct stack file for your target service
6. **Ansible inventory** - Uses `hosts.yml` not `hosts.ini`
7. **Docker network required** - Run `docker network create homelab_network` if missing
8. **API keys must be synced** - Run `sync-secrets.sh` before multi-system operations
9. **ChromaDB persistence** - Data in `data/chroma_db/` - back up before deleting
10. **UFW active** - Check firewall rules before troubleshooting connectivity
11. **FItnaai has legacy files** - `agents/review_agent.py` (root) differs from `agents/review/review_agent.py`
12. **"2026 Coding" directory** - Contains snapshots/experimentation, not active development - check project directories instead
13. **System context matters** - Currently on RTX1080 (production). ThinkPad = dev, VPS = public-facing (see [3-System Architecture](#3-system-architecture))

---

## Working Across Projects

**Context Switching:**
When user switches between projects, always:
1. Confirm which project they're referring to
2. Navigate to the correct directory
3. Reference the project-specific CLAUDE.md
4. Use the correct virtual environment (see gotcha #1 below)

**Cross-Project Operations:**
Some operations span multiple projects:
- **Secrets sync** - Use `/home/fitna/homelab/shared/scripts/sync-secrets.sh` (syncs to all 3 systems)
- **Sprint tracking** - Use `/home/fitna/homelab/shared/scripts/sprint-manager.sh` (tracks across all projects)
- **Git operations** - Each project has its own repository/branch strategy

**Shared Resources:**
- API keys: `/home/fitna/homelab/shared/secrets/.env.master`
- Scripts: `/home/fitna/homelab/shared/scripts/`
- Documentation: `/home/fitna/Documents/`

---

## Sprint Tracking

```bash
# Daily workflow
/home/fitna/homelab/shared/scripts/create-daily-sheet-enhanced.sh
/home/fitna/homelab/shared/scripts/create-evening-report.sh

# Sprint management
/home/fitna/homelab/shared/scripts/sprint-manager.sh start|status|end

# View sheets
cat /home/fitna/homelab/$(date +%d.%m.%y)/DAILY_WORK_SHEET.md
```
