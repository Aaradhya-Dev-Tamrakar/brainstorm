# 🌊 Fluid Wordmark Navbar — Production Boilerplate

> **Archetype:** Anthropic-style in-place syllable wordmark collapse (`ANTHROP\C` &rarr; `A\`)  
> **Architecture:** 3-Zone Fixed-Slot CSS Grid (`var(--nav-logo-slot) 1fr var(--nav-right-slot)`)  
> **CLS Guarantee:** Zero Cumulative Layout Shift (CLS = 0) on scroll and hover  
> **Dependencies:** None (Pure Vanilla HTML5 / Modern CSS / Micro-JS)

---

## ⚡ What This Boilerplate Solves

1. **In-Place Syllable Folding**: Instead of abruptly cross-fading or swapping logos on scroll, words fold gracefully into their capitalized initial monograms:
   ```text
   A[aradhya] D[ev] T[amrakar] .  ──(scroll > 50px)──>  A D T .
   ```
2. **Anti-Displacement Geometry**: Contraction from ~250px to ~60px takes place strictly inside a reserved CSS Grid slot (`--nav-logo-slot: 250px`). Adjacent navigation links and utility controls remain 100% frozen in place.
3. **120fps Hardware Acceleration**: Characters use `will-change: max-width, opacity, transform` with `-webkit-backface-visibility: hidden` and `transform: translateZ(0)` for zero-jitter, artifact-free GPU rendering.
4. **Hover-to-Peek Preview**: When scrolled, hovering or focusing on the collapsed monogram expands the full name smoothly without moving neighboring links.

---

## 📂 Boilerplate Structure

```text
fluid-wordmark-navbar/
├── index.html     # Runnable demo and standalone markup structure
├── styles.css     # 3-Zone CSS Grid, M3 spring kinematics, and GPU layer tokens
├── navbar.js      # Passive RAF scroll listener and dynamic syllable decomposing utility
└── README.md      # Integration instructions and calibration guide
```

---

## 🚀 Quick Integration

### 1. HTML Markup

```html
<nav id="nav">
  <!-- Zone 1: Dedicated Slot for Wordmark -->
  <div class="nav-brand-slot">
    <a href="/" class="nav-logo" aria-label="Brand Name">
      <span class="nav-brand-text">
        <span class="nav-word" data-word="First"><span class="nav-initial">F</span><span class="nav-rest">irst</span></span>
        <span class="nav-word" data-word="Last"><span class="nav-initial">L</span><span class="nav-rest">ast</span></span>
        <span class="nav-dot" aria-hidden="true">.</span>
      </span>
    </a>
  </div>

  <!-- Zone 2: Navigation Links -->
  <ul class="nav-links">
    <li><a href="#work">Work</a></li>
    <li><a href="#about">About</a></li>
  </ul>

  <!-- Zone 3: Right Controls -->
  <div class="nav-right">
    <a href="#contact" class="nav-cta">Contact</a>
  </div>
</nav>
```

### 2. Calibrating the Brand Slot Width

Measure your full expanded brand name at your target font size, add ~10–15px safety padding, and assign it to `--nav-logo-slot` in `styles.css`:

```css
#nav {
  /* Set to exact rendered width of full wordmark + comfortable clearance */
  --nav-logo-slot: 250px;
  --nav-right-slot: max-content;

  display: grid;
  grid-template-columns: var(--nav-logo-slot) 1fr var(--nav-right-slot);
  column-gap: 1.5rem;
}
```

### 3. Client Scroll Script

Include `navbar.js` before `</body>`. It attaches a passive `requestAnimationFrame` scroll watcher that applies `#nav.scrolled` when scrolling past 50px:

```html
<script src="navbar.js"></script>
```

Or initialize programmatically with custom names:

```javascript
FluidWordmarkNavbar.renderDecomposedWordmark(
  document.querySelector('.nav-logo'),
  'Anthropic Computing',
  '\\'
);
```

---

## ⚠️ Critical CSS Invariant Rules

| Invariant | Correct Approach | Hazardous Pitfall | Why |
| :--- | :--- | :--- | :--- |
| **Layout Containment** | `transform: translateZ(0)` | `contain: inline-size` | `contain: inline-size` causes Chromium/Blink to calculate auto-width inline text as 0px, causing the full name to vanish. |
| **Scroll Trigger** | Passive RAF class toggle (`.scrolled`) | `@supports (animation-timeline: scroll())` | Fixed navbar containers calculate pixel-range scroll timelines (`0px 80px`) at 100% on initial load in Blink. |
| **Grid Column 1** | `width: var(--nav-logo-slot)` | `width: auto` | Auto width collapses Column 1 when text shrinks, pulling all middle links to the left. |
| **CTA Padding** | Fixed `0.5rem 1.15rem` | Reduced padding on scroll | Shrinking button padding changes Zone 3 bounds and causes horizontal link drift. |
