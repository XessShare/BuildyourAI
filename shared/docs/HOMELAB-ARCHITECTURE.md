# Unified Homelab Architecture
**Last Updated:** 2025-12-23
**Version:** 1.0
**Author:** J-Jeco AI Platform + Homelab OSS Stack

---

## 🎯 Overview

This document describes the unified architecture of two integrated projects:
1. **Homelab OSS Stack** - Infrastructure & Services
2. **J-Jeco AI Platform** - Multi-Agent AI System

Both projects share the same hardware infrastructure and leverage synergies between services.

---

## 🏗️ Multi-Host Architecture

### Host A: PVE ThinkPad (192.168.16.7)

**Hardware:**
- ThinkPad T480s
- CPU: Intel Core i5-8350U (4 cores)
- RAM: 16 GB
- Storage: 512 GB NVMe SSD
- OS: Proxmox VE 8

**Role:** Primary Services Host

**Services Running:**
- Traefik (Reverse Proxy & SSL)
- Authentik (SSO & Identity Provider)
- Portainer (Docker Management)
- AdGuard Home (DNS Ad-Blocking)
- n8n (Workflow Automation)
- Grafana (Monitoring Dashboards)
- Prometheus (Metrics Collection)
- Loki + Promtail (Log Aggregation)
- Home Assistant (Smart Home Hub)
- MQTT Mosquitto (IoT Broker)
- Zigbee2MQTT, ESPHome, Node-RED

**Rationale:**
- Lower power consumption for 24/7 services
- Reliable for critical infrastructure (DNS, SSO, monitoring)
- Direct WiFi/Bluetooth for IoT devices

---

### Host B: PVE Ryzen RTX 1080 (192.168.17.1)

**Hardware:**
- Custom Build
- CPU: AMD Ryzen (8+ cores)
- GPU: NVIDIA RTX 1080 (8 GB VRAM)
- RAM: 32 GB
- Storage: 2 TB NVMe SSD
- OS: Proxmox VE 8

**Role:** Compute-Intensive Workloads

**Services Running:**
- PostgreSQL (Shared Database)
- Redis (Cache & Session Store)
- Ollama (Local LLM Inference)
- Ollama WebUI (AI Interface)
- Jellyfin (Media Server with GPU transcoding)
- Sonarr, Radarr, Prowlarr (Media Automation)
- qBittorrent + Gluetun (Downloads via VPN)
- Frigate NVR (AI Camera System)

**Rationale:**
- GPU acceleration for:
  - LLM inference (Ollama)
  - Video transcoding (Jellyfin)
  - AI object detection (Frigate)
- Higher RAM/Storage for databases and media
- Compute power for J-Jeco AI agents

---

## 🤖 J-Jeco AI Platform Integration

### Architecture

J-Jeco is a multi-agent AI system with specialized agents:

```
┌─────────────────────────────────────────────────────────┐
│                    J-Jeco AI Platform                    │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   Content    │  │  Researcher  │  │   Analyst    │  │
│  │   Creator    │  │    Agent     │  │    Agent     │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
│         │                  │                  │          │
│         └──────────────────┼──────────────────┘          │
│                            │                             │
│                   ┌────────▼────────┐                    │
│                   │ Project Manager │                    │
│                   │     Agent       │                    │
│                   └────────┬────────┘                    │
│                            │                             │
│  ┌─────────────────────────┼─────────────────────────┐  │
│  │          Shared LLM Infrastructure                 │  │
│  │  ┌──────────────┐  ┌──────────────┐              │  │
│  │  │   OpenAI     │  │  Anthropic   │              │  │
│  │  │  (GPT-4o)    │  │   (Claude)   │              │  │
│  │  └──────────────┘  └──────────────┘              │  │
│  │                                                    │  │
│  │  ┌──────────────┐  ┌──────────────┐              │  │
│  │  │    Ollama    │  │  Perplexity  │              │  │
│  │  │  (Local LLM) │  │  (Research)  │              │  │
│  │  └──────────────┘  └──────────────┘              │  │
│  └────────────────────────────────────────────────────┘  │
└───────────────────────────────────────────────────────────┘
```

### Agent Responsibilities

1. **Content Creator Agent**
   - Newsletter generation
   - Video script writing
   - Social media posts
   - LLM: GPT-4o, Claude Sonnet

2. **Researcher Agent**
   - Web research via Perplexity
   - Information validation
   - Source aggregation
   - LLM: Perplexity, GPT-4o

3. **Analyst Agent**
   - Data analysis
   - Trend detection
   - Performance metrics
   - LLM: Claude Opus, GPT-4o

4. **Verifier Agent**
   - Fact checking
   - Quality assurance
   - Consistency validation
   - LLM: Claude Sonnet

5. **Project Manager Agent**
   - Task orchestration
   - Workflow coordination
   - Status tracking
   - LLM: GPT-4o

---

## 🔄 Service Synergies

### 1. Ollama Integration

**Homelab Usage:**
- Local inference for privacy-sensitive tasks
- Fallback when cloud APIs are unavailable
- Cost optimization for high-volume requests

**J-Jeco Usage:**
- Local LLM inference for agents
- Model: Llama 3, Mistral, CodeLlama
- GPU acceleration via RTX 1080

**Configuration:**
- Ollama API: `http://192.168.17.1:11434`
- Models stored on Host B (fast NVMe)
- Accessible from both infrastructure and AI agents

---

### 2. Monitoring Stack

**Prometheus + Grafana monitors:**
- Infrastructure health (CPU, RAM, disk, network)
- Service availability (all Docker containers)
- AI agent performance metrics
- DNS query statistics (AdGuard Home)
- Media server stats (Jellyfin)

**Dashboards:**
- Node Exporter (system metrics)
- cAdvisor (container metrics)
- AdGuard Home (DNS stats) - Grafana Dashboard 13330
- Custom J-Jeco Agent Dashboard

---

### 3. Automation Integration

**n8n Workflows:**
- Trigger J-Jeco agents on schedule
- Process agent outputs (newsletter sending, social posting)
- Monitor homelab health and alert
- Backup automation

**Node-RED:**
- Smart home automation
- IoT device orchestration
- Integration with Home Assistant

**J-Jeco can trigger:**
- Smart home scenes via Home Assistant API
- Workflow execution via n8n webhooks
- Media management via Sonarr/Radarr API

---

### 4. AdGuard Home (DNS)

**Features:**
- Network-wide ad blocking
- DNS-over-HTTPS/TLS/QUIC
- Custom DNS rewrites for internal services
- Prometheus metrics export

**Integration:**
- J-Jeco Network Agent can query DNS statistics
- Grafana dashboard for DNS analytics
- Protected by Authentik SSO
- API: `http://192.168.16.7/control/stats`

**Advantages over Pi-hole:**
- Native DoH/DoT/DoQ (no additional tools)
- Better REST API for automation
- Multi-user support
- Built-in parental controls

---

### 5. Authentik SSO

**Protected Services:**
- All Traefik-routed services
- Grafana, Portainer, n8n
- AdGuard Home, Ollama WebUI
- Jellyfin (optional)

**Authentication Methods:**
- OIDC/SAML for services
- 2FA (TOTP)
- LDAP for legacy apps

---

## 📊 Network Architecture

```
Internet
   │
   ├─ Cloudflare (DNS + SSL)
   │     │
   │     └─ Let's Encrypt SSL Certificates
   │
   ├─ Tailscale VPN (Remote Access)
   │
   ▼
Traefik Reverse Proxy (Host A: 192.168.16.7)
   │
   ├─ Authentik SSO (Authentication)
   │
   ├─────────────────────────────────────┐
   │                                     │
   ▼                                     ▼
Host A Services                    Host B Services
(Low Power, Always-On)            (High Performance, GPU)
   │                                     │
   ├─ AdGuard Home (DNS)                ├─ PostgreSQL (Database)
   ├─ Prometheus (Metrics)              ├─ Redis (Cache)
   ├─ Grafana (Dashboards)              ├─ Ollama (LLM Inference)
   ├─ Home Assistant (Smart Home)       ├─ Jellyfin (Media Server)
   ├─ n8n (Automation)                  ├─ Frigate (AI Cameras)
   └─ Portainer (Management)            └─ Media Stack (*arr + qBit)
```

---

## 🔒 Security Model

### Layers of Security

1. **Network Level**
   - Firewall (UFW on both hosts)
   - AdGuard DNS filtering
   - VPN access (Tailscale)
   - No direct port forwarding

2. **Application Level**
   - Traefik SSL termination (Let's Encrypt)
   - Authentik SSO with 2FA
   - Service-level authentication
   - Docker network isolation

3. **Data Level**
   - Encrypted backups (Restic)
   - Secrets management (.env.master)
   - No secrets in Git
   - PostgreSQL password protection

---

## 📁 Repository Structure

```
/home/fitna/homelab/
├── infrastructure/              # Homelab OSS Stack
│   ├── docker/
│   │   ├── stacks/             # Docker Compose files
│   │   │   ├── core-hostA.yml
│   │   │   ├── core-hostB.yml
│   │   │   ├── automation.yml   (AdGuard, n8n, Ollama)
│   │   │   ├── monitoring.yml
│   │   │   ├── homeassistant.yml
│   │   │   └── media.yml
│   │   ├── prometheus/          # Prometheus config
│   │   ├── grafana/             # Grafana provisioning
│   │   ├── traefik/             # Traefik config
│   │   └── mosquitto/           # MQTT config
│   ├── ansible/                 # Ansible playbooks
│   └── docs/                    # Infrastructure documentation
│
├── ai-platform/                 # J-Jeco AI Platform
│   ├── 1-first-agent/          # Multi-agent system
│   │   ├── agents/             # Agent implementations
│   │   ├── config.py           # Configuration
│   │   ├── main.py             # Entry point
│   │   └── requirements.txt
│   ├── ARCHITECTURE.md          # AI platform architecture
│   └── SETUP_GUIDE.md           # Setup instructions
│
└── shared/                      # Shared resources
    ├── secrets/
    │   └── .env.master          # Centralized secrets
    ├── scripts/
    │   ├── snapshot.sh          # Backup script
    │   └── sync-secrets.sh      # Secret sync utility
    └── docs/
        ├── ADGUARD-vs-PIHOLE.md
        ├── HOMELAB-ARCHITECTURE.md (this file)
        └── private-docs/        # User guides
```

---

## 🚀 Deployment Strategy

### Phase 1: Core Infrastructure (Host B)
1. Deploy PostgreSQL + Redis
2. Verify database connectivity

### Phase 2: Reverse Proxy & Auth (Host A)
1. Deploy Traefik with SSL
2. Deploy Authentik SSO
3. Configure OIDC providers

### Phase 3: Essential Services (Host A)
1. Deploy AdGuard Home (DNS)
2. Deploy Prometheus + Grafana
3. Deploy Portainer

### Phase 4: Home Automation (Host A)
1. Deploy Home Assistant
2. Deploy MQTT Mosquitto
3. Deploy Zigbee2MQTT, ESPHome

### Phase 5: Media & Compute (Host B)
1. Deploy Ollama + WebUI
2. Deploy Jellyfin
3. Deploy Media Stack (*arr + qBittorrent)

### Phase 6: AI Platform (Multi-Host)
1. Configure J-Jeco agents with .env.master
2. Test Ollama connectivity
3. Deploy n8n workflows

---

## 📈 Monitoring & Observability

### Metrics Collection

**Prometheus Scrape Jobs:**
- `prometheus` - Self-monitoring
- `node-exporter-hostA` - ThinkPad system metrics
- `node-exporter-hostB` - Ryzen system metrics
- `cadvisor` - Container metrics
- `traefik` - Reverse proxy stats
- `home-assistant` - Smart home metrics
- `postgres-exporter` - Database stats
- `scrutiny` - Disk health (S.M.A.R.T.)
- `adguardhome` - DNS query statistics

### Log Aggregation

**Loki + Promtail:**
- Centralized logging for all containers
- 31-day retention
- Queryable via Grafana

### Alerting

**Prometheus Alerts:**
- High CPU (>80% for 10min)
- High Memory (>90%)
- Low Disk Space (<10%)
- Service Down (uptime < 95%)

**Notification Channels:**
- Telegram (via J-Jeco Communicator Agent)
- Email (via SMTP)
- Grafana dashboards

---

## 🔧 Maintenance

### Backups

**Automated via Restic:**
- Daily: Configuration files, databases
- Weekly: Media metadata
- Monthly: Full system snapshots
- Destination: Local NAS + Backblaze B2

### Updates

**Docker Images:**
- Watchtower (auto-update non-critical services)
- Manual update: Databases, Authentik, Traefik

**System Updates:**
- Monthly: Proxmox VE updates
- Quarterly: Major version upgrades

### Monitoring

**Weekly Reviews:**
- Grafana dashboard checks
- Log review (errors, warnings)
- Disk usage trends

---

## 🎯 Future Enhancements

1. **GPU Passthrough for LLMs**
   - Direct RTX 1080 access for Ollama
   - Faster inference for J-Jeco agents

2. **High Availability**
   - PostgreSQL replication
   - Redis cluster
   - Traefik load balancing

3. **Advanced AI Workflows**
   - Voice-to-text transcription
   - Image generation (Stable Diffusion)
   - Video generation (HeyGen, D-ID)

4. **Kubernetes Migration**
   - K3s cluster for better orchestration
   - Service mesh with Istio
   - GitOps with FluxCD

---

## 📚 References

- [Homelab OSS Stack Documentation](../infrastructure/README.md)
- [J-Jeco AI Platform Architecture](../ai-platform/ARCHITECTURE.md)
- [AdGuard Home vs Pi-hole Comparison](./ADGUARD-vs-PIHOLE.md)
- [Deployment Guide](../infrastructure/DEPLOYMENT.md)
- [Secret Management Guide](../shared/scripts/sync-secrets.sh)

---

**Last Synced:** 2025-12-23
**Git Repository:** /home/fitna/homelab/
**Deployment Status:** Ready for Phase 1
