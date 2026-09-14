# Changelog

## 1.7.0 — 2026-09-14

The 1.6 rerun of the translation brief delivered what 1.6 asked for — a working estimator as the hero, graded A− — and
exposed four gaps the skill could not see.

- **Surface polarity was self-reported.** The run was logged as "light" because its hero was ochre; measured from a
  full-page screenshot, 84% of the page was dark, so the dark streak had never broken. Token-based measurement would
  not have caught it either (`surface.base` was light; the dark sections used `surface.inverse`). `design_log.py` now
  reads PNG screenshots with the standard library: `add --screenshot page.png` records the measured polarity and
  corrects a contradicting label, and `measure page.png` prints the dark share.
- **The result left the screen on phones.** On 375 px the price sat 1.4 screens below the inputs, with no sticky bar.
  `interaction-depth.md` now defines the mobile requirement as a test (change the main input; the new result is
  visible without scrolling), the review gate runs it, and `slop_lint.py` adds `interaction-result-offscreen` (LOW)
  when the page declares an interaction but has no sticky, fixed or dialog result.
- **Unchecked radios looked checked** on an ochre band inside a dark `color-scheme`. `components.md` craft floor and
  the review gate now cover native controls on a surface of the other polarity.
- **A price column was clipped** at 375 px, and a colour band ended mid-control on desktop. New narrow-table rule and
  two layout checks.
- Also: "honest deltas" (an option that changes nothing says so) and prices in the market's locale; selftest and eval 05
  extended.

## 1.6.0 — 2026-09-14

The 1.5 test page (a translation agency) earned a B+ and was still a brochure: one load-time stagger, a language
toggle, a contact form. The register table coupled interaction to visual ambition, so any business correctly placed
at R2 was also capped at "standard components + one custom affordance". For services, what sells is the visitor
answering their own question — price, date, availability — with a result they produced.

- New `references/interaction-depth.md`: I1 Static, I2 Functional, I3 Demonstrative, I4 Immersive, independent of
  the register; the rule that every Persuade page ships one signature interaction that performs the top job; a
  catalogue of conversion interactions for sixteen categories; explanatory scroll sequences; build guardrails
  (declared with `data-nsd-interaction`, native controls, announced results, reduced motion, no-JS equivalent).
- `SKILL.md`: non-negotiable 3 covers both axes; Phase 1 decides interaction depth and the signature interaction;
  Phases 5–6 build and verify it; budgets add ~5 minutes for I3; every run ends with `design_log.py add`.
- `expression-register.md`: interaction is a separate axis; R2 may use one explanatory sequence; the signature
  interaction is required at every register.
- `slop_lint.py`: `no-signature-interaction` (LOW) when nothing outside the contact form produces an announced
  result. The 1.5 translation page now receives it.
- `design_log.py`: surface polarity warns after two runs in a row instead of three; runs can record interaction depth.
- Review gate, anti-slop (the brochure page), ux-patterns, the brief / DESIGN.md / log templates, `audit_repo.py`,
  and a new `evals/05-signature-interaction.md` built from the B+ page.

## 1.5.0 — 2026-09-14

In real use the skill reached for photographs whether the design needed them or not. The cause was ours: fixing the
text-only pages in 1.1 had turned into a quota.

- The Standard budget said "3–6 photographs", the fallback floor said "three photographs", and agents read both as
  minimums. The budget now says "what the anchor type needs, 0–6 images; photographs only if the anchor is
  photographic".
- The linter only recognised `<img>`, `<picture>`, `<video>` and large SVG as a visual anchor, so the cheapest way to
  pass `no-imagery` and `thin-imagery` was to add photographs. The rules now read the direction's decision
  (`Anchor type:` in `DESIGN.md`, or `data-nsd-anchor` on the page): a typographic, colour-field or diagram anchor
  needs no photographs, `thin-imagery` only fires when the direction chose photography, and an undecided text-only
  page is still flagged.
- New rules: `images-contradict-direction` (photographs on a page whose direction chose type or colour) and
  `photo-stuffing` (an image in nearly every section).
- Non-negotiable 8 is now "a visual decision is required; photographs are one possible answer". Matching changes in
  `visual-material.md`, `expression-register.md`, `anti-slop.md`, the review gate and the `DESIGN.md` template.

## 1.4.0 — 2026-09-03

Three field tests of the paths that had never been run — an existing design system, an iOS screen, and eval 04 on
a weaker model — found three defects in the tools and one in the guidance.

- `build_tokens.py`: OKLCH colours were silently dropped from the Swift, Kotlin and Dart output. `color.md` tells
  authors to work in OKLCH, so the recommended input produced native token files with the colours missing and no
  error. `to_hex()` now resolves hex, `oklch()`, `rgb()` and DTCG colour objects, dark variants included.
- `slop_lint.py`: page-level imagery rules judged component source. A `.tsx` page that composes `<Panel>` has no
  `<img>` of its own and was graded C for it; those rules now read rendered documents only.
- `slop_lint.py`: new `marquee` rule. The catalog has banned the auto-scrolling marquee since 1.0, but nothing
  checked for it, and the weaker model shipped one for tour dates with a thematic justification.
  `expression-register.md` now marks it off-row at every register and names the rationalisation pattern.
- `slop_lint.py`: grades count distinct (rule, file) pairs. One choice repeated over six lines of CSS is one choice,
  not six, and should not turn a B into an F.
- Budgets are register-aware: 10–15 minutes at R1–R2, 20–25 at R3, where sourcing and checking real photography is
  most of the cost. Three runs in a row overran a flat 15-minute target, which made the target wrong, not the runs.

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
