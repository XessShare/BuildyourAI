# Skill: Agent Task Generator

## Name
**Agent Task Generator** - Optimized Multi-Agent Task Prompt Creation

## Description
This skill generates optimized, context-rich task prompts for specialized agents based on the proven template structure from `/home/fitna/homelab/sprints/sprint-26/agent-prompts-optimized/`. It creates 80-120 line prompts with shared context references, clear objectives, measurable requirements, and copy-pasteable execution instructions. The skill ensures agents receive comprehensive, actionable task definitions that enable autonomous execution.

## When to Use This Skill

### Trigger Conditions
Use this skill when the user requests ANY of the following:
- "Create an agent prompt for [task]"
- "Generate a task for [AgentType]"
- "Write an optimized prompt for [objective]"
- "Prepare agent instructions for [deliverable]"
- "Create a task delegation prompt"
- "Generate agent-specific task definition"

### Context Indicators
- User mentions specific agent types (ContentCreator, Researcher, Analyst, DeploymentOrchestrator, Verifier, ProjectManager)
- User discusses task delegation or multi-agent workflows
- User wants to create reusable task templates
- User references sprint planning or task allocation

## Process Steps

### Phase 1: Task Analysis (2-3 minutes)

1. **Identify Agent Type**
   Available agents:
   - **ContentCreatorAgent**: Copy, scripts, social media, newsletters
   - **ResearcherAgent**: Analysis, trends, competitors, communities
   - **AnalystAgent**: Dashboards, metrics, KPIs, tracking
   - **DeploymentOrchestrator**: Infrastructure, CI/CD, deployments
   - **VerifierAgent**: Testing, QA, security, code review
   - **ProjectManagerAgent**: Planning, coordination, reporting

2. **Extract Task Requirements**
   Ask user (if not provided):
   - What is the objective? (1-2 sentences)
   - What are the deliverables? (specific file paths)
   - What is the priority? (HIGH/MEDIUM/LOW/CONTINUOUS)
   - What is the deadline? (date or sprint milestone)
   - What context is needed? (project, sprint, brand, constraints)

3. **Define Success Criteria**
   Create 3-5 measurable checkboxes:
   - [ ] Deliverable X created at path Y
   - [ ] Meets quality standard Z
   - [ ] Reviewed and approved
   - [ ] Deployed/published (if applicable)

### Phase 2: Shared Context Setup (3-5 minutes)

4. **Reference Shared Context Files**
   Location: `/home/fitna/homelab/sprints/sprint-{NUMBER}/shared-context/`

   **Required Files:**
   - `@project-context.md` - Homelab architecture, goals, constraints
   - `@sprint-context.md` - Current sprint objectives, timeline, priorities
   - `@brand-guidelines.md` - Brand voice, tone, visual identity
   - `@output-structure.md` - Deliverable formatting standards

5. **Create Sprint-Specific Context** (if not exists)
   ```bash
   SPRINT_DIR="/home/fitna/homelab/sprints/sprint-{NUMBER}/shared-context"
   mkdir -p "$SPRINT_DIR"

   # Copy from previous sprint as template
   cp -r /home/fitna/homelab/sprints/sprint-26/shared-context/* "$SPRINT_DIR/"

   # Update sprint-context.md with current sprint goals
   ```

### Phase 3: Prompt Template Generation (5-10 minutes)

6. **Create Metadata Section**
   ```markdown
   ---
   agent: [AgentType]
   model: claude-sonnet-4.5
   priority: [HIGH/MEDIUM/LOW/CONTINUOUS]
   deadline: [YYYY-MM-DD or "End of Sprint X"]
   output_path: /home/fitna/homelab/[category]/sprint-{NUMBER}/
   ---
   ```

7. **Write Objective Section**
   - 1-2 sentences max
   - Action-oriented (Create, Analyze, Deploy, Verify)
   - Specific and measurable

   **Example:**
   ```markdown
   ## Objective
   Create a comprehensive landing page copy that explains Fitnaai's value proposition, targets early adopters, and drives beta signups with clear CTAs and social proof.
   ```

8. **Define Requirements Section** (5-10 items)
   - Each requirement is a bullet point
   - Must be verifiable (yes/no check)
   - Include constraints (word count, format, dependencies)

   **Example:**
   ```markdown
   ## Requirements
   1. Landing page copy (800-1200 words) with hero, features, testimonials, pricing, FAQ sections
   2. 3 distinct value propositions targeting fitness coaches, gym owners, and personal trainers
   3. Compelling hero headline (8-12 words) and subheadline (15-25 words)
   4. 5-7 feature descriptions with icon suggestions (50-80 words each)
   5. 3 fictional testimonials with realistic names, titles, and quotes (60-100 words each)
   6. Clear CTA buttons (primary: "Start Free Trial", secondary: "Watch Demo")
   7. FAQ section answering 8-10 common objections
   8. SEO-optimized meta title (50-60 chars) and description (150-160 chars)
   9. Tone: Professional, motivating, trustworthy (see @brand-guidelines.md)
   10. No marketing jargon, focus on tangible outcomes
   ```

9. **Add Task-Specific Context** (10-20 lines max)
   - Relevant background information
   - Constraints or dependencies
   - Reference materials

   **Example:**
   ```markdown
   ## Context
   Fitnaai is an AI-powered fitness platform for coaches to automate client onboarding, workout planning, and progress tracking. We're launching beta in 4 weeks with 10 invited fitness professionals. Competitors include Trainerize ($$$) and MyPT Hub ($$), but we differentiate with AI-driven personalization at 1/3 the price.

   Target audience: Fitness coaches managing 10-50 clients, tech-savvy, struggling with manual admin work, willing to try new tools. Pain points: time spent on repetitive tasks, client retention, workout customization at scale.

   Brand voice (from @brand-guidelines.md): We're the smart, efficient partner that frees coaches to focus on what they love—transforming lives. We don't overpromise, we deliver measurable time savings (avg. 10h/week).

   References:
   - Competitor analysis: /home/fitna/homelab/shared/research/sprint-26/competitor-analysis.md
   - User personas: /home/fitna/homelab/shared/docs/user-personas.md
   - Product features: /home/fitna/homelab/shared/docs/fitnaai-features.md
   ```

10. **Define Deliverables Section** (exact file paths)
    ```markdown
    ## Deliverables
    Create the following files in `/home/fitna/homelab/shared/content/sprint-26/landing-page/`:

    1. `hero-section.md` - Hero headline, subheadline, CTA (200-300 words)
    2. `features-section.md` - 5-7 feature blocks with descriptions (400-600 words)
    3. `testimonials-section.md` - 3 testimonials with names and titles (200-300 words)
    4. `faq-section.md` - 8-10 Q&A pairs (400-600 words)
    5. `meta-tags.md` - SEO title, description, social share text (100 words)
    6. `full-landing-page.md` - Complete assembled copy (1000-1200 words)
    ```

11. **Create Success Criteria Section** (checkboxes)
    ```markdown
    ## Success Criteria
    - [ ] All 6 deliverable files created with exact word counts
    - [ ] Hero headline A/B tested with 3 variants (select best)
    - [ ] Features aligned with product roadmap (verified against fitnaai-features.md)
    - [ ] Testimonials sound authentic (no generic praise, specific outcomes)
    - [ ] FAQs address top 10 objections from competitor reviews
    - [ ] SEO meta tags optimized (checked with Yoast/SEMrush)
    - [ ] Tone consistency score >90% (checked against brand-guidelines.md)
    - [ ] Copy reviewed by ProjectManagerAgent for clarity
    ```

12. **Add Execution Prompt Section** (copy-pasteable)
    ```markdown
    ## Execute This Task

    Copy and paste the following into your AI agent interface:

    ```
    You are ContentCreatorAgent. Your task is to create a landing page copy for Fitnaai's beta launch.

    Read the following context files first:
    - @project-context.md (homelab architecture and Fitnaai goals)
    - @sprint-context.md (Sprint 26 objectives and timeline)
    - @brand-guidelines.md (brand voice and tone standards)
    - @output-structure.md (deliverable formatting)

    [Full task context from above]

    Create all 6 deliverable files in `/home/fitna/homelab/shared/content/sprint-26/landing-page/`.

    Ensure every success criterion is met. Mark each checkbox when complete.
    ```
    ```

### Phase 4: Optimization and Validation (2-3 minutes)

13. **Validate Prompt Length**
    - Target: 80-120 lines
    - If <80 lines: Add more context or requirements
    - If >120 lines: Condense or split into multiple tasks

14. **Check for Ambiguity**
    Review each section:
    - [ ] Objective is specific (no vague goals)
    - [ ] Requirements are measurable (can be verified)
    - [ ] Deliverables have exact file paths
    - [ ] Success criteria are binary (yes/no)
    - [ ] No assumptions (all context provided)

15. **Test Copy-Pasteability**
    - Execution prompt should work standalone
    - All @references are valid file paths
    - No placeholders like [TBD] or [FILL IN]

## Rules and Constraints

### Hard Rules (Must Follow)
1. **ALWAYS reference shared context files** (@project-context.md, @sprint-context.md, etc.)
2. **Deliverables MUST have exact file paths** (no generic "create a document")
3. **Success criteria MUST be measurable** (checkboxes with verifiable outcomes)
4. **Prompt length: 80-120 lines** (excluding execution block)
5. **Agent type MUST match task category** (don't assign content creation to DeploymentOrchestrator)
6. **Priority MUST be set** (HIGH/MEDIUM/LOW/CONTINUOUS)
7. **Output path MUST exist or be creatable** (verify directory structure)

### Soft Rules (Best Practices)
- Limit requirements to 5-10 items (more = split into subtasks)
- Keep context section concise (10-20 lines max)
- Include 3-5 success criteria (not exhaustive)
- Reference existing files for context (avoid copy-pasting large blocks)
- Use concrete examples in requirements (not abstract descriptions)

### Quality Gates
Before finalizing prompt:
- [ ] Read by someone unfamiliar with the task → is it clear?
- [ ] Can success be measured objectively?
- [ ] Are all dependencies identified?
- [ ] Is the priority justified?
- [ ] Is the deadline realistic?

## Expected Outputs

### Deliverables
1. **Agent Task Prompt (.md file)** - Optimized 80-120 line prompt
2. **Shared Context Files** (if created) - 4 context files for sprint
3. **Execution Instructions** - Copy-pasteable prompt block

### File Structure
```
/home/fitna/homelab/sprints/sprint-{NUMBER}/agent-prompts-optimized/
├── ContentCreatorAgent-task-01-landing-page.md
├── ResearcherAgent-task-01-competitor-analysis.md
├── AnalystAgent-task-01-kpi-dashboard.md
├── DeploymentOrchestrator-task-01-cicd-pipeline.md
├── VerifierAgent-task-01-testing-framework.md
└── ProjectManagerAgent-task-01-sprint-planning.md
```

### Success Metrics
- ✅ Prompt length: 80-120 lines
- ✅ All metadata fields populated
- ✅ 5-10 measurable requirements
- ✅ Exact deliverable file paths
- ✅ 3-5 success criteria (checkboxes)
- ✅ Copy-pasteable execution block
- ✅ No ambiguous language

## Error Handling

### Common Issues & Solutions

**Issue: User provides vague objective**
- **Solution**: Ask clarifying questions (What exactly? By when? For whom?)
- **Example**: "Create content" → "Create what type? For which audience? With what goal?"

**Issue: Too many requirements (>10)**
- **Solution**: Split into multiple subtasks or prioritize top 5-7
- **Action**: Suggest breaking down into sprint phases

**Issue: Missing shared context files**
- **Solution**: Create from template (/sprints/sprint-26/shared-context/)
- **Fallback**: Embed context directly in prompt (increases length)

**Issue: Deliverable path doesn't exist**
- **Solution**: Create directory structure first or instruct agent to create
- **Command**: `mkdir -p /path/to/deliverables/`

**Issue: Success criteria not measurable**
- **Solution**: Rephrase as verifiable checkboxes
- **Bad**: "Make it good" → **Good**: "Tone consistency score >90%"

## Example Usage

### User Request
"Create a prompt for ResearcherAgent to analyze competitors for Fitnaai."

### Agent Response
```markdown
I'll create an optimized agent task prompt for competitor analysis.

**Agent:** ResearcherAgent
**Objective:** Analyze top 5 fitness coaching platforms to identify differentiation opportunities for Fitnaai's beta launch.

**Deliverables:**
- competitor-analysis.md (1500-2000 words)
- competitive-matrix.csv (feature comparison)
- positioning-recommendations.md (500-700 words)

**Output:** `/home/fitna/homelab/sprints/sprint-27/agent-prompts-optimized/ResearcherAgent-task-01-competitor-analysis.md`

✅ Prompt created (95 lines)
✅ 7 measurable requirements
✅ 5 success criteria
✅ Shared context references (@project-context.md, @brand-guidelines.md)
✅ Copy-pasteable execution block included

Ready for ResearcherAgent to execute!
```

## Integration Points

### Related Skills
- **Agent 1 - SprintManager**: Use to allocate generated prompts to sprint board
- **Agent 4 - DailyProgressReporter**: Track prompt execution progress
- **Agent 8 - SOPExecutor**: Execute prompts as standard procedures

### External Tools
- Shared context files: `/home/fitna/homelab/sprints/sprint-{NUMBER}/shared-context/`
- Agent prompt templates: `/home/fitna/homelab/sprints/sprint-26/agent-prompts/`
- Output directories: `/home/fitna/homelab/shared/{content,research,dashboards}/`

### Data Sources
- Agent definitions: `/home/fitna/homelab/AGENTS.md`
- Sprint plan: `/home/fitna/homelab/sprints/sprint-{NUMBER}/SPRINT_PLAN.md`
- Roadmap: `/home/fitna/homelab/ROADMAP_1M_18MONTHS.md`

## Version
v1.0 - Initial skill definition based on Sprint 26 agent prompt analysis
