# Deployment Guide - Homelab OSS Stack

Complete step-by-step deployment instructions for the entire homelab infrastructure.

---

## 📋 Prerequisites Checklist

Before starting, ensure you have:

- [ ] Proxmox VE 8+ installed on both hosts (or Debian 12+/Ubuntu 22.04+)
- [ ] Static IP addresses configured (192.168.16.7, 192.168.17.1)
- [ ] SSH access to both hosts (passwordless preferred)
- [ ] Domain name registered (for Cloudflare SSL)
- [ ] Cloudflare account with API token
- [ ] 200+ GB free storage on deployment host
- [ ] Control machine with Ansible 2.15+, Git, Docker installed

---

## 🚀 Phase 1: Infrastructure Bootstrap (Week 1)

### Step 1.1: Clone Repository

```bash
git clone https://github.com/YOUR-USERNAME/homelab-oss-stack.git
cd homelab-oss-stack
```

### Step 1.2: Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit with your settings
nano .env
```

**Critical variables to set:**
- `DOMAIN` - Your domain name
- `CLOUDFLARE_EMAIL` and `CLOUDFLARE_API_KEY`
- All `*_PASSWORD` variables (use strong, unique passwords)
- `AUTHENTIK_SECRET_KEY` (generate with `openssl rand -hex 50`)
- `VPN_*` variables for qBittorrent VPN

### Step 1.3: Configure Ansible Inventory

```bash
# Edit inventory with your IPs
nano ansible/inventory/hosts.yml

# Test connectivity
ansible all -i ansible/inventory/hosts.yml -m ping
```

### Step 1.4: Bootstrap Proxmox Hosts

```bash
# Run bootstrap playbook
ansible-playbook -i ansible/inventory/hosts.yml ansible/playbooks/00-bootstrap.yml

# Verify success
ansible all -i ansible/inventory/hosts.yml -m shell -a "ufw status"
```

**What this does:**
- Updates all packages
- Configures firewall (UFW)
- Sets timezone
- Creates swap file
- Hardens SSH
- Installs basic utilities

---

## 🐳 Phase 2: Docker Setup (Week 1-2)

### Step 2.1: Install Docker on Hosts

```bash
ansible-playbook -i ansible/inventory/hosts.yml ansible/playbooks/01-docker-setup.yml
```

### Step 2.2: Create Docker Networks

```bash
# SSH into primary host
ssh root@192.168.16.7

# Create shared network
docker network create homelab_network
```

### Step 2.3: Prepare Directory Structure

```bash
# On deployment host (pve-thinkpad)
mkdir -p /mnt/media/{tv,movies,downloads}
mkdir -p /opt/homelab/{traefik,mosquitto,prometheus,grafana}
```

---

## 🔐 Phase 3: Core Services (Week 2)

### Step 3.1: Deploy Traefik Configuration

```bash
# Create Traefik static config
cat > docker/traefik/traefik.yml <<EOF
api:
  dashboard: true
  insecure: false

entryPoints:
  web:
    address: ":80"
    http:
      redirections:
        entryPoint:
          to: websecure
          scheme: https
  websecure:
    address: ":443"

providers:
  docker:
    endpoint: "unix:///var/run/docker.sock"
    exposedByDefault: false
    network: homelab_network
  file:
    directory: /config
    watch: true

certificatesResolvers:
  cloudflare:
    acme:
      email: ${TRAEFIK_ACME_EMAIL}
      storage: /acme.json
      dnsChallenge:
        provider: cloudflare
        resolvers:
          - "1.1.1.1:53"
          - "1.0.0.1:53"

log:
  level: INFO
  filePath: /var/log/traefik/traefik.log

accessLog:
  filePath: /var/log/traefik/access.log
EOF

# Create acme.json
touch docker/traefik/acme.json
chmod 600 docker/traefik/acme.json
```

### Step 3.2: Deploy Core Stack

```bash
cd docker/stacks

# Start core services (Traefik + Authentik + Portainer)
docker compose -f core.yml up -d

# Check logs
docker compose -f core.yml logs -f
```

**Verify:**
- Traefik dashboard: https://traefik.yourdomain.com
- Authentik: https://auth.yourdomain.com (initial setup wizard)
- Portainer: https://portainer.yourdomain.com

### Step 3.3: Configure Authentik

1. Access https://auth.yourdomain.com
2. Complete initial setup wizard (create admin account)
3. Create application for each service:
   - Grafana (OIDC)
   - Nextcloud (OIDC)
   - Jellyfin (LDAP - optional)
4. Create user groups (admin, family, guests)
5. Enable 2FA (TOTP/WebAuthn)

### Step 3.4: Create Traefik Middleware

```bash
# Create dynamic config for Authentik middleware
cat > docker/traefik/dynamic/authentik.yml <<EOF
http:
  middlewares:
    authentik:
      forwardAuth:
        address: http://authentik-server:9000/outpost.goauthentik.io/auth/traefik
        trustForwardHeader: true
        authResponseHeaders:
          - X-authentik-username
          - X-authentik-groups
          - X-authentik-email
EOF
```

---

## 🏠 Phase 4: Home Assistant Stack (Week 2-3)

### Step 4.1: Configure Mosquitto

```bash
# Create Mosquitto config
cat > docker/mosquitto/mosquitto.conf <<EOF
listener 1883
allow_anonymous false
password_file /mosquitto/config/passwd

listener 9001
protocol websockets
EOF

# Create password file
docker run --rm -it eclipse-mosquitto mosquitto_passwd -c passwd mqtt
cp passwd docker/mosquitto/
```

### Step 4.2: Deploy Home Assistant Stack

```bash
cd docker/stacks

# Start Home Assistant + MQTT + Zigbee2MQTT + Node-RED
docker compose -f homeassistant.yml up -d

# Check logs
docker compose -f homeassistant.yml logs -f homeassistant
```

**Verify:**
- Home Assistant: https://ha.yourdomain.com
- Zigbee2MQTT: https://zigbee.yourdomain.com
- Node-RED: https://nodered.yourdomain.com

### Step 4.3: Configure Home Assistant

1. Complete onboarding wizard
2. Add MQTT integration (point to mosquitto container)
3. Add Zigbee2MQTT integration (auto-discovered)
4. Configure zones (home, work)
5. Create first automation

---

## 📺 Phase 5: Media Stack (Week 3-4)

### Step 5.1: Configure VPN for qBittorrent

Ensure `.env` has correct VPN settings:
```bash
VPN_SERVICE_PROVIDER=mullvad  # or nordvpn, expressvpn
VPN_TYPE=wireguard
WIREGUARD_PRIVATE_KEY=your_private_key
```

### Step 5.2: Deploy Media Stack

```bash
cd docker/stacks

# Start Jellyfin + *arr + qBittorrent
docker compose -f media.yml up -d

# Verify VPN is working
docker exec qbittorrent curl ifconfig.me
# Should show VPN IP, not your home IP
```

### Step 5.3: Configure *arr Apps

**Prowlarr (Indexer Manager):**
1. Access https://prowlarr.yourdomain.com
2. Add indexers (private trackers, Usenet)
3. Add apps (Sonarr, Radarr)
4. Test indexer searches

**Sonarr (TV Shows):**
1. Access https://sonarr.yourdomain.com
2. Settings → Download Clients → Add qBittorrent
3. Settings → Indexers → Sync from Prowlarr
4. Add TV shows to monitor

**Radarr (Movies):**
1. Access https://radarr.yourdomain.com
2. Same configuration as Sonarr
3. Add movies to monitor

**Jellyfin:**
1. Access https://jellyfin.yourdomain.com
2. Complete setup wizard
3. Add libraries (/data/tv, /data/movies)
4. Configure hardware transcoding (Intel QSV)

---

## 📊 Phase 6: Monitoring Stack (Week 4)

### Step 6.1: Configure Prometheus

```bash
# Create Prometheus config
cat > docker/prometheus/prometheus.yml <<EOF
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'node-exporter'
    static_configs:
      - targets: ['node-exporter:9100']

  - job_name: 'cadvisor'
    static_configs:
      - targets: ['cadvisor:8080']

  - job_name: 'traefik'
    static_configs:
      - targets: ['traefik:8080']
EOF
```

### Step 6.2: Deploy Monitoring Stack

```bash
cd docker/stacks

# Start Prometheus + Grafana + Loki + Uptime Kuma
docker compose -f monitoring.yml up -d
```

### Step 6.3: Configure Grafana

1. Access https://grafana.yourdomain.com
2. Login (admin / password from .env)
3. Add data sources:
   - Prometheus (http://prometheus:9090)
   - Loki (http://loki:3100)
4. Import dashboards:
   - Node Exporter Full (ID: 1860)
   - Docker Monitoring (ID: 893)
   - Traefik 2 (ID: 11462)

### Step 6.4: Configure Uptime Kuma

1. Access https://status.yourdomain.com
2. Create monitoring checks for all services
3. Create status page (public or private)
4. Configure notifications (Discord, Telegram, email)

---

## 💾 Phase 7: Backup & Recovery (Week 5)

### Step 7.1: Configure Restic

```bash
# Initialize Restic repository
docker run --rm -it \
  -v /var/lib/docker/volumes:/data \
  -e RESTIC_REPOSITORY=${RESTIC_REPOSITORY} \
  -e RESTIC_PASSWORD=${RESTIC_PASSWORD} \
  -e AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} \
  -e AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} \
  restic/restic init
```

### Step 7.2: Create Backup Script

```bash
cat > /opt/homelab/scripts/backup.sh <<'EOF'
#!/bin/bash
set -e

BACKUP_NAME="homelab-$(date +%Y%m%d-%H%M%S)"

# Backup Docker volumes
docker run --rm \
  -v /var/lib/docker/volumes:/data:ro \
  -e RESTIC_REPOSITORY=${RESTIC_REPOSITORY} \
  -e RESTIC_PASSWORD=${RESTIC_PASSWORD} \
  -e AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} \
  -e AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} \
  restic/restic backup /data \
    --tag daily \
    --host $(hostname)

# Prune old backups (keep 7 daily, 4 weekly, 12 monthly)
restic forget --prune \
  --keep-daily 7 \
  --keep-weekly 4 \
  --keep-monthly 12
EOF

chmod +x /opt/homelab/scripts/backup.sh
```

### Step 7.3: Schedule Backups

```bash
# Add to crontab
crontab -e

# Add line (daily at 2 AM):
0 2 * * * /opt/homelab/scripts/backup.sh >> /var/log/homelab-backup.log 2>&1
```

### Step 7.4: Test Restore

```bash
# List snapshots
restic snapshots

# Restore specific snapshot
restic restore SNAPSHOT_ID --target /tmp/restore-test

# Verify files
ls -la /tmp/restore-test
```

---

## 🔒 Phase 8: Security Hardening (Week 5)

### Step 8.1: Enable Fail2Ban

```bash
ansible-playbook -i ansible/inventory/hosts.yml ansible/playbooks/security-hardening.yml
```

### Step 8.2: Configure Tailscale VPN

```bash
# Install on both hosts
curl -fsSL https://tailscale.com/install.sh | sh

# Authenticate
tailscale up

# Verify mesh network
tailscale status
```

### Step 8.3: Security Audit Checklist

- [ ] All services behind Authentik SSO
- [ ] 2FA enabled for admin accounts
- [ ] UFW firewall active on all hosts
- [ ] Fail2Ban monitoring SSH
- [ ] Backups tested and verified
- [ ] SSL certificates valid (Let's Encrypt)
- [ ] Docker containers non-root where possible
- [ ] Secrets not in version control (.env in .gitignore)

---

## 📈 Phase 9: Optimization & Tuning

### Monitoring Alert Rules

Create alert rules in Prometheus for:
- High CPU usage (>80% for 5 min)
- High memory usage (>90%)
- Disk space low (<10%)
- Container restarts (>3 in 1 hour)
- SSL certificate expiry (<14 days)

### Performance Tuning

**Docker:**
```bash
# Limit log sizes
echo '{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  }
}' > /etc/docker/daemon.json

systemctl restart docker
```

**Jellyfin transcoding:**
- Enable Intel QSV (pass /dev/dri to container)
- Limit simultaneous transcodes
- Pre-transcode 4K → 1080p for bandwidth

---

## 🎓 Phase 10: Documentation & Handover

### Create Runbook

Document in `docs/`:
- Network topology diagram
- Service dependency map
- Common troubleshooting steps
- Restore procedures
- Contact information

### Training

For family members/team:
- How to request media (Overseerr)
- How to access services (Tailscale VPN)
- Basic troubleshooting (restarting containers)
- Who to contact for issues

---

## 🚨 Troubleshooting Common Issues

### Container won't start

```bash
# Check logs
docker logs <container_name>

# Restart container
docker restart <container_name>

# Rebuild and restart
docker compose down && docker compose up -d --force-recreate
```

### Traefik not routing

```bash
# Check Traefik logs
docker logs traefik

# Verify container labels
docker inspect <container_name> | grep traefik

# Check Traefik dashboard for errors
https://traefik.yourdomain.com
```

### Authentik SSO failing

```bash
# Check Authentik logs
docker logs authentik-server

# Verify OIDC configuration
# Authentik Admin → Applications → Check client ID/secret

# Test ForwardAuth endpoint
curl -v http://authentik-server:9000/outpost.goauthentik.io/auth/traefik
```

### VPN not working in qBittorrent

```bash
# Check Gluetun logs
docker logs gluetun

# Test IP from inside container
docker exec gluetun curl ifconfig.me

# Restart VPN container
docker restart gluetun
```

---

## 📞 Support & Resources

- **GitHub Issues**: Report bugs, request features
- **Documentation**: `/docs` folder
- **Community**: r/selfhosted, Home Assistant forums
- **Logs**: `/var/log/homelab-*.log`

---

**Deployment complete!** 🎉

Your homelab is now production-ready with:
- Automated infrastructure (Ansible)
- Reverse proxy with SSL (Traefik + Let's Encrypt)
- SSO + 2FA (Authentik)
- Smart home hub (Home Assistant)
- Media server (*arr + Jellyfin)
- Comprehensive monitoring (Prometheus + Grafana)
- Encrypted backups (Restic)

**Next steps**: Iterate, optimize, and enjoy your self-hosted stack!
