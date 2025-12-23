# Parallel Deployment Plan - Homelab OSS Stack

**Strategie:** Zwei-Agenten-Deployment mit Parallelisierung
**Ziel:** Beide Proxmox Hosts gleichzeitig konfigurieren + VPS-ready Traefik Setup
**Timeline:** 4-6 Stunden (mit Parallelisierung)

---

## 🎯 Deployment-Strategie

### Host-Verteilung

**Host A: pve-thinkpad (192.168.16.7)**
- Rolle: Lightweight Node (4 Cores, 8 GB RAM)
- Services:
  - Traefik (Core Reverse Proxy)
  - Authentik (SSO)
  - Home Assistant Stack
  - Pi-hole (DNS)
  - n8n (Workflow Automation)
  - Monitoring Stack

**Host B: pve-ryzen (192.168.17.1)**
- Rolle: Main Virtualization Host (8 Cores, 32 GB RAM)
- Services:
  - Ollama (LLM - benötigt mehr RAM/CPU)
  - Ollama WebUI
  - Media Stack (Jellyfin + *arr)
  - PostgreSQL (Shared Database)
  - Redis (Shared Cache)

**VPS (später einzubinden)**
- Public-facing Traefik Instance
- Cloudflare Tunnel Endpoint
- Load Balancer für beide Proxmox Hosts

---

## 🔐 IT-Sicherheits-Strategie: Domain vs. IP:Port

### ✅ EMPFOHLEN: Hybrid-Ansatz

**Phase 1: Internes Setup (JETZT)**
```
Zugriff:    IP:Port (192.168.16.7:XXXX)
Netzwerk:   Nur lokales LAN
Sicherheit: Firewall + Tailscale VPN
SSL:        Self-signed Zertifikate (temporär)
Kosten:     0 €
```

**Phase 2: VPN-Zugriff (Optional, in 1-2 Tagen)**
```
Zugriff:    .local Domain via Tailscale DNS
Netzwerk:   Tailscale Mesh VPN
Sicherheit: End-to-End encrypted
SSL:        Let's Encrypt via Tailscale
Kosten:     0 € (Tailscale Free Tier)
```

**Phase 3: Public Access (wenn Domain gekauft)**
```
Zugriff:    yourdomain.com Subdomains
Netzwerk:   Cloudflare Tunnel (kein Port Forwarding)
Sicherheit: Cloudflare WAF + Authentik 2FA
SSL:        Let's Encrypt via Cloudflare DNS
Kosten:     ~10 €/Jahr (Domain)
```

### ❌ NICHT EMPFOHLEN: Direkte Public IP Exposition
```
192.168.x.x:PORT → Internet
- Kein DDoS-Schutz
- Kein WAF
- Exponiert interne IP-Struktur
- Anfällig für Port-Scanning
```

---

## 📋 Paralleler Phasenplan

### PHASE 0: Vorbereitung (Agent 1 + 2 parallel)

**Agent 1 Tasks:**
```bash
- [ ] SSH-Keys generieren
- [ ] SSH-Keys zu pve-thinkpad deployen (192.168.16.7)
- [ ] Docker-Installation auf pve-thinkpad prüfen
- [ ] Firewall-Regeln auf pve-thinkpad konfigurieren
- [ ] Docker-Netzwerk erstellen: homelab_network
```

**Agent 2 Tasks:**
```bash
- [ ] SSH-Keys zu pve-ryzen deployen (192.168.17.1)
- [ ] Docker-Installation auf pve-ryzen prüfen
- [ ] Firewall-Regeln auf pve-ryzen konfigurieren
- [ ] Verzeichnisstruktur erstellen (/opt/homelab, /mnt/media)
```

**Synchronisierungspunkt:** Beide Hosts bereit ✅

---

### PHASE 1: Core Infrastructure (20 Minuten)

**Agent 1: Host A Setup**
```bash
# 1. Traefik Configuration erstellen
cd /g/docs/homelab-oss-stack
scp -r docker/traefik root@192.168.16.7:/opt/homelab/

# 2. Traefik Config für VPS-Integration anpassen
# (siehe Traefik VPS Config unten)

# 3. Core Stack deployen
scp docker/stacks/core.yml root@192.168.16.7:/opt/homelab/
ssh root@192.168.16.7 "cd /opt/homelab && docker compose -f core.yml up -d"

# 4. Authentik initialisieren
# Warten auf https://192.168.16.7:8080 (Traefik Dashboard)
# Warten auf https://192.168.16.7:9000 (Authentik)
```

**Agent 2: Host B Setup**
```bash
# 1. PostgreSQL + Redis deployen (benötigt für Authentik auf Host A)
# Diese Services laufen zentral auf Host B
ssh root@192.168.17.1 "docker run -d --name postgres --network homelab_network \
  -e POSTGRES_PASSWORD=changeme postgres:16-alpine"

# 2. Verzeichnisse für Media Stack vorbereiten
ssh root@192.168.17.1 "mkdir -p /mnt/media/{tv,movies,downloads}"

# 3. Monitoring-Exporters deployen
# Node Exporter für Prometheus-Monitoring
ssh root@192.168.17.1 "docker run -d --name node-exporter \
  --network homelab_network -p 9100:9100 prom/node-exporter"
```

**Synchronisierungspunkt:** Core Infrastructure läuft ✅

---

### PHASE 2: Automation Stack (30 Minuten)

**Agent 1: Pi-hole + n8n auf Host A**
```bash
# 1. Pi-hole deployen
scp docker/stacks/automation.yml root@192.168.16.7:/opt/homelab/
ssh root@192.168.16.7 "cd /opt/homelab && docker compose -f automation.yml up -d pihole n8n"

# 2. Pi-hole konfigurieren
# Browser: http://192.168.16.7:8053/admin
# Admin-Passwort aus .env verwenden

# 3. n8n initialisieren
# Browser: http://192.168.16.7:5678
# Initial Setup Wizard durchlaufen

# 4. Ersten Workflow testen (siehe Workflow unten)
```

**Agent 2: Ollama auf Host B**
```bash
# 1. Ollama deployen (benötigt mehr RAM)
scp docker/stacks/automation.yml root@192.168.17.1:/opt/homelab/
ssh root@192.168.17.1 "cd /opt/homelab && docker compose -f automation.yml up -d ollama ollama-webui"

# 2. Erstes LLM Modell pullen (z.B. Llama 3.2)
ssh root@192.168.17.1 "docker exec ollama ollama pull llama3.2"

# 3. Ollama WebUI testen
# Browser: http://192.168.17.1:8080
# Test-Prompt: "Hello, are you working?"

# 4. Ollama API testen
ssh root@192.168.17.1 "curl http://localhost:11434/api/generate -d '{
  \"model\": \"llama3.2\",
  \"prompt\": \"Why is the sky blue?\"
}'"
```

**Synchronisierungspunkt:** Automation Stack deployed ✅

---

### PHASE 3: Service Integration (45 Minuten)

**Agent 1: Home Assistant + Pi-hole Integration**
```bash
# 1. Home Assistant Stack deployen
scp docker/stacks/homeassistant.yml root@192.168.16.7:/opt/homelab/
ssh root@192.168.16.7 "cd /opt/homelab && docker compose -f homeassistant.yml up -d"

# 2. Pi-hole als DNS für Netzwerk konfigurieren
# Router-Config: Primary DNS = 192.168.16.7

# 3. Home Assistant Initial Setup
# Browser: http://192.168.16.7:8123
# Konto erstellen, Geräte-Discovery starten

# 4. MQTT in Home Assistant konfigurieren
# Integration: Mosquitto (mqtt://mosquitto:1883)
```

**Agent 2: Media Stack + Ollama Integration**
```bash
# 1. Media Stack deployen
scp docker/stacks/media.yml root@192.168.17.1:/opt/homelab/
ssh root@192.168.17.1 "cd /opt/homelab && docker compose -f media.yml up -d"

# 2. Jellyfin initialisieren
# Browser: http://192.168.17.1:8096
# Library Setup: /mnt/media/movies, /mnt/media/tv

# 3. *arr Stack konfigurieren
# Sonarr: http://192.168.17.1:8989
# Radarr: http://192.168.17.1:7878
# Prowlarr: http://192.168.17.1:9696

# 4. Ollama mit n8n verbinden (Host A → Host B)
# n8n Workflow: HTTP Request to http://192.168.17.1:11434/api
```

**Synchronisierungspunkt:** Services integriert ✅

---

### PHASE 4: Monitoring & Verification (30 Minuten)

**Agent 1: Monitoring Stack**
```bash
# 1. Monitoring Stack deployen
scp docker/stacks/monitoring.yml root@192.168.16.7:/opt/homelab/
ssh root@192.168.16.7 "cd /opt/homelab && docker compose -f monitoring.yml up -d"

# 2. Prometheus Targets konfigurieren
# Targets: Node Exporter (beide Hosts), cAdvisor, Services

# 3. Grafana Dashboards importieren
# Browser: http://192.168.16.7:3000
# Login: admin/admin (aus .env)
# Import Dashboard: 1860 (Node Exporter Full)

# 4. Uptime Kuma Status Page
# Browser: http://192.168.16.7:3001
# Monitors hinzufügen für alle Services
```

**Agent 2: Health Checks**
```bash
# 1. Container-Status prüfen auf Host B
ssh root@192.168.17.1 "docker ps --format 'table {{.Names}}\t{{.Status}}'"

# 2. Logs auf Fehler prüfen
ssh root@192.168.17.1 "docker logs ollama | tail -50"
ssh root@192.168.17.1 "docker logs jellyfin | tail -50"

# 3. Netzwerk-Konnektivität testen
ssh root@192.168.17.1 "docker exec ollama ping -c 2 192.168.16.7"

# 4. Resource Usage prüfen
ssh root@192.168.17.1 "docker stats --no-stream"
```

**Synchronisierungspunkt:** System vollständig deployed ✅

---

## 🔧 Traefik VPS-Integration Config

Erstelle diese Datei für spätere VPS-Integration:

**`docker/traefik/dynamic/vps-backend.yml`**
```yaml
# VPS Backend Configuration (für später)
# Ermöglicht Load Balancing zwischen Homelab und VPS

http:
  services:
    homelab-backend:
      loadBalancer:
        servers:
          - url: "http://192.168.16.7"  # pve-thinkpad
          - url: "http://192.168.17.1"  # pve-ryzen
        healthCheck:
          path: /health
          interval: 30s
          timeout: 5s

  middlewares:
    # IP Whitelist für VPS → Homelab Kommunikation
    vps-whitelist:
      ipWhiteList:
        sourceRange:
          - "YOUR_VPS_IP/32"
          - "192.168.16.0/24"  # Lokales Netz
          - "100.64.0.0/10"    # Tailscale Range

    # Rate Limiting für öffentliche Endpoints
    rate-limit:
      rateLimit:
        average: 100
        burst: 50
        period: 1s

  routers:
    # Router für VPS → Homelab Traffic
    vps-to-homelab:
      rule: "Host(`homelab.yourdomain.com`)"
      service: homelab-backend
      middlewares:
        - vps-whitelist
        - authentik
      tls:
        certResolver: cloudflare
```

---

## 🚀 n8n Workflow: Erster Automatisierungs-Test

**Workflow-Name:** "Ollama Status Monitor"

**Trigger:** Schedule (alle 5 Minuten)

**Nodes:**
1. **Schedule Trigger**
   - Cron: `*/5 * * * *`

2. **HTTP Request → Ollama**
   - URL: `http://192.168.17.1:11434/api/tags`
   - Method: GET
   - Returns: Liste aller geladenen Modelle

3. **IF Node**
   - Condition: `{{ $json.models.length > 0 }}`
   - True: Ollama läuft
   - False: Ollama down

4. **Webhook → Home Assistant** (True Branch)
   - URL: `http://homeassistant:8123/api/webhook/ollama_status`
   - Body: `{"status": "online", "models": "{{ $json.models.length }}"}`

5. **Email Alert** (False Branch)
   - To: Admin Email
   - Subject: "⚠️ Ollama is down!"
   - Body: "Ollama on pve-ryzen is not responding."

---

## 🔄 Synchronisierungspunkte

Beide Agenten müssen an diesen Punkten synchronisieren:

### Checkpoint 1: SSH & Docker Ready
```bash
# Agent 1 wartet auf:
ssh root@192.168.16.7 "docker --version"

# Agent 2 wartet auf:
ssh root@192.168.17.1 "docker --version"
```

### Checkpoint 2: Core Infrastructure
```bash
# Agent 1 wartet auf Traefik:
curl -k https://192.168.16.7:8080/ping

# Agent 2 wartet auf PostgreSQL:
ssh root@192.168.17.1 "docker exec postgres pg_isready"
```

### Checkpoint 3: Services Deployed
```bash
# Agent 1 überprüft:
curl http://192.168.16.7:8053  # Pi-hole
curl http://192.168.16.7:5678  # n8n

# Agent 2 überprüft:
curl http://192.168.17.1:11434/api/tags  # Ollama
curl http://192.168.17.1:8096  # Jellyfin
```

---

## 📊 Deployment-Timeline (mit 2 Agenten)

| Phase | Agent 1 (Host A) | Agent 2 (Host B) | Dauer | Gesamt |
|-------|------------------|------------------|-------|--------|
| **Phase 0** | SSH Setup + Docker Check | SSH Setup + Docker Check | 15 min | 15 min |
| **Phase 1** | Traefik + Authentik | PostgreSQL + Redis | 20 min | 35 min |
| **Phase 2** | Pi-hole + n8n | Ollama + WebUI | 30 min | 65 min |
| **Phase 3** | Home Assistant | Media Stack | 45 min | 110 min |
| **Phase 4** | Monitoring | Health Checks | 30 min | 140 min |
| **Testing** | Integration Tests | Performance Tests | 20 min | **160 min (2h 40min)** |

**Ohne Parallelisierung:** ~6-8 Stunden
**Mit Parallelisierung:** ~2h 40min
**Zeitersparnis:** 60%+

---

## ✅ Erfolgs-Kriterien

### Host A (pve-thinkpad)
- [ ] Traefik Dashboard erreichbar (Port 8080)
- [ ] Authentik Setup abgeschlossen
- [ ] Pi-hole blockiert Werbung
- [ ] Home Assistant läuft
- [ ] n8n Workflow aktiv
- [ ] Prometheus sammelt Metriken
- [ ] Grafana zeigt Dashboards

### Host B (pve-ryzen)
- [ ] Ollama antwortet auf API-Calls
- [ ] Ollama WebUI funktioniert
- [ ] Jellyfin zeigt Media Library
- [ ] Sonarr/Radarr konfiguriert
- [ ] PostgreSQL läuft stabil
- [ ] Logs zeigen keine Fehler

### Integration
- [ ] n8n kann Ollama abfragen (Host A → Host B)
- [ ] Prometheus scraped beide Hosts
- [ ] Pi-hole DNS funktioniert im Netzwerk
- [ ] Alle Container im `homelab_network`

---

## 🚨 Troubleshooting

### Problem: Container startet nicht
```bash
# Logs prüfen
docker logs <container-name>

# Restart
docker restart <container-name>

# Komplett neu
docker compose down && docker compose up -d
```

### Problem: Netzwerk-Fehler zwischen Hosts
```bash
# Connectivity testen
docker exec <container> ping 192.168.16.7
docker exec <container> ping 192.168.17.1

# Firewall prüfen
ufw status
ufw allow from 192.168.16.0/24
ufw allow from 192.168.17.0/24
```

### Problem: Traefik kann Services nicht erreichen
```bash
# Logs prüfen
docker logs traefik | grep -i error

# Netzwerk prüfen
docker network inspect homelab_network

# Labels prüfen
docker inspect <service> | grep traefik
```

---

## 📝 Nächste Schritte nach Deployment

1. **Tailscale VPN einrichten** (für remote access ohne Port Forwarding)
2. **Authentik 2FA aktivieren** (TOTP/WebAuthn)
3. **Backups konfigurieren** (Restic → NAS/Cloud)
4. **Grafana Alerts einrichten** (Telegram/Email)
5. **Domain kaufen** (später für öffentlichen Zugriff)
6. **VPS Setup** (Cloudflare Tunnel Endpoint)
7. **GitOps aktivieren** (Watchtower für Auto-Updates)

---

**Status:** ✅ Plan fertig, bereit für parallele Ausführung
**Nächster Schritt:** SSH-Keys einrichten, dann beide Agenten starten
