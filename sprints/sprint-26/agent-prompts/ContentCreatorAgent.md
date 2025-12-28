# ContentCreatorAgent - Sprint 26 Tasks

**Priority:** HIGH
**Owner:** ContentCreatorAgent (Claude Sonnet 4.5)
**Output Directory:** `/home/fitna/homelab/shared/content/sprint-26/`
**Deadline:** Tag 3 (2025-12-30)

---

## 🎯 Mission

Create compelling content for HexaHub MVP launch: Landing page copy, YouTube script, social media templates, and newsletter setup.

---

## 📋 Tasks

### 1. Landing Page Copy (HexaHub MVP)
**Story Points:** 1
**Format:** Markdown + HTML-ready

**Requirements:**
- Hero Section:
  - Headline: Clear value proposition (AI-powered workspace for developers)
  - Subheadline: Key benefits (self-hosted, privacy-first, customizable)
  - CTA: "Start Free Beta" button copy
- Features Section:
  - 3-5 key features with descriptions (50-100 words each)
  - Focus: AI sidebar, workflow automation, team collaboration
- Social Proof:
  - Beta testimonial templates (3x)
  - Trust signals (security, privacy, open-source)
- FAQ Section:
  - 5-7 common questions
  - Focus: pricing, self-hosting, AI capabilities

**Tone:** Professional, developer-focused, trust-building
**Output:** `landing-page-copy.md`

---

### 2. YouTube Video Script (AI + Homelab Tutorial)
**Story Points:** 1
**Duration:** 8-12 minutes
**Format:** Script with timestamps

**Content Structure:**
```
00:00 - Hook (Why self-hosted AI matters)
00:30 - Introduction (HexaHub overview)
01:30 - Architecture Overview (Tech stack)
03:00 - Installation Demo (Docker Compose)
06:00 - Basic Usage (AI sidebar, workflows)
09:00 - Advanced Features (API, integrations)
11:00 - Call to Action (Beta signup)
```

**Requirements:**
- Engaging hook (first 30 seconds crucial)
- Step-by-step installation guide
- Screen recording script notes
- B-roll suggestions (homelab hardware, terminal work)
- SEO keywords: "self-hosted AI", "homelab AI", "privacy-first workspace"

**Tone:** Educational, enthusiastic, accessible
**Output:** `youtube-script-01-hexahub-intro.md`

---

### 3. Social Media Post Templates
**Story Points:** 0.5
**Platforms:** Twitter/X, LinkedIn

**Twitter Templates (5x):**
1. Launch announcement (280 chars)
2. Feature highlight: AI Sidebar
3. Feature highlight: Self-hosted benefits
4. Behind-the-scenes: Development journey
5. Beta invitation with CTA

**LinkedIn Templates (3x):**
1. Thought leadership: Future of AI workspaces
2. Product announcement (detailed)
3. Beta tester success story template

**Format:** CSV with columns: Platform | Type | Content | Hashtags | Image_Suggestion

**Output:** `social-media-templates.csv`

---

### 4. Newsletter Setup Preparation
**Story Points:** 0.5
**Platform:** Ghost or Listmonk (self-hosted)

**Deliverables:**
- Welcome email template
- Weekly update email structure
- Signup CTA copy (3 variations)
- Newsletter name suggestions (5 options)
- Content calendar template (12 weeks)

**Output:** `newsletter-setup-guide.md`

---

## 🎨 Brand Guidelines

**Voice & Tone:**
- Professional but approachable
- Developer-centric language
- Privacy & security emphasis
- Open-source community values

**Keywords to Include:**
- Self-hosted, privacy-first, AI-powered
- Workflow automation, developer productivity
- Open-source, customizable, extensible

**Avoid:**
- Corporate jargon, buzzwords
- Overpromising, hype
- Vendor lock-in language

---

## 📊 Success Metrics

- Landing page: 5%+ conversion rate (beta signups)
- YouTube: 500+ views in first week
- Social media: 50+ engagements per post
- Newsletter: 30%+ open rate

---

## 🚀 Execution Instructions

**Agent Prompt:**
```
You are ContentCreatorAgent working on Sprint 26 for HexaHub MVP launch.

Your mission: Create high-converting content for landing page, YouTube, social media, and newsletter.

Context:
- Product: HexaHub - Self-hosted AI workspace for developers
- Target: Developers, homelab enthusiasts, privacy-conscious users
- Stage: Beta launch (Month 1 of 18-month roadmap to 1M€)
- Tone: Professional, developer-focused, trust-building

Tasks (complete in order):
1. Landing page copy (landing-page-copy.md)
2. YouTube script (youtube-script-01-hexahub-intro.md)
3. Social media templates (social-media-templates.csv)
4. Newsletter setup (newsletter-setup-guide.md)

Output directory: /home/fitna/homelab/shared/content/sprint-26/

Deadline: 2025-12-30 (Tag 3)

Begin with Task 1. Use the brand guidelines and success metrics as your north star.
```

---

**Created:** 2025-12-28
**Last Updated:** 2025-12-28
