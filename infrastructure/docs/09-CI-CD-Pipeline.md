# CI/CD Pipeline Documentation - Extended with Additional Security Checks

## Overview

The homelab-oss-stack uses a **6-team parallel GitHub Actions workflow** to validate configurations, scan for security issues, and coordinate deployments. This document explains the pipeline structure and how to extend it with custom checks.

## Workflow File Location

- **Main CI file**: `.github/workflows/ci-pre-deploy.yml`
- **Trigger events**:
  - `pull_request` on `main` or `develop` branches (when docker/stacks, ansible, or workflow files change)
  - `push` to `main` branch
  - Manual trigger via `workflow_dispatch`

## Pipeline Architecture (Updated)

### Team 1: Syntax & Config Validation (Critical Path)

**Goal**: Fast feedback on configuration errors

| Job | Duration | Purpose |
|-----|----------|---------|
| `validate-compose` | ~30s | Validate each compose file with `docker compose config` |
| `validate-yaml` | ~30s | Lint YAML syntax with `yamllint` (relaxed mode) |
| `validate-ansible` | ~45s | Check Ansible playbook syntax + run `ansible-lint` |

**Runs in parallel** → Total: ~45s (instead of 2 min sequential)

**Failure handling**: Critical checks that BLOCK deployment if failed

---

### Team 2: Enhanced Security Scanning

**Goal**: Comprehensive vulnerability detection across multiple vectors

| Job | Duration | Purpose | Type |
|-----|----------|---------|------|
| `security-scan-trivy` | ~2-3 min | Filesystem scan (configs, scripts) | Advisory |
| `security-scan-docker-images` | ~2-3 min | Scan Docker images from compose | Advisory |
| `security-scan-dockerfiles` | ~1 min | **NEW**: Dockerfile misconfigurations | Advisory |
| `security-scan-dependencies` | ~2 min | **NEW**: npm/pip/go vulnerabilities | Advisory |
| `security-scan-secrets` | ~1-2 min | **NEW**: Detect hardcoded secrets | Advisory |

All run in parallel → Total: ~5-8 min

---

### Team 3 & 4: Health + Consistency

**Team 3**: Healthcheck simulation (~1 min)  
**Team 4**: Consistency checks (~1 min)

---

## New Security Checks (Step-by-Step)

### Check 1: Dockerfile Scanning (Trivy config scan)

**What it does**: Scans Dockerfiles for security misconfigurations

**Location**: Team 2 - `security-scan-dockerfiles`

**Key features**:
- Auto-detects all `Dockerfile*` files
- Checks for: running as root, missing HEALTHCHECK, outdated base images
- Uploads SARIF to GitHub Security tab
- Non-blocking (advisory only)

**Example findings**:
```
⚠️ HIGH issues found:
  - AVD-DS-0001: User not set to non-root
  - AVD-DS-0002: No HEALTHCHECK defined
```

**To make it FAIL deployments**:
```yaml
security-scan-dockerfiles:
  ...
  steps:
    - uses: aquasecurity/trivy-action@master
      with:
        exit-code: '1'  # Changed from '0' to '1'
```

---

### Check 2: Dependency Scanning (npm/pip/go)

**What it does**: Finds known vulnerabilities in dependencies

**Location**: Team 2 - `security-scan-dependencies`

**Key features**:
- Auto-detects `package.json`, `requirements.txt`, `pyproject.toml`
- Uses Python `safety` tool for pip packages
- Uses Trivy for comprehensive scanning
- Skips node_modules and __pycache__

**Example findings**:
```
ℹ️ Found Python dependency files
🔍 Python dependency scan completed:
  - CVE-2023-1234: requests 2.28.0 (should use >= 2.28.1)
```

**To make it FAIL deployments** (Python):
```yaml
security-scan-dependencies:
  ...
  steps:
    - run: safety check --json > safety-report.json; exit $?
```

---

### Check 3: Secret Detection (TruffleHog)

**What it does**: Detects hardcoded API keys, tokens, and credentials

**Location**: Team 2 - `security-scan-secrets`

**Key features**:
- Scans git history + current files
- Only reports verified secrets (high accuracy)
- Detects: AWS keys, GitHub tokens, private keys, etc.
- Industry-standard secret detector

**Example findings**:
```
🔍 Found potential secrets:
  - AWS API Key in: ansible/vars/prod.yml:42
  - GitHub Token in: .env.backup:15
```

**To make it FAIL deployments** (default behavior):
```yaml
# Already fails on any verified secret (no exit-code param needed)
- uses: trufflesecurity/trufflehog@main
```

---

## How to Customize Security Checks

### Option A: Make a check BLOCKING (fail deployment)

**Example: Dockerfile scanning**

Edit `.github/workflows/ci-pre-deploy.yml`, find `security-scan-dockerfiles` job:

```yaml
security-scan-dockerfiles:
  ...
  steps:
    - uses: aquasecurity/trivy-action@master
      with:
        ...
        exit-code: '1'  # ← Change from '0' to '1'
```

### Option B: Exclude specific paths

**Example: Skip test directories in dependency scan**

Edit `security-scan-dependencies`:

```yaml
- run: |
    trivy fs . --severity HIGH,CRITICAL \
      --skip-dirs tests,docs,examples \
      --output trivy-deps.json
```

### Option B: Exclude specific paths

**Example: Skip test directories in dependency scan**

Edit `security-scan-dependencies`:

```yaml
- run: |
    trivy fs . --severity HIGH,CRITICAL \
      --skip-dirs tests,docs,examples \
      --output trivy-deps.json
```

### Option C: Add allowlists/exceptions

**For TruffleHog** (ignore false positives):

```yaml
security-scan-secrets:
  steps:
    - uses: trufflesecurity/trufflehog@main
      with:
        extra_args: --only-verified --exclude-paths tests/fixtures
```

---

## Template: Add Your Own Security Check

To add a new security job (e.g., Semgrep SAST scanning):

**Step 1**: Add the job under Team 2 (before `healthcheck-simulation`):

```yaml
security-scan-sast:
  name: "SAST: Static Analysis (Semgrep)"
  runs-on: ubuntu-latest
  permissions:
    contents: read
    security-events: write
  steps:
    - uses: actions/checkout@v4
      with:
        fetch-depth: 0

    - name: Run Semgrep SAST scan
      uses: returntocorp/semgrep-action@v1
      with:
        config: >-
          p/owasp-top-ten
          p/security-audit
        generateSarif: true
        sarif_file: semgrep.sarif

    - name: Upload SARIF report
      uses: github/codeql-action/upload-sarif@v2
      with:
        sarif_file: semgrep.sarif
        category: 'semgrep'
```

**Step 2**: Add to `pre-deploy-gate.needs` list:

```yaml
pre-deploy-gate:
  needs:
    - validate-compose
    - validate-yaml
    - validate-ansible
    - security-scan-trivy
    - security-scan-docker-images
    - security-scan-dockerfiles
    - security-scan-dependencies
    - security-scan-secrets
    - security-scan-sast  # ← ADD HERE
    - healthcheck-simulation
    - consistency-check
```

**Step 3**: Update gate status output:

```yaml
- name: Check all jobs status
  run: |
    echo "  ✓ Semgrep SAST: ${{ needs.security-scan-sast.result }}"
```

That's it! The new job will run in parallel with other Team 2 jobs.

---

## Final Gate: pre-deploy-gate

**Purpose**: Aggregate all results; determine if deployment can proceed

**Dependencies**: Requires ALL 10 jobs to complete

**Pass conditions**:
- `validate-compose` = success
- `validate-yaml` = success
- `validate-ansible` = success
- `consistency-check` = success
- Security/health jobs can be `failure` (non-blocking)

**Actions**:
1. Logs status of each job
2. **Comments on PR** with markdown table (if PR event)
3. Sets overall status for branch protection rules

**Example PR comment**:
```
## Pre-Deploy CI Summary

| Check | Result |
|-------|--------|
| Compose Validation | success |
| YAML Linting | success |
| Ansible Syntax | success |
| Trivy Filesystem | failure |
| Docker Images | success |
| Healthcheck Simulation | success |
| Consistency Check | success |
```

### Deployment Job (main branch only)

**Trigger conditions**:
- `github.ref == 'refs/heads/main'`
- `pre-deploy-gate.result == 'success'`

**Actions**:
1. Checks out code
2. Logs deployment metadata (actor, commit SHA, timestamp)
3. **Webhook trigger** (optional, requires `DEPLOY_WEBHOOK_URL` secret)

**To enable production deployments**:
1. Set up webhook receiver (e.g., n8n, custom endpoint)
2. Add GitHub secrets:
   - `DEPLOY_WEBHOOK_URL`: URL to post deployment event
   - `DEPLOY_TOKEN`: Bearer token for webhook auth (optional)
3. Uncomment the `curl` call in the `deploy` job

## Adding New Checks

### Add a Compose File to Validation

1. Edit `.github/workflows/ci-pre-deploy.yml`
2. Under `validate-compose` → `strategy.matrix.compose-file`, add:
```yaml
- docker/stacks/mynewstack.yml
```

### Add a New Security Scanner

1. Create new job under **Team 2** block
2. Use appropriate action (e.g., `aquasecurity/trivy-action@master`)
3. Add to `pre-deploy-gate.needs` list
4. Decide: fail-on-finding or advisory-only?

**Example: Add Dockerfile scanning**:
```yaml
security-scan-dockerfiles:
  name: "Scan Dockerfiles"
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - uses: aquasecurity/trivy-action@master
      with:
        scan-type: 'config'
        scan-ref: 'docker/'
        format: 'sarif'
        output: 'trivy-docker.sarif'
        exit-code: '0'
    - uses: github/codeql-action/upload-sarif@v2
      with:
        sarif_file: 'trivy-docker.sarif'
```

### Enforce Policy on Security Findings

To **fail deployment if vulnerabilities found**:

```yaml
security-scan-trivy:
  ...
  steps:
    ...
    - run: |
        trivy fs --exit-code 1 --severity HIGH,CRITICAL .
```

Then ensure `security-scan-trivy` is in `pre-deploy-gate.needs` with no `continue-on-error`.

## Secrets & Environment Configuration

### Required Secrets (for production deployment)

1. Go to **GitHub** → **Settings** → **Secrets and variables** → **Actions**
2. Add:

| Secret | Purpose | Example |
|--------|---------|---------|
| `DEPLOY_WEBHOOK_URL` | Endpoint to trigger deployment | `https://n8n.example.com/webhook/deploy` |
| `DEPLOY_TOKEN` | Bearer token for auth | `Bearer <secret-token>` |

### Using Secrets in Workflow

```yaml
- name: Trigger deployment
  run: |
    curl -X POST ${{ secrets.DEPLOY_WEBHOOK_URL }} \
      -H "Authorization: ${{ secrets.DEPLOY_TOKEN }}" \
      -H "Content-Type: application/json" \
      -d '{"sha":"${{ github.sha }}"}'
```

## Concurrency & Cancellation

The workflow uses concurrency groups to cancel previous runs:

```yaml
concurrency:
  group: ci-${{ github.ref }}
  cancel-in-progress: true
```

**Effect**: If you push a new commit to a PR before the previous run finishes, the old run is cancelled.

## Performance Tuning

### Current Timings (approximate)
- **Team 1** (validation): ~45s (parallel)
- **Team 2** (security): ~3-5 min (parallel, ~3 min longest)
- **Team 3** (health): ~1 min
- **Team 4** (consistency): ~1 min
- **Total**: ~6-7 min (all teams parallel)

### To Reduce Execution Time

1. **Reduce Trivy scope**:
   ```yaml
   # Only scan critical paths
   scan-ref: 'docker/stacks/ ansible/'
   ```

2. **Cache Docker layers**:
   ```yaml
   - uses: docker/setup-buildx-action@v3
     with:
       cache-from: type=registry,ref=ghcr.io/...
   ```

3. **Limit image scanning**:
   ```yaml
   # Only scan latest tag, not all variants
   --tag latest
   ```

## Debugging Failed Workflows

### View logs in GitHub
1. Go to **Actions** tab
2. Click the workflow run
3. Click the failed job
4. Expand the step to see full output

### Common Failures

**"docker compose config failed"**
- Check compose file syntax (indentation, missing colons)
- Run locally: `docker compose -f docker/stacks/core.yml config`

**"Trivy scan failed: image not found"**
- Image may not exist or be private
- Add `--allow-misspelled-repo-name` if needed

**"ansible-lint: too many warnings"**
- Review `.ansible-lint` config file (if exists)
- Or suppress specific warnings: `# noqa: E501`

### Manual Re-run

1. Go to **Actions** → workflow run
2. Click **Re-run failed jobs** or **Re-run all jobs**

## Branch Protection Rules

To enforce CI checks before merge:

1. **Settings** → **Branches** → **Branch protection rules** → **main**
2. Enable:
   - "Require status checks to pass before merging"
   - Select `pre-deploy-gate` as required check
3. (Optional) Require PR review + up-to-date branch

## Workflow Triggers (Optional Customization)

Current triggers:
```yaml
on:
  pull_request:
    branches: [main, develop]
    paths:
      - 'docker/stacks/**'
      - 'ansible/**'
      - '.github/workflows/**'
```

To add more triggers:
```yaml
  push:
    branches: [release/*]
  schedule:
    - cron: '0 2 * * 0'  # Weekly security scan
  workflow_dispatch:  # Manual trigger
```

## Next Steps

- [ ] Add `.ansible-lint` config file (if not present)
- [ ] Configure GitHub branch protection rules
- [ ] Set up deployment webhook endpoint
- [ ] Add `DEPLOY_WEBHOOK_URL` and `DEPLOY_TOKEN` secrets
- [ ] Test workflow on a feature branch (PR)
- [ ] Review CI logs and adjust fail conditions as needed

---

**Questions?** Check `.# curl -X POST ${{ secrets.DEPLOY_WEBHOOK_URL }} \ ← remove `#`` for inline comments and examples.
