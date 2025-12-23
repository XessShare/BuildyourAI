# Quick Reference: Security Checks Cheat Sheet

## 📍 Datei-Locations

```
.github/
├── workflows/
│   └── ci-pre-deploy.yml          ← Workflow-Datei mit allen 3 neuen Jobs
└── copilot-instructions.md        ← Aktualisiert mit CI/CD Referenzen

docs/
├── 09-CI-CD-Pipeline.md           ← Ausführliche Dokumentation
└── 10-Implementation-Guide.md     ← Schritt-für-Schritt Anleitung (diese Datei)
```

---

## 🔧 Schnelle Anpassungen

### Strict Mode aktivieren (Job blockiert Deploy)

**Dockerfile Scanning**:
```bash
# Datei: .github/workflows/ci-pre-deploy.yml
# Job: security-scan-dockerfiles
# Ändere: exit-code: '0' → exit-code: '1'
```

**Dependency Scanning**:
```bash
# Job: security-scan-dependencies
# Ändere: continue-on-error: true → continue-on-error: false
```

**Secret Detection**:
```bash
# Job: security-scan-secrets
# Standard: blockiert bereits (keine Änderung nötig)
```

### Pfade ignorieren

```yaml
# Dockerfile Scan:
scan-ref: 'docker/stacks/ ansible/'

# Dependency Scan:
skip-dirs: 'tests,docs,examples'

# Secret Detection:
extra_args: --exclude-paths .git|tests|docs
```

---

## 🧪 Lokales Testen

### 1. Dockerfile Scanning
```powershell
docker run --rm -v ${PWD}:/root aquasec/trivy:latest \
  config /root/docker --format table --severity HIGH
```

### 2. Dependency Scanning
```powershell
# Python
pip install safety
safety check requirements.txt

# Oder Trivy für alles:
docker run --rm -v ${PWD}:/root aquasec/trivy:latest \
  fs /root --severity HIGH --skip-dirs node_modules,__pycache__
```

### 3. Secret Detection
```powershell
docker run --rm -v ${PWD}:/root trufflesecurity/trufflehog:latest \
  filesystem /root --debug --only-verified
```

---

## 📊 Workflow-Status Übersicht

```
Team 1 (Syntax, ~45s)
├─ ✓ validate-compose
├─ ✓ validate-yaml
└─ ✓ validate-ansible

Team 2 (Security, ~5-8 min) [parallel]
├─ security-scan-trivy (advisory)
├─ security-scan-docker-images (advisory)
├─ security-scan-dockerfiles (NEW - advisory)
├─ security-scan-dependencies (NEW - advisory)
└─ security-scan-secrets (NEW - BLOCKING)

Team 3 (Health, ~1 min)
└─ ✓ healthcheck-simulation

Team 4 (Consistency, ~1 min)
└─ ✓ consistency-check

→ pre-deploy-gate (aggregates all results)
  └─ PASS: Teams 1 & 4 = success
  └─ WARN: Teams 2 & 3 can fail (advisory)

→ deploy (main branch only)
```

---

## ⚡ Häufige Aufgaben

### Problem: Dockerfile-Check meldet False Positive

**In Dockerfile hinzufügen**:
```dockerfile
# trivy:ignore=AVD-DS-0001
RUN apt-get install mypackage
```

### Problem: Abhängigkeits-CVE ist alt und bekannt

**requirements.txt** aktualisieren:
```bash
pip install --upgrade PACKAGENAME
pip freeze > requirements.txt
```

### Problem: Secret wurde committed (CRITICAL!)

```bash
# 1. Regeneriere das Secret (GitHub Token etc.)
# 2. Entferne aus Git:
git rm .env.backup
git commit -m "Remove exposed secrets"
git push

# 3. Optional: rewrite history (bei recent commit)
git filter-branch --tree-filter 'rm -f secrets-file' HEAD
git push --force
```

### Problem: CI schlägt fehl, aber ich sehe keine Logs

**Lösung**:
1. GitHub → **Actions** Tab
2. Klicke auf PR workflow
3. Klicke auf fehlenden Job
4. Expand fehlenden Step
5. Siehe full output

---

## 📝 Checkliste: Neuen Job hinzufügen

```
□ 1. Job-Template unter Team 2 kopieren
□ 2. Job-Namen ändern (z.B. security-scan-codescan)
□ 3. Alle `uses:` und `with:` anpassen
□ 4. Zu pre-deploy-gate.needs hinzufügen
□ 5. In gate status check output-Zeile hinzufügen
□ 6. Commit, push, PR erstellen
□ 7. Workflow-Logs überprüfen
```

---

## 🔗 Wichtige Links

- **Workflow-Datei**: `.github/workflows/ci-pre-deploy.yml`
- **Docs**: `docs/09-CI-CD-Pipeline.md`
- **Umsetzungsanleitung**: `docs/10-Implementation-Guide-Security-Checks.md`
- **Copilot Instructions**: `.github/copilot-instructions.md`

---

## 🎯 Default-Verhalten (nach Implementation)

| Job | Blockiert? | Reporte zu | Aktion bei Fehler |
|-----|-----------|-----------|------------------|
| validate-compose | ✓ Ja | - | Deploy blockiert |
| validate-yaml | ✓ Ja | - | Deploy blockiert |
| validate-ansible | ✓ Ja | - | Deploy blockiert |
| security-scan-trivy | ✗ Nein | GitHub Security | Warnung PR |
| security-scan-dockerfiles | ✗ Nein | GitHub Security | Warnung PR |
| security-scan-dependencies | ✗ Nein | GitHub Security | Warnung PR |
| security-scan-secrets | ✓ Ja (verified) | GitHub Security | PR Comment |
| consistency-check | ✓ Ja | - | Deploy blockiert |

---

## 💡 Pro-Tipps

1. **Erst advisory, dann strict**: Starte mit `exit-code: 0`, beobachte PRs, dann zu strict übergehen
2. **Exclude nicht forgessen**: skip-dirs für node_modules, .git etc. = schneller
3. **Local first**: Test lokal, bevor du in CI pusht
4. **Logs speichern**: Für debugging – exportier CI logs, falls nötig
5. **Version pinnen**: Trivy, Semgrep etc. – pin versions für consistency

---

**Zuletzt aktualisiert**: 2025-11-30  
**Status**: 3 neue Jobs implementiert, bereit zum Testing
