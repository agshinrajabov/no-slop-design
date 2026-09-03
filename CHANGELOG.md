# Changelog

## 1.3.0 — 2026-09-03

- `reveal-no-fallback` (HIGH, cross-file) in `slop_lint.py`: scroll-reveal styles that set `opacity: 0` with no
  `js`-class gate and no `<noscript>` reset leave the page blank when the script fails. Found by rendering the 1.2
  test page with scripting disabled.
- `motion.md` §7b with the two accepted fixes; review gate now includes a JavaScript-disabled pass.
- Template gaps closed: `DESIGN.md` carries the register, the direction and reference table, the imagery art
  direction, the alternative one register away, and the review of record (Standard mode writes no separate files);
  `design-log.json` records register, anchor type, art direction and previous registers; new `templates/assets.md`
  (art direction, photograph provenance with three-match notes, shot list, fonts, client to-supply list).
- README and SKILL.md corrected where they still described the pre-1.2 artefact set.

## 1.2.0 — 2026-09-03

- `references/expression-register.md`: R1 Utility / R2 Composed / R3 Expressive / R4 Experimental, how to choose
  from the audience's decision type and the category norm, a technique catalogue per register, the five conditions
  for R4, guardrails that never move, and register slop in both directions.
- Intake asks for the register with its cost; brief, moodboard, log and review gate all record and check it.
- `visual-material.md` §3b: the three-match test (subject, light, material) for choosing a specific photograph, plus
  "look at the image before you ship it".
- `build_tokens.py --check`: palette sanity check (accent hue vs brand hue, the blue/indigo band, untinted
  neutrals). Fixed `.tokens.json` being misread as a mode file.
- `slop_lint.py`: `ledger-site` and `thin-imagery` rules, with fixtures.
- Standard mode tightened to 10–15 minutes, 4–6 sections, direction and review written inside `DESIGN.md`, with
  explicit stop conditions.

## 1.1.0 — 2026-09-03

- `references/visual-material.md`: a designed visual anchor is required on Persuade surfaces, art direction is
  written before composition, prototypes carry real image elements, placeholders map to a shot list.
- Intake asks for market/country/language and for an existing or preferred design system; research and moodboard
  require local references alongside global ones.
- Standard and Deep modes with budgets.
- `slop_lint.py`: `no-imagery`, `ledger-hero`, `placeholder-box`.

## 1.0.0 — 2026-09-03

Initial release.

- `SKILL.md` router with 9 phases, non-negotiables, decision rules, and reference index.
- 19 references: discovery, existing design systems, mini user research, moodboard, inspiration sources, anti-slop catalog (incl. over-correction), design tokens (DTCG), color (OKLCH, APCA + WCAG), typography, spacing/layout/composition, components (state matrix, craft floor), UX patterns, content/microcopy, motion, accessibility (WCAG 2.2), web frontend (Tailwind v4, modern CSS), iOS (HIG, Liquid Glass), Android (Material 3 Expressive), review checklist (13 gates), handoff.
- Templates: brief, research synthesis, moodboard.html, DESIGN.md, DTCG token starter set (light + dark), contrast pairs, design log, component spec, review report.
- Scripts: `slop_lint.py`, `contrast.py` (WCAG + APCA, `--tokens` mode), `build_tokens.py` (CSS, Tailwind v4, Swift, Kotlin, Dart), `type_scale.py`.
- Evals: three scenarios with rubrics and a slop fixture.
