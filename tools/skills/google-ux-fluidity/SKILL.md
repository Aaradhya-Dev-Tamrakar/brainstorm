---
name: google-ux-fluidity
description: Enforces Google Material Design 3 (M3) UX fluidity, expressive motion curves, radial ink ripple state layers, container transforms, and tactile micro-interactions across web and app frontends.
---

# Google UX Fluidity & Motion Design System (Material 3)

This skill guides the implementation of Google's signature UX fluidity—as seen in Google Gemini, NotebookLM, Google Drive, and Material You.

## 1. Material 3 Motion Curves & Timing Tokens

Never use generic CSS ase or linear transitions. Always use Google's official M3 timing functions:

| Token | Cubic Bezier | Typical Use |
| :--- | :--- | :--- |
| **Emphasized (Default)** | cubic-bezier(0.2, 0.0, 0.0, 1.0) | Cards, dialogs, expandable surfaces |
| **Emphasized Decelerate** | cubic-bezier(0.05, 0.7, 0.1, 1.0) | Elements entering viewport, drawers, modals |
| **Emphasized Accelerate** | cubic-bezier(0.3, 0.0, 0.8, 0.15) | Elements exiting viewport, dismissed toasts |
| **Standard** | cubic-bezier(0.2, 0.0, 0.0, 1.0) | Simple state shifts, color transitions |

### Duration Tokens
- **Micro (Feedback)**: 100ms - 150ms (press states, checkbox toggles, ripples)
- **Small (Pills/Chips/Buttons)**: 200ms - 250ms (hover states, pill transitions)
- **Medium (Cards/Menus/Dropdowns)**: 300ms - 400ms (dropdown popups, card stagger)
- **Large (Drawers/Dialogs/Sheets)**: 450ms - 550ms (side drawers, full dialog container transforms)

---

## 2. Radial Ink Ripple Engine (M3 State Layer)

In authentic Google interfaces, clicking any interactive element emits a radial ink ripple originating from the exact cursor coordinate (clientX, clientY).

`javascript
function createGoogleRipple(event, element) {
  const rect = element.getBoundingClientRect();
  const circle = document.createElement('span');
  const diameter = Math.max(rect.width, rect.height);
  const radius = diameter / 2;

  circle.style.width = circle.style.height = ${diameter}px;
  circle.style.left = ${event.clientX - rect.left - radius}px;
  circle.style.top = ${event.clientY - rect.top - radius}px;
  circle.classList.add('google-ripple-effect');

  // Remove existing ripples
  const existing = element.querySelector('.google-ripple-effect');
  if (existing) existing.remove();

  element.appendChild(circle);
  setTimeout(() => circle.remove(), 600);
}
`

### Ripple CSS
`css
.google-ripple-host {
  position: relative;
  overflow: hidden;
  -webkit-mask-image: -webkit-radial-gradient(white, black); /* Safari border-radius clipping */
}

.google-ripple-effect {
  position: absolute;
  border-radius: 50%;
  transform: scale(0);
  animation: google-ripple-anim 0.55s cubic-bezier(0.2, 0, 0, 1) forwards;
  background-color: currentColor;
  opacity: 0.14;
  pointer-events: none;
}

@keyframes google-ripple-anim {
  to {
    transform: scale(2.5);
    opacity: 0;
  }
}
`

---

## 3. Container Transforms (Drawers & Modals)

When opening dialogs or expanding cards:
1. Interpolate ackdrop-filter: blur(0px) to lur(8px).
2. Scale the container from scale(0.92) to scale(1.0) using cubic-bezier(0.05, 0.7, 0.1, 1.0).
3. Give dialogs elevation level 3 or 4: ox-shadow: 0 16px 40px rgba(0, 0, 0, 0.2).

---

## 4. Google Quad-Color Loading Wave

Rather than generic spinning circles, Google products feature the iconic quad-color pulse:
- Google Blue (#8ab4f8 / #0b57d0)
- Google Red (#f28b82 / #b3261e)
- Google Yellow (#fdd663 / #8f6200)
- Google Green (#81c995 / #146c2e)

Dots bounce in a continuous fluid wave with phase-delayed sine offsets.

---

## 5. Tactile Micro-Interactions & State Layers

- **Active compression**: :active { transform: scale(0.975); } on buttons, chips, and cards.
- **Elevation hover**: Cards rise smoothly 	ranslateY(-3px) with dual-ambient shadow bloom.
- **Search bar expansion**: Focus transforms background color, adds a 2px blue ring, and glides smoothly.
- **Accessibility**: Always wrap motion in @media (prefers-reduced-motion: reduce) to disable non-essential animations.
