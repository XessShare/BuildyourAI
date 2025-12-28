# AGENTS.md - Homelab Repository Guide

**Last Updated:** 2025-12-28  
**Purpose:** Help AI agents work effectively in this homelab infrastructure repository

---

## 🏗️ Repository Overview

This is a **multi-component homelab infrastructure** combining:
- **Homelab OSS Stack**: Production-ready infrastructure with 30+ self-hosted services
- **J-Jeco AI Platform**: Multi-agent AI system for content creation and automation
- **3-System Architecture**: VPS (external), ThinkPad (192.168.16.7), RTX1080 (192.168.17.1)
- **Proxmox VE**: Virtualization layer on physical hardware

**Key Characteristics:**
- Modular Docker Compose stacks
- Infrastructure as Code (Ansible + Terraform)
- Security-first design (Traefik + Authentik SSO)
- GPU-accelerated AI workloads (RTX 1080)
- Multi-host deployment across 3 systems

---

## 📁 Repository Structure

```
/home/fitna/homelab/
├── infrastructure/              # Main homelab infrastructure
│   ├── docker/stacks/          # Docker Compose service definitions
│   ├── ansible/                # Automation playbooks & inventory
│   ├── docs/                   # Detailed documentation
│   ├── scripts/                # Utility scripts
│   ├── compose.yaml            # Root compose file (currently minimal)
│   ├── DEPLOYMENT.md           # Step-by-step deployment guide
│   ├── PROJECT_SUMMARY.md      # High-level overview
│   ├── PRE-DEPLOYMENT-CHECKLIST.md  # Deployment prerequisites
│   └── README.md               # Complete stack documentation
│
├── ai-platform/                # J-Jeco AI multi-agent system
│   ├── 1-first-agent/          # Core agent implementation
│   │   ├── main.py             # Main entry point
│   │   ├── config.py           # Agent configuration
│   │   └── requirements.txt    # Python dependencies
│   ├── ARCHITECTURE.md         # AI system architecture (500 lines)
│   ├── SETUP_GUIDE.md          # AI platform setup instructions
│   └── ai-agents-masterclass/  # Python venv
│
├── shared/                     # Cross-system shared resources
│   ├── scripts/
│   │   ├── sync-secrets.sh     # API key synchronization utility
│   │   └── snapshot.sh         # Backup/snapshot management
│   └── docs/                   # Shared documentation
│
├── brainstorm-workflow-automatisierung/  # Workflow automation POCs
│   ├── poc/prefect/            # Prefect workflow examples
│   ├── poc/n8n/                # n8n automation examples  
│   └── docs/                   # Workflow documentation
│
├── business-and-moonshot-guide/  # Strategic planning
│   ├── Business_Structuring_Guide.md
│   └── Moonshot_Brainstorm.md
│
├── .github/workflows/          # CI/CD automation
│   └── deploy.yml              # Deployment workflow
│
├── wireguard/                  # VPN configuration
│   ├── wg_confs/wg0.conf      # Main config
│   ├── server/                 # Server keys
│   └── peer1/, peer2/, peer3/  # Client configs
│
├── pihole/                     # Pi-hole DNS/ad-blocking
│   ├── etc-pihole/            # Pi-hole configuration
│   └── etc-dnsmasq.d/         # dnsmasq configuration
│
├── prometheus/                 # Monitoring configs
│   └── prometheus.yml/
│
├── docker-compose.yml          # Root-level compose (minimal)
├── SCHLACHTPLAN_2025.md        # Strategic roadmap
├── SSH_SETUP_GUIDE.md          # SSH key setup instructions
├── GAMING_PC_CONFIGURATION.md  # Gaming PC specific config
├── GAMING_PC_DEPLOYMENT_GUIDE.md
└── CODERABBIT_DEPLOYMENT_PROMPT.md  # CodeRabbit AI integration guide
```

---

## 🐳 Docker & Container Management

### Docker Compose Stacks

The infrastructure uses **multiple compose files** organized by function:

```bash
# Stack locations
/home/fitna/homelab/infrastructure/docker/stacks/

# Available stacks (ls output):
automation.yml        # Pi-hole, n8n, Ollama
core-hostA.yml        # Traefik, Authentik, Portainer (ThinkPad)
core-hostB.yml        # PostgreSQL, Redis (RTX1080)
core-phase1.yml       # Phased deployment approach
core.yml              # Combined core services
gaming-pc-ai.yml      # Gaming PC specific AI workloads
homeassistant.yml     # Smart home (HA, MQTT, Zigbee2MQTT, Node-RED)
media.yml             # Jellyfin, Sonarr, Radarr, qBittorrent
monitoring.yml        # Prometheus, Grafana, Loki, Uptime Kuma
scripts/              # Helper scripts for stack management
```

### Essential Docker Commands

```bash
# Navigate to stack directory
cd /home/fitna/homelab/infrastructure/docker/stacks

# Deploy a stack
docker compose -f <stack-name>.yml up -d

# View logs
docker compose -f <stack-name>.yml logs -f [service-name]

# Restart services
docker compose -f <stack-name>.yml restart [service-name]

# Stop and remove
docker compose -f <stack-name>.yml down

# Check status
docker compose -f <stack-name>.yml ps

# View all running containers
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# Check container resource usage
docker stats

# Create required network (if not exists)
docker network create homelab_network
```

### Important Docker Patterns

**Network:** All services use `homelab_network` for inter-container communication

**Labels:** Services use Traefik labels for automatic routing:
```yaml
labels:
  - "traefik.enable=true"
  - "traefik.http.routers.SERVICE.rule=Host(`SERVICE.${DOMAIN}`)"
  - "traefik.http.routers.SERVICE.entrypoints=websecure"
  - "traefik.http.routers.SERVICE.tls.certresolver=cloudflare"
  - "traefik.http.routers.SERVICE.middlewares=authentik@file"
```

**Environment Variables:** Loaded from `.env` files (NOT in version control)

---

## 🤖 Ansible Automation

### Inventory

```bash
# Location
/home/fitna/homelab/infrastructure/ansible/inventory/hosts.yml

# Hosts defined
- pve-thinkpad: 192.168.16.7 (lightweight node, 4 cores, 8GB RAM)
- pve-ryzen: 192.168.17.1 (main host, 8 cores, 32GB RAM)
```

### Playbooks

```bash
# Bootstrap playbook - initial host setup
ansible-playbook -i ansible/inventory/hosts.yml ansible/playbooks/00-bootstrap.yml

# What it does:
# - Updates packages
# - Configures UFW firewall
# - Sets timezone to Europe/Berlin
# - Creates 4GB swap file
# - Hardens SSH (key-only auth)
# - Installs: vim, git, curl, wget, htop, ufw, fail2ban, rsync

# Test inventory connectivity
ansible all -i ansible/inventory/hosts.yml -m ping

# Check UFW status on all hosts
ansible all -i ansible/inventory/hosts.yml -m shell -a "ufw status"
```

### Ansible Variables

```yaml
# Global defaults (from inventory)
ansible_user: root
ansible_python_interpreter: /usr/bin/python3
timezone: Europe/Berlin
docker_version: "24.0"
compose_version: "2.23.0"
```

---

## 🎯 AI Platform (J-Jeco)

### Python Environment

```bash
# Location
cd /home/fitna/homelab/ai-platform/1-first-agent

# Virtual environment (already exists)
source ../ai-agents-masterclass/bin/activate

# Install/update dependencies
pip install -r requirements.txt

# Main dependencies (from requirements.txt):
# LLM & AI Frameworks:
# - openai>=1.0.0
# - anthropic>=0.18.0
# - google-generativeai>=0.3.0
# - langchain>=0.1.0
# - langchain-openai>=0.0.5
# - langchain-anthropic>=0.1.0
# - langchain-google-genai>=1.0.0
#
# Data & Async:
# - numpy>=1.24.0
# - pandas>=2.0.0
# - asyncio>=3.4.3
#
# Environment & API:
# - python-dotenv>=1.0.0
# - requests>=2.31.0
# - httpx>=0.25.0
#
# Utilities:
# - pydantic>=2.0.0
# - tenacity>=8.2.0
#
# Vector Database:
# - chromadb>=0.4.0
# - sentence-transformers>=2.0.0
#
# Optional:
# - watchdog>=3.0.0  # File monitoring
# - cairosvg>=2.7.0  # SVG to PNG conversion
```

### Testing AI Agents

```bash
# Test all configured LLMs and API connectivity
cd /home/fitna/homelab/ai-platform/1-first-agent
python test_all_models.py

# Test individual agents
python test_analyst.py           # Test Analyst agent
python test_content_creator.py   # Test Content Creator agent
python test_researcher.py        # Test Researcher agent
python test_verifier.py          # Test Verifier agent

# Test specific functionality
python test_knowledge_base.py    # Test knowledge base integration
python test_visualization.py     # Test visualization generation
python test_deployment.py        # Test deployment orchestration (mock)
python test_deployment_mock.py   # Test deployment mock scenarios
python test_resource_management.py  # Test resource management (uses pytest)

# Test utilities
python test_telegram_notifier.py # Test Telegram notifications
python test_avatar_video.py      # Test avatar video generation

# Interactive model testing
python chat_with_model.py        # Chat interface for testing models

# Note: Some tests use pytest (test_resource_management.py), most use asyncio
# Run pytest tests with:
# python -m pytest test_resource_management.py -v
```

### Running AI Agents

```bash
# From ai-platform/1-first-agent directory
python main.py <command>

# Available commands:
python main.py                              # Start interactive mode
python main.py optimize-prompt "..."        # Optimize a prompt for clarity
python main.py plan-project "..."           # Create action plan for a project
python main.py simplify "..."               # Simplify technical text for non-tech audience
python main.py moonshot-check               # Check progress towards moonshot goal
python main.py interactive                  # Explicitly start interactive mode

# Examples:
python main.py optimize-prompt "mach mal content"
python main.py plan-project "Erstes Tutorial-Video erstellen"
python main.py moonshot-check
python main.py simplify "Kubernetes verwendet einen deklarativen Ansatz..."

# Interactive mode commands:
# Once in interactive mode (no args), use:
# - optimize   : Prompt optimieren
# - plan       : Projekt planen
# - simplify   : Tech-Content vereinfachen
# - moonshot   : Progress checken
# - help       : Show help
# - quit/exit  : Exit interactive mode
```

### API Key Management

**CRITICAL:** API keys are stored in `.env` files, **NOT** in Git

```bash
# Sync API keys across all 3 systems
/home/fitna/homelab/shared/scripts/sync-secrets.sh

# Master secrets location (default)
# ~/J-Jeco/.env.master or /home/fitna/homelab/shared/secrets/.env.master

# Systems defined in sync script:
# - vps: jonas-homelab-vps
# - rtx1080: 192.168.17.1  
# - thinkpad: pve-thinkpad

# Required API keys:
# Infrastructure (Homelab OSS Stack):
# - CLOUDFLARE_EMAIL
# - CLOUDFLARE_API_KEY
# - AUTHENTIK_SECRET_KEY
# - AUTHENTIK_POSTGRESQL_PASSWORD
# - POSTGRES_PASSWORD
# - PIHOLE_PASSWORD
# - GRAFANA_ADMIN_PASSWORD

# AI Platform (J-Jeco):
# - OPENAI_API_KEY
# - ANTHROPIC_API_KEY
# - GOOGLE_API_KEY
# - PERPLEXITY_API_KEY
# - TELEGRAM_BOT_TOKEN (optional)
# - HEYGEN_API_KEY (optional)
```

### AI System Architecture

Three-tier deployment:
- **VPS (91.107.198.37):** Lightweight agents (Communicator, Project Manager)
- **ThinkPad (192.168.16.7):** Development & testing
- **RTX1080 (192.168.17.1):** Heavy agents (Content Creator, GPU workloads)

---

## 🔐 Security & Access

### SSH Access

```bash
# Host mapping
pve-thinkpad    → 192.168.16.7
pve-ryzen       → 192.168.17.1
jonas-homelab-vps → [EXTERNAL_VPS_IP]

# SSH config expected at: ~/.ssh/config
# Key-based auth only (passwords disabled)
```

### Firewall (UFW)

```bash
# Ports allowed (configured by Ansible):
22    - SSH
80    - HTTP (redirects to 443)
443   - HTTPS
8006  - Proxmox Web UI
2377  - Docker Swarm management
7946  - Docker Swarm communication
4789  - Docker overlay network

# Check firewall status
ssh root@192.168.16.7 "ufw status verbose"
```

### SSO (Authentik)

- All services protected by Authentik SSO + 2FA
- Access at: `https://auth.${DOMAIN}`
- OIDC/SAML integration for compatible services

---

## 📊 Monitoring & Observability

### Prometheus Metrics

```bash
# Config location
/home/fitna/homelab/prometheus/prometheus.yml

# Scraped targets:
- prometheus:9090 (self)
- node-exporter:9100 (host metrics)
- cadvisor:8080 (container metrics)
- traefik:8080 (proxy metrics)
```

### Grafana Dashboards

Recommended dashboards (to import):
- Node Exporter Full (ID: 1860)
- Docker Container & Host (ID: 893)
- Traefik 2 (ID: 11462)

### Logs

```bash
# Docker Compose logs
docker compose -f <stack>.yml logs -f [service]

# System logs
/var/log/homelab-*.log

# Traefik logs
docker exec traefik cat /var/log/traefik/access.log
```

---

## 🚀 Deployment Workflow

### Pre-Deployment Checklist

1. **Environment Setup**
   ```bash
   # Copy and configure
   cp .env.example .env
   nano .env  # Fill in required values
   ```

2. **Network Creation**
   ```bash
   # On each host
   docker network create homelab_network
   ```

3. **Firewall Configuration**
   ```bash
   # Allow inter-host communication
   ssh root@192.168.16.7 "ufw allow from 192.168.17.0/24"
   ssh root@192.168.17.1 "ufw allow from 192.168.16.0/24"
   ```

4. **Secrets Sync**
   ```bash
   /home/fitna/homelab/shared/scripts/sync-secrets.sh
   ```

### Deployment Sequence

```bash
# Phase 1: Bootstrap Infrastructure (Ansible)
cd /home/fitna/homelab/infrastructure/ansible
ansible-playbook -i inventory/hosts.yml playbooks/00-bootstrap.yml

# Phase 2: Deploy Core Services
cd /home/fitna/homelab/infrastructure/docker/stacks

# On Host B (192.168.17.1): Database layer
ssh root@192.168.17.1
cd /opt/homelab
docker compose -f core-hostB.yml up -d

# Verify databases
docker exec postgresql pg_isready
docker exec redis redis-cli ping

# On Host A (192.168.16.7): Core services
ssh root@192.168.16.7
cd /opt/homelab
docker compose -f core-hostA.yml up -d

# Verify Traefik
curl -f http://localhost:8080

# Phase 3: Application Stacks (deploy in order)
docker compose -f monitoring.yml up -d     # First: for observability
docker compose -f homeassistant.yml up -d  # Smart home
docker compose -f media.yml up -d          # Media services
docker compose -f automation.yml up -d     # Automation tools
```

### CI/CD (GitHub Actions)

```bash
# Workflow file
/home/fitna/homelab/.github/workflows/deploy.yml

# Triggered on:
- Push to main/master branch
- Manual workflow dispatch

# Required GitHub Secrets:
- VPS_WEBHOOK_URL
- DEPLOY_TOKEN
- HEALTH_CHECK_URL (optional)

# Workflow steps:
1. Validate secrets
2. Trigger VPS webhook (with retry)
3. Wait for deployment (health check)
4. Auto-rollback on failure
```

---

## 🛠️ Common Tasks & Scripts

### Backup & Snapshots

```bash
# Snapshot script
/home/fitna/homelab/shared/scripts/snapshot.sh

# Create backup (manual)
/opt/homelab/scripts/backup.sh

# Restic backups (if configured)
restic snapshots                    # List backups
restic restore SNAPSHOT_ID --target /restore  # Restore
```

### Database Initialization

```bash
# PostgreSQL init script
/home/fitna/homelab/infrastructure/docker/stacks/scripts/init-databases.sh

# Creates databases for:
- Authentik
- n8n (optional)
```

### System Validation

```bash
# Pre-deployment validation script (from PRE-DEPLOYMENT-CHECKLIST.md)
# Creates script to check:
# - .env file exists
# - SSH access to both hosts
# - Docker running on both hosts
# - homelab_network exists
```

---

## 🔍 Troubleshooting

### Container Won't Start

```bash
# Check logs
docker logs <container-name>

# Restart container
docker restart <container-name>

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

# Access Traefik dashboard
https://traefik.${DOMAIN}
```

### Authentik SSO Failing

```bash
# Check logs
docker logs authentik-server

# Test ForwardAuth endpoint
curl -v http://authentik-server:9000/outpost.goauthentik.io/auth/traefik
```

### VPN Issues (qBittorrent)

```bash
# Check Gluetun logs
docker logs gluetun

# Verify VPN IP
docker exec gluetun curl ifconfig.me
# Should show VPN IP, not home IP

# Restart VPN
docker restart gluetun
```

### Service Health Checks

```bash
# PostgreSQL
docker exec postgresql pg_isready -U ${POSTGRES_USER}

# Redis
docker exec redis redis-cli ping

# Traefik
curl -f http://localhost:8080

# Check all container health
docker ps --filter "health=unhealthy"
```

---

## 📚 Important Documentation Files

### Must-Read Before Making Changes

1. **infrastructure/README.md** - Complete infrastructure documentation
2. **infrastructure/DEPLOYMENT.md** - Step-by-step deployment
3. **infrastructure/PRE-DEPLOYMENT-CHECKLIST.md** - Critical pre-deployment steps
4. **ai-platform/ARCHITECTURE.md** - AI system architecture
5. **SCHLACHTPLAN_2025.md** - Strategic roadmap

### Architecture Diagrams

```
Internet → Cloudflare Tunnel → Traefik → Authentik → Applications
                                    ↓
                            homelab_network
                                    ↓
                     ┌──────────────┴──────────────┐
                     ↓                             ↓
            Host A (ThinkPad)              Host B (RTX1080)
            - Traefik                      - PostgreSQL
            - Authentik                    - Redis
            - Home Assistant               - Heavy AI workloads
            - Monitoring                   - GPU processing
```

---

## 🎨 Code Conventions & Patterns

### Docker Compose

- **Networks:** Always use `homelab_network` for service communication
- **Environment:** Load from `.env` files with `${VARIABLE}` syntax
- **Healthchecks:** Include for critical services (databases, proxies)
- **Restart Policy:** Use `restart: unless-stopped` for production services

### Naming Conventions

- **Containers:** `service-name` (lowercase, hyphenated)
- **Networks:** `homelab_network`
- **Volumes:** `service-name_data`
- **Hosts:** `pve-<description>` (e.g., pve-thinkpad, pve-ryzen)

### File Organization

- **Compose stacks:** Group by function, not by technology
- **Scripts:** Executable (`chmod +x`), include shebang, use `set -e`
- **Docs:** Markdown with clear headings, examples, and troubleshooting

### Environment Variables

**NEVER commit these to Git:**
- API keys
- Passwords
- Tokens
- Private keys

**Always use:**
- `.env` files (in `.gitignore`)
- `sync-secrets.sh` for distribution
- Strong passwords (minimum 32 chars)

---

## 🚨 Critical Warnings

### DO NOT

- ❌ Commit `.env` files to Git
- ❌ Run `docker compose down` without checking data persistence
- ❌ Deploy to production without testing on staging
- ❌ Change database passwords without updating all dependent services
- ❌ Disable firewall without understanding implications
- ❌ Push to remote repositories without explicit request

### ALWAYS

- ✅ Read service logs before and after changes
- ✅ Test SSH access before running remote commands
- ✅ Create snapshots/backups before major changes
- ✅ Verify health checks after deployments
- ✅ Use exact whitespace/indentation when editing YAML
- ✅ Check git status before committing

---

## 🎯 Agent-Specific Guidance

### When Working with Docker Compose

1. **Read the compose file first** - Understand dependencies and volumes
2. **Check .env requirements** - Verify all variables are set
3. **Test connectivity** - Ensure networks and hosts are reachable
4. **Monitor logs** - Use `docker compose logs -f` during changes
5. **Verify health** - Check `docker ps` health status after deployment

### When Modifying Infrastructure

1. **Read infrastructure/DEPLOYMENT.md** - Understand the full deployment flow
2. **Check PRE-DEPLOYMENT-CHECKLIST.md** - Ensure prerequisites are met
3. **Use Ansible for host changes** - Don't manually SSH and modify
4. **Test on ThinkPad first** - Use development host before production
5. **Document changes** - Update relevant .md files

### When Working with AI Platform

1. **Activate venv first** - `source ai-agents-masterclass/bin/activate`
2. **Check .env.master** - Ensure API keys are synchronized
3. **Test API connectivity** - Run `python main.py moonshot-check`
4. **Respect system roles** - VPS=lightweight, ThinkPad=dev, RTX1080=heavy

### When Troubleshooting

1. **Check logs first** - Docker logs, system logs, application logs
2. **Verify basics** - Network, firewall, DNS, connectivity
3. **Test incrementally** - Isolate the failing component
4. **Document findings** - Update troubleshooting sections
5. **Preserve evidence** - Don't immediately restart failing services

---

## 📞 Quick Reference Commands

```bash
# Most common operations
cd /home/fitna/homelab/infrastructure/docker/stacks
docker compose -f core.yml ps                    # Check status
docker compose -f core.yml logs -f traefik       # View logs
docker compose -f core.yml restart <service>     # Restart service
docker compose -f core.yml up -d                 # Deploy/update

# Ansible operations
cd /home/fitna/homelab/infrastructure/ansible
ansible all -i inventory/hosts.yml -m ping       # Test connectivity
ansible-playbook -i inventory/hosts.yml playbooks/00-bootstrap.yml  # Bootstrap

# AI platform
cd /home/fitna/homelab/ai-platform/1-first-agent
source ../ai-agents-masterclass/bin/activate
python main.py <command>

# Secrets sync
/home/fitna/homelab/shared/scripts/sync-secrets.sh

# System health
docker ps --filter "health=unhealthy"
docker stats --no-stream
```

---

## 🔄 Version Information

**Current State:**
- Proxmox VE: 8.x
- Docker: 24.0+
- Docker Compose: 2.23.0+
- Traefik: v3.0
- Python: 3.13+
- Ansible: 2.15+

**Current Git State:**
Check `git status` to see any uncommitted changes, modified files, and untracked directories before deployment.

---

## 📂 Additional Project Components

### Workflow Automation (Brainstorm)

```bash
# Location
/home/fitna/homelab/brainstorm-workflow-automatisierung/

# Contains proof-of-concepts for:
# - Prefect workflows
# - n8n automation
# - GitHub to GitLab synchronization

# Example Prefect flow
cd /home/fitna/homelab/brainstorm-workflow-automatisierung/poc/prefect
# (Check for requirements.txt and setup instructions)
```

### WireGuard VPN Configuration

```bash
# Location
/home/fitna/homelab/wireguard/

# Configuration files:
wireguard/wg_confs/wg0.conf       # Main WireGuard config
wireguard/server/                  # Server keys
wireguard/peer1/, peer2/, peer3/  # Client configurations

# Each peer directory contains:
# - peer.conf       # Client-specific config
# - peer.png        # QR code for mobile setup
# - presharedkey    # Pre-shared key for additional security
# - privatekey      # Client private key
# - publickey       # Client public key (peer1 only shows this)

# CoreDNS configuration
wireguard/coredns/Corefile         # DNS configuration for VPN
```

### Business Strategy Documents

```bash
# Location
/home/fitna/homelab/business-and-moonshot-guide/

# Strategic planning documents:
Business_Structuring_Guide.md    # Business structure and planning
Moonshot_Brainstorm.md           # Long-term vision and goals
```

### Gaming PC Configuration

```bash
# Gaming-specific deployment configurations
/home/fitna/homelab/GAMING_PC_CONFIGURATION.md
/home/fitna/homelab/GAMING_PC_DEPLOYMENT_GUIDE.md

# AI workloads for gaming PC
/home/fitna/homelab/infrastructure/docker/stacks/gaming-pc-ai.yml
```

---

## 🏁 Getting Started Checklist

For agents beginning work in this repository:

1. [ ] Read this AGENTS.md completely
2. [ ] Read infrastructure/README.md for full context
3. [ ] Review HOMELAB_SCHLACHTPLAN.md and MIGRATION-PLAN.md in /home/fitna for strategic context
4. [ ] Check git status and understand current changes
5. [ ] Verify you can access both Proxmox hosts (192.168.16.7, 192.168.17.1)
6. [ ] Understand the 3-system architecture (VPS, ThinkPad, RTX1080)
7. [ ] Know which compose stack you'll be working with
8. [ ] Check if .env file exists and is properly configured
9. [ ] Understand the deployment workflow before making changes
10. [ ] Review recent commit history for context
11. [ ] Ask clarifying questions if deployment targets are ambiguous

---

## 📋 Additional Context Files

### Parent Directory Documentation

```bash
# Strategic planning (in /home/fitna/)
/home/fitna/HOMELAB_SCHLACHTPLAN.md  # Master infrastructure plan
/home/fitna/MIGRATION-PLAN.md        # Consolidation and migration strategy

# System diagnostic script
/home/fitna/diagnose_toshiba.sh      # Toshiba drive diagnostics

# Key points from these files:
# - 3-system architecture: VPS (external), ThinkPad (192.168.16.7), RTX1080 (192.168.17.1)
# - Proxmox VE as virtualization layer
# - Docker-based service deployment
# - J-Jeco AI platform integration with homelab infrastructure
# - Unified secret management across systems
```

---

## 📊 Daily Progress Tracking System

### Overview

This repository uses a comprehensive daily tracking system for monitoring progress across all projects (Agents, J-Jeco, Homelab).

### Daily Workflow Scripts

**Location:** `/home/fitna/homelab/shared/scripts/`

#### Create Daily Work Sheet (Enhanced Multi-Project)
```bash
# Create today's work sheet with project-specific tracking
/home/fitna/homelab/shared/scripts/create-daily-sheet-enhanced.sh

# Output: /home/fitna/homelab/DD.MM.YY/DAILY_WORK_SHEET.md
```

**Features:**
- ✅ Multi-project progress tracking (Agents, J-Jeco, Homelab)
- ✅ Project-specific task lists
- ✅ Time tracking per session (Morning/Afternoon/Evening)
- ✅ Cross-project integration tasks
- ✅ Visual progress bars (each █ = 5%)
- ✅ Blocker tracking with resolution history
- ✅ End-of-day summary with metrics

#### Generate Evening Report
```bash
# Analyze today's work and generate comprehensive report
/home/fitna/homelab/shared/scripts/create-evening-report.sh

# Output: /home/fitna/homelab/DD.MM.YY/EVENING_REPORT.md
```

**Features:**
- 📊 Automated task completion statistics
- 📈 Project-specific progress breakdown (Agents, J-Jeco, Homelab)
- 🎯 Performance analysis with recommendations
- 🔮 Tomorrow's preparation checklist
- 📎 Historical context and trends

### Daily Routine

#### Morning (Start of Day)
```bash
# 1. Create new daily sheet
/home/fitna/homelab/shared/scripts/create-daily-sheet-enhanced.sh

# 2. Review previous day's evening report
cat /home/fitna/homelab/$(date -d "yesterday" +%d.%m.%y)/EVENING_REPORT.md

# 3. Edit today's work sheet
nano /home/fitna/homelab/$(date +%d.%m.%y)/DAILY_WORK_SHEET.md

# 4. Set top 3 priorities
# 5. Update progress baselines
```

#### Throughout Day
- ✅ Check boxes `[ ]` → `[x]` as tasks complete
- ✅ Update progress bars periodically
- ✅ Document blockers immediately
- ✅ Move completed tasks to "Completed Tasks" section
- ✅ Track time per session

#### Evening (End of Day)
```bash
# 1. Complete all sections in DAILY_WORK_SHEET.md
# 2. Fill out "End of Day Summary"
# 3. Generate evening report
/home/fitna/homelab/shared/scripts/create-evening-report.sh

# 4. Review report
cat /home/fitna/homelab/$(date +%d.%m.%y)/EVENING_REPORT.md

# 5. Plan tomorrow's top 3 priorities
```

### Project-Specific Tracking

The enhanced daily sheets track progress separately for:

#### 🤖 AI Agents Project
- **Location:** `/home/fitna/J-Jeco/`
- **Focus:** Agent development, AGENTS.md updates, testing
- **Tasks:** Agent functionality, configurations, documentation

#### 🚀 J-Jeco Platform
- **Location:** `/home/fitna/homelab/ai-platform/1-first-agent/`
- **Focus:** LLM integration, workflows, knowledge base
- **Tasks:** Agent workflows, API integrations, ChromaDB management

#### 🏗️ Homelab Infrastructure
- **Location:** `/home/fitna/homelab/infrastructure/`
- **Focus:** Service deployment, health monitoring, integration
- **Tasks:** Docker stacks, Ansible playbooks, system maintenance

### Progress Visualization

**Progress Bar Syntax:**
```
Empty:    [░░░░░░░░░░░░░░░░░░░░] 0%
25%:      [█████░░░░░░░░░░░░░░░] 25%
50%:      [██████████░░░░░░░░░░] 50%
75%:      [███████████████░░░░░] 75%
Complete: [████████████████████] 100%
```

Each █ represents 5% progress (20 blocks total).

### Status Icons

**Task Status:**
- ⚪ Not Started
- 🟡 In Progress
- 🟢 Completed
- 🔴 Blocked
- 🔵 Waiting
- 🟣 On Hold

**Priority Levels:**
- 🔥 Critical
- ⚡ High
- ⭐ Medium
- 📌 Low
- 💡 Optional

**Project Categories:**
- 🤖 AI Agents
- 🚀 J-Jeco Platform
- 🏗️ Homelab Infrastructure
- 📚 Documentation
- 🔐 Security
- 🧪 Testing

### Evening Report Analysis

The evening report automatically:
1. **Counts tasks** (total, completed, pending)
2. **Calculates completion percentage**
3. **Filters by project** (agents, J-Jeco, homelab keywords)
4. **Extracts blockers** from work sheet
5. **Summarizes learnings** and notes
6. **Generates performance score** with recommendations
7. **Prepares tomorrow's focus** items

**Performance Ratings:**
- 🟢 **Excellent** (80-100%): Maintain workflow
- 🟡 **Good** (60-79%): Keep momentum
- 🟠 **Moderate** (40-59%): Review priorities
- 🔴 **Needs Improvement** (<40%): Address blockers

### Quick Access Commands

```bash
# View today's work sheet
cat /home/fitna/homelab/$(date +%d.%m.%y)/DAILY_WORK_SHEET.md

# Edit today's work sheet
nano /home/fitna/homelab/$(date +%d.%m.%y)/DAILY_WORK_SHEET.md

# View today's evening report
cat /home/fitna/homelab/$(date +%d.%m.%y)/EVENING_REPORT.md

# View yesterday's evening report
cat /home/fitna/homelab/$(date -d "yesterday" +%d.%m.%y)/EVENING_REPORT.md

# List all daily directories
ls -ld /home/fitna/homelab/[0-9][0-9].*
```

### Integration with Git

The daily sheets and reports are **not committed to Git** (they're in `.gitignore`), but they serve as:
- 📊 **Local progress tracking** for personal productivity
- 🔍 **Debugging reference** when issues arise
- 📈 **Historical analysis** of work patterns
- 📝 **Documentation source** for commit messages

**Best Practice:**  
Use evening reports to write meaningful commit messages capturing the day's work.

### Related Documentation

- **Progress Tracking Guide:** `/home/fitna/homelab/shared/docs/PROGRESS_TRACKING_GUIDE.md`
- **Strategic Plan:** `/home/fitna/homelab/SCHLACHTPLAN_V2.md`
- **Project Status:** Various `PROJECT_STATUS.md` files in project directories

---

**End of AGENTS.md**

**Remember:** This is a production homelab serving real users. Always test changes on ThinkPad (dev) before deploying to RTX1080 (production) or VPS (public). When in doubt, read the detailed documentation in `infrastructure/docs/` and create snapshots before major changes.
