# Eval 01 — New product landing page (full path, Persuade mode)

## Prompt

> We're launching Ledgerly, an invoicing tool for freelance translators and interpreters in Europe. They bill in
> several currencies, chase late payers, and hate accounting software. Design the landing page. There's no brand yet
> except the name. Stack is Next.js with Tailwind v4. I'm not available for questions for the next few hours; make
> sensible decisions and tell me what you assumed.

## Expected behaviour

Phases 0–7 in order, autonomous mode (assumptions stated), one check-in artefact (the moodboard with a recommended
direction), then a built prototype and a review report.

## Rubric (0 / 1 / 2 each)

**Brief & research**
1. Wrote `design/brief.md` with a specific memorable thing (not "clean, modern") and contestable attributes/anti-attributes.
2. Stated assumptions explicitly with risks; did not ask a questionnaire.
3. Wrote job stories for translators (multi-currency billing, chasing late payers, avoiding accounting jargon) with evidence type labelled (assumption vs source).
4. Competitor teardown of 3+ real invoicing tools (named), with category clichés identified and one deliberate departure argued.
5. Every insight in `design/research.md` ends in a design decision and a place it appears.

**Moodboard**
6. 2–3 named directions, differing on ≥ 2 axes, each with a thesis sentence, type pairing with reasons, OKLCH palette, radius/density/motion posture, and a "not this" list.
7. ≥ 5 references per direction, each with a "Taken:" line; ≥ 30% non-UI; none from Dribbble/Behance concepts; references are real (URLs) or explicitly marked as described-not-captured.
8. Specimen rendered per direction (headline, paragraph, button, input, data row) with the proposed tokens.
9. No watch-list typeface without a written reason; no purple/indigo gradient; no cream+terracotta by reflex.

**System**
10. `tokens/` in DTCG with primitives → semantic (light + dark) → components; `build_tokens.py --check` clean.
11. `contrast.py --tokens` passes; dark mode is a separate palette (surfaces L≈0.18–0.24), not an inversion.
12. `design/DESIGN.md` written from the template with the attribute → visual consequence table filled.

**Composition & build**
13. First viewport is a poster: one headline ≤ 8 words, one action, one real product visual or typographic composition; no pill badge, no two identical buttons, no centered-everything.
14. No 3-icon-card feature grid; features shown in context; section rhythm varies; no fixed hero→features→logos→testimonials→pricing→FAQ→CTA skeleton.
15. Pricing (if present) honest: no "Most popular" unless justified; multi-currency shown because the research said so.
16. No fabricated logos, testimonials, metrics, or avatars; `[placeholders]` listed for the user.
17. Prototype uses only tokens (no literal hex/px/font in components); Tailwind v4 `@theme` from `build/theme.css`.
18. Craft floor applied: `::selection`, focus ring, `tabular-nums`, `text-wrap`, real punctuation; responsive at 360/768/1280 with no horizontal scroll.
19. Copy: verb+object buttons, no banned words, delete-30% evident (short, specific sentences).
20. Motion: at most one orchestrated entrance; no fade-up on every section; reduced-motion path.

**Review**
21. Ran `slop_lint.py` (grade A/B, remaining hits annotated) and `contrast.py`; walked the 13 gates; wrote the studio test answers; fixed blockers before presenting.
22. Final message: decisions and why, evidence, assumptions, open items, grades; in plain sentences; no process narration.

Max 44. Pass ≥ 35 with items 16, 11, and 21 at 2.

## Rubric additions (1.1)

| Criterion | Pass condition |
|---|---|
| Market and audience | Brief names country, language, script, local conventions; research and moodboard include at least 2 local references |
| Design system question | Intake explicitly asked for Figma / Storybook / tokens / brand guide, or stated none and that one will be built |
| Visual anchor | First viewport has a designed photograph, product, illustration, or graphic device; prototype contains real img/picture/video elements; no gray placeholder boxes |
| Not the skill's own tell | Not dark surface + serif display + fact table + one button; could not be mistaken for another industry's page by swapping nouns |
| Budget | Standard mode finished in 15 minutes or less with one direction plus an alternative; no unrequested documents |
