# Spacing, Layout & Composition

Layout is where generated UI is most recognisable: the centered hero, the three cards, the bento, the identical
section rhythm, the card inside a card. The cause is **component-first assembly** — snapping blocks from a library
onto a page — instead of **composition** — deciding what the eye should meet first, second, third, and shaping space
to make that happen. This file covers the spacing system, grids, surface hierarchy, and how to compose pages and
app screens so they read as designed.

## Contents

1. Spacing system
2. Surface hierarchy: how to separate things (in order)
3. Radius, borders, elevation
4. Grid and containers
5. Breakpoints
6. Composition method (any surface)
7. Marketing / landing pages (Persuade)
8. Product / app UI (Operate)
9. Reading surfaces (Read)
10. Density and rhythm
11. Layout slop and fixes
12. Checks

---

## 1. Spacing system

- **Base unit 4px**; primary rhythm 8px. Scale: `0 2 4 6 8 12 16 20 24 32 40 48 64 80 96 128` (`space.0 … space.24`
  in tokens). Off-scale values (13px, 17px, 22px) are drift.
- **Semantic spacing** on top: `inset` (padding inside a container), `stack` (vertical gap between siblings),
  `inline` (horizontal gap), `gutter` (between columns), `margin.page`. Each has `xs sm md lg xl` mapped to the scale
  per density mode.
- **Proximity encodes relationship** (Gestalt): related items closer than unrelated. Concretely, the gap *inside* a
  group must be smaller than the gap *between* groups by at least one scale step, usually two.
  Heading → its paragraph: `stack.sm` (8–12). Paragraph → next heading: `stack.xl` (32–48).
- **Padding grows with container size**: small control 8–12, card 16–24, section 48–96 (fluid via `clamp()`), page
  margins 16 (mobile) → 24 → 48+.
- **Optical adjustments** beat mathematical ones: icons next to text sit 1–2px lower than centred; text inside
  buttons needs 1px more bottom padding for most faces; large radius needs more inner padding.
- Fluid space: `--space-section: clamp(3rem, 2rem + 4vw, 6rem)`; generate pairs like Utopia (min at 320, max at 1240).

## 2. Surface hierarchy: how to separate things (in order)

When two things need visual separation, use the **cheapest** device that works, in this order:

1. **Whitespace** (change the gap).
2. **Alignment** (a shared left edge or baseline groups more than any box).
3. **Typography** (weight/size change marks a new group).
4. **A 3–5% lightness shift** of the surface (`surface.sunken` / `surface.raised`).
5. **A hairline** (`border.subtle`, 1px, ≥ 3:1 only if it must be perceivable; otherwise very low contrast).
6. **Elevation** (shadow in light, lightness step in dark) — only for things that actually float: menus, popovers,
   modals, dragged items, sticky bars.
7. **A card** — only when the card *is* the interaction (a selectable, draggable, or independently actionable object).

Slop starts at step 7 and works backwards. Most generated UIs wrap everything in a bordered, shadowed card because
the model learned layout from component demos.

## 3. Radius, borders, elevation

**Radius hierarchy** (values per direction; the *relationship* is fixed):

| Token | Typical | Used for |
|---|---|---|
| `radius.none` | 0 | tables, dividers, full-bleed media |
| `radius.control` | 4–8 | buttons, inputs, chips, checkboxes |
| `radius.card` | 8–16 | cards, panels, popovers |
| `radius.sheet` | 16–28 | sheets, dialogs, large media |
| `radius.pill` | 9999 | pills, avatars, toggles |

Nested elements: `inner = outer − padding` (a 12px card with 8px padding holds 4px controls). Same radius on
everything = "bubbly template". Squircles / continuous corners on iOS.

**Borders:** hairline `1px` at low contrast for structure; `2px` only for focus and selected states. Never a colored
left/top border as decoration. Never dashed except drop zones.

**Elevation (light mode):** three levels max. Shadows are tinted with the surface hue (never pure black), have
two layers (ambient + key), and low opacity: `0 1px 2px oklch(… / 0.06), 0 4px 12px oklch(… / 0.08)`. Dark mode: no
shadows for elevation; step the surface lightness (+0.03–0.04 L per level) and add an optional 1px lighter inner
border. Buttons don't cast shadows unless the whole design is tactile.

## 4. Grid and containers

- **Columns:** 12 (web), 4 (phone), 8 (tablet). Gutter `space.6` (24) desktop, `space.4` (16) mobile. Margins ≥ gutter.
- **Content width:** cap long text at `65–75ch` (`size.measure.max`); cap page content at 1200–1440px; let media and
  backgrounds break out (`grid-column: 1 / -1`) — controlled asymmetry is what separates composed from templated.
- **One container per page, not per section.** Give sections different widths on purpose (narrow prose, wide table,
  full-bleed image).
- **CSS:** `display: grid` with named areas for page-level layout; flex for one-dimensional groups; container queries
  for components; `minmax(0, 1fr)` not `1fr` to prevent overflow; `gap` not margins between siblings; logical
  properties (`margin-inline`, `padding-block`) for RTL.
- **Alignment:** everything on the grid or deliberately off it. Text left-aligned; numbers right-aligned; icons
  optically aligned to the text x-height; baselines aligned across columns where the eye compares.

## 5. Breakpoints

Content-driven, named by the layout change, not the device. Typical: `narrow < 600` (single column), `regular
600–904` (two columns / rail), `wide 905–1239` (sidebar + content), `max ≥ 1240` (sidebar + content + aside). Test
at 320, 360, 390, 768, 1024, 1280, 1440, 1920. Mobile layouts must make *design* sense, not be stacked desktop
columns: reorder, drop, and change component type (table → priority columns; sidebar → tabs/bottom nav).

## 6. Composition method (any surface)

1. **List what's on the screen** by user priority (from the job stories), not by section template.
2. **Assign one focal point**: the largest, highest-contrast, first-read element. Exactly one per viewport.
3. **Decide the reading path**: Z (scanning, marketing), F (reading, lists), or single column (forms, mobile).
   Place the primary action where the path ends.
4. **Choose a structure** that fits the content's shape: sequence → steps; comparison → table/side-by-side;
   hierarchy → nested lists/tree; overview + detail → master-detail; one object → single column; many equal
   objects → grid; one dominant + supporting → 2:1 split.
5. **Set scale contrast**: the focal element is 2–3× the size of the next tier. Timid 1.25× contrast reads flat.
6. **Vary rhythm**: alternate dense and airy, wide and narrow, image and text. Identical section heights are a tell.
7. **Squint test**: blur the screen; the hierarchy should still be visible. Cover the logo; the brand should still
   be recognisable from type, color, and structure.
8. **Remove**: delete every element that doesn't serve the job or the focal point. Then remove one more thing.

## 7. Marketing / landing pages (Persuade)

- **First viewport = poster, not document.** Budget: brand, one headline (≤ 8 words), one supporting sentence, one
  action group, and **one designed visual anchor** (photograph, product, illustration, graphic device, color field,
  or video; see `visual-material.md` §2). The anchor is chosen before the type is set. A fact table can support the
  anchor; it cannot replace it. Full-bleed or deliberate asymmetry; no inset rounded hero panel.
- **No cards in the hero.** No pill badge above the headline. No two identical buttons.
- **Each section has one job** and its own composition. Ban the fixed skeleton (hero → 3 features → logos →
  testimonials → pricing → FAQ → CTA). Choose from structures that fit the argument:
  problem→proof→product; product walkthrough (long, scroll-driven); manifesto (typographic); comparison-led;
  single-feature deep dive; story (case study first); catalogue (for many SKUs); tool-first (interactive demo
  above the fold).
- **Features in context:** show the real UI doing the thing, one feature per section with a real caption. Icon-tile
  grids are the template; if a grid of small facts is genuinely needed, drop the icons and vary the cell sizes.
- **Proof only when real**: real logos, real numbers with source, real names. Otherwise omit; fake proof is slop and
  a trust risk.
- **Typographic scale is bigger here** (ratio 1.333+), measure still ≤ 70ch, generous section spacing (64–128).
- **Closing action**: one, specific, repeats the primary promise. Footer is navigation, not a fourth CTA.

## 8. Product / app UI (Operate)

- **Structure = primary workspace + navigation + secondary context.** Decide which is which per screen; the
  workspace gets ≥ 60% of the width.
- **Calm surface hierarchy**: one base surface, one raised for panels, one sunken for wells. Few colors; accent
  reserved for the primary action and selection.
- **Dense but readable**: body 14–16px, row height 40–48 (comfortable) / 32–36 (compact), consistent column
  alignment, `tabular-nums`.
- **Cards only when the card is the object** (a selectable item). Lists, tables, and sections separated by whitespace
  and hairlines otherwise. No KPI-card mosaics; dashboards answer 1–3 questions above the fold.
- **Navigation shaped by the object model**: nouns users think in, depth ≤ 2, current location always visible.
- **Section headings state what the area is or lets you do** ("Team members", "Billing"), not brand copy.
- **States are layout**: empty, loading (shape-matched skeletons), error, partial, and offline are designed for every
  region, not bolted on.
- **Toolbars**: primary action right (LTR), destructive separated, ≤ 5 visible actions, overflow menu after.
- **Forms**: single column, top-aligned labels, groups separated by `stack.xl`, field width ≈ input length.

## 9. Reading surfaces (Read)

Single column, 60–70ch, 18–20px body, line-height 1.6–1.7, generous paragraph spacing (`stack.md` = 1em),
headings with more space above than below, a sticky but quiet table of contents on wide screens, figures allowed to
break out to 80–90ch, code blocks full measure with horizontal scroll, footnotes inline-expandable. No sidebars
competing with the text; no cards for paragraphs.

## 10. Density and rhythm

Offer at most two density modes (comfortable/compact) via semantic spacing and control-size tokens; never per-screen
ad hoc spacing. Rhythm inside a screen: repeated units (rows, cards) share exact dimensions; between groups, spacing
steps up. Across a page, alternate. Across an app, keep the same density per surface mode.

## 11. Layout slop and fixes

| Slop | Fix |
|---|---|
| Centered hero + badge + two buttons | Left-aligned or asymmetric poster; one action; no badge |
| 3 icon cards | Product in context, one feature per section, or a plain two-column fact list |
| Bento by reflex | Only for genuinely unequal related facts; otherwise a list |
| Everything in a card; nested cards | Apply §2 order: whitespace → alignment → type → tint → hairline → elevation → card |
| Same `py-20` on every section | Section spacing tuned to each section's weight (32–128) |
| Uniform `rounded-2xl` | Radius hierarchy (§3) |
| `max-w-7xl` on every section | One page container; vary section widths; break-outs |
| Stacked desktop columns on mobile | Re-designed mobile structure (reorder, drop, change component type) |
| Dashboard of KPI cards | Workspace + context; 1–3 questions answered; tables/charts sized by importance |
| Sidebar + topbar + card grid admin template | Navigation from the object model; screen-specific layout |
| Decorative dividers (waves, blobs, dotted grids) | Remove; adjust spacing or add real content |

## 12. Checks

- One focal point per viewport; scale contrast ≥ 2× between tiers.
- All spacing on the 4px scale; inner gaps < outer gaps.
- Separation achieved with the cheapest device (§2); cards justified.
- Radius hierarchy applied; nested radii computed.
- Content measure ≤ 75ch; page container consistent; deliberate break-outs.
- Mobile layout redesigned, not stacked; no horizontal scroll at 320px.
- Section rhythm varies; no fixed skeleton.
- States (empty/loading/error) designed for each region.
- Squint test and cover-the-logo test pass.
