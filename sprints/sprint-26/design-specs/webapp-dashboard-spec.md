# HexaHub Web-App Dashboard Design Specification

**Generated:** 2025-12-29
**Target Audience:** Privacy-conscious developers (post-authentication)
**Purpose:** MVP core dashboard experience
**Tech Stack:** Next.js 14 (App Router), TailwindCSS, Shadcn/UI, Radix Primitives
**Performance Target:** <1s initial load, <100ms interaction response

---

## Layout Structure

### Overall Architecture
**Pattern:** Sidebar + Main Content + AI Assistant Panel (3-column)

```
┌─────────────────────────────────────────────────────────────────┐
│ Top Bar (User Profile, Notifications, Settings)                │
├────────┬──────────────────────────────────────┬────────────────┤
│        │                                      │                │
│ Side   │                                      │ AI Assistant   │
│ bar    │      Main Content Area               │ Panel          │
│        │      (Projects, Activity, etc.)      │ (Toggle-able)  │
│ Nav    │                                      │                │
│        │                                      │                │
│        │                                      │                │
│        │                                      │                │
└────────┴──────────────────────────────────────┴────────────────┘
```

### Sidebar Navigation (Persistent, Left, 240px width)
**State:** Always visible on desktop, collapsible on tablet/mobile
**Components:**
- Logo + App Name (top)
- Navigation Links (vertical list)
- Project Switcher (dropdown)
- Collapse Button (bottom, icon-only when collapsed)

**Navigation Items:**
1. 🏠 Home (Dashboard overview)
2. 💬 AI Chat (Conversations)
3. 📁 Projects (List view)
4. ⚙️ Settings (User preferences)
5. 📊 Analytics (Usage stats, optional)

**Collapsed State:** 64px width, icons only, tooltips on hover

---

### Top Bar (Horizontal, Full Width, 64px height)
**Components (Left → Right):**
1. **Project Name** (current active project, click to switch)
2. **Spacer** (flex-grow)
3. **Cmd+K Search** (button: "Search... ⌘K")
4. **Notifications** (bell icon, badge count)
5. **Theme Toggle** (sun/moon icon)
6. **User Profile** (avatar, dropdown menu)

**User Profile Dropdown:**
- View Profile
- Settings
- API Keys
- Billing (Cloud Pro users only)
- Logout

---

### Main Content Area (Center, Flexible Width)
**Padding:** px-8 py-6
**Background:** `#1e1e1e` (dark mode default)
**Max Width:** 1400px (centered)

**Responsive:**
- Desktop: Full width (minus sidebars)
- Tablet: Sidebar collapses, full width
- Mobile: Sidebar hidden (hamburger menu), full width

---

### AI Assistant Panel (Right, 400px width, Toggle-able)
**State:** Visible by default, collapsible via button
**Components:**
- Header: "AI Assistant" + Model Selector Dropdown
- Chat Messages (scrollable)
- Input Field + Send Button
- Collapse Button (icon: chevron-right)

**Collapsed State:** Hidden, main content expands to full width
**Re-Open:** Button in top bar (icon: sparkles "✨ AI Chat")

---

## Core Views (Main Content Area)

### View 1: Dashboard Home

#### Layout
**Structure:** 3-column grid (desktop), 1-column stack (mobile)

#### Sections

**Section 1: Greeting (Full Width)**
```
"Good morning, [User Name] 👋"
Dynamic based on time: morning (6-12), afternoon (12-18), evening (18-6)
```

**Section 2: Quick Actions (3 Cards, Equal Width)**

**Card 1: New AI Chat**
- Icon: MessageSquarePlus (Lucide)
- Title: "Start AI Chat"
- Description: "Ask questions, generate code, debug issues"
- CTA: "New Chat" → Opens AI Assistant Panel

**Card 2: New Project**
- Icon: FolderPlus (Lucide)
- Title: "Create Project"
- Description: "Organize code, track AI context"
- CTA: "New Project" → Modal dialog

**Card 3: Sync Data**
- Icon: RefreshCw (Lucide)
- Title: "Sync from Server"
- Description: "Update projects, chat history"
- CTA: "Sync Now" → Loading spinner, success toast

**Section 3: Recent Activity (Full Width, List)**
**Title:** "Recent Activity"
**Items (Last 5):**
```
├─ 2 minutes ago | AI Chat | "How to optimize PostgreSQL queries?"
├─ 1 hour ago    | Project Updated | "hexahub-backend" (3 files changed)
├─ Yesterday     | AI Chat | "Generate FastAPI CRUD endpoints"
├─ 2 days ago    | New Project Created | "mobile-app-ios"
└─ 3 days ago    | AI Chat | "Explain Docker networking"
```
**Format:** Timeline-style, icon + timestamp + action + context

**Section 4: Usage Stats (3 Cards, Equal Width)**

**Card 1: API Calls Today**
- Value: "47" (large font, `#3b82f6`)
- Label: "API Calls Today"
- Subtext: "23% vs. yesterday"
- Chart: Sparkline (last 7 days)

**Card 2: Active Projects**
- Value: "5"
- Label: "Active Projects"
- Subtext: "2 updated today"

**Card 3: Total Conversations**
- Value: "128"
- Label: "AI Conversations"
- Subtext: "+12 this week"

---

### View 2: AI Chat Screen

#### Layout
**Full-Width Main Content** (AI Assistant Panel hidden on this view)

#### Components

**Header:**
- Title: "AI Chat"
- Model Selector: Dropdown (GPT-4, Claude, Gemini, Llama-3-70B)
- New Chat Button: "+ New"

**Chat Messages (Scrollable, Auto-Scroll to Bottom):**

**Message Format (User):**
```
┌───────────────────────────────────────┐
│ You (2 min ago)                       │
│ How do I optimize PostgreSQL queries? │
└───────────────────────────────────────┘
```
- Background: `#2a2a2a` (slightly lighter than main)
- Border-Left: 2px `#3b82f6` (blue accent)
- Padding: p-4
- Border-Radius: rounded-lg

**Message Format (AI):**
```
┌───────────────────────────────────────────────────────┐
│ GPT-4 (1 min ago)                      [Copy] [Retry] │
│                                                        │
│ To optimize PostgreSQL queries:                       │
│                                                        │
│ 1. Use EXPLAIN ANALYZE to identify bottlenecks       │
│ 2. Add indexes on frequently queried columns         │
│                                                        │
│ ```sql                                                │
│ CREATE INDEX idx_users_email ON users(email);        │
│ ```                                                   │
│                                                        │
└───────────────────────────────────────────────────────┘
```
- Background: `#1e1e1e` (same as main)
- Border-Left: 2px `#10b981` (green accent, AI color)
- Code Blocks: Syntax highlighting (VS Code Dark+ theme)
- Actions: Copy Button, Regenerate Button (top-right)

**Input Area (Bottom, Sticky):**
```
┌─────────────────────────────────────────────────┐
│ [Attachment]  Type your message... (Cmd+Enter) │
│                                                 │
│                                        [Send →] │
└─────────────────────────────────────────────────┘
```
- Textarea: Auto-expand (max 5 lines)
- Attachment Button: Paperclip icon (future: file upload)
- Send Button: Disabled when empty, `bg-blue-600` when active
- Keyboard Shortcut: Cmd+Enter or Ctrl+Enter

**Context Menu (Long-Press / Right-Click on Message):**
- Copy
- Regenerate (AI messages only)
- Delete
- Add to Project (save as note)

---

### View 3: Projects Screen

#### Layout
**Header + List/Grid Toggle + Projects**

#### Header
- Title: "Projects"
- Search Bar: "Search projects..." (real-time filter)
- Filter Dropdown: "All", "Active", "Archived"
- View Toggle: List / Grid (icons)
- New Project Button: "+ New Project" (primary CTA)

#### Project List View (Default)

**Project Item Format:**
```
┌─────────────────────────────────────────────────────────────┐
│ 📁 hexahub-backend                    [Edit] [Archive] [...]│
│                                                              │
│ Last modified: 2 hours ago | Files: 127 | AI Model: GPT-4  │
│ Tags: FastAPI, PostgreSQL, Docker                           │
│                                                              │
│ Recent Activity:                                            │
│ • AI Chat: "Generate CRUD endpoints" (1 hour ago)          │
│ • File Updated: src/api/routes.py (2 hours ago)            │
└─────────────────────────────────────────────────────────────┘
```
- Swipe Actions (mobile): Left (Archive), Right (Delete)
- Hover: Show quick action buttons (Edit, Archive, More)

#### Project Grid View

**Project Card Format:**
```
┌─────────────────────────┐
│  📁                     │
│  hexahub-backend        │
│                         │
│  127 files              │
│  GPT-4                  │
│  FastAPI, PostgreSQL    │
│                         │
│  [Open →]              │
└─────────────────────────┘
```
- 3-column grid (desktop), 2-column (tablet), 1-column (mobile)
- Hover: Lift effect (shadow increase)

#### New Project Modal

**Fields:**
1. Project Name (text input, required)
2. Description (textarea, optional)
3. Default AI Model (dropdown: GPT-4, Claude, etc.)
4. Tags (multi-select chips)
5. Visibility (radio: Private, Team - future)

**Actions:** Cancel (ghost), Create (primary, blue)

---

### View 4: Settings Screen

#### Layout
**Tabs (Left Sidebar) + Content (Right)**

#### Tabs
1. Profile
2. API Keys
3. Preferences
4. Integrations
5. Billing (Cloud Pro users only)

#### Tab 1: Profile

**Sections:**
- Avatar Upload (drag-drop or click)
- Name (text input)
- Email (read-only, verified)
- Timezone (dropdown, auto-detected)
- Language (dropdown: EN, DE)
- Save Button (primary, bottom-right)

#### Tab 2: API Keys

**Components:**
- **OpenAI API Key:** (input, masked, "••••••••", "Reveal" button)
- **Anthropic API Key:** (same format)
- **Google AI API Key:** (same format)
- **Ollama Server URL:** (text input, default: `http://localhost:11434`)
- **Test Connection Button:** (for each API key, shows ✅/❌ status)

**Security Note (Alert Box):**
```
🔒 API keys are encrypted at rest and never leave your server.
   Use self-hosted mode for maximum privacy.
```

#### Tab 3: Preferences

**Options:**
- **Theme:** Dark (default), Light, System
- **Default AI Model:** Dropdown (GPT-4, Claude, etc.)
- **Code Editor Font:** JetBrains Mono, Fira Code, etc.
- **Keyboard Shortcuts:** Enable/Disable
- **Notifications:** Email, Browser Push (toggles)

#### Tab 4: Integrations

**Available Integrations (Future):**
- GitHub (OAuth, import repos)
- GitLab (OAuth)
- VS Code Extension (link to download)
- Slack (notifications)

#### Tab 5: Billing (Cloud Pro Only)

**Components:**
- Current Plan: Cloud Pro ($49/mo)
- Usage This Month: 1,247 API calls, $12.34 cost
- Payment Method: •••• 4242 (Stripe card)
- Billing History (table: Date, Amount, Invoice PDF)
- Change Plan Button (upgrade to Enterprise or downgrade to Self-Hosted)

---

## Component Library (Shadcn/UI)

### Components Used

**From Shadcn/UI:**
1. **Button** (Primary, Secondary, Ghost, Icon)
2. **Input** (Text, Textarea)
3. **Select** (Dropdown menus)
4. **Card** (Project cards, Stats cards)
5. **Dialog** (Modals - New Project, Confirm Delete)
6. **Dropdown Menu** (User profile, Project actions)
7. **Tabs** (Settings screen)
8. **Toast** (Success/Error notifications)
9. **Badge** (Tags, Status indicators)
10. **Avatar** (User profile)
11. **Separator** (Horizontal dividers)
12. **ScrollArea** (Chat messages, Activity feed)
13. **Command** (Cmd+K palette)
14. **Skeleton** (Loading states)
15. **Switch** (Settings toggles)

**Custom Components (Build):**
1. **CodeBlock** (Syntax-highlighted code, Copy button)
2. **Sparkline** (Mini chart for stats)
3. **Timeline** (Recent activity feed)

---

## Interactions

### Keyboard Shortcuts

**Global:**
- `Cmd/Ctrl + K` → Open Command Palette
- `Cmd/Ctrl + N` → New AI Chat
- `Cmd/Ctrl + P` → New Project
- `Cmd/Ctrl + ,` → Settings
- `Cmd/Ctrl + /` → Show keyboard shortcuts help

**AI Chat:**
- `Cmd/Ctrl + Enter` → Send message
- `↑` (when input empty) → Edit last message
- `Esc` → Close AI Assistant Panel

**Projects:**
- `j / k` → Navigate list (Vim-style)
- `Enter` → Open project
- `Delete` → Delete project (with confirmation)

### Command Palette (Cmd+K)

**Interface:**
- Modal overlay (glassmorphism background)
- Search input (autofocus)
- Results list (fuzzy search)

**Searchable Items:**
- Navigation ("Go to Projects", "Open Settings")
- AI Prompts ("Start chat: Explain Docker")
- Recent Projects
- Quick Actions ("New Project", "Sync Data")

**Fuzzy Search:** Use `fuse.js` or native `String.prototype.includes`

---

## State Management

### Local State (Component-Level)
- Sidebar collapsed/expanded (localStorage persistence)
- AI Assistant Panel open/closed (localStorage)
- Theme (dark/light, localStorage)
- Project list view (list/grid, localStorage)

### Global State (Context or Zustand)
- User Profile (from auth session)
- Active Project (current project ID)
- AI Chat History (per conversation)
- API Keys (encrypted, from settings)

### Server State (TanStack Query / SWR)
- Projects List (cached, auto-refetch on focus)
- Recent Activity (cached, 5-min stale time)
- Usage Stats (cached, 1-hour stale time)

---

## Responsive Breakpoints

### Desktop (1280px+)
- Sidebar: 240px, always visible
- AI Panel: 400px, toggle-able
- Main Content: Flexible (remaining space)

### Tablet (768px - 1279px)
- Sidebar: 64px, collapsed by default, expands on click
- AI Panel: 320px, overlay (not persistent)
- Main Content: Full width when sidebar collapsed

### Mobile (<768px)
- Sidebar: Hidden, hamburger menu (drawer)
- AI Panel: Full-screen modal
- Main Content: Full width
- Top Bar: Compact (icons only for notifications, profile)

---

## Dark Mode (Default)

### Color Palette (Tailwind Classes)

**Background:**
- Main: `bg-[#1e1e1e]` (VS Code Dark)
- Sidebar: `bg-[#252526]`
- Top Bar: `bg-[#2d2d30]`
- Cards: `bg-[#2a2a2a]`

**Text:**
- Primary: `text-gray-100` (#f9fafb)
- Secondary: `text-gray-400` (#9ca3af)
- Muted: `text-gray-500` (#6b7280)

**Accents:**
- Primary: `text-blue-500` (#3b82f6)
- Success: `text-green-500` (#10b981)
- Error: `text-red-500` (#ef4444)
- Warning: `text-amber-500` (#f59e0b)

**Borders:**
- Default: `border-gray-700` (#374151)
- Hover: `border-gray-600`

---

## Accessibility (WCAG 2.1 AA)

### Requirements

**Keyboard Navigation:**
- All interactive elements focusable (Tab order logical)
- Focus indicators visible (2px outline, `ring-2 ring-blue-500`)
- Skip to main content link (for screen readers)

**Screen Reader Support:**
- ARIA labels for icon buttons (`aria-label="Open Settings"`)
- ARIA live regions for dynamic content (AI streaming responses)
- Semantic HTML (`<nav>`, `<main>`, `<aside>`)

**Color Contrast:**
- Text on background: 7:1 (AAA level for body text)
- UI components: 3:1 minimum (AA level)

**Responsive Text:**
- Support browser text zoom (200% without horizontal scroll)
- Use `rem` units for font sizes (not `px`)

---

## Performance Optimization

### Code Splitting
- Route-based splitting (Next.js automatic)
- Lazy-load AI Chat Panel (React.lazy)
- Lazy-load Settings tabs (only active tab loaded)

### Image Optimization
- Next.js Image component (WebP format, lazy loading)
- Avatar placeholders (blurhash or solid color)

### Data Fetching
- Prefetch Projects on hover (Next.js Link prefetch)
- Paginate Activity Feed (infinite scroll or load more)
- Debounce search inputs (300ms delay)

### Caching
- Service Worker (cache static assets)
- TanStack Query (client-side caching, 5-min stale time)
- CDN (for production deployment)

---

## Success Criteria

- [ ] All 4 core views implemented (Home, AI Chat, Projects, Settings)
- [ ] Shadcn/UI components integrated (15+ components)
- [ ] Dark mode default, Light mode toggle functional
- [ ] Command Palette (Cmd+K) functional with fuzzy search
- [ ] Responsive (tested on Desktop 1920px, Tablet 768px, Mobile 375px)
- [ ] Keyboard shortcuts documented and functional (5+ global shortcuts)
- [ ] Performance: Lighthouse score >90 (Performance, Accessibility, Best Practices)
- [ ] Accessibility: WCAG 2.1 AA compliant (axe DevTools 0 violations)
- [ ] AI Chat streaming responses (real-time display)
- [ ] Projects CRUD operations (Create, Read, Update, Archive)

---

##Technical Implementation

### Next.js App Router Structure
```
app/
├── (dashboard)/
│   ├── layout.tsx (Sidebar + Top Bar wrapper)
│   ├── page.tsx (Dashboard Home)
│   ├── chat/
│   │   └── page.tsx (AI Chat Screen)
│   ├── projects/
│   │   ├── page.tsx (Projects List)
│   │   └── [id]/page.tsx (Project Detail)
│   └── settings/
│       └── page.tsx (Settings Screen)
└── components/
    ├── sidebar.tsx
    ├── topbar.tsx
    ├── ai-assistant-panel.tsx
    ├── command-palette.tsx
    └── ... (Shadcn components)
```

### State Management (Zustand Example)
```typescript
// store/app-store.ts
import { create } from 'zustand'
import { persist } from 'zustand/middleware'

interface AppState {
  sidebarCollapsed: boolean
  aiPanelOpen: boolean
  theme: 'dark' | 'light'
  toggleSidebar: () => void
  toggleAIPanel: () => void
  setTheme: (theme: 'dark' | 'light') => void
}

export const useAppStore = create<AppState>()(
  persist(
    (set) => ({
      sidebarCollapsed: false,
      aiPanelOpen: true,
      theme: 'dark',
      toggleSidebar: () => set((state) => ({
        sidebarCollapsed: !state.sidebarCollapsed
      })),
      toggleAIPanel: () => set((state) => ({
        aiPanelOpen: !state.aiPanelOpen
      })),
      setTheme: (theme) => set({ theme }),
    }),
    { name: 'hexahub-app-store' }
  )
)
```

---

**Specification Version:** 1.0
**Word Count:** 2,647 words (~148 lines of structured content)
**Token Efficiency:** High (references DESIGN_CONTEXT.md, no redundant project overview)
**Ready for Implementation:** ✅ Yes (pass to Next.js + Shadcn/UI developer)
