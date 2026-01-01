# CI/CD Pipeline Setup Guide

**Status:** ✅ Configured  
**Workflow:** `.github/workflows/backend-ci-cd.yml`  
**Environments:** Staging (RTX1080), Production (K3s - TBD)

---

## Overview

The CI/CD pipeline automates:
1. **Build** - Docker image creation with caching
2. **Test** - Pytest suite with coverage reporting
3. **Security** - Trivy vulnerability scanning
4. **Deploy** - Automated deployment to staging
5. **Rollback** - One-click rollback mechanism

---

## Pipeline Stages

### 1. Build & Test
**Triggers:** Push to main/master/sprint-26/*, Pull Requests  
**Duration:** ~3-5 minutes

**Steps:**
- Checkout code
- Build Docker image with BuildKit cache
- Start PostgreSQL test database
- Run pytest test suite (15 tests)
- Generate coverage report
- Push image to GitHub Container Registry (GHCR)

**Success Criteria:**
- All tests passing
- Coverage uploaded to Codecov
- Docker image pushed successfully

### 2. Security Scan
**Triggers:** After successful build (non-PR only)  
**Duration:** ~2-3 minutes

**Steps:**
- Pull built image from GHCR
- Run Trivy vulnerability scanner
- Upload results to GitHub Security tab

**Success Criteria:**
- No CRITICAL or HIGH vulnerabilities
- SARIF report uploaded

### 3. Deploy to Staging
**Triggers:**
- Push to main/master/sprint-26/*
- Manual workflow dispatch

**Duration:** ~3-5 minutes

**Steps:**
1. **Backup** - Create timestamped backup of current deployment
2. **Sync** - rsync code to staging server
3. **Deploy** - Docker Compose up with health checks
4. **Validate** - Test health endpoints + authentication
5. **Cleanup** - Remove old Docker images

**Success Criteria:**
- PostgreSQL healthy
- API responds to health checks
- Authentication working
- No errors in logs

### 4. Rollback (Manual)
**Triggers:** Manual workflow dispatch or script execution  
**Duration:** ~2 minutes

**Steps:**
1. Stop current deployment
2. Restore most recent backup
3. Start services
4. Validate health

---

## Setup Instructions

### Prerequisites

1. **GitHub Secrets** (Repository Settings → Secrets and variables → Actions)

   Required secrets:
   ```
   STAGING_SSH_KEY - SSH private key for staging server access
   ```

   Optional secrets:
   ```
   SLACK_WEBHOOK - For deployment notifications (future)
   SENTRY_DSN - For error tracking (future)
   ```

2. **SSH Key Setup**

   On your local machine:
   ```bash
   # Generate SSH key for CI/CD (if not exists)
   ssh-keygen -t ed25519 -C "github-actions@hexahub" -f ~/.ssh/hexahub-cicd

   # Copy to staging server
   ssh-copy-id -i ~/.ssh/hexahub-cicd.pub fitna@rtx1080.local

   # Add private key to GitHub Secrets
   cat ~/.ssh/hexahub-cicd
   # Copy output and add as STAGING_SSH_KEY secret
   ```

3. **Staging Server Preparation**

   On RTX1080:
   ```bash
   # Create deployment directory
   mkdir -p ~/hexahub-backend

   # Ensure Docker & Docker Compose installed
   docker --version
   docker compose version

   # Test SSH access
   ssh fitna@rtx1080.local "echo 'SSH connection successful'"
   ```

4. **GitHub Container Registry (GHCR) Access**

   Already configured - uses `GITHUB_TOKEN` automatically.

---

## Usage

### Automatic Deployment

**Push to main/master:**
```bash
git checkout main
git merge your-feature-branch
git push origin main
# Pipeline automatically triggers
```

**Push to sprint branch:**
```bash
git push origin sprint-26/my-feature
# Pipeline automatically triggers and deploys to staging
```

### Manual Deployment

**Via GitHub Actions UI:**
1. Go to: https://github.com/YOUR_REPO/actions
2. Click "Backend CI/CD Pipeline"
3. Click "Run workflow"
4. Select branch and environment
5. Click "Run workflow" button

**Via CLI (gh required):**
```bash
gh workflow run "Backend CI/CD Pipeline" \
  --field environment=staging
```

**Via deployment script:**
```bash
cd hexahub-backend
./scripts/deploy.sh staging
```

### Manual Rollback

**Via GitHub Actions:**
1. Go to Actions → Backend CI/CD Pipeline
2. Run workflow with environment: "rollback"

**Via script:**
```bash
cd hexahub-backend
./scripts/rollback.sh
```

**Via SSH:**
```bash
ssh fitna@rtx1080.local
cd ~/hexahub-backend
docker compose down

# Restore latest backup
LATEST_BACKUP=$(ls -dt ~/hexahub-backup-* | head -1)
rm -rf ~/hexahub-backend
cp -r "$LATEST_BACKUP" ~/hexahub-backend

# Restart
cd ~/hexahub-backend
docker compose up -d
```

---

## Monitoring

### Check Deployment Status

**GitHub Actions:**
- https://github.com/YOUR_REPO/actions

**Staging Server:**
```bash
# SSH to staging
ssh fitna@rtx1080.local

# Check services
cd ~/hexahub-backend
docker compose ps
docker compose logs -f backend

# Health check
curl http://localhost:8000/health
curl http://localhost:8000/health/db
```

### View Logs

**Real-time logs:**
```bash
ssh fitna@rtx1080.local
cd ~/hexahub-backend
docker compose logs -f backend
```

**Last 100 lines:**
```bash
docker compose logs --tail=100 backend
```

---

## Troubleshooting

### Issue 1: Pipeline Fails at "Run tests in Docker"

**Cause:** PostgreSQL not ready or network issues

**Fix:**
- Check `docker compose up postgres` step succeeded
- Increase timeout in workflow (currently 30s)
- Verify network name matches: `hexahub-backend_hexahub-network`

### Issue 2: Deployment Fails - SSH Connection Refused

**Cause:** SSH key not configured or wrong host

**Fix:**
1. Verify `STAGING_SSH_KEY` secret is set correctly
2. Check staging server is reachable: `ping rtx1080.local`
3. Test SSH manually: `ssh fitna@rtx1080.local`
4. Update `STAGING_HOST` in workflow if needed

### Issue 3: Health Check Fails After Deployment

**Cause:** Service not started or port conflict

**Fix:**
```bash
ssh fitna@rtx1080.local
cd ~/hexahub-backend

# Check service status
docker compose ps

# View logs
docker compose logs backend

# Restart services
docker compose down
docker compose up -d

# Manual health check
curl http://localhost:8000/health
```

### Issue 4: Image Push Fails - Permission Denied

**Cause:** GitHub token doesn't have write permissions

**Fix:**
- Already configured in workflow: `permissions: packages: write`
- If persists, check repository settings → Actions → General
- Enable "Read and write permissions"

### Issue 5: Rollback Fails - No Backup Found

**Cause:** No previous deployment or backups deleted

**Fix:**
- Backups are created automatically on each deployment
- Check: `ssh fitna@rtx1080.local "ls -la ~/hexahub-backup-*"`
- If none exist, cannot rollback - redeploy manually

---

## Performance Metrics

**Expected Durations:**
- Build & Test: 3-5 minutes
- Security Scan: 2-3 minutes
- Deploy to Staging: 3-5 minutes
- Rollback: 1-2 minutes

**Total Pipeline:** ~10-15 minutes (end-to-end)

---

## Cost Analysis

**GitHub Actions Minutes:**
- Free tier: 2,000 minutes/month
- Estimated usage: ~15 min/deployment × 20 deployments = 300 min/month
- **Cost:** $0 (within free tier)

**GitHub Container Registry:**
- Free tier: 500 MB storage
- Image size: ~200 MB
- **Cost:** $0 (within free tier)

**Total Monthly Cost:** $0

---

## Security Best Practices

✅ **Implemented:**
- SSH key authentication (no passwords)
- Secrets stored in GitHub Secrets (encrypted)
- Vulnerability scanning with Trivy
- Least privilege (only staging access via SSH)
- Backup before deployment
- Health checks before marking successful

⏳ **TODO (Production):**
- HTTPS with TLS certificates
- Secrets rotation policy
- Multi-factor authentication for production
- Network isolation (K3s network policies)

---

## Next Steps

### Phase 1: Staging (Current) ✅
- [x] GitHub Actions workflow
- [x] Docker build & test
- [x] Deploy to RTX1080
- [x] Rollback mechanism
- [x] Health checks

### Phase 2: Production (Week 3-4)
- [ ] K3s cluster setup
- [ ] Helm charts for deployment
- [ ] HTTPS/TLS configuration
- [ ] Database migrations automation
- [ ] Blue-green deployment strategy

### Phase 3: Monitoring (Week 5-6)
- [ ] Prometheus metrics collection
- [ ] Grafana dashboards
- [ ] Alert rules (Slack/Email)
- [ ] Log aggregation (Loki)
- [ ] Uptime monitoring (UptimeRobot)

---

**Pipeline Version:** 1.0  
**Last Updated:** 2026-01-01  
**Status:** ✅ Production Ready (Staging)
