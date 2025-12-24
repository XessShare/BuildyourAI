# SSH Setup Guide für DeploymentOrchestratorAgent

## 🔍 Aktueller Status (2024-12-24)

### Test-Ergebnisse:

| System | Host | Status | Problem |
|--------|------|--------|---------|
| **VPS** | jonas-homelab-vps (91.107.198.37) | ❌ Permission denied | Public Key nicht autorisiert |
| **ThinkPad** | 192.168.16.7 | ❌ Permission denied | Public Key nicht autorisiert |
| **RTX1080** | 192.168.17.1 | ❌ No route to host | Netzwerk nicht erreichbar |

### SSH-Key Status:
- ✅ SSH-Key existiert: `~/.ssh/id_ed25519`
- ✅ SSH-Agent läuft: PID 258633
- ✅ Key im Agent: `fitna@github`

---

## 🔧 Lösungsschritte

### Option A: Automatisches Setup (empfohlen wenn Passwort-Login möglich)

```bash
# 1. Public Key anzeigen (zum manuellen Kopieren)
cat ~/.ssh/id_ed25519.pub

# 2. VPS Setup
ssh-copy-id jonas-homelab-vps
# Wenn Root-User erforderlich:
ssh-copy-id root@jonas-homelab-vps

# 3. ThinkPad Setup
ssh-copy-id fitna@192.168.16.7

# 4. RTX1080 Setup (wenn im lokalen Netzwerk)
ssh-copy-id fitna@192.168.17.1
```

### Option B: Manuelles Setup (wenn ssh-copy-id nicht funktioniert)

#### Für VPS (jonas-homelab-vps):

```bash
# 1. Public Key kopieren
cat ~/.ssh/id_ed25519.pub

# 2. Auf VPS einloggen (mit Passwort)
ssh jonas-homelab-vps
# oder als root:
ssh root@91.107.198.37

# 3. Auf dem VPS:
mkdir -p ~/.ssh
chmod 700 ~/.ssh
echo "HIER_PUBLIC_KEY_EINFÜGEN" >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
exit

# 4. Test
ssh jonas-homelab-vps "echo VPS OK"
```

#### Für ThinkPad (192.168.16.7):

```bash
# Gleicher Prozess wie VPS
ssh fitna@192.168.16.7

# Auf ThinkPad:
mkdir -p ~/.ssh
chmod 700 ~/.ssh
echo "HIER_PUBLIC_KEY_EINFÜGEN" >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
exit

# Test
ssh 192.168.16.7 "echo ThinkPad OK"
```

#### Für RTX1080 (192.168.17.1):

**Problem**: "No route to host" bedeutet, dass das System vom aktuellen Rechner nicht erreichbar ist.

**Mögliche Ursachen**:
1. RTX1080 ist in einem anderen Netzwerk (z.B. 192.168.17.x vs 192.168.16.x)
2. VPN/WireGuard nicht aktiv
3. Firewall blockiert Zugriff

**Lösungen**:

```bash
# Option 1: Via VPS als Jump Host
ssh -J jonas-homelab-vps fitna@192.168.17.1

# Option 2: Via ThinkPad als Jump Host (wenn im gleichen LAN)
ssh -J 192.168.16.7 fitna@192.168.17.1

# Option 3: Direkt vom ThinkPad aus
# Erst auf ThinkPad einloggen, dann von dort aus:
ssh fitna@192.168.16.7
ssh-copy-id fitna@192.168.17.1
```

### Option C: SSH Config mit Jump Hosts

Erstelle/Editiere `~/.ssh/config`:

```bash
# VPS (direkt erreichbar)
Host vps
    HostName 91.107.198.37
    User fitna
    IdentityFile ~/.ssh/id_ed25519

Host jonas-homelab-vps
    HostName 91.107.198.37
    User fitna
    IdentityFile ~/.ssh/id_ed25519

# ThinkPad (direkt erreichbar)
Host thinkpad
    HostName 192.168.16.7
    User fitna
    IdentityFile ~/.ssh/id_ed25519

# RTX1080 (via VPS Jump Host)
Host rtx1080
    HostName 192.168.17.1
    User fitna
    IdentityFile ~/.ssh/id_ed25519
    ProxyJump jonas-homelab-vps

# Alternative: RTX1080 via ThinkPad
Host rtx1080-local
    HostName 192.168.17.1
    User fitna
    IdentityFile ~/.ssh/id_ed25519
    ProxyJump thinkpad
```

Nach SSH Config Setup:

```bash
# Test mit Aliases
ssh vps "echo VPS OK"
ssh thinkpad "echo ThinkPad OK"
ssh rtx1080 "echo RTX1080 OK"
```

---

## 🧪 Verifikation

Nach dem Setup, führe diese Tests aus:

```bash
# 1. Basis-Verbindungstest
ssh jonas-homelab-vps "echo VPS: OK"
ssh 192.168.16.7 "echo ThinkPad: OK"
ssh 192.168.17.1 "echo RTX1080: OK"

# 2. Docker-Test
ssh jonas-homelab-vps "docker ps"
ssh 192.168.16.7 "docker ps"
ssh 192.168.17.1 "docker ps"

# 3. Secrets-Sync Test
cd /home/fitna/homelab/shared/scripts
./sync-secrets.sh test

# 4. DeploymentAgent Test
cd /home/fitna/homelab/ai-platform/1-first-agent
source ../ai-agents-masterclass/bin/activate
python test_deployment.py
```

---

## 🔒 Sicherheit

### Best Practices implementiert:

✅ **Ed25519 Keys** (modern, secure)
```bash
# Key Info:
ssh-keygen -l -f ~/.ssh/id_ed25519.pub
```

✅ **Key-basierte Auth** (kein Passwort)
```bash
# Test passwordless
ssh -o BatchMode=yes jonas-homelab-vps "echo OK"
```

### Zusätzliche Härtung (optional):

```bash
# Auf Remote-Systemen:
# 1. Disable password auth
sudo sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config

# 2. Only allow specific user
echo "AllowUsers fitna" | sudo tee -a /etc/ssh/sshd_config

# 3. Restart SSH
sudo systemctl restart sshd
```

---

## 🚨 Troubleshooting

### Problem: "Permission denied (publickey)"

```bash
# Debug-Modus
ssh -vvv jonas-homelab-vps

# Prüfe:
# 1. Wird der richtige Key verwendet?
# 2. Ist der Key im authorized_keys auf dem Remote?
# 3. Sind die Permissions korrekt?

# Auf Remote prüfen:
ssh jonas-homelab-vps
ls -la ~/.ssh/
cat ~/.ssh/authorized_keys | grep "fitna@github"
```

### Problem: "No route to host"

```bash
# 1. Ping-Test
ping -c 3 192.168.17.1

# 2. Netzwerk-Route prüfen
ip route get 192.168.17.1

# 3. Firewall-Status
sudo ufw status

# 4. Via Jump Host versuchen
ssh -J 192.168.16.7 192.168.17.1
```

### Problem: "Host key verification failed"

```bash
# Remove old key
ssh-keygen -R 192.168.16.7
ssh-keygen -R 192.168.17.1
ssh-keygen -R jonas-homelab-vps

# Neu verbinden (akzeptiert neuen Key)
ssh jonas-homelab-vps
```

---

## 📋 Checkliste

Nach erfolgreichem Setup:

- [ ] VPS: Passwortloser SSH-Login funktioniert
- [ ] ThinkPad: Passwortloser SSH-Login funktioniert
- [ ] RTX1080: SSH-Login funktioniert (direkt oder via Jump Host)
- [ ] Docker auf allen Hosts erreichbar
- [ ] `sync-secrets.sh test` erfolgreich
- [ ] `test_deployment.py` zeigt grüne Tests
- [ ] SSH Config für Aliases erstellt
- [ ] Alte Passwort-Auth deaktiviert (optional)

---

## 🎯 Nächste Schritte nach SSH-Setup

Sobald alle SSH-Verbindungen funktionieren:

1. **Deployment-Tests durchführen**
   ```bash
   python test_deployment.py
   ```

2. **Erste Staging-Deployment**
   ```python
   result = await agent.execute({
       "commit_hash": "main",
       "environment": "staging"
   })
   ```

3. **Production-Deployment**
   ```python
   result = await agent.execute({
       "commit_hash": "main",
       "environment": "production"
   })
   ```

---

**Version**: 1.0
**Created**: 2024-12-24
**Status**: ⏳ Awaiting SSH Setup
