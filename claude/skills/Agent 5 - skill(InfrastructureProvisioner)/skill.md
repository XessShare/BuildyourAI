# Skill: Infrastructure Provisioner

## Name
**Infrastructure Provisioner** - Automated Ansible-Based Host Provisioning

## Description
This skill automates the initial provisioning and configuration of homelab infrastructure hosts using Ansible playbooks from `/home/fitna/homelab/infrastructure/ansible/`. It performs bootstrap operations including package updates, UFW firewall configuration, Docker installation, SSH hardening, timezone setup, and essential utilities installation across the 3-system deployment (VPS, ThinkPad, RTX1080).

## When to Use This Skill

### Trigger Conditions
Use this skill when the user requests ANY of the following:
- "Provision [host/server]"
- "Bootstrap new infrastructure"
- "Set up [VPS/ThinkPad/RTX1080] from scratch"
- "Run Ansible playbooks"
- "Initialize new host"
- "Configure server infrastructure"
- "Prepare host for Docker deployment"

### Context Indicators
- User mentions new servers, fresh installs, or bare-metal setup
- User discusses Ansible, provisioning, or infrastructure as code
- User needs to configure firewall, SSH, or system settings
- User mentions host inventory or multi-host setup

## Process Steps

### Phase 1: Pre-Provisioning Preparation (5-10 minutes)

1. **Verify Ansible Installation**
   ```bash
   ansible --version || {
     echo "Installing Ansible..."
     sudo apt update && sudo apt install -y ansible
   }
   ```

2. **Check Host Inventory**
   Reference: `/home/fitna/homelab/infrastructure/ansible/inventory/hosts.yml`

   **Verify hosts are defined:**
   ```yaml
   all:
     children:
       production:
         hosts:
           vps:
             ansible_host: 91.107.198.37
             ansible_user: fitna
           rtx1080:
             ansible_host: 192.168.17.1
             ansible_user: fitna
       staging:
         hosts:
           thinkpad:
             ansible_host: 192.168.16.7
             ansible_user: fitna
   ```

3. **Test SSH Connectivity**
   ```bash
   # Test all hosts
   ansible all -i /home/fitna/homelab/infrastructure/ansible/inventory/hosts.yml -m ping

   # Expected output:
   # vps | SUCCESS => {"ping": "pong"}
   # rtx1080 | SUCCESS => {"ping": "pong"}
   # thinkpad | SUCCESS => {"ping": "pong"}
   ```

   **If SSH fails:**
   - Check SSH keys: `/home/fitna/homelab/SSH_SETUP_GUIDE.md`
   - Run: `ssh-copy-id fitna@HOST_IP`

4. **Review Playbook Tasks**
   Reference: `/home/fitna/homelab/infrastructure/ansible/playbooks/00-bootstrap.yml`

   **Tasks to be executed:**
   - Update package cache (apt update)
   - Upgrade all packages (apt upgrade)
   - Install essential utilities (curl, wget, git, vim, htop, net-tools)
   - Configure UFW firewall (allow 22, 80, 443, 51820)
   - Set timezone to Europe/Berlin
   - Create swap file (4GB)
   - Install Docker and Docker Compose
   - Configure Docker group permissions
   - Harden SSH (disable password auth, key-only)
   - Create homelab directory structure

### Phase 2: Execute Ansible Bootstrap (10-20 minutes)

5. **Run Bootstrap Playbook**

   **Full deployment (all hosts):**
   ```bash
   cd /home/fitna/homelab/infrastructure/ansible

   ansible-playbook playbooks/00-bootstrap.yml \
     -i inventory/hosts.yml \
     --ask-become-pass
   ```

   **Single host deployment:**
   ```bash
   # VPS only
   ansible-playbook playbooks/00-bootstrap.yml \
     -i inventory/hosts.yml \
     --limit vps \
     --ask-become-pass

   # ThinkPad only
   ansible-playbook playbooks/00-bootstrap.yml \
     -i inventory/hosts.yml \
     --limit thinkpad \
     --ask-become-pass

   # RTX1080 only
   ansible-playbook playbooks/00-bootstrap.yml \
     -i inventory/hosts.yml \
     --limit rtx1080 \
     --ask-become-pass
   ```

6. **Monitor Playbook Execution**
   Watch output for:
   - `ok`: Task completed successfully
   - `changed`: Task made changes (expected on first run)
   - `failed`: Task failed (requires investigation)
   - `skipped`: Task skipped due to conditions

   **Expected duration per host:** 5-15 minutes

### Phase 3: Post-Provisioning Validation (5 minutes)

7. **Verify Package Updates**
   ```bash
   ansible all -i inventory/hosts.yml -m command -a "apt list --upgradable" --become
   ```
   **Expected:** Empty list or only non-critical packages

8. **Verify UFW Firewall**
   ```bash
   ansible all -i inventory/hosts.yml -m command -a "ufw status" --become
   ```
   **Expected:**
   ```
   Status: active
   22/tcp                     ALLOW       Anywhere
   80/tcp                     ALLOW       Anywhere
   443/tcp                    ALLOW       Anywhere
   51820/udp                  ALLOW       Anywhere
   ```

9. **Verify Docker Installation**
   ```bash
   ansible all -i inventory/hosts.yml -m command -a "docker --version"
   ansible all -i inventory/hosts.yml -m command -a "docker compose version"
   ```
   **Expected:** Docker 24+ and Docker Compose 2.20+

10. **Verify Timezone**
    ```bash
    ansible all -i inventory/hosts.yml -m command -a "timedatectl"
    ```
    **Expected:** `Time zone: Europe/Berlin`

11. **Verify Swap File**
    ```bash
    ansible all -i inventory/hosts.yml -m command -a "free -h" --become
    ```
    **Expected:** Swap showing ~4GB

12. **Verify SSH Hardening**
    ```bash
    ansible all -i inventory/hosts.yml -m command -a "grep PasswordAuthentication /etc/ssh/sshd_config" --become
    ```
    **Expected:** `PasswordAuthentication no`

### Phase 4: Directory Structure Setup

13. **Create Homelab Directory Structure**
    ```bash
    ansible all -i inventory/hosts.yml -m file -a "path=/home/fitna/homelab state=directory"
    ansible all -i inventory/hosts.yml -m file -a "path=/home/fitna/homelab/infrastructure state=directory"
    ansible all -i inventory/hosts.yml -m file -a "path=/home/fitna/homelab/logs state=directory"
    ansible all -i inventory/hosts.yml -m file -a "path=/home/fitna/homelab/backups state=directory"
    ```

14. **Sync Docker Compose Stacks**
    ```bash
    # Copy Docker Compose files to hosts
    ansible-playbook playbooks/sync-docker-stacks.yml -i inventory/hosts.yml
    ```

### Phase 5: Specialized Host Configuration

15. **VPS-Specific Configuration**
    Reference: `/home/fitna/homelab/infrastructure/ansible/playbooks/configure-vps.yml`

    ```bash
    ansible-playbook playbooks/configure-vps.yml -i inventory/hosts.yml
    ```

    **Tasks:**
    - Open public ports (80, 443)
    - Install Certbot for SSL
    - Configure DNS records
    - Enable UFW rate limiting on SSH

16. **RTX1080-Specific Configuration (GPU Host)**
    Reference: `/home/fitna/homelab/GAMING_PC_CONFIGURATION.md`

    ```bash
    ansible-playbook playbooks/configure-rtx1080.yml -i inventory/hosts.yml
    ```

    **Tasks:**
    - Install NVIDIA drivers
    - Install NVIDIA Container Toolkit
    - Configure Docker GPU support
    - Set up Ollama for AI workloads

17. **ThinkPad-Specific Configuration (Development)**
    ```bash
    ansible-playbook playbooks/configure-thinkpad.yml -i inventory/hosts.yml
    ```

    **Tasks:**
    - Install development tools (Python, Node.js, Go)
    - Configure VS Code Server
    - Set up testing environment

## Rules and Constraints

### Hard Rules (Must Follow)
1. **ALWAYS test SSH connectivity** before running playbooks
2. **NEVER skip firewall configuration** (security critical)
3. **ALWAYS backup existing configs** before overwriting
4. **Run playbooks with --check first** (dry-run mode) for production
5. **UFW MUST allow SSH (port 22)** before enabling (avoid lockout)
6. **Playbooks MUST be idempotent** (safe to run multiple times)
7. **NEVER hardcode passwords** in playbooks (use Ansible Vault)

### Soft Rules (Best Practices)
- Run bootstrap on staging (ThinkPad) before production
- Tag tasks for selective execution (--tags docker, --tags firewall)
- Log all playbook runs for audit trail
- Use Ansible Vault for sensitive variables
- Document any manual post-provisioning steps

### Safety Mechanisms
1. **Dry-Run Mode**: `ansible-playbook --check` (test without changes)
2. **Diff Mode**: `ansible-playbook --diff` (show changes before applying)
3. **Step Mode**: `ansible-playbook --step` (confirm each task)
4. **Rollback Snapshots**: Create system snapshot before major changes

## Expected Outputs

### Deliverables
1. **Provisioning Log** - Ansible playbook execution output
2. **Validation Report** - Post-provisioning checks
3. **Host Inventory** - Updated with provisioned hosts
4. **Configuration Backup** - Pre-provisioning state

### Success Metrics
- ✅ All hosts reachable via SSH
- ✅ UFW firewall active with correct rules
- ✅ Docker and Docker Compose installed
- ✅ Timezone set to Europe/Berlin
- ✅ Swap file active (4GB)
- ✅ SSH hardened (key-only auth)
- ✅ No failed Ansible tasks

## Error Handling

### Common Issues & Solutions

**Issue: SSH connection refused**
- **Solution**: Copy SSH key with `ssh-copy-id fitna@HOST`
- **Check**: `/home/fitna/homelab/SSH_SETUP_GUIDE.md`

**Issue: UFW blocks SSH (lockout)**
- **Solution**: Access via console, run `ufw allow 22/tcp && ufw reload`
- **Prevention**: Always allow SSH before enabling UFW

**Issue: Docker installation fails**
- **Solution**: Check Docker apt repository, update GPG keys
- **Docs**: https://docs.docker.com/engine/install/ubuntu/

**Issue: Ansible task timeout**
- **Solution**: Increase timeout in ansible.cfg: `timeout = 60`
- **Action**: Check host network connectivity

**Issue: Package conflicts during upgrade**
- **Solution**: Run `apt-get dist-upgrade` instead of `apt-get upgrade`
- **Escalate**: Manual intervention may be required

## Example Usage

### User Request
"Provision the new VPS server for production deployment."

### Agent Response
```markdown
I'll provision the VPS (91.107.198.37) with bootstrap configuration.

**Pre-Provisioning Checks:**
✅ SSH connectivity: OK
✅ Ansible installed: v2.15.0
✅ Host inventory: VPS defined

**Running Bootstrap Playbook...**

PLAY [Bootstrap homelab hosts] *************************
TASK [Update apt cache] ******************************** ok: [vps]
TASK [Upgrade all packages] **************************** changed: [vps]
TASK [Install essential utilities] ********************* changed: [vps]
TASK [Configure UFW firewall] ************************** changed: [vps]
TASK [Set timezone to Europe/Berlin] ******************* changed: [vps]
TASK [Create swap file (4GB)] ************************** changed: [vps]
TASK [Install Docker] ********************************** changed: [vps]
TASK [Harden SSH configuration] ************************ changed: [vps]

PLAY RECAP *********************************************
vps: ok=12 changed=8 unreachable=0 failed=0 skipped=0

**Post-Provisioning Validation:**
✅ Docker: 24.0.7 installed
✅ UFW: Active (ports 22, 80, 443, 51820 open)
✅ Timezone: Europe/Berlin (CET)
✅ Swap: 4.0G active
✅ SSH: Key-only authentication enabled

**Duration:** 8 minutes 42 seconds
**Status:** ✅ SUCCESS

VPS is ready for Docker stack deployment!
```

## Integration Points

### Related Skills
- **Agent 2 - DeploymentOrchestrator**: Use after provisioning to deploy stacks
- **Agent 6 - MonitoringSetup**: Deploy monitoring after provisioning
- **Agent 10 - SecretSynchronizer**: Sync secrets after provisioning

### External Tools
- Ansible playbooks: `/home/fitna/homelab/infrastructure/ansible/playbooks/`
- Host inventory: `/home/fitna/homelab/infrastructure/ansible/inventory/hosts.yml`
- SSH guide: `/home/fitna/homelab/SSH_SETUP_GUIDE.md`

### Data Sources
- Bootstrap playbook: `/home/fitna/homelab/infrastructure/ansible/playbooks/00-bootstrap.yml`
- Infrastructure README: `/home/fitna/homelab/infrastructure/README.md`

## Version
v1.0 - Initial skill definition based on Ansible infrastructure provisioning analysis
