# Design Language

A register says how loud a page is. Interaction depth says how much the visitor can do. Neither says **which
language the page speaks**: two correct R2 pages can be a dark developer tool, a neutral component library, an
illustrated payments site, a Swiss editorial page, a brutalist portfolio or a GOV.UK service. This skill spent
twenty-one versions making pages differ from each other on surface, hue, composition and dialect, and its user
still saw one studio's work across ten industries, because every page was pulled toward one language — the
composed, tinted, one-anchor, one-bold-move school every rule in this skill was written in. Differing from your own
history is not the same as fitting the world the business lives in.

The fix is not a menu of styles. A menu becomes the next template. The fix is to **measure the market's language
on fixed axes and converge on it**, then diverge from it only where the brief says so and only by the amount the
brief buys.

## Contents

1. The principle: converge on the market, diverge from the skill
2. The nine axes and their vocabulary
3. Measuring the market fingerprint
4. Writing the language into the direction
5. How the skill's rules read under a language
6. Calibration points (not a menu)
7. What stays slop in every language
8. Checks

---

## 1. The principle: converge on the market, diverge from the skill

- The page's language comes from **the category's own pages** — the competitors the visitor has just looked at and
  the category's global leaders — not from this skill's taste and not from the last project. A dev tool speaks dev
  tool, a family-law firm speaks family law, and each one's slop is the *untouched default of its own language*, not
  the language itself.
- `design_log.py` still stops the skill repeating itself, but a repeat is now judged by language: two unrelated
  industries in the same language is the warning; two ceramics shops in the same language is expected.
- Departures are bought by the brief. "Stand out in a saturated category" buys one or two axes, named, with the
  reason. Four or more departures put the page in another category's language, which is how a bakery ends up
  looking like a foundation model's launch page.
- Nothing here is a taste judgement. Every word on the profile is a measurement from `shoot.py` or, when a page
  cannot be fetched, a judgement by eye written in the same words.

## 2. The nine axes and their vocabulary

The profile is nine words joined by `;`, in this order. Only these words. `?` for an axis that could not be
measured. `shoot.py` prints it as the `language` line; `design_log.py` refuses anything else.

| # | Axis | Words | Measured as |
|---|---|---|---|
| 1 | **surface** | light · dark · mixed | dark share of the first two viewports' pixels (≤ 35% light, ≥ 60% dark) |
| 2 | **chroma** | achromatic · low · saturated | share of pixels carrying colour (saturation ≥ 0.25): < 5% · < 30% · ≥ 30% |
| 3 | **type** | grotesk · humanist · serif · slab · mono · condensed · system | the largest heading's family |
| 4 | **density** | tight · medium · airy | share of the first two viewports covered by lines of text: ≥ 16% · ≥ 7% · below |
| 5 | **radius** | square · soft · round · pill | median control radius: < 3 · ≤ 10 · ≤ 24 · larger |
| 6 | **imagery** | none · product · photo · illustration · type · 3d | the largest non-text element in the first two viewports (`product` when the page declares a product anchor; a competitor's screenshot reads as `photo`) |
| 7 | **layout** | centered · left · asymmetric · grid | where the first viewport's largest heading sits, or a ≥ 3-column grid owning the viewport |
| 8 | **motion** | none · functional · choreographed · scene | transitions only · keyframes or reveal-on-scroll · canvas, WebGL, GSAP/ScrollTrigger, Lenis, Rive |
| 9 | **controls** | hairline · solid · raw | the main button: transparent with a thin border · filled · 2px+ border with no radius or a hard offset shadow |

The five-word `dialect` line (control shape, dividers, labels, section headers, display face) stays: it is the
finer fingerprint of the components. The language is the coarser one that says which world the page belongs to.

## 3. Measuring the market fingerprint

In Phase 2, with the competitor first screens already open:

```
python3 scripts/shoot.py --profile https://local-competitor.az https://second-local.az https://global-leader.com https://second-global.com
```

- Three to five pages: at least two from the audience's own market, at least one global category leader. Not
  Dribbble, not a template gallery: pages the visitor could actually land on.
- The `market` line is the most common word per axis; the `split` lines show where the category disagrees. A split
  axis is a free choice; a unanimous axis is the category's language and needs a reason to leave.
- A fetched page runs without its scripts, with reveal states forced visible, so a hydration error or a
  reveal-on-scroll does not measure as a blank page. **Look at the PNG it names** for each page; if the render is
  wrong (a menu left open, a hero missing), open that page in the browser and write its profile by eye with the same
  nine words. A page that cannot be fetched at all (a 403, a bot wall) is judged by eye the same way.
- Write the result in `DESIGN.md` as `Market: <profile> — from n pages: <urls>` (or `… by eye: <urls>`). `slop_lint.py`
  looks for that line.

Budget: about 15–20 seconds per page. Four pages fit inside the Standard research box.

## 4. Writing the language into the direction

In `DESIGN.md` §1, after the direction sentence:

```
**Design language** (`design-language.md`): light;low;serif;airy;square;photo;left;functional;hairline
Market: light;low;serif;medium;soft;photo;left;functional;solid — from 4 pages: <url> <url> <url> <url>
Departs on: density (airy — the brief says "unhurried"; the three local firms are dense and look like directories);
controls (hairline — one action per section, the photograph carries the weight). Nearest calibration point: §6 "quiet
editorial".
```

Rules:

- The language is chosen **before** tokens (Phase 3, with the direction) and **measured after** the build
  (`shoot.py index.html` prints the page's actual profile). If the measured line differs from the declared one, either
  the page or the declaration is wrong; record the measured one with `design_log.py add --language` and say which.
- Every departure names the axis, the word, and the brief's reason. "To be different" is not a reason; the
  convergence log handles difference.
- `data-nsd-design-language="…"` on `<html>` or `<body>` is the same declaration for a page without a design folder.
- Register `plan --language … --market-language …` in Phase 3 so runs in parallel and the history see it.

## 5. How the skill's rules read under a language

The skill's rules were written in one language. Under another they are read as follows; `slop_lint.py` applies the
mechanical part when a valid `Design language:` line exists.

| Rule | Reads as |
|---|---|
| The bold move (`expression-register.md` §4b) | Still owed. For `imagery: product` or `density: tight` the floors scale by two thirds: a developer tool owns its first screen with the interface at a quarter of the viewport, documentation with the search and the first answer — not with a poster |
| The anchor (`visual-material.md` §2) | Chosen inside the language: a `product` language anchors on the interface, an `illustration` language on the system, a `type` language on the words |
| The signature interaction (`interaction-depth.md` §3) | Still owed on every Persuade page; its *form* follows the language — a playground in a dev tool, a live search in documentation, the scene itself in a `scene` language, a picker beside the photograph in a hospitality page |
| Accent from the brand hue (non-negotiable 7) | Unchanged, but `chroma: achromatic` languages carry the brand in one accent on neutral surfaces, and that accent is still the brand's hue |
| Tinted neutrals, 60/30/10 (`color.md`) | `achromatic` languages tint less (chroma 0.002–0.006) and may split 80/15/5; still no untinted grey next to a tinted one |
| "Centred everything", three-column grids, bento (`anti-slop.md` §3) | Native in `layout: centered` and `grid` languages and in `imagery: product` pages; not flagged there. What is still flagged: the three-icon-card row with a testimonial strip, the 2×2 bento by reflex on a page whose content is not four unequal facts |
| The ledger site, tables as sections | Native in `density: tight` languages (documentation, utilities, GOV.UK-style services); not flagged there |
| System type (`anti-slop.md` §2) | A decision in `type: system` languages (brutalist, some editorial, some utilities) when the market line shows it; still flagged as the reflex default elsewhere |
| Uniform large radius | A decision in `radius: pill` languages (playful consumer, some fintech) |
| Dashed borders, hard shadows, 2px rules | Native in `controls: raw` languages (brutalist, zine, some agency portfolios) |
| Reveal-on-scroll on every section | Expected in `choreographed` and `scene` languages; still needs the no-JS fallback |
| Dark by default | A category norm in developer tools, cinema, music, gaming; `surface: dark` in the market line is the reason. Dark for "tech feeling" on a bakery is still slop |
| Over-correction slop (`anti-slop.md` §8) | Every genre in that table is a legitimate language when the market line or a brand attribute puts the page there. What §8 catches is the genre's *untouched default*: the brutalist page that is only 2px borders and Arial, the editorial page that is only an italic serif and "Vol. 01", the dev-tool page that is only a black background and a glow |
| The starter dialect, untouched theme values, the reflex typeface, purple gradients, glow blobs, fake proof | **Unchanged in every language.** These are defaults nobody chose, whatever the language |

## 6. Calibration points (not a menu)

Six well-known points in the nine-axis space, so a profile can be read and a market line recognised. They are
here to calibrate the eye, **never to pick from**: a page's language comes from its measured market, and
`design_log.py` warns when one of these is repeated across unrelated industries.

| Point | Profile | Native to | Its untouched default (the slop) | Its crafted version |
|---|---|---|---|---|
| Developer tool, dark | dark;achromatic;grotesk;medium;soft;product;centered;choreographed;hairline | dev tools, infrastructure, AI products | black background, one glow, Inter, a terminal screenshot, "Ship faster" | a real interface at scale, one accent from the brand, type with a voice, a working playground |
| Component library / neutral SaaS | light;achromatic;grotesk;medium;round;product;grid;functional;solid | B2B software, design systems, productivity | untouched shadcn theme, Geist, a bento of feature cards | regenerated palette, one product screenshot the content needs, grids only where the content is a set |
| Illustrated fintech | light;low;grotesk;tight;soft;3d;grid;scene;hairline | payments, banking infrastructure, insurance | a stock 3D coin, gradient mesh, "Financial infrastructure for the internet" | an illustration system that explains the product, diagrams that redraw with the visitor's inputs |
| Quiet editorial | light;low;serif;airy;square;photo;left;functional;hairline | law, architecture, publishing, heritage, luxury | Instrument Serif italic, thin rules, "Vol. 01", one cream page | a serif chosen for the reading length, real photography of the place and people, a measure that reads |
| Neo-brutalist | light;saturated;system;medium;square;type;asymmetric;functional;raw | zines, agency portfolios, culture, counter-positioned brands | Arial + 2px borders + hot pink + a marquee | type as image with a real point of view, a grid that breaks for a reason, raw controls that still meet AA |
| Public service utility | light;low;grotesk;tight;square;none;left;none;solid | government, transit, health information, utilities | a blue header and a wall of links | a task-first first screen, one search that answers, tables that reflow, a page that works without JavaScript |

Other languages exist by the thousand — luxury hospitality (mixed;low;serif;airy;square;photo;asymmetric;
choreographed;hairline), playful consumer (light;saturated;humanist;medium;pill;illustration;centered;
choreographed;solid), immersive launch (dark;saturated;condensed;airy;square;3d;asymmetric;scene;hairline), a
Shopify-style catalogue, a Japanese minimal shop, a maximalist music page. Do not look them up here; measure them.

## 7. What stays slop in every language

Chosen-by-nobody is the test, and the language does not change it:

- untouched theme or template values (`shadcn-default-theme`, `starter-dialect`, the Tailwind default primary)
- the reflex typeface with no brand line (Inter, Roboto, Poppins, Space Grotesk …) — a `system` or `grotesk` language
  still chooses its face on purpose and writes why
- purple/indigo gradients, gradient text, glow blobs, neon on black, sparkles and rocket icons
- fabricated proof: metrics, logos, testimonials, avatars, urgency
- a page that fails AA, keyboard, reduced motion or the no-JS render, whatever the language's motion word
- the language chosen from taste: a `Design language:` line with no `Market:` evidence (`design-language-unmeasured`)
- the same language on unrelated industries in a row (`design_log.py`: "design language")

## 8. Checks

- [ ] `Market:` line in `DESIGN.md` from `shoot.py --profile` (or by eye) with ≥ 3 pages, ≥ 2 local
- [ ] `Design language:` line with nine vocabulary words, written in Phase 3 before tokens
- [ ] every departure from the market line names the axis, the word and the brief's reason; ≤ 3 departures
- [ ] the built page's measured `language` line matches the declared one, or the difference is explained and the
      measured one recorded
- [ ] `design_log.py plan … --language … --market-language …` in Phase 3; `add --language` in Phase 7
- [ ] no "design language" or "market fit" warning left unanswered under "Convergence overrides"
- [ ] §7 holds: nothing on the page is the language's untouched default
