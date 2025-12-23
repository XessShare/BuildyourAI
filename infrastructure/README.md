# Homelab OSS Stack - Production-Ready Infrastructure

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Platform](https://img.shields.io/badge/platform-Proxmox%20%7C%20Docker-orange.svg)
![Status](https://img.shields.io/badge/status-Production%20Ready-green.svg)

**Modular, reproducible, open-source homelab infrastructure for automation, smart home, multimedia, and monitoring.**

---

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Stack Components](#stack-components)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Deployment](#deployment)
- [Security](#security)
- [Monitoring](#monitoring)
- [Backup Strategy](#backup-strategy)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

---

## 🎯 Overview

This repository provides a **complete, production-ready homelab stack** using only open-source software. Designed for:

- **Automation enthusiasts** seeking Infrastructure as Code
- **Smart home users** wanting local-first control
- **Media server operators** running Jellyfin + *arr suite
- **DevOps engineers** practicing containerization at home
- **Privacy advocates** avoiding cloud dependencies

### Key Features

✅ **Modular Design** - Deploy only what you need
✅ **Docker-First** - Consistent, portable, reproducible
✅ **Security Hardened** - SSO, 2FA, encrypted backups
✅ **Fully Automated** - Ansible + Terraform + GitOps
✅ **Well Documented** - Step-by-step guides + diagrams
✅ **Cost Effective** - $0/month in software licenses

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│ External Users                                               │
└──────────────┬──────────────────────────────────────────────┘
               │
          Cloudflare Tunnel (DDoS Protection + SSL)
               │
┌──────────────▼──────────────────────────────────────────────┐
│ Proxmox VE Hypervisor (192.168.16.7 + 192.168.17.1)         │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ Traefik (Reverse Proxy + Let's Encrypt)              │  │
│  │  └─ Authentik (SSO + 2FA + RBAC)                     │  │
│  └──┬────────────────────────────────────────────────────┘  │
│     │                                                        │
│  ┌──▼─────────────────────────────────────────────────────┐ │
│  │ Core Services (Docker Compose)                         │ │
│  │  ├─ Home Assistant (Smart Home Hub)                    │ │
│  │  ├─ Jellyfin (Media Server)                            │ │
│  │  ├─ Nextcloud (File Sync)                              │ │
│  │  ├─ *arr Suite (Sonarr/Radarr/Prowlarr)                │ │
│  │  └─ qBittorrent + Gluetun (Downloads + VPN)            │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ Observability Stack                                    │  │
│  │  ├─ Prometheus + Grafana (Metrics + Dashboards)       │  │
│  │  ├─ Loki + Promtail (Log Aggregation)                 │  │
│  │  ├─ Uptime Kuma (Status Page)                          │  │
│  │  └─ Netdata (Real-time Monitoring)                     │  │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ IoT & Automation                                        │ │
│  │  ├─ Mosquitto (MQTT Broker)                            │ │
│  │  ├─ Zigbee2MQTT (Zigbee Bridge)                        │ │
│  │  ├─ ESPHome (DIY Sensors)                              │ │
│  │  ├─ Node-RED (Flow-based Automation)                   │ │
│  │  └─ Frigate NVR (AI Camera System)                     │ │
│  └────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────┘
               │
          Tailscale VPN (Mesh Network)
               │
┌──────────────▼──────────────────────────────────────────────┐
│ Internal Users (Encrypted Access)                            │
└──────────────────────────────────────────────────────────────┘
```

---

## 📦 Stack Components

### 1. Automation & Orchestration

| Tool | Function | Why Included |
|------|----------|--------------|
| **Ansible** | Configuration management | Idempotent, agentless, mature |
| **Terraform** | Infrastructure as Code | State management, reproducible |
| **Docker Compose** | Multi-container orchestration | Simple, portable, GitOps-ready |
| **Portainer** | Docker GUI management | Team collaboration, visual debugging |
| **n8n** | Workflow automation | Self-hosted Zapier alternative |
| **Node-RED** | IoT flow automation | Visual programming, MQTT native |

### 2. Home Assistant & IoT

| Tool | Function | Why Included |
|------|----------|--------------|
| **Home Assistant** | Smart home hub | 2000+ integrations, local-first |
| **Mosquitto** | MQTT broker | Lightweight, industry standard |
| **Zigbee2MQTT** | Zigbee to MQTT bridge | Vendor-agnostic, 5000+ devices |
| **ESPHome** | ESP32/ESP8266 firmware | YAML config, OTA updates |
| **Frigate NVR** | AI camera system | Coral TPU support, HomeKit integration |
| **Z-Wave JS UI** | Z-Wave management | Modern alternative to OpenZWave |

### 3. Multimedia & Cloud

| Tool | Function | Why Included |
|------|----------|--------------|
| **Jellyfin** | Media server | No paywalls, hardware transcoding |
| **Sonarr/Radarr** | TV/Movie PVR | Automated downloads + quality upgrades |
| **Prowlarr** | Indexer manager | Centralized search configuration |
| **qBittorrent** | Download client | VPN-compatible, web UI |
| **Nextcloud** | File sync & collaboration | Google Drive alternative |
| **PhotoPrism** | Photo management | AI tagging, facial recognition |
| **Immich** | Mobile photo backup | Google Photos alternative |
| **Audiobookshelf** | Audiobook server | Native mobile apps, podcast support |

### 4. Remote Access & Security

| Tool | Function | Why Included |
|------|----------|--------------|
| **Traefik** | Reverse proxy | Auto-discovery, Let's Encrypt native |
| **Authentik** | SSO + Identity Provider | OIDC/SAML, 2FA, LDAP |
| **Tailscale** | Mesh VPN | Zero-config, NAT traversal |
| **Cloudflare Tunnel** | Public access | No port forwarding, DDoS protection |
| **WireGuard** | VPN protocol | Fast, modern, secure |

### 5. Monitoring & Backup

| Tool | Function | Why Included |
|------|----------|--------------|
| **Prometheus** | Metrics database | Time-series, powerful querying |
| **Grafana** | Visualization | Beautiful dashboards, alerting |
| **Loki** | Log aggregation | Label-based, Grafana native |
| **Uptime Kuma** | Status page | Uptime monitoring, public pages |
| **Netdata** | Real-time monitoring | 1-second granularity, anomaly detection |
| **Restic** | Encrypted backups | Deduplication, S3-compatible |
| **Duplicati** | GUI backups | User-friendly, cloud backends |
| **Scrutiny** | Disk health | S.M.A.R.T. monitoring, alerts |

---

## ⚙️ Prerequisites

### Hardware Requirements

| Tier | CPU | RAM | Storage | Use Case |
|------|-----|-----|---------|----------|
| **Minimal** | 2 cores | 4 GB | 50 GB | Basic services (HA, monitoring) |
| **Standard** | 4 cores | 8 GB | 250 GB | + Media server (1080p) |
| **Recommended** | 6+ cores | 16 GB | 500 GB | + 4K transcoding, multiple users |
| **Enterprise** | 8+ cores | 32 GB | 2 TB | Full stack + LLMs + AI workloads |

### Software Requirements

- **OS**: Debian 12+ or Ubuntu 22.04+ (or Proxmox VE 8+)
- **Docker**: 24.0+
- **Docker Compose**: 2.20+
- **Ansible**: 2.15+ (control node)
- **Terraform**: 1.6+ (optional, for IaC)
- **Git**: 2.40+

### Network Requirements

- Static IP for homelab host (recommended)
- Domain name (for Cloudflare Tunnel + SSL)
- Ports: 22 (SSH), 80/443 (HTTP/S), 8006 (Proxmox - optional)

---

## 🚀 Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/XessShare/homelab-oss-stack.git
cd homelab-oss-stack
```

### 2. Configure Environment

```bash
cp .env.example .env
nano .env  # Edit with your settings
```

### 3. Deploy Infrastructure (Ansible)

```bash
# Install Ansible dependencies
ansible-galaxy install -r ansible/requirements.yml

# Bootstrap Proxmox hosts
ansible-playbook -i ansible/inventory/hosts.yml ansible/playbooks/00-bootstrap.yml

# Deploy Docker stack
ansible-playbook -i ansible/inventory/hosts.yml ansible/playbooks/01-docker-setup.yml
```

### 4. Deploy Services (Docker Compose)

```bash
cd docker/stacks

# Core services (Traefik + Authentik)
docker compose -f core.yml up -d

# Home Assistant stack
docker compose -f homeassistant.yml up -d

# Media stack (Jellyfin + *arr)
docker compose -f media.yml up -d

# Monitoring stack (Prometheus + Grafana)
docker compose -f monitoring.yml up -d
```

### 5. Access Services

- **Traefik Dashboard**: https://traefik.yourdomain.com
- **Authentik**: https://auth.yourdomain.com
- **Home Assistant**: https://ha.yourdomain.com
- **Jellyfin**: https://jellyfin.yourdomain.com
- **Grafana**: https://grafana.yourdomain.com

---

## 📚 Documentation

Detailed guides in [docs/](./docs):

- [01-Installation.md](./docs/01-Installation.md) - Step-by-step setup
- [02-Network-Setup.md](./docs/02-Network-Setup.md) - Traefik + DNS configuration
- [03-Security-Hardening.md](./docs/03-Security-Hardening.md) - Authentik + 2FA
- [04-Home-Assistant.md](./docs/04-Home-Assistant.md) - Smart home setup
- [05-Media-Server.md](./docs/05-Media-Server.md) - Jellyfin + *arr configuration
- [06-Monitoring.md](./docs/06-Monitoring.md) - Prometheus + Grafana dashboards
- [07-Backup-Recovery.md](./docs/07-Backup-Recovery.md) - Backup strategies + restore tests
- [08-Troubleshooting.md](./docs/08-Troubleshooting.md) - Common issues + solutions

---

## 🔒 Security

This stack implements **defense-in-depth** security:

### Layer 1: Network
- Tailscale VPN for internal access
- Cloudflare WAF for external services
- UFW firewall on all hosts
- Fail2Ban for brute-force protection

### Layer 2: Authentication
- Authentik SSO with 2FA (TOTP/WebAuthn)
- RBAC with groups and policies
- OIDC/SAML for all compatible services

### Layer 3: Encryption
- Let's Encrypt SSL for all services
- Encrypted backups (AES-256)
- Encrypted VPN tunnels

### Layer 4: Application
- Docker network isolation
- Read-only containers where possible
- Non-root users
- Security scanning (Trivy)

---

## 📊 Monitoring

Pre-configured dashboards for:

- **Host Metrics**: CPU, RAM, disk, network (Node Exporter → Prometheus)
- **Container Metrics**: cAdvisor → Prometheus
- **Application Logs**: Promtail → Loki → Grafana
- **Service Uptime**: Uptime Kuma
- **Disk Health**: Scrutiny (S.M.A.R.T. data)

Default alert rules:
- High CPU/RAM usage (>80%)
- Disk space low (<10%)
- Service down (>5 min)
- SSL certificate expiry (<14 days)
- SMART disk errors

---

## 💾 Backup Strategy

**3-2-1 Rule**: 3 copies, 2 media types, 1 offsite

### Automated Backups

```yaml
Daily:
  - Docker volumes (Restic → local NAS)
  - Home Assistant config (git push)

Weekly:
  - Proxmox VMs (PBS)
  - Full system snapshot

Monthly:
  - Offsite backup (Restic → Backblaze B2)
  - Restore test (documented)
```

### Restore Procedures

See [docs/07-Backup-Recovery.md](./docs/07-Backup-Recovery.md)

---

## 🛠️ Troubleshooting

### Common Issues

**Container won't start**
```bash
docker logs <container-name>  # Check logs
docker compose down && docker compose up -d  # Restart stack
```

**Service unreachable via Traefik**
```bash
docker exec traefik cat /var/log/traefik/access.log | grep <service>
# Check Traefik dashboard for routing errors
```

**Authentik SSO failing**
```bash
docker logs authentik-server
# Verify OIDC configuration in Authentik admin panel
```

See [docs/08-Troubleshooting.md](./docs/08-Troubleshooting.md) for detailed guides.

---

## 🤝 Contributing

Contributions welcome! Please:

1. Fork this repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file.

---

## 🙏 Acknowledgments

- [Awesome-Selfhosted](https://github.com/awesome-selfhosted/awesome-selfhosted) - Inspiration
- [TechnoTim](https://technotim.live/) - Homelab tutorials
- [LinuxServer.io](https://www.linuxserver.io/) - Quality container images
- Home Assistant Community - Endless integrations

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/XessShare/homelab-oss-stack/issues)
- **Discussions**: [GitHub Discussions](https://github.com/XessShare/homelab-oss-stack/discussions)
- **Documentation**: [docs/](./docs)

---

**Built with ❤️ for the self-hosting community**
