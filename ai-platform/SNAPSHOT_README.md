# Snapshot Utility - Projekt-Backup-System

🔄 **Timestamped Snapshots für sichere Entwicklung und Debugging**

## 📸 Was ist das?

Ein einfaches, aber mächtiges Snapshot-System für Ihr J-Jeco Projekt:
- Erstellt timestamped Backups des gesamten Projekts
- Snapshots werden **nie überschrieben**
- Einfaches Rollback bei Problemen
- Automatisches Backup vor jedem Restore
- Perfekt für Debugging und Experimente

## 🚀 Schnellstart

```bash
# Snapshot erstellen
./snapshot.sh create "Vor neuer Feature-Implementation"

# Alle Snapshots anzeigen
./snapshot.sh list

# Snapshot wiederherstellen
./snapshot.sh restore snapshot_20251220_134158

# Alte Snapshots aufräumen (behalte letzte 10)
./snapshot.sh cleanup 10
```

## 📋 Alle Kommandos

### Snapshot erstellen
```bash
./snapshot.sh create [beschreibung]
```

**Beispiele:**
```bash
./snapshot.sh create "Vor Content Creator Agent"
./snapshot.sh create "Funktionierender Zustand - alle Tests grün"
./snapshot.sh create  # Ohne Beschreibung
```

**Was wird gesnapshot:**
- ✅ Alle Projektdateien
- ✅ Python Code
- ✅ Konfiguration
- ✅ README & Docs
- ❌ Virtual Environment (`ai-agents-masterclass/`)
- ❌ Git History (`.git/`)
- ❌ Runtime Data (`data/`, `logs/`, `output/`)
- ❌ API Keys (`.env`)

### Snapshots auflisten
```bash
./snapshot.sh list
```

**Output:**
```
📋 Verfügbare Snapshots:

1. snapshot_20251220_134158
   Erstellt: 2025-12-20 13:41:58
   Größe: 88K
   Info: Initial project state - AI Agents Framework complete

2. snapshot_20251220_150000
   Erstellt: 2025-12-20 15:00:00
   Größe: 120K
   Info: Content Creator Agent implementiert

Total: 2 Snapshot(s)
```

### Snapshot wiederherstellen
```bash
./snapshot.sh restore snapshot_20251220_134158
```

**Sicherheitsfeatures:**
- ⚠️ Zeigt Warnung und fragt nach Bestätigung
- 📸 Erstellt automatisch Backup des aktuellen Zustands
- 🔄 Stellt dann den gewählten Snapshot wieder her
- ✅ Sie verlieren nie Daten!

**Ablauf:**
```
1. Warnung anzeigen
2. Snapshot-Info anzeigen
3. Benutzer-Bestätigung einholen
4. Automatisches Backup erstellen (snapshot_pre_restore_...)
5. Snapshot wiederherstellen
6. Erfolg melden
```

### Snapshot-Info anzeigen
```bash
./snapshot.sh info snapshot_20251220_134158
```

**Output:**
```
Snapshot erstellt: Fr 20. Dez 13:41:58 CET 2025
Timestamp: 20251220_134158
Git Commit: 935e943
Git Branch: main
Beschreibung: Initial project state - AI Agents Framework complete
```

### Snapshot löschen
```bash
./snapshot.sh delete snapshot_20251220_134158
```

⚠️ Fragt nach Bestätigung vor dem Löschen.

### Alte Snapshots aufräumen
```bash
./snapshot.sh cleanup [anzahl]
```

**Beispiele:**
```bash
./snapshot.sh cleanup 10  # Behalte letzte 10 Snapshots
./snapshot.sh cleanup 5   # Behalte letzte 5 Snapshots
./snapshot.sh cleanup     # Behalte letzte 10 (default)
```

Löscht automatisch die **ältesten** Snapshots und behält nur die angegebene Anzahl.

## 📂 Snapshot-Verzeichnis

Snapshots werden gespeichert in:
```
/home/fitna/homelab/snap/J-Jeco/
├── snapshot_20251220_134158/
│   ├── 1-first-agent/
│   ├── .gitignore
│   └── snapshot_info.txt
├── snapshot_20251220_150000/
│   └── ...
└── snapshot_pre_restore_20251220_160000/
    └── ...
```

**Vorteile:**
- Außerhalb des Projekts → kein Versehen beim `git add`
- Übersichtlich organisiert
- Einfach zu browsen

## 🎯 Anwendungsfälle

### 1. Vor riskanten Änderungen
```bash
./snapshot.sh create "Vor Refactoring der Agent-Architektur"
# ... mache Änderungen ...
# Falls etwas schiefgeht:
./snapshot.sh restore snapshot_20251220_xxx
```

### 2. Debugging-Sessions
```bash
# State vor Bug-Reproduktion
./snapshot.sh create "Bug reproduzierbar - vor Fix-Versuch"

# Experimentiere mit Fixes
# ...

# Falls Fix nicht funktioniert, zurück zum Start
./snapshot.sh restore snapshot_20251220_xxx
```

### 3. Regelmäßige Backups
```bash
# Cronjob für tägliche Snapshots
0 2 * * * cd /home/fitna/homelab/J-Jeco && ./snapshot.sh create "Daily backup" && ./snapshot.sh cleanup 7
```

### 4. Vor Git-Operations
```bash
# Vor komplexem Merge/Rebase
./snapshot.sh create "Vor Git Merge"

# Mache Git-Operation
git merge feature-branch

# Falls Merge-Konflikt unlösbar:
./snapshot.sh restore snapshot_20251220_xxx
```

### 5. Experiment-Branches (ohne Git)
```bash
# Snapshot als "Branch"
./snapshot.sh create "Stable - vor Experiment A"

# Experimentiere wild
# ...

# Zurück zu stable
./snapshot.sh restore snapshot_20251220_xxx

# Neues Experiment
./snapshot.sh create "Stable - vor Experiment B"
```

## 🔧 Technische Details

### Was wird ausgeschlossen?
- `ai-agents-masterclass/` - Virtual Environment (zu groß, einfach neu zu erstellen)
- `__pycache__/` und `*.pyc` - Compiled Python (wird neu generiert)
- `.git/` - Git History (separates VCS)
- `data/`, `logs/`, `output/` - Runtime-Daten
- `.env` - API Keys (Sicherheit!)

### Snapshot-Metadaten
Jeder Snapshot enthält `snapshot_info.txt`:
- Zeitstempel
- Git Commit Hash (falls verfügbar)
- Git Branch
- Benutzer-Beschreibung

### Performance
- Kleine Snapshots (~100KB) dank excludes
- Schnelle Erstellung (<1 Sekunde)
- Verwendet `tar` für effizientes Kopieren

## 🛡️ Sicherheit

### Vor Restore:
1. ✅ Automatisches Backup des aktuellen Zustands
2. ✅ Benutzer-Bestätigung erforderlich
3. ✅ Snapshot-Info wird angezeigt

### Datenverlust verhindern:
- Vor jedem Restore → automatisches Backup als `snapshot_pre_restore_...`
- Sie können jederzeit zum Zustand vor dem Restore zurück!

### API Keys:
- `.env` Dateien werden **nicht** gesnapshot
- Ihre API Keys bleiben sicher

## 📊 Best Practices

### 1. Beschreibende Namen
```bash
# ❌ Schlecht
./snapshot.sh create

# ✅ Gut
./snapshot.sh create "Content Creator Agent v1 - funktioniert"
./snapshot.sh create "Vor Upgrade auf LangChain 1.3"
```

### 2. Regelmäßige Cleanups
```bash
# Wöchentlich alte Snapshots aufräumen
./snapshot.sh cleanup 10
```

### 3. Snapshots vor kritischen Operationen
- Vor großen Refactorings
- Vor Dependency-Upgrades
- Vor Produktions-Deployments
- Vor experimentellen Features

### 4. Kombiniere mit Git
```bash
# Git für permanente History
git commit -m "Feature X"

# Snapshot für schnelle Rollbacks während Entwicklung
./snapshot.sh create "Feature X committed - vor nächstem Schritt"
```

## 🆚 Snapshot vs. Git

| Feature | Snapshot | Git |
|---------|----------|-----|
| **Geschwindigkeit** | ⚡ Sehr schnell | 🐢 Langsamer |
| **Einfachheit** | ✅ 1 Befehl | ⚠️ Mehrere Befehle |
| **Permanenz** | 📁 Lokal | ☁️ Remote (nach push) |
| **Kollaboration** | ❌ Nein | ✅ Ja |
| **History** | 📸 Snapshots | 📜 Komplette History |
| **Use Case** | Debugging, Quick Rollback | Versionskontrolle, Team |

**Empfehlung:** Nutzen Sie beide!
- Git für permanente Versionen
- Snapshots für schnelle Experimente

## 🔍 Troubleshooting

### "Snapshot existiert bereits"
Unmöglich durch Timestamp-System. Falls doch:
```bash
# Warte 1 Sekunde und versuche erneut
sleep 1
./snapshot.sh create "Beschreibung"
```

### "Kein Platz mehr"
```bash
# Cleanup alte Snapshots
./snapshot.sh cleanup 5

# Oder manuell löschen
./snapshot.sh delete snapshot_20251220_xxx
```

### Snapshot-Verzeichnis voll
```bash
# Zeige Größe aller Snapshots
du -sh /home/fitna/homelab/snap/J-Jeco/*

# Lösche große/alte Snapshots
./snapshot.sh delete snapshot_xxx
```

## 📚 Beispiel-Workflow

```bash
# Morning: Start des Tages
./snapshot.sh create "Start of day - clean state"

# Feature-Entwicklung
./snapshot.sh create "Vor Content Creator Implementation"
# ... implementiere Feature ...
./snapshot.sh create "Content Creator - erste Version"

# Bug gefunden
./snapshot.sh create "Bug entdeckt - vor Debug-Session"
# ... debugge und fixe ...
./snapshot.sh create "Bug gefixt - funktioniert"

# End of day: Cleanup
./snapshot.sh cleanup 7
git add .
git commit -m "Content Creator Agent implementiert"
git push
```

## 🎉 Quick Reference

```bash
# Create
./snapshot.sh create "Beschreibung"

# List
./snapshot.sh list

# Restore
./snapshot.sh restore snapshot_xxx

# Info
./snapshot.sh info snapshot_xxx

# Delete
./snapshot.sh delete snapshot_xxx

# Cleanup
./snapshot.sh cleanup 10

# Help
./snapshot.sh help
```

---

**Version**: 1.0
**Created**: 2025-12-20
**Location**: `/home/fitna/homelab/J-Jeco/snapshot.sh`

🚀 **Happy Snapshotting!**
