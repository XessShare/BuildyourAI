# Skill: SOP Executor

## Name
**SOP Executor** - Guided Standard Operating Procedure Execution

## Description
This skill provides step-by-step guided execution of standard operating procedures (SOPs) documented across the homelab project. It references procedures from `/home/fitna/homelab/SSH_SETUP_GUIDE.md`, `/home/fitna/homelab/shared/docs/BENUTZERHANDBUCH.md`, admin guides, and infrastructure documentation to execute common tasks like SSH setup, backup/restore, troubleshooting, and secret management with validation at each step.

## When to Use This Skill

### Trigger Conditions
Use this skill when the user requests ANY of the following:
- "Set up SSH keys"
- "Run backup procedure"
- "Troubleshoot [service/issue]"
- "Execute SOP for [task]"
- "Follow the procedure for [operation]"
- "How do I [standard operation]?"
- "Restore from backup"

### Context Indicators
- User mentions documented procedures or SOPs
- User needs to perform routine maintenance tasks
- User encounters common issues with known solutions
- User requests step-by-step guidance for infrastructure tasks

## Available SOPs

### 1. SSH Key Setup (Priority: HIGH)
**Reference:** `/home/fitna/homelab/SSH_SETUP_GUIDE.md`

**When to Use:**
- Setting up passwordless authentication to VPS, ThinkPad, or RTX1080
- Configuring new development machine
- Troubleshooting SSH connection issues

**Steps:**
1. **Generate SSH Key (if not exists)**
   ```bash
   # Check for existing key
   ls -la ~/.ssh/id_ed25519*

   # Generate new ed25519 key
   ssh-keygen -t ed25519 -C "your_email@example.com" -f ~/.ssh/id_ed25519

   # Start SSH agent
   eval "$(ssh-agent -s)"

   # Add key to agent
   ssh-add ~/.ssh/id_ed25519
   ```

2. **Distribute Key to Hosts**
   ```bash
   # Copy to VPS
   ssh-copy-id -i ~/.ssh/id_ed25519.pub fitna@91.107.198.37

   # Copy to ThinkPad
   ssh-copy-id -i ~/.ssh/id_ed25519.pub fitna@192.168.16.7

   # Copy to RTX1080
   ssh-copy-id -i ~/.ssh/id_ed25519.pub fitna@192.168.17.1
   ```

3. **Configure SSH Config**
   Create `~/.ssh/config`:
   ```
   Host vps
     HostName 91.107.198.37
     User fitna
     IdentityFile ~/.ssh/id_ed25519

   Host thinkpad
     HostName 192.168.16.7
     User fitna
     IdentityFile ~/.ssh/id_ed25519

   Host rtx1080
     HostName 192.168.17.1
     User fitna
     IdentityFile ~/.ssh/id_ed25519
   ```

4. **Test Connections**
   ```bash
   ssh vps "echo 'VPS connection successful'"
   ssh thinkpad "echo 'ThinkPad connection successful'"
   ssh rtx1080 "echo 'RTX1080 connection successful'"
   ```

**Validation:**
- [ ] SSH key generated (ed25519)
- [ ] Key copied to all 3 hosts
- [ ] SSH config created with host aliases
- [ ] Passwordless login works for all hosts

---

### 2. Secrets Management (Priority: HIGH)
**Reference:** `/home/fitna/homelab/shared/scripts/sync-secrets.sh`

**When to Use:**
- Adding new API keys or credentials
- Syncing secrets across hosts (VPS, ThinkPad, RTX1080)
- Updating environment variables for services

**Steps:**
1. **Edit Master Secrets File**
   ```bash
   # Location: /home/fitna/homelab/shared/secrets/.env.master
   # NEVER commit this file to Git!

   vim /home/fitna/homelab/shared/secrets/.env.master
   ```

   **Add/Update Secrets:**
   ```env
   # Database
   POSTGRES_PASSWORD=xxxxx
   REDIS_PASSWORD=xxxxx

   # APIs
   OPENAI_API_KEY=sk-xxxxx
   STRIPE_SECRET_KEY=sk_live_xxxxx

   # Authentication
   AUTHENTIK_SECRET_KEY=xxxxx
   PORTAINER_ADMIN_PASSWORD=xxxxx
   ```

2. **Sync Secrets to Hosts**
   ```bash
   /home/fitna/homelab/shared/scripts/sync-secrets.sh all

   # Or sync to specific host
   /home/fitna/homelab/shared/scripts/sync-secrets.sh vps
   /home/fitna/homelab/shared/scripts/sync-secrets.sh thinkpad
   /home/fitna/homelab/shared/scripts/sync-secrets.sh rtx1080
   ```

3. **Verify Secrets on Hosts**
   ```bash
   ssh vps "cat /home/fitna/homelab/shared/secrets/.env | wc -l"
   # Should match master file line count
   ```

4. **Restart Services (if needed)**
   ```bash
   # Restart services that use updated secrets
   docker compose -f /path/to/stack.yml restart service-name
   ```

**Validation:**
- [ ] Master secrets file updated
- [ ] Secrets synced to all hosts
- [ ] Line count matches across hosts
- [ ] Services restarted if needed
- [ ] .env files NOT committed to Git

---

### 3. Backup & Restore (Priority: CRITICAL)
**Reference:** `/home/fitna/homelab/shared/scripts/snapshot.sh`

**When to Use:**
- Before major deployments or changes
- Regular scheduled backups (daily, weekly, monthly)
- Disaster recovery scenarios

**Create Backup:**
```bash
# Create snapshot
/home/fitna/homelab/shared/scripts/snapshot.sh create "Pre-deployment backup"

# List snapshots
/home/fitna/homelab/shared/scripts/snapshot.sh list

# Verify backup
ls -lh /home/fitna/homelab/backups/latest/
```

**Restore from Backup:**
```bash
# List available snapshots
/home/fitna/homelab/shared/scripts/snapshot.sh list

# Restore from specific snapshot
/home/fitna/homelab/shared/scripts/snapshot.sh restore snapshot-20250128-143022

# Verify restoration
docker compose ps
```

**Validation:**
- [ ] Snapshot created successfully
- [ ] Backup size reasonable (check with `du -sh`)
- [ ] Restoration tested (in staging environment)

---

### 4. Troubleshooting Common Issues (Priority: MEDIUM)

**Issue: Container Won't Start**
```bash
# 1. Check logs
docker logs container-name --tail 100

# 2. Check container status
docker ps -a | grep container-name

# 3. Try restart
docker restart container-name

# 4. Force recreate
docker compose -f stack.yml up -d --force-recreate container-name

# 5. Check resource limits
docker stats container-name
```

**Issue: Traefik Not Routing**
```bash
# 1. Check Traefik logs
docker logs traefik --tail 100

# 2. Verify labels on service
docker inspect service-name | grep -A 10 Labels

# 3. Check Traefik dashboard
# Access: http://traefik.yourdomain.com/dashboard/

# 4. Test DNS resolution
nslookup service.yourdomain.com

# 5. Verify SSL certificate
echo | openssl s_client -connect service.yourdomain.com:443 | grep subject
```

**Issue: Authentik SSO Failing**
```bash
# 1. Check Authentik logs
docker logs authentik-server --tail 100

# 2. Verify OIDC configuration
# Authentik → Applications → [App] → Check Provider settings

# 3. Test endpoint
curl -I https://auth.yourdomain.com/.well-known/openid-configuration

# 4. Check database connection
docker exec authentik-server python -m authentik.lib.dbtest
```

**Issue: VPN (Gluetun) Not Connecting**
```bash
# 1. Check Gluetun logs
docker logs gluetun --tail 100

# 2. Verify VPN credentials in .env
cat /path/to/.env | grep VPN

# 3. Verify public IP (should be VPN IP, not home IP)
docker exec gluetun curl -s ifconfig.me

# 4. Restart VPN
docker restart gluetun

# 5. Test from downstream container
docker exec qbittorrent curl -s ifconfig.me
```

---

### 5. Update Procedure (Priority: MEDIUM)

**Update Docker Images:**
```bash
# 1. Pull latest images
cd /home/fitna/homelab/infrastructure/docker/stacks
docker compose -f stack.yml pull

# 2. Create backup before update
/home/fitna/homelab/shared/scripts/snapshot.sh create "Pre-update backup"

# 3. Recreate containers with new images
docker compose -f stack.yml up -d

# 4. Verify services healthy
docker ps --format "table {{.Names}}\t{{.Status}}"

# 5. Check logs for errors
docker compose -f stack.yml logs --tail 50
```

**Update System Packages:**
```bash
# Run on all hosts
ansible all -i /home/fitna/homelab/infrastructure/ansible/inventory/hosts.yml \
  -m apt -a "update_cache=yes upgrade=dist" --become

# Or manually on each host
ssh vps "sudo apt update && sudo apt upgrade -y"
ssh thinkpad "sudo apt update && sudo apt upgrade -y"
ssh rtx1080 "sudo apt update && sudo apt upgrade -y"
```

---

### 6. Health Check Procedure (Priority: LOW)

**Daily Health Check:**
```bash
# 1. Check all containers running
docker ps --filter "status=exited"

# 2. Check disk space (should be >10% free)
df -h

# 3. Check memory usage (should be <90%)
free -h

# 4. Check Docker stats
docker stats --no-stream

# 5. Check recent logs for errors
docker compose logs --since 1h | grep -i error

# 6. Verify critical services
curl -I https://yourdomain.com
curl -I https://auth.yourdomain.com
curl -I https://portainer.yourdomain.com
```

## Rules and Constraints

### Hard Rules (Must Follow)
1. **ALWAYS create backup** before destructive operations
2. **NEVER skip validation steps** at end of procedures
3. **ALWAYS document deviations** from standard procedure
4. **Secrets MUST NEVER be logged** or printed to console
5. **SSH keys MUST be ed25519** (not RSA)
6. **Troubleshooting MUST check logs first** before restarting

### Soft Rules (Best Practices)
- Execute SOPs in staging before production
- Document any manual steps not in SOP
- Update SOP documentation if procedure changes
- Use descriptive snapshot names (include reason)

### Quality Gates
Before marking SOP execution complete:
- [ ] All validation checkboxes marked
- [ ] No errors in logs
- [ ] Services respond to health checks
- [ ] Documentation updated (if deviations)

## Expected Outputs

### Deliverables
1. **Execution Log** - Commands run and outputs
2. **Validation Report** - Checklist of completed validations
3. **Issue Resolution** - For troubleshooting SOPs
4. **Updated Documentation** - If SOP changed

### Success Metrics
- ✅ All validation steps passed
- ✅ Services healthy after execution
- ✅ No errors or warnings in logs
- ✅ Procedure completed within expected time

## Error Handling

### Common Issues & Solutions

**Issue: Backup fails (disk space)**
- **Solution**: Clean up old backups, increase retention policy
- **Command**: `rm -rf /home/fitna/homelab/backups/old-*`

**Issue: Secret sync fails (SSH)**
- **Solution**: Verify SSH connectivity, re-run sync
- **Check**: SOP #1 (SSH Key Setup)

**Issue: Service doesn't start after update**
- **Solution**: Rollback to previous image version
- **Command**: `docker compose -f stack.yml down && restore backup`

**Issue: Procedure documentation outdated**
- **Solution**: Update SOP documentation, notify users
- **Action**: Create PR with SOP updates

## Example Usage

### User Request
"Set up SSH keys for the new VPS server."

### Agent Response
```markdown
I'll guide you through SSH key setup for the VPS.

**Step 1: Generate SSH Key**
```bash
ssh-keygen -t ed25519 -C "your_email@example.com" -f ~/.ssh/id_ed25519
```
✅ Key generated: ~/.ssh/id_ed25519

**Step 2: Copy Key to VPS**
```bash
ssh-copy-id -i ~/.ssh/id_ed25519.pub fitna@91.107.198.37
```
Enter password when prompted (last time!)

**Step 3: Configure SSH Config**
Added VPS alias to ~/.ssh/config:
```
Host vps
  HostName 91.107.198.37
  User fitna
  IdentityFile ~/.ssh/id_ed25519
```

**Step 4: Test Connection**
```bash
ssh vps "echo 'Connection successful'"
```
✅ VPS connection successful

**Validation:**
✅ SSH key generated (ed25519)
✅ Key copied to VPS
✅ SSH config updated
✅ Passwordless login working

You can now connect with: `ssh vps`
```

## Integration Points

### Related Skills
- **Agent 2 - DeploymentOrchestrator**: Execute deployment SOPs
- **Agent 5 - InfrastructureProvisioner**: Execute provisioning SOPs
- **Agent 10 - SecretSynchronizer**: Execute secret management SOPs

### External Tools
- Scripts: `/home/fitna/homelab/shared/scripts/`
- Documentation: `/home/fitna/homelab/shared/docs/`
- Admin guides: `/home/fitna/homelab/shared/docs/private-docs/admin/`

### Data Sources
- SSH guide: `/home/fitna/homelab/SSH_SETUP_GUIDE.md`
- User handbook: `/home/fitna/homelab/shared/docs/BENUTZERHANDBUCH.md`
- Troubleshooting guides: Infrastructure documentation

## Version
v1.0 - Initial skill definition based on homelab SOP analysis
