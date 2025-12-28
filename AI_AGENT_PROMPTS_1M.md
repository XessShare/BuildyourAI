# 💬 AI Agent Prompts - 1M€ Roadmap

**Purpose:** Schnelle, fokussierte Prompts für AI Agent Tasks  
**Usage:** Copy-paste für maximale Effizienz

---

## 🚀 Phase 1: Foundation (M1-3)

### Week 1-2: Core Setup

```
@DeploymentOrchestrator
Task: Setup HexaHub MVP Backend
Stack: FastAPI + PostgreSQL + Redis
Requirements:
- User auth (JWT)
- CRUD endpoints (Pages, Databases)
- Swagger docs
- Docker Compose
Deadline: 2 weeks
```

```
@ContentCreatorAgent
Task: Landing Page Copy
Product: Fitnaai (AI Workspace)
USP: Self-hosted Notion + AI Assistant
Target: Developers, Privacy-conscious users
Tone: Professional, Technical
Deliverable: Headline, 3 features, CTA
```

```
@ResearcherAgent
Task: Competitor Analysis
Competitors: Notion, Sider AI, n8n
Focus: Pricing, Features, Market gaps
Output: Markdown table comparison
```

### Week 3-4: Beta Launch

```
@CommunicatorAgent
Task: Beta User Outreach
Channels: Reddit (r/selfhosted), HackerNews, ProductHunt
Message: Beta invite for self-hosted AI workspace
Target: 100 outreach → 10 signups
Template: Personalized, value-first
```

```
@AnalystAgent
Task: Landing Page Analytics Setup
Tools: PostHog (self-hosted)
Metrics: Visitors, Signups, Conversion rate
Dashboard: Real-time
Alert: < 2% conversion rate
```

### Week 5-8: Content Engine

```
@ContentCreatorAgent
Task: YouTube Video Script
Topic: "Build Your Own AI Assistant - Self-Hosted"
Duration: 10 minutes
Structure: Hook, Problem, Solution, Demo, CTA
Tone: Educational, Enthusiastic
Target: 1K views in first week
```

```
@ResearcherAgent
Task: SEO Keyword Research
Niche: Self-hosted AI, Productivity tools
Goal: 10 keywords (low competition, high intent)
Output: Title ideas + content outline
Tool: Perplexity
```

---

## 🎯 Phase 2: Validation (M4-6)

### Product Hunt Launch

```
@ProjectManagerAgent
Task: Product Hunt Launch Plan
Timeline: 2 weeks prep → Launch day
Checklist:
- Product page optimization
- Maker story
- First 50 users testimonials
- Social media blitz
- Hunter outreach (5 candidates)
Goal: Top 5 of the Day
```

```
@CommunicatorAgent
Task: PH Launch Social Posts
Platforms: Twitter, LinkedIn, HackerNews
Frequency: Pre-launch (3 days), Launch day (hourly), Post (3 days)
Content: Teasers, Behind-the-scenes, Launch announcement
Tone: Excited, Authentic
```

### Consulting Package

```
@AnalystAgent
Task: Consulting Pricing Model
Services: Setup, Training, Custom integration
Research: Market rates (competitors)
Output: 3 tiers with pricing, deliverables, timeframe
Margin: 70%+
```

---

## 📈 Phase 3: Scale (M7-9)

### Automation

```
@DeploymentOrchestrator
Task: K8s Migration Plan
Current: Docker Compose on VPS
Target: Kubernetes (EKS/GKE)
Requirements:
- Auto-scaling (HPA)
- Zero-downtime deploys
- Cost optimization
- Monitoring (Prometheus)
Timeline: 4 weeks
Budget: < 500€/mo
```

```
@VerifierAgent
Task: Automated Testing Suite
Coverage: API endpoints, Auth, CRUD
Tools: Pytest + FastAPI TestClient
CI/CD: GitHub Actions
Target: 80% coverage
Alert: Failing tests block deployment
```

### Team Hire

```
@ResearcherAgent
Task: Developer Job Posting
Role: Full-Stack (FastAPI + Next.js)
Salary: 50K€/yr (remote)
Skills: Python, React, Docker, AI/ML
Platforms: RemoteOK, AngelList, LinkedIn
Deliverable: Job description + screening questions
```

---

## 🚀 Phase 4-6: Acceleration (M10-18)

### Fundraising

```
@AnalystAgent
Task: Investor Deck
Slides: Problem, Solution, Market, Traction, Team, Ask
Traction: MRR chart, User growth, Retention
Ask: 250K€ Seed @ 2M€ valuation
Deliverable: 12-slide deck (PDF + Pitch)
```

```
@ResearcherAgent
Task: Investor Outreach List
Focus: SaaS, AI, Privacy-tech
Stage: Seed (100K-500K€)
Geography: EU-based
Output: 50 investors (email, LinkedIn, focus)
```

### Enterprise Sales

```
@CommunicatorAgent
Task: Enterprise Sales Email
Target: CTOs, IT Directors (500+ employee companies)
Pitch: Self-hosted AI for enterprise security
USP: On-premise, GDPR-compliant, White-label
CTA: Demo call booking
Template: Personalized (company research)
```

---

## 🤖 Daily Operations Prompts

### Daily Standup

```
@ProjectManagerAgent
Task: Daily Standup Summary
Input: Team updates (async)
Output: 
- Progress vs. sprint goal
- Blockers identified
- Action items
- Velocity tracking
Format: Markdown, < 200 words
```

### Content Calendar

```
@ContentCreatorAgent
Task: Weekly Content Calendar
Platforms: Twitter (daily), LinkedIn (3x/week), Blog (1x/week), YouTube (1x/week)
Topics: AI, Self-hosting, Productivity, Homelab
Format: Calendar view with copy drafts
Automation: Schedule via Buffer/Hootsuite
```

### Metrics Report

```
@AnalystAgent
Task: Weekly Metrics Report
Metrics:
- MRR (current, growth %)
- Customers (total, new, churn)
- Signups (funnel conversion)
- Content (views, subs, engagement)
Format: Dashboard + PDF summary
Distribution: Email (Friday 6pm)
```

---

## 🔥 Emergency Prompts

### Downtime

```
@DeploymentOrchestrator
URGENT: Production Down
1. Health check all services
2. Check logs (last 1hr)
3. Rollback if recent deploy
4. Notify users (status page)
5. Root cause analysis
Report: Incident timeline + fix
```

### Churn Alert

```
@CommunicatorAgent
URGENT: Churn > 5% this month
1. Identify churned users (exit survey)
2. Interview 5 users (why?)
3. Win-back campaign (discount offer)
4. Product feedback to dev team
Goal: < 3% churn next month
```

---

## 📊 Reporting Prompts

### Monthly Review

```
@AnalystAgent
Task: Monthly Business Review
Period: [Month]
Sections:
1. Revenue (MRR, ARR, growth)
2. Customers (total, new, churn, LTV/CAC)
3. Product (features shipped, bugs fixed)
4. Content (traffic, leads, conversions)
5. Risks & Opportunities
6. Next month goals
Format: Markdown + Charts
Audience: Internal + Advisors
```

### Investor Update

```
@ProjectManagerAgent
Task: Investor Update Email
Frequency: Monthly
Template:
- Key metrics (MRR, users, growth %)
- Highlights (wins, milestones)
- Challenges (honest assessment)
- Asks (intros, advice, feedback)
- Next month focus
Tone: Transparent, Optimistic, Data-driven
```

---

## 🎯 Growth Hacking Prompts

### Viral Loop

```
@AnalystAgent
Task: Referral Program Design
Mechanics: Give 1 month free, Get 1 month free
Tracking: Unique referral links
Target: K-factor > 1.0 (viral)
Implementation: Backend + UI + Email automation
```

### Content SEO

```
@ResearcherAgent + @ContentCreatorAgent
Task: SEO Content Cluster
Pillar: "Self-Hosted AI Tools"
Spokes: 10 articles (1500 words each)
Keywords: Long-tail, low competition
Internal linking: Hub-and-spoke model
Goal: Rank #1-5 in 3 months
```

---

## 🧪 Experimentation Prompts

### A/B Test

```
@AnalystAgent
Task: Landing Page A/B Test
Variants:
  A: "Build Your AI Workspace" (control)
  B: "Privacy-First AI Assistant" (variant)
Metric: Signup conversion
Sample: 1000 visitors per variant
Duration: 7 days
Decision: Ship winner if > 20% lift
```

### Pricing Test

```
@AnalystAgent
Task: Pricing Elasticity Study
Test: 29€ vs 39€ vs 49€ (Solo tier)
Method: Geo-based split (DE, AT, CH)
Duration: 30 days
Metric: MRR, conversion rate, churn
Goal: Optimal price point (max revenue)
```

---

## 💡 Quick Win Prompts

### Free Tool

```
@ContentCreatorAgent + @DeploymentOrchestrator
Task: AI Prompt Optimizer (Free Tool)
Feature: Improves any prompt for better AI results
Tech: Simple web form + GPT-4 API
Branding: "Powered by Fitnaai"
CTA: "Try Fitnaai for more tools"
Launch: Product Hunt, Reddit
Goal: 1K users → 2% convert to paid
```

### Case Study

```
@CommunicatorAgent
Task: Customer Success Story
Customer: [Name]
Format: Problem-Solution-Results
Metrics: Time saved, Cost reduced, ROI
Media: Written (blog) + Video (YouTube)
Distribution: Website, Newsletter, Social
Permission: Customer approval required
```

---

## 🎓 Learning Prompts

### Skill Gap

```
@ResearcherAgent
Task: Identify Skill Gaps
Areas: Product management, Growth marketing, Enterprise sales
Resources: Courses, Books, Podcasts (top 3 each)
Time: 2 hours/week learning budget
Output: Learning roadmap (3 months)
```

---

## ⚡ Template Structure

**Standard Prompt Format:**
```
@[Agent Name]
Task: [Brief title]
[Key details]
Deadline: [When]
Deliverable: [Format/Spec]
Success: [How to measure]
```

**Keep prompts:**
- ✅ Specific (clear scope)
- ✅ Actionable (agent can execute)
- ✅ Measurable (success criteria)
- ✅ Time-bound (deadline)
- ✅ Contextual (enough info)

---

## 🔗 Quick Links

- [Roadmap](/home/fitna/homelab/ROADMAP_1M_18MONTHS.md)
- [Tracker](/home/fitna/homelab/shared/dashboards/1m-roadmap-tracker.md)
- [Agents Guide](/home/fitna/homelab/AGENTS.md)
- [Sprint Manager](/home/fitna/homelab/shared/scripts/sprint-manager.sh)

---

**Usage:**
1. Find relevant prompt
2. Copy to clipboard
3. Paste in agent interface (main.py, run_agents.py)
4. Customize [placeholders]
5. Execute

**Prompts Version:** 1.0  
**Last Updated:** 2025-12-28
