# 🔐 Fitna Homelab - Admin Master Guide
## Vollständige Systemverwaltung & Wartung

> **Vertraulich:** Nur für System-Administratoren

---

## 📋 Inhaltsverzeichnis

1. [System-Übersicht](#system-übersicht)
2. [Tägliche Aufgaben](#tägliche-aufgaben)
3. [Wöchentliche Wartung](#wöchentliche-wartung)
4. [Account-Verwaltung](#account-verwaltung)
5. [Notfall-Prozeduren](#notfall-prozeduren)
6. [Sicherheit & Backups](#sicherheit--backups)

---

## 🏗️ System-Übersicht

### Ihre drei Systeme

```
┌─────────────────────────────────────────────────────────────┐
│  VPS (Cloud)                                                │
│  • IP: 91.107.198.37                                       │
│  • Hostname: jonas-homelab-vps                             │
│  • OS: Ubuntu 24.04 LTS                                    │
│  • Rolle: Public-facing services, Newsletter, APIs         │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  RTX1080 (Proxmox Host)                                     │
│  • IP: 192.168.17.1 (LAN)                                  │
│  • OS: Proxmox VE                                          │
│  • GPU: GeForce GTX 1080                                   │
│  • Rolle: AI Processing, Production Services               │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  ThinkPad (Development)                                     │
│  • IP: 192.168.16.x (LAN)                                  │
│  • OS: Arch Linux / Proxmox VE                             │
│  • Rolle: Development, Testing                             │
└─────────────────────────────────────────────────────────────┘
```

### Laufende Services (docker-compose)

| Service | Port | Beschreibung | Kritisch |
|---------|------|--------------|----------|
| **Portainer** | 9000 | Docker Management UI | ✅ Ja |
| **Nginx Proxy Manager** | 81, 80, 443 | Reverse Proxy & SSL | ✅ Ja |
| **Grafana** | 3000 | Monitoring Dashboards | ⚠️ Wichtig |
| **Prometheus** | 9090 | Metrics Collection | ⚠️ Wichtig |
| **Uptime Kuma** | 3001 | Service Monitoring | ⚠️ Wichtig |
| **Pi-hole** | 8080, 53 | DNS & Ad-Blocking | ✅ Ja |
| **WireGuard** | 51820 | VPN Server | ✅ Ja |

---

## 🔑 Master-Zugangsdaten

### SSH-Zugriff

**Alle Systeme:**
```bash
# Key-Datei:
~/.ssh/homelab_master

# Verbindungen:
ssh -i ~/.ssh/homelab_master root@91.107.198.37  # VPS
ssh -i ~/.ssh/homelab_master root@192.168.17.1   # RTX1080
ssh -i ~/.ssh/homelab_master fitna@pve-thinkpad  # ThinkPad

# Oder mit SSH-Config:
ssh jonas-homelab-vps
ssh proxmox-rtx1080
ssh pve-thinkpad
```

### Service-Zugänge

**Portainer:**
- URL: `http://192.168.17.1:9000`
- User: `admin`
- Password: *[Im Password Manager]*

**Nginx Proxy Manager:**
- URL: `http://192.168.17.1:81`
- User: `admin@fitna.local`
- Password: *[Im Password Manager]*

**Grafana:**
- URL: `http://192.168.17.1:3000`
- User: `admin`
- Initial Password: `admin` (ÄNDERN!)

**Pi-hole:**
- URL: `http://192.168.17.1:8080/admin`
- Password: *[Im Password Manager]*

**Proxmox Web UI:**
- URL: `https://192.168.17.1:8006`
- User: `root@pam`
- Password: *[Im Password Manager]*

---

## 📅 Tägliche Aufgaben

### Morgen-Routine (10 Minuten)

```bash
#!/bin/bash
# Daily Morning Check

# 1. Alle Systeme erreichbar?
echo "🔌 Teste Verbindungen..."
ssh jonas-homelab-vps "uptime"
ssh proxmox-rtx1080 "uptime"
ssh pve-thinkpad "uptime"

# 2. Docker Services Status
echo "🐳 Docker Status..."
cd /home/fitna/homelab
docker-compose ps

# 3. Disk Space Check
echo "💾 Disk Space..."
df -h | grep -E '(Filesystem|/$|/home)'

# 4. Updates verfügbar?
echo "📦 Updates..."
apt update &>/dev/null && apt list --upgradable 2>/dev/null | grep -v "Listing"
```

**Speichern als:** `/home/fitna/scripts/daily-check.sh`

### Service-Health-Check

**Uptime Kuma Dashboard prüfen:**
```bash
# Browser öffnen:
firefox http://192.168.17.1:3001

# Oder CLI-Check:
curl -s http://192.168.17.1:3001/api/status-page/health | jq
```

**Alle Services grün?** → Alles OK ✅

---

## 🛠️ Wöchentliche Wartung

### Sonntags, 10:00 Uhr

#### 1. System-Updates

```bash
# Auf JEDEM System ausführen:

# 1. Update Package Lists
apt update

# 2. Prüfe verfügbare Updates
apt list --upgradable

# 3. Installiere Updates (wenn safe)
apt upgrade -y

# 4. Auto-Remove alte Packages
apt autoremove -y

# 5. Clean Cache
apt autoclean
```

**Reboot nötig?**
```bash
# Check:
[ -f /var/run/reboot-required ] && echo "Reboot needed" || echo "No reboot needed"

# Reboot planen:
shutdown -r +5 "System reboot for updates in 5 minutes"
```

#### 2. Docker Maintenance

```bash
cd /home/fitna/homelab

# 1. Update alle Images
docker-compose pull

# 2. Recreate Container mit neuen Images
docker-compose up -d

# 3. Cleanup alte Images
docker image prune -af

# 4. Cleanup alte Volumes (VORSICHT!)
docker volume prune -f
```

#### 3. Backup-Verifikation

```bash
# Prüfe letzte Backups:
ls -lh /mnt/backup/homelab/ | tail -5

# Prüfe Backup-Größe:
du -sh /mnt/backup/homelab/

# Test Restore (Dry-Run):
./scripts/backup-restore.sh --verify
```

#### 4. Log-Rotation

```bash
# Logs älter als 30 Tage löschen:
find /var/log -type f -name "*.log" -mtime +30 -delete

# Docker Logs beschränken:
docker ps -q | xargs -I {} sh -c 'docker inspect {} | grep LogPath | cut -d\" -f4 | xargs truncate -s 10M'
```

---

## 👥 Account-Verwaltung

### User-Rollen im System

```
┌──────────────────────────────────────────────────────┐
│  ROLLE          │  Zugriff                          │
├──────────────────────────────────────────────────────┤
│  Admin (Sie)    │  Voll (SSH, Root, alle Services)  │
│  AI-Services    │  API-Keys, Docker-Container       │
│  Angestellte    │  Web-UIs, Read-Only, VPN          │
│  Freunde        │  Ausgewählte Services, VPN        │
└──────────────────────────────────────────────────────┘
```

### 1. Admin-Account (Sie)

**Bereits vorhanden:**
- SSH-Zugriff: `fitna` (mit homelab_master key)
- Sudo-Rechte: Ja
- Docker-Gruppe: Ja

**Keine weiteren Admins hinzufügen** (Security Best Practice)

---

### 2. AI-Service-Accounts

**Zweck:** Für AI-Agenten und automatisierte Prozesse

#### Account erstellen:

```bash
# 1. System-User erstellen (kein Login)
sudo useradd -r -s /usr/sbin/nologin -d /opt/ai-services ai-service

# 2. Docker-Gruppe hinzufügen
sudo usermod -aG docker ai-service

# 3. API-Keys-Verzeichnis
sudo mkdir -p /opt/ai-services/.secrets
sudo chown ai-service:ai-service /opt/ai-services/.secrets
sudo chmod 700 /opt/ai-services/.secrets

# 4. Secrets kopieren
sudo cp /home/fitna/J-Jeco/.env.master /opt/ai-services/.secrets/.env
sudo chown ai-service:ai-service /opt/ai-services/.secrets/.env
```

#### Service-spezifische Accounts:

**Content Creator Bot:**
```bash
# Docker Container mit eigenem User:
docker run -d \
  --name content-creator \
  --user 1001:1001 \
  -v /opt/ai-services/content-creator:/data \
  -v /opt/ai-services/.secrets:/secrets:ro \
  your-content-creator-image
```

---

### 3. Angestellten-Accounts

**Zweck:** Team-Mitglieder mit begrenztem Zugriff

#### Account erstellen:

```bash
#!/bin/bash
# Angestellten-Account erstellen

USERNAME="max.mustermann"

# 1. Linux-User
sudo useradd -m -s /bin/bash ${USERNAME}
echo "${USERNAME}:$(openssl rand -base64 12)" | sudo chpasswd

# 2. SSH-Key Setup (User gibt public key)
sudo mkdir -p /home/${USERNAME}/.ssh
echo "ssh-ed25519 AAAA... user@host" | sudo tee /home/${USERNAME}/.ssh/authorized_keys
sudo chmod 700 /home/${USERNAME}/.ssh
sudo chmod 600 /home/${USERNAME}/.ssh/authorized_keys
sudo chown -R ${USERNAME}:${USERNAME} /home/${USERNAME}/.ssh

# 3. Sudo-Rechte (Read-Only Befehle)
echo "${USERNAME} ALL=(ALL) NOPASSWD: /usr/bin/docker ps, /usr/bin/systemctl status" | sudo tee /etc/sudoers.d/${USERNAME}

# 4. Portainer Account
# → Manuell in Portainer UI: User > Add User > Role: "Standard User"

# 5. Grafana Account
# → Manuell in Grafana UI: Users > Invite > Role: "Viewer"
```

#### WireGuard VPN für Angestellte:

```bash
# 1. Neuer Peer konfigurieren
cd /home/fitna/homelab
nano docker-compose.yml

# Erhöhe PEERS:
# PEERS=5  # War 3, jetzt 5

# 2. Recreate Wireguard
docker-compose up -d wireguard

# 3. Config extrahieren
docker exec wireguard cat /config/peer4/peer4.conf > vpn-config-max.conf

# 4. QR-Code für Mobile
docker exec wireguard cat /config/peer4/peer4.png | base64 -d > vpn-config-max-qr.png

# 5. Sicher an Angestellten senden (verschlüsselt!)
gpg -c vpn-config-max.conf
# Per Email an max.mustermann@firma.de
```

#### Was kann ein Angestellter?

- ✅ VPN-Zugriff zum Netzwerk
- ✅ Web-UIs nutzen (Grafana, Uptime Kuma)
- ✅ Logs ansehen (read-only)
- ✅ Docker-Status prüfen
- ❌ Keine SSH-Root-Rechte
- ❌ Keine Konfigurationsänderungen
- ❌ Keine Container starten/stoppen

---

### 4. Freunde-Accounts

**Zweck:** Begrenzte Service-Nutzung (z.B. Pi-hole, VPN)

#### Account erstellen:

```bash
#!/bin/bash
# Freunde-Account (nur Web-Services)

FRIEND_NAME="julia"

# 1. WireGuard VPN-Zugang
cd /home/fitna/homelab
nano docker-compose.yml
# PEERS=6

docker-compose up -d wireguard

# Config extrahieren
docker exec wireguard cat /config/peer5/peer5.conf > vpn-${FRIEND_NAME}.conf
docker exec wireguard cat /config/peer5/peer5.png | base64 -d > vpn-${FRIEND_NAME}-qr.png

# 2. Pi-hole: Erstelle Whitelist für Freund
docker exec pihole pihole -w trusted-friend-domain.com
```

#### Was kann ein Freund?

- ✅ VPN nutzen (sicheres Internet)
- ✅ Pi-hole DNS (Werbung blocken)
- ✅ Ausgewählte Web-Services (z.B. Uptime Kuma)
- ❌ Kein SSH-Zugriff
- ❌ Keine Admin-Panels
- ❌ Kein Zugriff auf sensible Services

#### Freund-spezifische Nginx-Config:

```nginx
# In Nginx Proxy Manager:
# Proxy Host für Freunde-Services

server {
    listen 443 ssl;
    server_name friends.fitna.local;

    location / {
        # Nur Uptime Kuma
        proxy_pass http://uptime-kuma:3001;

        # IP Whitelist (nur VPN IPs)
        allow 10.8.0.0/24;
        deny all;
    }
}
```

---

## 🚨 Notfall-Prozeduren

### Szenario 1: Service ist down

```bash
# 1. Welcher Service?
docker-compose ps

# 2. Logs prüfen
docker-compose logs [service-name] --tail=50

# 3. Restart versuchen
docker-compose restart [service-name]

# 4. Falls Fehler persistiert:
docker-compose down
docker-compose up -d

# 5. Immer noch Probleme?
docker-compose down
docker volume ls  # Prüfe Volumes
docker-compose up -d --force-recreate
```

### Szenario 2: Festplatte voll

```bash
# 1. Was ist voll?
df -h

# 2. Größte Dateien finden
du -sh /* | sort -hr | head -10

# 3. Docker Cleanup
docker system prune -af --volumes

# 4. Logs cleanup
journalctl --vacuum-size=100M

# 5. Alte Snapshots löschen
cd /home/fitna/homelab/snap
ls -lh | head -20
rm -rf snapshot_20241001_*  # Alte löschen
```

### Szenario 3: System nicht erreichbar

**Via Proxmox Console:**
```bash
# 1. Login über Proxmox Web UI
# 2. Console öffnen
# 3. Check Network:
ip addr show
ip route

# 4. Restart Networking
systemctl restart networking

# 5. Check SSH
systemctl status sshd
systemctl restart sshd
```

### Szenario 4: Datenverlust/Restore

```bash
# 1. Snapshot restore (lokal)
cd /home/fitna/homelab/J-Jeco
./snapshot.sh list
./snapshot.sh restore snapshot_YYYYMMDD_HHMMSS

# 2. Backup restore (extern)
cd /mnt/backup/homelab
tar -xzf backup-YYYY-MM-DD.tar.gz -C /home/fitna/homelab/

# 3. Docker Volumes restore
docker run --rm -v portainer_data:/volume -v /mnt/backup:/backup alpine \
  tar -xzf /backup/portainer-data.tar.gz -C /volume
```

---

## 🔒 Sicherheit & Backups

### Tägliche Backups (Automatisch)

**Cron-Job einrichten:**
```bash
crontab -e

# Täglich um 2 Uhr nachts
0 2 * * * /home/fitna/scripts/backup-homelab.sh
```

**Backup-Script:** `/home/fitna/scripts/backup-homelab.sh`
```bash
#!/bin/bash
# Homelab Daily Backup

BACKUP_DIR="/mnt/backup/homelab"
DATE=$(date +%Y-%m-%d)

# 1. Docker Volumes
docker run --rm \
  -v portainer_data:/volume \
  -v ${BACKUP_DIR}:/backup \
  alpine tar -czf /backup/portainer-data-${DATE}.tar.gz -C /volume .

# 2. Config-Dateien
tar -czf ${BACKUP_DIR}/configs-${DATE}.tar.gz \
  /home/fitna/homelab/docker-compose.yml \
  /home/fitna/homelab/prometheus/ \
  /home/fitna/homelab/wireguard/

# 3. Secrets (verschlüsselt!)
tar -czf - /home/fitna/J-Jeco/.env.master | \
  gpg -c > ${BACKUP_DIR}/secrets-${DATE}.tar.gz.gpg

# 4. Cleanup alte Backups (>30 Tage)
find ${BACKUP_DIR} -name "*.tar.gz*" -mtime +30 -delete

echo "Backup completed: ${DATE}"
```

### Security-Audit (Monatlich)

```bash
#!/bin/bash
# Monthly Security Audit

echo "=== Security Audit $(date) ===" | tee -a /var/log/security-audit.log

# 1. Offene Ports prüfen
echo "[*] Open Ports:"
ss -tuln | tee -a /var/log/security-audit.log

# 2. Failed Login Attempts
echo "[*] Failed SSH Logins:"
grep "Failed password" /var/log/auth.log | tail -20

# 3. Docker Security Scan
echo "[*] Docker Security:"
docker scan --accept-license portainer/portainer-ce:latest

# 4. Certificates Expiry
echo "[*] SSL Certificates:"
find /home/fitna/homelab/nginx-proxy-manager -name "*.pem" -exec openssl x509 -in {} -noout -enddate \;

# 5. User List
echo "[*] System Users:"
cat /etc/passwd | grep "/bin/bash"
```

### Password Rotation (Quartalsweise)

**Checklist:**
- [ ] Portainer Admin Password
- [ ] Grafana Admin Password
- [ ] Pi-hole Web Password
- [ ] Proxmox Root Password
- [ ] SSH-Keys neu generieren (optional)
- [ ] API-Keys (OpenAI, Anthropic)

---

## 📊 Monitoring & Alerts

### Grafana Dashboards Setup

**Wichtige Dashboards:**

1. **System Overview**
   - CPU, RAM, Disk Usage
   - Network Traffic
   - Docker Container Status

2. **Service Health**
   - Uptime per Service
   - Response Times
   - Error Rates

3. **Security**
   - Failed Login Attempts
   - Unusual Traffic Patterns
   - Certificate Expiry

**Alert-Channels konfigurieren:**

```bash
# Telegram-Bot erstellen (via @BotFather)
# Token: TELEGRAM_BOT_TOKEN

# In Grafana UI:
# Alerting > Contact Points > Add Contact Point
# Type: Telegram
# Bot Token: <your token>
# Chat ID: <your chat id>
```

### Uptime Kuma Monitoring

**Services hinzufügen:**

1. Portainer: `http://192.168.17.1:9000`
2. Nginx PM: `http://192.168.17.1:81`
3. Grafana: `http://192.168.17.1:3000`
4. VPS: `https://jonas-homelab-vps` (ping)
5. GitHub: `https://github.com` (extern)

**Notifications:**
- Telegram
- Email
- Discord (optional)

---

## 🎓 Best Practices

### Dos ✅

- **Dokumentiere Änderungen** in `/home/fitna/homelab/CHANGELOG.md`
- **Teste in Dev** (ThinkPad) vor Production
- **Snapshots vor großen Änderungen**
- **Regelmäßige Backups verifizieren**
- **Secrets nie in Git committen**
- **Updates immer sonntags**

### Don'ts ❌

- **Niemals direkt in Production testen**
- **Keine Passwörter in Scripts**
- **Keine Root-Logins ohne Key**
- **Keine ungeplanten Reboots (außer Notfall)**
- **Keine Docker-Befehle mit `--rm` auf Production-Daten**

---

## 📞 Support & Eskalation

**Bei Problemen:**

1. **Check Logs:** `docker-compose logs`
2. **Check Dokumentation:** Diese Datei!
3. **Community:** Reddit /r/selfhosted
4. **GitHub Issues:** Für spezifische Tools

**Externe Hilfe:**
- Docker: https://docs.docker.com
- Proxmox: https://pve.proxmox.com/wiki
- Linux: https://wiki.archlinux.org

---

**Dokument-Version:** 1.0
**Letzte Aktualisierung:** 2025-12-20
**Nächste Review:** 2026-01-20

**🔐 Vertraulich - Nur für Admin**
