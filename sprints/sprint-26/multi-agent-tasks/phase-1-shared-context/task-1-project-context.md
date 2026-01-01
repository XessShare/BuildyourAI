# Task 1: HexaHub Project Context

**Agent:** ResearcherAgent
**Model:** Perplexity (Deep Research)
**Output:** `/home/fitna/homelab/sprints/sprint-26/shared-context/project-context.md`
**Length:** 60 lines

---

## Mission

Research and create a comprehensive HexaHub project context document that will be included in all 24 Sprint 26 agent prompts. This is the foundation context that every agent needs.

---

## Research Requirements

Use Perplexity to research:

1. **Self-hosted AI workspace market (2025)**
   - Current state of AI-powered development tools
   - Competitors: Cursor, GitHub Copilot, Codeium, Tabnine
   - Self-hosting trend in developer tools

2. **Privacy-first AI tools**
   - Why developers want self-hosted solutions
   - Data sovereignty concerns
   - Enterprise vs. individual use cases

3. **Multi-model AI architecture**
   - OpenAI, Anthropic, local LLMs (Ollama, LM Studio)
   - Vendor lock-in problems
   - Open-source AI model ecosystem

---

## Output Structure (60 lines)

```markdown
# HexaHub Project Context

## Product Overview
[4-5 sentences on what HexaHub is - self-hosted AI workspace for developers]

## Value Proposition
[3 key benefits - self-hosting, privacy, multi-model]

## Tech Stack
**Backend:**
- FastAPI + PostgreSQL + Redis
- Multi-model AI integration (OpenAI, Anthropic, local LLMs)
- Authentik (SSO/Auth)

**Frontend:**
- Next.js + TypeScript
- TailwindCSS

**Infrastructure:**
- Docker Compose (Staging: RTX1080 homelab)
- K3s (Future: Cloud migration)
- Prometheus + Grafana (Monitoring)

## Target Audience
1. **Primary:** Developers (30-45, privacy-conscious, self-hosting advocates)
   - Pain points: [list 2-3]
   - Use cases: [list 2-3]

2. **Secondary:** Homelab enthusiasts (tech-savvy, DIY infrastructure)
   - Pain points: [list 2-3]
   - Use cases: [list 2-3]

3. **Tertiary:** Small dev teams (2-10 people, remote-first)
   - Pain points: [list 2-3]
   - Use cases: [list 2-3]

## Key Differentiators (vs. Cursor, Copilot, etc.)
1. **True Self-Hosting:** Not just "bring your own API key" - full stack deployment
2. **Multi-Model AI:** OpenAI, Anthropic, local LLMs (no vendor lock-in)
3. **Open-Source Friendly:** Extensible architecture, plugin system
4. **Privacy-First:** Data never leaves your infrastructure

## Business Model
- Freemium: Self-hosted free, cloud-hosted paid ($49-$199/mo)
- Target: 1M€ ARR in 18 months
- Phase 1 (Month 1): MVP + Beta (100 users)
- Phase 2 (Month 2-6): Growth (1.5K€ → 15K€ MRR)
- Phase 3 (Month 7-18): Scale (15K€ → 83K€ MRR)

## Reference
- Full Roadmap: `/home/fitna/homelab/ROADMAP_1M_18MONTHS.md`
- Sprint 26 Plan: `/home/fitna/homelab/sprints/sprint-26/SPRINT_PLAN.md`
```

---

## Success Criteria

- [ ] 60 lines exactly (±5 lines acceptable)
- [ ] Factually accurate (research-backed)
- [ ] Clear value proposition for developers
- [ ] Realistic target audience pain points
- [ ] Compelling differentiators vs. competitors
- [ ] Ready to be included in 24 agent prompts

---

## Execution Prompt (For Perplexity)

```
You are ResearcherAgent using Perplexity to research the self-hosted AI workspace market.

Your mission: Create a comprehensive HexaHub project context document (60 lines).

Research focus:
1. Self-hosted AI tools market in 2025
2. Privacy-first developer tools trend
3. Multi-model AI architecture benefits
4. Target audience pain points (developers, homelab enthusiasts)

Product: HexaHub
- Self-hosted AI workspace for developers
- Tech: FastAPI, PostgreSQL, Next.js, Authentik
- Differentiator: True self-hosting + multi-model AI + open-source
- Business: Freemium, 1M€ ARR target in 18 months

Output format: Use the structure template above.
Length: 60 lines (strict).

Write the complete project-context.md file now. Use factual research, not generic marketing speak.
```
