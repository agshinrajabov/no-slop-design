# Motion

Motion in UI has four jobs: confirm an action (feedback), show where something came from or went (orientation and
spatial continuity), pull the eye to a change that needs it (attention), and, rarely and once per product, carry
a brand signature. Anything else is decoration and reads as slop (see `anti-slop.md` §7). The operating rule:
one orchestrated entrance per screen at most, then motion only for state change. Every value below is a token
(see §9 and `design-tokens.md`); nothing is hard-coded in components.

## Contents

1. When motion is allowed
2. Duration
3. Easing and springs
4. Performance rules
5. Modern CSS: View Transitions, `@starting-style`, scroll-driven animation
6. Choreography patterns
7. Micro-interaction catalog
8. Reduced motion
9. Tokens
10. Motion slop list
11. Review checklist
12. Sources

## 1. When motion is allowed

| Job | Example | If removed, what breaks |
|---|---|---|
| Feedback | Button press, toggle flip, checkbox draw, ripple | User doubts the tap registered |
| Orientation | Sheet slides from the edge it lives on; list item expands into detail; back reverses forward | User loses where they are in the hierarchy |
| Attention | New toast enters; field shakes once on invalid submit; badge count bumps | User misses a change outside their focus |
| Brand signature | One launch or first-load choreography; a logo mark animation | Nothing functional; keep to one place, <= 800ms, skippable |

Test for each animation: name its job from this table. If the answer is "it looks alive" or "it fills the wait",
delete it. Content must be fully visible and usable with all animation disabled.

## 2. Duration

| Element or distance | Enter | Exit | Notes |
|---|---|---|---|
| Micro feedback (press, ripple start, color change) | 80 to 100ms | same | Below 80ms is not perceived as motion |
| Hover, toggle, checkbox, switch, focus ring | 120 to 150ms | 100ms | |
| Reveal: dropdown, tooltip, popover, menu, accordion panel | 200 to 250ms | 150 to 200ms | Origin-anchored (see §7) |
| Sheet, drawer, dialog, page-level transition | 300 to 400ms | 200 to 300ms | Larger distance, longer time |
| Full-screen, hero, container transform on mobile | 400 to 500ms | 300 to 350ms | >= 500ms only here, and only once per flow |
| Stagger between list items | 20 to 50ms per item | reverse order, 0 to 20ms | Cap total choreography at 300ms; stagger at most 6 to 8 items, rest appear together |

Rules: exits are 20 to 30% shorter than entrances (the user already decided to leave). Small elements move
faster than large ones. Elements travelling farther take longer, but never past the cap. On desktop, shave 10 to
20% off mobile values; on large tablets add 10%. Delay on hover-triggered reveals (tooltips) is 300 to 500ms;
delay on state-change motion is 0.

Perception anchors: 100ms feels instant; 1 s keeps the flow of thought; 10 s loses attention (NN/g). Anything
under 300ms needs no loading indicator at all.

## 3. Easing and springs

| Token | cubic-bezier | Use | Why |
|---|---|---|---|
| `standard` | `(0.2, 0, 0, 1)` | Elements that move on screen and stay (position, size change) | Fast start, soft landing; reads as physical |
| `decelerate` | `(0, 0, 0, 1)` | Entering elements (menus, sheets, toasts) | Starts at full speed as if already moving, settles into place |
| `accelerate` | `(0.3, 0, 1, 1)` | Exiting elements | Leaves with increasing speed; no lingering |
| `emphasized` | `(0.2, 0, 0, 1)` at longer duration, or M3 emphasized keyframes | Hero container transforms | Reserved for the one signature moment |
| `linear` | `linear` | Opacity-only fades under 150ms, progress bars, color | Perceptual curves add nothing to a fade |

Why `ease-in-out` is wrong for most UI: it starts slowly, so the first 50ms look like lag, and it ends slowly, so
a 250ms transition feels like 350. UI elements should react instantly (decelerate for things arriving, standard
for things moving) and only accelerate when leaving. Use symmetric curves for looping or ambient motion only.

Springs replace curves when the motion can be interrupted mid-flight (gesture-driven sheets, drag release,
toggles the user can flick back) or when velocity must carry over from a gesture. Springs are defined by physics,
so there is no fixed duration; the framework computes it.

| Framework | Parameters | Sensible defaults |
|---|---|---|
| Physics (generic) | stiffness k, damping c, mass m; damping ratio = c / (2 * sqrt(k * m)); ratio 1 = no overshoot | k 300 to 500, ratio 0.8 to 1.0 for UI; ratio 0.6 to 0.7 only for playful elements |
| SwiftUI | `.spring(response:, dampingFraction:)`; presets `.smooth` (no bounce), `.snappy` (slight), `.bouncy` (visible) | `response: 0.35, dampingFraction: 0.85` for sheets; `.snappy` for toggles |
| Material 3 Expressive (Compose `MotionScheme`) | Spatial springs (position, size; may overshoot) vs effects springs (color, opacity; damping ratio 1, never overshoot); each in fast / default / slow | Expressive scheme approx.: spatial default stiffness 380, ratio 0.8; fast 800 / 0.6; slow 200 / 0.8; effects default stiffness 1600, ratio 1.0. Standard scheme uses ratio 0.9 and stiffer springs. Check current Compose source for exact numbers |
| Framer Motion / Motion for React | `type: "spring", stiffness, damping, mass` or `duration` + `bounce` | `{ stiffness: 400, damping: 35 }` for UI; `{ duration: 0.3, bounce: 0 }` when a fixed length is needed |
| CSS (2026) | `linear()` easing can approximate a spring with generated stops | Generate stops from a spring solver; no native CSS spring |

Rule: effects (color, opacity) never overshoot. Overshoot on position is allowed only when ratio >= 0.7 and
the element is user-driven (dragged, flicked). Never bounce a dialog, a toast, or a page.

## 4. Performance rules

| Rule | Value | Why |
|---|---|---|
| Animate only `transform` and `opacity` | Also allowed: `filter` (careful), `clip-path`, `background-color` on small elements | These run on the compositor; no layout, no paint |
| Never animate layout properties | `width`, `height`, `top`, `left`, `margin`, `padding`, `font-size`, `border-width`, `box-shadow` | Each frame triggers layout and paint on the whole subtree |
| Fake the expensive ones | Height reveal: `grid-template-rows: 0fr` to `1fr` or `transform: scaleY` on a clip; shadow lift: cross-fade two pre-rendered shadows via `opacity` | Same visual, compositor-only |
| `will-change` | Add just before an animation starts, remove after; never on more than a handful of elements; never in a stylesheet globally | Each promoted layer costs GPU memory |
| Frame budget | 16.7ms per frame at 60Hz, 8.3ms at 120Hz; JS on the main thread during an animation should stay under 4ms | Dropped frames are more noticeable than no animation |
| `content-visibility: auto` | On long lists and off-screen sections; pair with `contain-intrinsic-size` | Skips rendering work outside the viewport |
| Reduce concurrent animations | <= 3 simultaneous animated layers on mobile | Compositor thrash on mid-range Android |
| Prefer CSS or Web Animations API over rAF loops | WAAPI: `el.animate(keyframes, {duration, easing, fill})` | Runs off main thread when possible; respects reduced-motion hooks |
| Measure | Chrome DevTools Performance panel, Layers panel, `Rendering > Paint flashing`; Xcode Instruments Core Animation; Android GPU rendering profile | "Looks smooth on my M-series laptop" is not a measurement |

```css
.card { transition: transform 150ms cubic-bezier(0.2, 0, 0, 1), opacity 150ms linear; } /* explicit, never `all` */
.card:hover { transform: translateY(-1px); }
.shadow-lift { position: relative; }
.shadow-lift::after { content: ""; position: absolute; inset: 0; box-shadow: var(--shadow-3); opacity: 0;
                      transition: opacity 150ms linear; pointer-events: none; }
.shadow-lift:hover::after { opacity: 1; }
```

## 5. Modern CSS: View Transitions, `@starting-style`, scroll-driven animation

### View Transitions API (route and shared-element transitions)

Same-document (SPA), broadly supported in 2026:

```js
if (!document.startViewTransition) { updateDOM(); }
else { document.startViewTransition(() => updateDOM()); }
```

```css
.thumb  { view-transition-name: hero-image; }     /* same name on the old thumb and the new hero */
::view-transition-old(root), ::view-transition-new(root) { animation-duration: 250ms; }
::view-transition-group(hero-image) { animation-timing-function: cubic-bezier(0.2, 0, 0, 1); animation-duration: 350ms; }
@media (prefers-reduced-motion: reduce) { ::view-transition-group(*), ::view-transition-old(*), ::view-transition-new(*) { animation: none !important; } }
```

Cross-document (MPA) transitions opt in with `@view-transition { navigation: auto; }` on both pages; customise
in the `pageswap` (source) and `pagereveal` (destination) events. Support is narrower than same-document; keep it
progressive. `view-transition-name` must be unique per document at snapshot time; `view-transition-class`
lets many items share one animation rule (e.g. list rows).

### Entry and exit of `display: none`, `popover`, `<dialog>`

```css
[popover] { opacity: 0; transform: translateY(4px);
            transition: opacity 200ms linear, transform 200ms cubic-bezier(0, 0, 0, 1),
                        display 200ms allow-discrete, overlay 200ms allow-discrete; }
[popover]:popover-open { opacity: 1; transform: none;
  @starting-style { opacity: 0; transform: translateY(4px); } }
dialog::backdrop { transition: opacity 200ms linear, display 200ms allow-discrete, overlay 200ms allow-discrete; opacity: 0; }
dialog[open]::backdrop { opacity: 1; @starting-style { opacity: 0; } }
```

`@starting-style` supplies the "from" state for an element that had no previous rendered state;
`transition-behavior: allow-discrete` (here via the shorthand) lets `display` and `overlay` flip at the end of
the exit instead of instantly. Baseline since August 2024. Exit uses `accelerate` and a shorter duration.

### Scroll-driven animations

`animation-timeline: scroll()` (progress of a scroller) and `view()` (progress of an element through the
viewport) replace IntersectionObserver reveal libraries and run on the compositor. Legitimate uses: reading
progress bar, header condense on scroll, a sticky table header shadow, image reveal in a long editorial page.
Not legitimate: fading up every section of a marketing page (§10). Always wrap in reduced-motion and
`@supports (animation-timeline: scroll())`.

```css
@supports (animation-timeline: scroll()) {
  .progress { animation: grow linear both; animation-timeline: scroll(root); transform-origin: left; }
  @keyframes grow { from { transform: scaleX(0); } to { transform: scaleX(1); } }
}
```

## 6. Choreography patterns

| Pattern | Use | Spec |
|---|---|---|
| Container transform | Card to detail, FAB to sheet, search field to results | Outgoing and incoming share bounds; 300 to 400ms `standard`; content fades out first 90ms, container morphs, new content fades in last 210ms; implement with View Transitions or shared element APIs |
| Shared axis (X / Y / Z) | Sibling screens: onboarding steps (X), tabs in a bottom bar (X), parent to child in a list (Z), step forms (Y) | Outgoing: fade out 90ms + move 30px along axis; incoming: fade in 210ms + move from 30px; total 300ms; back reverses direction |
| Fade through | Unrelated screens (bottom nav destinations), theme switch | Out 90ms opacity, in 210ms opacity + scale 0.92 to 1 |
| List add / remove (FLIP) | Reorder, insert, delete, filter | First, Last, Invert, Play: measure before and after, apply inverse `transform`, animate to identity in 200 to 250ms `standard`; removed item fades and scales to 0.96 in 150ms `accelerate`; neighbours slide with FLIP; stagger <= 30ms |
| Skeleton to content | Data fetch with known layout | Skeleton matches the final shape (line count, image aspect); show only if load > 300ms; cross-fade to content in 150ms; never bounce content into place |
| Optimistic UI | Like, save, toggle, add to cart | Apply the final state in < 100ms with the micro feedback; roll back with a 150ms fade and an inline error if the request fails; do not show a spinner |
| Loading indicators | Nothing < 300ms; skeleton or indeterminate indicator 300ms to 3 s; determinate progress with real percentage > 3 s; add text ("Uploading 3 of 12") > 10 s | A spinner that flashes for 80ms reads as a glitch |
| Toast stack | Notifications | New toast enters from its edge 200ms `decelerate`; older toasts shift with FLIP; auto-dismiss >= 5 s, pausable on hover/focus; exit 150ms `accelerate` |
| Error shake | Invalid submit on a password or PIN field | One shake: translateX 0, -6, 6, -4, 4, 0 over 300ms; never repeat; pair with the error text |

## 7. Micro-interaction catalog

| Interaction | Enter | Exit | Detail |
|---|---|---|---|
| Button press | 80ms `scale(0.98)` or `translateY(1px)` on `:active` | 120ms back | Never scale above 1 on hover; hover changes color/underline |
| Toggle switch | Thumb 150ms `standard`, track color 150ms `linear` | same | Overshoot only if spring ratio >= 0.7 and gesture-driven |
| Checkbox | Check-draw via `stroke-dashoffset` 150ms `decelerate`; box fill 100ms | Fill 100ms, mark 80ms | |
| Radio | Dot scales 0 to 1, 120ms `decelerate` | 100ms | |
| Input focus | Border color and ring 120ms `linear` | 120ms | Label float, if used, 150ms `standard` |
| Tooltip | Show after 300 to 500ms hover/focus delay; fade + 4px move, 150ms `decelerate` | 100ms fade | No delay when moving between tooltips in the same group |
| Menu / popover | 200ms `decelerate`, `transform-origin` at the trigger edge, scale 0.96 to 1 + fade | 150ms `accelerate` | Origin-anchored, or it looks like it fell from the sky |
| Accordion | Height via `grid-template-rows`, 200 to 250ms `standard`; chevron rotates 200ms | 200ms | |
| Tabs | Indicator slides 200ms `standard`; panel fade-through 150ms | | |
| Dialog | Scale 0.96 to 1 + fade, 250ms `decelerate`; backdrop fade 200ms | 150ms `accelerate` | Focus moves in during the animation, not after |
| Bottom sheet | Translate from bottom edge, 300ms `decelerate` or spring `response 0.35, ratio 0.85` | 250ms `accelerate` | Follows finger during drag, then springs to snap point |
| Toast | See §6 | | |
| Drag lift | 150ms: shadow opacity to elevation 3, scale 1.02, cursor `grabbing` | Drop: 200ms `standard` to slot | Haptic light impact on lift (mobile) |
| Pull to refresh | Indicator follows finger with 0.5 resistance; at threshold, 100ms snap + haptic | Collapse 200ms | Native components preferred (see `mobile-ios.md`, `mobile-android.md`) |
| Selection / checkmark confirm | 100ms color + 150ms mark draw | | Haptic selection tick on mobile |
| Haptics pairing (iOS `UIImpactFeedbackGenerator`, Android `HapticFeedbackConstants`) | Light: toggle, selection; Medium: drag lift, threshold reached; Success/Error notification: completed payment, failed submit | | Never on hover or scroll; at most one haptic per user action |

## 8. Reduced motion

Strategy: reduced motion is a different design, not a switch that breaks the current one. Keep opacity and color
changes, instant state swaps, and progress indicators. Remove parallax, scale beyond 1.02, slides longer than
20px, auto-playing carousels and video, ambient background motion, spring overshoot, and scroll-driven effects.
Cross-fades under 200ms are safe for nearly everyone.

```css
@media (prefers-reduced-motion: reduce) {
  :root { --duration-fast: 0ms; --duration-base: 0ms; --duration-slow: 0ms; }
  .sheet, .menu, [popover] { transition-property: opacity; transform: none !important; }
  .parallax, .marquee { animation: none; transform: none; }
}
@media (prefers-reduced-motion: no-preference) { .hero-mark { animation: signature 700ms var(--ease-emphasized) both; } }
```

```js
const mq = matchMedia('(prefers-reduced-motion: reduce)');
const reduced = () => mq.matches || document.documentElement.dataset.motion === 'reduced';
mq.addEventListener('change', applyMotionPrefs);
```

Also expose an app-level toggle (Settings > Appearance > Reduce motion) that sets `data-motion="reduced"` on
`<html>`; store it per user. Native: read `UIAccessibility.isReduceMotionEnabled` (iOS) and the animator duration
scale (Android). View Transitions and scroll-driven animations must be disabled under the same query (§5).
Legal floor is in `accessibility.md` §6: no flashing > 3/s, pause for auto-moving content > 5 s.

## 9. Tokens

Define motion in the DTCG format (`design-tokens.md` covers the pipeline) and emit CSS custom properties plus
platform constants. Duration is `{ "value": n, "unit": "ms" }`; easing is `cubicBezier` `[x1, y1, x2, y2]`;
the `transition` composite type bundles duration, delay, and timing function.

```json
{
  "duration": {
    "instant": { "$type": "duration", "$value": { "value": 80,  "unit": "ms" } },
    "fast":    { "$type": "duration", "$value": { "value": 150, "unit": "ms" } },
    "base":    { "$type": "duration", "$value": { "value": 250, "unit": "ms" } },
    "slow":    { "$type": "duration", "$value": { "value": 350, "unit": "ms" } },
    "slower":  { "$type": "duration", "$value": { "value": 500, "unit": "ms" } }
  },
  "easing": {
    "standard":   { "$type": "cubicBezier", "$value": [0.2, 0, 0, 1] },
    "decelerate": { "$type": "cubicBezier", "$value": [0, 0, 0, 1] },
    "accelerate": { "$type": "cubicBezier", "$value": [0.3, 0, 1, 1] },
    "emphasized": { "$type": "cubicBezier", "$value": [0.2, 0, 0, 1] }
  },
  "transition": {
    "reveal": { "$type": "transition", "$value": { "duration": "{duration.base}", "delay": { "value": 0, "unit": "ms" }, "timingFunction": "{easing.decelerate}" } }
  }
}
```

```css
:root { --duration-instant: 80ms; --duration-fast: 150ms; --duration-base: 250ms; --duration-slow: 350ms; --duration-slower: 500ms;
        --ease-standard: cubic-bezier(0.2, 0, 0, 1); --ease-decelerate: cubic-bezier(0, 0, 0, 1);
        --ease-accelerate: cubic-bezier(0.3, 0, 1, 1); --ease-emphasized: cubic-bezier(0.2, 0, 0, 1); }
```

Naming: semantic tiers (`instant / fast / base / slow / slower`) rather than raw numbers so a product-wide
retune touches one file. Component tokens reference tiers: `menu.enter.duration = {duration.base}`. Spring
tokens (native) store `stiffness`, `dampingRatio`, `mass` as plain numbers under `spring.spatial.*` and
`spring.effects.*`.

## 10. Motion slop list

Expanded from `anti-slop.md` §7. Any item present is a fail in review unless the brief names it explicitly.

| Tell | Why it fails | Replace with |
|---|---|---|
| Fade-up on every section (`whileInView`, AOS, `data-aos="fade-up"`) | Signals a template; delays content; breaks with reduced motion | Content visible at rest; one entrance at page load if any |
| `whileInView` reflex on cards, stats, testimonials | Same as above; ten identical reveals per scroll | Static layout; motion only on interaction |
| Typewriter headline | Hides the message; unreadable for screen readers mid-typing; 2023 AI-landing cliche | Set the headline in type (`typography.md`) |
| Blinking cursor, terminal cosplay | Decorative flicker; fails the "job" test | Remove |
| Marquee / infinite logo ticker | Auto-moving > 5 s needs pause (2.2.2); unreadable; usually fake logos | Static grid of real logos, or none |
| Count-up stat animation | Number is unreadable until it stops; often decorates a fabricated metric | Static number with tabular figures; real value or none |
| Parallax backgrounds | Vestibular trigger; janky on mid-range devices; explains no spatial relation | Flat layers; if depth is the point, a 1-time container transform |
| Tilt / 3D hover cards | Pointer gimmick; no touch equivalent; layout noise | Color or underline hover state |
| Bounce / elastic easing on UI chrome | Toys, not tools; adds 200ms of settling | `standard`, `decelerate`, springs with ratio >= 0.8 |
| Hover scale on every card | Reflow noise; scale > 1.02 blurs text | `translateY(-1px)` + shadow cross-fade, or nothing |
| Content invisible at rest (opacity 0 until JS) | Blank page on slow JS, in reader mode, in reduced motion | Progressive enhancement; animate from visible |
| 500ms+ UI transitions | Feels like lag; blocks the next action | §2 table |
| `transition: all` | Animates layout properties by accident; hard to reason about | Explicit property list |
| Spinners for instant actions | Flicker; lies about latency | Nothing < 300ms; optimistic UI |
| Gradient shimmer on text, animated gradient borders, glow pulses | 2024 "AI product" tell; distracts from content | Static color from `color.md` |
| Auto-rotating hero carousel | Nobody reads slide 2; 2.2.2 pause control required | One hero; tabs if there are truly several |
| Scroll-jacking (hijacked wheel, snap-to-full-screen sections) | Breaks zoom, keyboard, screen readers, reduced motion | Normal scroll; `scroll-snap` only for carousels |
| Confetti on routine actions | Trivialises the action; reserve for once-per-account milestones | One-time success state with a 150ms check draw |

## 11. Review checklist

- [ ] Every animation names one job from §1; unnamed ones are removed
- [ ] At most one entrance choreography per screen; total <= 300ms; nothing animates on scroll except §5 approved cases
- [ ] All content visible and usable with animation disabled and with JS disabled
- [ ] Durations use tokens; micro 80 to 150ms, reveals 200 to 250ms, sheets 300 to 400ms; nothing >= 500ms outside full-screen or hero
- [ ] Exits 20 to 30% shorter than entrances and use `accelerate`
- [ ] Entering elements use `decelerate`; moving elements use `standard`; no `ease-in-out` on UI chrome; no bounce on dialogs, toasts, pages
- [ ] Springs: effects never overshoot; spatial ratio >= 0.7 and only on gesture-driven elements
- [ ] Only `transform` and `opacity` animate; no `transition: all`; no layout properties (check with Paint flashing)
- [ ] `will-change` is scoped and temporary; <= 3 concurrent animated layers on mobile
- [ ] 60fps on a mid-range Android and a 2-generation-old iPhone, measured, not assumed; 120Hz safe
- [ ] Menus and popovers open from their trigger origin (`transform-origin` set)
- [ ] Route and shared-element changes use View Transitions with a no-support fallback and a reduced-motion override
- [ ] `display: none` / popover / dialog entry and exit use `@starting-style` and `allow-discrete`, not JS timers
- [ ] Loading: nothing < 300ms, shape-matched skeleton 300ms to 3 s, real progress > 3 s
- [ ] `prefers-reduced-motion` handled per component (opacity kept, movement removed) and an in-app toggle exists
- [ ] No flashing > 3/s; auto-moving content > 5 s has pause/stop; no auto-rotating carousels
- [ ] Haptics only on discrete user actions, one per action, paired with visible feedback
- [ ] No item from the §10 slop list is present
- [ ] Motion tokens follow `design-tokens.md` naming; no raw `ms` or `cubic-bezier` values in component CSS

## 12. Sources

- Material Design 3, Motion overview and easing/duration tokens: https://m3.material.io/styles/motion/overview
- Material Design 3, Motion physics system (Expressive): https://m3.material.io/styles/motion/overview/how-it-works
- Material Components Android, Motion theming: https://github.com/material-components/material-components-android/blob/master/docs/theming/Motion.md
- Material Design 3, Transition patterns (container transform, shared axis, fade through): https://m3.material.io/styles/motion/transitions/transition-patterns
- Apple HIG, Motion: https://developer.apple.com/design/human-interface-guidelines/motion
- Apple Developer, SwiftUI `Animation.spring(response:dampingFraction:)`: https://developer.apple.com/documentation/swiftui/animation/spring(response:dampingfraction:blendduration:)
- Motion (Framer Motion), Transition and spring options: https://motion.dev/docs/react-transitions
- MDN, View Transition API: https://developer.mozilla.org/en-US/docs/Web/API/View_Transition_API
- MDN, `@starting-style`: https://developer.mozilla.org/en-US/docs/Web/CSS/@starting-style
- MDN, `transition-behavior`: https://developer.mozilla.org/en-US/docs/Web/CSS/transition-behavior
- MDN, CSS scroll-driven animations: https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_scroll-driven_animations
- MDN, `prefers-reduced-motion`: https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion
- web.dev, Animations guide (compositor-only properties): https://web.dev/articles/animations-guide
- web.dev, FLIP technique (Paul Lewis): https://aerotwist.com/blog/flip-your-animations/
- NN/g, Response Times: The 3 Important Limits: https://www.nngroup.com/articles/response-times-3-important-limits/
- NN/g, Animation duration and motion in UX: https://www.nngroup.com/articles/animation-duration/
- W3C WAI, WCAG 2.2 SC 2.2.2 Pause, Stop, Hide and 2.3.1 Three Flashes: https://www.w3.org/WAI/WCAG22/Understanding/
- Design Tokens Community Group, Format Module (duration, cubicBezier, transition): https://www.designtokens.org/tr/drafts/format/
- Maxime Heckel, The physics behind spring animations: https://blog.maximeheckel.com/posts/the-physics-behind-spring-animations/
