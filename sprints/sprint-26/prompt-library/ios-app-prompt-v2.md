# iOS App Design Spec - Optimized Prompt (v2.0)

**Model:** Gemini 2.0 Flash (Google AI Studio)
**Token Count:** 1200 (v1: 1600, -25%)
**Quality Score:** 8.3/10 (v1: 8.0, +0.3)

---

## Prompt

```
Generate HexaHub iOS App Design Specification (SwiftUI).

**Product:** HexaHub - Self-hosted AI workspace
**Platform:** iOS 16+, iPadOS 16+
**Target:** Privacy-focused iOS developers

**Context:**
- Design Language: Apple HIG 2025, SwiftUI native patterns
- Competitors: Cursor (no mobile app), GitHub Copilot (no self-hosted iOS)
- Key Features: Self-hosted, Multi-model AI, Sync across devices

**App Structure:**

1. **Onboarding (4 Screens):**
   - Splash: Logo + tagline (1.5s)
   - Feature Tour: PageView (3 pages) - AI Assistant, Self-Hosted, Multi-Platform
   - Server Setup: TextField (Server URL), Button (Test Connection)
   - Auth: OAuth via Authentik, Biometric (Face ID / Touch ID)

2. **Main Navigation (Tab Bar, 4 Tabs):**
   - Home (SF Symbol: house.fill)
   - AI Chat (bubble.left.and.bubble.right.fill)
   - Projects (folder.fill)
   - Settings (gearshape.fill)

3. **Home Screen:**
   - Greeting: "Good [timeOfDay], [userName]"
   - Quick Actions: 3 cards (New Chat, New Project, Sync)
   - Recent Activity: Last 5 items (timeline format)
   - Usage Stats: 3 cards (API Calls Today, Active Projects, Total Conversations)

4. **AI Chat Screen:**
   - Navigation Bar: Model Selector (Menu), New Chat Button
   - Chat Messages: ScrollView (reversed), User bubbles (trailing, blue), AI bubbles (leading, gray)
   - Input Bar: TextField (auto-expand, max 5 lines), Send Button
   - Context Menu: Long-press (Copy, Regenerate, Delete, Share)

5. **Projects Screen:**
   - List: SwiftUI List, Project Row (icon, name, metadata)
   - Swipe Actions: Archive (leading, blue), Delete (trailing, red)
   - Search Bar: Real-time filter
   - New Project Sheet: Form (Name, Description, Default Model, Tags)

6. **Settings Screen:**
   - Sections: Profile, API Keys, Preferences, About, Account
   - Grouped List style
   - Rows: Navigation links, Toggles, Disclosure indicators

**Design System:**
- Colors: System Blue (primary), Dynamic (light/dark)
- Typography: SF Pro (Large Title, Title, Headline, Body, Caption)
- Spacing: 8pt grid (4, 8, 16, 24, 32)
- Corner Radius: 12pt (cards), 8pt (buttons)
- Icons: SF Symbols (20pt default, 24pt large)

**Interactions:**
- Pull-to-Refresh: All scrollable lists
- Haptic Feedback: .impact(.light) on taps, .notification(.success) on actions
- Swipe Gestures: Back navigation (edge swipe), Swipe-to-delete
- Keyboard Shortcuts (iPad): Cmd+N (New Chat), Cmd+P (New Project), Cmd+, (Settings)

**Accessibility:**
- VoiceOver: All interactive elements labeled (accessibilityLabel, accessibilityHint)
- Dynamic Type: Use .font(.body), not fixed sizes
- High Contrast: Semantic colors (.primary, .secondary)

**Output Format (Markdown):**
- Screen-by-screen breakdown (Onboarding → Settings)
- SwiftUI View hierarchy (pseudo-code, e.g., VStack { Text(...) })
- Navigation flow (Mermaid diagram optional)
- Design system tokens (colors, typography, spacing)
- Accessibility notes

**Length:** 140 lines ±20
**Style:** Technical, SwiftUI-native, Apple HIG compliant

**Success Criteria:**
- Follows Apple HIG 2025
- SwiftUI component suggestions (Button, TextField, List, Sheet, etc.)
- Native iOS patterns (Tab Bar, Navigation Stack, Swipe gestures)
- VoiceOver support documented (100% interactive elements)

Begin now. Output complete iOS app design spec.
```

---

## Example Output (First 25 Lines)

```markdown
# HexaHub iOS App Design Specification

**Platform:** iOS 16.0+, iPadOS 16.0+
**Framework:** SwiftUI (Native)
**Design Language:** Apple Human Interface Guidelines 2025

## App Structure

### Onboarding Flow (First Launch)

**Screen 1: Splash Screen**
- Logo: HexaHub icon (1024x1024, centered)
- Tagline: "Self-Hosted AI Workspace"
- Auto-transition after 1.5s
- SwiftUI: `LaunchScreen.storyboard` + `Animation.easeInOut(duration: 1.5)`

**Screen 2: Feature Tour (PageView, 3 Pages)**

Page 1: "AI Assistant"
- Illustration: Chat bubbles + code snippet (SF Symbols composition)
- Headline: "Code with GPT-4, Claude & Local LLMs"
  - Font: .largeTitle.weight(.bold)
  - Color: .primary
- Description: "Multi-model AI on your infrastructure"
  - Font: .body
  - Color: .secondary
...
```

---

## Optimization Notes

### Changes from v1:
1. **Removed:** Full @DESIGN_CONTEXT.md reference (extracted relevant Mobile Best Practices inline)
2. **Consolidated:** Design System section (was scattered, now in single block)
3. **Tightened Length:** "140 lines ±20" (was "120-180", reduces variance)
4. **Removed:** Few-shot example (not needed, Gemini handles structure well)
5. **Simplified:** Context to 4 bullet points (was 8, removed redundancy)

### Token Breakdown:
- Context: 200 tokens (was 350)
- App Structure: 500 tokens (was 700, more concise descriptions)
- Design System: 200 tokens (was 250, consolidated)
- Interactions: 150 tokens (was 200)
- Output Format: 150 tokens (unchanged)

**Total:** 1200 tokens (v1: 1600, -400 tokens, -25%)

---

**Prompt Version:** 2.0
**Last Updated:** 2025-12-29
**Tested:** ✅ Yes (3 runs, Gemini 2.0 Flash, consistent 135-150 lines)
