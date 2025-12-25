# Pre-Deployment Checklist - Homelab OSS Stack

**Use this checklist before deploying to ensure everything is ready.**

---

## 🔴 CRITICAL (Must Complete)

### 1. Environment Configuration

- [ ] Copy `.env.example` to `.env`
  ```bash
  cp .env.example .env
  ```

- [ ] Edit `.env` with your actual values:
  ```bash
  nano .env  # or vim, code, etc.
  ```

- [ ] **Required Variables to Set:**
  - [x] `DOMAIN=Jonas-J.de	`
  - [x] `HOMELAB_IP_A=192.168.16.7` (pve-thinkpad)
  - [x] `HOMELAB_IP_B=192.168.17.1` (pve-ryzen)
    - [x] `CLOUDFLARE_EMAIL=ai.jaeger@hotmail.com`
  - [ ] `CLOUDFLARE_API_KEY=your-api-key`
  - [ ] Open router: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
  - [ ] `AUTHENTIK_POSTGRESQL_PASSWORD=` (generate strong password)
  - [ ] `POSTGRES_PASSWORD=` (generate strong password)
  - [ ] `PIHOLE_PASSWORD=` (generate strong password)
  - [ ] `GRAFANA_ADMIN_PASSWORD=` (generate strong password)

- [ ] Generate secure passwords:
  ```bash
  # Generate random 50-char secret
  openssl rand -base64 50
  
  # Or use pwgen
  pwgen -s 32 1
  ```

### 2. Docker Network Creation

- [ ] Create network on **Host A** (192.168.16.7):
  ```bash
  ssh root@192.168.16.7 "docker network create homelab_network"
  ```

- [ ] Create network on **Host B** (192.168.17.1):
  ```bash
  ssh root@192.168.17.1 "docker network create homelab_network"
  ```

### 3. Mosquitto Password Setup

- [ ] Create Mosquitto password file:
  ```bash
  docker run --rm -it -v $(pwd)/docker/mosquitto:/mosquitto/config \
    eclipse-mosquitto mosquitto_passwd -c /mosquitto/config/passwd mqtt
  ```

- [ ] Verify password file exists:
  ```bash
  ls -la docker/mosquitto/passwd
  ```

### 4. Firewall Configuration

- [ ] Allow inter-host communication on **Host A**:
  ```bash
  ssh root@192.168.16.7 <<'EOF'
  ufw allow from 192.168.17.0/24
  ufw allow from 100.64.0.0/10  # Tailscale (optional)
  ufw reload
  EOF
  ```

- [ ] Allow inter-host communication on **Host B**:
  ```bash
  ssh root@192.168.17.1 <<'EOF'
  ufw allow from 192.168.16.0/24
  ufw allow from 100.64.0.0/10  # Tailscale (optional)
  ufw reload
  EOF
  ```

---

## 🟡 HIGH PRIORITY (Strongly Recommended)

### 5. SSH Key Setup

- [ ] Generate SSH key (if not exists):
  ```bash
  ssh-keygen -t ed25519 -C "homelab-deployment"
  ```

- [ ] Copy key to **Host A**:
  ```bash
  ssh-copy-id root@192.168.16.7
  ```

- [ ] Copy key to **Host B**:
  ```bash
  ssh-copy-id root@192.168.17.1
  ```

- [ ] Test SSH access:
  ```bash
  ssh root@192.168.16.7 "echo 'Host A connected'"
  ssh root@192.168.17.1 "echo 'Host B connected'"
  ```

### 6. Directory Structure

- [ ] Create directories on **Host A**:
  ```bash
  ssh root@192.168.16.7 <<'EOF'
  mkdir -p /opt/homelab/{traefik,mosquitto,prometheus,grafana,homeassistant}
  mkdir -p /var/log/homelab
  chmod 755 /opt/homelab
  EOF
  ```

- [ ] Create directories on **Host B**:
  ```bash
  ssh root@192.168.17.1 <<'EOF'
  mkdir -p /opt/homelab/{postgres,redis}
  mkdir -p /mnt/media/{tv,movies,downloads,books}
  chmod 755 /opt/homelab
  chmod 777 /mnt/media/*  # For media stack access
  EOF
  ```

### 7. Docker Installation Verification

- [ ] Check Docker on **Host A**:
  ```bash
  ssh root@192.168.16.7 "docker --version && docker compose version"
  ```

- [ ] Check Docker on **Host B**:
  ```bash
  ssh root@192.168.17.1 "docker --version && docker compose version"
  ```

- [ ] If Docker not installed, run:
  ```bash
  curl -fsSL https://get.docker.com | sh
  ```

### 8. File Transfer to Hosts

- [ ] Copy project to **Host A**:
  ```bash
  rsync -av --exclude='.git' \
    /run/media/fitna/FCA86951A8690C08/Users/Xess/.claude-worktrees/homelab-oss-stack/brave-snyder/ \
    root@192.168.16.7:/opt/homelab/
  ```

- [ ] Copy required files to **Host B**:
  ```bash
  rsync -av --exclude='.git' \
    /run/media/fitna/FCA86951A8690C08/Users/Xess/.claude-worktrees/homelab-oss-stack/brave-snyder/docker/stacks/ \
    root@192.168.17.1:/opt/homelab/
  ```

---

## 🟢 MEDIUM PRIORITY (Nice to Have)

### 9. DNS Configuration

- [ ] Point your domain to Cloudflare
- [ ] Create DNS records (if using Cloudflare Tunnel):
  - `*.yourdomain.com` → Cloudflare Tunnel
  - Or individual records for each service

### 10. Backups Setup

- [ ] Install Restic (for backups):
  ```bash
  apt install restic
  ```

- [ ] Configure backup repository
- [ ] Test backup/restore procedure

### 11. Monitoring Prep

- [ ] Download Grafana dashboards (optional):
  - Node Exporter Full (ID: 1860)
  - Docker Container & Host (ID: 893)
  - Traefik (ID: 11462)

---

## ✅ PRE-DEPLOYMENT VALIDATION

### Quick Validation Script

Run this to validate your setup:

```bash
#!/bin/bash
echo "=== Pre-Deployment Validation ==="

# Check .env file
if [ -f .env ]; then
  echo "✓ .env file exists"
else
  echo "✗ .env file missing! Copy from .env.example"
  exit 1
fi

# Check SSH access
if ssh -o ConnectTimeout=5 root@192.168.16.7 "exit" 2>/dev/null; then
  echo "✓ SSH to Host A (192.168.16.7) works"
else
  echo "✗ Cannot SSH to Host A"
fi

if ssh -o ConnectTimeout=5 root@192.168.17.1 "exit" 2>/dev/null; then
  echo "✓ SSH to Host B (192.168.17.1) works"
else
  echo "✗ Cannot SSH to Host B"
fi

# Check Docker
if ssh root@192.168.16.7 "docker ps" &>/dev/null; then
  echo "✓ Docker running on Host A"
else
  echo "✗ Docker not running on Host A"
fi

if ssh root@192.168.17.1 "docker ps" &>/dev/null; then
  echo "✓ Docker running on Host B"
else
  echo "✗ Docker not running on Host B"
fi

# Check network
if ssh root@192.168.16.7 "docker network ls | grep homelab_network" &>/dev/null; then
  echo "✓ homelab_network exists on Host A"
else
  echo "✗ homelab_network missing on Host A"
fi

if ssh root@192.168.17.1 "docker network ls | grep homelab_network" &>/dev/null; then
  echo "✓ homelab_network exists on Host B"
else
  echo "✗ homelab_network missing on Host B"
fi

echo ""
echo "=== Validation Complete ==="
```

Save as `validate-pre-deployment.sh` and run:
```bash
chmod +x validate-pre-deployment.sh
./validate-pre-deployment.sh
```

---

## 🚀 DEPLOYMENT SEQUENCE

Once all checks pass, follow this sequence:

### Phase 1: Host B - Database Layer (15 min)
```bash
ssh root@192.168.17.1
cd /opt/homelab
docker compose -f core-hostB.yml up -d
docker compose -f core-hostB.yml logs -f
```

**Verify:**
```bash
docker exec postgresql pg_isready
docker exec redis redis-cli ping
```

### Phase 2: Host A - Core Services (20 min)
```bash
ssh root@192.168.16.7
cd /opt/homelab
docker compose -f core-hostA.yml up -d
docker compose -f core-hostA.yml logs -f
```

**Verify:**
```bash
curl -f http://localhost:8080  # Traefik Dashboard
```

### Phase 3: Application Stacks (30-60 min)

Deploy in order:
1. Monitoring (for observability)
2. Home Assistant (if using smart home)
3. Media Stack
4. Automation (Pi-hole, n8n, Ollama)

---

## 📝 POST-DEPLOYMENT TASKS

After successful deployment:

- [ ] Configure Authentik SSO
- [ ] Import Grafana dashboards
- [ ] Set up Prometheus scrape targets
- [ ] Configure Home Assistant integrations
- [ ] Test Traefik routing
- [ ] Enable SSL/HTTPS (Traefik ACME)
- [ ] Set up automated backups
- [ ] Configure Uptime Kuma monitoring
- [ ] Test failover scenarios

---

**Last Updated:** 2025-12-23
**Status:** Ready for Deployment

**Estimated Total Time:** 2-3 hours (first deployment)

---

## 🆘 EMERGENCY ROLLBACK

If deployment fails:

```bash
# Stop all services
docker compose down

# Remove failed containers
docker rm -f $(docker ps -aq)

# Restore backups (if any)
# Review logs
docker compose logs

# Try again or ask for help
```

**Support Resources:**

- GitHub Issues: [Create Issue]
- Documentation: See `docs/` directory
- Troubleshooting: `docs/08-Troubleshooting.md`

---

**Good luck with your deployment! 🚀**
