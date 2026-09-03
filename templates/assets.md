# Assets — {Project}

Every image, video, font and icon the design uses, where it came from, and what has to replace it before launch.
Written during Phase 5–6; handed to the client with the prototype. See `references/visual-material.md`.

## Art direction (from the direction block in `DESIGN.md`)

| Dimension | Decision |
|---|---|
| Anchor type | {full-bleed photograph · product-first · type as image · colour field · illustration · video · scene} |
| Subject | {the actual place / people / product / process — name them} |
| People | {none · hands only · candid at work · portraits} |
| Light | {morning side light · overcast · studio · golden hour} — one light across the set |
| Treatment | {natural · muted −15% · warm grade toward hue {h} · black and white} — one treatment across the set |
| Crop & framing | {…}; leave negative space where type sits |
| Ratios | hero {3:2} · portrait {4:5} · detail {1:1} · video {16:9} |
| Banned | {stock clichés for this category, listed} |

## Photographs used in the prototype

Placeholders until the client's own shoot. Each one passed the three-match test (`visual-material.md` §3b) and was
opened and looked at, not just linked.

| # | Where used | Subject | Source (URL) | Photographer / licence | Three-match note (subject · light · material) |
|---|---|---|---|---|---|
| P1 | hero | | | Unsplash License | |
| P2 | | | | | |
| P3 | | | | | |

## Shot list for the real shoot

What the client should photograph, in priority order. Ratios and framing match the slots above so the swap is a
file replacement, not a redesign.

| # | Shot | Framing / ratio | Light | Replaces | Notes |
|---|---|---|---|---|---|
| S1 | | | | P1 | |
| S2 | | | | P2 | |
| S3 | | | | — | future use |

## Video / motion

| Clip | Where | Length | Poster frame | Source | Reduced-motion behaviour |
|---|---|---|---|---|---|
| | | ≤ 12 s, muted, loop | | | poster only |

## Illustration, icons, graphic devices

| Item | Style / system | Source or author | Licence | Notes |
|---|---|---|---|---|
| icon set | {family, stroke, sizes 16/20/24} | | | `currentColor`, `aria-hidden` when decorative |
| graphic device | {the recurring motif} | | | drawn from {reference} |

## Typefaces

| Role | Family | Weights / axes loaded | Source | Licence | Self-hosted? | Subset |
|---|---|---|---|---|---|---|
| Display | | | | | | |
| Text | | | | | | |
| Mono | | | | | | |

Production: self-host, subset to the scripts in use, `font-display: swap` with `size-adjust` fallback metrics,
preload the one file used above the fold.

## Logo and brand marks

| Asset | Format | Where it lives | Clear space | Minimum size | Notes |
|---|---|---|---|---|---|
| wordmark | SVG | | | | |
| favicon set | SVG + 180/192/512 PNG | | — | — | plus `theme-color` |

## Must be supplied by the client before launch

Everything the design shows as `[bracketed placeholder]` or licensed stand-in:

- [ ] {Real photographs per the shot list}
- [ ] {Prices, hours, address, phone, legal entity}
- [ ] {Names, titles, testimonials with permission}
- [ ] {Logo files, brand fonts if licensed}
- [ ] {Analytics / booking / payment endpoints}

Nothing on this list was invented. If a number, name or logo appears in the prototype, it is either supplied by the
client or clearly bracketed.
