# GitHub Actions Setup Guide - Design Spec Auto-Update

**Purpose:** Automate weekly design spec regeneration using Claude & Gemini
**Workflow File:** `.github/workflows/design-spec-update.yml`
**Status:** ✅ Updated (now generates all 5 specs)

---

## Prerequisites

You need API keys from:
1. **Anthropic** (for Claude Sonnet 4.5) - Landing Page, Web-App, Design System
2. **Google AI** (for Gemini 2.0 Flash) - iOS, Android

---

## Step 1: Get API Keys

### Anthropic API Key (Claude)

1. **Sign in to Anthropic Console:**
   - URL: https://console.anthropic.com
   - Use your existing Anthropic account

2. **Create API Key:**
   - Navigate to: Settings → API Keys
   - Click "Create Key"
   - Name: `GitHub Actions - Design Specs`
   - Copy the key (starts with `sk-ant-...`)
   - ⚠️ **Save immediately** - shown only once

3. **Verify Credit Balance:**
   - Check: Settings → Billing
   - Ensure you have >$5 credits (weekly runs cost ~$0.17)

---

### Google AI API Key (Gemini)

1. **Sign in to Google AI Studio:**
   - URL: https://aistudio.google.com/apikey
   - Use your Google account

2. **Create API Key:**
   - Click "Create API Key"
   - Select project or create new: "HexaHub Design Automation"
   - Copy the key (starts with `AIza...`)
   - ⚠️ **Save immediately**

3. **Verify API Access:**
   - Test URL: https://aistudio.google.com/
   - Ensure Gemini 2.0 Flash is available (experimental model)
   - Free tier: 15 requests/min, 1500 requests/day (sufficient for weekly runs)

---

## Step 2: Add Secrets to GitHub Repository

### Method 1: GitHub Web UI (Recommended)

1. **Navigate to Repository Settings:**
   ```
   https://github.com/fitna/homelab/settings/secrets/actions
   ```
   - Or: Repository → Settings → Secrets and variables → Actions

2. **Add ANTHROPIC_API_KEY:**
   - Click "New repository secret"
   - Name: `ANTHROPIC_API_KEY`
   - Value: Paste your Anthropic key (sk-ant-...)
   - Click "Add secret"

3. **Add GOOGLE_API_KEY:**
   - Click "New repository secret"
   - Name: `GOOGLE_API_KEY`
   - Value: Paste your Google AI key (AIza...)
   - Click "Add secret"

4. **Verify Secrets Added:**
   - You should see:
     - ✅ `ANTHROPIC_API_KEY` (added X minutes ago)
     - ✅ `GOOGLE_API_KEY` (added X minutes ago)

---

### Method 2: GitHub CLI (Alternative)

If you have `gh` CLI installed:

```bash
# Add Anthropic API Key
gh secret set ANTHROPIC_API_KEY --body "sk-ant-YOUR_KEY_HERE"

# Add Google API Key
gh secret set GOOGLE_API_KEY --body "AIzaYOUR_KEY_HERE"

# List secrets to verify
gh secret list
```

---

## Step 3: Verify Workflow Configuration

### Check Workflow File

```bash
# Verify workflow exists
ls -la /home/fitna/homelab/.github/workflows/design-spec-update.yml

# Check workflow is valid YAML
python3 -c "import yaml; yaml.safe_load(open('.github/workflows/design-spec-update.yml'))"
```

**Expected Output:** No errors (silent success)

### Review Trigger Configuration

The workflow runs on:
- **Weekly:** Every Monday at 9 AM UTC
- **Manual:** Via GitHub UI (Actions → Design Spec Auto-Update → Run workflow)
- **Auto:** When design research or context files change

---

## Step 4: Test Workflow (Manual Trigger)

### Option A: GitHub Web UI (Easiest)

1. **Navigate to Actions Tab:**
   ```
   https://github.com/fitna/homelab/actions
   ```

2. **Select Workflow:**
   - Click "Design Spec Auto-Update" (left sidebar)

3. **Manual Trigger:**
   - Click "Run workflow" (top-right)
   - Branch: `sprint-26/multi-agent-prompt-optimization` (or current branch)
   - Click green "Run workflow" button

4. **Monitor Execution:**
   - Workflow appears in list (status: 🟡 Running)
   - Click on run to see live logs
   - Expected duration: 3-5 minutes (5 specs × ~45s each)

5. **Check Results:**
   - ✅ Success: All steps green, PR created
   - ❌ Failure: Check logs, verify API keys

---

### Option B: GitHub CLI (Alternative)

```bash
# Trigger workflow manually
gh workflow run "Design Spec Auto-Update"

# Monitor workflow status
gh run list --workflow=design-spec-update.yml

# View logs of latest run
gh run view --log
```

---

## Step 5: Verify PR Creation

After successful workflow run:

1. **Check Pull Requests:**
   ```
   https://github.com/fitna/homelab/pulls
   ```

2. **Expected PR:**
   - Title: "🤖 Design Spec Auto-Update (Week X)"
   - Labels: `design`, `automated`, `sprint-26`
   - Branch: `design-spec-update-week-X`
   - Base: `master`

3. **Review PR Contents:**
   - Changes tab shows 5 files modified:
     - `sprints/sprint-26/design-specs/landing-page-spec.md`
     - `sprints/sprint-26/design-specs/webapp-dashboard-spec.md`
     - `sprints/sprint-26/design-specs/design-system-foundations.md`
     - `sprints/sprint-26/design-specs/ios-app-spec.md`
     - `sprints/sprint-26/design-specs/android-app-spec.md`

4. **Review Checklist (in PR description):**
   - [ ] All 5 specs align with brand guidelines (no buzzwords)
   - [ ] Competitor differentiation included
   - [ ] Mobile-responsive notes present (iOS, Android)
   - [ ] Conversion optimization notes present (Landing Page)
   - [ ] Component library references present (Web-App, Design System)

5. **Merge PR (if quality is good):**
   - Review diffs (compare old vs new specs)
   - Approve if no issues
   - Merge to update production specs

---

## Troubleshooting

### Issue 1: Workflow Fails with "ANTHROPIC_API_KEY not found"

**Cause:** Secret not set or named incorrectly

**Fix:**
1. Go to: Repository → Settings → Secrets and variables → Actions
2. Verify secret name is exactly `ANTHROPIC_API_KEY` (case-sensitive)
3. If missing, add it (Step 2)
4. Re-run workflow

---

### Issue 2: Workflow Fails with "Rate limit exceeded" (Gemini)

**Cause:** Free tier limit (15 requests/min, 1500 requests/day)

**Fix:**
1. Wait 1 minute, re-run workflow
2. If persistent, upgrade to Gemini paid tier ($0.10 per 1M tokens)
3. Or: Reduce weekly runs frequency (monthly instead)

---

### Issue 3: Workflow Succeeds but No PR Created

**Cause:** No changes detected (specs identical to previous run)

**Expected Behavior:** Workflow only creates PR if specs changed

**Verify:**
- Check workflow logs: "Check for changes" step
- Output: `changes=true` (PR created) or silent (no PR)

**If you want to force PR creation:**
- Manually edit `DESIGN_CONTEXT.md` (add comment)
- Re-run workflow (will detect change, regenerate specs)

---

### Issue 4: Claude Model Error "claude-sonnet-4-20250514 not found"

**Cause:** Model ID outdated or deprecated

**Fix:**
1. Check latest model ID: https://docs.anthropic.com/en/docs/models-overview
2. Update workflow file (replace model ID in 3 places):
   ```bash
   # Find and replace
   sed -i 's/claude-sonnet-4-20250514/claude-sonnet-4-20250929/g' .github/workflows/design-spec-update.yml
   ```
3. Commit change, re-run workflow

---

### Issue 5: PR Created but Files Not Changed

**Cause:** Prompt extraction failed (```  block parsing issue)

**Verify Prompt Format:**
```bash
# Check prompt files have correct structure
grep -A 5 "^## Prompt" sprints/sprint-26/prompt-library/*-v2.md
```

**Expected:** Each prompt has `## Prompt` section followed by ``` code block

**Fix:** Ensure prompts follow format (see `landing-page-prompt-v2.md` as reference)

---

## Maintenance

### Weekly Monitoring (Recommended)

1. **Check Workflow Runs:**
   - URL: https://github.com/fitna/homelab/actions
   - Filter: "Design Spec Auto-Update"
   - Verify: Last run succeeded (green checkmark)

2. **Review Auto-Generated PRs:**
   - Check: Are specs improving over time?
   - Merge: PRs that pass quality review
   - Close: PRs with no meaningful changes

3. **Monitor API Costs:**
   - Anthropic: https://console.anthropic.com/settings/billing
   - Google AI: https://aistudio.google.com/ (free tier, no billing)
   - Expected: ~$0.17/week for Claude (Gemini is free)

---

### Update Prompts (When Needed)

If specs quality degrades or requirements change:

1. **Edit Prompt Files:**
   - Update: `sprints/sprint-26/prompt-library/*-v2.md`
   - Test manually first (Google AI Studio or ContentCreatorAgent)

2. **Commit Changes:**
   ```bash
   git add sprints/sprint-26/prompt-library/
   git commit -m "refactor: Update design prompts (v2.1)"
   git push
   ```

3. **Re-run Workflow:**
   - Trigger manually (GitHub Actions → Run workflow)
   - Verify: New PRs use updated prompts

---

### Disable/Pause Workflow (If Needed)

To stop weekly runs without deleting workflow:

1. **Edit Workflow File:**
   ```bash
   # Comment out schedule trigger
   sed -i 's/  schedule:/#  schedule:/g' .github/workflows/design-spec-update.yml
   sed -i 's/    - cron:/#    - cron:/g' .github/workflows/design-spec-update.yml
   ```

2. **Commit Change:**
   ```bash
   git add .github/workflows/design-spec-update.yml
   git commit -m "chore: Pause weekly design spec updates"
   git push
   ```

3. **Re-enable Later:**
   - Uncomment schedule lines
   - Commit and push

---

## Cost Analysis

### Claude Sonnet 4.5 (3 specs)

**Per Run:**
- Input: ~3,050 tokens (prompts + context)
- Output: ~12,060 tokens (3 specs × ~140 lines)
- Cost: $0.009 input + $0.181 output = **$0.19 per run**

**Monthly (4 runs):** ~$0.76
**Yearly (52 runs):** ~$9.88

---

### Gemini 2.0 Flash (2 specs)

**Per Run:**
- Input: ~2,350 tokens
- Output: ~8,000 tokens
- Cost: **$0.00** (free tier covers 1500 requests/day)

**Monthly:** $0.00
**Yearly:** $0.00

---

### Total Cost

**Weekly:** $0.19 (Claude only)
**Monthly:** $0.76
**Yearly:** $9.88

**ROI:**
- Manual regeneration: ~2 hours/week = 104 hours/year
- Automated: ~5 minutes review/week = 4.3 hours/year
- **Time Saved:** 100 hours/year (~$15,000 value at $150/hr developer rate)
- **Net Savings:** $14,990 (after $10 API cost)

---

## Next Steps

After setup is complete:

1. **✅ Verify First Run:**
   - Manual trigger workflow
   - Review PR quality
   - Merge if good

2. **📅 Set Calendar Reminder:**
   - Every Monday 10 AM (1 hour after workflow runs)
   - Review and merge PR (5-10 min task)

3. **🔄 Iterate:**
   - Monitor spec quality over 4 weeks
   - Update prompts if needed (v2.1, v2.2, etc.)
   - Add more specs (e.g., API docs, Deployment guide)

4. **📊 Track Metrics:**
   - Document in: `PROMPT_OPTIMIZATION_REPORT.md`
   - Quality scores per week
   - Token usage trends
   - Manual intervention frequency

---

**Setup Guide Version:** 1.0
**Last Updated:** 2025-12-30
**Author:** Fitna + Claude Sonnet 4.5
**Status:** ✅ Ready for implementation
