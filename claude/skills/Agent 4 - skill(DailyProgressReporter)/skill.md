# Skill: Daily Progress Reporter

## Name
**Daily Progress Reporter** - Automated Daily and Evening Work Tracking

## Description
This skill automates the generation of daily work sheets and evening progress reports using the scripts from `/home/fitna/homelab/shared/scripts/create-daily-sheet-enhanced.sh` and `create-evening-report.sh`. It tracks task completion, calculates progress metrics, generates performance scores, and provides actionable recommendations based on the comprehensive tracking guide from `/home/fitna/homelab/shared/docs/DAILY_TRACKING_COMPLETE_GUIDE.md`.

## When to Use This Skill

### Trigger Conditions
Use this skill when the user requests ANY of the following:
- "Create today's work sheet"
- "Generate evening report"
- "Track daily progress"
- "Create daily tracking document"
- "How did I do today?"
- "Generate performance report"
- "Create work summary for [date]"

### Context Indicators
- User mentions daily standup, EOD (end of day), or progress tracking
- User asks about task completion rates or productivity metrics
- User wants to review accomplishments or identify blockers
- Time-based triggers (morning routine, evening routine)

## Process Steps

### Phase 1: Morning Routine - Daily Work Sheet (5-10 minutes)

1. **Generate Daily Work Sheet**
   ```bash
   /home/fitna/homelab/shared/scripts/create-daily-sheet-enhanced.sh
   ```

   **Output Location:** `/home/fitna/homelab/daily-tracking/YYYY-MM-DD-work-sheet.md`

2. **Work Sheet Structure**
   ```markdown
   # Daily Work Sheet - [DATE]

   ## Top 3 Priorities Today
   1. [ ] [Priority 1] - [Project] - [Est. time]
   2. [ ] [Priority 2] - [Project] - [Est. time]
   3. [ ] [Priority 3] - [Project] - [Est. time]

   ## Yesterday's Evening Report Summary
   [Auto-populated from previous day's evening report]

   ## Project: AI Agents (J-Jeco Platform)
   - [ ] Task 1 description
   - [ ] Task 2 description
   Progress: [████░░░░░░░░░░░░░░░░] 20% (each █ = 5%)

   ## Project: Homelab Infrastructure
   - [ ] Task 1 description
   - [ ] Task 2 description
   Progress: [██████░░░░░░░░░░░░░░] 30%

   ## Project: Fitnaai SaaS
   - [ ] Task 1 description
   - [ ] Task 2 description
   Progress: [████████░░░░░░░░░░░░] 40%

   ## Learning & Development
   - [ ] Task 1 description
   Progress: [██░░░░░░░░░░░░░░░░░░] 10%

   ## Blockers & Challenges
   - [Blocker 1 description]
   - [Blocker 2 description]

   ## Notes & Insights
   - [Note 1]
   - [Note 2]

   ## Time Tracking
   | Session | Project | Start | End | Duration | Completed |
   |---------|---------|-------|-----|----------|-----------|
   | 1 | | | | | |
   ```

3. **Review Yesterday's Evening Report**
   ```bash
   YESTERDAY=$(date -d "yesterday" +%Y-%m-%d)
   cat /home/fitna/homelab/daily-tracking/$YESTERDAY-evening-report.md
   ```

   **Extract:**
   - Incomplete tasks (carry forward to today)
   - Unresolved blockers
   - Performance score and recommendations

4. **Set Top 3 Priorities**
   - Use Eisenhower Matrix (Urgent + Important)
   - Estimate time per priority (realistic, not optimistic)
   - Align with sprint goals or roadmap milestones

### Phase 2: Throughout Day - Progress Updates (Continuous)

5. **Check Off Completed Tasks**
   - Mark checkboxes: `- [ ]` → `- [x]`
   - Update progress bars (each █ = 5%)
   - Log time in time tracking table

6. **Document Blockers Immediately**
   Add to "Blockers & Challenges" section with:
   - Description of blocker
   - Impact on timeline
   - Attempted solutions
   - Required help/resources

7. **Track Time Sessions**
   Update time tracking table:
   ```markdown
   | Session | Project | Start | End | Duration | Completed |
   |---------|---------|-------|-----|----------|-----------|
   | 1 | Homelab | 08:00 | 10:30 | 2.5h | Deploy monitoring stack |
   | 2 | Fitnaai | 11:00 | 13:00 | 2.0h | Landing page copy |
   ```

### Phase 3: Evening Routine - Generate Report (10-15 minutes)

8. **Run Evening Report Script**
   ```bash
   /home/fitna/homelab/shared/scripts/create-evening-report.sh \
     /home/fitna/homelab/daily-tracking/$(date +%Y-%m-%d)-work-sheet.md
   ```

   **Output:** `/home/fitna/homelab/daily-tracking/$(date +%Y-%m-%d)-evening-report.md`

9. **Evening Report Structure**
   ```markdown
   # Evening Report - [DATE]

   ## Overall Statistics
   - Total tasks: X
   - Completed: Y (Z%)
   - Pending: A
   - Progress: [████████░░░░░░░░░░░░] Z%

   ## Project Breakdown

   ### AI Agents (J-Jeco Platform)
   - Total: X tasks
   - Completed: Y (Z%)
   - Progress: [██████░░░░░░░░░░░░░░] Z%

   ### Homelab Infrastructure
   - Total: X tasks
   - Completed: Y (Z%)
   - Progress: [████░░░░░░░░░░░░░░░░] Z%

   ### Fitnaai SaaS
   - Total: X tasks
   - Completed: Y (Z%)
   - Progress: [██████░░░░░░░░░░░░░░] Z%

   ### Learning & Development
   - Total: X tasks
   - Completed: Y (Z%)
   - Progress: [██░░░░░░░░░░░░░░░░░░] Z%

   ## Key Achievements
   - ✅ [Achievement 1 from completed tasks]
   - ✅ [Achievement 2 from completed tasks]
   - ✅ [Achievement 3 from completed tasks]

   ## Blockers Encountered
   - 🚧 [Blocker 1]
   - 🚧 [Blocker 2]

   ## Tomorrow's Preparation
   - [ ] [Carry-forward task 1]
   - [ ] [Carry-forward task 2]
   - [ ] [New priority task]

   ## Performance Score: XX% 🟢/🟡/🟠/🔴

   ### Rating: [Excellent/Good/Moderate/Needs Improvement]

   ### Recommendations:
   - [Recommendation 1 based on completion rate]
   - [Recommendation 2 based on blockers]
   - [Recommendation 3 based on time usage]
   ```

10. **Calculate Performance Score**
    Formula: `(Completed Tasks / Total Tasks) × 100`

    **Rating Scale:**
    - 🟢 **Excellent (80-100%)**: Maintain current workflow
    - 🟡 **Good (60-79%)**: Keep momentum, address minor blockers
    - 🟠 **Moderate (40-59%)**: Review priorities, reduce scope
    - 🔴 **Needs Improvement (<40%)**: Address blockers urgently, reassess capacity

11. **Extract Key Achievements**
    Auto-extract from completed checkboxes:
    - Prioritize HIGH priority completions
    - Include measurable outcomes (e.g., "Deployed 3 services")
    - Highlight cross-project impacts

12. **Analyze Blockers**
    For each blocker:
    - Categorize: Technical, Resource, Decision, External
    - Assess impact: Critical (blocks sprint), High, Medium, Low
    - Suggest mitigation: Who to contact, what to research, how to workaround

13. **Generate Recommendations**
    Based on metrics:

    **If completion <40%:**
    - "Reduce tomorrow's task count by 30%"
    - "Focus on top 2 priorities only"
    - "Schedule blocker resolution session"

    **If completion 60-79%:**
    - "Good progress, address [specific blocker]"
    - "Carry forward incomplete tasks to tomorrow"
    - "Maintain current pace"

    **If completion >80%:**
    - "Excellent day! Maintain workflow"
    - "Consider adding stretch goals tomorrow"
    - "Document successful patterns"

### Phase 4: Weekly Review (Friday Evening)

14. **Generate Weekly Summary**
    ```bash
    # Aggregate all week's evening reports
    WEEK_START=$(date -d "last monday" +%Y-%m-%d)
    WEEK_END=$(date +%Y-%m-%d)

    cat /home/fitna/homelab/daily-tracking/{$WEEK_START..$WEEK_END}-evening-report.md > \
      /home/fitna/homelab/daily-tracking/weekly-summary-$(date +%Y-W%U).md
    ```

15. **Weekly Metrics**
    ```markdown
    # Weekly Summary - Week [NUMBER] ([DATE RANGE])

    ## Overall Performance
    - Average daily completion: XX%
    - Total tasks completed: XX
    - Total blockers resolved: XX
    - Performance trend: [📈 Improving / 📉 Declining / ➡️ Stable]

    ## Project Progress
    | Project | Tasks Done | Progress Gain | Status |
    |---------|------------|---------------|--------|
    | AI Agents | XX | +XX% | 🟢/🟡/🟠/🔴 |
    | Homelab | XX | +XX% | 🟢/🟡/🟠/🔴 |
    | Fitnaai | XX | +XX% | 🟢/🟡/🟠/🔴 |

    ## Top Achievements This Week
    1. [Achievement 1]
    2. [Achievement 2]
    3. [Achievement 3]

    ## Persistent Blockers
    - [Blocker that appeared >2 times]

    ## Next Week Focus
    - [Priority 1 based on roadmap]
    - [Priority 2 based on blockers]
    - [Priority 3 based on velocity]
    ```

## Rules and Constraints

### Hard Rules (Must Follow)
1. **Morning sheet MUST be created before 9:00 AM**
2. **Evening report MUST be generated before end of day**
3. **All tasks MUST have checkboxes** ([ ] or [x])
4. **Progress bars MUST match completion %** (each █ = 5%)
5. **Top 3 priorities are MANDATORY** (no more, no less)
6. **Blockers MUST be documented same-day** (no delayed reporting)
7. **Performance score MUST be calculated** (no subjective guessing)

### Soft Rules (Best Practices)
- Limit tasks per project to 5-7 (more = split into subtasks)
- Update progress bars every 2-3 hours
- Log time sessions as they happen (not retroactively)
- Review evening report before planning next day
- Archive weekly summaries for velocity tracking

### Quality Gates
Before finalizing evening report:
- [ ] All checkboxes marked ([ ] or [x])
- [ ] Progress bars accurate (count █ symbols)
- [ ] Key achievements extracted (top 3)
- [ ] Blockers documented with impact
- [ ] Performance score calculated correctly
- [ ] Recommendations are actionable

## Expected Outputs

### Deliverables
1. **Daily Work Sheet** - Morning planning document
2. **Evening Report** - End-of-day progress summary
3. **Weekly Summary** - Friday aggregated report
4. **Performance Metrics** - Completion rates and trends

### File Structure
```
/home/fitna/homelab/daily-tracking/
├── 2025-01-27-work-sheet.md
├── 2025-01-27-evening-report.md
├── 2025-01-28-work-sheet.md
├── 2025-01-28-evening-report.md
├── weekly-summary-2025-W04.md
└── archive/
    └── 2025-01/
        ├── 2025-01-20-work-sheet.md
        └── 2025-01-20-evening-report.md
```

### Success Metrics
- ✅ Daily work sheet created before 9 AM
- ✅ Evening report generated every workday
- ✅ Performance score >60% (weekly average)
- ✅ Blockers resolved within 2 days
- ✅ Weekly velocity trending up or stable

## Error Handling

### Common Issues & Solutions

**Issue: Script not found**
- **Solution**: Verify path `/home/fitna/homelab/shared/scripts/create-evening-report.sh`
- **Fallback**: Create report manually using template

**Issue: Progress bars don't match completion %**
- **Solution**: Auto-calculate: `(Completed / Total) × 20 = number of █ symbols`
- **Example**: 7/10 tasks = 70% = 14 █ symbols (70/5)

**Issue: No tasks completed (0%)**
- **Action**: Investigate blockers, reassess priorities, reduce scope
- **Report**: Include detailed blocker analysis

**Issue: >100% completion (new tasks added during day)**
- **Solution**: Separate "Bonus Tasks" section for unplanned work
- **Metric**: Track planned vs. unplanned ratio

**Issue: Missing time tracking data**
- **Solution**: Estimate based on commits, logs, calendar events
- **Prevention**: Use Pomodoro timer or time tracking tool

## Example Usage

### User Request
"Generate my evening report for today."

### Agent Response
```markdown
I'll generate your evening report for 2025-01-28.

**Reading work sheet:** `/home/fitna/homelab/daily-tracking/2025-01-28-work-sheet.md`

**Overall Statistics:**
- Total tasks: 15
- Completed: 11 (73%)
- Pending: 4
- Progress: [██████████████░░░░░░] 73%

**Project Breakdown:**
- AI Agents: 5/6 tasks (83%) [████████████████░░░░] 🟢
- Homelab: 4/5 tasks (80%) [████████████████░░░░] 🟢
- Fitnaai: 2/4 tasks (50%) [██████████░░░░░░░░░░] 🟠

**Key Achievements:**
✅ Deployed monitoring stack (Prometheus + Grafana)
✅ Created 3 agent task prompts (ContentCreator, Researcher, Analyst)
✅ Fixed critical authentication bug in Authentik

**Blockers:**
🚧 CodeRabbit integration pending SSH key setup
🚧 Landing page copy awaiting brand guidelines review

**Performance Score: 73% 🟡 Good**

**Recommendations:**
- Good progress! Address SSH key blocker tomorrow morning.
- Complete Fitnaai tasks (2 remaining) before EOD tomorrow.
- Maintain current pace, you're on track for sprint goals.

**Report saved:** `/home/fitna/homelab/daily-tracking/2025-01-28-evening-report.md`
```

## Integration Points

### Related Skills
- **Agent 1 - SprintManager**: Update sprint burndown from daily progress
- **Agent 3 - AgentTaskGenerator**: Track agent task execution progress
- **Agent 7 - RoadmapTracker**: Feed velocity data to roadmap tracker

### External Tools
- Scripts: `/home/fitna/homelab/shared/scripts/create-daily-sheet-enhanced.sh`
- Scripts: `/home/fitna/homelab/shared/scripts/create-evening-report.sh`
- Guide: `/home/fitna/homelab/shared/docs/DAILY_TRACKING_COMPLETE_GUIDE.md`

### Data Sources
- Sprint plan: `/home/fitna/homelab/sprints/sprint-{NUMBER}/SPRINT_PLAN.md`
- Roadmap: `/home/fitna/homelab/ROADMAP_1M_18MONTHS.md`
- Time tracking logs: `/home/fitna/homelab/logs/time-tracking/`

## Version
v1.0 - Initial skill definition based on daily tracking workflow analysis
