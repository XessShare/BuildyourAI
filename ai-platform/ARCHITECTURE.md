# J-Jeco Homelab Architektur
## Drei Systeme - Ein Team

> **Einfach erklärt:** Stellen Sie sich drei Computer vor, die zusammenarbeiten wie ein Team in einem Unternehmen. Jeder hat seine spezielle Aufgabe, aber alle teilen sich wichtige Informationen (API-Schlüssel).

---

## 🏢 Das Team: Ihre drei Systeme

```
┌─────────────────────────────────────────────────────────────────┐
│                    INTERNET (öffentlich)                         │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ SSH/HTTPS
                             ▼
            ┌────────────────────────────────────┐
            │  🌍 VPS (Cloud-Server)             │
            │  jonas-homelab-vps                 │
            │  91.107.198.37                     │
            │                                    │
            │  Rolle: "Der Außendienstler"       │
            │  • Öffentlich erreichbar           │
            │  • Newsletter versenden            │
            │  • Webhooks empfangen              │
            │  • API Gateway                     │
            └────────────────┬───────────────────┘
                             │
                             │ WireGuard VPN
                             │
            ┌────────────────┴───────────────────┐
            │                                    │
            ▼                                    ▼
┌───────────────────────┐          ┌───────────────────────┐
│ 💻 PVE ThinkPad       │          │ 🎮 Proxmox RTX 1080   │
│ (Proxmox VE)          │          │ 192.168.17.1          │
│                       │          │                       │
│ Rolle: "Dev & Test"   │          │ Rolle: "Die Kraftmaschine" │
│ • Entwicklung         │◄────────►│ • AI Model Training  │
│ • Testing             │ LAN      │ • Video Generation    │
│ • Snapshots           │          │ • Heavy Computing     │
│ • Git Repository      │          │ • Production Services │
└───────────────────────┘          └───────────────────────┘

               GEMEINSAM: API Keys, Config, Daten
```

---

## 🎯 Die drei Teammitglieder

### 1. 🌍 VPS - Der Außendienstler
**IP:** `91.107.198.37` (öffentlich)
**Name:** `jonas-homelab-vps`

**Wie ein Mitarbeiter im Außendienst:**
- Hat Kontakt zur Außenwelt (Internet)
- Nimmt Bestellungen entgegen (API Calls)
- Versendet Newsletter
- Leitet wichtige Anfragen ans Team weiter

**Aufgaben:**
- ✅ Newsletter verschicken (Ghost/Listmonk)
- ✅ Webhooks empfangen (GitHub, Stripe, etc.)
- ✅ Reverse Proxy (Nginx)
- ✅ SSL/HTTPS Termination
- ✅ Lightweight AI-Agents (Communicator, Project Manager)

**Warum hier?**
- Immer online (99.9% Uptime)
- Schnelle Internetverbindung
- Öffentliche IP-Adresse

---

### 2. 💻 PVE ThinkPad - Die Entwicklungswerkstatt
**Lokales Netzwerk** (z.B. 192.168.16.x)
**Name:** `pve-thinkpad`

**Wie eine Werkstatt für Prototypen:**
- Hier wird entwickelt und getestet
- Schnelle Änderungen möglich
- Snapshots vor jedem Experiment
- Kein Risiko für Production

**Aufgaben:**
- ✅ Code-Entwicklung
- ✅ Git Repository (lokaler Clone)
- ✅ Testing & Debugging
- ✅ Snapshots & Rollbacks
- ✅ Lightweight AI-Agents Tests

**Warum hier?**
- Schneller Zugriff (lokal)
- Keine Cloud-Kosten
- Volle Kontrolle

---

### 3. 🎮 Proxmox RTX 1080 - Die Kraftmaschine
**IP:** `192.168.17.1` (lokales Netzwerk)
**Name:** `proxmox-rtx1080`

**Wie eine Fabrik mit starken Maschinen:**
- Hat die Power (RTX 1080 GPU!)
- Erledigt schwere Aufgaben
- Läuft 24/7 für Production
- Hosting der Hauptservices

**Aufgaben:**
- ✅ AI Model Inference (GPU-beschleunigt)
- ✅ Video-Generation (Avatar-Videos)
- ✅ Training von Custom Models
- ✅ Production Services (Portainer, Grafana, etc.)
- ✅ Heavy AI-Agents (Research, Content Creator)

**Warum hier?**
- RTX 1080 GPU für AI
- Immer verfügbar (24/7)
- Genug Power für Production

---

## 🔑 API-Schlüssel: Das gemeinsame Geheimnis

**Einfach erklärt:** API-Schlüssel sind wie Passwörter, mit denen Ihre Computer mit externen Diensten sprechen können (OpenAI, Anthropic, etc.). Alle drei Computer brauchen dieselben Schlüssel.

### Strategie: "Ein Schlüsselbund für alle"

```
┌─────────────────────────────────────────────────────────┐
│         🔐 Zentraler API-Schlüssel-Speicher             │
│                                                         │
│   Location: Proxmox RTX 1080 (192.168.17.1)            │
│   File: /mnt/shared-secrets/.env.shared                │
│                                                         │
│   Inhalt:                                              │
│   • OPENAI_API_KEY=sk-...                             │
│   • ANTHROPIC_API_KEY=sk-ant-...                      │
│   • TELEGRAM_BOT_TOKEN=...                            │
│   • etc.                                              │
└─────────────────────────────────────────────────────────┘
                          │
                          │ Synchronisation
         ┌────────────────┼────────────────┐
         │                │                │
         ▼                ▼                ▼
    ┌────────┐      ┌────────┐      ┌────────┐
    │  VPS   │      │ ThinkPad│      │ RTX1080│
    │ .env   │      │  .env   │      │  .env  │
    └────────┘      └────────┘      └────────┘
```

### Drei Methoden (von einfach bis professionell)

#### **Methode 1: Manuelles Kopieren** (Einfachste)
```bash
# Auf RTX1080: Master .env erstellen
nano /home/shared/.env.master

# Per SCP an andere Systeme verteilen
scp /home/shared/.env.master vps:/path/to/project/.env
scp /home/shared/.env.master thinkpad:/path/to/project/.env
```

**Für wen:** Anfänger, kleine Setups
**Vorteil:** Super einfach
**Nachteil:** Manuell bei jeder Änderung

---

#### **Methode 2: Sync-Script** (Empfohlen)
```bash
# Automatisches Sync-Script
./sync-secrets.sh

# Synct .env von RTX1080 zu allen anderen
```

**Für wen:** Fortgeschrittene
**Vorteil:** Ein Befehl, alles synced
**Nachteil:** Muss manuell gestartet werden

---

#### **Methode 3: HashiCorp Vault** (Professionell)
```bash
# Zentrale Secrets-Verwaltung
vault kv get secret/jjeco/api-keys
```

**Für wen:** Profis, große Setups
**Vorteil:** Maximal sicher, Audit-Logs
**Nachteil:** Komplexer Setup

---

## 📋 Aufgabenverteilung

### Content-Erstellung (Tutorial-Videos)

```
1. ThinkPad: Script entwickeln
   └─> Git commit

2. RTX1080: Script generieren (AI)
   └─> Voice Synthesis
   └─> Avatar Animation (GPU!)
   └─> Video Assembly

3. VPS: Video hochladen & verteilen
   └─> YouTube Upload
   └─> Newsletter versenden
```

### Newsletter-Versand

```
1. RTX1080: Content generieren (AI)
   └─> Research Agent sammelt News
   └─> Content Agent schreibt Newsletter

2. VPS: Newsletter versenden
   └─> Ghost/Listmonk
   └─> Email Distribution

3. ThinkPad: Tracking & Analytics
   └─> Öffnungsraten monitoren
```

### AI-Agent-Orchestrierung

```
┌─────────────────────────────────────────────┐
│  Agent-Verteilung nach System-Stärken       │
└─────────────────────────────────────────────┘

VPS (Lightweight Agents):
├─ Communicator Agent (Prompt Optimization)
├─ Project Manager Agent (Orchestration)
└─ Webhook Handler Agent

ThinkPad (Development):
├─ Development & Testing aller Agents
├─ Debug & Logging
└─ Snapshot Management

RTX1080 (Heavy Agents):
├─ Content Creator Agent (GPU für Video)
├─ Research Agent (Large Context)
├─ Verification Agent (Model Inference)
└─ Investment Analyzer Agent (Data Crunching)
```

---

## 🔄 Datenfluss-Beispiel: "Newsletter erstellen"

### Schritt für Schritt (kinderleicht erklärt)

**1. ThinkPad gibt den Startschuss**
```bash
# Developer auf ThinkPad:
python main.py plan-project "Newsletter #1 erstellen"
```
*Wie: "Chef sagt: Wir machen einen Newsletter!"*

**2. RTX1080 erstellt den Content**
```bash
# AI-Agenten auf RTX1080 arbeiten parallel:
- Research Agent sammelt AI-News der Woche
- Content Agent schreibt Newsletter-Text
- Verification Agent prüft Fakten
```
*Wie: "Die Arbeiter in der Fabrik erstellen das Produkt"*

**3. Alle prüfen gemeinsam**
```bash
# ThinkPad holt sich Preview:
scp rtx1080:/output/newsletter.html ./preview/

# Developer prüft und gibt OK
```
*Wie: "Chef schaut sich das Produkt an und sagt: Gut!"*

**4. VPS versendet an die Welt**
```bash
# VPS verschickt Newsletter:
- An alle 100 Subscriber
- Tracking-Pixel einfügen
- Versandstatistik loggen
```
*Wie: "Die Post bringt das Produkt zu den Kunden"*

---

## 🌐 Netzwerk-Verbindungen

### Wie reden die Computer miteinander?

```
Internet
   │
   │ (HTTPS/SSH)
   │
   ▼
┌──────────┐
│   VPS    │ Public IP: 91.107.198.37
└────┬─────┘
     │
     │ WireGuard VPN (verschlüsselter Tunnel)
     │ VPN IP: 10.8.0.1
     │
     ├─────────────┬─────────────┐
     │             │             │
     ▼             ▼             ▼
┌─────────┐  ┌──────────┐  ┌──────────┐
│ThinkPad │  │ RTX1080  │  │ Weitere  │
│VPN: .2  │  │ VPN: .3  │  │ Geräte   │
└─────────┘  └──────────┘  └──────────┘
     │             │
     │   Lokales   │
     │   Netzwerk  │
     │   (LAN)     │
     └─────┬───────┘
           │
    192.168.17.0/24
```

**Einfach erklärt:**

1. **Internet → VPS:** Wie ein Brief, der zur Postfiliale kommt
2. **VPS → Homelab (VPN):** Wie ein sicherer Tunnel unter der Erde
3. **ThinkPad ↔ RTX1080 (LAN):** Wie Nachbarn, die direkt miteinander reden

---

## 🔐 Sicherheit: Wie bleiben die Geheimnisse geheim?

### Drei Sicherheitsebenen

**Ebene 1: Verschlüsselte Verbindung (VPN)**
```
Alle Daten zwischen VPS und Homelab gehen durch einen
verschlüsselten Tunnel (WireGuard).

Wie: Ein Rohrpost-System, bei dem niemand reingucken kann.
```

**Ebene 2: SSH-Keys (keine Passwörter)**
```
Computer authentifizieren sich mit Schlüsseln, nicht Passwörtern.

Wie: Ein spezieller Fingerabdruck, den nur Sie haben.
```

**Ebene 3: .env Dateien (nie in Git)**
```
API-Schlüssel stehen NICHT im Code, sondern in .env Dateien.
Diese werden NIEMALS zu GitHub gepusht.

Wie: Das Rezept ist öffentlich, aber die geheime Zutat nicht.
```

---

## 📦 Deployment-Strategie

### Von Entwicklung zu Production

```
┌─────────────────────────────────────────────────────────┐
│                  DEVELOPMENT FLOW                        │
└─────────────────────────────────────────────────────────┘

1. ThinkPad (Dev)
   ├─ Code schreiben
   ├─ Lokal testen
   ├─ Snapshot erstellen
   └─ Git commit

2. GitHub (Sync)
   ├─ Code pushen
   └─ Webhook triggert

3. RTX1080 (Staging)
   ├─ Git pull
   ├─ Tests laufen
   ├─ Docker build
   └─ Staging deployment

4. Manual Approval
   ├─ Developer prüft Staging
   └─ Gibt Production-Freigabe

5. VPS & RTX1080 (Production)
   ├─ Git pull auf beiden
   ├─ Docker restart
   └─ Services online
```

---

## 🎨 Visuelle Zusammenfassung

```
┌───────────────────────────────────────────────────────────┐
│              WER MACHT WAS?                                │
├───────────────────────────────────────────────────────────┤
│                                                           │
│  💻 ThinkPad: "Der Entwickler"                           │
│  ├─ Schnell & flexibel                                   │
│  ├─ Entwicklung & Tests                                  │
│  └─ Snapshots & Rollbacks                                │
│                                                           │
│  🎮 RTX1080: "Die Fabrik"                                │
│  ├─ Stark & zuverlässig (GPU!)                           │
│  ├─ AI-Processing                                        │
│  └─ Production Services                                  │
│                                                           │
│  🌍 VPS: "Der Verkäufer"                                  │
│  ├─ Immer erreichbar                                     │
│  ├─ Kontakt nach außen                                  │
│  └─ Newsletter & APIs                                    │
│                                                           │
└───────────────────────────────────────────────────────────┘

        Alle teilen: API-Keys, Config, Daten
```

---

## 🚀 Quick Start: System-Setup

### Schritt 1: API-Keys zentral ablegen (RTX1080)

```bash
# Auf RTX1080:
mkdir -p /home/shared/secrets
nano /home/shared/secrets/.env.master

# Inhalt:
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
```

### Schritt 2: Zu anderen Systemen verteilen

```bash
# Von RTX1080 zu VPS:
scp /home/shared/secrets/.env.master jonas-homelab-vps:~/J-Jeco/.env

# Von RTX1080 zu ThinkPad:
scp /home/shared/secrets/.env.master pve-thinkpad:~/J-Jeco/.env
```

### Schritt 3: Teste auf jedem System

```bash
# Auf jedem System:
cd ~/J-Jeco/1-first-agent
source ../ai-agents-masterclass/bin/activate
python main.py moonshot-check
```

---

## 📚 Glossar (Wörterbuch für Begriffe)

- **VPS:** Virtueller Server in der Cloud (wie ein Computer den Sie mieten)
- **Proxmox:** Software um viele virtuelle Computer zu verwalten
- **API-Key:** Passwort für Programme (nicht für Menschen)
- **SSH:** Sichere Fernsteuerung eines Computers
- **VPN:** Verschlüsselter Tunnel zwischen Computern
- **LAN:** Lokales Netzwerk (Computer im gleichen Haus)
- **Docker:** Programm-Container (wie Apps auf dem Handy)
- **GPU:** Grafikkarte (gut für AI-Berechnungen)

---

## ❓ Häufige Fragen

**Q: Warum drei Computer statt einem?**
A: Wie im echten Leben: Spezialisierung! Der eine ist öffentlich erreichbar, der andere hat Power, der dritte ist flexibel für Entwicklung.

**Q: Müssen alle drei immer laufen?**
A: Nein! Für Entwicklung reicht ThinkPad. Für Production: VPS + RTX1080.

**Q: Was passiert wenn einer ausfällt?**
A: VPS und RTX1080 können alleine arbeiten. ThinkPad ist nur für Development.

**Q: Ist das nicht kompliziert?**
A: Am Anfang ja, aber dann läuft es automatisch. Wie Auto fahren lernen!

---

**Version:** 1.0
**Created:** 2025-12-20
**Für:** Jung & Alt, Anfänger & Profis0
