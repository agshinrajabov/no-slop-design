# Accessibility

Target WCAG 2.2 Level AA on every screen by default, treat AAA criteria as design targets where they are cheap
(focus appearance, target size, contrast), and verify with a keyboard, a screen reader, and `scripts/contrast.py`
before calling anything done. Accessibility failures are also slop tells (see `anti-slop.md` §9): a generated UI
that drops focus rings, labels inputs with placeholders, or encodes status in color alone reads as unfinished.
This file gives the exact numbers, attributes, and patterns; `color.md`, `typography.md`, `components.md`,
`mobile-ios.md`, and `mobile-android.md` hold the platform detail.

## Contents

1. Baseline: standards and law
2. Contrast
3. Keyboard and focus
4. Semantics and ARIA
5. Forms
6. Motion and vestibular safety
7. Color and perception
8. Touch and pointer
9. Text, zoom, and reflow
10. Media and images
11. Testing protocol
12. Mobile-native pointers
13. Checklist (40 items, POUR)
14. Sources

## 1. Baseline: standards and law

| Standard / law | Status (Sept 2026) | What it requires of you |
|---|---|---|
| WCAG 2.2 | W3C Recommendation since 5 Oct 2023; current normative version | Level AA is the default target; 4.1.1 Parsing was removed |
| WCAG 3.0 | Working Draft (March 2026 draft); Candidate Rec not expected before late 2027 | Not citable for compliance; contrast algorithm explicitly "to be determined" |
| EU Accessibility Act (Directive 2019/882) | Applies to products/services placed on the EU market since 28 June 2025 | Conformance is shown via EN 301 549; first enforcement cases filed late 2025 |
| EN 301 549 V3.2.1 | Harmonised EU standard; references WCAG 2.1 AA | V4 aligning to WCAG 2.2 pending; build to 2.2 AA and you cover both |
| ADA (US) | Title II rule (Apr 2024) mandates WCAG 2.1 AA for state/local government, phased 2026 and 2027; Title III enforced through litigation using WCAG as the de facto standard | WCAG 2.1 AA minimum, 2.2 AA recommended |
| Section 508 (US federal) | Incorporates WCAG 2.0 AA since 2018 refresh | Federal procurement; VPAT/ACR documents conformance |

### The nine criteria new in WCAG 2.2

| SC | Level | Exact requirement | Implementation note |
|---|---|---|---|
| 2.4.11 Focus Not Obscured (Min) | AA | Focused component is not *entirely* hidden by author content (sticky headers, cookie banners, chat widgets) | `scroll-padding-top` = sticky header height; banners must not cover the focus target |
| 2.4.12 Focus Not Obscured (Enh) | AAA | *No part* of the focused component is hidden | Same, stricter |
| 2.4.13 Focus Appearance | AAA | Indicator area at least a 2 CSS px thick perimeter of the component; 3:1 change between focused and unfocused states | 2px solid outline with 3:1 vs both the component and its background satisfies it |
| 2.5.7 Dragging Movements | AA | Anything done by dragging can be done with a single pointer without dragging, unless dragging is essential | Sliders get +/- buttons or a number input; sortable lists get "move up/down" |
| 2.5.8 Target Size (Min) | AA | Targets at least 24 by 24 CSS px. Exceptions: spacing (a 24px circle centred on the target intersects no other target), equivalent control elsewhere, inline in text, user-agent default, essential | See §8 |
| 3.2.6 Consistent Help | A | Help mechanisms (contact, chat, FAQ link) appear in the same relative order on every page where present | Put help in the same header/footer slot site-wide |
| 3.3.7 Redundant Entry | A | Information the user already entered in the same process is auto-populated or selectable, unless re-entry is essential, for security, or the data expired | "Billing same as shipping" checkbox; keep step data across a wizard |
| 3.3.8 Accessible Authentication (Min) | AA | No cognitive function test (memorise, transcribe, solve puzzle) at any step unless an alternative or assistance exists; object recognition and personal-content recognition are allowed | Allow paste in password fields; support password managers and passkeys; no "retype the code shown" without an alternative |
| 3.3.9 Accessible Authentication (Enh) | AAA | Same, without the object/personal-content exceptions | Passkeys, magic links, OAuth |

## 2. Contrast

WCAG 2.x ratios are the compliance baseline everywhere in 2026. APCA is a design-time readability tool: use it to
pick pairs that read well, then confirm the WCAG 2 ratio. Both are computed by `scripts/contrast.py`.

| Content | WCAG 2.x AA | WCAG 2.x AAA | SC |
|---|---|---|---|
| Body text (< 24px, or < 18.66px bold) | 4.5:1 | 7:1 | 1.4.3 / 1.4.6 |
| Large text (>= 24px regular, or >= 18.66px at weight >= 700) | 3:1 | 4.5:1 | 1.4.3 / 1.4.6 |
| UI component boundaries, states, focus indicators | 3:1 vs adjacent colors | n/a | 1.4.11 |
| Graphical objects needed to understand content (chart lines, icons) | 3:1 | n/a | 1.4.11 |
| Disabled controls, pure decoration, logos | exempt | exempt | 1.4.3 |
| Placeholder text | 4.5:1 (it is text) | 7:1 | 1.4.3 |

18pt = 24px and 14pt = 18.66px; WCAG counts CSS px at 96 dpi.

APCA Lc targets (polarity-aware; light-on-dark scores lower than the reverse):

| Lc | Use | Minimum size and weight (guidance) |
|---|---|---|
| 90 | Preferred for long-form body text | 14px/400 or 18px/300 |
| 75 | Minimum for body text columns | 16px/400, 18px/300, 14px/700 |
| 60 | Minimum for content text that is not body copy | 18px/400 or 14px/700 |
| 45 | Headlines, large labels, fine icons | 24px/700 or 36px/400 |
| 30 | Placeholder and disabled text, large solid icons | >= 5.5px stroke |
| 15 | Threshold of visibility for non-text elements | treat anything lower as invisible |

```bash
python3 scripts/contrast.py "#1a1a1a" "#fafaf7" --size 16 --weight 400   # WCAG ratio + APCA Lc
python3 scripts/contrast.py --pairs pairs.txt                             # exit 1 if any pair fails AA
```

Dark-mode traps: pure `#fff` on `#000` reads as halation for many readers (use L 0.90 to 0.95 text on L 0.10 to
0.15 surfaces per `color.md`); saturated brand colors that pass on white often fail on dark surfaces; borders at
step 6 of a dark scale rarely reach 3:1 and need step 7 or 8.

## 3. Keyboard and focus

| Rule | Value | Why |
|---|---|---|
| Tab order equals visual reading order | No positive `tabindex`; DOM order = visual order; avoid `order`/`flex-direction: row-reverse` on interactive rows | 2.4.3 Focus Order |
| Focus indicator is always visible | Never `outline: none` without a replacement; style `:focus-visible`, not `:focus` | 2.4.7, 2.4.13 |
| Ring geometry | 2px solid, `outline-offset: 2px`, 3:1 against adjacent colors; a two-tone ring (white inner, dark outer) passes on any background | 1.4.11, 2.4.13 |
| Skip link | First focusable element, `href="#main"`, visible on focus, target has `tabindex="-1"` | 2.4.1 |
| Escape closes | Dialogs, menus, popovers, comboboxes, tooltips | Expected by AT users; 1.4.13 |
| No traps | Focus can always leave by Tab or Escape; iframes and embeds included | 2.1.2 |
| Dialog focus | On open: move focus to the dialog (first field or the heading with `tabindex="-1"`); trap inside; on close: return to the invoker | ARIA APG dialog pattern |
| Menu focus | Open: first item; Arrow keys move; Home/End; type-ahead; Escape returns to trigger | APG menu pattern |
| Route change (SPA) | Move focus to the new page `<h1>` (or `<main tabindex="-1">`) and update `document.title`; announce via live region if focus cannot move | Nothing else tells a screen reader the page changed |
| Composite widgets | Roving `tabindex`: one item has `tabindex="0"`, the rest `-1`; arrows move the 0 | Tab reaches the widget once, arrows move within (tabs, toolbars, grids, listboxes, radiogroups) |
| Shortcuts | Single-character shortcuts need a way to turn off or remap, or only fire on focus | 2.1.4 |

```css
:focus-visible {
  outline: 2px solid var(--color-focus);   /* >= 3:1 vs surface and vs the control */
  outline-offset: 2px;
}
/* two-tone ring for arbitrary backgrounds */
.card:focus-visible { outline: 2px solid #fff; box-shadow: 0 0 0 4px #1a1a1a; }
html { scroll-padding-top: var(--header-height); }  /* 2.4.11 under sticky headers */
```

## 4. Semantics and ARIA

Order of preference: native element with built-in semantics, then native element plus one attribute, then ARIA
role plus the full keyboard contract from the ARIA Authoring Practices. No ARIA is better than bad ARIA: a
`<div role="button">` without `tabindex="0"`, Enter/Space handling, and a name is worse than a plain `<div>`.

| Need | Use | Not |
|---|---|---|
| Performs an action | `<button type="button">` | `<a href="#">`, `<div onclick>` |
| Navigates to a URL | `<a href>` | `<button>` with `location.href` |
| Modal | `<dialog>` + `showModal()` (gives focus trap, Escape, `inert` background) | hand-rolled overlay |
| Disclosure | `<details><summary>` | div with toggled class |
| Choice from list | `<select>`, `<input type="radio">` | custom listbox unless typeahead/multiselect is required |
| Status message | `role="status"` (polite) or `role="alert"` (assertive) | focus stealing, `alert()` |
| Decorative icon | `aria-hidden="true"` + `focusable="false"` on SVG | `alt="icon"` |

Accessible names, in resolution order: `aria-labelledby` (points at visible text; wins over everything), then
`aria-label` (invisible string; use only for icon-only controls), then native label (`<label for>`, button text,
`alt`), then `title` (unreliable; never rely on it). The visible label text must be contained in the accessible
name (2.5.3 Label in Name) so voice users can say what they see.

```html
<button type="button" aria-label="Close" aria-controls="filters" aria-expanded="true">
  <svg aria-hidden="true" focusable="false">…</svg>
</button>
<nav aria-label="Primary"><a href="/docs" aria-current="page">Docs</a></nav>
<section aria-labelledby="pricing-h"><h2 id="pricing-h">Pricing</h2></section>
<div role="status" aria-live="polite" class="sr-only" id="toast-region"></div>
<ul aria-busy="true" aria-describedby="loading-msg">…</ul>
```

| Attribute | When | Notes |
|---|---|---|
| Landmarks: `header/nav/main/aside/footer`, `role="search"`, `<form aria-label>` | Every page has exactly one `<main>`; label repeated landmarks (`<nav aria-label="Footer">`) | Screen reader users jump by landmark |
| Heading outline | One `<h1>`; no skipped levels; headings describe sections, never chosen for size (size comes from `typography.md` tokens) | Headings are the primary navigation for screen reader users |
| `aria-live="polite"` | Toasts, save confirmations, async results, character counters | Region must exist in the DOM before content is injected |
| `aria-live="assertive"` / `role="alert"` | Errors that block the task, session expiry | Interrupts; use rarely |
| `aria-invalid="true"` + `aria-describedby="err-id"` | Field with a visible error | Set on submit or blur, clear when fixed |
| `aria-busy="true"` | Region being replaced (skeletons, infinite scroll) | Remove when done; pair with a polite announcement |
| `aria-expanded` + `aria-controls` | Disclosure triggers, menus, accordions, comboboxes | State lives on the trigger, not the panel |
| `aria-current="page" / "step" / "true"` | Current nav item, wizard step, pagination page | Replaces color-only "active" styling |
| `aria-pressed` | Toggle buttons (bold, mute, favourite) | Not for tabs (use `role="tab"` + `aria-selected`) |
| `aria-describedby` | Helper text, formats, constraints | Read after the name; keep it short |
| `inert` | Everything outside an open modal, off-canvas drawers while closed | `<dialog>.showModal()` does this for you |

## 5. Forms

| Rule | Value | Why |
|---|---|---|
| Visible persistent label | `<label for>` above or beside every field; placeholder is a hint, not a label | Placeholder disappears on typing, fails 4.5:1 by default, is not read reliably (1.3.1, 3.3.2) |
| Autofill | `autocomplete` tokens: `name`, `given-name`, `family-name`, `email`, `tel`, `street-address`, `postal-code`, `country`, `cc-number`, `cc-exp`, `one-time-code`, `new-password`, `current-password`, `username` | 1.3.5 Identify Input Purpose; 3.3.7 |
| Keyboard type | `inputmode="numeric"` (PIN, OTP), `"decimal"`, `"tel"`, `"email"`, `"url"`; keep `type="text"` for numbers with formatting | Right mobile keyboard without spinner controls |
| Required | Mark in the label ("Email (required)") or `*` plus a legend explaining it; set `required` and `aria-required` only when the attribute is absent | Do not mark optional fields only when most are required, and vice versa |
| Error message | What happened plus how to fix it, inline next to the field, linked with `aria-describedby`, and repeated in a summary with links at the top of the form on submit; move focus to the summary or the first invalid field | 3.3.1, 3.3.3 |
| Error timing | Validate on blur; after a first error, re-validate on each input; never validate on first keystroke | Premature red states fail users mid-typing |
| Do not disable submit | Keep the button enabled; on click, validate and show every error | Disabled buttons give no feedback, are skipped by Tab, and fail contrast |
| Never block paste | No `onpaste="return false"`, no `autocomplete="off"` on password or code fields | 3.3.8 |
| Groups | `<fieldset><legend>` for radio groups, checkbox groups, address blocks | Legend is read with each option |
| Time limits | Warn before session timeout, allow extension, preserve entered data | 2.2.1, 3.3.7 |

```html
<label for="email">Email</label>
<input id="email" name="email" type="email" autocomplete="email" inputmode="email"
       aria-describedby="email-hint email-err" aria-invalid="true" required>
<p id="email-hint">We send the receipt here.</p>
<p id="email-err" class="error">Enter an email address in the format name@example.com.</p>
```

## 6. Motion and vestibular safety

| Rule | Value | SC |
|---|---|---|
| Respect `prefers-reduced-motion: reduce` | Keep: opacity and color transitions, instant state changes. Drop: parallax, scale/zoom, slide distances > 20px, auto-playing carousels and video, background motion, spring overshoot | 2.3.3 |
| Flashing | Nothing flashes more than 3 times per second, or the flashing area is below the general flash threshold | 2.3.1 |
| Auto-moving content longer than 5 s | Provide pause, stop, or hide (carousels, tickers, animated backgrounds) | 2.2.2 |
| Auto-play audio longer than 3 s | Provide a stop control or do not autoplay | 1.4.2 |

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation-duration: 0.01ms !important; animation-iteration-count: 1 !important;
                           transition-duration: 0.01ms !important; scroll-behavior: auto !important; }
}
```

Prefer per-component reduced variants over the blanket rule when the product is motion-heavy; see `motion.md` §8.

## 7. Color and perception

| Rule | Value | Why |
|---|---|---|
| No color-only meaning | Every status pairs color with an icon, text, or pattern; links inside body text get an underline, not only a hue | 1.4.1; ~8% of men have red-green deficiency |
| Red/green pairs | Add shape (check vs cross), text ("Passed"/"Failed"), or use blue/orange when only two hues are available | Deuteranopia sees them as the same brown |
| Charts | Direct labels, dashed/dotted line styles, texture fills, and a colorblind-safe ordinal palette (see `color.md`) | Legends that rely on 6 hues fail |
| Dark mode | Re-check every pair; desaturate accent chroma by ~0.02 to 0.04 in OKLCH; avoid pure black | Halation and chroma bloom |
| `prefers-contrast: more` | Raise borders to step 8, text to step 12, remove translucency and thin weights | Respects OS "Increase contrast" |
| `forced-colors: active` (Windows High Contrast) | Use `currentColor` for icons, system colors (`Canvas`, `CanvasText`, `ButtonText`, `Highlight`, `LinkText`), `border: 1px solid transparent` so outlines appear, `outline` not `box-shadow` for focus, `forced-color-adjust: none` only for color swatches | Backgrounds and shadows are stripped; only borders, outlines, and text survive |

```css
@media (forced-colors: active) {
  .btn { border: 1px solid ButtonText; }
  .toggle[aria-checked="true"]::after { background: Highlight; forced-color-adjust: none; }
  .swatch { forced-color-adjust: none; }
}
```

## 8. Touch and pointer

| Platform | Minimum | Recommended | Spacing |
|---|---|---|---|
| Web (WCAG 2.5.8 AA) | 24 x 24 CSS px, or a 24px circle that intersects no neighbour | 44 x 44 (2.5.5 AAA) | 8px between adjacent targets |
| iOS (HIG) | 44 x 44 pt | 44 x 44 pt | 8 pt |
| Android (Material) | 48 x 48 dp (about 9 mm) | 48 x 48 dp | 8 dp |

Extend the hit area with padding or a pseudo-element rather than enlarging the icon. Inline text links are
exempt from 2.5.8 but not from 44pt on native platforms when they are the primary control.

Hover-only content is forbidden (1.4.13 Content on Hover or Focus): tooltips and hover cards must be dismissible
(Escape) without moving the pointer, hoverable (pointer can move onto the content), and persistent (stays until
dismissed or invalid). Everything reachable by hover must be reachable by focus and by tap. Pointer cancellation
(2.5.2): fire actions on `click`/`pointerup`, never on `pointerdown`, so a user can slide off to abort.

## 9. Text, zoom, and reflow

| Rule | Value | SC |
|---|---|---|
| Zoom to 200% | No loss of content or function; layout may change | 1.4.4 |
| Reflow at 320 CSS px wide (400% on 1280) | Single column, no horizontal scroll for vertical content; exceptions: data tables, maps, diagrams, toolbars that need 2D | 1.4.10 |
| Text spacing override survives | line-height 1.5x, paragraph spacing 2x font size, letter-spacing 0.12em, word-spacing 0.16em with no clipping or overlap | 1.4.12 |
| Units | Font sizes in `rem`; spacing that must scale with text in `em`/`rem`; media queries in `em` | Respects browser font-size setting |
| `clamp()` for fluid type | Use `rem` in both min and max slots and a `vw` + `rem` middle term; a pure `vw` middle term does not respond to browser zoom, which fails 1.4.4 | `clamp(1rem, 0.9rem + 0.5vw, 1.25rem)` |
| Viewport meta | `width=device-width, initial-scale=1` only; never `user-scalable=no` or `maximum-scale=1` | 1.4.4 on mobile |
| Body line-height | >= 1.5 (see `typography.md`); line length 45 to 75 characters | 1.4.8, readability |
| Minimum body size | 16px default; 14px only for secondary text at 4.5:1 or better | Readability at arm's length |
| Truncation | Never hide critical text behind `text-overflow: ellipsis` without a full-text alternative (tooltip that meets 1.4.13, or wrap) | Names, amounts, and errors must be complete |

## 10. Media and images

Alt text decision tree:

| Image role | Markup | Text rule |
|---|---|---|
| Informative (adds meaning) | `<img alt="…">` | Describe content and purpose in <= 125 characters; no "image of" |
| Decorative (adds nothing) | `<img alt="">` or CSS background; inline SVG `aria-hidden="true" focusable="false"` | Empty, not missing |
| Functional (inside a link or button) | `alt` = the action or destination ("Search", "Home"), not the picture ("magnifier") | Matches visible label if any |
| Complex (chart, diagram, infographic) | Short `alt` naming the subject + long description adjacent or via `aria-describedby`/`<details>` | Include the data the chart shows, or a table |
| Text in image | Avoid; if unavoidable, `alt` = the exact text | 1.4.5 Images of Text |
| Meaningful inline SVG | `role="img"` + `<title id>` + `aria-labelledby` | `<title>` alone is inconsistently exposed |
| Icon fonts | `aria-hidden="true"` + adjacent text or `aria-label` on the control | Icon glyphs read as random letters |

Video needs synchronized captions (1.2.2) and audio description or a transcript (1.2.3/1.2.5); audio-only needs
a transcript (1.2.1). Autoplay: muted, with visible controls, and a pause button reachable by keyboard. Live
video needs live captions at AA (1.2.4).

## 11. Testing protocol

Automated tools find roughly 30 to 40% of issues by count in most independent evaluations (GDS: best single tool
40% of 142 seeded barriers; Deque reports 57% by volume for axe-core). Zero automated errors is the floor, not
the goal. Every screen also gets a keyboard pass and a screen reader pass.

| Tool | Use | Command / entry |
|---|---|---|
| axe-core | Engine behind most tools; run in unit/e2e tests | `@axe-core/playwright`, `jest-axe`, `axe DevTools` extension |
| Lighthouse | Quick score; audits axe subset plus contrast | Chrome DevTools > Lighthouse > Accessibility |
| pa11y / pa11y-ci | CLI crawl in CI | `npx pa11y-ci --sitemap https://site/sitemap.xml` |
| Accessibility Insights (Microsoft) | Guided manual assessment with tab-stop visualiser | FastPass, then Assessment |
| Browser a11y tree | Verify names, roles, states | Chrome DevTools > Accessibility pane; Firefox Inspector |

Manual keyboard pass: Tab through the whole page. Can you see where you are at every stop? Does order match
reading order? Does Enter/Space activate every control? Does Escape close every overlay? Does focus return to the
trigger? Is anything reachable by mouse that is not reachable by keyboard?

Screen reader quick commands:

| Action | VoiceOver macOS (VO = Ctrl+Option) | VoiceOver iOS | NVDA (Windows, Insert = NVDA key) | TalkBack (Android) |
|---|---|---|---|---|
| Toggle on/off | Cmd+F5 | Triple-click side button | Ctrl+Alt+N / NVDA+Q | Hold both volume keys 3 s |
| Next item | VO+Right | Swipe right | Down arrow | Swipe right |
| Activate | VO+Space | Double-tap | Enter | Double-tap |
| Read from here | VO+A | Two-finger swipe down | NVDA+Down | Two-finger swipe down / read from next item in menu |
| Next heading | VO+Cmd+H | Rotor set to Headings, swipe down | H | Swipe up/down to select "Headings", then swipe down |
| Next landmark / form field | VO+U (rotor) | Rotor | D / F | Reading controls menu |
| Rotor / element list | VO+U | Two-finger rotate | NVDA+F7 | Swipe up or down (reading controls) |
| Escape / back | Escape | Two-finger scrub (Z shape) | Escape | Swipe down then left |

Test on: VoiceOver + Safari (macOS, iOS), NVDA + Chrome or Firefox (Windows), TalkBack + Chrome (Android). JAWS if
the audience is enterprise or government. Also test at 200% zoom, at 320px width, with Windows High Contrast, and
with the OS "Reduce motion" setting on.

## 12. Mobile-native pointers

Details live in `mobile-ios.md` and `mobile-android.md`; the non-negotiables:

| Platform | Attribute or API | Rule |
|---|---|---|
| iOS | `accessibilityLabel` | Name, no control type ("Add to cart", not "Add to cart button") |
| iOS | `accessibilityTraits` | `.button`, `.header`, `.selected`, `.notEnabled`, `.updatesFrequently` |
| iOS | `accessibilityHint` | Optional outcome phrase; VoiceOver reads it after a pause |
| iOS | Dynamic Type | Use text styles (`.body`, `.headline`), support up to AX5 with reflow; test with Larger Accessibility Sizes |
| iOS | VoiceOver rotor | Headers, links, form controls: mark headers with `.header` so the rotor has something to jump to |
| iOS | `UIAccessibility.isReduceMotionEnabled`, `.isReduceTransparencyEnabled`, `.isBoldTextEnabled` | Branch motion and blur on these |
| Android | `contentDescription` | Same naming rule; `null` for decorative images; `importantForAccessibility="no"` |
| Android | TalkBack | Group related views with `screenReaderFocusable`; heading role via `ViewCompat.setAccessibilityHeading` / Compose `semantics { heading() }` |
| Android | Font scale | Use `sp` for text, never `dp`; test at 200% font scale and largest display size |
| Android | Touch targets | 48dp; `TouchDelegate` or `Modifier.minimumInteractiveComponentSize()` |
| Android | Animator duration scale | Read `Settings.Global.ANIMATOR_DURATION_SCALE`; Compose animations respect it |

## 13. Checklist (40 items)

Grouped by the four WCAG principles (POUR).

Perceivable
- [ ] Every informative image has descriptive `alt`; decorative images have `alt=""` or `aria-hidden`
- [ ] Body text >= 4.5:1, large text and UI parts >= 3:1, verified with `scripts/contrast.py` in both themes
- [ ] No information conveyed by color alone (icons, text, patterns, underlines present)
- [ ] Video has captions; audio has transcripts; autoplay is muted and stoppable
- [ ] Headings form a correct outline with one `<h1>` and no skipped levels
- [ ] Landmarks present: one `<main>`, labelled `<nav>`s, `<header>`, `<footer>`
- [ ] Layout survives 200% zoom and 320px reflow without horizontal scroll or clipped text
- [ ] Text spacing override (1.5 / 2 / 0.12em / 0.16em) causes no overlap or truncation
- [ ] Font sizes in `rem`; no `user-scalable=no`
- [ ] Forced-colors mode shows borders, focus, and icons (uses `currentColor` and system colors)

Operable
- [ ] Every action works with keyboard alone; no mouse-only or hover-only features
- [ ] Focus visible at every stop: 2px ring, 2px offset, 3:1 contrast, never removed
- [ ] Tab order matches visual order; no positive `tabindex`
- [ ] Skip link is the first focusable element and works
- [ ] No keyboard trap; Escape closes dialogs, menus, popovers, tooltips
- [ ] Dialogs move focus in on open and back to the trigger on close; background is `inert`
- [ ] SPA route changes move focus to the new `<h1>` or `<main>` and update `document.title`
- [ ] Focused elements are not hidden under sticky headers or banners (`scroll-padding-top`)
- [ ] Targets >= 24 x 24 CSS px web, 44pt iOS, 48dp Android, with 8px spacing
- [ ] Every drag interaction has a tap or keyboard alternative
- [ ] Actions fire on `click`/`pointerup`, not `pointerdown`
- [ ] Nothing flashes > 3 times per second; auto-moving content > 5 s has pause/stop
- [ ] `prefers-reduced-motion` removes parallax, scaling, auto-play, and large slides
- [ ] Time limits can be extended; entered data survives a timeout
- [ ] Single-key shortcuts can be disabled or remapped

Understandable
- [ ] Every input has a visible persistent label; placeholder is a hint only
- [ ] Correct `autocomplete` and `inputmode` on every field that has a matching token
- [ ] Errors say what happened and how to fix it, inline plus summary, linked with `aria-describedby`, `aria-invalid` set
- [ ] Validation runs on blur, re-runs on input after an error; submit is never disabled as validation
- [ ] Paste is never blocked; password managers and passkeys work; no cognitive-test-only auth
- [ ] Required fields marked in the label; legend explains the marker
- [ ] Previously entered data is auto-filled within a multi-step flow
- [ ] Help links appear in the same place on every page
- [ ] `lang` attribute set on `<html>` and on any passage in another language
- [ ] Link text is meaningful out of context (no "click here"; see `content-microcopy.md`)

Compatible (WCAG principle 4)
- [ ] Native elements used for buttons, links, inputs, dialogs, disclosures before any ARIA
- [ ] Every custom widget follows the ARIA APG keyboard contract and exposes name, role, state
- [ ] Icon-only controls have `aria-label`; visible label text is contained in the accessible name
- [ ] Live regions exist before content is injected; toasts use `role="status"`, blocking errors `role="alert"`
- [ ] axe-core reports zero violations in CI, and one VoiceOver or NVDA pass plus one TalkBack or iOS VoiceOver pass is recorded per release

## 14. Sources

- W3C WAI, What's New in WCAG 2.2: https://www.w3.org/WAI/standards-guidelines/wcag/new-in-22/
- W3C, WCAG 2.2 Recommendation: https://www.w3.org/TR/WCAG22/
- W3C, WCAG 3.0 Working Draft: https://www.w3.org/TR/wcag-3.0/
- Adrian Roselli, WCAG 3 Contrast as of April 2026: https://adrianroselli.com/2026/04/wcag3-contrast-as-of-april-2026.html
- W3C WAI, ARIA Authoring Practices Guide (patterns): https://www.w3.org/WAI/ARIA/apg/patterns/
- W3C WAI, Images Tutorial (alt decision tree): https://www.w3.org/WAI/tutorials/images/decision-tree/
- W3C WAI, Forms Tutorial: https://www.w3.org/WAI/tutorials/forms/
- European Commission, European Accessibility Act: https://commission.europa.eu/strategy-and-policy/policies/justice-and-fundamental-rights/disability/union-equality-strategy-rights-persons-disabilities-2021-2030/european-accessibility-act_en
- ETSI, EN 301 549 V3.2.1: https://www.etsi.org/deliver/etsi_en/301500_301599/301549/03.02.01_60/en_301549v030201p.pdf
- US DOJ, ADA Title II Web Rule: https://www.ada.gov/resources/2024-03-08-web-rule/
- APCA in a Nutshell: https://git.apcacontrast.com/documentation/APCA_in_a_Nutshell
- MDN, `:focus-visible`: https://developer.mozilla.org/en-US/docs/Web/CSS/:focus-visible
- MDN, `forced-colors`: https://developer.mozilla.org/en-US/docs/Web/CSS/@media/forced-colors
- MDN, `prefers-reduced-motion`: https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion
- MDN, HTML `autocomplete` attribute: https://developer.mozilla.org/en-US/docs/Web/HTML/Attributes/autocomplete
- Apple HIG, Accessibility: https://developer.apple.com/design/human-interface-guidelines/accessibility
- Android Developers, Make apps more accessible: https://developer.android.com/guide/topics/ui/accessibility/apps
- Android Accessibility Help, Touch target size: https://support.google.com/accessibility/android/answer/7101858
- GOV.UK GDS, What we found when we tested tools on the world's least-accessible webpage: https://accessibility.blog.gov.uk/2017/02/24/what-we-found-when-we-tested-tools-on-the-worlds-least-accessible-webpage/
- Deque, Automated Accessibility Coverage Report: https://www.deque.com/automated-accessibility-coverage-report/
- Deque, axe-core: https://github.com/dequelabs/axe-core
- NVDA keyboard commands: https://www.nvaccess.org/files/nvda/documentation/keyCommands.html
- Apple, VoiceOver gestures on iPhone: https://support.apple.com/guide/iphone/learn-voiceover-gestures-iph3e2e2281/ios
- Google, TalkBack gestures: https://support.google.com/accessibility/android/answer/6151827
