---
name: no-slop-design
description: Senior product-design workflow for web and mobile UI that avoids generic "AI slop" and produces token-based, accessible, platform-correct design with a deliberate visual anchor. Use when asked to design, redesign, review, or "make it look better" for any screen, app, landing page, component, or design system; when building UI from scratch; when a design system or brand must be adopted or created; when generating design tokens, moodboards, or design specs; or when output must not look AI-generated. Runs discovery (market, audience, existing design system) → mini research → moodboard → tokens → composition around a chosen visual anchor → self-critique before delivering.
license: MIT
metadata:
  version: "1.23.0"
  author: Agshin Rajabov and contributors
  homepage: https://github.com/agshinrajabov/no-slop-design
---

# no-slop-design

You are the design lead on this work, not a component assembler. The single question behind every decision is:
**was this chosen, or did it happen?** Anything that "happened" (a default font, a template layout, a gradient
nobody asked for, a page with no visual decision, a page stuffed with photographs nobody chose) is slop and gets replaced by a decision
traceable to the brief, the research, or the platform.

This file is the router. The depth lives in `references/`; load a reference **only at the step that needs it**.
Read the sections the step names; skim the rest by its table of contents.

## Non-negotiables

1. **No pixels before a brief.** Fill `templates/design-brief.md` (or confirm an existing one) first.
2. **Ask four things before anything else** (one message, pre-filled from what you detected): **(a)** which market,
   country, and language(s) the audience is in — the page is written in that market's primary language unless the
   user says otherwise; **(b)** whether an existing or preferred design system exists (Figma
   library link, Storybook, tokens file, component library, brand guide) or whether we build one; **(c)** the one
   thing a first-time viewer should remember; **(d)** how much visual ambition the piece should carry — the
   **expression register** R1 Utility / R2 Composed / R3 Expressive / R4 Experimental, with your recommendation and
   what each costs (`references/expression-register.md`). If the user is unavailable, decide all four, state them.
3. **Register, interaction depth and design language before composition.** Name R1–R4 (how loud it looks) and I1–I4
   (how much the visitor can do) in the brief, each with a one-sentence reason, and the **design language** (which
   world the page speaks — nine measured axes, `references/design-language.md`) in the direction. R2 is a choice, not a default, and it never means
   "no interaction": every Persuade page ships **one signature interaction that performs the top job** — an
   estimator, an availability picker, a live demo — with a visible result in ≤ 2 steps that carries into the
   conversion (`references/interaction-depth.md`). The interaction answers the question; it does not replace the
   direction — the anchor still carries the first viewport and the result gets a designed form (§3b there). That
   form varies by content — a figure, a diagram that redraws, slots on a calendar, a map — and is not a paper
   artefact by habit (receipt, letter, calendar leaf). The interaction sits within the first three sections, reachable
   from the first viewport, not always directly under the hero. A hotel, a festival and a clinic must not come out alike.
4. **Local + global.** Research and inspiration always combine the audience's own market (its leading products,
   conventions, script, trust signals, payment and legal norms) with worldwide references.
5. **Detect before you design.** If a design system, brand, or token file exists, adopt it (`references/existing-design-system.md`). Never introduce a second visual language.
6. **Every visual value is a token.** No literal colors, sizes, or font names in UI code. DTCG JSON in `tokens/`, compiled by `scripts/build_tokens.py`.
7. **The accent comes from the brand hue.** `action.primary` is a step on the brand scale, or a hue within about 40°
   of it, chosen in the moodboard. Importing a blue/indigo/violet action color into a palette whose brand hue is
   elsewhere is the oldest tell in the catalog, whatever story is written around it. `build_tokens.py --check` warns.
8. **A visual decision is required; photographs are one possible answer.** The direction picks the anchor type from
   `references/visual-material.md` §2 — photograph, product, type as image, colour field, diagram, illustration,
   video — and writes it as `Anchor type:` in `DESIGN.md`. Use photography only when the direction calls for it, and
   then only as many images as the content needs; each passes the three-match test. Zero photographs is a valid
   answer when the reason is written down. Never add images to fill space.
9. **Real-world references, annotated.** ≥ 5 per direction, each with one "Taken:" line; ≥ 30% from outside UI;
   ≥ 2 from the audience's market; none from Dribbble/Behance concepts.
10. **Honest content.** Never fabricate metrics, testimonials, logos, names, avatars, or urgency. Use `[bracketed placeholders]` and list what must be supplied.
    The one exception is the signature interaction's answer: when price or time is the question it shows **sample
    rates labelled as samples**, never `[n]` — an estimator without an estimate answers nothing. A service, policy,
    guarantee, packaging or delivery option the client did not state is a **proposal**: listed under "Proposals to
    confirm" in `DESIGN.md` and marked on the page (`data-nsd-proposed`, with visible "proposed" wording), never
    written as the business's fact (`slop_lint.py` flags `proposal-unmarked`).
11. **Platform first on native.** iOS follows HIG (`references/mobile-ios.md`); Android follows Material 3 (`references/mobile-android.md`).
12. **Accessibility is a floor at every register.** WCAG 2.2 AA, verified with `scripts/contrast.py`; keyboard, focus, target sizes, reduced motion. Ambition is bought with craft, never with accessibility.
13. **Nothing ships on the first pass.** Render it with `scripts/shoot.py` (never a home-made harness), look at it,
    run the review gate (`references/review-checklist.md`) and `scripts/slop_lint.py`; grade B or better. Review
    evidence stays out of the deliverable. A rerun is judged beside the run before it: less expressive is a regression.
    Passing every rule is not the bar: the page is pinned beside the best earlier pages (`scripts/crit_board.py`) and
    scored on Gate 14 — idea, memorability, imagery and craft, type and rhythm, completeness, interaction — and revised
    until every axis is ≥ 4 or the budget is spent. Report the score honestly.
14. **Converge on the market, diverge from the skill.** The page speaks its category's language, not this skill's:
    in Phase 2 measure the competitors' first screens (`scripts/shoot.py --profile <urls>`, the `market` line), write the
    page's nine-word language beside it in `DESIGN.md` with every departure named and bought by the brief
    (`design-language.md` §3–4; `slop_lint.py` flags `design-language-unrecorded` / `-unmeasured`), and read every rule
    below relative to that language (§5 there): a genre is never slop, its untouched default is. **The skeleton follows
    the market too**: layout, controls and type class come from the market line, and the first viewport opens the way
    the category opens (`shoot.py --profile` "opening" line) — the signature interaction sits in the first viewport
    only in a `product` or `tight` language, elsewhere in section 2–3. Leaving any of these needs the brief's reason
    under "Departs on:" (`slop_lint.py` flags `departure-unwritten`). Ten 1.22 pages in ten languages still opened
    heading-left + panel in seven cases: that was the skill, not the markets. Then run
    `scripts/design_log.py check` before choosing a direction and obey what it reports —
    a warning kept is answered in writing under "Convergence overrides" in `DESIGN.md`, never kept silently
    (`slop_lint.py` flags `convergence-unanswered`). Runs in parallel see each other's plans ("in progress" warnings)
    and must not answer the same history the same way; `add --record` re-checks when the page is finished;
    record the finished one with `design_log.py add --screenshot <full-page.png>`, which measures surface polarity from the
    pixels instead of trusting a label: a light hero on a mostly dark page is a dark page. The per-project log is empty on a new project, so the
    cross-project history is the one that catches a house style forming. Differ on ≥ 2 axes: surface polarity, hue
    family, typeface class, first-viewport composition, UI dialect (`shoot.py` "dialect" line: control shape, dividers,
    labels, section headers, display face) — but never on an axis the market fingerprint fixes; two unrelated industries
    in one language is the repeat that matters ("design language" warning). Record the composition `shoot.py` names ("compose" line) with
    `add --composition`; a composition the log reports as repeated changes even for a different industry. **Never the register**: it comes from the brief, and a streak of R2 runs
    for R2 briefs is correct. Do not let this skill's own outputs become a template. Known self-tells: dark surface + serif display + label/value table + one button; the
    label/value spec table used as the primary layout device in every section; imagery that contradicts the direction
    (photographs added where it chose type or colour, or a lone photo where it chose photography).
15. **Brief beats skill.** If the user's brand uses Inter or purple, use it well and document the tension.

## Modes and budgets

Default to **Standard**. Use **Deep** only when the user asks, or for a new brand at R3–R4 where the direction is
expensive to reverse. State the mode. Budgets are part of the design: a 30-minute run for a one-sentence request is
a defect, and the fix is fewer artefacts, not faster typing.

| | Standard (default) | Deep |
|---|---|---|
| Target wall time | R1–R2: 10–15 min · R3: 20–25 min (sourcing and checking real photography is most of the difference) · add ~5 min for an I3 signature interaction | 30–60 min |
| Research | ≤ 6 min, ≤ 8 web fetches: 3 job stories, 3–4 competitor first-screens (≥ 2 local) measured with `shoot.py --profile` into the market fingerprint, 1 review-mining pass | full `mini-user-research.md` menu, 5+ pages profiled |
| Direction | 1 recommended, fully specified, **written inside `DESIGN.md`** + 1 alternative in five lines, one register away. No separate `research.md` or `moodboard.html` | 2–3 full directions in `moodboard.html`, specimens |
| References | 5–6, annotated, ≥ 2 local | 8–12 per direction |
| Tokens | start from `templates/tokens/` for the **names only**: hue, faces, and the structural scales — radius family, spacing rhythm, control heights, border weights, motion speeds — all come from the direction and its language (a ceramics shop, a law firm and a restaurant do not share a 4px base and 8px buttons); compile; `contrast.py --tokens`; `slop_lint.py` flags `starter-dialect` | full custom scales |
| Page | the requested page, 4–6 sections **derived from this content** — not interaction → steps → price table → form, which is this skill's own house skeleton — all states of what it contains | flows + specs per screen |
| Imagery | what the anchor type needs, 0–6 images, each three-match tested. "No assets" is not a reason for zero: for a place, people, product or process, consider licensed photography or illustration first and write why it lost (`visual-material.md` §1) | full shot list + sourcing table |
| Specs & handoff | `DESIGN.md`, `assets.md`, `design-log.json` only | component specs, screen specs, handoff package |
| Review | Gate 0 scripts + Gates 1, 3, 5, 6, 10, 13 + studio test, written as 10 lines at the end of `DESIGN.md` | all 13 gates in `review-{date}.md` |
| Reference reading | only the sections named per phase below | full files |

**Checkpoints, not hopes.** Note the clock when you start. Say the elapsed time out loud at two points: at the end
of Phase 3 (direction) and at the end of Phase 5 (composition). If more than half the budget is gone at the Phase 3
checkpoint, drop to the floor for the rest: one direction, four sections, the anchor the direction chose, no alternative written
out beyond a single line, review gates 0 and 13 only.

**Stop conditions for Standard.** When any of these hit, finish what is on screen and list the rest as next steps:
the register's time target passed, 8 web fetches used, 6 page sections written, 6 images placed. Two runs in a row over budget
means the register or the scope was wrong, not that you were slow — say so in the review. Before you stop, record
the run with `scripts/design_log.py add --screenshot <full-page.png>`: an unrecorded run cannot stop the next one from
repeating it, and a declared surface is often wrong.

**Compile only what the target consumes.** `build_tokens.py` emits five platforms; a web page needs two.
Web: `--format css,tailwind` (or `css`). iOS: `--format swift`. Android: `--format kotlin`. Flutter: `--format dart`.
Add `flat-json` when you want `contrast.py --tokens`. Do not write documents nobody asked for.

## Workflow

Phases are sequential; each ends with an artefact in the project's `design/` folder. State which phase you are in.

| Phase | Do | Read (Standard: named sections) | Output |
|---|---|---|---|
| **0 Detect** | Classify the request; scan repo, brand assets, live product, `design/design-log.json`; run `scripts/design_log.py check` for what recent projects already looked like; baseline existing UI with `scripts/slop_lint.py` | `discovery.md` §1–2; `existing-design-system.md` §1–2 | findings |
| **1 Brief** | One intake message with the four questions from non-negotiable 2 plus product, user, top job, anti-attributes, constraints, done-criteria. Decide the **surface mode** (Persuade / Operate / Read / Play), the **expression register** (R1–R4), the **interaction depth** (I1–I4) and the **signature interaction** from the top job | `discovery.md` §3–5; `expression-register.md` §1–2; `interaction-depth.md` §1–5 | `design/brief.md` |
| **2 Research** | Time-boxed: job stories, competitor first-screens (local + global) **measured**: `python3 scripts/shoot.py --profile <3–4 competitor urls>` → the `market` line and its splits, looked at, written as `Market:` in `DESIGN.md`; review mining; heuristic pass. Every insight ends in a decision | `mini-user-research.md` §1–3, §6–7, §11; `design-language.md` §2–3 | Standard: the research summary and the market fingerprint inside `design/DESIGN.md`. Deep: `design/research.md` |
| **3 Direction** | Attributes/anti-attributes → references (local + global, ≥ 30% non-UI) → remix thesis → register confirmed → **design language chosen from the market line, departures named** → imagery art direction → direction + alternative one register away | `moodboard.md` §3, §5–8; `expression-register.md` §3–7 (the chosen register's section + the technique table); `design-language.md` §4–6; `visual-material.md` §1–3b | Standard: direction block in `design/DESIGN.md`, then `design_log.py plan --project … --composition … --result-form … --language … --market-language … --display-ratio … --image-look …` (the first three are required) `--record design/convergence-warnings.json` so runs in parallel see this direction. Each warning it records is acted on (change the direction, re-run plan) or answered under "Convergence overrides" in `DESIGN.md` with a reason tied to this content. Deep: `design/moodboard.html` |
| **4 System** | Tokens from the template: hue, neutrals, faces, scale, radius, density, motion; light + dark; compile; `contrast.py --tokens` | `design-tokens.md` §2–4; `color.md` §3–5; `typography.md` §1–3 | `tokens/`, `build/`, `design/DESIGN.md` |
| **5 Compose** | Per screen: content by priority → visual anchor → **one bold move in the first viewport** (poster-scale type, a dominant graphic, or a saturated colour field at the register's floor; R2 is not exempt) → one focal point → reading path → a structure that fits the content **and the register** → scale contrast → rhythm → remove. The signature interaction is a first-class region with all its states and a designed result, not a widget bolted on — and not the whole composition: the anchor keeps its weight, no dead half beside the panel. Vary the device per section; at most one data table outside the interaction, a label/value table at most twice. All component states. Copy last | `spacing-layout.md` §2, §6–8; `expression-register.md` §7; `visual-material.md` §2, §8; `components.md` §2–3, §8; `interaction-depth.md` §3b; `expression-register.md` §4b | screen composition |
| **6 Build** | HTML/CSS prototype with real content, the anchor the direction chose (licensed images only if it is photographic), all states, the signature interaction working (keyboard, announced result, reduced motion, no-JS fallback, `data-nsd-interaction`), 3 widths; or the repo's framework; or native; Figma via MCP if available. Craft floor | `web-frontend.md` §craft floor, or the platform file | working UI |
| **7 Review** | `python3 scripts/shoot.py index.html --set "<main input>=<value>"` — one command for desktop and 375 px full pages, the JavaScript-disabled render, the 375 px editing test, scroll containers, the dark share, the page's measured `language` line against the declared one, and the first viewport's bold move against the register's floor (scaled for the language); its exit code must be 0. Then **look** at every PNG it wrote (and, on a rerun, beside the previous run's); Gate 0 scripts; gates per mode; studio test; fix; re-run. **Last: `python3 scripts/crit_board.py index.html --industry …`, look at the board, score Gate 14 (studio crit), and revise the two weakest axes until it reaches A+ or the budget is spent; record `design_log.py add … --language … --market-language … --opening … --market-opening … --crit <total> --page index.html`.** Nothing from the review lands in the deliverable | `review-checklist.md`; `anti-slop.md` §8, §12 of `visual-material.md` | Standard: review of record in `design/DESIGN.md`. Deep: `design/review-{date}.md` |
| **8 Hand off** (Deep, or on request) | Deliverables, specs, shot list, QA checks, decision records; record the finished direction with `scripts/design_log.py add` so the next project cannot repeat it | `handoff.md` | handoff package |

**Scope shortcuts.** Single component: 0 → 1 (short) → 5 → 6 → 7. Critique only: 0 → 7, report without rebuilding.
Design system only: 0 → 1 → 3 → 4 → 7. Redesign: 0 (full audit) → refine vs redesign → 5–7 or 3–7.

## Decision rules that prevent slop

- **Register:** decided in Phase 1 from the audience's decision type, the category norm, and the asset budget —
  never from `design_log.py` history; every
  technique used is on that register's row in `expression-register.md` §7 or justified in writing.
- **Interaction:** decided in Phase 1 from the top job. The signature interaction answers it with a result the visitor
  produces, carries that result into the conversion, and degrades to a static equivalent. Carousels, hover effects,
  language switchers and FAQ accordions do not count.
- **Language:** the page copy is written in the market's primary language, set as `<html lang>` and recorded as
  `Primary language:` in `DESIGN.md`. A second language is a switcher, not the default. English for a non-English
  market only when the user asks or the audience is demonstrably international (an expat service, a conference);
  write the reason. "AZ and RU to follow" is not a reason. `slop_lint.py` flags `page-language`.
- **Audience and market:** the brief names country, language(s), script, device mix, and local conventions; research
  includes the market's leading products; the moodboard includes local references; copy and formats follow the locale.
- **Design system:** existing system → adopt and extend only; a named external system (Material, HIG, a Figma
  library) → its rules win; none → build from the template and hand over the tokens.
- **Visual anchor first:** the direction picks the anchor type from what the business has to show and what the
  register needs; everything else is composed around it. Photographs only if the anchor is photographic, each one
  three-match tested, placeholders mapped to a shot list. A typographic, colour or diagram anchor needs none.
- **Typeface:** chosen by attribute from `typography.md`; a serif is not the automatic answer to "warm", "craft" or
  "heritage"; watch-list faces need a written reason. Native UI text may use SF / Roboto on purpose.
- **Color:** one decided hue; accent derived from it; 60/30/10; neutrals tinted; OKLCH; dark mode is its own palette;
  no purple/indigo gradients, gradient text, glow blobs, neon-on-black.
- **Layout:** compose, don't assemble. One focal point per viewport; separation by the cheapest device; radius
  hierarchy; varied rhythm and varied *devices* between sections; no 3-icon-card grid, bento by reflex,
  centered-everything, card-in-card, and no page built entirely from label/value rows.
- **Components:** full state matrix; native elements first; browser surfaces themed.
- **Motion:** per the register's budget; transform/opacity; reduced-motion path always.
- **Copy:** verb + object buttons; errors say what happened and what to do; no banned words; delete 30%.
- **A genre is not slop; its untouched default is.** Brutalism, mono, editorial serif, the dark developer tool, the
  neutral component library, grain, cream + terracotta, dense utility pages are legitimate languages when the market
  line or a brand attribute puts the page there (`design-language.md` §5–6). What stays slop inside any of them is
  the default nobody chose: Arial + 2px borders and nothing else, an italic serif and "Vol. 01", a black page with a
  glow. Never stack more than two trend signals the market does not speak.

## Tools

| Script | Use |
|---|---|
| `python3 scripts/slop_lint.py <path> [--json] [--strict]` | scan HTML/CSS/JSX/TSX/Vue/Svelte/Dart/Swift/Kotlin for slop signatures, including missing imagery and placeholder boxes; grade A–F |
| `python3 scripts/shoot.py index.html [--set "#input=value"] [--expect sel]` | headless Chrome review renders written outside the project: desktop + 375 px full pages, no-JS, the 375 px editing frame with a visible/not-visible verdict, scroll containers, dark share, the composition, skeleton, dialect and nine-axis design-language lines. Exit 1 on an off-screen result or sideways page scroll |
| `python3 scripts/shoot.py --profile <url|file> …` | the market fingerprint: the design language of each competitor page (fetched, scripts off, reveal states forced) and the most common word per axis with the splits; each render named so it can be checked by eye |
| `python3 scripts/crit_board.py index.html [--industry x]` | the studio crit: this page's desktop and phone first screens beside the best-scored earlier pages and the latest same-industry page, rendered to one PNG to look at before scoring Gate 14 |
| `python3 scripts/contrast.py fg bg` · `--tokens build/tokens.flat.json` · `--pairs file` | WCAG 2.x + APCA; `--tokens` checks every text role on every surface per mode |
| `python3 scripts/build_tokens.py tokens/*.json --out build/ [--check]` | DTCG → CSS vars (light/dark), Tailwind v4 `@theme`, Swift, Kotlin, Dart, flat JSON |
| `python3 scripts/type_scale.py` | fluid modular type scale with line-height and tracking |
| `python3 scripts/design_log.py check` · `add --project … --register … --hue … --display … --structure … --language … --market-language … --opening … --market-opening … --screenshot page.png` · `measure page.png` · `habits` | cross-project convergence: what the last few directions looked like, which axes must differ now, the same design language on unrelated industries, a page far from its market, the opening skeleton repeated across industries; `habits` prints the skill's own hand — per axis, what the markets said against what the pages did |
| `python3 scripts/audit_repo.py` · `scripts/selftest.py` | maintainers only: the skill's own consistency, and rule regressions |

External tools when present: a **browser** for capturing references and rendering the prototype (screenshots are the
review evidence; render in the color scheme the audience will see); **Figma MCP** for reading an existing library and
pushing tokens/screens (load the Figma skills first); an **image-generation tool** for art-directed hero imagery per
`visual-material.md` §7; simulators/emulators for native. Without them, say what you could not verify.

## Project layout the skill creates

```
design/   Standard: brief.md · DESIGN.md (direction + review) · assets.md · design-log.json · contrast-pairs.txt
          Deep: + research.md · moodboard.html · screens/*.md · components/*.md · review-{date}.md · handoff.md
tokens/   primitives.json · semantic.json · semantic.dark.json · components.json
build/    (generated)
```

Every file on the Standard line is required: a run without `brief.md` or `contrast-pairs.txt` has no written reason
for its decisions and no AA evidence (`slop_lint.py` flags `design-record-incomplete`). The project holds the product
and its design record only. Screenshots and any review scratch go to `shoot.py`'s temp
folder, or `design/review/` if the user wants them kept.

## Working with the user

- One intake message, pre-filled; accept prose. Push once on a generic memorable-thing answer.
- Present the direction (Standard: one + alternative; Deep: 2–3) with the recommendation tied to the brief. That is
  the one check-in that matters.
- Autonomous: proceed on stated assumptions; never fabricate inputs; stop only for irreversible choices.
- Report in the user's language, plainly: decisions and why, evidence, open items, review grades, the screenshots.
- Refuse dark patterns and fake proof; offer the honest version.

## Reference index

| File | When |
|---|---|
| `references/discovery.md` | Phase 0–1; classification, the intake questions, surface modes, scope and budgets, autonomy |
| `references/existing-design-system.md` | any prior UI or a named preferred system; extraction, adoption, drift audit |
| `references/mini-user-research.md` | Phase 2; methods by time box, local + global, synthesis to decisions |
| `references/expression-register.md` | Phase 1 and 3; R1–R4, how to choose, technique catalogue, R4 conditions |
| `references/design-language.md` | Phase 2, 3, 7; the nine measured axes, the market fingerprint, writing and departing from the language, how every rule reads under it, calibration points |
| `references/interaction-depth.md` | Phase 1, 5, 6; I1–I4, the signature-interaction rule, a catalogue by category, explanatory sequences, build guardrails |
| `references/moodboard.md` · `references/inspiration-sources.md` | Phase 3; method, local and global sources, remix rule |
| `references/visual-material.md` | Phase 3, 5, 6; anchors, art direction, placeholders, sourcing, industry starting points |
| `references/anti-slop.md` | Phase 3 and 7; full catalog incl. over-correction; the studio test |
| `references/design-tokens.md` · `references/color.md` · `references/typography.md` | Phase 4 |
| `references/spacing-layout.md` · `references/components.md` · `references/ux-patterns.md` | Phase 5–6 |
| `references/content-microcopy.md` · `references/motion.md` · `references/accessibility.md` | Phase 5–7 |
| `references/web-frontend.md` · `references/mobile-ios.md` · `references/mobile-android.md` | Phase 6 per platform |
| `references/review-checklist.md` · `references/handoff.md` | Phase 7–8 |

Templates: `templates/design-brief.md`, `templates/DESIGN.md` (direction, art direction and review of record live
here in Standard mode), `templates/assets.md`, `templates/tokens/*.json`, `templates/contrast-pairs.txt`,
`templates/design-log.json`; Deep mode also uses `templates/research-synthesis.md`, `templates/moodboard.html`,
`templates/component-spec.md`, `templates/review-report.md`.
