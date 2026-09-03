# Color

Build palettes as **systems**, in **OKLCH**, from **one decided hue**, with **semantic roles** on top. Never ship a
primitive (`blue-600`) into UI code; ship a role (`action.primary`).

## Contents

1. Decide before generating
2. Why OKLCH
3. Building a scale
4. Semantic roles (the layer UI code uses)
5. Contrast: comply with WCAG 2.2, design with APCA
6. Practical recipes
7. Gradients, if the brand earns them
8. Token shape (DTCG)
9. Anti-patterns

---

## 1. Decide before generating

From the moodboard: the dominant hue (one), its temperature, the neutral tint, the chroma ceiling (muted vs. rich),
light-first or dark-first, and the emotional register (calm / energetic / serious / warm). Write them down. A
palette generated without these is a Tailwind palette with extra steps.

**60 / 30 / 10.** Sixty percent of any screen is neutral surface, thirty percent is secondary surface/text, ten
percent is accent. Extend hues with tints and shades, never with new hues. Three hue families maximum (neutral,
brand, one accent) plus fixed status hues.

## 2. Why OKLCH

`oklch(L C H)`: L = perceived lightness 0–1, C = chroma 0–~0.4, H = hue 0–360. Equal L looks equally bright across
hues (HSL lies about this: HSL yellow at 50% is far lighter than HSL blue at 50%). Consequences:

- Scales built by sweeping L at fixed H produce steps that *feel* even.
- Multi-hue palettes at equal L and C carry equal visual weight (charts, tags, avatars).
- Gradients in `oklch` interpolation don't pass through muddy gray.
- Browser support is universal in 2026; provide hex fallbacks only for email.

## 3. Building a scale

Use 11–12 steps. Radix's semantics are the best default for *what each step is for*:

| Step | Use | Light L (typ.) | Dark L (typ.) |
|---|---|---|---|
| 1 | app background | 0.99 | 0.19 |
| 2 | subtle background, cards | 0.975 | 0.22 |
| 3 | UI element background (normal) | 0.95 | 0.25 |
| 4 | UI element hover | 0.92 | 0.28 |
| 5 | UI element active / selected | 0.89 | 0.31 |
| 6 | subtle border, separators | 0.85 | 0.35 |
| 7 | interactive element border | 0.79 | 0.40 |
| 8 | strong border, focus ring (≥ 3:1 vs step 1) | 0.64 | 0.50 |
| 9 | solid fill (buttons, badges) — purest chroma | brand L | brand L +0.05 |
| 10 | solid hover | 9 −0.04 | 9 +0.04 |
| 11 | low-contrast text (≥ Lc 60 on step 2) | 0.45 | 0.80 |
| 12 | high-contrast text (≥ Lc 90 on step 2) | 0.22 | 0.94 |

**Chroma curve:** chroma must fall toward both ends of the scale or the extremes clip and look "radioactive".
A workable curve is `C(L) = Cmax · sin(π · L)` clamped so that steps 1–2 sit at C ≤ 0.02 and step 9 carries the
brand's full chroma. Muted brands: Cmax ≈ 0.10–0.16. Rich brands: 0.20–0.26. Check every value stays in sRGB gamut
(or declare P3 with fallbacks).

**Hue drift:** small deliberate drift (±3–8°) across the scale reads as crafted. Warm hues shift toward yellow as
they lighten; cool hues toward cyan. Don't drift more than that or steps stop matching.

**Neutrals are never gray.** Tint the neutral scale toward the brand hue at C ≈ 0.004–0.012. Warm brand → warm
neutrals; cool brand → cool neutrals. Never mix.

**Dark mode is a separate palette, not an inversion.** Build dark steps independently (dark surfaces increase
perceived chroma, so accents need C −15–25%). Elevation in dark mode is a lightness step up (+0.03–0.04 L per
level), not a shadow. Base surface L ≈ 0.18–0.24 (≈ #121212–#1e1e1e), never `#000`. Body text L ≈ 0.90–0.93, never `#fff`.

## 4. Semantic roles (the layer UI code uses)

Minimum viable role set. Each role has a light and a dark value; each is a token aliasing a primitive step.

```
surface.base · surface.raised · surface.sunken · surface.overlay · surface.inverse
text.primary · text.secondary · text.tertiary · text.disabled · text.on-action · text.on-inverse · text.link · text.link-visited
border.subtle · border.strong · border.focus
action.primary · action.primary-hover · action.primary-pressed · action.secondary(-hover/-pressed) · action.destructive(…)
status.success / warning / danger / info — each with .fill · .surface · .text · .border
selection · focus · scrim · skeleton
```

Rules:
- A semantic token aliases a **primitive**, never another semantic (max chain depth 2; component tokens may alias semantics).
- Status hues are hue-locked (success ≈ 145°, warning ≈ 80°, danger ≈ 25°, info ≈ 245° in OKLCH) but their L and C
  are matched to the brand scale so they don't look pasted in.
- Never encode meaning in color alone: pair with icon, label, or pattern (8% of men are red-green deficient).
- Link color must differ from body text by more than color (underline) in running text; visited must differ from unvisited.

## 5. Contrast: comply with WCAG 2.2, design with APCA

Both, always. WCAG 2.x is the legal baseline; APCA models perceived contrast better (especially dark mode and thin
type) but WCAG 3 has not adopted a final algorithm and is years away.

| Element | WCAG 2.2 AA | APCA target (design tool) |
|---|---|---|
| Body text (16px/400) | ≥ 4.5:1 | Lc ≥ 75 (90 preferred for long reading) |
| Large text (≥ 24px, or ≥ 18.66px bold) | ≥ 3:1 | Lc ≥ 60 |
| Headlines ≥ 36px or 24px bold | ≥ 3:1 | Lc ≥ 45 |
| Secondary / metadata text | ≥ 4.5:1 (still text) | Lc ≥ 60 |
| Placeholder / disabled | exempt but keep legible | Lc ≥ 30 |
| UI component boundaries, icons, focus rings vs adjacent | ≥ 3:1 | Lc ≥ 30–45 |
| Non-text minimum visibility | — | Lc ≥ 15 |

Verify with `python3 scripts/contrast.py --tokens build/tokens.flat.json` (checks every text role on every surface, per mode), `contrast.py fg bg --size 16 --weight 400`, or a pairs file. Test **every** text role on
**every** surface role it can legally appear on, in both modes. Put the pairs list in the repo
(`design/contrast-pairs.txt`) so it runs in CI.

Common failures: gray-500 secondary text on white (≈ 4.6:1 — passes barely, feels weak, fails on off-white
surfaces); white on brand step 9 when the brand is yellow/orange/light green (use step 11/12 as text on light
fills instead); tinted text on tinted surfaces in dark mode.

## 6. Practical recipes

**From a single brand hex to a system:**
1. Convert to OKLCH; note L, C, H.
2. Decide chroma ceiling (is the brand louder or quieter than this swatch?).
3. Generate 12 steps with the L table above and the chroma curve; place the brand at step 9 (adjust L to 0.55–0.65 for a usable solid).
4. Build neutrals at the same H with C 0.006.
5. Build status scales at locked hues with the same curve.
6. Assign semantic roles; run contrast pairs; fix by moving L, not by adding hues.
7. Repeat for dark with its own L table.

**Charts / data:** categorical palettes at equal L (≈ 0.65 light / 0.75 dark) and equal C, hues spaced ≥ 40°
apart, max 6–7 categories, then switch encoding.

**Dark-mode button text:** the dark-mode brand fill is usually lighter (step 7–8) so white text fails; use a near-black `text.on-action` in dark mode. Check, don't assume.

**Brand color that fails as a button fill (yellow, lime, pastel):** use it as identity (large surfaces, marks,
illustration) and choose a darker step (11) or a near-black for action fills. Don't force accessibility onto a hue
that can't carry it.

**Color-scheme meta:** set `color-scheme: light dark` on `:root` when both modes exist so native form controls and
scrollbars follow.

## 7. Gradients, if the brand earns them

- Interpolate in `oklch` or `oklab`: `linear-gradient(in oklch, var(--a), var(--b))`.
- Keep ΔL small (≤ 0.15) or ΔH small (≤ 30°); large both ways = the AI look.
- One gradient per screen, on one surface, never on text, never behind text you need to read.
- Mesh/blob gradients are almost always filler. Ask what content the space wanted.

## 8. Token shape (DTCG)

```json
{
  "color": {
    "$type": "color",
    "neutral": { "1": { "$value": "oklch(0.99 0.004 70)" }, "12": { "$value": "oklch(0.22 0.012 70)" } },
    "brand":   { "9": { "$value": "oklch(0.58 0.17 40)" } },
    "text":    { "primary": { "$value": "{color.neutral.12}" } },
    "action":  { "primary": { "$value": "{color.brand.9}" } }
  }
}
```

Dark values live in `semantic.dark.json` overriding the same paths. `scripts/build_tokens.py` emits both.

## 9. Anti-patterns (see anti-slop.md §1)

Purple/indigo gradient · gradient text · glow blobs · pure black + neon · Tailwind blue-600 as brand · untouched
shadcn HSL values · five pastel accents with no dominant · cream+terracotta by reflex · mixed neutral temperatures ·
gray text on color · color-only status · dark mode by inversion.
