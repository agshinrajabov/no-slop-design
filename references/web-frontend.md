# Web Frontend

How to implement the design on the web so the result reads as crafted rather than generated. Covers the CSS architecture that keeps tokens (`design-tokens.md`) as the single source of truth, the modern CSS baseline as of September 2026, the details generated code skips, responsive and dark-mode implementation, performance as a design constraint, framework notes and quality gates. Visual decisions themselves live in `color.md`, `typography.md`, `spacing-layout.md`, `components.md`, `motion.md`; accessibility requirements in `accessibility.md`; the taste-level slop list in `anti-slop.md`.

## Contents

1. Architecture
2. Tailwind v4 specifics
3. Modern CSS to use by default
4. The craft floor
5. Responsive
6. Dark mode
7. Performance as design
8. Framework notes
9. Iconography implementation
10. Quality gates
11. Web slop list (implementation level)
12. Sources

## 1. Architecture

Pipeline: `tokens/*.json` (DTCG) → Style Dictionary v5 → `build/tokens.css` (custom properties on `:root`, per-theme overrides) → either `build/theme.css` (Tailwind v4 `@theme inline` that maps utilities onto those properties) or vanilla CSS that references them directly. Components reference only semantic tokens (`--color-fg-muted`, `--space-4`); never primitives (`--blue-500`) and never raw values.

Layer order, declared once at the top of the entry stylesheet:

```css
@layer reset, tokens, base, components, utilities;
@import "./reset.css" layer(reset);
@import "../build/tokens.css" layer(tokens);
@import "./base.css" layer(base);          /* html, body, headings, links, forms */
@import "./components.css" layer(components);
/* Tailwind v4 appends its own theme/base/components/utilities layers */
```

Rule: a component file that contains a hex, an `rgb()`, a bare `px` for spacing, or a font-family string fails review. Allowed raw values: `0`, `1px` borders and hairlines, `100%`, `auto`, `currentColor`, `transparent`.

Theming shadcn/ui or Radix so it stops looking like shadcn:

| Step | What to change | Why |
|---|---|---|
| 1 | Regenerate every variable in `globals.css` (`--background`, `--foreground`, `--primary`, `--muted`, `--border`, `--ring`, chart colours, sidebar colours) from your tokens; do not keep any default OKLCH value | The default palette is the fingerprint |
| 2 | Replace the single `--radius` with a hierarchy: control radius (inputs, buttons), container radius (cards, dialogs), pill radius; nested radius = outer minus padding | Uniform `rounded-lg` everywhere is a default, not a decision |
| 3 | Remove default `shadow-sm` on cards and inputs; use border or surface colour steps from `color.md` unless shadow is a token | Shadows on everything flatten hierarchy |
| 4 | Define your own focus ring (`--ring` colour, offset, width) and apply it via `:focus-visible` | Default `ring-2 ring-ring/50` is recognisable |
| 5 | Set type scale, weights and line heights from `typography.md`; override `text-sm` defaults inside components | Inter at 14px with `font-medium` on every label is the second fingerprint |
| 6 | Audit each component's class list and delete utilities that duplicate tokenised base styles | Keeps the component readable |

Component library guidance:

| Option | Choose when | Notes |
|---|---|---|
| Headless: Radix Primitives, React Aria Components, Ark UI, Base UI | You own the visual system; need correct a11y behaviour | React Aria has the most complete keyboard and i18n behaviour; Base UI is the successor path for Radix and MUI internals |
| shadcn/ui | Starting point for internal tools; team will re-theme fully (table above) | Copy-in code; treat as scaffolding, not a dependency |
| Full styled kits (MUI, Ant, Mantine, Chakra) | Internal admin with no brand requirement | Hard to make look non-default; acceptable in Operate for back-office |
| Web components (Lit, Shoelace/Web Awesome) | Multi-framework organisation | Style through custom properties and `::part()` |

Styling approach by team:

| Team | Approach |
|---|---|
| 1–3 people, one framework | Tailwind v4 with `@theme inline` over `tokens.css`; a small `components.css` layer for complex states |
| Design-system team, multiple consumers | Vanilla CSS with custom properties, or vanilla-extract for typed tokens; ship both `tokens.css` and a Tailwind preset |
| Large product team on React | CSS Modules or vanilla-extract for components, Tailwind for layout utilities; lint against arbitrary values |
| Content sites, Astro or static | Vanilla CSS with `@layer`, no runtime styling |

## 2. Tailwind v4 specifics

Namespaces recognised by `@theme` (each generates utilities and variants): `--color-*`, `--font-*`, `--text-*`, `--font-weight-*`, `--tracking-*`, `--leading-*`, `--breakpoint-*`, `--container-*`, `--spacing-*`, `--radius-*`, `--shadow-*`, `--inset-shadow-*`, `--drop-shadow-*`, `--blur-*`, `--perspective-*`, `--aspect-*`, `--ease-*`, `--animate-*`.

```css
@import "tailwindcss";

/* wipe defaults so only your tokens generate utilities */
@theme {
  --color-*: initial;
  --font-*: initial;
  --shadow-*: initial;
  --radius-*: initial;
  --breakpoint-*: initial;
  --breakpoint-md: 48rem;
  --breakpoint-lg: 64rem;
  --breakpoint-xl: 80rem;
}

/* inline: utilities read the live custom property, so themes switch at runtime */
@theme inline {
  --color-bg: var(--color-bg);
  --color-fg: var(--color-fg);
  --color-fg-muted: var(--color-fg-muted);
  --color-accent: var(--color-accent);
  --font-sans: var(--font-family-sans);
  --text-body: var(--font-size-body);
  --text-body--line-height: var(--line-height-body);
  --radius-control: var(--radius-control);
  --radius-container: var(--radius-container);
  --ease-standard: var(--ease-standard);
  --spacing: var(--space-unit); /* 0.25rem default; all spacing utilities multiply this */
}

@custom-variant dark (&:where([data-theme=dark], [data-theme=dark] *));
@custom-variant compact (&:where([data-density=compact], [data-density=compact] *));

@utility tabular { font-variant-numeric: tabular-nums; }
@utility stack-* { display: flex; flex-direction: column; gap: --spacing(--value(integer)); }
```

Rules: `@theme` (not inline) when a value is static and should be inlined into utilities; `@theme inline` when the value is a `var()` that changes per theme; `@theme static` to emit every variable even if unused. Container queries are built in: `@container` on the parent, `@sm:`/`@md:` variants on children, sizes from `--container-*`. Do not use arbitrary values (`p-[13px]`, `text-[#333]`) in components; if a value is needed, it becomes a token.

## 3. Modern CSS to use by default

All rows are Baseline Widely Available or Newly Available across Chrome, Edge, Firefox and Safari as of September 2026 unless flagged.

| Feature | Use for | Note |
|---|---|---|
| Logical properties (`margin-inline`, `inset-inline-start`, `padding-block`) | Every spacing and positioning declaration | Enables RTL without overrides |
| Container queries (`container-type: inline-size`, `@container (min-width: 32rem)`) | Component layout changes | Name containers for nested cases |
| `:has()` | Parent styling from child state (`.field:has(:invalid)`), layout switches | Keep selectors shallow for performance |
| Nesting | Component files | Use `&` explicitly for pseudo-classes |
| `color-mix(in oklch, var(--color-accent) 12%, transparent)` | Hover tints, alpha variants from one token | Prefer over hard-coded alpha hexes |
| `light-dark(var(--l), var(--d))` | Two-mode tokens in one declaration | Requires `color-scheme: light dark` on the root |
| `clamp()` | Fluid type and space | See `typography.md` and `spacing-layout.md` for scales |
| `text-wrap: balance` | Headings ≤4 lines | `text-wrap: pretty` for body to avoid orphans |
| `field-sizing: content` | Auto-growing `textarea` and `select` | Set `max-block-size` |
| `<dialog>` + `showModal()` | Modals; native focus trap, top layer, `::backdrop` | Close on `Escape` is built in; add `closedby="any"` for light dismiss |
| Popover API (`popover`, `popovertarget`) | Menus, tooltips, toasts (`popover=manual`) | Top layer, light dismiss, no z-index wars |
| Anchor positioning (`anchor-name`, `position-anchor`, `position-area`, `position-try-fallbacks`) | Placing popovers and tooltips without JS | Baseline 2026 for core properties; keep a `@supports` fallback for older Safari |
| `@starting-style` + `transition-behavior: allow-discrete` | Entry animations for `display: none` → shown, dialogs, popovers | Pairs with `overlay` in transitions |
| View Transitions (same-document) | State and route changes in SPAs | Cross-document is not Baseline yet; feature-detect and treat as enhancement |
| Scroll-driven animations (`animation-timeline: scroll()` / `view()`) | Progress bars, reveal-on-scroll | Respect `prefers-reduced-motion` (see `motion.md`) |
| `scrollbar-gutter: stable` | Prevent layout jump when scrollbars appear | On `html` or scroll containers |
| `overscroll-behavior: contain` | Sheets, drawers, chat panes | Stops scroll chaining to the page |
| `accent-color` | Native checkbox, radio, range, progress | One line themes all native controls |
| `color-scheme` | Native form controls, scrollbars, `<dialog>` backdrop in dark mode | Declare on `:root` and per theme |
| `inset`, `aspect-ratio`, `min()`/`max()` | Positioning and media boxes | Replace padding-hack ratios |
| Subgrid | Aligning card internals across a grid row | `grid-template-rows: subgrid` on the card |
| `:focus-visible` | Focus rings only for keyboard | Never remove outline without replacing it here |
| `interpolate-size: allow-keywords` | Animating to `height: auto` (accordions, details) | Chromium and Safari; harmless where unsupported |
| `@property` | Animating custom properties (gradients, angles) | Needed for typed transitions |
| `@scope` | Limiting component styles without BEM | Newly Available; fine for progressive use |

## 4. The craft floor

Everything below ships in `base.css` for every project. Generated code almost always omits these; their absence is the first tell.

```css
:root {
  color-scheme: light dark;
  accent-color: var(--color-accent);
  scrollbar-color: var(--color-border-strong) transparent;
  caret-color: var(--color-accent);
  -webkit-text-size-adjust: 100%;
  font-kerning: normal;
  font-variant-ligatures: common-ligatures contextual;
  text-rendering: optimizeLegibility;
  hanging-punctuation: first last;
  scrollbar-gutter: stable;
  interpolate-size: allow-keywords;
}
html { hyphens: auto; -webkit-hyphens: auto; overflow-wrap: break-word; }
::selection { background: var(--color-selection-bg); color: var(--color-selection-fg); }
:focus-visible { outline: var(--focus-ring-width) solid var(--color-focus); outline-offset: var(--focus-ring-offset); }
:focus:not(:focus-visible) { outline: none; }
a { text-underline-offset: 0.15em; text-decoration-thickness: from-font; text-decoration-skip-ink: auto; }
button, [role=button], a, label, summary { -webkit-tap-highlight-color: transparent; touch-action: manipulation; }
button, input, select, textarea { font: inherit; color: inherit; letter-spacing: inherit; }
button { cursor: pointer; }
button:disabled, [aria-disabled=true] { cursor: not-allowed; }
label { user-select: none; cursor: default; }
input[type=search] { -webkit-appearance: none; appearance: none; }
input[type=search]::-webkit-search-decoration,
input[type=search]::-webkit-search-cancel-button { -webkit-appearance: none; }
::placeholder { color: var(--color-fg-placeholder); opacity: 1; } /* token must pass 3:1 against field bg */
table, .numeric { font-variant-numeric: tabular-nums; }
img, video, svg, canvas { display: block; max-inline-size: 100%; block-size: auto; }
textarea { field-sizing: content; min-block-size: 3lh; max-block-size: 20lh; resize: vertical; }
[hidden] { display: none !important; }
@media (prefers-reduced-motion: reduce) {
  *, ::before, ::after { animation-duration: 0.01ms !important; animation-iteration-count: 1 !important; transition-duration: 0.01ms !important; scroll-behavior: auto !important; }
}
@media print {
  nav, aside, .no-print { display: none; }
  a[href^="http"]::after { content: " (" attr(href) ")"; }
  body { color: #000; background: #fff; } /* the one place raw values are allowed */
}
```

Document head, every page:

```html
<html lang="en" dir="ltr">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="color-scheme" content="light dark">
<meta name="theme-color" media="(prefers-color-scheme: light)" content="#f7f6f3">
<meta name="theme-color" media="(prefers-color-scheme: dark)" content="#111110">
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="icon" href="/icon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/manifest.webmanifest">
```

Rules: never `maximum-scale=1` or `user-scalable=no`; `lang` matches the content language and changes per element for embedded foreign text; safe areas via `padding-inline: max(var(--space-4), env(safe-area-inset-left))` on full-bleed bars; `cursor: pointer` only on things that navigate or trigger, `cursor: text` on editable areas, `grab`/`grabbing` on draggables; the SVG favicon carries a `prefers-color-scheme` media query inside its `<style>`.

## 5. Responsive

- Breakpoints are content-driven and named for the layout change (`--breakpoint-sidebar: 64rem` means "sidebar appears here"), not for devices. Typical set: 3–4 breakpoints, in `rem`.
- Fluid first: type and space scale with `clamp()` between breakpoints so most components never need a media query.
- Container queries for components; media queries only for page-level layout.
- Viewport units: `dvh` for full-height app shells, `svh` for above-the-fold heroes; never `100vh` on mobile.
- Images: `srcset` with width descriptors and an accurate `sizes` attribute; `<picture>` only for art direction (different crop per width) or format fallback; always `width` and `height` attributes.
- Overflow: `100vw` includes the scrollbar on desktop; use `100%` or `inline-size: 100%`. Add `overflow-x: clip` on `body` only as a temporary diagnostic, never as the fix.
- Touch targets ≥24×24 CSS px minimum (WCAG 2.2), 44×44 preferred for primary controls; see `accessibility.md`.
- Test widths: 320, 360, 390, 768, 1024, 1280, 1440, 1920. Also 200% zoom at 1280 (equivalent to 640) and 400% zoom (WCAG reflow at 320).

## 6. Dark mode

Implementation contract:

```html
<script>
  /* inline in <head>, before any stylesheet, to prevent a flash */
  (function () {
    try {
      var t = localStorage.getItem('theme');
      if (t === 'dark' || t === 'light') document.documentElement.dataset.theme = t;
    } catch (e) {}
  })();
</script>
```

```css
:root { color-scheme: light dark; }
:root[data-theme=light] { color-scheme: light; }
:root[data-theme=dark]  { color-scheme: dark; }
:root {
  --color-bg: light-dark(var(--neutral-0), var(--neutral-950));
  --color-fg: light-dark(var(--neutral-900), var(--neutral-50));
  --color-surface-2: light-dark(var(--neutral-50), var(--neutral-900));
}
```

`light-dark()` resolves against `color-scheme`, so the `data-theme` attribute overrides system preference with no duplicated blocks. Rules: dark surfaces step up in lightness for elevation instead of casting shadows (shadow tokens resolve to near-transparent in dark); images with white backgrounds get a per-mode source via `<picture media="(prefers-color-scheme: dark)">` or a CSS `filter` only when the asset is a line illustration; logos ship in both modes; charts re-tokenise series colours per mode; `theme-color` meta per mode as above; test every contrast pair in both modes (`color.md`, `accessibility.md`).

## 7. Performance as design

Core Web Vitals thresholds (75th percentile of real visits): LCP ≤ 2.5s, INP ≤ 200ms, CLS ≤ 0.1. INP is the most commonly failed metric in 2026; its usual causes are design-side.

| Metric | Design-side causes | Fix |
|---|---|---|
| LCP | Hero image or web font as the largest element; carousels; background-image heroes | `<img fetchpriority="high">` for the hero, no `loading="lazy"` on it; AVIF or WebP; preload the one font file used above the fold; no CSS background for the LCP image |
| INP | Heavy click handlers, animation libraries on the main thread, layout-thrashing hover effects, autocomplete filtering on every keystroke | CSS transitions instead of JS animation; debounce inputs 150–300ms; break long tasks; `content-visibility: auto` on long lists |
| CLS | Images without dimensions, late-loading fonts with different metrics, banners injected above content, skeletons smaller than content | `width`/`height` or `aspect-ratio` on every media box; `size-adjust` fallback fonts; reserve banner space or animate it in from a fixed slot; skeletons match final dimensions |

Font loading:

```css
@font-face {
  font-family: "Brand Sans";
  src: url("/fonts/brand-sans-latin.woff2") format("woff2");
  font-display: swap;          /* optional for body text; use "optional" for non-critical display faces */
  unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+2000-206F, U+2074, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;
}
@font-face {
  font-family: "Brand Sans Fallback";
  src: local("Arial");
  size-adjust: 104%; ascent-override: 92%; descent-override: 24%; line-gap-override: 0%;
}
:root { --font-family-sans: "Brand Sans", "Brand Sans Fallback", system-ui, sans-serif; }
```

Rules: self-host; one variable font file per family where the family offers it; subset by script; `<link rel="preload" as="font" type="font/woff2" crossorigin>` for at most one or two files; ≤2 families, ≤4 total weights/styles shipped; no Google Fonts `<link>` in production (third-party connection, no subsetting control, privacy).

Images: AVIF first, WebP fallback via `<picture>`; `loading="lazy"` and `decoding="async"` below the fold only; explicit dimensions; `sizes` reflecting real layout, not `100vw`. Prefer CSS and the Web Animations API over animation libraries; a page needing Framer Motion for a fade is over-tooled.

## 8. Framework notes

| Framework | Do | Avoid |
|---|---|---|
| Next.js / React | Server Components by default; client islands only for interactivity; `next/font` with `display: 'swap'` and `adjustFontFallback`; `next/image` with `priority` on the LCP image and `sizes` set; theme attribute set in a root inline script | Styling through JS props (`<Box p={4}>`) when a class or token works; `use client` on layout shells |
| Vue / Nuxt | `<style scoped>` or CSS Modules referencing tokens; `useHead` for theme-color and color-scheme; Nuxt Image with formats `['avif','webp']` | Inline `:style` objects for anything themable |
| Svelte / SvelteKit | Component-scoped CSS with tokens; `enhanced:img`; transitions via CSS where possible | Svelte transitions on every mount |
| Astro | Zero-JS by default; `<Image>`/`<Picture>`; scoped styles; islands with `client:visible` | Hydrating whole pages for one widget |
| Any | Keep design decisions in CSS and tokens; JS reads tokens via `getComputedStyle` when it must (charts, canvas) | Duplicating token values in a JS theme object that drifts from `tokens.css` |

Charts: pass series colours from tokens (`getComputedStyle(root).getPropertyValue('--chart-1')`) and re-read on theme change; never hard-code palette arrays.

## 9. Iconography implementation

- One icon set, one stroke width (commonly 1.5px at 24px), one corner style; do not mix Lucide with Heroicons.
- Delivery: inline SVG components (tree-shaken) or a sprite (`<use href="/icons.svg#arrow-right">`); no icon fonts.
- Colour via `fill="currentColor"` or `stroke="currentColor"`; size via `width`/`height` in `em` or a size token so icons scale with text.
- Decorative icons: `aria-hidden="true"` and `focusable="false"`. Icon-only buttons: `aria-label` on the button, not `<title>` in the SVG.
- Optical alignment: nudge with `translate` or `margin-block-start: -0.05em` next to text; a 16px icon beside 14px text sits on the x-height, not the baseline.
- Icon sizes as tokens: 16, 20, 24 (and 32 for empty states); never arbitrary.

## 10. Quality gates

| Gate | Tool | Pass condition |
|---|---|---|
| Slop lint | `scripts/slop_lint.py` over `src/**/*.{css,tsx,vue,svelte,astro}` | 0 raw hex/rgb, 0 `transition-all`, 0 `outline-none` without `focus-visible`, 0 arbitrary Tailwind values, ≤1 `backdrop-blur`, 0 `blur-3xl` |
| Contrast | `contrast-pairs.txt` checked by script against `build/tokens.css` in both themes | Every pair ≥4.5:1 text, ≥3:1 UI and placeholder |
| Accessibility | axe-core in Playwright on every route | 0 serious or critical |
| Lighthouse | CI on 3 key routes, mobile profile | Performance ≥90, Accessibility 100, CLS <0.1 |
| Visual regression | Playwright screenshots at 360, 768, 1440, both themes | Diff <0.1% or reviewed |
| Console | Playwright `page.on('console')` | 0 errors, 0 React/Vue warnings |
| Keyboard walkthrough | Manual or scripted `Tab` sequence per screen | Every control reachable, visible focus, logical order, `Escape` closes overlays |
| Reduced motion | Playwright `emulateMedia({ reducedMotion: 'reduce' })` | No motion >0.01ms except opacity |
| Reflow | 320px width and 400% zoom | No horizontal scroll, no clipped controls |

## 11. Web slop list (implementation level)

Any of these in a diff is a review blocker unless `DESIGN.md` records a reason.

| Signal | Why it reads as generated | Replace with |
|---|---|---|
| Untouched shadcn theme (default OKLCH values, single `--radius`) | Recognisable palette and radius | Section 1 table |
| `transition-all` | Animates layout properties, causes jank, signals no decision | Named properties: `transition: color .15s var(--ease-standard), background-color .15s ...` |
| `outline-none` / `focus:outline-none` | Removes keyboard focus | `:focus-visible` ring from tokens |
| `hover:scale-105` on cards, buttons, images | Layout-affecting motion on everything | Colour or border change; scale only on one designated hero object, if at all |
| `bg-white/70 backdrop-blur` sticky nav | Template default | Solid surface token with a 1px border token |
| `rounded-2xl shadow-lg p-6` card grid | The default card | Card spec from `components.md`: container radius token, border or surface step, density from `spacing-layout.md` |
| `text-center` on every section | No hierarchy, no reading direction | Left-aligned body; centre only short headings in Persuade heroes |
| `max-w-7xl mx-auto px-4` on every section | One rhythm for all content | Measure per content type: prose 60–75ch, tables full width, forms ≤40rem |
| Gradient text (`bg-clip-text text-transparent`) | 2023 template signature | Solid foreground token |
| `blur-3xl` orbs, `absolute -z-10 rounded-full bg-purple-500/30` | Decorative fog | Nothing, or a real image |
| Inline hex values, `text-[#333]`, `bg-[#0f172a]` | Bypasses tokens | Semantic token utility |
| Google Fonts `<link>` with 3–6 families | Slow, untyped, generic | Self-hosted ≤2 families, section 7 |
| `animate-pulse` on everything loading | Uniform shimmer | Skeleton sized like content, no animation under 300ms |
| `space-y-4` between unrelated sections | Uniform rhythm | Spacing scale steps that differ by relationship (`spacing-layout.md`) |
| Emoji as icons | Inconsistent across platforms | Icon set, section 9 |
| `z-[9999]` | Stacking wars | Popover API and `<dialog>` top layer |

## 12. Sources

- Tailwind CSS, Theme variables (namespaces, `initial`, `@theme inline`, `@theme static`): https://tailwindcss.com/docs/theme
- Tailwind CSS, Dark mode and `@custom-variant`: https://tailwindcss.com/docs/dark-mode
- Tailwind CSS, Adding custom styles (`@utility`, `@variant`): https://tailwindcss.com/docs/adding-custom-styles
- shadcn/ui, Theming and Tailwind v4: https://ui.shadcn.com/docs/theming and https://ui.shadcn.com/docs/tailwind-v4
- web.dev, Core Web Vitals thresholds: https://web.dev/articles/vitals
- web.dev, INP: https://web.dev/articles/inp
- web.dev, Optimize LCP: https://web.dev/articles/optimize-lcp
- web.dev, Optimize CLS: https://web.dev/articles/optimize-cls
- web.dev, Best practices for fonts: https://web.dev/articles/font-best-practices
- web.dev, New to the web platform, June 2026: https://web.dev/blog/web-platform-06-2026
- MDN, `light-dark()`: https://developer.mozilla.org/en-US/docs/Web/CSS/color_value/light-dark
- MDN, `color-mix()`: https://developer.mozilla.org/en-US/docs/Web/CSS/color_value/color-mix
- MDN, CSS anchor positioning: https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_anchor_positioning
- MDN, `@starting-style`: https://developer.mozilla.org/en-US/docs/Web/CSS/@starting-style
- MDN, View Transition API: https://developer.mozilla.org/en-US/docs/Web/API/View_Transition_API
- MDN, Popover API: https://developer.mozilla.org/en-US/docs/Web/API/Popover_API
- MDN, `<dialog>`: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/dialog
- MDN, `field-sizing`: https://developer.mozilla.org/en-US/docs/Web/CSS/field-sizing
- MDN, `interpolate-size`: https://developer.mozilla.org/en-US/docs/Web/CSS/interpolate-size
- MDN, `text-wrap`: https://developer.mozilla.org/en-US/docs/Web/CSS/text-wrap
- MDN, `size-adjust`: https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face/size-adjust
- MDN, `scrollbar-gutter`: https://developer.mozilla.org/en-US/docs/Web/CSS/scrollbar-gutter
- MDN, `@layer`: https://developer.mozilla.org/en-US/docs/Web/CSS/@layer
- Can I use, CSS anchor positioning: https://caniuse.com/css-anchor-positioning
- Style Dictionary, DTCG support: https://styledictionary.com/info/dtcg/
- W3C WCAG 2.2, Target Size (Minimum) 2.5.8: https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html
- W3C WCAG 2.2, Reflow 1.4.10: https://www.w3.org/WAI/WCAG22/Understanding/reflow.html
- Next.js, Font optimisation: https://nextjs.org/docs/app/building-your-application/optimizing/fonts
- Next.js, Image component: https://nextjs.org/docs/app/api-reference/components/image
- Deque, axe-core: https://github.com/dequelabs/axe-core
- Playwright, Visual comparisons: https://playwright.dev/docs/test-snapshots
