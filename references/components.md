# Components

A component is finished when it has every state, is built only from tokens, meets accessibility requirements, and
carries the system's voice in its copy. Generated UI ships the default state of a library component and calls it
done; that is where "assembled, not designed" comes from. This file gives the anatomy, the state matrix, the
craft floor, and per-component rules. Write specs with `templates/component-spec.md`.

## Contents

1. Component decision rules
2. The state matrix (mandatory)
3. Craft floor: details that read as designed
4. Buttons
5. Inputs and forms controls
6. Selection controls
7. Navigation components
8. Containers: cards, panels, lists, tables
9. Overlays: dialog, sheet, popover, menu, tooltip, toast
10. Feedback: empty, loading, error, progress, badges
11. Media, avatars, icons
12. Component slop
13. Checks

---

## 1. Component decision rules

- **Native element first** (`button`, `a`, `input`, `select`, `dialog`, `details`, `popover`), then a headless
  library (Radix, React Aria, Ark, Base UI), then custom. Styled kits (shadcn, MUI) are starting points whose every
  token must be replaced.
- **Reuse before creating.** A new component needs a written reason in its spec.
- **Variants over new components.** Size and emphasis are props, not new files.
- **One component, one job.** A card that is also a button, a link, and a menu is three components.
- **Composition over configuration.** Slots (`leading`, `trailing`, `footer`) beat 30 boolean props.
- **Tokens only.** Any literal color/size/font in a component file is a defect (`scripts/slop_lint.py`, grep).

## 2. The state matrix (mandatory)

Every interactive component defines all of these; non-interactive ones define the applicable subset.

| State | Trigger | Visual rule | A11y rule |
|---|---|---|---|
| default | — | tokens per variant | role + name |
| hover | pointer only (`@media (hover: hover)`) | one property changes (bg or underline), 120ms | never the only affordance |
| focus-visible | keyboard | 2px ring, 2px offset, `color.focus`, 3:1 vs adjacent; never removed | visible for all focusable |
| active / pressed | pointer down / key down | darker step or 1px translate / 0.98 scale, 80ms | — |
| selected / checked / current | state | fill or 2px border + icon or label, not color only | `aria-selected/checked/current` |
| disabled | prop | `opacity.disabled` on the whole control, `cursor: not-allowed`; text still ≥ 3:1 | `disabled` or `aria-disabled` (keep focusable when it explains why) |
| loading / busy | async | label stays, spinner replaces icon, width locked, no layout shift | `aria-busy` |
| error / invalid | validation | `border.status.danger` 1–2px + message below + icon | `aria-invalid`, `aria-describedby` |
| success | after action | brief confirmation (color/icon), then return to default | `aria-live="polite"` if not obvious |
| read-only | prop | no interactive affordance, normal text contrast | `readonly` |
| empty | no data | designed empty state, not blank | — |
| dark mode | mode | every token mapped | contrast re-checked |
| RTL | dir | mirrored layout, directional icons flipped, non-directional not | — |
| reduced motion | media query | transitions to opacity/none | — |
| forced colors | media query | borders visible, `currentColor`, system colors | — |

Missing states in generated UI, in order of frequency: focus-visible, loading, error, empty, pressed, forced colors.

## 3. Craft floor: details that read as designed

The cheapest signals that a UI was built rather than assembled. Do all of them.

- **Browser surfaces themed from tokens:** `::selection` (brand tint + readable text), `caret-color`, `scrollbar-color`
  / `::-webkit-scrollbar` (thin, surface-tinted), `accent-color` for native controls, focus ring, `text-underline-offset`
  (0.15em) and `text-decoration-thickness` (1px), `::placeholder` color at ≥ 3:1.
- **Numerals:** `font-variant-numeric: tabular-nums` in any column, timer, price, or counter.
- **Touch:** `-webkit-tap-highlight-color: transparent` with your own pressed state; `touch-action: manipulation`.
- **Cursor correctness:** pointer only on links/buttons, `text` on inputs, `grab/grabbing` on drag handles,
  `not-allowed` on disabled.
- **Icons:** `currentColor`, 1px optical alignment with x-height, consistent stroke, `aria-hidden` when decorative.
- **Truncation:** `text-overflow: ellipsis` or `line-clamp` with a tooltip/title for the full text; never let labels
  wrap to two lines on buttons.
- **Alignment:** button label optically centred (some faces need 1px extra bottom padding); icon + label gap `space.2`.
- **Hit areas** larger than visuals: 32px control → 44px hit area via padding or pseudo-element.
- **Transitions** explicit and short (`background-color 120ms var(--ease-standard)`), never `all`.
- **Pressed** feedback exists on everything clickable.
- **Loading** never shifts layout: reserve space, lock widths, skeletons match shapes.
- **Real characters:** `…`, curly quotes, `×` for close (or an icon), `–` for ranges.
- **Density parity:** all controls in a row share height (input 40 + button 40, not 38 + 44).

## 4. Buttons

| Rule | Value |
|---|---|
| Emphasis levels | primary (one per view) · secondary · tertiary/ghost · destructive · link-style |
| Heights | 32 / 40 / 48 (`size.control.*`); touch surfaces min 44 |
| Padding-x | 12 / 16 / 20; icon-only = square |
| Label | verb + object, sentence case, ≤ 3 words, no trailing arrow glyph by default |
| Radius | `radius.control`; pill only as a system-wide decision |
| Icon | 16/20 at `currentColor`, leading for meaning, trailing for direction/menu |
| Fill | solid; no gradients, no glow, no shadow unless the whole system is tactile |
| Hover | one step darker/lighter (`action.primary.hover`) |
| Pressed | one more step + 1px translate or 0.98 scale |
| Disabled | reduced opacity; explain why nearby if non-obvious |
| Loading | spinner replaces leading icon; label stays; width locked |
| Groups | primary right (LTR) on web/iOS/Android; destructive separated; ≤ 3 in a row |
| Destructive | secondary styling until confirmed; confirmation or undo required |

Never: two primaries side by side; "Submit"; disabled submit as validation; full-width buttons on desktop forms
(fine on mobile); icon-only without `aria-label` and tooltip.

## 5. Inputs and form controls

| Rule | Value |
|---|---|
| Label | visible, above the field, persistent; placeholder is a hint, never the label or realistic sample data |
| Height | matches button height in the same row |
| Width | ≈ expected input length (postcode short, email long); never all full-width on desktop |
| Border | `border.strong` 1px; focus adds ring, not a thicker border that shifts layout |
| Helper text | below, `text.secondary`, ≤ 1 line; error replaces helper, keeps position |
| Error | `status.danger` border + icon + specific message; `aria-invalid` + `aria-describedby` |
| Validation timing | on blur; after first error, re-validate on input; never on first keystroke |
| Required | mark optional fields when most are required, or mark required with text, not only `*` color |
| Types | correct `type`/`inputmode`/`autocomplete`; native pickers on mobile |
| Password | show/hide toggle, no forced composition rules, paste allowed, passkeys first |
| Textarea | `field-sizing: content` with min/max rows |
| Select | native `<select>` for ≤ 15 simple options; combobox with search beyond; never custom for the sake of styling |
| Search | `type="search"`, clear button, submit on Enter, results announce |
| Number/currency | text with `inputmode="decimal"`, formatted on blur, unit adornment inside the field |
| Date | native on mobile; on desktop a text field with mask + optional picker; show format |
| File | native input styled via label; drop zone dashed border (the only legit dashed border) |

## 6. Selection controls

| Control | Use when | Not when |
|---|---|---|
| Checkbox | multiple independent choices; a single opt-in that needs a save | instant effect (use switch) |
| Radio | 2–5 mutually exclusive, all visible; default selected | > 5 (select), or none-selected must be allowed (add an explicit option) |
| Switch | instant binary setting with immediate effect | anything requiring a save/confirm |
| Segmented control | 2–5 views of the same content | navigation between pages (tabs) or actions (buttons) |
| Chips (filter) | multi-select filters showing state | primary actions |
| Slider | approximate continuous value; show the value | precise entry (add a number field) |
| Stepper | small integer ranges | large ranges |

All: 20–24px visual, 44px hit area, label clickable, state not color-only (checkmark, dot, position), focus ring on
the control, keyboard operable (Space/Arrows), grouped with `fieldset/legend`.

## 7. Navigation components

| Component | Rules |
|---|---|
| Top nav (web) | ≤ 7 items, current item marked by more than color, logo → home, one primary action at most, sticky only if the page is long and nav is used mid-page; no `bg-white/70 backdrop-blur` reflex |
| Sidebar (app) | 200–280px, collapsible to icons with tooltips, groups with headings, current item filled, nested ≤ 1 level |
| Tab bar (mobile) | 3–5 items, icon + label, current filled, no more-menu as the 5th unless needed; iOS floating capsule (26), Android navigation bar |
| Tabs (in-page) | 2–7, underline or segmented, `aria-selected`, arrow-key navigation, URL reflects tab |
| Breadcrumbs | for hierarchies ≥ 3 deep; last item not a link; truncate middle on mobile |
| Pagination | page numbers for scannable sets, "load more" for feeds, infinite scroll only with a footer reachable |
| Command palette | ⌘K/Ctrl-K, fuzzy search, recent items, keyboard-only friendly; not a replacement for nav |
| Stepper | for linear multi-step; shows total, current, completed; back always possible |
| Back link | web: browser back + in-page "← Back to X" where the entry point isn't obvious |

## 8. Containers: cards, panels, lists, tables

- **Card** only when the card is the object (selectable, draggable, independently actionable). Anatomy: media
  (optional), title, metadata, one action or the whole card clickable (then no nested buttons; use a stretched
  link). Hover: subtle (bg tint or border), not lift+scale. No colored left border.
- **Panel/section**: heading + content separated by whitespace and, at most, a hairline.
- **List**: 40–56px rows, leading icon/avatar, primary + secondary text, trailing meta/chevron; dividers or spacing,
  not cards; swipe actions on mobile with visible alternatives.
- **Table**: text left, numbers right, `tabular-nums`, header sticky, first column sticky when wide, row hover, row
  height by density, sort indicators on header, filters above, bulk actions appear on selection, empty/loading/error
  rows, responsive by column priority (hide/collapse), never card-ify every row on mobile by default.
- **Accordion/disclosure**: `details/summary` or `aria-expanded`; one open at a time only when content is long;
  chevron rotates; not for primary content.

## 9. Overlays

| Component | Use | Rules |
|---|---|---|
| Dialog (modal) | decision or short task that must complete/abandon | `<dialog>`, focus trapped, Esc closes, returns focus, title = question or task, buttons specific verbs, max-width 480–640, no nested dialogs |
| Sheet (side/bottom) | longer tasks, filters, detail without losing context | side sheet 400–560 web; bottom sheet with detents on mobile; drag handle; scrim `color.scrim` |
| Popover | small contextual content anchored to a trigger | anchored (CSS anchor positioning / popover API), Esc + outside-click close, arrow optional, not for critical flows |
| Menu | list of actions | `role="menu"`, arrow keys, type-ahead, destructive item separated and red, icons optional but consistent |
| Tooltip | name/hint for icon-only controls | 300–500ms delay, `aria-describedby`, no interactive content, not for essential info, none on touch |
| Toast | non-blocking confirmation | 4–8s (longer with action), pause on hover, max 1–3 stacked, bottom-left/right (web) or top (mobile), `aria-live="polite"`; errors needing action are not toasts |
| Banner | persistent page-level status | top of content area, dismissible if non-critical, one at a time |

## 10. Feedback

- **Empty state**: what this is + why it's empty + one primary action (+ optional secondary "learn"); tone warm and
  specific; illustration only if the system has an illustration style; never "No data" alone.
- **Loading**: < 300ms nothing; 300ms–3s shape-matched skeleton (no shimmer on dark if it flickers); > 3s determinate
  progress or a background job with notification; never a full-page spinner for a partial update.
- **Error**: what happened + what to do + retry; inline for fields, banner for regions, dialog only if blocking;
  never only red, never blame, never raw codes.
- **Progress**: determinate when possible; steps for multi-stage; `aria-valuenow`.
- **Badge/count**: ≤ 99+ , tabular, min 20px, not color-only; status badges use icon + text.
- **Status dot**: only for live/presence states that actually change; never a decorative pulse.

## 11. Media, avatars, icons

- Images: fixed aspect via `aspect-ratio`, `object-fit`, `srcset`, alt per decision tree, placeholder color from the
  image's dominant tone, never stretched.
- Avatars: 24/32/40/48, initials fallback in a tinted surface with readable text (not random hue per user unless
  contrast-checked), status dot only when presence matters, never stock faces.
- Icons: one family, one stroke weight, sizes 16/20/24 on a grid, `currentColor`, labels for icon-only, no emoji, no
  ✨ for AI, custom marks for the 3–5 icons that define the product if the brand warrants it.

## 12. Component slop

Untouched shadcn card (`rounded-xl border bg-card shadow-sm p-6`) · glass cards · colored left border · icon in
tinted circle · gradient/glow buttons · pill "New ✨" badge · pulsing dot · placeholder-as-label · 38px input next to
44px button · toggle for save-required settings · custom select for styling · hover-only affordances · lift+scale
hover on every card · toast for errors that need action · nested modals · spinner for instant actions · emoji icons ·
"Submit" · two primaries · `outline: none`.

## 13. Checks

- Every component has the full state matrix, verified in light and dark.
- Only tokens in component code; no literals.
- Craft floor items applied globally (`::selection`, caret, scrollbar, focus, numerals, tap highlight).
- Hit areas ≥ 44 (touch) / 24 (WCAG minimum) with 8px spacing.
- Copy follows `content-microcopy.md`; button labels are verb + object.
- Keyboard: Tab order, Enter/Space, Esc, arrows in composites; focus visible everywhere.
- Loading and error never shift layout; empty states designed.
- Reduced-motion and forced-colors variants exist.
