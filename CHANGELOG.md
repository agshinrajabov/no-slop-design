# Changelog

## 1.10.0 — 2026-09-14

The 1.9.0 run was correct on every rule — Azerbaijani, R2 argued from the brief, a working estimator — and its first
viewport was forgettable: a 70 px headline, a thin route line, a row of form fields. R2 had been read as "nothing
loud", when it means "one loud thing".

- **The bold move** (`expression-register.md` §4b): every Persuade first viewport above R1 carries one — type at
  poster scale (R2: display ≥ 6× body; R3–R4: 8×), a drawn graphic (≥ 30% of the 1280×800 viewport; 45%), or a
  saturated colour field with type on it (≥ 40% with type ≥ 3×; 60%). Dark and near-white bands are surfaces, icons
  are not graphics, and the move must be the direction's idea. Composition step, review gate, catalog tell and
  eval 05 item 23.
- **`shoot.py` measures it** in the first viewport, reads the register from `design/DESIGN.md` (or `--register`),
  and fails the review when no measure reaches the floor. Calibrated against the four translation runs, it agrees
  with the side-by-side judgement: 1.6 passes on its amber field (92%), 1.8.0 on 195 px type (13.9×), 1.7.1 (4.4×,
  a dark band) and 1.9.0 (5×, no graphic or field) fail. Colour is read through a canvas so OKLCH tokens and
  one-colour gradients count.

## 1.9.1 — 2026-09-14

The 1.9.0 rerun (Azerbaijani, R2 from the brief, a route diagram as the anchor, 11 minutes, lint A) reported its page
as 79% dark. It is 20% dark. Headless Chrome follows the operating system's colour scheme, the machine was in dark
mode, and every page in these tests ships a `prefers-color-scheme: dark` palette.

- **Correction to 1.7.0.** The finding that the 1.6 page was "logged as light while 84% of its pixels were dark" came
  from the same artefact: rendered in the light scheme its audience sees by default, that page is 8% dark. The agent's
  "light" label was right. Measuring polarity from pixels is still correct; the example was not. README amended.
- **`shoot.py --scheme light|dark`** (default light) pins `prefers-color-scheme` on every render, prints it, and puts
  dark renders in their own folder. The machine's own mode is never used.
- **The editing test missed a mobile dock** that repeats the result with `aria-hidden` (correctly, to avoid a double
  announcement) instead of being a live region. When no live region is on screen, the test now accepts visible text the
  edit changed that repeats a number from the result, and says so. Verdicts across the four runs: 1.6 not visible,
  1.7.1, 1.8.0 and 1.9.0 visible.

## 1.9.0 — 2026-09-14

The 1.8.0 rerun of the translation brief was the best of the three — a raspberry colour field with the headline
stitched and sealed, a drawn bundle as the estimator's result, 14 minutes, lint A — and it made two decisions the
brief did not support.

- **It wrote the page in English for a Baku agency**, with Azerbaijani and Russian "to follow". The page is now written
  in the market's primary language by default: intake question (a), a `Primary language:` field in the brief and
  `DESIGN.md`, a localization rule to design with the real strings (Azerbaijani, Russian and German headlines run
  20–35% longer), a review gate item, a tell, and `slop_lint.py` `page-language` (MED) when `<html lang>` is missing
  or differs from the declared primary language.
- **It raised the register to R3 because the last three runs were R2.** `design_log.py check` counted the register as
  an axis to break, so history was deciding ambition. The register is now reported as a note ("keep the register the
  brief calls for") and removed from the axes to vary; `SKILL.md`, the review gate and the catalog say the same.
- Selftest covers both; eval 05 gains rubric items 21–22.

## 1.8.1 — 2026-09-14

- `shoot.py` reported "result not visible" on the 1.8.0 test page while its sticky bar showed the new price. It looked
  for results only inside `[data-nsd-interaction]`, and the bar was a sibling. It now watches every `output` and
  `aria-live` region on the page and counts the ones the edit changed; if nothing changed it says so. Verdicts on
  the three translation runs: 1.6 not visible, 1.7.1 visible, 1.8.0 visible.

## 1.8.0 — 2026-09-14

The 1.7.1 rerun of the translation brief passed what 1.7 asked for — the result stayed visible while editing at
375 px, prices used the market's locale, surface polarity was measured — and was a step back as a design. Screenshots
side by side with 1.6 showed what the checks could not: the bold colour field and the drawn route of working days
were gone, replaced by a dark form panel, a large heading, an empty half of the first viewport and two data tables.
The run also took 24 minutes, a third of it spent building its own screenshot harness, which it left in the
deliverable.

- **New `scripts/shoot.py`.** One command renders desktop and 375 px full pages and a JavaScript-disabled page with
  headless Chrome, runs the 375 px editing test (`--set "#pages=12"`: set the inputs, keep the edited control on
  screen, report whether the result is visible), lists every horizontal scroll container, and prints the dark share
  for `design_log.py`. It writes to a temp folder and refuses to write into the deliverable. Exit 1 on an
  off-screen result or a page that scrolls sideways. On the 1.6 page it reports the result not visible; on 1.7.1,
  visible — the verdicts the manual reviews reached.
- **The interaction does not replace the direction** (`interaction-depth.md` §3b): the anchor keeps full weight in
  the first viewport, the result gets a designed form, no dead half beside the panel, one data table outside the
  interaction, and a rerun is compared with the run before it. New gate items, a new over-correction tell, and
  `slop_lint.py` `tables-as-sections` (MED), which ignores tables drawn inside the interaction and Operate surfaces.
- **Tables that scroll without a cue.** The 1.7.1 steps table was 8 px wider than its container at 375 px, so the
  last column simply looked missing. `components.md` gives a CSS-only edge cue; `slop_lint.py` adds
  `table-scroll-no-cue` (LOW) unless the page has scroll shadows, a mask or a narrow reflow.
- **Review scaffolding.** `slop_lint.py` adds `review-scaffolding` (MED) for wrapper pages that only frame a local
  page and for `shots/`-style folders beside it. `SKILL.md` and the checklist say review evidence is not product.
- **`neon-on-black` false positive.** It fired on `--color-black: #000000`, a primitive in a compiled token file;
  it now requires a background context.
- Selftest covers every change; eval 05 gains rubric items 17–20.

## 1.7.1 — 2026-09-14

- `interaction-result-offscreen` gave the 1.6 page a pass because its CSS contained a `position: fixed` dock. The dock
  was `hidden` by default and only appeared after the result had scrolled past, so it never showed while the visitor
  was editing — the exact failure the rule exists for. The rule now ignores sticky headers and elements hidden by
  default, and the 1.6 page is flagged. Mobile guidance and the review gate name the pattern.

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
