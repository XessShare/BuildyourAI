# Fitnaai Landing Page Design Specification - Google AI Studio Prompt (v1.0)

**Model:** Gemini 2.0 Flash Experimental
**Token Budget:** ~1000 tokens
**Expected Output:** 120±20 lines Markdown
**Created:** 2025-12-30

---

## Usage Instructions

1. **Extract NotebookLM Insights** from: `https://notebooklm.google.com/notebook/f4992ba4-24e8-4f61-9729-445284fd5189`
2. **Replace `[INSERT NOTEBOOKLM INSIGHTS HERE]`** section below with extracted content
3. **Open Google AI Studio:** `https://aistudio.google.com/`
4. **Copy entire prompt** (from "---PROMPT START---" to "---PROMPT END---")
5. **Paste into AI Studio** → Select "Gemini 2.0 Flash Experimental"
6. **Configure:**
   - Temperature: 0.7
   - Top-K: 40
   - Top-P: 0.95
   - Max Tokens: 4096
7. **Run** and export output to: `sprints/sprint-26/design-specs/fitnaai-landing-page-spec.md`

---

## ---PROMPT START---

Generate Fitnaai Landing Page Design Specification.

**Product:** Fitnaai - AI-Powered Self-Hosting Platform
**Core Platform:** J-Jeco (Content Automation with 7 AI Agents)
**GitHub Repository:** https://github.com/XessShare/BuildyourAI
**Target Audience:** Privacy-focused developers (30-45), homelab enthusiasts
**Goal:** Beta launch, >3% conversion (visitor → GitHub star + newsletter signup)

---

### Context (from NotebookLM)

[INSERT NOTEBOOKLM INSIGHTS HERE]

**Expected sections to extract from NotebookLM:**
- Key Features (J-Jeco's 7 agents, multi-LLM support)
- Unique Value Propositions (self-hosted, privacy-first)
- GitHub Repository Highlights (code examples, tutorials)
- Moonshot Vision (100K YouTube subscribers, 1M EUR ARR)

---

### Competitors

| Competitor | Hosting | Privacy | Pricing | Open-Source |
|------------|---------|---------|---------|-------------|
| **Cursor** | Cloud-only | Data sent to cloud | $20/mo | No |
| **GitHub Copilot** | Cloud-only | Data sent to GitHub | $10/mo | No |
| **Codeium** | Freemium | Hybrid (partial local) | Free + $12/mo Pro | Partial |

---

### Differentiators (Fitnaai / J-Jeco)

✅ **True Self-Hosting** - Runs on your Proxmox/Docker/K3s infrastructure
✅ **Multi-Model AI** - GPT-4, Claude, Gemini, Ollama (local) - no vendor lock-in
✅ **7 AI Agents** - Parallel execution:
   1. ContentCreator
   2. Researcher
   3. Verifier
   4. Analyst
   5. ProjectManager
   6. Communicator
   7. DeploymentOrchestrator
✅ **Open-Source Core** - Apache 2.0 license
✅ **Privacy-First** - Code & data never leave your servers
✅ **Developer-First** - Cmd+K, keyboard shortcuts, API-first

---

### Brand Voice Guidelines

**DO:**
- Professional, developer-to-developer tone
- Technically accurate (assume developer knowledge)
- Direct & clear (no fluff, no marketing speak)
- Privacy-conscious messaging
- Emphasize: Self-hosted, privacy-first, AI-powered

**DON'T:**
- Use buzzwords: "Revolutionary", "game-changing", "disruptive", "synergy", "10× your productivity"
- Overpromise: "Never write code again", "Replace your entire team"
- Use excessive emojis or exclamation marks

**Good Example:** "HexaHub runs on your infrastructure. Your data never leaves your servers."
**Bad Example:** "Revolutionary AI that will 10× your productivity and change everything!"

---

### Requirements

#### **1. Hero Section**
- **Headline:** <10 words, emphasize "Self-Hosted AI Automation"
- **Subheadline:** Mention 7 AI agents, multi-LLM support (20-30 words)
- **CTA Primary:** "Explore on GitHub" (link to XessShare/BuildyourAI)
- **CTA Secondary:** "Join Beta Waitlist"
- **Trust Signals:**
  - GitHub stars count badge
  - "100% Self-Hosted" badge
  - "Open-Source" badge (Apache 2.0)
- **Visual Suggestion:** Architecture diagram (7 agents + LLM connections)
- **Layout:** Full-width, centered content, left 60% (text), right 40% (visual)

---

#### **2. Features Section (6 Cards)**

**Grid Layout:** 3 columns (desktop), 2 columns (tablet), 1 column (mobile)

**Card 1: 7 AI Agents**
- Icon: Bot/Robot icon
- Title: "7 Specialized AI Agents"
- Description: Content, Research, Verify, Analyze, PM, Communicate, Deploy - working in parallel
- Tech Note: LangChain + LangGraph orchestration

**Card 2: Multi-LLM Support**
- Icon: Network/Cloud icon
- Title: "Multi-Model AI"
- Description: GPT-4, Claude 3, Gemini 2.0, Ollama (local) - no vendor lock-in
- Tech Note: Switch models freely via API

**Card 3: Self-Hosted Infrastructure**
- Icon: Server/Database icon
- Title: "True Self-Hosting"
- Description: Runs on Proxmox, Docker, K3s - your infrastructure, your control
- Tech Note: No external dependencies

**Card 4: Privacy-First**
- Icon: Shield/Lock icon
- Title: "Privacy & Data Sovereignty"
- Description: Code & data never leave your servers - GDPR-ready by design
- Tech Note: Zero telemetry, full control

**Card 5: Open-Source Core**
- Icon: Code/GitHub icon
- Title: "Open-Source Core"
- Description: Apache 2.0 license - community-driven development
- Tech Note: GitHub: XessShare/BuildyourAI

**Card 6: Developer Experience**
- Icon: Terminal/Keyboard icon
- Title: "Developer-First"
- Description: Cmd+K command palette, keyboard shortcuts, API-first design
- Tech Note: Built by developers, for developers

---

#### **3. GitHub Repository Showcase**

**Section Title:** "Explore the Codebase"
**Layout:** 2-column grid

**Left Column: Repository Stats**
- Lines of Code badge
- GitHub Stars badge
- Contributors badge
- Last Commit timestamp
- License badge (Apache 2.0)

**Right Column: Highlighted Directories**
1. **`/agents/`** - 11 specialized AI agent implementations
2. **`/orchestration/`** - Parallel execution engine (LangChain + LangGraph)
3. **`/visualization/`** - Mermaid diagrams & mindmap generators
4. **`/examples/`** - Multi-model workflow templates

**CTA:** "Browse Docs & Labs on GitHub" (prominent button, primary color)
**Secondary CTA:** "Star on GitHub" (GitHub icon + star count)

---

#### **4. Comparison Table**

**Table Title:** "How Fitnaai Compares"

| Feature | Fitnaai (J-Jeco) | Cursor | GitHub Copilot | Codeium |
|---------|------------------|--------|----------------|---------|
| **Hosting** | ✅ Self-Hosted | ❌ Cloud-only | ❌ Cloud-only | ⚠️ Limited |
| **Privacy** | ✅ 100% Local | ❌ Data → Cloud | ❌ Data → GitHub | ⚠️ Hybrid |
| **AI Models** | ✅ GPT-4, Claude, Gemini, Ollama | ❌ GPT-4 only | ❌ Codex only | ⚠️ Limited |
| **Pricing** | ✅ Free (Self-Hosted) | $20/mo | $10/mo | Free + $12/mo |
| **Open-Source** | ✅ Apache 2.0 | ❌ Proprietary | ❌ Proprietary | ⚠️ Partial |
| **AI Agents** | ✅ 7 Specialized | ❌ Single | ❌ Single | ❌ Single |
| **Vendor Lock-in** | ✅ None | ❌ High | ❌ High | ⚠️ Medium |

**Note Below Table:** "Comparison as of Dec 2025. Competitor features may change."

---

#### **5. Moonshot Vision (Timeline)**

**Section Title:** "The Journey Ahead"
**Subtitle:** "From beta to 100K community in 18 months"

**Timeline Visualization (Mermaid Gantt or Markdown list):**

**Month 1 (Jan 2026):** Beta Launch
- Landing Page live
- GitHub Docs complete
- Community Discord open

**Month 3 (Mar 2026):** Early Traction
- 1K GitHub Stars
- 500 YouTube Subscribers
- First 100 self-hosted deployments

**Month 6 (Jun 2026):** Web-App Launch
- Dashboard UI (Next.js + Shadcn/UI)
- Command Palette (Cmd+K)
- 5K GitHub Stars

**Month 12 (Dec 2026):** Mobile Apps
- iOS App (SwiftUI)
- Android App (Jetpack Compose)
- 10K YouTube Subscribers

**Month 18 (Jun 2027):** Moonshot Achieved
- 100K YouTube Subscribers
- 1M EUR ARR (sponsorships, courses, consulting)
- Community-driven development at scale

**CTA:** "Join the Journey" (Newsletter signup)

---

#### **6. Pricing Tiers**

**3-Tier Pricing Table:**

**Free (Self-Hosted)** - $0/forever
- ✅ All 7 AI agents
- ✅ Unlimited usage (your infrastructure)
- ✅ Community support (GitHub Discussions)
- ✅ Apache 2.0 license
- ✅ Full source code access
- **CTA:** "Get Started (GitHub)"

**Cloud Pro (Future)** - $49/mo
- ✅ Everything in Free, plus:
- ✅ Managed hosting (no setup)
- ✅ Auto-updates
- ✅ Priority support (email)
- ✅ 99.9% uptime SLA
- **Badge:** "Coming Soon"
- **CTA:** "Join Waitlist"

**Enterprise (Future)** - $199/mo
- ✅ Everything in Cloud Pro, plus:
- ✅ Dedicated infrastructure
- ✅ Custom AI model fine-tuning
- ✅ SSO/SAML integration
- ✅ 24/7 support (Slack)
- ✅ SLA with credits
- **Badge:** "Coming Q2 2026"
- **CTA:** "Contact Sales"

**Note:** "Self-Hosted tier is free forever. Cloud tiers fund open-source development."

---

#### **7. Social Proof**

**GitHub Stars:** Dynamic badge showing current count
**Metrics (Placeholder):**
- "X developers self-hosting J-Jeco"
- "Y API calls processed"
- "Z hours of AI automation"

**Testimonials (3 Beta User Quotes - Placeholder):**

**Quote 1:**
> "Finally, an AI platform I can self-host. No more vendor lock-in, no more data privacy concerns."
>
> — **Max M.**, Senior DevOps Engineer

**Quote 2:**
> "The 7-agent architecture is brilliant. Research, verification, and content creation all happen in parallel."
>
> — **Sarah K.**, Technical Writer

**Quote 3:**
> "Switching between GPT-4 and Claude locally without API limits? Game changer for my homelab."
>
> — **Alex T.**, ML Engineer

---

#### **8. FAQ (6 Questions)**

**1. How is Fitnaai different from Cursor?**
- Answer: Cursor is cloud-only with vendor lock-in. Fitnaai (J-Jeco) is self-hosted, open-source, and supports multiple AI models (GPT-4, Claude, Gemini, Ollama).

**2. What hardware do I need to self-host J-Jeco?**
- Answer: Minimum: 4 CPU cores, 8GB RAM, 50GB storage. Recommended: 8+ cores, 16GB+ RAM, NVMe SSD. Runs on Proxmox, Docker, K3s, or bare metal.

**3. Can I use GPT-4 in self-hosted mode?**
- Answer: Yes, via OpenAI API (bring your own key). Also supports Claude (Anthropic), Gemini (Google), and local Ollama models (Llama, Mistral).

**4. Is the platform open-source?**
- Answer: Yes, core platform is Apache 2.0 licensed on GitHub (XessShare/BuildyourAI). Community contributions welcome.

**5. How do I deploy to my homelab?**
- Answer: Docker Compose (easiest), Kubernetes/K3s (scalable), or LXC containers (Proxmox). Full docs on GitHub.

**6. Which AI models are supported?**
- Answer: GPT-4, GPT-4 Turbo, Claude 3 (Opus, Sonnet, Haiku), Gemini 2.0 Flash, Ollama (Llama 3, Mistral, CodeLlama). Model switching via config.

---

#### **9. Newsletter Signup**

**Section Title:** "Get Updates on Fitnaai Development"
**Subtitle:** "100% privacy-focused, no spam, unsubscribe anytime"

**Form Fields:**
- Email (required)
- Checkbox: "I want to receive beta access invitations"

**CTA Button:** "Join Newsletter"
**Badge:** "🔒 Privacy-First - We never share your email"

**Post-Signup Message:** "Thanks! Check your inbox for confirmation."

---

#### **10. Footer**

**4-Column Layout:**

**Column 1: Product**
- Features
- Pricing
- Documentation (GitHub)
- Changelog

**Column 2: Resources**
- GitHub Repository
- Tutorials & Guides
- Blog (Medium/Dev.to)
- YouTube Channel

**Column 3: Company**
- About Fitnaai
- Moonshot Vision
- Newsletter
- Contact

**Column 4: Community**
- Discord Server
- GitHub Discussions
- YouTube (100K goal)
- Twitter/X

**Bottom Footer:**
- Copyright: "© 2025 Fitnaai. Apache 2.0 License."
- Links: Privacy Policy | Terms of Service | Code of Conduct
- Badge: "Built with ❤️ by the open-source community"

---

### Output Format (Markdown Structure)

Your output should follow this structure:

```markdown
# Fitnaai Landing Page Design Specification

**Platform:** Web (Next.js 14)
**Design System:** Shadcn/UI + TailwindCSS
**Theme:** Dark mode default (VS Code colors)
**Target:** Privacy-focused developers, homelab enthusiasts

## 1. Hero Section
### Layout
[Describe 60/40 split, full-width container]

### Copy
**Headline:** [<10 words]
**Subheadline:** [20-30 words]

### CTAs
- Primary: "Explore on GitHub" (bg-blue-600)
- Secondary: "Join Beta Waitlist" (border-blue-600)

### Trust Signals
- [GitHub stars badge]
- [100% Self-Hosted badge]
- [Open-Source badge]

### Visual
[Architecture diagram suggestion: 7 agents connected to LLM APIs]

---

## 2. Features Section (6 Cards)
[3-column grid on desktop]

### Card 1: 7 Specialized AI Agents
[Icon, title, description, tech note]

[Continue for all 6 cards...]

---

## 3. GitHub Repository Showcase
[2-column layout: stats + directories]

---

## 4. Comparison Table
[Full table with 7 rows × 5 columns]

---

## 5. Moonshot Vision Timeline
[Timeline with 5 milestones]

---

## 6. Pricing Tiers
[3-tier comparison table]

---

## 7. Social Proof
[GitHub badge + 3 testimonials]

---

## 8. FAQ (6 Questions)
[Q&A format with expand/collapse]

---

## 9. Newsletter Signup
[Email form with privacy badge]

---

## 10. Footer
[4-column footer layout]

---

## Component Library (Shadcn/UI)

**Components to use:**
- Button (primary, secondary, ghost variants)
- Card (with header, content, footer)
- Badge (success, info, neutral, warning)
- Separator
- Tabs (for pricing tiers)
- Accordion (for FAQ)
- Input (email field)

---

## Design System Constraints

**Colors:**
- Primary: #3b82f6 (Blue)
- Secondary: #10b981 (Green)
- Background: #1e1e1e (VS Code Dark)
- Text: #e0e0e0 (Light gray)
- Code: #d4d4d4 (VS Code text)

**Typography:**
- Sans-serif: Inter (headings, body)
- Monospace: JetBrains Mono (code, tech specs)

**Spacing:**
- Base: 4px
- Scale: 8px, 16px, 24px, 32px, 48px, 64px

**Component Styling:**
- Corner Radius: 8px (buttons, cards)
- Border Width: 1px
- Shadow: soft (rgba(0,0,0,0.1))

---

## Accessibility Notes

**WCAG 2.1 AA Compliance:**
- Contrast ratios: ≥4.5:1 (text), ≥3:1 (UI elements)
- Keyboard navigation: Tab, Enter, Escape
- Focus indicators: 2px outline, visible on all interactive elements
- Screen reader labels: All buttons, links, form fields
- Alt text: All images, icons (decorative marked as aria-hidden)

**Mobile Responsive:**
- Breakpoints: 640px (mobile), 768px (tablet), 1024px (desktop)
- Touch targets: ≥44px × 44px
- Font scaling: 16px base (mobile), 18px (desktop)

---

## GitHub Integration Notes

**Embed GitHub Stats:**
- Stars: Use shields.io badge or GitHub API
- Contributors: GitHub API `/repos/XessShare/BuildyourAI/contributors`
- Last Commit: GitHub API `/repos/XessShare/BuildyourAI/commits`

**Dynamic Badges:**
```html
<img src="https://img.shields.io/github/stars/XessShare/BuildyourAI?style=social" alt="GitHub stars" />
```

**Repository Links:**
- Main: `https://github.com/XessShare/BuildyourAI`
- Docs: `https://github.com/XessShare/BuildyourAI#readme`
- Issues: `https://github.com/XessShare/BuildyourAI/issues`
- Discussions: `https://github.com/XessShare/BuildyourAI/discussions`

---

## Conversion Optimization Notes

**5+ CTAs Total:**
1. Hero: "Explore on GitHub" (primary)
2. Hero: "Join Beta Waitlist" (secondary)
3. GitHub Showcase: "Browse Docs & Labs on GitHub"
4. GitHub Showcase: "Star on GitHub"
5. Pricing: "Get Started (GitHub)"
6. Newsletter: "Join Newsletter"
7. Footer: "GitHub Repository" link

**Trust Signals:**
- GitHub stars badge (social proof)
- "100% Self-Hosted" badge (privacy)
- "Open-Source" badge (transparency)
- Testimonials (user validation)
- Comparison table (differentiation)

**Mobile-Responsive:**
- Hero: Stack vertically on mobile (headline → visual → CTAs)
- Features: 1 column on mobile, 2 on tablet, 3 on desktop
- Table: Horizontal scroll on mobile with sticky first column
- Footer: 1 column on mobile, 2 on tablet, 4 on desktop
```

---

### Length Constraint
**120 lines ±20** (100-140 lines total in final markdown)

---

### Style Guidelines
- **Tone:** Technical, developer-to-developer
- **Voice:** Professional, direct, no marketing fluff
- **Language:** Assume developer knowledge (API, Docker, K3s, LLM, etc.)
- **Clarity:** Short sentences, bullet points, scannable sections

---

### Success Criteria

Before submitting output, validate:

✅ **Brand Voice:** No "revolutionary", "game-changing", "synergy"
✅ **Competitor Differentiation:** Self-hosted vs. Cloud-only clearly stated
✅ **GitHub Featured:** Repo prominently featured in ≥3 sections
✅ **Conversion-Optimized:** ≥5 CTAs (GitHub, Newsletter, Beta)
✅ **Mobile-Responsive:** Notes included for all breakpoints
✅ **Privacy-First:** Messaging emphasized throughout
✅ **J-Jeco's 7 Agents:** Clearly explained with names
✅ **Moonshot Timeline:** Included with 5 milestones
✅ **Accessibility:** WCAG 2.1 AA notes provided
✅ **Design System:** Colors, fonts, spacing constraints specified

---

**Begin now. Output complete Fitnaai landing page design specification following the structure above.**

## ---PROMPT END---
