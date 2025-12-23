# Schritt-für-Schritt: Zusätzliche Security Checks implementieren

## 📚 Inhaltsverzeichnis

1. [Überblick: Was wurde hinzugefügt?](#überblick)
2. [Check 1: Dockerfile Scanning](#dockerfile-scanning)
3. [Check 2: Dependency Scanning](#dependency-scanning)
4. [Check 3: Secret Detection](#secret-detection)
5. [Testen & Debuggen](#testen--debuggen)
6. [Optionale Erweiterungen](#optionale-erweiterungen)

---

## Überblick

**Drei neue Security Jobs wurden zu `Team 2` hinzugefügt:**

| Job | Was es tut | Status |
|-----|-----------|--------|
| `security-scan-dockerfiles` | Findet Misconfigurations in Dockerfiles | ✅ Implementiert |
| `security-scan-dependencies` | Sucht CVEs in npm/pip/go Packages | ✅ Implementiert |
| `security-scan-secrets` | Findet Hardcoded API Keys & Tokens | ✅ Implementiert |

**Status der Workflow-Datei**: `.github/workflows/ci-pre-deploy.yml`
- Alle 3 Jobs sind bereits eingefügt
- Sie laufen parallel für schnelle Ausführung
- Sie sind derzeit **nicht-blockierend** (advisory only)

---

## Dockerfile Scanning

### Was macht dieser Check?

Scannt alle `Dockerfile*` Dateien im Repository auf Sicherheitsprobleme:

✅ Findet: Root-User, fehlende Healthchecks, alte Base-Images, exposed Ports ohne EXPOSE  
❌ Blockiert Deploy: Nein (advisory)

### Wo ist der Job in der Workflow-Datei?

Datei: `.github/workflows/ci-pre-deploy.yml`

Suche nach:
```yaml
security-scan-dockerfiles:
  name: "Trivy: Dockerfile Scanning"
```

### Wie funktioniert er?

**Schritt 1**: Findet alle Dockerfiles
```bash
find . -name "Dockerfile*" -type f | grep -v ".git"
```

**Schritt 2**: Scannt mit Trivy config scan
```bash
trivy config . --format sarif --output trivy-dockerfile.sarif
```

**Schritt 3**: Uploaded Report zu GitHub Security
- Tab: **Security** → **Code scanning** → `trivy-dockerfile`

### Beispiel-Output

```
Found Dockerfiles:
  - Dockerfile
  - Dockerfile.prod
  - docker/build/Dockerfile.ci

Scanning...
⚠️ HIGH issues found:
  ✗ AVD-DS-0001: Container should not run as root
    File: Dockerfile:5
    Reason: USER directive not set
  
  ✗ AVD-DS-0002: Healthcheck should be defined
    File: Dockerfile:8
    Reason: No HEALTHCHECK instruction
```

### So aktivierst du STRICT Mode (lässt Deploy FEHLSCHLAGEN)

**Situation**: Du willst, dass Deploy fehlschlägt, wenn kritische Dockerfile-Issues gefunden werden.

**Schritte**:

1. Öffne `.github/workflows/ci-pre-deploy.yml`
2. Suche `security-scan-dockerfiles` Job
3. Finde die Zeile:
```yaml
exit-code: '0'  # Advisory only
```

4. Ändere zu:
```yaml
exit-code: '1'  # Will fail deployment on HIGH/CRITICAL
```

5. Commit & Push:
```powershell
git add .github/workflows/ci-pre-deploy.yml
git commit -m "Enable strict Dockerfile scanning"
git push
```

6. Beim nächsten PR wird der Check streng angewendet

### So ignorierst du False Positives

**Problem**: Der Check meldet etwas, das ok ist.

**Lösung**: Füge Trivy ignore-Kommentar in Dockerfile ein:

```dockerfile
# In Dockerfile
FROM ubuntu:22.04

# trivy:ignore=AVD-DS-0001
RUN apt-get install myapp

# trivy:ignore=AVD-DS-0002,AVD-DS-0003
COPY . /app
```

---

## Dependency Scanning

### Was macht dieser Check?

Findet bekannte Sicherheitslücken (CVEs) in Abhängigkeiten:

- **Python**: Scannt `requirements.txt`, `setup.py`, `pyproject.toml`
- **Node.js**: Scannt `package.json` (via npm audit)
- **Go**: Detektiert go.mod vulnerabilities

✅ Findet: CVE-2023-1234 in requests 2.28.0 (sollte 2.29.0 sein)  
❌ Blockiert Deploy: Nein (advisory only, es sei denn, du aktivierst strict mode)

### Wo ist der Job in der Workflow-Datei?

Datei: `.github/workflows/ci-pre-deploy.yml`

Suche nach:
```yaml
security-scan-dependencies:
  name: "Dependency Check (npm/pip/go)"
```

### Wie funktioniert er?

**Schritt 1**: Prüft auf Dependency-Dateien
```bash
# Findet diese Dateien automatisch:
- package.json (Node.js)
- requirements*.txt (Python)
- setup.py, pyproject.toml (Python)
- go.mod (Go)
```

**Schritt 2**: Scannt mit `safety` (für Python)
```bash
pip install safety
safety check --json > safety-report.json
```

**Schritt 3**: Scannt mit Trivy (alle Sprachen)
```bash
trivy fs . --severity HIGH,CRITICAL
```

### Beispiel-Output

```
ℹ️ Found Python dependency files:
  - requirements.txt
  - requirements-dev.txt

🔍 Python dependency scan completed:
  ✗ CVE-2023-0123: requests 2.28.0
    Affected: 2.28.0
    Fixed: >= 2.29.0
    Severity: HIGH

✓ Found 1 HIGH vulnerability
```

### So aktivierst du STRICT Mode

**Situation**: Du möchtest, dass Deployments fehlschlagen, wenn kritische Abhängigkeits-CVEs gefunden werden.

**Schritte**:

1. Öffne `.github/workflows/ci-pre-deploy.yml`
2. Suche `security-scan-dependencies` → Schritt `Scan Python dependencies with safety`
3. Finde:
```yaml
- run: |
    pip install safety
    safety check --json > safety-report.json 2>&1 || true
    ...
  continue-on-error: true
```

4. Ändere `continue-on-error: true` zu `false`:
```yaml
continue-on-error: false  # Will now fail on CVEs
```

5. Commit & Push:
```powershell
git add .github/workflows/ci-pre-deploy.yml
git commit -m "Enable strict dependency scanning"
git push
```

### So ignorierst du falsche Positive

**Problem**: Der Check findet ein CVE, das im Kontext nicht relevant ist (z. B. dev-dependency).

**Lösung 1**: Nutze requirements-dev.txt für Dev-Dependencies
```bash
# In CI, nur production scannen:
safety check requirements.txt --json
```

**Lösung 2**: Aktualisiere oder pin die Abhängigkeit
```bash
# requirements.txt
requests==2.29.0  # Updated to safe version
```

---

## Secret Detection

### Was macht dieser Check?

Findet hardcoded Secrets im Code:

✅ Findet:
- AWS Access Keys
- GitHub Personal Access Tokens
- API Keys (OpenAI, Stripe, etc.)
- Private SSH Keys
- Database Passwords

❌ Blockiert Deploy: Ja (findet verifizierte Secrets) – das ist **Sicherheitsfeature**

### Wo ist der Job in der Workflow-Datei?

Datei: `.github/workflows/ci-pre-deploy.yml`

Suche nach:
```yaml
security-scan-secrets:
  name: "Secret Detection (TruffleHog)"
```

### Wie funktioniert er?

**Nutzt TruffleHog**: Industry-Standard secret scanner (von Truffle Security)

**Scans**:
1. Aktuellen Git Branch
2. Git History (letzte Commits)
3. Nur verifizierte Secrets (keine False Positives)

**Beispiel-Ausführung**:
```bash
trufflehog git file://. --only-verified
```

### Beispiel-Output

```
🔍 Found potential secrets:
  ✗ AWS Access Key ID
    Pattern: AWS
    File: ansible/vars/prod.yml
    Line: 42
  
  ✗ GitHub Personal Access Token
    Pattern: GitHub
    File: .env.backup
    Line: 15
```

### Was tun, wenn du ein Secret findest?

**WICHTIG**: Wenn TruffleHog echte Secrets findet, sind diese bereits ins Git committed!

**Sofort-Maßnahmen**:

1. **GitHub Secret Scanner mitteilen** (automatisch getan)

2. **Regeneriere den Secret** (z. B. GitHub Token):
   - Gehe zu GitHub Settings → Developer settings → Personal access tokens
   - Lösche das alte Token
   - Erstelle ein neues Token

3. **Entferne Secret aus Git**:
```bash
# Option A: Aus aktueller Datei entfernen und commit
git rm .env.backup
git commit -m "Remove .env.backup with exposed secrets"
git push

# Option B: Rewrite git history (wenn es recent ist)
git filter-branch --tree-filter 'rm -f ansible/vars/prod.yml' HEAD
git push --force
```

4. **Aktiviere Secret Scanning** in GitHub (wenn nicht schon):
   - Settings → Security & analysis → Secret scanning
   - Enable "Push protection" (verhindert weitere Secret-Commits)

### So ignorierst du False Positives

**Problem**: TruffleHog meldet einen Secret, der keiner ist.

**Lösung**: Nutze TruffleHog Allowlist

```yaml
security-scan-secrets:
  steps:
    - uses: trufflesecurity/trufflehog@main
      with:
        extra_args: --only-verified --exclude-paths .git|tests/fixtures
```

---

## Testen & Debuggen

### Lokales Testing (ohne GitHub)

Du kannst die Checks lokal testen, bevor du sie commitest:

#### Test 1: Dockerfile Scanning

```powershell
# Installiere trivy
choco install trivy

# Oder via docker:
docker run --rm -v ${PWD}:/root aquasec/trivy:latest config ./docker
```

#### Test 2: Dependency Scanning

```powershell
# Python Packages
pip install safety
safety check requirements.txt

# Oder Trivy
trivy fs . --severity HIGH,CRITICAL
```

#### Test 3: Secret Detection

```powershell
# Installiere trufflehog
pip install truffleHog3

# Oder docker:
docker run --rm -v ${PWD}:/root trufflesecurity/trufflehog:latest \
  filesystem /root --debug --only-verified
```

### GitHub Workflow Debugging

**Schritt 1**: Push auf Feature Branch
```powershell
git checkout -b feature/test-security
git add .
git commit -m "Test security checks"
git push origin feature/test-security
```

**Schritt 2**: Erstelle PR
- Gehe zu GitHub → Create Pull Request
- Base: `main`, Compare: `feature/test-security`

**Schritt 3**: Beobachte Workflow
- Tab: **Actions** → wähle PR workflow aus
- Klicke auf Job → Expanded Details

**Schritt 4**: Logs prüfen
- Bei Fehler: Klicke auf fehlenden Step
- Siehe vollständige Output

### Häufige Fehler

**Fehler 1**: "Dockerfile not found"
```
❌ No Dockerfiles found in repository
```
**Lösung**: Du hast keine Dockerfiles. Das ist OK! Der Check ist optional.

**Fehler 2**: "Safety failed - dependency vulnerabilities"
```
❌ CVE-2023-0123: requests 2.28.0
```
**Lösung**: Aktualisiere die Abhängigkeit:
```bash
pip install --upgrade requests
pip freeze > requirements.txt
```

**Fehler 3**: "TruffleHog found secret!"
```
❌ AWS Access Key detected in file
```
**Lösung**: Siehe Sektion "Secret Detection" → "Was tun, wenn du ein Secret findest?"

---

## Optionale Erweiterungen

### Option 1: Strikten Mode für einen Check aktivieren

Beispiel: Nur Dockerfiles blockieren, andere bleiben advisory

```yaml
security-scan-dockerfiles:
  exit-code: '1'  # BLOCKIERT

security-scan-dependencies:
  exit-code: '0'  # Advisory only
  
security-scan-secrets:
  # Default: blockiert
```

### Option 2: Neue Checks hinzufügen

Beispiel: **Semgrep SAST Scanning** hinzufügen

```yaml
# Füge diesen Job vor healthcheck-simulation ein:

security-scan-sast:
  name: "SAST: Code Analysis (Semgrep)"
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    
    - name: Run Semgrep
      uses: returntocorp/semgrep-action@v1
      with:
        config: p/owasp-top-ten
        generateSarif: true
        sarif_file: semgrep.sarif
    
    - name: Upload to GitHub Security
      uses: github/codeql-action/upload-sarif@v2
      with:
        sarif_file: semgrep.sarif
```

Dann `security-scan-sast` zu `pre-deploy-gate.needs` hinzufügen.

### Option 3: Policy Gates konfigurieren

Beispiel: Nur CRITICAL Findings blockieren, HIGH nur warnen

```yaml
security-scan-trivy:
  steps:
    - run: |
        trivy fs . --severity CRITICAL --exit-code 1
        trivy fs . --severity HIGH
```

---

## Zusammenfassung: Deine nächsten Schritte

1. ✅ **3 neue Checks sind bereits implementiert** in `.github/workflows/ci-pre-deploy.yml`

2. **Zum Testen**:
   ```powershell
   git checkout -b feature/test-security-checks
   git add .github/workflows/ci-pre-deploy.yml
   git commit -m "Test expanded security checks"
   git push origin feature/test-security-checks
   # Erstelle PR und beobachte die Checks
   ```

3. **Zum Aktivieren von Strict Mode** (falls gewünscht):
   - Ändere `exit-code: '0'` zu `exit-code: '1'` für den gewünschten Job
   - Commit und Push

4. **Bei gefundenen Problemen**:
   - Logs in GitHub Actions prüfen
   - Lokal mit Trivy/Safety/TruffleHog testen
   - Fixes committed und erneut testen

5. **Weitere Checks hinzufügen**:
   - Nutze das "Template: Add Your Own Security Check" in `docs/09-CI-CD-Pipeline.md`

---

**Fragen?** Siehe `docs/09-CI-CD-Pipeline.md` für ausführliche Dokumentation.
