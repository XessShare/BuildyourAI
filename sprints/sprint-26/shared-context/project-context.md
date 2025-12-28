# HexaHub Project Context

## Product Overview

HexaHub is a self-hosted AI workspace designed for developers who prioritize data sovereignty and infrastructure control. Unlike cloud-based alternatives such as Cursor, GitHub Copilot, and Codeium, HexaHub deploys entirely on your own infrastructure - from homelab servers to enterprise Kubernetes clusters. The platform integrates multiple AI providers (OpenAI, Anthropic, and local LLMs via Ollama) into a unified developer experience, eliminating vendor lock-in while providing context-aware code assistance, workflow automation, and team collaboration features.

## Value Proposition

1. **True Self-Hosting:** Complete stack deployment on your infrastructure - not just API key integration. Your code context, prompts, and data never leave your servers.
2. **Multi-Model AI Freedom:** Switch between OpenAI GPT-4, Claude, and local LLMs (Mistral, Llama) without changing workflows. Optimize for cost, privacy, or capability per use case.
3. **Open-Source Architecture:** Extensible plugin system, transparent codebase, and community-driven development. No black-box AI processing.

## Tech Stack

**Backend:**
- FastAPI + PostgreSQL + Redis
- Multi-model AI integration (OpenAI, Anthropic, Ollama local LLMs)
- Authentik (SSO/Auth with OIDC/SAML)

**Frontend:**
- Next.js 14 + TypeScript
- TailwindCSS + Shadcn/UI

**Infrastructure:**
- Docker Compose (Staging: RTX1080 homelab)
- K3s (Future: Cloud migration via EKS/GKE)
- Prometheus + Grafana (Monitoring & Observability)

## Target Audience

1. **Primary:** Privacy-Conscious Developers (30-45, self-hosting advocates)
   - Pain points: Code transmitted to third-party servers, vendor lock-in, subscription fatigue
   - Use cases: AI-assisted coding without data exposure, local model experimentation, team collaboration

2. **Secondary:** Homelab Enthusiasts (tech-savvy infrastructure builders)
   - Pain points: Cloud AI tools with no self-host option, fragmented dev tooling, expensive GPU utilization
   - Use cases: GPU-accelerated local AI workspace, unified home server stack, learning AI infrastructure

3. **Tertiary:** Small Dev Teams (2-10 people, remote-first startups)
   - Pain points: Per-seat SaaS costs, compliance concerns, context switching between tools
   - Use cases: Team AI workspace under $200/month, shared context across projects, custom integrations

## Key Differentiators (vs. Cursor, Copilot, Codeium, Tabnine)

1. **True Self-Hosting:** Not just "bring your API key" - full backend, database, and AI orchestration on your servers
2. **Multi-Model AI:** OpenAI + Anthropic + Ollama local models - choose per task, no vendor lock-in
3. **Open-Source Friendly:** Apache 2.0 core, plugin marketplace, community contributions welcome
4. **Privacy-First Design:** Zero telemetry by default, air-gapped deployment option, GDPR-ready

## Market Context (2025)

The AI coding tools market has grown significantly with GitHub Copilot (1.3M+ paid subscribers), Cursor ($400M valuation), and Codeium (500K+ users). However, privacy concerns drive 23% of enterprise developers to seek self-hosted alternatives. The open-source LLM ecosystem (Llama 3, Mistral, CodeLlama) enables production-quality local inference, reducing dependency on cloud APIs.

## Business Model

- **Freemium:** Self-hosted always free, cloud-hosted tiers at $49-$199/month
- **Target:** 1M EUR ARR in 18 months
- **Phase 1 (Month 1-3):** MVP + Beta (100 users, 1.5K EUR MRR)
- **Phase 2 (Month 4-6):** Growth & PMF (50 customers, 9.5K EUR MRR)
- **Phase 3 (Month 7-18):** Scale (15K users, 83K EUR MRR)

## Reference Documentation

- Full Roadmap: `/home/fitna/homelab/ROADMAP_1M_18MONTHS.md`
- Sprint 26 Plan: `/home/fitna/homelab/sprints/sprint-26/SPRINT_PLAN.md`
- Brand Guidelines: `/home/fitna/homelab/sprints/sprint-26/shared-context/brand-guidelines.md`
