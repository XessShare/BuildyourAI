# Task Prompt Template - Usage Guide

## Purpose

This template creates focused, 80-120 line task prompts for Sprint 26's 24 agent tasks. It solves the problem of 200-316 line prompts that mix multiple tasks and duplicate context.

---

## How to Use This Template

### Step 1: Copy the Template
```bash
cp /home/fitna/homelab/sprints/sprint-26/shared-context/task-prompt-template.md \
   /home/fitna/homelab/sprints/sprint-26/multi-agent-tasks/phase-X/task-Y-[name].md
```

### Step 2: Fill Placeholders

Replace ALL `[bracketed placeholders]` with specific values:

1. **Header Section:**
   - `[AgentName]` → ContentCreatorAgent, ResearcherAgent, etc.
   - `[N]` → Task number (1-4 per agent)
   - `[Specific Task Title]` → Concrete title (e.g., "Landing Page Copy")

2. **Metadata:**
   - `[AgentType]` → Same as AgentName
   - `[LLM Model]` → Claude Sonnet 4.5 / GPT-4o-mini / Perplexity Sonar
   - `[X]` → Story points (0.5, 1, 1.5, 2)
   - `[Priority]` → HIGH, MEDIUM, or LOW
   - `[Deadline]` → Specific date or Tag number

3. **Content Sections:**
   - Write 1-2 sentence objective (be specific!)
   - List 5-10 concrete, measurable requirements
   - Add ONLY task-specific context (not general project info)
   - Define exact deliverable paths and formats
   - Create 3-5 measurable success criteria

4. **Execution Prompt:**
   - This MUST be copy-pasteable to AI without edits
   - Include brief context from shared files
   - Restate requirements clearly
   - Specify exact output format and location

### Step 3: Validate

Check your completed prompt:
- [ ] 80-120 lines total (±5 acceptable)
- [ ] All `[placeholders]` replaced
- [ ] No duplicated context from shared-context files
- [ ] Execution prompt is self-contained and copy-pasteable
- [ ] Success criteria are measurable (no vague statements)

---

## Example: ContentCreatorAgent Task 1

**Before (from old prompt):** 166 lines mixing 4 tasks + duplicated brand guidelines

**After (using template):** 95 lines, focused on ONLY landing page copy

```markdown
# ContentCreatorAgent - Task 1: Landing Page Copy (HexaHub MVP)

**Metadata:**
- Agent: ContentCreatorAgent
- Model: Claude Sonnet 4.5
- Story Points: 1
- Priority: HIGH
- Deadline: Tag 3 (2025-12-30)
- Output File: `/home/fitna/homelab/shared/content/sprint-26/landing-page-copy.md`

**Shared Context (Read before executing):**
- @project-context.md - Product overview, tech stack, target audience
- @sprint-context.md - Sprint 26 goals, timeline, agent allocation
- @brand-guidelines.md - Voice, tone, keywords

---

## Objective

Create conversion-optimized landing page copy for HexaHub MVP beta launch, targeting privacy-conscious developers with clear value proposition, feature highlights, and strong CTA.

---

## Requirements

1. Hero Section: Headline + subheadline clearly stating "self-hosted AI workspace for developers"
2. Value Proposition: 3 key benefits (privacy, multi-model AI, open-source) in 50-100 words each
3. Features Section: 3-5 core features with descriptions (AI sidebar, workflow automation, team collaboration)
4. Social Proof: 3 beta testimonial templates + trust signals (security, privacy badges)
5. FAQ Section: 5-7 questions covering pricing, self-hosting, AI capabilities
6. CTA: "Start Free Beta" button copy with urgency/scarcity element
7. SEO: Target keywords "self-hosted AI", "privacy-first workspace", "developer AI tools"

**Technical Constraints:**
- Markdown format with HTML-ready structure (use ## for sections, ### for subsections)
- Max 1500 words total (focus on clarity over length)

---

## Context (Task-Specific Only)

**Key Information for This Task:**
- Target conversion rate: 5%+ (beta signups from landing page visitors)
- Competitor reference: Cursor, GitHub Copilot, Codeium (emphasize privacy gaps)
- Unique angle: "True self-hosting" (not just API key integration)
- CTA leads to: Beta signup form (email capture for Ghost/Listmonk newsletter)

**Dependencies:**
- None (this is a foundational task)

---

## Deliverables

**Primary Output:**
1. **landing-page-copy.md** - Complete landing page copy with all sections
   - Format: Markdown with HTML structure comments
   - Location: `/home/fitna/homelab/shared/content/sprint-26/`
   - Length: ~1200-1500 words

**Quality Standards:**
- Aligns with brand guidelines (no buzzwords like "revolutionary", "game-changing")
- Includes all primary keywords at least 2x each
- Passes readability test (Grade 10-12 reading level for technical audience)

---

## Success Criteria

- [ ] Contains all 6 required sections (Hero, Value Prop, Features, Social Proof, FAQ, CTA)
- [ ] Uses keywords "self-hosted", "privacy-first", "AI workspace" at least 2x each
- [ ] No buzzwords from brand guidelines avoid-list
- [ ] FAQ section has 5-7 questions with clear answers
- [ ] CTA is action-oriented and includes urgency element

---

## Execution Prompt (Copy to AI Agent)

\`\`\`
You are ContentCreatorAgent working on Sprint 26, Task 1: Landing Page Copy.

**Context** (from shared-context files):
- Product: HexaHub - Self-hosted AI workspace for developers
- Sprint Goal: MVP launch foundation (landing page, content engine, infrastructure)
- Target Audience: Privacy-conscious developers (30-45), homelab enthusiasts
- Brand Voice: Professional but approachable, developer-to-developer, no fluff

**Your Specific Task:**
Create conversion-optimized landing page copy for HexaHub MVP beta launch with clear value proposition and strong CTA targeting 5%+ conversion rate.

**Requirements:**
1. Hero Section: Headline + subheadline (self-hosted AI workspace)
2. Value Proposition: 3 key benefits (privacy, multi-model AI, open-source) - 50-100 words each
3. Features: 3-5 core features (AI sidebar, workflow automation, team collaboration)
4. Social Proof: 3 testimonial templates + trust signals
5. FAQ: 5-7 questions (pricing, self-hosting, AI capabilities)
6. CTA: "Start Free Beta" with urgency element
7. SEO: Keywords "self-hosted AI", "privacy-first workspace", "developer AI tools" (2x each)

**Task-Specific Context:**
- Competitors: Cursor, Copilot, Codeium (emphasize privacy gaps)
- Unique angle: "True self-hosting" (full backend, not just API keys)
- CTA destination: Beta signup form (email capture for newsletter)

**Output:**
File: /home/fitna/homelab/shared/content/sprint-26/landing-page-copy.md
Format: Markdown with HTML structure comments (## for sections, ### for subsections)
Length: ~1200-1500 words

**Success Criteria:**
- All 6 sections complete
- Keywords used 2x+ each
- No buzzwords ("revolutionary", "game-changing", "disruptive")
- FAQ has 5-7 clear Q&As

**Deadline:** Tag 3 (2025-12-30)

Begin now. Output the complete landing-page-copy.md file.
\`\`\`

---

**Task Created:** 2025-12-28
**Last Updated:** 2025-12-28
**Estimated Completion Time:** 2-3 hours
```

---

## Common Mistakes to Avoid

1. **Duplicating Context:** Don't copy project overview from @project-context.md into task prompts
2. **Vague Requirements:** "Create good content" → "Create 1500-word landing page with 5%+ conversion CTA"
3. **Unmeasurable Success Criteria:** "Looks professional" → "Passes ESLint with 0 errors"
4. **Non-Copy-Pasteable Execution Prompts:** Include ALL context in the execution block
5. **Mixing Multiple Tasks:** One task per file (not 4 tasks in one prompt)
6. **Missing File Paths:** Always specify exact absolute paths for deliverables
7. **Ignoring Length Limit:** Keep to 80-120 lines (the example above is 95 lines)

---

## Next Steps

After creating task prompts using this template:

1. **Validate:** Run line count check: `wc -l task-X-name.md` (should be 80-120)
2. **Test:** Copy execution prompt to AI agent and verify it works standalone
3. **Review:** Check against template-usage-guide.md success criteria
4. **Iterate:** Update template if you find consistent issues across tasks

---

**Template Version:** 1.0
**Created:** 2025-12-28
**For:** Sprint 26 (24 agent tasks across 6 agents)
