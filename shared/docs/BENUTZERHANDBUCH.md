# Fitna Homelab - Benutzerhandbuch

**Version:** 1.0
**Stand:** 2025-12-19
**Autor:** Claude AI / Fitna

---

## Inhaltsverzeichnis

1. [Einführung](#1-einführung)
2. [Architektur](#2-architektur)
3. [Erste Schritte](#3-erste-schritte)
4. [Services im Detail](#4-services-im-detail)
5. [SSH-Zugang](#5-ssh-zugang)
6. [Wartung & Updates](#6-wartung--updates)
7. [Troubleshooting](#7-troubleshooting)
8. [Sicherheit](#8-sicherheit)
9. [Referenz](#9-referenz)

---

## 1. Einführung

### Was ist ein Homelab?

Ein Homelab ist eine private IT-Infrastruktur zum Lernen, Experimentieren und Betreiben eigener Dienste. Dein Setup umfasst:

- **Lokaler Server (highload):** Arch Linux, Docker-Host
- **Proxmox VE:** Virtualisierungsplattform für VMs und Container
- **Hetzner VPS:** Cloud-Server für externe Dienste
- **Netzwerk:** 192.168.0.0/16 mit Gateway 192.168.16.1

### Warum Docker?

Docker ermöglicht es, Anwendungen isoliert und reproduzierbar zu betreiben:
- **Portabilität:** Läuft überall gleich
- **Isolation:** Services stören sich nicht gegenseitig
- **Einfache Updates:** `docker-compose pull && docker-compose up -d`
- **Ressourceneffizient:** Kein vollständiges OS pro Anwendung

---

## 2. Architektur

```
┌─────────────────────────────────────────────────────────────┐
│                         INTERNET                             │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Router/Gateway                            │
│                    192.168.16.1                              │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│   highload    │    │   Proxmox     │    │   Laptop      │
│ 192.168.16.2  │    │ 192.168.16.X  │    │ 192.168.16.X  │
│               │    │               │    │               │
│ ┌───────────┐ │    │ ┌───────────┐ │    │               │
│ │  Docker   │ │    │ │   VMs     │ │    │               │
│ │  Stack    │ │    │ │   LXCs    │ │    │               │
│ └───────────┘ │    │ └───────────┘ │    │               │
└───────────────┘    └───────────────┘    └───────────────┘

                    ┌───────────────┐
                    │  Hetzner VPS  │
                    │  (Extern)     │
                    └───────────────┘
```

### Docker-Stack Übersicht

| Kategorie | Service | Port | Funktion |
|-----------|---------|------|----------|
| Management | Portainer | 9000/9443 | Docker-Verwaltung via Web |
| Proxy | Nginx Proxy Manager | 80/443/81 | Reverse Proxy, SSL |
| Monitoring | Grafana | 3000 | Dashboards & Visualisierung |
| Monitoring | Prometheus | 9090 | Metrik-Sammlung |
| Monitoring | Uptime Kuma | 3001 | Service-Überwachung |
| Monitoring | Node Exporter | 9100 | System-Metriken |
| DNS | Pi-hole | 8080 | Werbeblocker, lokales DNS |
| VPN | WireGuard | 51820/udp | VPN-Zugang |

---

## 3. Erste Schritte

### 3.1 Stack starten

```bash
# Zum Homelab-Verzeichnis wechseln
cd ~/homelab

# Alle Services starten
docker-compose up -d

# Status prüfen
docker-compose ps
```

### 3.2 Erster Zugriff auf Services

1. **Portainer** (http://localhost:9000)
   - Beim ersten Aufruf: Admin-Benutzer anlegen
   - Passwort: Mindestens 12 Zeichen

2. **Nginx Proxy Manager** (http://localhost:81)
   - Login: `admin@example.com`
   - Passwort: `changeme`
   - **Sofort ändern!**

3. **Grafana** (http://localhost:3000)
   - Login: `admin` / `admin`
   - Passwort beim ersten Login ändern

4. **Pi-hole** (http://localhost:8080/admin)
   - Passwort: `changeme`
   - Ändern via: `docker exec pihole pihole -a -p`

### 3.3 WireGuard VPN einrichten

Nach dem Start werden automatisch 3 Peer-Konfigurationen erstellt:

```bash
# Konfigurationen anzeigen
ls ~/homelab/wireguard/peer*/

# QR-Code für Mobilgeräte anzeigen
docker exec wireguard /app/show-peer 1
```

---

## 4. Services im Detail

### 4.1 Portainer - Docker Management

**Was ist das?**
Eine Web-Oberfläche zur Verwaltung von Docker-Containern, Images, Volumes und Netzwerken.

**Wofür brauchst du es?**
- Container starten/stoppen ohne Kommandozeile
- Logs einsehen
- Ressourcenverbrauch überwachen
- Neue Container deployen

**Wichtige Aktionen:**
```bash
# Container-Logs in Portainer:
# Sidebar → Containers → [Container] → Logs

# Oder via CLI:
docker logs -f [container-name]
```

### 4.2 Nginx Proxy Manager - Reverse Proxy

**Was ist das?**
Ein Reverse Proxy leitet eingehende Anfragen an die richtigen Services weiter und kümmert sich um SSL-Zertifikate.

**Beispiel-Setup:**
1. Dashboard → Proxy Hosts → Add Proxy Host
2. Domain: `portainer.local`
3. Forward Hostname: `portainer`
4. Forward Port: `9000`
5. SSL: Let's Encrypt (für öffentliche Domains)

### 4.3 Grafana & Prometheus - Monitoring

**Prometheus** sammelt Metriken von allen Services.
**Grafana** visualisiert diese in Dashboards.

**Dashboard importieren:**
1. Grafana → Dashboards → Import
2. Dashboard-ID eingeben (z.B. `1860` für Node Exporter)
3. Prometheus als Datenquelle wählen

### 4.4 Pi-hole - DNS & Werbeblocker

**Aktivieren im Netzwerk:**

Option A: Router-DNS auf Pi-hole setzen
```
DNS-Server: 192.168.16.2
```

Option B: Einzelnes Gerät konfigurieren
```
# Linux: /etc/resolv.conf
nameserver 192.168.16.2
```

**Blocklisten hinzufügen:**
1. Pi-hole Admin → Adlists
2. URL hinzufügen, z.B.:
   - `https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts`

---

## 5. SSH-Zugang

### 5.1 Dein SSH-Key

```bash
# Öffentlichen Key anzeigen
cat ~/.ssh/homelab_master.pub

# Ausgabe kopieren und auf Zielhost einfügen
```

### 5.2 Key auf Remote-Host kopieren

```bash
# Automatisch
ssh-copy-id -i ~/.ssh/homelab_master.pub root@192.168.16.X

# Manuell (auf dem Zielhost)
echo "DEIN_PUBLIC_KEY" >> ~/.ssh/authorized_keys
```

### 5.3 SSH-Config nutzen

Nach Anpassung von `~/.ssh/config`:

```bash
# Statt:
ssh -i ~/.ssh/homelab_master root@192.168.16.100

# Einfach:
ssh proxmox
```

---

## 6. Wartung & Updates

### 6.1 Docker-Stack aktualisieren

```bash
cd ~/homelab

# Neue Images ziehen
docker-compose pull

# Container mit neuen Images starten
docker-compose up -d

# Alte Images aufräumen
docker image prune -f
```

### 6.2 System-Updates

**Arch Linux (PC/Laptop):**
```bash
sudo pacman -Syu
```

**Proxmox VE:**
```bash
ssh proxmox
apt update && apt upgrade -y
```

**Debian/Ubuntu (VPS):**
```bash
ssh hetzner
apt update && apt upgrade -y
```

### 6.3 Backup-Strategie

**Docker Volumes sichern:**
```bash
# Backup erstellen
docker run --rm -v portainer_data:/data -v $(pwd):/backup \
  alpine tar czf /backup/portainer_backup.tar.gz /data

# Wiederherstellen
docker run --rm -v portainer_data:/data -v $(pwd):/backup \
  alpine tar xzf /backup/portainer_backup.tar.gz
```

---

## 7. Troubleshooting

### Container startet nicht

```bash
# Logs prüfen
docker logs [container-name]

# Container-Status
docker inspect [container-name] | grep -A 10 "State"

# Neustart erzwingen
docker-compose restart [service-name]
```

### Port bereits belegt

```bash
# Prüfen wer den Port nutzt
sudo ss -tulpn | grep :80

# Prozess beenden oder Port in docker-compose.yml ändern
```

### Kein Netzwerkzugang

```bash
# Docker-Netzwerk prüfen
docker network ls
docker network inspect homelab

# DNS-Auflösung testen
docker exec [container] nslookup google.com
```

### SSH-Verbindung fehlgeschlagen

```bash
# Verbose-Modus für Debugging
ssh -vvv user@host

# Häufige Ursachen:
# - Falscher Key: IdentityFile prüfen
# - Berechtigungen: chmod 600 ~/.ssh/*
# - Firewall: Port 22 offen?
```

---

## 8. Sicherheit

### 8.1 Sofort-Maßnahmen

- [ ] Alle Default-Passwörter ändern
- [ ] SSH-Root-Login deaktivieren (auf Produktiv-Servern)
- [ ] Firewall aktivieren (ufw/nftables)
- [ ] Fail2ban installieren

### 8.2 Passwörter ändern

```bash
# Pi-hole
docker exec pihole pihole -a -p NEUES_PASSWORT

# Grafana: Über Web-UI
# Nginx Proxy Manager: Über Web-UI
# Portainer: Über Web-UI
```

### 8.3 Firewall-Basics

```bash
# UFW installieren (wenn nicht vorhanden)
sudo pacman -S ufw

# Grundkonfiguration
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

---

## 9. Referenz

### 9.1 Wichtige Pfade

| Pfad | Beschreibung |
|------|--------------|
| `~/homelab/` | Docker-Stack Hauptverzeichnis |
| `~/homelab/docker-compose.yml` | Stack-Definition |
| `~/.ssh/config` | SSH-Konfiguration |
| `~/.ssh/homelab_master` | Privater SSH-Key |
| `~/.ssh/homelab_master.pub` | Öffentlicher SSH-Key |

### 9.2 Nützliche Befehle

```bash
# Docker
docker ps                          # Laufende Container
docker-compose logs -f             # Live-Logs
docker system df                   # Speicherverbrauch
docker system prune -a             # Aufräumen (Vorsicht!)

# Netzwerk
ip addr                            # IP-Adressen
ss -tulpn                          # Offene Ports
ping 192.168.16.1                  # Gateway-Test

# System
htop                               # Ressourcen-Monitor
df -h                              # Festplattenplatz
free -h                            # RAM-Nutzung
```

### 9.3 Port-Übersicht

| Port | Service | Protokoll |
|------|---------|-----------|
| 22 | SSH | TCP |
| 53 | Pi-hole DNS | TCP/UDP |
| 80 | HTTP (NPM) | TCP |
| 81 | NPM Admin | TCP |
| 443 | HTTPS (NPM) | TCP |
| 3000 | Grafana | TCP |
| 3001 | Uptime Kuma | TCP |
| 8080 | Pi-hole Admin | TCP |
| 9000 | Portainer | TCP |
| 9090 | Prometheus | TCP |
| 9100 | Node Exporter | TCP |
| 51820 | WireGuard | UDP |

---

## Support

Bei Fragen oder Problemen:
1. Logs prüfen: `docker-compose logs [service]`
2. Dokumentation der jeweiligen Software konsultieren
3. GitHub Issues / Community-Foren

---

*Erstellt mit Claude AI | 2025-12-19*
