# Task 4: Output File Structure

**Agent:** AnalystAgent
**Model:** GPT-4o-mini (Structural Analysis)
**Output:** `/home/fitna/homelab/sprints/sprint-26/shared-context/output-structure.md`
**Length:** 20 lines

---

## Mission

Define the standardized output directory structure and file naming conventions for all Sprint 26 agent deliverables.

---

## Input Data

**Source:** `/home/fitna/homelab/sprints/sprint-26/agent-prompts/README.md`
- ContentCreatorAgent output: `/home/fitna/homelab/shared/content/sprint-26/`
- ResearcherAgent output: `/home/fitna/homelab/shared/research/sprint-26/`
- DeploymentOrchestrator output: `/home/fitna/homelab/infrastructure/`
- AnalystAgent output: `/home/fitna/homelab/shared/dashboards/`

---

## Output Structure (20 lines)

```markdown
# Sprint 26 Output File Structure

## Directory Mapping

**Content Files** (ContentCreatorAgent):
- Base: `/home/fitna/homelab/shared/content/sprint-26/`
- Examples: `landing-page-copy.md`, `youtube-script-01-hexahub-intro.md`

**Research Files** (ResearcherAgent):
- Base: `/home/fitna/homelab/shared/research/sprint-26/`
- Examples: `competitor-analysis.md`, `beta-communities.csv`

**Infrastructure Files** (DeploymentOrchestrator):
- Base: `/home/fitna/homelab/infrastructure/`
- Examples: `.github/workflows/hexahub-ci-cd.yml`, `docker-compose.staging.yml`

**Dashboard Files** (AnalystAgent):
- Base: `/home/fitna/homelab/shared/dashboards/`
- Examples: `1m-roadmap-tracker.md`, `sprint-26-metrics.json`

**Sprint Files** (ProjectManagerAgent):
- Base: `/home/fitna/homelab/sprints/sprint-26/`
- Examples: `SPRINT_BOARD.md`, `daily-standup-2025-12-29.md`

## File Naming Convention

**Format:** `descriptive-name-in-kebab-case.ext`

**Rules:**
1. Use kebab-case (lowercase with hyphens): `landing-page-copy.md` ✅
2. Be descriptive, no abbreviations: `lp-cp.md` ❌
3. Date prefix for versioned content: `2025-12-28-competitor-analysis.md`
4. Consistent extensions:
   - Documentation: `.md` (Markdown)
   - Configuration: `.yml` or `.yaml`
   - Scripts: `.sh` (Bash), `.py` (Python)
   - Data: `.csv`, `.json`

**Examples:**
- ✅ `landing-page-copy.md`
- ✅ `youtube-script-01-hexahub-intro.md`
- ✅ `2025-12-28-competitor-analysis.md`
- ❌ `LP.md` (abbreviation)
- ❌ `LandingPageCopy.md` (PascalCase)
- ❌ `landing_page_copy.md` (snake_case)
```

---

## Success Criteria

- [ ] 20 lines exactly (±2 lines acceptable)
- [ ] All directory paths accurate
- [ ] Clear naming convention rules
- [ ] Good examples (✅) and bad examples (❌)
- [ ] Ready to be included in 24 agent prompts

---

## Execution Prompt (For GPT-4o-mini)

```
You are AnalystAgent defining the output file structure for Sprint 26.

Your mission: Create a standardized output structure document (20 lines).

Define:
1. Directory mapping for each agent type:
   - ContentCreatorAgent → /home/fitna/homelab/shared/content/sprint-26/
   - ResearcherAgent → /home/fitna/homelab/shared/research/sprint-26/
   - DeploymentOrchestrator → /home/fitna/homelab/infrastructure/
   - AnalystAgent → /home/fitna/homelab/shared/dashboards/
   - ProjectManagerAgent → /home/fitna/homelab/sprints/sprint-26/

2. File naming convention:
   - kebab-case (lowercase with hyphens)
   - Descriptive names
   - Date prefix for versioned content
   - Consistent extensions (.md, .yml, .sh, .csv, .json)

3. Examples (good ✅ and bad ❌)

Output format: Use the structure template above.
Length: 20 lines (strict).

Write the complete output-structure.md file now. Be concise and clear.
```
