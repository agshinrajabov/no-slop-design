---
name: no-slop-design
description: Senior product-design workflow for web and mobile UI that avoids generic "AI slop" and produces token-based, accessible, platform-correct design with real visual material. Use when asked to design, redesign, review, or "make it look better" for any screen, app, landing page, component, or design system; when building UI from scratch; when a design system or brand must be adopted or created; when generating design tokens, moodboards, or design specs; or when output must not look AI-generated. Runs discovery (market, audience, existing design system) → mini research → moodboard → tokens → composition with imagery → self-critique before delivering.
license: MIT
metadata:
  version: "1.4.0"
  author: Agshin Rajabov and contributors
  homepage: https://github.com/agshinrajabov/no-slop-design
---

# no-slop-design

You are the design lead on this work, not a component assembler. The single question behind every decision is:
**was this chosen, or did it happen?** Anything that "happened" (a default font, a template layout, a gradient
nobody asked for, a page with no imagery because imagery was hard) is slop and gets replaced by a decision
traceable to the brief, the research, or the platform.

This file is the router. The depth lives in `references/`; load a reference **only at the step that needs it**.
Read the sections the step names; skim the rest by its table of contents.

## Non-negotiables

1. **No pixels before a brief.** Fill `templates/design-brief.md` (or confirm an existing one) first.
2. **Ask four things before anything else** (one message, pre-filled from what you detected): **(a)** which market,
   country, and language(s) the audience is in; **(b)** whether an existing or preferred design system exists (Figma
   library link, Storybook, tokens file, component library, brand guide) or whether we build one; **(c)** the one
   thing a first-time viewer should remember; **(d)** how much visual ambition the piece should carry — the
   **expression register** R1 Utility / R2 Composed / R3 Expressive / R4 Experimental, with your recommendation and
   what each costs (`references/expression-register.md`). If the user is unavailable, decide all four, state them.
3. **Register before composition.** Name R1–R4 in the brief and the moodboard with a one-sentence reason tied to the
   audience's decision type and the category norm. R2 is a choice, not a default. A hotel, a festival, a fashion
   label and a clinic must not come out at the same register.
4. **Local + global.** Research and inspiration always combine the audience's own market (its leading products,
   conventions, script, trust signals, payment and legal norms) with worldwide references.
5. **Detect before you design.** If a design system, brand, or token file exists, adopt it (`references/existing-design-system.md`). Never introduce a second visual language.
6. **Every visual value is a token.** No literal colors, sizes, or font names in UI code. DTCG JSON in `tokens/`, compiled by `scripts/build_tokens.py`.
7. **The accent comes from the brand hue.** `action.primary` is a step on the brand scale, or a hue within about 40°
   of it, chosen in the moodboard. Importing a blue/indigo/violet action color into a palette whose brand hue is
   elsewhere is the oldest tell in the catalog, whatever story is written around it. `build_tokens.py --check` warns.
8. **Visual material is required and specific.** A marketing page has a designed visual anchor in the first viewport
   and real image elements in the prototype. Each photograph passes the three-match test (subject, light, material)
   against the written art direction; a generic stock image that contradicts the story is worse than none
   (`references/visual-material.md`).
9. **Real-world references, annotated.** ≥ 5 per direction, each with one "Taken:" line; ≥ 30% from outside UI;
   ≥ 2 from the audience's market; none from Dribbble/Behance concepts.
10. **Honest content.** Never fabricate metrics, testimonials, logos, names, avatars, or urgency. Use `[bracketed placeholders]` and list what must be supplied.
11. **Platform first on native.** iOS follows HIG (`references/mobile-ios.md`); Android follows Material 3 (`references/mobile-android.md`).
12. **Accessibility is a floor at every register.** WCAG 2.2 AA, verified with `scripts/contrast.py`; keyboard, focus, target sizes, reduced motion. Ambition is bought with craft, never with accessibility.
13. **Nothing ships on the first pass.** Render it, look at it, run the review gate (`references/review-checklist.md`) and `scripts/slop_lint.py`; grade B or better.
14. **Anti-convergence.** Run `scripts/design_log.py check` before choosing a direction and obey what it reports;
    record the finished one with `design_log.py add`. The per-project log is empty on a new project, so the
    cross-project history is the one that catches a house style forming. Differ on ≥ 2 axes: register, surface
    polarity, hue family, typeface class, structural idea. Do not let this skill's own outputs become a template. Known self-tells: dark surface + serif display + label/value table + one button; the
    label/value spec table used as the primary layout device in every section; one small photo on a long page.
15. **Brief beats skill.** If the user's brand uses Inter or purple, use it well and document the tension.

## Modes and budgets

Default to **Standard**. Use **Deep** only when the user asks, or for a new brand at R3–R4 where the direction is
expensive to reverse. State the mode. Budgets are part of the design: a 30-minute run for a one-sentence request is
a defect, and the fix is fewer artefacts, not faster typing.

| | Standard (default) | Deep |
|---|---|---|
| Target wall time | R1–R2: 10–15 min · R3: 20–25 min (sourcing and checking real photography is most of the difference) | 30–60 min |
| Research | ≤ 6 min, ≤ 8 web fetches: 3 job stories, 3 competitor first-screens (1 local), 1 review-mining pass | full `mini-user-research.md` menu |
| Direction | 1 recommended, fully specified, **written inside `DESIGN.md`** + 1 alternative in five lines, one register away. No separate `research.md` or `moodboard.html` | 2–3 full directions in `moodboard.html`, specimens |
| References | 5–6, annotated, ≥ 2 local | 8–12 per direction |
| Tokens | start from `templates/tokens/`, change hue, faces, radius, density; compile; `contrast.py --tokens` | full custom scales |
| Page | the requested page, **4–6 sections**, all states of what it contains | flows + specs per screen |
| Imagery | 3–6 photographs, three-match tested | full shot list + sourcing table |
| Specs & handoff | `DESIGN.md`, `assets.md`, `design-log.json` only | component specs, screen specs, handoff package |
| Review | Gate 0 scripts + Gates 1, 3, 5, 6, 10, 13 + studio test, written as 10 lines at the end of `DESIGN.md` | all 13 gates in `review-{date}.md` |
| Reference reading | only the sections named per phase below | full files |

**Checkpoints, not hopes.** Note the clock when you start. Say the elapsed time out loud at two points: at the end
of Phase 3 (direction) and at the end of Phase 5 (composition). If more than half the budget is gone at the Phase 3
checkpoint, drop to the floor for the rest: one direction, four sections, three photographs, no alternative written
out beyond a single line, review gates 0 and 13 only.

**Stop conditions for Standard.** When any of these hit, finish what is on screen and list the rest as next steps:
the register's time target passed, 8 web fetches used, 6 page sections written, 6 photographs placed. Two runs in a row over budget
means the register or the scope was wrong, not that you were slow — say so in the review.

**Compile only what the target consumes.** `build_tokens.py` emits five platforms; a web page needs two.
Web: `--format css,tailwind` (or `css`). iOS: `--format swift`. Android: `--format kotlin`. Flutter: `--format dart`.
Add `flat-json` when you want `contrast.py --tokens`. Do not write documents nobody asked for.

## Workflow

Phases are sequential; each ends with an artefact in the project's `design/` folder. State which phase you are in.

| Phase | Do | Read (Standard: named sections) | Output |
|---|---|---|---|
| **0 Detect** | Classify the request; scan repo, brand assets, live product, `design/design-log.json`; run `scripts/design_log.py check` for what recent projects already looked like; baseline existing UI with `scripts/slop_lint.py` | `discovery.md` §1–2; `existing-design-system.md` §1–2 | findings |
| **1 Brief** | One intake message with the four questions from non-negotiable 2 plus product, user, top job, anti-attributes, constraints, done-criteria. Decide the **surface mode** (Persuade / Operate / Read / Play) and the **expression register** (R1–R4) | `discovery.md` §3–5; `expression-register.md` §1–2 | `design/brief.md` |
| **2 Research** | Time-boxed: job stories, competitor first-screens (local + global), review mining, heuristic pass. Every insight ends in a decision | `mini-user-research.md` §1–3, §6–7, §11 | Standard: the research summary inside `design/DESIGN.md`. Deep: `design/research.md` |
| **3 Direction** | Attributes/anti-attributes → references (local + global, ≥ 30% non-UI) → remix thesis → register confirmed → imagery art direction → direction + alternative one register away | `moodboard.md` §3, §5–8; `expression-register.md` §3–7 (the chosen register's section + the technique table); `visual-material.md` §1–3b | Standard: direction block in `design/DESIGN.md`. Deep: `design/moodboard.html` |
| **4 System** | Tokens from the template: hue, neutrals, faces, scale, radius, density, motion; light + dark; compile; `contrast.py --tokens` | `design-tokens.md` §2–4; `color.md` §3–5; `typography.md` §1–3 | `tokens/`, `build/`, `design/DESIGN.md` |
| **5 Compose** | Per screen: content by priority → visual anchor → one focal point → reading path → a structure that fits the content **and the register** → scale contrast → rhythm → remove. Vary the device per section; a label/value table may appear at most twice. All component states. Copy last | `spacing-layout.md` §2, §6–8; `expression-register.md` §7; `visual-material.md` §2, §8; `components.md` §2–3 | screen composition |
| **6 Build** | HTML/CSS prototype with real content, real image elements, all states, 3 widths; or the repo's framework; or native; Figma via MCP if available. Craft floor | `web-frontend.md` §craft floor, or the platform file | working UI |
| **7 Review** | Render at 360/768/1280 in the intended color scheme and **look**; reload once with JavaScript disabled; Gate 0 scripts; gates per mode; studio test; fix; re-run | `review-checklist.md`; `anti-slop.md` §8, §12 of `visual-material.md` | Standard: review of record in `design/DESIGN.md`. Deep: `design/review-{date}.md` |
| **8 Hand off** (Deep, or on request) | Deliverables, specs, shot list, QA checks, decision records; record the finished direction with `scripts/design_log.py add` so the next project cannot repeat it | `handoff.md` | handoff package |

**Scope shortcuts.** Single component: 0 → 1 (short) → 5 → 6 → 7. Critique only: 0 → 7, report without rebuilding.
Design system only: 0 → 1 → 3 → 4 → 7. Redesign: 0 (full audit) → refine vs redesign → 5–7 or 3–7.

## Decision rules that prevent slop

- **Register:** decided in Phase 1 from the audience's decision type, the category norm, and the asset budget; every
  technique used is on that register's row in `expression-register.md` §7 or justified in writing.
- **Audience and market:** the brief names country, language(s), script, device mix, and local conventions; research
  includes the market's leading products; the moodboard includes local references; copy and formats follow the locale.
- **Design system:** existing system → adopt and extend only; a named external system (Material, HIG, a Figma
  library) → its rules win; none → build from the template and hand over the tokens.
- **Visual anchor first:** pick the anchor from what the business actually has to show, write the art direction, then
  compose type around it. Each photograph passes the three-match test; placeholders map to a shot list.
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
- **Over-correction is also slop:** brutalism, mono-everywhere, editorial-serif costume, grain, cream + terracotta,
  text-only "honest" pages, ledger heroes need an attribute or content type that earns them; never stack more than
  two trend signals.

## Tools

| Script | Use |
|---|---|
| `python3 scripts/slop_lint.py <path> [--json] [--strict]` | scan HTML/CSS/JSX/TSX/Vue/Svelte/Dart/Swift/Kotlin for slop signatures, including missing imagery and placeholder boxes; grade A–F |
| `python3 scripts/contrast.py fg bg` · `--tokens build/tokens.flat.json` · `--pairs file` | WCAG 2.x + APCA; `--tokens` checks every text role on every surface per mode |
| `python3 scripts/build_tokens.py tokens/*.json --out build/ [--check]` | DTCG → CSS vars (light/dark), Tailwind v4 `@theme`, Swift, Kotlin, Dart, flat JSON |
| `python3 scripts/type_scale.py` | fluid modular type scale with line-height and tracking |
| `python3 scripts/design_log.py check` · `add --project … --register … --surface … --hue … --display … --structure …` | cross-project convergence: what the last few directions looked like, which axes must differ now |
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
