---
name: shadcn-context
description: Provides exact component schemas, prop definitions, and composition rules for shadcn/ui, Radix UI primitives, and modern design system packs to prevent style hallucinations.
category: frontend
---

# Shadcn-Context & Design System Packs

This skill equips Antigravity with exact component schemas, prop definitions, and composition rules for **shadcn/ui**, **Radix UI Primitives**, and **Tailwind CSS**, preventing component hallucinations and ensuring strict compliance with production component architectures.

---

## 1. Core Architecture & Utility Foundation

### The `cn()` Utility
All className composition must use the project `cn()` utility combining `clsx` and `tailwind-merge`:
```typescript
import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
```

### Class Variance Authority (CVA)
Component variants must be declared with `class-variance-authority`:
```typescript
import { cva, type VariantProps } from "class-variance-authority"

export const buttonVariants = cva(
  "inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground shadow hover:bg-primary/90",
        destructive: "bg-destructive text-destructive-foreground shadow-sm hover:bg-destructive/90",
        outline: "border border-input bg-background shadow-sm hover:bg-accent hover:text-accent-foreground",
        secondary: "bg-secondary text-secondary-foreground shadow-sm hover:bg-secondary/80",
        ghost: "hover:bg-accent hover:text-accent-foreground",
        link: "text-primary underline-offset-4 hover:underline",
      },
      size: {
        default: "h-9 px-4 py-2",
        sm: "h-8 rounded-md px-3 text-xs",
        lg: "h-10 rounded-md px-8",
        icon: "h-9 w-9",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
)
```

---

## 2. Component Composition Schemas

### Dialog / Modal
```tsx
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"

<Dialog>
  <DialogTrigger asChild>
    <Button variant="outline">Open Dialog</Button>
  </DialogTrigger>
  <DialogContent className="sm:max-w-[425px]">
    <DialogHeader>
      <DialogTitle>Edit Profile</DialogTitle>
      <DialogDescription>Make changes here and click save.</DialogDescription>
    </DialogHeader>
    {/* Body content */}
    <DialogFooter>
      <Button type="submit">Save changes</Button>
    </DialogFooter>
  </DialogContent>
</Dialog>
```

### Form Field (React Hook Form + Zod)
```tsx
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form"

<FormField
  control={form.control}
  name="username"
  render={({ field }) => (
    <FormItem>
      <FormLabel>Username</FormLabel>
      <FormControl>
        <Input placeholder="shadcn" {...field} />
      </FormControl>
      <FormDescription>Your public display name.</FormDescription>
      <FormMessage />
    </FormItem>
  )}
/>
```

---

## 3. Anti-Hallucination & Customization Rules

1. **Exact Import Paths**: Always import components from `@/components/ui/<component>` (or project alias) rather than inventing arbitrary wrapper libraries.
2. **The `asChild` Pattern**: When wrapping custom buttons or Link components (such as Next.js `Link`), use `asChild` on the Trigger to pass accessibility props to the direct child element without rendering duplicate button wrappers.
3. **No Cookie-Cutter Defaults**:
   - Customize border-radii (`rounded-xl` or `rounded-2xl` for modern software).
   - Augment standard buttons with subtle inner highlight rims (`shadow-[inset_0_1px_0_rgba(255,255,255,0.15)]`).
   - Replace standard black overlays with frosted blurred backdrops (`backdrop-blur-sm bg-black/50`).
4. **Accessibility Integrity**: Never remove `DialogTitle` or `DialogDescription`—if visually hidden, use the `sr-only` utility to maintain screen reader compliance.
