# Agent 2 Start-Prompt

**KOPIERE DIESEN TEXT IN EINEN NEUEN CLAUDE CODE CHAT:**

---

Du bist Agent 2 in einem parallelen Deployment-Projekt für ein Homelab OSS Stack.

## Deine Rolle

Du bist verantwortlich für das Deployment auf **Host B: pve-ryzen (192.168.17.1)**

Dieser Host ist der leistungsstärkere Server:
- **CPU:** 8 Cores (Ryzen)
- **RAM:** 32 GB
- **Storage:** 56 GB
- **Rolle:** Main Virtualization Host

## Deine Services

Du deployst folgende Services auf Host B:
1. **Ollama** - Local LLM Inference Engine (benötigt viel RAM)
2. **Ollama WebUI** - Browser-Interface für Ollama
3. **Media Stack** - Jellyfin + Sonarr + Radarr + Prowlarr + qBittorrent
4. **PostgreSQL** - Shared Database (auch für Authentik auf Host A)
5. **Redis** - Shared Cache (auch für Authentik auf Host A)
6. **Node Exporter** - Prometheus Monitoring

## Projektkontext

**Repository:** https://github.com/XessShare/homelab-oss-stack
**Lokaler Pfad:** G:\docs\homelab-oss-stack

**Parallelarbeit mit Agent 1:**
- Agent 1 arbeitet an Host A (192.168.16.7 - pve-thinkpad)
- Agent 1 deployt: Traefik, Authentik, Pi-hole, Home Assistant, n8n, Monitoring
- Ihr synchronisiert an festgelegten Checkpoints

## Detaillierter Arbeitsplan

Lies und folge genau diesem Plan:
**`G:\docs\homelab-oss-stack\PARALLEL_DEPLOYMENT_PLAN.md`**

Deine Aufgaben sind alle mit **"Agent 2 Tasks"** markiert.

## Start-Checklist

Bevor du beginnst, prüfe:
- [ ] Repository geklont: `cd G:\docs\homelab-oss-stack`
- [ ] SSH-Key vorhanden (Agent 1 erstellt den Key, du nutzt ihn)
- [ ] SSH-Zugang zu 192.168.17.1 funktioniert
- [ ] Docker auf 192.168.17.1 installiert
- [ ] `.env` Datei konfiguriert

## Deine ersten Befehle

```bash
# 1. Wechsle ins Projekt-Verzeichnis
cd G:\docs\homelab-oss-stack

# 2. Teste SSH-Zugang
ssh root@192.168.17.1 "echo 'SSH zu pve-ryzen erfolgreich' && hostname"

# 3. Prüfe Docker-Installation
ssh root@192.168.17.1 "docker --version && docker compose version"

# 4. Prüfe Firewall
ssh root@192.168.17.1 "ufw status"

# 5. Erstelle Docker-Netzwerk (falls noch nicht vorhanden)
ssh root@192.168.17.1 "docker network create homelab_network || echo 'Netzwerk existiert bereits'"
```

## Synchronisierungspunkte

**WICHTIG:** Warte an diesen Punkten auf Agent 1!

### Checkpoint 1: SSH & Docker Ready
Nachdem du obige Befehle erfolgreich ausgeführt hast, sage:
> "Agent 2: Checkpoint 1 erreicht - SSH und Docker auf pve-ryzen funktionieren ✅"

### Checkpoint 2: Core Infrastructure
Nachdem du PostgreSQL und Redis deployed hast, sage:
> "Agent 2: Checkpoint 2 erreicht - PostgreSQL und Redis laufen ✅"

### Checkpoint 3: Services Deployed
Nachdem Ollama und Media Stack laufen, sage:
> "Agent 2: Checkpoint 3 erreicht - Ollama und Media Stack deployed ✅"

## Deployment-Reihenfolge

Folge dieser Reihenfolge:

### Phase 0: Vorbereitung (15 min)
```bash
# SSH-Keys deployen (nutze den Key von Agent 1)
# Docker Check
# Firewall konfigurieren
# Verzeichnisse erstellen
```

### Phase 1: Core Infrastructure (20 min)
```bash
# PostgreSQL deployen (für Authentik auf Host A)
# Redis deployen (für Authentik auf Host A)
# Node Exporter deployen (für Prometheus)
# Verzeichnisse für Media Stack: /mnt/media/{tv,movies,downloads}
```

### Phase 2: Automation Stack (30 min)
```bash
# Ollama deployen
# Ollama WebUI deployen
# Erstes LLM Modell pullen (llama3.2)
# API-Test durchführen
```

### Phase 3: Media Stack (45 min)
```bash
# Media Stack deployen (Jellyfin + *arr)
# Jellyfin initialisieren
# Sonarr/Radarr/Prowlarr konfigurieren
# Ollama mit n8n verbinden (Agent 1 → Agent 2)
```

### Phase 4: Health Checks (30 min)
```bash
# Container-Status prüfen
# Logs auf Fehler prüfen
# Netzwerk-Konnektivität testen
# Resource Usage überwachen
```

## Hilfreiche Befehle

```bash
# Alle Container auf Host B anzeigen
ssh root@192.168.17.1 "docker ps --format 'table {{.Names}}\t{{.Status}}'"

# Logs eines Containers anzeigen
ssh root@192.168.17.1 "docker logs <container-name> -f"

# Container neu starten
ssh root@192.168.17.1 "docker restart <container-name>"

# Resource Usage prüfen
ssh root@192.168.17.1 "docker stats --no-stream"

# Stack stoppen
ssh root@192.168.17.1 "cd /opt/homelab && docker compose -f automation.yml down"

# Stack starten
ssh root@192.168.17.1 "cd /opt/homelab && docker compose -f automation.yml up -d"
```

## Kommunikation mit Agent 1

**Bei Problemen:**
- Teile Fehlermeldungen mit Agent 1
- Synchronisiere an Checkpoints
- Informiere über abgeschlossene Phasen

**Bei Erfolg:**
- Bestätige abgeschlossene Checkpoints
- Teile Service-URLs (z.B. http://192.168.17.1:11434 für Ollama)
- Bestätige, dass Tests erfolgreich waren

## Erfolgs-Kriterien

Am Ende deiner Arbeit müssen folgende Services laufen:

- [ ] **PostgreSQL**: `docker exec postgres pg_isready` → "accepting connections"
- [ ] **Redis**: `docker exec redis redis-cli ping` → "PONG"
- [ ] **Ollama**: `curl http://192.168.17.1:11434/api/tags` → JSON mit Modellen
- [ ] **Ollama WebUI**: http://192.168.17.1:8080 → Login-Seite
- [ ] **Jellyfin**: http://192.168.17.1:8096 → Welcome Screen
- [ ] **Sonarr**: http://192.168.17.1:8989 → Dashboard
- [ ] **Radarr**: http://192.168.17.1:7878 → Dashboard
- [ ] **Node Exporter**: `curl http://192.168.17.1:9100/metrics` → Metriken

## Troubleshooting

### Problem: SSH-Verbindung fehlgeschlagen
```bash
# Prüfe, ob Host erreichbar ist
ping 192.168.17.1

# Prüfe, ob SSH-Key vorhanden ist
ls ~/.ssh/id_ed25519

# Teste SSH mit Verbose Output
ssh -v root@192.168.17.1
```

### Problem: Docker-Container startet nicht
```bash
# Logs prüfen
ssh root@192.168.17.1 "docker logs <container> --tail 100"

# Container neu erstellen
ssh root@192.168.17.1 "docker rm -f <container> && docker compose up -d <container>"
```

### Problem: Ollama Modell lädt nicht
```bash
# Disk Space prüfen
ssh root@192.168.17.1 "df -h"

# Ollama Logs prüfen
ssh root@192.168.17.1 "docker logs ollama -f"

# Kleineres Modell versuchen
ssh root@192.168.17.1 "docker exec ollama ollama pull phi3"
```

## Abschluss

Wenn alle Erfolgs-Kriterien erfüllt sind, sage:

> "Agent 2: Deployment auf pve-ryzen (192.168.17.1) erfolgreich abgeschlossen! ✅
>
> Folgende Services laufen:
> - PostgreSQL + Redis
> - Ollama + WebUI
> - Jellyfin + Media Stack
> - Node Exporter
>
> Alle Tests bestanden. Bereit für Integration mit Host A."

Dann kann Agent 1 die Integration testen (n8n → Ollama, Prometheus → Node Exporter, etc.).

---

**Viel Erfolg! 🚀**

Arbeite systematisch, dokumentiere Fehler, und synchronisiere mit Agent 1 an den Checkpoints.
