# [AgentName] - Task 1: Roadmap Tracker Initialization

**Metadata:**
- Agent: [AgentType - e.g., ContentCreatorAgent, ResearcherAgent]
- Model: [LLM Model - Claude Sonnet 4.5 / GPT-4o-mini / Perplexity Sonar]
- Story Points: [X]
- Priority: [HIGH / MEDIUM / LOW]
- Deadline: [YYYY-MM-DD or Tag N]
- Output File: `/home/fitna/homelab/[specific/path/to/output.ext]`

**Shared Context (Read before executing):**
- @project-context.md - Product overview, tech stack, target audience
- @sprint-context.md - Sprint 26 goals, timeline, agent allocation
- @brand-guidelines.md - Voice, tone, keywords (for content tasks only)

---

## Objective

[1-2 clear sentences stating the SPECIFIC objective of THIS TASK ONLY. Be measurable and concrete.]

Example: "Create conversion-optimized landing page copy for HexaHub MVP beta launch, targeting privacy-conscious developers with clear value proposition and CTA."

---

## Requirements

[5-10 specific, actionable requirements. Each must be measurable and testable.]

1. [Specific requirement with measurable criteria]
2. [Specific requirement with measurable criteria]
3. [Specific requirement with measurable criteria]
4. [Specific requirement with measurable criteria]
5. [Specific requirement with measurable criteria]

**Technical Constraints:**
- [Any technical limitations, format requirements, or dependencies]
- [File size limits, API constraints, or compatibility requirements]

---

## Context (Task-Specific Only)

[ONLY context unique to THIS SPECIFIC TASK - max 20 lines]
[Do NOT repeat project overview, sprint goals, or brand voice - those are in shared-context/]

**Key Information for This Task:**
- [Specific detail 1 that only applies to this task]
- [Specific detail 2 that only applies to this task]
- [Relevant data, research, or reference materials]

**Dependencies:**
- [Other tasks that must complete first, if any]
- [External resources needed]

---

## Deliverables

**Primary Output:**
1. **[Filename.ext]** - [Brief description of what this file contains]
   - Format: [Markdown / YAML / CSV / Python / JSON / etc.]
   - Location: `/home/fitna/homelab/[exact/path/]`
   - Length: [Approx. lines/words if applicable]

**Optional Outputs (if applicable):**
2. **[Filename2.ext]** - [Description]

**Quality Standards:**
- [Specific quality criteria - e.g., "80%+ test coverage", "passes ESLint"]
- [Validation method - e.g., "validated with yamllint", "tested with 3 user scenarios"]

---

## Success Criteria

- [ ] [Measurable criterion 1 - e.g., "File exists at specified path"]
- [ ] [Measurable criterion 2 - e.g., "Contains all 5 required sections"]
- [ ] [Measurable criterion 3 - e.g., "Passes validation script"]
- [ ] [Measurable criterion 4 - e.g., "Meets 80-120 line length requirement"]
- [ ] [Quality criterion - e.g., "Aligns with brand guidelines (no buzzwords)"]

---

## Execution Prompt (Copy to AI Agent)

```
You are [AgentName] working on Sprint 26, Task 1: [Task Title].

**Context** (from shared-context files):
- Product: HexaHub - Self-hosted AI workspace for developers
- Sprint Goal: [Brief from sprint-context.md]
- Target Audience: Privacy-conscious developers, homelab enthusiasts
- Brand Voice: [Brief from brand-guidelines.md - if content task]

**Your Specific Task:**
[Restate objective in 1-2 sentences]

**Requirements:**
1. [Requirement 1]
2. [Requirement 2]
3. [Requirement 3]
4. [Requirement 4]
5. [Requirement 5]

**Task-Specific Context:**
- [Key detail 1]
- [Key detail 2]

**Output:**
File: /home/fitna/homelab/[exact/path/to/output.ext]
Format: [Specific format requirements]
Length: [Expected length if applicable]

**Success Criteria:**
- [Primary success metric]
- [Quality standard]

**Deadline:** [Date or Tag]

Begin now. Output the complete [deliverable name] and confirm completion against success criteria.
```

---

## Additional Notes

[Optional section for any other relevant information - max 10 lines]
[Examples: Known issues, future considerations, reference links]

---

**Task Created:** [YYYY-MM-DD]
**Last Updated:** [YYYY-MM-DD]
**Estimated Completion Time:** [X hours/days]
