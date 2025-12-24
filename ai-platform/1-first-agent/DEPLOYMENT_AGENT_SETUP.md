# DeploymentOrchestratorAgent - Setup & Usage Guide

## 🎯 Overview

Der DeploymentOrchestratorAgent automatisiert Deployments über 3 Systeme:
- **VPS** (jonas-homelab-vps / 91.107.198.37)
- **ThinkPad** (192.168.16.7)
- **RTX1080** (192.168.17.1)

## ✅ Features

- ✅ Asymmetrisches Error Handling (VPS-Failure ≠ RTX1080-Rollback)
- ✅ Retry mit Exponential Backoff
- ✅ Health Checks zwischen allen Phasen
- ✅ Snapshot-basierter Rollback
- ✅ Structured Status Returns
- ✅ Comprehensive Logging

---

## 🔧 Prerequisites

### 1. SSH-Key Setup

Der Agent benötigt passwortlosen SSH-Zugriff zu allen Systemen:

```bash
# SSH-Keys generieren (falls noch nicht vorhanden)
ssh-keygen -t ed25519 -C "deployment-agent@homelab"

# Public Key zu allen Systemen kopieren
ssh-copy-id jonas-homelab-vps
ssh-copy-id 192.168.16.7
ssh-copy-id 192.168.17.1

# Testen
ssh jonas-homelab-vps "echo OK"
ssh 192.168.16.7 "echo OK"
ssh 192.168.17.1 "echo OK"
```

### 2. Secrets-Sync Script

Stelle sicher, dass `sync-secrets.sh` funktioniert:

```bash
cd /home/fitna/homelab/shared/scripts
./sync-secrets.sh test    # Test connections
./sync-secrets.sh status  # Check sync status
```

### 3. Snapshot Script

Für Rollback-Funktionalität benötigt:

```bash
cd /home/fitna/homelab/shared/scripts
./snapshot.sh list        # List snapshots
./snapshot.sh create test-snapshot
./snapshot.sh rollback test-snapshot
```

### 4. Docker auf allen Hosts

Verifiziere Docker-Installation:

```bash
ssh 192.168.16.7 "docker ps"
ssh 192.168.17.1 "docker ps"
ssh jonas-homelab-vps "docker ps"
```

---

## 🚀 Usage

### Basic Usage

```python
import asyncio
from agents.deployment_orchestrator import DeploymentOrchestratorAgent

async def deploy():
    agent = DeploymentOrchestratorAgent()

    result = await agent.execute({
        "commit_hash": "main",
        "environment": "production",
        "rollback_on_failure": True,
        "skip_tests": False
    })

    print(f"Status: {result['status']}")
    print(f"Systems deployed: {result['systems_deployed']}")
    print(f"Duration: {result['duration_seconds']}s")

asyncio.run(deploy())
```

### Advanced Usage

```python
# Staging deployment with tests
result = await agent.execute({
    "commit_hash": "feature-branch",
    "environment": "staging",
    "rollback_on_failure": True,
    "skip_tests": False  # Run full test suite
})

# Production deployment (skip tests if already validated)
if result['status'] == 'success':
    prod_result = await agent.execute({
        "commit_hash": "feature-branch",
        "environment": "production",
        "rollback_on_failure": True,
        "skip_tests": True  # Already tested in staging
    })
```

---

## 📋 Deployment Workflow

Der Agent führt 8 Phasen aus:

### Phase 1: Pre-flight Validation
- ✅ SSH connectivity check
- ✅ Docker daemon running
- ✅ Disk space check (≥10GB free)
- ✅ No concurrent deployments

### Phase 2: Secrets Sync
- Synchronisiert API-Keys via `sync-secrets.sh`
- Verifiziert Sync auf allen Systemen

### Phase 3: Snapshots
- Erstellt Proxmox Snapshots auf RTX1080
- Rollback-Point für Production

### Phase 4: ThinkPad Deployment (Staging)
- Git pull & checkout commit
- Docker Compose up
- Health checks

### Phase 5: Automated Tests
- Runs pytest suite
- Validates deployment
- **Blocks production if tests fail**

### Phase 6: RTX1080 Deployment (Production)
- Git pull & checkout
- Docker Compose up
- Health checks

### Phase 7: VPS Deployment (Public Services)
- **With retry logic** (3 attempts, exponential backoff)
- **Independent from RTX1080** (partial success allowed)
- Alerts on failure

### Phase 8: Verification
- Comprehensive health checks
- Service availability validation
- **Full rollback if verification fails**

---

## 🔄 Error Handling

### Scenario 1: ThinkPad Deployment Fails
```
Action: Rollback ThinkPad
Status: FAILED
RTX1080: Not touched
VPS: Not touched
```

### Scenario 2: Tests Fail
```
Action: Rollback ThinkPad
Status: FAILED
Note: Production not affected
```

### Scenario 3: RTX1080 Deployment Fails
```
Action: Full rollback (ThinkPad + RTX1080)
Status: ROLLED_BACK
VPS: Not touched
```

### Scenario 4: VPS Deployment Fails (RTX1080 already deployed)
```
Action: VPS rollback only
Status: PARTIAL_SUCCESS
RTX1080: Remains deployed
Alert: Manual intervention required
```

### Scenario 5: Verification Fails
```
Action: Full rollback (all systems)
Status: ROLLED_BACK
```

---

## 📊 Return Status

Der Agent gibt strukturierte Status zurück:

```python
{
    "status": "success" | "partial_success" | "failed" | "aborted" | "rolled_back",
    "phase": "current_phase",
    "systems_deployed": ["thinkpad", "rtx1080", "vps"],
    "duration_seconds": 180,
    "error": None | "error message",
    "details": {
        "pre_flight": {...},
        "secrets_sync": {...},
        "snapshots": {...},
        "thinkpad": {...},
        "tests": {...},
        "rtx1080": {...},
        "vps": {...},
        "verification": {...}
    }
}
```

---

## 🧪 Testing

### Run Test Suite

```bash
cd /home/fitna/homelab/ai-platform/1-first-agent
source ../ai-agents-masterclass/bin/activate
python test_deployment.py
```

### Test Individual Components

```python
from agents.deployment_orchestrator import DeploymentOrchestratorAgent

agent = DeploymentOrchestratorAgent()

# Test pre-flight checks
preflight = await agent._validate_systems_ready()

# Test secrets sync
secrets = await agent._sync_secrets()

# Test health checks
health = await agent._check_system_health("rtx1080")

# Test snapshots
snapshots = await agent._create_snapshots()
```

---

## 🔐 Security

### SSH Keys
- Verwendet Ed25519 Keys (modern, secure)
- Passwortlos (für Automation)
- Separate Keys für Deployment empfohlen

### Secrets Management
- Nutzt bestehende `sync-secrets.sh` Infrastruktur
- .env Dateien niemals in Git
- Verschlüsselte Übertragung (SCP)

### Audit Logging
- Alle Deployments werden geloggt: `logs/deployment_orchestrator.log`
- Timestamps und Status für jeden Schritt
- Fehler werden mit Stack Trace protokolliert

---

## 📈 Monitoring

### Logs

```bash
# Deployment-Logs
tail -f ai-platform/1-first-agent/logs/deployment_orchestrator.log

# System-Logs auf Remote
ssh 192.168.17.1 "docker logs traefik"
```

### Metrics

Agent tracked automatisch:
- `tasks_completed`: Anzahl erfolgreicher Deployments
- `tokens_used`: LLM-Token für Reasoning
- `errors`: Fehler-Counter
- `created_at`: Agent-Start-Zeit

Access via:
```python
metrics = agent.get_metrics()
print(metrics)
```

---

## 🐛 Troubleshooting

### SSH Connection Fails

```bash
# Test SSH-Verbindung
ssh -vvv 192.168.17.1

# Prüfe SSH-Agent
ssh-add -l

# Re-add key
ssh-add ~/.ssh/id_ed25519
```

### Secrets Sync Fails

```bash
# Manual sync
cd /home/fitna/homelab/shared/scripts
./sync-secrets.sh status
./sync-secrets.sh sync

# Prüfe Master Secrets
cat ~/J-Jeco/.env.master | grep API_KEY
```

### Docker Compose Fails

```bash
# Check Docker status
ssh 192.168.17.1 "systemctl status docker"

# Check compose file
ssh 192.168.17.1 "cd ~/homelab && docker compose config"

# Manual deploy
ssh 192.168.17.1 "cd ~/homelab && docker compose up -d"
```

### Snapshot Creation Fails

```bash
# Check Proxmox API
ssh 192.168.17.1 "pvesh get /cluster/resources"

# Check disk space
ssh 192.168.17.1 "df -h"

# Manual snapshot
ssh 192.168.17.1 "/home/fitna/homelab/shared/scripts/snapshot.sh create manual-test"
```

---

## 🔮 Future Enhancements

### Planned Features

- [ ] **GitHub Webhook Integration** - Trigger deployments via GitHub Actions
- [ ] **Telegram Notifications** - Real-time deployment alerts
- [ ] **Blue-Green Deployments** - Zero-downtime deployments
- [ ] **Canary Deployments** - Gradual rollout with traffic splitting
- [ ] **Deployment History** - Database of all deployments
- [ ] **Web Dashboard** - Real-time deployment monitoring
- [ ] **Multi-Branch Support** - Deploy different branches to different environments
- [ ] **Custom Health Checks** - User-definable health check endpoints

### Integration Points

- **CI/CD**: GitHub Actions, GitLab CI, Jenkins
- **Monitoring**: Prometheus, Grafana, Loki
- **Notifications**: Telegram, Email, Slack
- **Orchestration**: Kubernetes, Docker Swarm
- **Infrastructure**: Terraform, Ansible

---

## 📚 References

### CodeRabbit Review Findings

Dieser Agent addressiert folgende CodeRabbit-Findings:

1. ✅ **Asymmetrisches Error Handling** (CODERABBIT_DEPLOYMENT_PROMPT.md:227-230)
2. ✅ **Health Checks zwischen Phasen** (SCHLACHTPLAN_2025.md:435-515)
3. ✅ **Retry-Logic für VPS** (SCHLACHTPLAN_2025.md:587-620)
4. ✅ **Structured Status Returns** (SCHLACHTPLAN_2025.md:549-581)

### Related Documentation

- `/home/fitna/homelab/SCHLACHTPLAN_2025.md` - Overall deployment plan
- `/home/fitna/homelab/shared/scripts/sync-secrets.sh` - Secrets management
- `/home/fitna/homelab/CODERABBIT_DEPLOYMENT_PROMPT.md` - CodeRabbit analysis

---

## 💡 Quick Start Checklist

- [ ] SSH-Keys zu allen Systemen kopiert
- [ ] `sync-secrets.sh test` erfolgreich
- [ ] `snapshot.sh list` funktioniert
- [ ] Docker auf allen Hosts läuft
- [ ] Virtual Environment aktiviert
- [ ] Test-Suite ausgeführt: `python test_deployment.py`
- [ ] Erste Staging-Deployment: `commit_hash=dev, environment=staging`
- [ ] Production-Deployment: `commit_hash=main, environment=production`

---

**Version**: 1.0
**Created**: 2024-12-24
**Agent Version**: 0.2.0
**Status**: ✅ Production Ready (nach SSH-Setup)
