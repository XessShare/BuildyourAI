# Sprint 26 - Agent Delegation Prompts

**Sprint:** 26 (2025-12-28 to 2026-01-11)
**Goal:** Foundation Setup for HexaHub MVP
**Total Agent Tasks:** 24 across 6 agents
**Expected Hours Saved:** ~45 hours

---

## 📊 Agent Overview

| Agent | Priority | Tasks | Story Points | Deadline | Status |
|-------|----------|-------|--------------|----------|--------|
| **ContentCreatorAgent** | HIGH | 4 | 3.0 | Tag 3 (Dec 30) | 🟡 Pending |
| **ResearcherAgent** | HIGH | 4 | 3.5 | Tag 2 (Dec 29) | 🟡 Pending |
| **AnalystAgent** | MEDIUM | 4 | 2.0 | Daily | 🟡 Pending |
| **DeploymentOrchestrator** | HIGH | 4 | 6.0 | Tag 5 (Dec 31) | 🟡 Pending |
| **VerifierAgent** | CONTINUOUS | 4 | 2.0 | Continuous | 🟡 Pending |
| **ProjectManagerAgent** | MEDIUM | 4 | 1.5 | Daily | 🟡 Pending |

**Total:** 24 tasks, 18.0 Story Points

---

## 🚀 Quick Start

### 1. ContentCreatorAgent
**Focus:** Landing page copy, YouTube script, social media templates, newsletter setup

```bash
# Read the prompt
cat /home/fitna/homelab/sprints/sprint-26/agent-prompts/ContentCreatorAgent.md

# Execute with Claude/GPT-4
# Copy the "Agent Prompt" section and paste into your AI tool
# Output goes to: /home/fitna/homelab/shared/content/sprint-26/
```

**Deliverables:**
- `landing-page-copy.md`
- `youtube-script-01-hexahub-intro.md`
- `social-media-templates.csv`
- `newsletter-setup-guide.md`

---

### 2. ResearcherAgent
**Focus:** Competitor analysis, beta communities, trending topics, market research

```bash
# Read the prompt
cat /home/fitna/homelab/sprints/sprint-26/agent-prompts/ResearcherAgent.md

# Execute with Claude Opus/Perplexity
# Output goes to: /home/fitna/homelab/shared/research/sprint-26/
```

**Deliverables:**
- `competitor-analysis.md`
- `beta-communities.csv`
- `influencers.csv`
- `outreach-strategy.md`
- `trending-topics-report.md`
- `market-research-report.md`

---

### 3. DeploymentOrchestrator
**Focus:** CI/CD pipeline, staging environment, monitoring, K3s prep

```bash
# Read the prompt
cat /home/fitna/homelab/sprints/sprint-26/agent-prompts/DeploymentOrchestrator.md

# Execute (mix of automated + human oversight)
# Output goes to: /home/fitna/homelab/infrastructure/
```

**Deliverables:**
- `.github/workflows/hexahub-ci-cd.yml`
- `infrastructure/docker-compose.staging.yml`
- `infrastructure/monitoring/prometheus.yml`
- `infrastructure/k8s/hexahub-chart/`
- Multiple setup scripts and documentation

---

### 4. AnalystAgent
**Focus:** Roadmap tracker, metrics dashboard, KPI baseline, daily tracking

**Tasks:**
1. Initialize roadmap tracker dashboard
2. Setup Grafana sprint metrics
3. Define baseline KPIs (MRR=0, Customers=0, Velocity=21 SP)
4. Daily progress tracking automation

**Output:** `shared/dashboards/`

---

### 5. VerifierAgent
**Focus:** Testing, CodeRabbit integration, QA checklists, security scanning

**Tasks:**
1. Pytest baseline for existing services
2. CodeRabbit integration (active via GitHub)
3. QA checklist for MVP (API, Auth flow)
4. Security scan (dependencies, vulnerabilities)

**Output:** Continuous integration

---

### 6. ProjectManagerAgent
**Focus:** Sprint planning, standup automation, board updates, blocker tracking

**Tasks:**
1. Sprint planning completion (✅ Done)
2. Daily standup automation setup
3. Kanban board updates (SPRINT_BOARD.md)
4. Blocker tracking system

**Output:** `sprints/sprint-26/`

---

## 📋 Execution Workflow

### Day 1 (2025-12-28) - ✅ DONE
- [x] Sprint 26 initialized
- [x] Sprint plan created
- [x] Git repository organized
- [x] Agent prompts created
- [x] Daily tracking activated

### Day 2-3 (2025-12-29 to 2025-12-30)
**Priority: Research + Content**
1. Launch ResearcherAgent tasks (Deadline: Tag 2)
2. Launch ContentCreatorAgent tasks (Deadline: Tag 3)
3. AnalystAgent: Initialize dashboards

### Day 4-5 (2025-12-31 to 2026-01-01)
**Priority: Infrastructure**
1. DeploymentOrchestrator: CI/CD setup
2. DeploymentOrchestrator: Staging environment
3. VerifierAgent: Testing baseline

### Day 6-7 (2026-01-02 to 2026-01-03)
**Priority: Monitoring + Integration**
1. DeploymentOrchestrator: Monitoring stack
2. VerifierAgent: QA checklists
3. ProjectManagerAgent: Sprint review prep

### Week 2 (Day 8-14)
**Priority: Completion + Sprint Review**
- Finish remaining tasks
- Testing & QA
- Sprint retrospective
- Plan Sprint 27

---

## 📂 Directory Structure

```
/home/fitna/homelab/
├── sprints/sprint-26/
│   ├── SPRINT_PLAN.md
│   ├── SPRINT_BOARD.md
│   └── agent-prompts/          ← You are here
│       ├── README.md            ← This file
│       ├── ContentCreatorAgent.md
│       ├── ResearcherAgent.md
│       ├── DeploymentOrchestrator.md
│       └── [More agents TBD]
├── shared/
│   ├── content/sprint-26/      ← ContentCreatorAgent output
│   ├── research/sprint-26/     ← ResearcherAgent output
│   └── dashboards/             ← AnalystAgent output
└── infrastructure/             ← DeploymentOrchestrator output
```

---

## 🎯 Success Criteria

**Sprint 26 is successful when:**
- ✅ All 24 agent tasks completed
- ✅ 18-21 Story Points done
- ✅ HexaHub backend scaffolding deployed to staging
- ✅ CI/CD pipeline automated
- ✅ Content ready for launch (landing page, YT script)
- ✅ 100 beta user communities identified
- ✅ Monitoring dashboards live

---

## 💡 Tips for Working with Agents

1. **Copy-paste the full prompt** from each agent file
2. **Provide context** (link to roadmap, sprint plan)
3. **Iterate on output** - agents learn from feedback
4. **Save outputs** in the designated directories
5. **Track completion** - update SPRINT_BOARD.md

---

## 🔗 Related Documents

- [Sprint 26 Plan](../SPRINT_PLAN.md)
- [Sprint 26 Board](../SPRINT_BOARD.md)
- [1M€ Roadmap](/home/fitna/homelab/ROADMAP_1M_18MONTHS.md)
- [Execution Plan](/home/fitna/.claude/plans/melodic-wobbling-volcano.md)

---

**Created:** 2025-12-28
**Status:** Ready for Execution
**Next Action:** Launch ResearcherAgent (Tag 2 deadline)
