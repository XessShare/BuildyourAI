# 🔐 Fitna Homelab - Private Documentation
## Vertrauliche Systemdokumentation

> **WICHTIG:** Diese Dokumentation ist PRIVAT und vertraulich!
> Niemals öffentlich teilen oder zu Git committen!

---

## 📚 Dokumentations-Struktur

```
.private-docs/
├── README.md (diese Datei)
├── admin/          → Für System-Administratoren
├── ai/             → Für AI-Service-Management
├── employee/       → Für Mitarbeiter
└── friends/        → Für Freunde mit limitiertem Zugriff
```

---

## 👥 Zugriff nach Rolle

### 🔐 Admin (Fitna)

**Voller Zugriff auf alles:**
- System-Administration
- Alle Services
- Account-Verwaltung
- Backups & Recovery

**Dokumentation:**
📖 `admin/00_ADMIN_MASTER_GUIDE.md`

**Beinhaltet:**
- Tägliche/Wöchentliche Wartungsaufgaben
- Account-Erstellung für alle Rollen
- Notfall-Prozeduren
- Security & Backups
- Monitoring & Alerts

---

### 🤖 AI-Services

**Zugriff:**
- API-Keys-Verwaltung
- AI-Agenten starten/stoppen
- GPU-Monitoring
- Token-Usage-Tracking

**Dokumentation:**
📖 `ai/AI_SERVICES_GUIDE.md`

**Beinhaltet:**
- API-Key-Management
- Agent-Deployment
- Video-Generation
- Troubleshooting

---

### 👔 Mitarbeiter (Angestellte)

**Zugriff:**
- VPN
- Web-UIs (Grafana, Uptime Kuma, Portainer)
- Read-Only Logs
- Git Repository (lesen)

**Dokumentation:**
📖 `employee/EMPLOYEE_GUIDE.md`

**Beinhaltet:**
- VPN-Setup
- Tool-Nutzung (Grafana, Uptime Kuma, Portainer)
- Tägliche Aufgaben
- Support-Kontakte

---

### 👋 Freunde

**Zugriff:**
- VPN (sicheres Internet)
- Pi-hole (Ad-Blocking)
- Uptime Kuma (nur ansehen)

**Dokumentation:**
📖 `friends/FRIENDS_GUIDE.md`

**Beinhaltet:**
- Einfache VPN-Setup-Anleitung
- Pi-hole nutzen
- Basic Troubleshooting

---

## 🗂️ Weitere wichtige Dokumente

### Homelab-Stack (übergeordnet)

**Location:** `/home/fitna/homelab/`

- `docker-compose.yml` - Service-Definitionen
- `README.md` - Quick Start
- `BENUTZERHANDBUCH.md` - Deutsches Handbuch

### J-Jeco AI Platform

**Location:** `/home/fitna/homelab/J-Jeco/`

- `ARCHITECTURE.md` - System-Architektur (3 Systeme)
- `SETUP_GUIDE.md` - Vollständiges Setup aller Systeme
- `SNAPSHOT_README.md` - Backup/Snapshot-System
- `sync-secrets.sh` - API-Key-Sync-Tool

**AI-Agenten:**
- `1-first-agent/PROJECT_VISION.md` - Vision & Roadmap
- `1-first-agent/README.md` - Agent-Framework Docs

---

## 🎯 Quick Links

### Admin-Aufgaben

**Täglich:**
```bash
# Morning Check
/home/fitna/scripts/daily-check.sh

# Service Status
cd ~/homelab && docker-compose ps
```

**Wöchentlich (Sonntag):**
```bash
# System Updates
sudo apt update && sudo apt upgrade -y

# Docker Updates
cd ~/homelab && docker-compose pull && docker-compose up -d

# Cleanup
docker system prune -af
```

**Account erstellen:**
```bash
# Angestellter: siehe admin/00_ADMIN_MASTER_GUIDE.md Abschnitt 3
# Freund: siehe admin/00_ADMIN_MASTER_GUIDE.md Abschnitt 4
```

### AI-Services

**API-Keys synchronisieren:**
```bash
cd /home/fitna/homelab/J-Jeco
./sync-secrets.sh sync
```

**Agent starten (RTX1080):**
```bash
ssh proxmox-rtx1080
cd ~/J-Jeco/1-first-agent
source ../ai-agents-masterclass/bin/activate
python main.py
```

---

## 🔒 Sicherheit

### Was gehört NICHT in Git?

- ❌ Diese `.private-docs/` Ordner
- ❌ `.env` und `.env.master` Dateien
- ❌ SSH-Keys (`~/.ssh/`)
- ❌ Passwörter, Tokens, API-Keys
- ❌ Backup-Dateien mit sensiblen Daten

### Was ist in Git erlaubt?

- ✅ Code (Python, Shell-Scripts)
- ✅ Dokumentation (öffentlich)
- ✅ Docker-Compose (ohne Secrets)
- ✅ `.env.template` (Template ohne echte Keys)

### .gitignore Check

**Stelle sicher dass diese Zeilen in `.gitignore` sind:**
```
.private-docs/
.env
*.env
.env.master
~/.ssh/
```

---

## 📋 Checklisten

### Neuer Mitarbeiter

- [ ] Linux-User erstellen
- [ ] SSH-Key setup
- [ ] VPN-Zugang (WireGuard peer)
- [ ] Portainer Account (Standard User)
- [ ] Grafana Account (Viewer)
- [ ] Guide zuschicken: `employee/EMPLOYEE_GUIDE.md`
- [ ] Einweisung (15 Min Video-Call)

### Neuer Freund

- [ ] WireGuard VPN-Config generieren
- [ ] QR-Code erstellen
- [ ] Config sicher versenden (verschlüsselt!)
- [ ] Guide zuschicken: `friends/FRIENDS_GUIDE.md`
- [ ] Kurze Erklärung (WhatsApp/Telegram)

### System-Wartung (Monatlich)

- [ ] Alle Systeme updaten
- [ ] Backups verifizieren
- [ ] Passwörter rotieren (quartalsweise)
- [ ] Logs durchsehen
- [ ] Security Audit
- [ ] Disk Space prüfen
- [ ] Alte Snapshots cleanup

---

## 📞 Support & Kontakte

**Admin-Kontakte:**
- Email: admin@fitna.local
- Telegram: @fitna_admin
- Notfall: *[Telefonnummer privat]*

**Externe Ressourcen:**
- Docker Docs: https://docs.docker.com
- Proxmox Wiki: https://pve.proxmox.com/wiki
- WireGuard Docs: https://www.wireguard.com/quickstart/
- Reddit r/selfhosted: https://reddit.com/r/selfhosted

---

## 🎓 Lernen & Weiterbildung

**Für Mitarbeiter:**
- Docker-Grundlagen: https://docker-curriculum.com
- Linux-Basics: https://linuxjourney.com
- Grafana-Tutorials: https://grafana.com/tutorials

**Für Admins:**
- Proxmox-Kurs: https://www.proxmox.com/en/training
- Docker Advanced: https://docs.docker.com/get-started/
- Security Best Practices: https://cisecurity.org

---

## 📝 Changelog

### 2025-12-20 - Initial Creation
- Admin Guide erstellt
- AI Services Guide erstellt
- Employee Guide erstellt
- Friends Guide erstellt
- Struktur aufgebaut

### Geplante Updates
- [ ] Video-Tutorials für Mitarbeiter
- [ ] Automated Onboarding-Scripts
- [ ] Interactive Troubleshooting-Guide
- [ ] FAQ-Section erweitern

---

**Version:** 1.0
**Letzte Aktualisierung:** 2025-12-20
**Nächste Review:** 2026-01-20

🔐 **Vertraulich - Nicht öffentlich teilen!**
