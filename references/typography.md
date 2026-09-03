# Typography

Typography is 80% of what makes a UI read as designed. It is also where generated UI fails first: the reflex font,
the flat scale, the tracked uppercase eyebrow. Every typographic decision here must trace back to an attribute in
the brief.

## 1. Selecting typefaces

**Method:** attributes → construction → candidates → test in situ → pick one display voice and one text workhorse.

| Brand attribute | Construction that carries it | Open-source candidates (2026) |
|---|---|---|
| Precise, engineered, calm | Neo-grotesque / Swiss, tight apertures, low contrast | Schibsted Grotesk · Hanken Grotesk · Switzer · Funnel Sans · Geist (dev-tool contexts only, now a mild tell) |
| Friendly, human, approachable | Humanist sans, open apertures, slight stroke modulation | Source Sans 3 · Nunito Sans · Atkinson Hyperlegible Next · Mona Sans · Figtree |
| Warm, crafted, artisanal | Soft serif / "wonky" serif, variable optical size | Fraunces · Newsreader · Literata · Gelasio |
| Editorial, authoritative, heritage | Transitional/old-style text serif + tight display | Newsreader · Source Serif 4 · Libre Caslon · Playfair (display only, tired) · Instrument Serif (display only, saturated) |
| Bold, contemporary, cultural | Wide/expressive grotesque with width axis | Bricolage Grotesque · Unbounded · Archivo (wide cuts) · Anybody |
| Luxury, quiet confidence | High-contrast didone or refined sans with generous spacing | Bodoni Moda · Cormorant (display only) · Cabinet Grotesk · General Sans |
| Technical, data-dense, honest | Mono for data + neutral sans for UI | JetBrains Mono · Commit Mono · Geist Mono · IBM Plex Mono · Fragment Mono |
| Playful, young | Rounded or geometric with personality | Sora (tired) · Outfit (tired) · Fredoka (careful) · Gabarito · Bricolage at heavy weights |
| Institutional, civic, trustworthy | Public-sector humanist sans | Public Sans · IBM Plex Sans · Inter (only here, and only deliberately) |
| Multi-script (Arabic, Cyrillic, Devanagari, CJK) | Superfamily with matched scripts | Noto family (pick the specific script cut) · IBM Plex (Arabic, Devanagari, Thai, JP, KR) · Vazirmatn (FA/AR) · Readex Pro (AR) · Cairo (AR) · Amiri (AR text) |

**Watch list (converging into slop):** Inter, Roboto, Poppins, Montserrat, Open Sans, Lato, Space Grotesk, Plus
Jakarta Sans, Sora, Outfit, DM Sans, Manrope, Geist, Satoshi + General Sans, Instrument Serif italic accents.
Not banned; they need a written reason.

**Platform exception:** native iOS (SF Pro / SF Compact / New York) and Android (Roboto / Roboto Flex /
Google Sans) system faces are correct defaults for *native app UI* because they carry Dynamic Type, optical sizes,
and OS conventions. A brand face can be used for display/marketing surfaces inside the app; body UI text should
usually stay system unless the brand face ships proper size-class scaling.

**Sources:** Google Fonts (check version and axes), Fontshare (ITF, free commercial), Fontsource (self-host), Velvetyne,
Collletttivo, The League of Moveable Type, Uncut.wtf. Verify licence for embedding in apps (some OFL builds forbid
renaming, not use).

## 2. Pairing

- One **display voice** (headlines, hero, numerals) + one **text workhorse** (UI, body). A third face only for
  code/data (mono). Never four.
- Contrast in **construction** (serif × grotesque; wide × narrow; high-contrast × mono-linear), but harmony in
  **x-height and proportions** — set both at 16px and compare the lowercase.
- Same family at two optical sizes or widths (Fraunces 9pt/144pt; Newsreader Display/Text; Bricolage width axis) is
  the safest sophisticated pairing.
- Hierarchy comes from size, weight, and space **before** it comes from a second family.
- Avoid the 2025 formula "grotesque body + italic serif accent word". If you want a serif, commit to it for headlines.

## 3. Scale

Modular ratios: 1.125 (major second — dense apps), 1.2 (minor third — product UI), 1.25 (major third — general web),
1.333 (perfect fourth — marketing/editorial), 1.5–1.618 (dramatic display). **Below 1.2 the hierarchy disappears;
above 1.5 you need few steps.**

Fluid scale (Utopia method): define min viewport/base/ratio and max viewport/base/ratio; each step becomes
`clamp(min, intercept + slope·vw, max)`. Generate with `python3 scripts/type_scale.py --min-base 16 --max-base 18
--min-ratio 1.2 --max-ratio 1.25`. Keep min/max in `rem` so browser text zoom still works (WCAG 1.4.4, 200%).

Typical role set:

| Role | Size (min→max) | LH | Tracking | Weight | Notes |
|---|---|---|---|---|---|
| display | 40→72px | 1.0–1.05 | −0.02 to −0.03em | display face | one per page, `text-wrap: balance` |
| h1 | 32→44 | 1.1 | −0.02em | | |
| h2 | 24→32 | 1.2 | −0.01em | | |
| h3 | 20→24 | 1.25 | −0.01em | | |
| h4 / lead | 18→20 | 1.4 | 0 | | |
| body | 16→18 | 1.5–1.65 | 0 | 400 | ≥ 16px always on web |
| body-sm | 14→15 | 1.5 | 0 | | metadata, tables |
| label | 13→14 | 1.3 | 0 | 500 | buttons, form labels |
| caption | 12 | 1.35 | +0.01em | | floor; never smaller for functional text |
| code | 13→14 | 1.55 | 0 | mono | `font-variant-ligatures: none` in code editors if ligatures confuse |

Mobile floors: iOS body 17pt (Dynamic Type "Large"), caption 11–12pt; Android body 14–16sp, label 11–12sp. Always
support Dynamic Type / font scaling up to at least 200% without clipping.

## 4. Setting text well (the details that read as craft)

- **Measure:** 45–75 characters per line; 60–70 ideal. Set `max-width: 65ch` on prose containers.
- **Line-height:** longer measure → taller line-height. Body 1.5–1.65; headings tighten as they grow.
- **Tracking:** display slightly negative; body 0; small caps / uppercase labels +0.04–0.08em; **never** track lowercase body.
- **Weights:** two clearly distinct weights minimum (e.g. 400 + 600). Avoid 500-only "all medium" UIs. Load only weights you use.
- **Rag & wrap:** `text-wrap: balance` on headings (≤ 4 lines), `text-wrap: pretty` on paragraphs; `hyphens: auto` for narrow columns with `lang` set.
- **Numerals:** `font-variant-numeric: tabular-nums` in tables, timers, prices, dashboards; proportional in prose. Old-style figures in editorial prose if the face has them.
- **Punctuation:** curly quotes “ ” ‘ ’, real ellipsis …, en dash for ranges (9–5), em dash sparingly (UI copy: almost never), non-breaking spaces before units and after short words.
- **Widows/orphans:** headlines should not end in a single short word; adjust copy or `balance`.
- **Case:** sentence case for UI (buttons, labels, headings) unless the brand system says otherwise. Title Case reads American-corporate; ALL CAPS only for tiny labels with tracking.
- **Alignment:** left-aligned for anything longer than two lines. Never justify on the web. Centered only for short display moments.
- **Vertical rhythm:** spacing between heading and its paragraph < spacing between paragraph and next heading (heading belongs to what follows).
- **Optical alignment:** hang punctuation and bullets in editorial contexts; align icon optical centre, not bounding box, with text x-height.
- **Rendering:** `-webkit-font-smoothing: antialiased` only on dark backgrounds with light text; otherwise leave default. `font-display: swap` with `size-adjust` fallback metrics to avoid layout shift; preload the one display file used above the fold.
- **Variable fonts:** ship one file, use `font-variation-settings` for opsz/wdth; set `font-optical-sizing: auto`.
- **Multilingual:** define a fallback chain per script; check line-height for Arabic/Devanagari (need 1.7–1.9); mirror tracking rules per script; test with the longest translation (German, Finnish) and shortest (Chinese).

## 5. Tokens

```json
{
  "font": {
    "family": { "$type": "fontFamily",
      "display": { "$value": ["Bricolage Grotesque", "system-ui", "sans-serif"] },
      "text":    { "$value": ["Schibsted Grotesk", "system-ui", "sans-serif"] },
      "mono":    { "$value": ["Commit Mono", "ui-monospace", "monospace"] } },
    "weight": { "$type": "fontWeight", "regular": { "$value": 400 }, "medium": { "$value": 500 }, "semibold": { "$value": 600 } }
  },
  "typography": { "$type": "typography",
    "body": { "$value": { "fontFamily": "{font.family.text}", "fontSize": "clamp(1rem, 0.9565rem + 0.2174vw, 1.125rem)",
                          "fontWeight": "{font.weight.regular}", "lineHeight": 1.55, "letterSpacing": "0" } }
  }
}
```

Composite `typography` tokens keep role definitions in one place; `build_tokens.py` expands them into
`--typography-body-size/-lh/-weight/-family/-tracking`.

## 6. Review questions

1. Can you name the attribute each typeface serves?
2. Squint: is there a clear three-level hierarchy without reading?
3. Is any lowercase text tracked? Any body under 16px? Any measure over 75ch?
4. Are quotes, ellipses, and dashes real characters?
5. Is the display face used more than once per viewport? (It shouldn't be.)
6. Would this typography survive a rebrand of the color palette? (Good type systems do.)
