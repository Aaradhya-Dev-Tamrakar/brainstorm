---
name: design-taste-frontend
description: "Use when building high-agency frontend interfaces with strict design taste, calibrated color, responsive layout, and motion rules. Overrides generic AI styling defaults, Lila/purple glows, and Inter overuse."
category: frontend
risk: safe
source: community
source_repo: sickn33/antigravity-awesome-skills
tags: [frontend, design, ui, react, antigravity]
tools: [antigravity, claude, cursor]
---

# High-Agency Frontend Design Skill

## When to Use
- Use when creating, improving, or reviewing frontend UI with strong design taste and anti-generic constraints.
- Use when React, Next.js, Tailwind, motion, component states, typography, spacing, color, or responsive behavior need senior-level design judgment.
- Use when the output must override common LLM UI biases such as centered heroes, generic purple gradients, card overuse, missing interactive states, and fragile layouts.

---

## 1. ACTIVE BASELINE CONFIGURATION
* **DESIGN_VARIANCE: 8** (1 = Perfect Symmetry, 10 = Artsy Chaos / Asymmetric)
* **MOTION_INTENSITY: 6** (1 = Static/No movement, 10 = Cinematic/Magic Physics)
* **VISUAL_DENSITY: 4** (1 = Art Gallery/Airy, 10 = Pilot Cockpit/Packed Data)

> **AI Directive:** The standard baseline for all generations is strictly set to (8, 6, 4). Adapt these dynamically whenever explicitly requested by the user in chat.

---

## 2. DEFAULT ARCHITECTURE & CONVENTIONS

* **Dependency Verification [MANDATORY]:** Before importing ANY 3rd party library (e.g. `framer-motion`, `lucide-react`, `@phosphor-icons/react`), inspect package dependencies. If missing, output the exact install command before providing the code. Never assume a package exists.
* **Component Model:** In React/Next.js, default to Server Components for static layouts and data fetching. Isolate interactive motion and glass elements into client leaves marked with `'use client'`.
* **ANTI-EMOJI POLICY [CRITICAL]:** NEVER use emojis in code, markup, headings, or alt text. Replace symbols with high-quality icons (Phosphor, Radix, Lucide) or clean SVG primitives. Emojis are strictly BANNED.
* **Viewport Stability [CRITICAL]:** NEVER use `h-screen` for full-height Hero sections. ALWAYS use `min-h-[100dvh]` to prevent catastrophic layout jumping on mobile browsers.
* **CSS Grid Over Flex-Math:** Avoid complex flexbox percentage math (`w-[calc(33%-1rem)]`). ALWAYS use CSS Grid (`grid grid-cols-1 md:grid-cols-3 gap-6`) for reliable structures.
* **Icons:** Standardize icon package and stroke width globally (e.g. `strokeWidth={1.5}` or `2.0`).

---

## 3. DESIGN ENGINEERING DIRECTIVES (Bias Correction)

### Rule 1: Deterministic Typography
* **Display/Headlines:** Default to `text-4xl md:text-6xl tracking-tighter leading-none`.
  * **Anti-Slop:** Discourage generic `Inter` for creative or flagship interfaces. Choose expressive typefaces: `Geist`, `Cabinet Grotesk`, `Satoshi`, or `Outfit`.
  * **Dashboard Rule:** Serif fonts are strictly BANNED for software dashboards. Use high-end Sans-Serif pairings (`Geist` + `Geist Mono` or `Satoshi` + `JetBrains Mono`).
* **Body/Paragraphs:** `text-base text-gray-600 dark:text-zinc-400 leading-relaxed max-w-[65ch]`.

### Rule 2: Color Calibration
* **Strict Constraint:** Maximum 1 primary accent color. Saturation < 80%.
* **The Lila / Neon Purple Ban:** The generic "AI Purple/Blue" aesthetic is strictly BANNED. No neon purple button glows or cliché gradient pills. Ground designs in neutral slate/zinc bases with deliberate, high-contrast accents (e.g. Emerald, Electric Blue, Warm Amber, or Crimson).
* **Color Consistency:** Maintain single palette temperature (either cool slate or warm neutral) across the entire application.

### Rule 3: Layout Diversification & Spatial Asymmetry
* **Anti-Center Bias:** Centered Hero/H1 sections are strictly BANNED when `DESIGN_VARIANCE > 4`. Force 50/50 split screens, left-aligned content with right-aligned floating interactive assets, or deliberate asymmetric whitespace.

### Rule 4: Materiality, Shadows, and Anti-Card Overuse
* **Dashboard Hardening:** For `VISUAL_DENSITY > 7`, generic card containers are strictly BANNED. Use grouping via `border-t`, `divide-y`, or negative space. Data metrics should breathe freely.
* **Elevation Tint:** When shadows are applied, tint them slightly toward the background hue rather than harsh pure black.

### Rule 5: Interactive UI States
Every interactive element must include:
1. **Default & Hover State:** Subtle micro-lift and luminance shift.
2. **Active State:** Physical click feedback (`-translate-y-[1px]` or `scale-[0.98]`).
3. **Loading State:** Dimension-matched skeleton loaders (never generic spinning circles).
4. **Empty State:** Contextual guidance and immediate call-to-action.
5. **Error State:** Clear, inline validation messages.

---

## 4. CREATIVE PROACTIVITY (Anti-Slop Implementation)

* **Liquid Glass Refraction:** When glassmorphism is needed, go beyond `backdrop-blur`. Add a 1px inner border and a subtle top highlight reflection:
  ```css
  backdrop-filter: blur(16px) saturate(180%);
  border: 1px solid rgba(255, 255, 255, 0.08);
  box-shadow: inset 0 1px 0 0 rgba(255, 255, 255, 0.1), 0 20px 40px -15px rgba(0, 0, 0, 0.5);
  ```
* **Magnetic Micro-Physics (MOTION_INTENSITY > 5):** Use Framer Motion's `useMotionValue` and `useTransform` outside React render cycles to prevent performance degradation on mobile.
* **Perpetual Spring Micro-Interactions:** Apply premium Spring Physics (`type: "spring", stiffness: 100, damping: 20` or CSS `cubic-bezier(0.16, 1, 0.3, 1)`)—never linear easing.
* **Staggered Orchestration:** Reveal lists and grids sequentially with staggered cascade delays (`animation-delay: calc(var(--index) * 80ms)`).
* **Hardware Acceleration:** Animate exclusively via `transform` and `opacity`. Never animate `top`, `left`, `width`, or `height`.
