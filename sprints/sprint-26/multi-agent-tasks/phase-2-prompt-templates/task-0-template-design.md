# Task 0: Agent Prompt Template Design

**Agent:** CommunicatorAgent
**Model:** Claude 3.5 Sonnet (Prompt Engineering Expert)
**Output:** Template file + Documentation
**Length:** Template 80-120 lines, Documentation 30 lines

---

## Mission

Design the universal template for all 24 Sprint 26 agent task prompts. This template will be used to restructure existing agent prompts from 200-316 lines down to 80-120 lines.

---

## Requirements

The template must:
1. **Be highly focused** - 1 task per prompt (not 4 like current)
2. **Include shared context** - Reference to shared-context/ files
3. **Clear structure** - Objective, Requirements, Deliverables, Success Criteria
4. **Executable** - End with ready-to-copy prompt for AI agent
5. **Consistent** - Same format for all 24 tasks

---

## Current Problem (Analyze these files)

Read existing prompts:
- `/home/fitna/homelab/sprints/sprint-26/agent-prompts/ContentCreatorAgent.md` (166 lines, 4 tasks)
- `/home/fitna/homelab/sprints/sprint-26/agent-prompts/DeploymentOrchestrator.md` (316 lines, 4 tasks)

Problems:
- Too long (AI loses focus after ~150 lines)
- Context duplicated across all prompts
- Hard to iterate on individual tasks
- Mixed concerns (context + multiple tasks)

---

## Template Structure (Design this)

```markdown
# [Agent Name] - Task [N]: [Specific Task Title]

**Metadata:**
- Agent: [AgentType]
- Model: [LLM Model - Perplexity/GPT-4o-mini/Claude Sonnet]
- Includes: @shared-context/project-context.md, @sprint-context.md, @brand-guidelines.md (if content task)
- Story Points: X
- Priority: HIGH/MEDIUM/LOW
- Deadline: YYYY-MM-DD
- Output: /path/to/specific/file.ext

---

## Objective

[1-2 sentences stating the clear, measurable objective of THIS SPECIFIC TASK ONLY]

---

## Requirements

[5-10 specific, actionable requirements for this task]

- Requirement 1
- Requirement 2
- ...

---

## Context (Task-Specific Only)

[ONLY context unique to this specific task - max 20 lines]
[Do NOT repeat general project context - that's in shared-context/]

**Key information:**
- [Specific detail 1]
- [Specific detail 2]

---

## Deliverables

1. **[File 1]** - [Description]
2. **[File 2]** (optional) - [Description]

**Format:** [Markdown/YAML/CSV/etc.]
**Location:** [Exact file path]

---

## Success Criteria

- [ ] Criterion 1 (measurable)
- [ ] Criterion 2 (measurable)
- [ ] Criterion 3 (measurable)

---

## Execution Prompt (Copy to AI Agent)

```
You are [AgentName] working on Sprint 26, Task [N]: [Title].

**Context** (from shared-context files):
- Product: HexaHub - [brief from project-context]
- Sprint Goal: [from sprint-context]
- Brand: [from brand-guidelines if applicable]

**Your Task:**
[Specific objective restated]

**Requirements:**
1. [Requirement 1]
2. [Requirement 2]
...

**Output:**
File: /path/to/output/file.ext
Format: [specific format]
Length: [if applicable]

**Success:**
[Clear success metric]

Begin now. Output the complete [deliverable name] file.
```

---

## Additional Guidelines

1. **Length:** 80-120 lines total (strict)
2. **Sections:** Always include all 8 sections above
3. **Shared Context:** Never duplicate - always reference @shared-context/
4. **Execution Prompt:** Must be copy-pasteable directly to AI
5. **Specificity:** Every requirement must be actionable and measurable

---

```

---

## Output Requirements

Create TWO files:

### 1. Template File: `/home/fitna/homelab/sprints/sprint-26/shared-context/task-prompt-template.md`
- The complete template structure above
- With [placeholders] for variables
- 80-120 lines

### 2. Documentation: `/home/fitna/homelab/sprints/sprint-26/shared-context/template-usage-guide.md`
- How to use the template (30 lines)
- Example: Fill in ContentCreatorAgent Task 1
- Common mistakes to avoid

---

## Success Criteria

- [ ] Template is 80-120 lines (±5 acceptable)
- [ ] All 8 required sections present
- [ ] Execution Prompt section is copy-pasteable
- [ ] Documentation explains usage clearly
- [ ] Example shows how to fill placeholders
- [ ] Ready to be used for 24 task prompts

---

## Execution Prompt (For Claude Sonnet)

```
You are CommunicatorAgent (Prompt Engineering Expert) using Claude 3.5 Sonnet.

Your mission: Design the universal agent prompt template for Sprint 26.

**Problem:** Current agent prompts are 200-316 lines, too long, unfocused.
**Solution:** Template that creates 80-120 line focused prompts.

Read and analyze:
1. /home/fitna/homelab/sprints/sprint-26/agent-prompts/ContentCreatorAgent.md
2. /home/fitna/homelab/sprints/sprint-26/agent-prompts/DeploymentOrchestrator.md

Design template with 8 sections:
1. Metadata (agent, model, includes, story points, output)
2. Objective (1-2 sentences, specific)
3. Requirements (5-10 actionable items)
4. Context - Task-Specific Only (max 20 lines)
5. Deliverables (exact file paths)
6. Success Criteria (measurable checkboxes)
7. Execution Prompt (copy-pasteable to AI)
8. Additional Guidelines

Create:
1. Template: /home/fitna/homelab/sprints/sprint-26/shared-context/task-prompt-template.md (80-120 lines)
2. Documentation: /home/fitna/homelab/sprints/sprint-26/shared-context/template-usage-guide.md (30 lines)

Include example showing ContentCreatorAgent Task 1 filled in.

Begin now. This template will be used for all 24 tasks.
```
