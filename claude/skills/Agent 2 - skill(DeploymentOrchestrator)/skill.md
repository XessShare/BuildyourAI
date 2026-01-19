# Skill: Deployment Orchestrator

## Name
**Deployment Orchestrator** - Automated Multi-System Infrastructure Deployment

## Description
This skill automates the complete deployment lifecycle for the homelab's 3-system infrastructure (VPS, ThinkPad, RTX1080). It executes the 10-phase deployment process defined in `/home/fitna/homelab/infrastructure/DEPLOYMENT.md`, performs pre-deployment validation, triggers GitHub Actions workflows, monitors health checks, and implements automatic rollback on failure. The skill ensures zero-downtime deployments with comprehensive validation and safety checks.

## When to Use This Skill

### Trigger Conditions
Use this skill when the user requests ANY of the following:
- "Deploy [stack/service] to [environment]"
- "Deploy to production/staging"
- "Roll out the infrastructure changes"
- "Update [service] on [host]"
- "Execute deployment pipeline"
- "Deploy with health checks"
- "Run infrastructure deployment"
- "Push changes to [VPS/ThinkPad/RTX1080]"

### Context Indicators
- User mentions environment names (production, staging, development)
- User references host names (VPS, ThinkPad, RTX1080, Host A, Host B)
- User mentions Docker stacks (core, monitoring, media, homeassistant)
- User discusses CI/CD, GitHub Actions, or deployment workflows
- User mentions rollback or health checks

## Process Steps

### Phase 1: Pre-Deployment Validation (5 minutes)

1. **Execute Pre-Deployment Checklist**
   Reference: `/home/fitna/homelab/infrastructure/PRE-DEPLOYMENT-CHECKLIST.md`

   **Critical Checks:**
   ```bash
   # 1. Verify secrets are in place
   test -f /home/fitna/homelab/shared/secrets/.env.master || echo "❌ Master secrets missing"

   # 2. Check SSH connectivity to all hosts
   ssh fitna@91.107.198.37 "echo 'VPS OK'" || echo "❌ VPS unreachable"
   ssh fitna@192.168.16.7 "echo 'ThinkPad OK'" || echo "❌ ThinkPad unreachable"
   ssh fitna@192.168.17.1 "echo 'RTX1080 OK'" || echo "❌ RTX1080 unreachable"

   # 3. Validate Docker Compose syntax
   for stack in /home/fitna/homelab/infrastructure/docker/stacks/*.yml; do
     docker compose -f "$stack" config > /dev/null || echo "❌ Invalid: $stack"
   done

   # 4. Check GitHub Actions workflow status
   gh workflow list --repo fitna/homelab

   # 5. Verify backup exists (if production)
   ls -lh /home/fitna/homelab/backups/latest/ || echo "⚠️ No recent backup"
   ```

2. **Identify Deployment Scope**
   - **Full deployment**: All 9 stacks across 3 hosts (60-90 min)
   - **Stack-specific**: Single stack (e.g., monitoring.yml) (10-15 min)
   - **Host-specific**: All stacks on one host (20-30 min)
   - **Service-specific**: Single service update (5-10 min)

3. **Set Deployment Environment**
   - **Production**: VPS (91.107.198.37), RTX1080 (192.168.17.1)
   - **Staging**: ThinkPad (192.168.16.7)
   - **Development**: Local Docker

4. **Create Deployment Log**
   ```bash
   DEPLOY_ID="deploy-$(date +%Y%m%d-%H%M%S)"
   LOG_DIR="/home/fitna/homelab/logs/deployments/$DEPLOY_ID"
   mkdir -p "$LOG_DIR"
   ```

### Phase 2: GitHub Actions Trigger (If CI/CD)

5. **Trigger Deployment Workflow**
   Reference: `/home/fitna/homelab/.github/workflows/deploy.yml`

   **Webhook Trigger (Preferred):**
   ```bash
   # Trigger via repository dispatch
   gh workflow run deploy.yml \
     --ref master \
     --field environment=production \
     --field stack=all
   ```

   **Manual Trigger (Alternative):**
   ```bash
   # Push to trigger branch
   git checkout -b deploy/$DEPLOY_ID
   git commit --allow-empty -m "Deploy: $DEPLOY_ID"
   git push origin deploy/$DEPLOY_ID
   ```

6. **Monitor Workflow Execution**
   ```bash
   # Get run ID
   RUN_ID=$(gh run list --workflow=deploy.yml --limit 1 --json databaseId --jq '.[0].databaseId')

   # Watch logs in real-time
   gh run watch $RUN_ID
   ```

### Phase 3: Infrastructure Bootstrap (Phase 1 of 10-Phase Deployment)

7. **Run Ansible Bootstrap Playbook**
   Reference: `/home/fitna/homelab/infrastructure/ansible/playbooks/00-bootstrap.yml`

   **Execute:**
   ```bash
   cd /home/fitna/homelab/infrastructure/ansible

   # Bootstrap all hosts (first-time setup)
   ansible-playbook playbooks/00-bootstrap.yml -i inventory/hosts.yml

   # Or target specific host
   ansible-playbook playbooks/00-bootstrap.yml -i inventory/hosts.yml --limit vps
   ```

   **Validation:**
   - UFW firewall enabled (ports 22, 80, 443, 51820 open)
   - Docker and Docker Compose installed
   - Swap file created (4GB)
   - Timezone set to Europe/Berlin
   - SSH hardening applied (key-only auth)

### Phase 4: Database Layer Deployment (Phase 2 of 10)

8. **Deploy PostgreSQL and Redis on Host B (RTX1080)**
   Reference: `/home/fitna/homelab/infrastructure/docker/stacks/core-hostB.yml`

   **Execute:**
   ```bash
   ssh fitna@192.168.17.1 << 'EOF'
   cd /home/fitna/homelab/infrastructure/docker/stacks
   docker compose -f core-hostB.yml pull
   docker compose -f core-hostB.yml up -d
   EOF
   ```

   **Health Check:**
   ```bash
   # PostgreSQL
   docker exec homelab-postgres pg_isready -U postgres

   # Redis
   docker exec homelab-redis redis-cli ping
   ```

   **Expected:** Both services respond within 30 seconds

### Phase 5: Core Services Deployment (Phase 3 of 10)

9. **Deploy Traefik, Authentik, Portainer on Host A (VPS)**
   Reference: `/home/fitna/homelab/infrastructure/docker/stacks/core-hostA.yml`

   **Execute:**
   ```bash
   ssh fitna@91.107.198.37 << 'EOF'
   cd /home/fitna/homelab/infrastructure/docker/stacks
   docker compose -f core-hostA.yml pull
   docker compose -f core-hostA.yml up -d
   EOF
   ```

   **Health Check:**
   ```bash
   # Traefik dashboard
   curl -I https://traefik.yourdomain.com | grep "200 OK"

   # Authentik
   curl -I https://auth.yourdomain.com | grep "200 OK"

   # Portainer
   curl -I https://portainer.yourdomain.com | grep "200 OK"
   ```

   **Timeout:** 15 minutes (includes SSL cert generation)

### Phase 6: Application Stacks Deployment (Phase 4-9 of 10)

10. **Deploy Application Stacks Sequentially**

    **Order (to respect dependencies):**
    1. **Monitoring Stack** (monitoring.yml)
       - Prometheus, Grafana, Loki, Uptime Kuma
       - Health: `curl http://localhost:9090/-/healthy`

    2. **Home Assistant Stack** (homeassistant.yml)
       - Home Assistant, MQTT, Zigbee2MQTT, Node-RED
       - Health: `curl http://localhost:8123`

    3. **Media Stack** (media.yml)
       - Jellyfin, Sonarr, Radarr, qBittorrent
       - Health: `curl http://localhost:8096/health`

    4. **Automation Stack** (automation.yml)
       - Pi-hole, n8n, Ollama
       - Health: `curl http://localhost:5678/healthz`

    **Execution Template:**
    ```bash
    for stack in monitoring homeassistant media automation; do
      echo "Deploying $stack stack..."
      ssh fitna@TARGET_HOST << EOF
        cd /home/fitna/homelab/infrastructure/docker/stacks
        docker compose -f ${stack}.yml pull
        docker compose -f ${stack}.yml up -d
        sleep 30  # Allow services to initialize
      EOF

      # Run health check
      ./health-check.sh $stack || {
        echo "❌ Health check failed for $stack"
        exit 1
      }
    done
    ```

### Phase 7: Health Monitoring (Continuous, 15-min timeout)

11. **Monitor Service Health**
    Create: `/home/fitna/homelab/infrastructure/scripts/health-check.sh`

    ```bash
    #!/bin/bash
    STACK=$1
    TIMEOUT=900  # 15 minutes
    INTERVAL=10  # Check every 10 seconds
    ELAPSED=0

    case $STACK in
      monitoring)
        HEALTH_URL="http://localhost:9090/-/healthy"
        ;;
      homeassistant)
        HEALTH_URL="http://localhost:8123"
        ;;
      media)
        HEALTH_URL="http://localhost:8096/health"
        ;;
      automation)
        HEALTH_URL="http://localhost:5678/healthz"
        ;;
    esac

    while [ $ELAPSED -lt $TIMEOUT ]; do
      if curl -sf $HEALTH_URL > /dev/null; then
        echo "✅ $STACK is healthy"
        exit 0
      fi
      sleep $INTERVAL
      ELAPSED=$((ELAPSED + INTERVAL))
    done

    echo "❌ $STACK health check timeout"
    exit 1
    ```

12. **Log Health Status**
    ```bash
    docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" > $LOG_DIR/containers.txt
    docker stats --no-stream > $LOG_DIR/stats.txt
    ```

### Phase 8: Rollback on Failure

13. **Automatic Rollback Logic**
    Reference: `.github/workflows/deploy.yml` lines 45-60

    **Trigger Conditions:**
    - Health check fails after 15 minutes
    - Container crashes (exit code != 0)
    - HTTP endpoint returns 5xx errors

    **Rollback Steps:**
    ```bash
    # 1. Stop failed deployment
    docker compose -f $FAILED_STACK down

    # 2. Restore previous version from backup
    BACKUP_DIR="/home/fitna/homelab/backups/pre-deploy-$DEPLOY_ID"
    docker compose -f $BACKUP_DIR/$FAILED_STACK up -d

    # 3. Verify rollback success
    ./health-check.sh $STACK || {
      echo "🚨 CRITICAL: Rollback failed, manual intervention required"
      # Send alert notification
    }

    # 4. Log rollback event
    echo "$(date): Rolled back $STACK to previous version" >> $LOG_DIR/rollback.log
    ```

14. **Notification on Rollback**
    ```bash
    # Send alert (if notification service configured)
    curl -X POST https://ntfy.sh/homelab-alerts \
      -H "Title: Deployment Rollback" \
      -H "Priority: urgent" \
      -d "Stack $STACK failed health check. Rolled back to previous version."
    ```

### Phase 9: Post-Deployment Validation (Phase 10 of 10)

15. **Run Integration Tests**
    ```bash
    # Test end-to-end connectivity
    curl -I https://yourdomain.com | grep "200 OK"

    # Verify SSL certificates
    echo | openssl s_client -connect yourdomain.com:443 2>&1 | grep "Verify return code: 0"

    # Check all containers are running
    EXPECTED_COUNT=25  # Adjust based on deployed stacks
    RUNNING_COUNT=$(docker ps --filter "status=running" -q | wc -l)
    [ $RUNNING_COUNT -eq $EXPECTED_COUNT ] || echo "⚠️ Container count mismatch"
    ```

16. **Generate Deployment Report**
    ```bash
    cat > $LOG_DIR/deployment-report.md << EOF
    # Deployment Report: $DEPLOY_ID

    **Date:** $(date)
    **Environment:** $ENVIRONMENT
    **Scope:** $SCOPE
    **Duration:** $DURATION seconds

    ## Deployed Stacks
    $(ls -1 *.yml)

    ## Health Status
    $(docker ps --format "- {{.Names}}: {{.Status}}")

    ## Rollbacks
    $(cat rollback.log 2>/dev/null || echo "None")

    ## Validation
    - [x] All containers running
    - [x] Health checks passing
    - [x] SSL certificates valid
    - [x] Integration tests passed

    **Status:** ✅ SUCCESS
    EOF
    ```

### Phase 10: Cleanup and Notification

17. **Cleanup Temporary Resources**
    ```bash
    # Remove old Docker images
    docker image prune -f

    # Cleanup old deployment logs (keep last 10)
    cd /home/fitna/homelab/logs/deployments
    ls -t | tail -n +11 | xargs rm -rf
    ```

18. **Send Success Notification**
    ```bash
    echo "✅ Deployment $DEPLOY_ID completed successfully at $(date)" | \
      tee -a /home/fitna/homelab/logs/deployment-history.log
    ```

## Rules and Constraints

### Hard Rules (Must Follow)
1. **ALWAYS run pre-deployment checklist** before any deployment
2. **NEVER deploy to production without SSH key verification**
3. **ALWAYS validate Docker Compose syntax** before deploying
4. **Database layer MUST deploy before application stacks**
5. **Health checks are MANDATORY** with 15-minute timeout
6. **Automatic rollback MUST trigger** on health check failure
7. **Secrets MUST NEVER be logged** or exposed in deployment reports
8. **Production deployments REQUIRE backup** to exist first

### Soft Rules (Best Practices)
- Test in staging before production
- Deploy during low-traffic hours (2-6 AM)
- Monitor logs in real-time during deployment
- Keep deployment windows under 90 minutes
- Document any manual interventions
- Notify stakeholders before major deployments

### Safety Mechanisms
1. **Retry Logic**: Up to 3 retries with exponential backoff (30s, 60s, 120s)
2. **Circuit Breaker**: Stop deployment if 2+ consecutive stacks fail
3. **Canary Deployment**: Deploy to staging first, then production
4. **Blue-Green**: Keep previous version running until new version healthy

## Expected Outputs

### Deliverables
1. **Deployment Log** - Complete execution log in `$LOG_DIR/`
2. **Deployment Report** - Summary in `deployment-report.md`
3. **Health Status** - Container health and stats
4. **Rollback Log** - Any rollback events (if applicable)
5. **Notification** - Success/failure alert

### File Structure
```
/home/fitna/homelab/logs/deployments/deploy-YYYYMMDD-HHMMSS/
├── deployment-report.md
├── containers.txt
├── stats.txt
├── rollback.log (if applicable)
└── health-checks.log
```

### Success Metrics
- ✅ All containers running (status: Up)
- ✅ Health checks passing (HTTP 200 OK)
- ✅ No rollbacks triggered
- ✅ Deployment completed within timeout (90 min)
- ✅ Zero downtime for critical services
- ✅ SSL certificates valid (>14 days expiry)

## Error Handling

### Common Issues & Solutions

**Issue: SSH connection refused**
- **Solution**: Verify SSH keys with `ssh-copy-id fitna@HOST`
- **Check**: `/home/fitna/homelab/SSH_SETUP_GUIDE.md`

**Issue: Docker Compose syntax error**
- **Solution**: Run `docker compose -f stack.yml config` to validate
- **Fix**: Correct indentation and environment variable syntax

**Issue: Health check timeout**
- **Solution**: Check container logs with `docker logs CONTAINER_NAME`
- **Action**: Trigger automatic rollback

**Issue: Port already in use**
- **Solution**: Stop conflicting service or change port in Docker Compose
- **Check**: `netstat -tulpn | grep PORT`

**Issue: SSL certificate generation fails**
- **Solution**: Verify DNS records point to correct IP
- **Check**: Traefik logs for ACME challenge errors

**Issue: Database migration fails**
- **Solution**: Rollback database to previous snapshot
- **Action**: Restore from `/home/fitna/homelab/backups/db/`

## Example Usage

### User Request
"Deploy the monitoring stack to production with health checks and automatic rollback."

### Agent Response
```markdown
I'll deploy the monitoring stack (Prometheus, Grafana, Loki, Uptime Kuma) to production with comprehensive validation.

**Pre-Deployment Validation:**
✅ SSH connectivity to VPS (91.107.198.37): OK
✅ Docker Compose syntax validation: OK
✅ Secrets verification: OK
✅ Recent backup exists: OK (2h ago)

**Deployment Execution:**
📦 Pulling latest images...
🚀 Starting monitoring stack...
⏳ Health check (timeout: 15 min)...

**Health Status:**
✅ Prometheus: http://localhost:9090/-/healthy (200 OK)
✅ Grafana: http://localhost:3000/api/health (200 OK)
✅ Loki: http://localhost:3100/ready (200 OK)
✅ Uptime Kuma: http://localhost:3001 (200 OK)

**Deployment Report:**
- Duration: 4 minutes 23 seconds
- Containers: 4/4 running
- Rollbacks: 0
- Status: ✅ SUCCESS

Log: /home/fitna/homelab/logs/deployments/deploy-20250128-143022/
```

## Integration Points

### Related Skills
- **Agent 5 - InfrastructureProvisioner**: Use for initial host setup
- **Agent 6 - MonitoringSetup**: Use after deployment to configure dashboards
- **Agent 10 - SecretSynchronizer**: Use before deployment to sync secrets

### External Tools
- GitHub Actions: `.github/workflows/deploy.yml`
- Ansible: `/home/fitna/homelab/infrastructure/ansible/`
- Docker Compose: `/home/fitna/homelab/infrastructure/docker/stacks/`
- Health check script: `/home/fitna/homelab/infrastructure/scripts/health-check.sh`

### Data Sources
- Deployment guide: `/home/fitna/homelab/infrastructure/DEPLOYMENT.md`
- Pre-deployment checklist: `/home/fitna/homelab/infrastructure/PRE-DEPLOYMENT-CHECKLIST.md`
- Host inventory: `/home/fitna/homelab/infrastructure/ansible/inventory/hosts.yml`

## Version
v1.0 - Initial skill definition based on 10-phase deployment workflow analysis
