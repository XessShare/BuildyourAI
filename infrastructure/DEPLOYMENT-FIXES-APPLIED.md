# Deployment Fixes Applied - Homelab OSS Stack
**Date:** 2025-12-23
**Status:** READY FOR PRE-DEPLOYMENT TESTING

---

## ✅ FIXES COMPLETED

### 1. Missing Configuration Files Created

All missing configuration files have been created:

```
✓ docker/mosquitto/mosquitto.conf
✓ docker/mosquitto/README.md (setup instructions)
✓ docker/prometheus/prometheus.yml
✓ docker/prometheus/alerts/basic-alerts.yml
✓ docker/loki/loki-config.yml
✓ docker/promtail/promtail-config.yml
✓ docker/grafana/provisioning/datasources/datasources.yml
✓ docker/grafana/provisioning/dashboards/dashboards.yml
✓ docker/traefik/dynamic/authentik.yml
✓ docker/traefik/dynamic/vps-backend.yml
✓ docker/traefik/acme.json (created with chmod 600)
```

### 2. Git Security Issues Fixed

```
✓ Added .env.production to .gitignore
✓ Created Mosquitto password setup instructions
```

**IMPORTANT:** Before pushing to Git:
```bash
# Remove .env.production from Git history (if already committed)
git rm --cached .env.production
git commit -m "Security: Remove .env.production from version control"
```

### 3. Port Conflict Resolved

```
✓ Changed Ollama WebUI port from 8080 to 8081
  - File: docker/stacks/automation.yml:101
  - Traefik Dashboard: Port 8080 ✓
  - Ollama WebUI: Port 8081 ✓
```

### 4. PostgreSQL/Redis Multi-Host Configuration

Created new file for multi-host deployment:

```
✓ docker/stacks/core-hostA.yml
  - Traefik, Authentik, Portainer
  - Connects to PostgreSQL/Redis on Host B (192.168.17.1)
  - Uses ${HOMELAB_IP_B} variable
```

**Deployment Options:**
- **Single-Host:** Use `core.yml` (includes PostgreSQL/Redis locally)
- **Multi-Host:** Use `core-hostB.yml` on Host B + `core-hostA.yml` on Host A

### 5. Hardcoded Password Fixed

```
✓ docker/stacks/scripts/init-databases.sh:15
  - Changed from 'changeme-strong-password'
  - Now uses ${AUTHENTIK_POSTGRESQL_PASSWORD}
```

---

## 📋 PRE-DEPLOYMENT CHECKLIST

### CRITICAL - Must do BEFORE deployment

- [ ] **Create Docker Network** on BOTH hosts:
  ```bash
  # Host A (192.168.16.7)
  ssh root@192.168.16.7 "docker network create homelab_network"

  # Host B (192.168.17.1)
  ssh root@192.168.17.1 "docker network create homelab_network"
  ```

- [ ] **Create Mosquitto Password File:**
  ```bash
  docker run --rm -it -v ./docker/mosquitto:/mosquitto/config \
    eclipse-mosquitto mosquitto_passwd -c /mosquitto/config/passwd mqtt
  ```

- [ ] **Verify .env File** has all required variables:
  ```bash
  # Compare with .env.example
  diff .env .env.example

  # Ensure HOMELAB_IP_B is set to 192.168.17.1
  grep HOMELAB_IP_B .env
  ```

- [ ] **Set HOMELAB_IP_B in .env:**
  ```bash
  echo "HOMELAB_IP_B=192.168.17.1" >> .env
  ```

- [ ] **Firewall Rules** - Allow inter-host communication:
  ```bash
  # Host A
  ssh root@192.168.16.7 "ufw allow from 192.168.17.0/24"

  # Host B
  ssh root@192.168.17.1 "ufw allow from 192.168.16.0/24"
  ```

### DEPLOYMENT SEQUENCE (Multi-Host)

**Phase 1: Host B - Database Layer**
```bash
# 1. Deploy PostgreSQL + Redis + Node Exporter
ssh root@192.168.17.1
cd /opt/homelab
docker compose -f core-hostB.yml up -d

# 2. Verify services are running
docker compose -f core-hostB.yml ps
docker exec postgresql pg_isready
docker exec redis redis-cli ping
```

**Phase 2: Host A - Core Services**
```bash
# 1. Deploy Traefik + Authentik + Portainer
ssh root@192.168.16.7
cd /opt/homelab
docker compose -f core-hostA.yml up -d

# 2. Verify Traefik and Authentik start
docker compose -f core-hostA.yml logs -f
```

**Phase 3: Test Connectivity**
```bash
# From Host A, test connection to Host B services
docker exec authentik-server nc -zv 192.168.17.1 5432  # PostgreSQL
docker exec authentik-server nc -zv 192.168.17.1 6379  # Redis
```

---

## 🎯 NEXT STEPS

After successful deployment of core services:

1. **Configure Authentik SSO**
   - Initial setup wizard
   - Create admin user
   - Configure 2FA

2. **Deploy Application Stacks**
   - homeassistant.yml (Host A)
   - media.yml (Host B)
   - monitoring.yml (Host A)
   - automation.yml (both hosts)

3. **Set up Monitoring**
   - Import Grafana dashboards
   - Configure Prometheus targets
   - Test alerting

4. **Security Hardening**
   - Enable Traefik SSL/ACME
   - Activate Authentik 2FA
   - Configure Fail2Ban
   - Set up Tailscale VPN

---

## 🔧 TROUBLESHOOTING

### Issue: Network not found
```bash
Error: network homelab_network not found
```

**Solution:**
```bash
docker network create homelab_network
```

### Issue: Authentik can't connect to PostgreSQL
```bash
Error: could not connect to server: Connection refused
```

**Solution:**
```bash
# Verify PostgreSQL is running on Host B
ssh root@192.168.17.1 "docker exec postgresql pg_isready"

# Verify network connectivity from Host A
ping 192.168.17.1

# Check firewall rules
ssh root@192.168.17.1 "ufw status | grep 192.168.16"
```

### Issue: Port already in use
```bash
Error: bind: address already in use
```

**Solution:**
```bash
# Find process using port
sudo lsof -i :PORT

# Or stop conflicting service
sudo systemctl stop service-name
```

---

## 📊 SERVICE ACCESS URLs

After successful deployment:

### Host A Services (192.168.16.7)
- **Traefik Dashboard:** http://192.168.16.7:8080
- **Authentik:** http://192.168.16.7:9000
- **Portainer:** http://192.168.16.7:9001 (if deployed)

### Host B Services (192.168.17.1)
- **PostgreSQL:** 192.168.17.1:5432
- **Redis:** 192.168.17.1:6379
- **Ollama WebUI:** http://192.168.17.1:8081

---

**Deployment Status:** ✅ FIXES APPLIED - READY FOR TESTING

**Estimated Deployment Time:** 2-3 hours (multi-host setup)

---

## 🔄 GIT STATUS

Before deploying, commit these fixes:

```bash
cd /run/media/fitna/FCA86951A8690C08/Users/Xess/.claude-worktrees/homelab-oss-stack/brave-snyder

# Stage all changes
git add .

# Commit (if Git repo is initialized)
git commit -m "Fix: Apply pre-deployment fixes

- Add missing configuration files (Mosquitto, Prometheus, Loki, Grafana, Traefik)
- Fix security issue: Add .env.production to .gitignore
- Resolve port conflict: Ollama WebUI 8080 → 8081
- Create multi-host setup: core-hostA.yml for PostgreSQL/Redis on Host B
- Fix hardcoded password in init-databases.sh
- Add deployment instructions and checklists

Ready for deployment testing."
```

---

**End of Deployment Fixes Report**
