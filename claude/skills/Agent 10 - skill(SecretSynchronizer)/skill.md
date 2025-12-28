# Skill: Secret Synchronizer

## Name
**Secret Synchronizer** - Automated Multi-Host Secret Distribution

## Description
This skill automates the secure distribution and synchronization of secrets (API keys, passwords, tokens) across the 3-system homelab deployment (VPS, ThinkPad, RTX1080). It manages the master secrets file at `/home/fitna/homelab/shared/secrets/.env.master`, validates secret formatting, securely copies to remote hosts using SSH, and ensures secrets are never committed to version control.

## When to Use This Skill

### Trigger Conditions
Use this skill when the user requests ANY of the following:
- "Sync secrets to [hosts/all]"
- "Update API keys"
- "Distribute secrets"
- "Add new secret/credential"
- "Synchronize environment variables"
- "Update [service] password"

### Context Indicators
- User mentions API keys, passwords, tokens, or credentials
- User needs to add/update secrets for services
- User discusses .env files or environment variables
- User mentions secret management or security

## Process Steps

### Phase 1: Master Secrets Management (5 minutes)

1. **Open Master Secrets File**
   ```bash
   # Location: /home/fitna/homelab/shared/secrets/.env.master
   # WARNING: This file contains sensitive data and MUST NEVER be committed to Git!

   vim /home/fitna/homelab/shared/secrets/.env.master
   ```

2. **Add or Update Secrets**
   **Format:** `KEY=value` (no spaces around =)

   **Categories:**

   **Database Credentials:**
   ```env
   POSTGRES_USER=homelab_admin
   POSTGRES_PASSWORD=strongpassword123!
   POSTGRES_DB=homelab
   REDIS_PASSWORD=redispass456!
   ```

   **API Keys:**
   ```env
   OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx
   ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxx
   STRIPE_SECRET_KEY=sk_live_xxxxxxxxxxxxx
   STRIPE_PUBLISHABLE_KEY=pk_live_xxxxxxxxxxxxx
   ```

   **Authentication & SSO:**
   ```env
   AUTHENTIK_SECRET_KEY=random-64-char-string
   AUTHENTIK_POSTGRES_PASSWORD=authentik_db_pass
   PORTAINER_ADMIN_PASSWORD=portainer_admin_pass
   GRAFANA_ADMIN_PASSWORD=grafana_admin_pass
   ```

   **Email & Notifications:**
   ```env
   SMTP_HOST=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USER=your-email@gmail.com
   SMTP_PASSWORD=app-specific-password
   TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
   TELEGRAM_CHAT_ID=123456789
   ```

   **VPN & Network:**
   ```env
   VPN_SERVICE_PROVIDER=nordvpn
   VPN_USER=your-vpn-username
   VPN_PASSWORD=your-vpn-password
   WIREGUARD_PRIVATE_KEY=xxxxxxxxxxxxx
   WIREGUARD_PUBLIC_KEY=xxxxxxxxxxxxx
   ```

   **Monitoring & Observability:**
   ```env
   GRAFANA_API_KEY=glsa_xxxxxxxxxxxxx
   PROMETHEUS_WEB_PASSWORD=prometheus_pass
   LOKI_AUTH_ENABLED=false
   UPTIME_KUMA_PASSWORD=kuma_pass
   ```

3. **Validate Secret Formatting**
   ```bash
   # Check for common formatting errors
   grep -E '^\s+' /home/fitna/homelab/shared/secrets/.env.master && echo "❌ Leading whitespace found"
   grep -E '\s+=\s+' /home/fitna/homelab/shared/secrets/.env.master && echo "❌ Spaces around = sign"
   grep -E '^[^#].*\s$' /home/fitna/homelab/shared/secrets/.env.master && echo "❌ Trailing whitespace found"

   # Should have no output if formatting correct
   ```

4. **Verify No Secrets in Git**
   ```bash
   # Check .gitignore includes secrets
   grep -q ".env" /home/fitna/homelab/.gitignore || echo "⚠️ Add .env to .gitignore!"

   # Verify no .env files staged
   git status | grep -q ".env" && echo "❌ DANGER: .env file staged for commit!" || echo "✅ No secrets in Git"
   ```

### Phase 2: Secret Distribution (5-10 minutes)

5. **Run Secret Sync Script**
   Reference: `/home/fitna/homelab/shared/scripts/sync-secrets.sh`

   **Sync to All Hosts:**
   ```bash
   /home/fitna/homelab/shared/scripts/sync-secrets.sh all
   ```

   **Sync to Specific Host:**
   ```bash
   # VPS only
   /home/fitna/homelab/shared/scripts/sync-secrets.sh vps

   # ThinkPad only
   /home/fitna/homelab/shared/scripts/sync-secrets.sh thinkpad

   # RTX1080 only
   /home/fitna/homelab/shared/scripts/sync-secrets.sh rtx1080
   ```

6. **Verify Sync Completion**
   ```bash
   # Check line count matches master
   MASTER_LINES=$(wc -l < /home/fitna/homelab/shared/secrets/.env.master)

   for host in vps thinkpad rtx1080; do
     REMOTE_LINES=$(ssh $host "wc -l < /home/fitna/homelab/shared/secrets/.env")
     if [ "$MASTER_LINES" -eq "$REMOTE_LINES" ]; then
       echo "✅ $host: $REMOTE_LINES lines (match)"
     else
       echo "❌ $host: $REMOTE_LINES lines (expected $MASTER_LINES)"
     fi
   done
   ```

7. **Verify File Permissions**
   ```bash
   # Secrets should be readable only by owner (600)
   for host in vps thinkpad rtx1080; do
     ssh $host "ls -l /home/fitna/homelab/shared/secrets/.env" | grep -q "rw-------" && \
       echo "✅ $host: Permissions correct (600)" || \
       echo "❌ $host: Permissions incorrect (should be 600)"
   done
   ```

### Phase 3: Service Restart (If Needed)

8. **Identify Services Using Updated Secrets**
   Common services that need restart after secret updates:
   - **Database layer**: PostgreSQL, Redis
   - **Authentication**: Authentik
   - **Monitoring**: Grafana, Prometheus
   - **Email**: SMTP containers
   - **VPN**: Gluetun
   - **AI Services**: Ollama (if using API keys)

9. **Restart Services with Updated Secrets**
   ```bash
   # Restart specific service
   ssh vps "cd /home/fitna/homelab/infrastructure/docker/stacks && \
            docker compose -f core-hostA.yml restart authentik-server"

   # Restart entire stack (if many secrets changed)
   ssh vps "cd /home/fitna/homelab/infrastructure/docker/stacks && \
            docker compose -f core-hostA.yml up -d --force-recreate"

   # Verify service health after restart
   ssh vps "docker ps --filter 'name=authentik' --format 'table {{.Names}}\t{{.Status}}'"
   ```

10. **Validate Services Using New Secrets**
    ```bash
    # Test database connection
    docker exec homelab-postgres pg_isready -U $POSTGRES_USER

    # Test Redis auth
    docker exec homelab-redis redis-cli -a $REDIS_PASSWORD ping

    # Test API key (example: OpenAI)
    curl https://api.openai.com/v1/models \
      -H "Authorization: Bearer $OPENAI_API_KEY" | jq '.data[0].id'

    # Test SMTP (send test email)
    echo "Test" | mail -s "Test Email" your-email@gmail.com
    ```

### Phase 4: Security Audit (5 minutes)

11. **Audit Secret Security**
    - [ ] Master secrets file permissions: 600 (owner read/write only)
    - [ ] No secrets in Git repository or commit history
    - [ ] All secrets synced to remote hosts
    - [ ] Remote secret files have 600 permissions
    - [ ] No secrets logged in deployment logs
    - [ ] No secrets exposed in Docker Compose files (use ${VAR} references)
    - [ ] API keys rotated regularly (every 90 days)

12. **Check for Exposed Secrets**
    ```bash
    # Search Git history for potential secrets
    git log --all --full-history --source --all -- '*/.env*'

    # Should return nothing (secrets should be gitignored)

    # Check for hardcoded secrets in codebase
    grep -r "sk-" /home/fitna/homelab/infrastructure/ --exclude-dir=.git
    grep -r "password.*=" /home/fitna/homelab/infrastructure/ --exclude-dir=.git | grep -v "PASSWORD}"

    # Review findings manually (some may be false positives)
    ```

13. **Generate Secret Inventory**
    ```bash
    # Create secret inventory (for documentation, NOT for sharing!)
    cat > /home/fitna/homelab/shared/secrets/secret-inventory.md << EOF
    # Secret Inventory - $(date +%Y-%m-%d)

    ## Database Credentials
    - PostgreSQL: User, Password, DB name
    - Redis: Password

    ## API Keys
    - OpenAI: API key (expires: N/A)
    - Anthropic: API key (expires: N/A)
    - Stripe: Secret key, Publishable key (rotate: 90 days)

    ## Authentication
    - Authentik: Secret key, DB password
    - Portainer: Admin password
    - Grafana: Admin password

    ## Email & Notifications
    - SMTP: Host, port, user, password
    - Telegram: Bot token, Chat ID

    ## VPN
    - VPN provider: Username, password
    - WireGuard: Private key, public key

    ## Last Updated
    $(date)

    ## Next Rotation Due
    $(date -d "+90 days")
    EOF
    ```

### Phase 5: Backup and Recovery (Continuous)

14. **Backup Master Secrets**
    ```bash
    # Create encrypted backup
    BACKUP_DIR="/home/fitna/homelab/backups/secrets"
    mkdir -p "$BACKUP_DIR"

    # Encrypt with GPG (requires passphrase)
    gpg --symmetric --cipher-algo AES256 \
      -o "$BACKUP_DIR/.env.master-$(date +%Y%m%d).gpg" \
      /home/fitna/homelab/shared/secrets/.env.master

    # Store backup securely (offline or encrypted cloud storage)
    ```

15. **Document Recovery Procedure**
    ```markdown
    ## Secret Recovery Procedure

    1. Locate encrypted backup:
       `/home/fitna/homelab/backups/secrets/.env.master-YYYYMMDD.gpg`

    2. Decrypt with GPG:
       ```bash
       gpg -o .env.master -d /path/to/.env.master-YYYYMMDD.gpg
       ```

    3. Restore to master location:
       ```bash
       cp .env.master /home/fitna/homelab/shared/secrets/.env.master
       chmod 600 /home/fitna/homelab/shared/secrets/.env.master
       ```

    4. Sync to all hosts:
       ```bash
       /home/fitna/homelab/shared/scripts/sync-secrets.sh all
       ```

    5. Restart affected services
    ```

## Rules and Constraints

### Hard Rules (Must Follow)
1. **NEVER commit .env files to Git** (even encrypted)
2. **Master secrets file MUST have 600 permissions** (owner only)
3. **Remote secrets MUST have 600 permissions** (owner only)
4. **Sync MUST use SSH** (never plain text over network)
5. **Secrets MUST be backed up encrypted** (GPG or similar)
6. **API keys MUST be rotated every 90 days** (security policy)
7. **NEVER log secrets** in deployment logs or console output

### Soft Rules (Best Practices)
- Use strong, unique passwords (20+ characters, mixed case, symbols)
- Prefer API keys over passwords (easier to rotate)
- Document secret purpose in inventory (not in .env file)
- Test secret validity after rotation
- Notify team when secrets rotated

### Quality Gates
Before marking secret sync complete:
- [ ] Master secrets file validated (no formatting errors)
- [ ] Secrets synced to all 3 hosts
- [ ] Line counts match across all hosts
- [ ] File permissions verified (600)
- [ ] Services restarted and healthy
- [ ] No secrets in Git (verified)
- [ ] Backup created (encrypted)

## Expected Outputs

### Deliverables
1. **Updated .env.master** - Master secrets file
2. **Sync Confirmation** - Verification of successful sync
3. **Service Health Report** - Services using new secrets healthy
4. **Secret Inventory** - Documentation of secrets (secure location)
5. **Encrypted Backup** - GPG-encrypted backup of secrets

### Success Metrics
- ✅ All 3 hosts have identical .env files
- ✅ File permissions: 600 on all hosts
- ✅ Services restarted and healthy
- ✅ 0 secrets in Git repository
- ✅ Backup created and encrypted

## Error Handling

### Common Issues & Solutions

**Issue: SSH connection fails during sync**
- **Solution**: Verify SSH keys set up (see Agent 8 - SOPExecutor)
- **Command**: `ssh vps "echo 'test'"` (should work without password)

**Issue: File permissions incorrect after sync**
- **Solution**: Manually fix permissions on remote hosts
- **Command**: `ssh vps "chmod 600 /home/fitna/homelab/shared/secrets/.env"`

**Issue: Line count mismatch after sync**
- **Solution**: Re-run sync script, verify no network interruption
- **Check**: `diff /local/.env.master <(ssh vps cat /remote/.env)`

**Issue: Service won't start after secret update**
- **Solution**: Check secret format (no extra spaces, correct syntax)
- **Validate**: `docker compose config` (shows resolved environment variables)

**Issue: Secret accidentally committed to Git**
- **URGENT**: Remove from history immediately
- **Command**:
  ```bash
  # Remove from current commit
  git rm --cached .env
  git commit --amend --no-edit

  # Remove from history (if already pushed)
  git filter-branch --index-filter \
    'git rm --cached --ignore-unmatch shared/secrets/.env' HEAD

  # Rotate ALL secrets in the exposed file immediately!
  ```

**Issue: Lost master secrets file**
- **Solution**: Restore from encrypted backup (see Phase 5, Step 15)
- **Prevention**: Automate weekly encrypted backups

## Example Usage

### User Request
"Update the OpenAI API key and sync to all hosts."

### Agent Response
```markdown
I'll update the OpenAI API key and sync to all hosts.

**Step 1: Updating Master Secrets**
Editing `/home/fitna/homelab/shared/secrets/.env.master`:
```env
OPENAI_API_KEY=sk-proj-newkeyxxxxxxxxxxxxxxx
```
✅ Master secrets updated

**Step 2: Validating Formatting**
✅ No leading whitespace
✅ No spaces around = sign
✅ No trailing whitespace

**Step 3: Syncing to Hosts**
```bash
/home/fitna/homelab/shared/scripts/sync-secrets.sh all
```

Syncing to VPS (91.107.198.37)... ✅
Syncing to ThinkPad (192.168.16.7)... ✅
Syncing to RTX1080 (192.168.17.1)... ✅

**Step 4: Verifying Sync**
✅ VPS: 47 lines (match)
✅ ThinkPad: 47 lines (match)
✅ RTX1080: 47 lines (match)

**Step 5: Checking File Permissions**
✅ VPS: Permissions correct (600)
✅ ThinkPad: Permissions correct (600)
✅ RTX1080: Permissions correct (600)

**Step 6: Services Using OpenAI API**
Identifying services: Ollama container

Restarting Ollama... ✅
```bash
ssh rtx1080 "docker restart ollama"
```

**Step 7: Validating New API Key**
Testing OpenAI connection...
```bash
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY" | jq '.data[0].id'
```
✅ Response: "gpt-4" (API key valid)

**Step 8: Creating Encrypted Backup**
```bash
gpg --symmetric --cipher-algo AES256 \
  -o backups/secrets/.env.master-20250128.gpg \
  shared/secrets/.env.master
```
✅ Encrypted backup created

**Security Checklist:**
✅ No secrets in Git
✅ File permissions: 600 on all hosts
✅ API key validated
✅ Services healthy
✅ Backup created (encrypted)

**OpenAI API key updated and synced successfully!**
```

## Integration Points

### Related Skills
- **Agent 2 - DeploymentOrchestrator**: Sync secrets before deployment
- **Agent 5 - InfrastructureProvisioner**: Sync secrets after host provisioning
- **Agent 8 - SOPExecutor**: Execute secret management SOPs

### External Tools
- Sync script: `/home/fitna/homelab/shared/scripts/sync-secrets.sh`
- GPG for encryption
- SSH for secure transfer

### Data Sources
- Master secrets: `/home/fitna/homelab/shared/secrets/.env.master`
- .gitignore: `/home/fitna/homelab/.gitignore`
- Docker Compose stacks: `/home/fitna/homelab/infrastructure/docker/stacks/`

## Version
v1.0 - Initial skill definition based on secret management workflow analysis
