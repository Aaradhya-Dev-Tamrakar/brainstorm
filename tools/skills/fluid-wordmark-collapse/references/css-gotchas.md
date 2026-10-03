# Critical CSS Gotchas & Runtime Pitfalls

## 1. The `contain: inline-size` Disappearing Text Trap

### The Symptom
When applying CSS Containment to collapsible trailing spans (`.nav-rest`), text disappears completely upon page load, leaving only the anchor initials (`ADT.`) even when unscrolled at the top of the page.

### The Root Cause
Under CSS Containment Level 2 / Level 3 (Container Queries), `contain: inline-size` forces the layout engine to calculate the element's inline size **as if it contains no child nodes or text**:
- If an element has `max-width: 140px` but no explicit `width`, its default `width: auto` resolves to `0px` under inline-size containment.
- Combined with `overflow: hidden`, all inner text is clipped completely, rendering the element invisible.

### The Antidote
Never apply `contain: inline-size` or `contain: size` to dynamically measured text segments. Instead, apply isolated GPU promotion:

```css
/* DO NOT USE:
contain: layout inline-size style; 
*/

/* CORRECT PATTERN: */
.nav-rest {
  display: inline-block;
  overflow: hidden;
  white-space: nowrap;
  vertical-align: baseline;
  will-change: max-width, opacity, transform;
  -webkit-backface-visibility: hidden;
  backface-visibility: hidden;
}
```

---

## 2. The `animation-timeline: scroll()` Inside Fixed Navbars Trap

### The Symptom
Using native `@supports (animation-timeline: scroll())` keyframes causes the wordmark to immediately lock into its 100% collapsed state (`max-width: 0`) at scroll position 0.

### The Root Cause
1. **Invalid Range Syntax**: In standard CSS Scroll-Driven Animations, pixel ranges like `animation-range: 0px 80px;` are valid on `view()` timelines, but are **ignored or invalid** on `scroll()` timelines.
2. **Fixed Container Context**: For `position: fixed` elements, root scroll timelines often evaluate fill-mode (`both`) at 100% progress before user interaction occurs, prematurely collapsing the content.

### The Antidote
Rely on deterministic, hardware-accelerated CSS transitions coupled with a passive `requestAnimationFrame` scroll class toggle:

```javascript
// High-performance passive scroll listener in runtime
let scrollTicking = false;
function onScroll() {
  const y = window.scrollY;
  if (nav) nav.classList.toggle('scrolled', y > 50);
  scrollTicking = false;
}

window.addEventListener('scroll', () => {
  if (!scrollTicking) {
    requestAnimationFrame(onScroll);
    scrollTicking = true;
  }
}, { passive: true });
```

```css
/* Declarative CSS transition engine */
.nav-rest {
  max-width: 140px;
  opacity: 0.88;
  transform: scaleX(1) translateX(0);
  transition:
    max-width 0.45s cubic-bezier(0.16, 1, 0.3, 1),
    opacity 0.3s cubic-bezier(0.16, 1, 0.3, 1),
    transform 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}

#nav.scrolled .nav-rest {
  max-width: 0;
  opacity: 0;
  transform: scaleX(0.75) translateX(-4px);
  pointer-events: none;
}
```

---

## 3. Subpixel Blur & Text Aliasing Preservation

When animating `transform: scaleX()` or `translateX()`, browsers can rasterize text into a low-resolution bitmap cache, resulting in blurry fonts during motion.

### Prevention Checklist
1. **Anchor Transform Origin**: Always set `transform-origin: left baseline;` so characters collapse directly toward their capital initial rather than scaling toward the geometric center.
2. **Hardware Acceleration Specularity**: Include `-webkit-backface-visibility: hidden; backface-visibility: hidden;` to force the GPU to maintain subpixel anti-aliasing.
3. **Paired Scale & Max-Width**: Do not use `scaleX(0)` alone; pair `scaleX(0.75)` with `max-width: 0` to preserve crisp font contours right until the clipping boundary.
