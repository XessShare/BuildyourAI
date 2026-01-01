# Skill: Sprint Manager

## Name
**Sprint Manager** - Automated Agile Sprint Planning and Tracking

## Description
This skill automates the complete 2-week agile sprint lifecycle for the homelab project, including sprint initialization, multi-agent task allocation, progress tracking, and reporting. The skill follows the established sprint management workflow from `/home/fitna/homelab/sprints/sprint-26/` and uses the automated sprint-manager.sh script.

## When to Use This Skill

### Trigger Conditions
Use this skill when the user requests ANY of the following:
- "Create a new sprint plan"
- "Start sprint [number]"
- "Initialize sprint planning for [project/goal]"
- "Set up the next 2-week sprint"
- "Allocate tasks to agents for the upcoming sprint"
- "Generate a sprint board"
- "Update sprint progress"
- "Track sprint burndown"

### Context Indicators
- User mentions sprint numbers (e.g., "Sprint 27", "next sprint")
- User discusses 2-week planning cycles
- User wants to allocate work to multiple agents
- User needs task tracking with story points
- User mentions "burndown chart" or "velocity"

## Process Steps

### Phase 1: Sprint Initialization (5-10 minutes)

1. **Gather Sprint Information**
   - Sprint number (e.g., 27)
   - Sprint goals (2-3 high-level objectives)
   - Start date and end date (2-week cycle)
   - Available agents (default: ContentCreator, Researcher, Analyst, DeploymentOrchestrator, Verifier, ProjectManager)
   - Total story points baseline (default: 21 SP)

2. **Create Sprint Directory Structure**
   ```bash
   mkdir -p /home/fitna/homelab/sprints/sprint-{NUMBER}
   mkdir -p /home/fitna/homelab/sprints/sprint-{NUMBER}/agent-prompts
   mkdir -p /home/fitna/homelab/sprints/sprint-{NUMBER}/shared-context
   ```

3. **Generate SPRINT_PLAN.md**
   Use template from `/home/fitna/homelab/sprints/sprint-26/SPRINT_PLAN.md`:

   **Required Sections:**
   - **Sprint Header**: Sprint number, dates, goals
   - **Team Capacity**: Agent list with roles and capacity
   - **Task Breakdown**:
     - Agent name
     - Priority (HIGH/MEDIUM/LOW/CONTINUOUS)
     - Number of tasks
     - Story points estimate
     - Task descriptions (numbered list)
   - **Total Story Points**: Sum across all agents
   - **Success Criteria**: Measurable outcomes (checkboxes)
   - **Dependencies**: Cross-agent dependencies
   - **Risks & Mitigation**: Known blockers and solutions

4. **Generate SPRINT_BOARD.md**
   Use Kanban board template:

   **Columns:**
   - **Backlog** (tasks not started)
   - **In Progress** (active work, limit WIP)
   - **Testing/Review** (completed but under verification)
   - **Done** (fully completed)

   **Task Format:**
   ```markdown
   - [ ] [AGENT_NAME] Task description (X SP) | Priority: Y | Owner: Z
   ```

5. **Create Shared Context Files**
   Copy from `/home/fitna/homelab/sprints/sprint-26/shared-context/`:
   - `project-context.md` - Homelab architecture and goals
   - `sprint-context.md` - Current sprint objectives and constraints
   - `brand-guidelines.md` - Brand voice and style
   - `output-structure.md` - Deliverable formatting standards

### Phase 2: Agent Task Allocation (10-15 minutes)

6. **Allocate Tasks by Agent Type**

   **ContentCreatorAgent** (Priority: HIGH):
   - Landing page copy
   - Video scripts
   - Social media content
   - Newsletter templates
   - Output: `/home/fitna/homelab/shared/content/sprint-{NUMBER}/`

   **ResearcherAgent** (Priority: HIGH):
   - Competitor analysis
   - Market research
   - Trend analysis
   - Community research
   - Output: `/home/fitna/homelab/shared/research/sprint-{NUMBER}/`

   **AnalystAgent** (Priority: MEDIUM):
   - Roadmap tracking
   - KPI dashboards
   - Metrics analysis
   - Daily tracking setup
   - Output: `/home/fitna/homelab/shared/dashboards/`

   **DeploymentOrchestrator** (Priority: HIGH):
   - CI/CD pipeline setup
   - Infrastructure deployment
   - Monitoring configuration
   - K3s preparation
   - Output: `/home/fitna/homelab/infrastructure/`

   **VerifierAgent** (Priority: CONTINUOUS):
   - Testing framework
   - CodeRabbit integration
   - QA checklists
   - Security scanning
   - Output: Continuous validation

   **ProjectManagerAgent** (Priority: MEDIUM):
   - Sprint planning
   - Standup automation
   - Board updates
   - Blocker tracking
   - Output: `/home/fitna/homelab/sprints/sprint-{NUMBER}/`

7. **Calculate Story Points**
   - Use Fibonacci sequence: 1, 2, 3, 5, 8, 13
   - Consider complexity, uncertainty, effort
   - Sum total should match team velocity (baseline: 21 SP)

8. **Define Success Criteria**
   Create measurable checkboxes:
   - [ ] All HIGH priority tasks completed (80%+ of SP)
   - [ ] No critical blockers remaining
   - [ ] Code review completed for all deliverables
   - [ ] Documentation updated
   - [ ] Deployment validated in staging

### Phase 3: Sprint Tracking (Daily, 2 weeks)

9. **Daily Standup Automation**
   Run: `/home/fitna/homelab/shared/scripts/sprint-manager.sh standup sprint-{NUMBER}`

   **Output Format:**
   ```markdown
   # Daily Standup - Sprint {NUMBER} - Day {X}/10

   ## Yesterday's Completed Tasks
   - [Agent] Task description (X SP) ✅

   ## Today's Plan
   - [Agent] Task description (X SP) 🔄

   ## Blockers
   - [Agent] Blocker description 🚧

   ## Burndown
   Total SP: 21 | Completed: X | Remaining: Y | Days Left: Z
   Progress: [████░░░░░░] X%
   ```

10. **Update SPRINT_BOARD.md**
    - Move completed tasks to "Done"
    - Update task checkboxes: `- [ ]` → `- [x]`
    - Add new tasks to "Backlog" if scope changes
    - Flag blockers with 🚧 emoji

11. **Track Burndown**
    Update progress daily:
    ```markdown
    ## Sprint Burndown Chart (Text-based)

    Day 1:  [████████████████████] 21 SP
    Day 2:  [██████████████████░░] 19 SP
    Day 3:  [████████████████░░░░] 17 SP
    Day 4:  [██████████████░░░░░░] 15 SP
    Day 5:  [████████████░░░░░░░░] 13 SP
    Day 6:  [██████████░░░░░░░░░░] 11 SP
    Day 7:  [████████░░░░░░░░░░░░] 9 SP
    Day 8:  [██████░░░░░░░░░░░░░░] 7 SP
    Day 9:  [████░░░░░░░░░░░░░░░░] 5 SP
    Day 10: [██░░░░░░░░░░░░░░░░░░] 3 SP
    ```

### Phase 4: Sprint Review & Retrospective (End of Sprint)

12. **Generate Sprint Review Report**
    Run: `/home/fitna/homelab/shared/scripts/sprint-manager.sh review sprint-{NUMBER}`

    **Include:**
    - Completed tasks vs. planned (%)
    - Story points delivered vs. committed
    - Velocity trend (compare to previous sprints)
    - Key achievements (bullet points)
    - Incomplete tasks and reasons
    - Stakeholder feedback

13. **Conduct Sprint Retrospective**
    Create `RETROSPECTIVE.md`:

    **Sections:**
    - **What Went Well** 🟢
      - List successes and positive patterns
    - **What Didn't Go Well** 🔴
      - List challenges and blockers
    - **Action Items** 🎯
      - Concrete improvements for next sprint
      - Assign owners and deadlines
    - **Velocity Analysis**
      - Actual velocity vs. planned
      - Adjust baseline for next sprint

14. **Archive Sprint Artifacts**
    ```bash
    # Create archive directory
    mkdir -p /home/fitna/homelab/sprints/archive/sprint-{NUMBER}

    # Copy final state
    cp -r /home/fitna/homelab/sprints/sprint-{NUMBER}/* \
          /home/fitna/homelab/sprints/archive/sprint-{NUMBER}/
    ```

## Rules and Constraints

### Hard Rules (Must Follow)
1. **Sprint duration is ALWAYS 2 weeks (10 working days)**
2. **Total story points must be realistic** (baseline: 21 SP, adjust based on velocity)
3. **Every task MUST have an owner** (agent or human)
4. **HIGH priority tasks MUST be completed** before MEDIUM/LOW
5. **All deliverables MUST have exact file paths** in agent prompts
6. **Success criteria MUST be measurable** (no vague statements)
7. **Dependencies MUST be identified upfront** to avoid blockers
8. **Daily updates are MANDATORY** (use sprint-manager.sh)

### Soft Rules (Best Practices)
- Limit work-in-progress (WIP) to 3 tasks per agent
- Break down tasks >5 SP into smaller tasks
- Reserve 20% capacity for unplanned work
- Include at least one learning/improvement task per sprint
- Document all decisions in sprint notes
- Celebrate wins in sprint review

### Quality Gates
Before marking a task as "Done":
- [ ] Code review completed (CodeRabbit or peer)
- [ ] Tests passing (unit, integration, E2E)
- [ ] Documentation updated
- [ ] Deployed to staging (if applicable)
- [ ] Acceptance criteria met (all checkboxes)

## Expected Outputs

### Deliverables
1. **SPRINT_PLAN.md** - Complete sprint plan with agent allocation
2. **SPRINT_BOARD.md** - Kanban board for task tracking
3. **shared-context/** - 4 shared context files for agent prompts
4. **agent-prompts/** - Individual agent task prompts (optional)
5. **Daily standup reports** - Auto-generated via script
6. **RETROSPECTIVE.md** - End-of-sprint learnings

### File Structure
```
/home/fitna/homelab/sprints/sprint-{NUMBER}/
├── SPRINT_PLAN.md
├── SPRINT_BOARD.md
├── RETROSPECTIVE.md (end of sprint)
├── shared-context/
│   ├── project-context.md
│   ├── sprint-context.md
│   ├── brand-guidelines.md
│   └── output-structure.md
├── agent-prompts/
│   ├── ContentCreatorAgent.md
│   ├── ResearcherAgent.md
│   ├── AnalystAgent.md
│   ├── DeploymentOrchestrator.md
│   ├── VerifierAgent.md
│   └── ProjectManagerAgent.md
└── daily-reports/
    ├── day-01-standup.md
    ├── day-02-standup.md
    └── ...
```

### Success Metrics
- ✅ Sprint plan completed within 10 minutes
- ✅ All agents have clear, actionable tasks
- ✅ Story points balanced across agents (no single bottleneck)
- ✅ Daily standups generated automatically
- ✅ 80%+ of committed story points delivered
- ✅ Velocity tracked for continuous improvement

## Error Handling

### Common Issues & Solutions

**Issue: User doesn't provide sprint goals**
- **Solution**: Ask clarifying questions about objectives
- **Fallback**: Use previous sprint goals as template

**Issue: Story points exceed team capacity**
- **Solution**: Prioritize tasks, move LOW priority to backlog
- **Warning**: Flag capacity mismatch to user

**Issue: Agent dependencies create circular deadlock**
- **Solution**: Reorder tasks to break circular dependencies
- **Escalate**: If unresolvable, ask user to reprioritize

**Issue: Sprint-manager.sh script not found**
- **Solution**: Check `/home/fitna/homelab/shared/scripts/sprint-manager.sh`
- **Fallback**: Generate reports manually using templates

**Issue: Previous sprint not archived**
- **Solution**: Offer to archive before starting new sprint
- **Warning**: Don't overwrite active sprint data

## Example Usage

### User Request
"Create a new sprint plan for Sprint 27 focused on launching the beta version of Fitnaai and improving infrastructure monitoring."

### Agent Response
```markdown
I'll create Sprint 27 plan with focus on beta launch and monitoring improvements.

**Sprint 27 Goals:**
1. Launch Fitnaai beta with 10 invited users
2. Implement comprehensive infrastructure monitoring
3. Complete landing page and signup flow

**Team Capacity:** 6 agents, 21 story points

Let me generate the sprint plan and board...

✅ Created `/home/fitna/homelab/sprints/sprint-27/SPRINT_PLAN.md`
✅ Created `/home/fitna/homelab/sprints/sprint-27/SPRINT_BOARD.md`
✅ Allocated tasks across 6 agents
✅ Total story points: 21 SP (baseline maintained)

**High-Priority Tasks:**
- ContentCreatorAgent: Beta launch announcement copy (3 SP)
- DeploymentOrchestrator: Prometheus + Grafana setup (6 SP)
- ResearcherAgent: Beta user onboarding strategy (3.5 SP)

Sprint starts [DATE] and ends [DATE] (10 working days).
Daily standups will be auto-generated at 9:00 AM.
```

## Integration Points

### Related Skills
- **Agent 3 - AgentTaskGenerator**: Use to create detailed agent prompts
- **Agent 4 - DailyProgressReporter**: Use for detailed daily tracking
- **Agent 7 - RoadmapTracker**: Update roadmap based on sprint progress

### External Tools
- `/home/fitna/homelab/shared/scripts/sprint-manager.sh` - Sprint automation
- `/home/fitna/homelab/shared/scripts/create-daily-sheet-enhanced.sh` - Daily tracking
- GitHub Projects (optional) - Sync sprint board to GitHub

### Data Sources
- Previous sprint retrospectives (velocity trends)
- Roadmap milestones (`/home/fitna/homelab/ROADMAP_1M_18MONTHS.md`)
- Agent capacity data (historical performance)

## Version
v1.0 - Initial skill definition based on Sprint 26 workflow analysis
