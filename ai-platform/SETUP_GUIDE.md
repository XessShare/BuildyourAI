# J-Jeco System Setup Guide
## Schritt-für-Schritt Anleitung für alle drei Systeme

> **Ziel:** Alle drei Systeme (VPS, ThinkPad, RTX1080) arbeiten zusammen mit denselben API-Keys

---

## 🎯 Übersicht: Was machen wir?

```
1. Master Secrets erstellen (auf einem System)
2. Secrets zu allen Systemen verteilen
3. Projekt auf jedem System einrichten
4. Testen ob alles funktioniert
```

**Zeitaufwand:** 30-45 Minuten
**Schwierigkeitsgrad:** Mittel

---

## 📋 Voraussetzungen (Checklist)

Bevor Sie starten, stellen Sie sicher dass:

- [ ] Alle drei Systeme laufen
- [ ] SSH-Zugriff zu allen Systemen funktioniert
- [ ] Git ist installiert
- [ ] Python 3.13+ ist installiert
- [ ] Sie haben Ihre API-Keys bereit (OpenAI, Anthropic)

### SSH-Zugriff testen

```bash
# Von Ihrem aktuellen System zu allen anderen:
ssh jonas-homelab-vps "echo VPS erreichbar"
ssh 192.168.17.1 "echo RTX1080 erreichbar"
ssh pve-thinkpad "echo ThinkPad erreichbar"  # Name anpassen!
```

Alle sollten antworten. Falls nicht → SSH-Keys setup nötig!

---

## 🚀 Setup: Schritt für Schritt

### Schritt 1: Master Secrets erstellen

**Wo:** Auf dem System, wo Sie gerade sind (z.B. ThinkPad)

```bash
cd /home/fitna/homelab/J-Jeco

# Template erstellen
./sync-secrets.sh create-master

# Template mit echten API-Keys füllen
nano .env.master
```

**Was eintragen:**

```bash
# Mindestens diese Keys brauchen Sie:
OPENAI_API_KEY=sk-...     # Von https://platform.openai.com
ANTHROPIC_API_KEY=sk-ant-...  # Von https://console.anthropic.com

# Optional (später):
TELEGRAM_BOT_TOKEN=...
HEYGEN_API_KEY=...
```

**Speichern:** `Ctrl+O`, dann `Enter`, dann `Ctrl+X`

---

### Schritt 2: SSH-Verbindungen testen

```bash
# Teste ob alle Systeme erreichbar sind:
./sync-secrets.sh test
```

**Erwartete Ausgabe:**
```
🔌 Teste Verbindungen zu allen Systemen...

Testing vps (jonas-homelab-vps)... ✅ Erreichbar
Testing rtx1080 (192.168.17.1)... ✅ Erreichbar
Testing thinkpad (pve-thinkpad)... ✅ Erreichbar
```

**Falls Fehler:**
- Prüfe SSH-Config: `cat ~/.ssh/config`
- Prüfe Hostnamen/IPs in `sync-secrets.sh`
- Editiere System-Definitionen bei Bedarf

---

### Schritt 3: Secrets verteilen

```bash
# Verteile Master Secrets zu allen Systemen:
./sync-secrets.sh sync
```

**Was passiert:**
1. Script prüft Master Secrets
2. Verbindet zu jedem System
3. Kopiert `.env` Datei
4. Verifiziert erfolgreichen Transfer

**Erwartete Ausgabe:**
```
📤 Sync zu vps (jonas-homelab-vps)...
✅ Erfolgreich synced (25 Zeilen)

📤 Sync zu rtx1080 (192.168.17.1)...
✅ Erfolgreich synced (25 Zeilen)

═══════════════════════════════════
✅ Erfolgreich: 3
❌ Fehlgeschlagen: 0
═══════════════════════════════════
```

---

### Schritt 4: Projekt auf allen Systemen clonen

**Auf JEDEM System ausführen:**

#### 4a) VPS Setup

```bash
# SSH zum VPS
ssh jonas-homelab-vps

# Repository clonen
cd ~
git clone git@github.com:XessShare/J-Jeco.git
cd J-Jeco

# Virtual Environment setup
python3 -m venv ai-agents-masterclass
source ai-agents-masterclass/bin/activate
cd 1-first-agent
pip install -r requirements.txt

# Test
python main.py moonshot-check
```

#### 4b) RTX1080 Setup

```bash
# SSH zu RTX1080
ssh 192.168.17.1

# Repository clonen
cd ~
git clone git@github.com:XessShare/J-Jeco.git
cd J-Jeco

# Virtual Environment setup
python3 -m venv ai-agents-masterclass
source ai-agents-masterclass/bin/activate
cd 1-first-agent
pip install -r requirements.txt

# Test
python main.py moonshot-check
```

#### 4c) ThinkPad Setup

```bash
# Bereits vorhanden! Nur .env prüfen:
cd /home/fitna/homelab/J-Jeco/1-first-agent

# Prüfe ob .env vorhanden:
ls -la .env

# Test
source ../ai-agents-masterclass/bin/activate
python main.py moonshot-check
```

---

### Schritt 5: Verify - Alles funktioniert?

**Status prüfen:**

```bash
# Auf dem System mit sync-secrets.sh:
./sync-secrets.sh status
```

**Erwartete Ausgabe:**
```
📊 Status aller Systeme:

Master Secrets:
  📁 /home/fitna/J-Jeco/.env.master
  📄 25 Zeilen, 8 Keys
  📅 2025-12-20 14:00:00

vps (jonas-homelab-vps):
  ✅ Secrets vorhanden
  📄 25 Zeilen
  🔄 In Sync

rtx1080 (192.168.17.1):
  ✅ Secrets vorhanden
  📄 25 Zeilen
  🔄 In Sync

thinkpad (pve-thinkpad):
  ✅ Secrets vorhanden
  📄 25 Zeilen
  🔄 In Sync
```

**Alle grün?** Perfect! ✅

---

## 🎨 Systemspezifische Konfiguration

Nach dem Basis-Setup können Sie jedes System für seine Rolle optimieren:

### VPS - Der Außendienstler

**Zusätzliche Services:**

```bash
# Nginx Reverse Proxy
docker run -d \
  --name nginx-proxy-manager \
  -p 80:80 -p 443:443 \
  -p 81:81 \
  jc21/nginx-proxy-manager

# Ghost CMS für Newsletter
docker run -d \
  --name ghost \
  -p 2368:2368 \
  -e url=https://yourdomain.com \
  ghost:latest
```

**Firewall konfigurieren:**
```bash
# Ports öffnen
ufw allow 80/tcp
ufw allow 443/tcp
ufw allow 22/tcp
ufw enable
```

---

### RTX1080 - Die Kraftmaschine

**GPU-Treiber prüfen:**

```bash
# NVIDIA Driver check
nvidia-smi

# Sollte GPU zeigen:
# +-----------------------------------------------------------------------------+
# | NVIDIA-SMI 535.xx    Driver Version: 535.xx    CUDA Version: 12.x         |
# +-------------------------------+----------------------+----------------------+
# | GPU  Name        TCC/WDDM | Bus-Id        Disp.A | Volatile Uncorr. ECC |
# |   0  GeForce GTX 1080    |               |                              |
```

**Docker mit GPU-Support:**

```bash
# NVIDIA Container Toolkit installieren
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | \
  sudo tee /etc/apt/sources.list.d/nvidia-docker.list

sudo apt-get update
sudo apt-get install -y nvidia-docker2
sudo systemctl restart docker

# Test GPU im Container
docker run --rm --gpus all nvidia/cuda:11.8.0-base-ubuntu22.04 nvidia-smi
```

**Portainer mit GPU:**
```bash
# Portainer starten
docker run -d \
  -p 9000:9000 \
  --name portainer \
  --restart always \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v portainer_data:/data \
  portainer/portainer-ce:latest
```

---

### ThinkPad - Die Entwicklungswerkstatt

**Development Tools:**

```bash
# VS Code Server (optional)
curl -fsSL https://code-server.dev/install.sh | sh
code-server

# Git Hooks für Auto-Testing
cd /home/fitna/homelab/J-Jeco
nano .git/hooks/pre-commit

# Inhalt:
#!/bin/bash
cd 1-first-agent
source ../ai-agents-masterclass/bin/activate
python -m pytest tests/ 2>/dev/null || true
```

**Snapshot-Automatisierung:**
```bash
# Cron für automatische Snapshots
crontab -e

# Täglich um 2 Uhr morgens:
0 2 * * * cd /home/fitna/homelab/J-Jeco && ./snapshot.sh create "Daily auto-snapshot" && ./snapshot.sh cleanup 7
```

---

## 🔄 Workflow: Tägliche Nutzung

### Morgens: Check Status

```bash
# Auf jedem System:
ssh <system> "cd J-Jeco && git pull && systemctl status docker"
```

### Während Entwicklung: Secrets aktualisiert?

```bash
# Master Secrets ändern:
nano .env.master

# Zu allen Systemen verteilen:
./sync-secrets.sh sync

# Status prüfen:
./sync-secrets.sh status
```

### Abends: Sync & Backup

```bash
# Code committen
cd /home/fitna/homelab/J-Jeco
git add .
git commit -m "Feature X"
git push

# Snapshot erstellen
./snapshot.sh create "End of day - Feature X complete"

# Alte Snapshots cleanup
./snapshot.sh cleanup 7
```

---

## 🐛 Troubleshooting

### Problem: SSH-Verbindung schlägt fehl

**Symptom:**
```
Testing vps (jonas-homelab-vps)... ❌ Nicht erreichbar
```

**Lösung:**
```bash
# 1. Prüfe SSH-Config
cat ~/.ssh/config

# 2. Teste manuelle Verbindung
ssh jonas-homelab-vps

# 3. Prüfe SSH-Key
ssh-add -l

# 4. Falls kein Key: Erstelle einen
ssh-keygen -t ed25519
ssh-copy-id jonas-homelab-vps
```

---

### Problem: Secrets werden nicht synced

**Symptom:**
```
❌ SCP fehlgeschlagen
```

**Lösung:**
```bash
# 1. Prüfe ob remote directory existiert
ssh <system> "mkdir -p ~/J-Jeco/1-first-agent"

# 2. Manuelle Kopie zum Test
scp .env.master <system>:~/J-Jeco/1-first-agent/.env

# 3. Verifiziere
ssh <system> "cat ~/J-Jeco/1-first-agent/.env | head -5"
```

---

### Problem: API-Keys funktionieren nicht

**Symptom:**
```
OpenAI API Error: Invalid API key
```

**Lösung:**
```bash
# 1. Prüfe .env Inhalt (auf dem betroffenen System)
cat ~/J-Jeco/1-first-agent/.env | grep OPENAI_API_KEY

# 2. Test API-Key direkt
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer YOUR_API_KEY"

# 3. Falls Key ungültig: Neu generieren
# → https://platform.openai.com/api-keys

# 4. Master Secrets aktualisieren
nano .env.master

# 5. Neu verteilen
./sync-secrets.sh sync
```

---

### Problem: Git clone schlägt fehl

**Symptom:**
```
Permission denied (publickey)
```

**Lösung:**
```bash
# 1. GitHub SSH-Key check
ssh -T git@github.com

# 2. Falls fehlerhaft: SSH-Key zu GitHub hinzufügen
cat ~/.ssh/id_ed25519.pub
# → Kopieren und bei GitHub einfügen

# 3. Alternative: HTTPS clone
git clone https://github.com/XessShare/J-Jeco.git
```

---

## 📊 Maintenance-Checkliste

### Täglich
- [ ] `git pull` auf allen Systemen
- [ ] Docker Services Status check
- [ ] Logs prüfen

### Wöchentlich
- [ ] `./sync-secrets.sh status` - Sync-Status prüfen
- [ ] `./snapshot.sh cleanup 7` - Alte Snapshots löschen
- [ ] Backups verifizieren

### Monatlich
- [ ] System-Updates (`apt update && apt upgrade`)
- [ ] Docker Images updaten
- [ ] Festplattenspeicher prüfen
- [ ] API-Key Rotation (Security Best Practice)

---

## 🎓 Nächste Schritte

Nach dem erfolgreichen Setup können Sie:

1. **Content Creator Agent implementieren**
   ```bash
   cd 1-first-agent
   nano agents/content_creator_agent.py
   ```

2. **Newsletter-System aufsetzen**
   - Ghost CMS auf VPS
   - Email-Automation konfigurieren

3. **Monitoring einrichten**
   - Grafana auf RTX1080
   - Prometheus Metrics
   - Alert-System via Telegram

4. **Production Deployment**
   - Docker Compose für alle Services
   - Automatische Updates
   - Health-Checks

---

## 📚 Weitere Ressourcen

- **Architecture Overview:** `ARCHITECTURE.md`
- **Snapshot System:** `SNAPSHOT_README.md`
- **Project Vision:** `1-first-agent/PROJECT_VISION.md`
- **Agent Development:** `1-first-agent/README.md`

---

**Happy Hacking! 🚀**

Bei Problemen: Check die Troubleshooting-Section oder erstelle ein GitHub Issue.
