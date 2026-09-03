# {Product} Design System — DESIGN.md

> The single source of truth for how {Product} looks, feels, and behaves. Lives at the repo root (or `/design`).
> Any agent or human designing for {Product} loads this first. If something is not decided here, decide it here
> before using it in a screen. Raw values live in `tokens/*.json` (DTCG); this document explains **why**.

## 0. Status

| Field | Value |
|---|---|
| Version | 0.1.0 |
| Owner | |
| Last reviewed | {date} |
| Applies to | {web app · marketing · iOS · Android · Flutter} |
| Token source | `tokens/primitives.json`, `tokens/semantic.json`, `tokens/semantic.dark.json`, `tokens/components.json` |
| Build | `python3 scripts/build_tokens.py tokens/*.json --out build/` |

## 1. Foundations of intent

**The memorable thing:** {one sentence}

**Attributes / anti-attributes:**

| We are | We are not | Visual consequence |
|---|---|---|
| | | |
| | | |
| | | |

**Moodboard:** `design/moodboard.html` — Direction {A/B/C} "{name}" approved on {date}. Reference set: {n} references, each annotated with what was taken.

**Design principles (max 5, each with a tie-breaker rule):**
1. *{Principle}* — when in conflict with {other}, {this} wins because {…}.
2. …

## 2. Color

**Model:** OKLCH primitives → semantic roles → component tokens. Never use a primitive in UI code.

### Primitive scales
| Scale | Hue (°) | Steps | Notes |
|---|---|---|---|
| neutral | {e.g. 70 (warm)} | 0–1000 in 50s | tinted toward brand hue, chroma {0.004–0.012} |
| brand | | | |
| accent | | | |
| status: success / warning / danger / info | | | hue-locked, chroma matched to brand |

### Semantic roles (light · dark)
| Role | Light | Dark | Use |
|---|---|---|---|
| `surface.base` | | | page background |
| `surface.raised` | | | cards that are interactive, sheets |
| `surface.sunken` | | | wells, inputs on raised |
| `surface.overlay` | | | menus, popovers |
| `text.primary` | | | |
| `text.secondary` | | | |
| `text.tertiary` | | | metadata; still ≥ 4.5:1 |
| `text.on-action` | | | |
| `text.link` | | | visited differs |
| `border.subtle` / `border.strong` | | | |
| `action.primary` / `-hover` / `-pressed` | | | |
| `focus` | | | 3:1 vs adjacent, 2px ring |
| `status.*` + `status.*-surface` + `status.*-text` | | | |

**Dark mode rules:** elevation by lightness step (not shadow), text off-white `{L≈0.93}`, accent chroma −10–20%, no pure black, images dimmed 10%.

**Contrast policy:** WCAG 2.2 AA everywhere; APCA Lc ≥ 75 body, ≥ 60 secondary, ≥ 45 large/UI. Verified with `scripts/contrast.py --pairs design/contrast-pairs.txt`.

## 3. Typography

| Role | Family | Why this face (one sentence, tied to attributes) | Weights loaded |
|---|---|---|---|
| Display | | | |
| Text / UI | | | |
| Mono (if any) | | | |

**Scale:** {ratio min→max}, fluid via `clamp()` (`scripts/type_scale.py --min-base … --max-base …`).

| Token | Size (min→max) | Line-height | Tracking | Use |
|---|---|---|---|---|
| `text.display` | | 1.0–1.05 | −0.03em | hero, one per page |
| `text.h1` … `text.h4` | | | | |
| `text.body-lg` / `text.body` / `text.body-sm` | | 1.5–1.6 | 0 | |
| `text.label` / `text.caption` | | 1.3–1.4 | 0 / +0.01em | ≥ 12px |

**Rules:** measure 45–75ch; `text-wrap: balance` on headings, `pretty` on paragraphs; `tabular-nums` for numbers; real quotes and ellipsis; never letter-space lowercase; never fake bold/italic.

**Script coverage:** {Latin ext · Cyrillic · Arabic · …} — fallback chain per script: {…}

## 4. Spacing, sizing, layout

- Base unit **4px**; scale `space.0–space.24` = 0, 2, 4, 6, 8, 12, 16, 20, 24, 32, 40, 48, 64, 80, 96, 128.
- Density modes: {comfortable (default) · compact} — how they map.
- Layout grid: {12-col, gutter `space.6`, margin `space.6`→`space.12`}; max content width {…}; reading width {65–72ch}.
- Breakpoints: {360 · 600 · 905 · 1240 · 1440} (content-driven, name them by layout change, not device).
- Radius hierarchy: `radius.none 0 · radius.control 6 · radius.card 12 · radius.sheet 20 · radius.pill 999` — nested inner = outer − padding.
- Elevation: `shadow.raised` / `shadow.overlay` / `shadow.modal` — {light: shadow; dark: lightness step}.
- Control heights: 32 / 40 / 48; icon sizes 16 / 20 / 24; touch targets ≥ 44 (iOS) / 48 (Android).

## 5. Motion

| Token | Value | Use |
|---|---|---|
| `duration.instant` | 80ms | press feedback |
| `duration.fast` | 120–150ms | hover, toggles |
| `duration.base` | 200–250ms | reveal, menus |
| `duration.slow` | 300–400ms | sheets, page-level |
| `ease.standard` | cubic-bezier(0.2, 0, 0, 1) | most things |
| `ease.decelerate` | cubic-bezier(0, 0, 0, 1) | entering |
| `ease.accelerate` | cubic-bezier(0.3, 0, 1, 1) | exiting |

Motion principles: {2–3 signature moments named here}; everything else is functional. `prefers-reduced-motion` → {what remains}.

## 6. Iconography & imagery

- Icon set: {name, stroke weight, optical sizes}; custom icons follow {grid}. Never emoji as icons.
- Illustration / photo direction: {style, color treatment, subjects, what's banned}.
- Empty states, error states: {illustration or typographic? decide once}.

## 7. Components (index)

| Component | Spec | Status |
|---|---|---|
| Button | `components/button.md` | ✅ |
| Input / Select / Checkbox / Radio / Switch | | |
| Card (only when the card IS the interaction) | | |
| Navigation (top / side / tab bar) | | |
| Table / List / Data row | | |
| Dialog / Sheet / Popover / Toast | | |
| Empty state / Error state / Skeleton | | |

## 8. Voice & microcopy

Tone in three words: {…}. Sentence case. Verb-first buttons. Errors say what happened + what to do. See `references/content-microcopy.md` banned list; project-specific bans: {…}

## 9. Platform notes

- **Web:** CSS custom properties from `build/tokens.css`; Tailwind v4 `@theme` from `build/theme.css`; `color-scheme` set; focus rings; `env(safe-area-inset-*)`.
- **iOS:** SF Pro / SF Rounded unless brand face has Dynamic Type sizing; 44pt targets; native navigation; materials only where HIG intends.
- **Android:** Material 3 shape/type scales mapped from tokens; 48dp targets; predictive back; dynamic color {on/off}.

## 10. Never list (project-specific slop)

- {e.g. no gradient buttons}
- {e.g. no icon-in-circle feature rows}
- …

## 11. Changelog

| Version | Date | Change |
|---|---|---|
| 0.1.0 | | initial |
