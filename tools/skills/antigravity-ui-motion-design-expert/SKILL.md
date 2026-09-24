---
name: antigravity-ui-motion-design-expert
description: Instructs the agent to implement spatial layouts, weightless 3D CSS transforms, multi-layer glassmorphism, ambient gradient meshes, and smooth animation timelines (GSAP, CSS transitions) for interactive frontends.
category: frontend
---

# Antigravity UI & Motion Design Expert

This skill guides the agent away from flat, lifeless web design by implementing weightless depth, spatial awareness, physical momentum, and tactile micro-interactions.

---

## 1. Spatial Layouts & 3D CSS Transforms

- **Container Perspective**: Apply `perspective: 1000px` to parent grid/list containers.
- **Card Tilt & Float Physics**:
  - Cards support subtle reactive elevation:
    ```css
    transform: perspective(1000px) rotateX(0deg) rotateY(0deg) translateZ(0);
    transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.25s ease;
    ```
  - On hover:
    ```css
    transform: translateY(-4px) scale(1.008);
    box-shadow: 0 20px 30px -10px rgba(0, 0, 0, 0.5), 
                0 0 20px -5px rgba(99, 102, 241, 0.2);
    ```

---

## 2. Advanced Multi-Layer Glassmorphism

Avoid harsh flat panels or opaque boxes. Use frosted glass layering:
- **Surface**: `backdrop-filter: blur(16px) saturate(180%)`
- **Background**: `rgba(15, 23, 42, 0.65)` to `rgba(30, 41, 59, 0.55)`
- **Border**:
  - Gradient or dual-stop border simulating rim lighting:
    ```css
    border: 1px solid rgba(255, 255, 255, 0.08);
    ```
  - Top highlight reflection:
    ```css
    box-shadow: inset 0 1px 0 0 rgba(255, 255, 255, 0.1);
    ```

---

## 3. Ambient Lighting & Mesh Gradients

To create an immersive canvas:
- Render fixed ambient light orbs in the background:
  - Top-left: Indigo orb (`radial-gradient(circle at 10% 20%, rgba(99, 102, 241, 0.12) 0%, transparent 40%)`)
  - Bottom-right: Purple/Violet orb (`radial-gradient(circle at 90% 80%, rgba(139, 92, 246, 0.08) 0%, transparent 45%)`)
- Ensure ambient layers have `pointer-events: none` and `z-index: 0`.

---

## 4. Motion Curves & Micro-Interactions

- **Default Ease**: Use spring or hyper-responsive curves rather than linear or standard ease:
  - `cubic-bezier(0.16, 1, 0.3, 1)` (snappy ease-out with soft settle).
- **Staggered Entry**: Mount child elements with sequential delays:
  - `transition-delay: calc(var(--index, 0) * 40ms)`.
