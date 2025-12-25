# AGENTS.md - Homelab Repository Guide

**Last Updated:** 2025-12-25  
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
│   └── docs/                   # Workflow documentation
│
├── .github/workflows/          # CI/CD automation
│   └── deploy.yml              # Deployment workflow
│
├── wireguard/                  # VPN configuration
├── pihole/                     # Pi-hole DNS/ad-blocking
├── prometheus/                 # Monitoring configs
├── docker-compose.yml          # Root-level compose (minimal)
├── SCHLACHTPLAN_2025.md        # Strategic roadmap
└── SSH_SETUP_GUIDE.md          # SSH key setup instructions
```

---

## 🐳 Docker & Container Management

### Docker Compose Stacks

The infrastructure uses **multiple compose files** organized by function:

```bash
# Stack locations
/home/fitna/homelab/infrastructure/docker/stacks/

# Core infrastructure
core-hostA.yml        # Traefik, Authentik, Portainer (ThinkPad)
core-hostB.yml        # PostgreSQL, Redis (RTX1080)
core.yml              # Combined core services

# Application stacks
homeassistant.yml     # Smart home (HA, MQTT, Zigbee2MQTT, Node-RED)
media.yml             # Jellyfin, Sonarr, Radarr, qBittorrent
monitoring.yml        # Prometheus, Grafana, Loki, Uptime Kuma
automation.yml        # Pi-hole, n8n, Ollama
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

# Main dependencies
# - openai>=1.0.0
# - anthropic>=0.18.0
# - google-generativeai>=0.3.0
# - langchain>=0.1.0
# - python-dotenv>=1.0.0
```

### Running AI Agents

```bash
# From ai-platform/1-first-agent directory
python main.py <command>

# Available commands (inferred from codebase):
# - moonshot-check: Verify API connectivity
# - plan-project: Create project plans
# (Check main.py or config.py for full command list)
```

### API Key Management

**CRITICAL:** API keys are stored in `.env` files, **NOT** in Git

```bash
# Sync API keys across all 3 systems
/home/fitna/homelab/shared/scripts/sync-secrets.sh

# Creates/syncs these files:
# - Master: ~/J-Jeco/.env.master (source of truth)
# - Distributed to: VPS, ThinkPad, RTX1080

# Required API keys:
# - OPENAI_API_KEY
# - ANTHROPIC_API_KEY
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

## 🏁 Getting Started Checklist

For agents beginning work in this repository:

1. [ ] Read this AGENTS.md completely
2. [ ] Read infrastructure/README.md for full context
3. [ ] Check git status and understand current changes
4. [ ] Verify you can access both Proxmox hosts (192.168.16.7, 192.168.17.1)
5. [ ] Understand the 3-system architecture (VPS, ThinkPad, RTX1080)
6. [ ] Know which compose stack you'll be working with
7. [ ] Check if .env file exists and is properly configured
8. [ ] Understand the deployment workflow before making changes
9. [ ] Review recent commit history for context
10. [ ] Ask clarifying questions if deployment targets are ambiguous

---

**End of AGENTS.md**

**Remember:** This is a production homelab serving real users. Always test changes on ThinkPad (dev) before deploying to RTX1080 (production) or VPS (public). When in doubt, read the detailed documentation in `infrastructure/docs/` and create snapshots before major changes.
