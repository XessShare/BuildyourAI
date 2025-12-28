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

## File Naming Convention

**Format:** `descriptive-name-in-kebab-case.ext`

**Rules:**
1. Use kebab-case (lowercase with hyphens): `landing-page-copy.md` ✅
2. Be descriptive, no abbreviations: `lp-cp.md` ❌
3. Date prefix for versioned content: `2025-12-28-competitor-analysis.md`
4. Extensions: `.md` (docs), `.yml` (config), `.sh` (scripts), `.csv/.json` (data)
