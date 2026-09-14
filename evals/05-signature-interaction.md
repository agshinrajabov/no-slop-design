# Eval 05 — Signature interaction on a restrained register (Persuade, R2 + I3)

## Prompt

> Design a website for a translation agency.

## Why this eval exists

The 1.5 run of this exact prompt made a good R2 page — a typeset bilingual document as the anchor, zero stock
photography — and graded B+. It was also a brochure: one load-time stagger and a language toggle, nothing the
visitor could do. For a service whose first question is "what does it cost and when is it ready", that sells less.
The register had quietly capped interaction. A correct run keeps the restrained register and adds the interaction.

**Mode:** Standard.

## Rubric (0 / 1 / 2 each)

**Axes**
1. Brief names the register (R2 expected, or argued otherwise) and the interaction depth (I3 expected) separately,
   each with a reason.
2. Brief and `DESIGN.md` name the signature interaction as *top job → result → carries into*.

**The interaction**
3. The visitor gets a price and a ready date (or the equivalent answer) in ≤ 2 steps, in or right after the first
   viewport.
4. The result carries into the conversion: prefilled quote form, WhatsApp message, or similar.
5. Estimates are labelled as estimates; assumptions (page size, working days, fees) are visible; nothing is hidden
   behind sign-up.
6. Keyboard-operable, result announced (`<output>` or `aria-live`), reduced-motion respected, and a static
   equivalent (the price table) on the page without JavaScript.
7. `data-nsd-interaction` present; `slop_lint.py` reports no `no-signature-interaction`.

**Motion with a job**
8. If there is a scroll sequence, it explains the process (scan → translate → check → certify), stays in one section,
   has at most four states, and falls back to static states under reduced motion and without JavaScript.
9. No decorative interaction: no chatbot bubble, carousel, marquee, custom cursor, fake live counter.

**Carry-over from 1.5**
10. The anchor is still a decision (`Anchor type:` declared), and photographs appear only if it is photographic.
11. `design_log.py check` was run before the direction and `design_log.py add` after; if the recent runs were dark,
    this one breaks the surface streak or says why not.
12. Standard budget respected (R2 + I3: about 15–20 minutes).

## Failure signatures

- The estimator appears only inside the contact form, or only after scrolling past every section.
- A language switch or FAQ accordion presented as "the interaction".
- A quiz wall before any information.
- The page becomes R3 in its visuals to justify the interaction — the axes were supposed to be separate.

## Rubric additions (1.7)

13. At 375 px, changing the main input shows the new result without scrolling.
14. Surface polarity was recorded from a measured full-page screenshot (`design_log.py add --screenshot`), and a
    dark-share above 0.6 is reported as dark even when the hero is light.
15. Native radios and checkboxes read correctly on every surface; no table column is clipped at 360 px; no section
    background ends mid-content.
16. Options that change nothing say so beside the result; prices are formatted in the market's locale.

## Rubric additions (1.8)

17. The direction's anchor carries the first viewport at full weight; the estimator's result has a designed form; no
    dead half beside the panel; at most one data table outside the interaction (`tables-as-sections` clean).
18. Not less expressive than the previous run of this eval, judged from first viewports side by side.
19. `shoot.py` was used for the review renders; its 375 px editing test passed; every scroll container it listed
    reflows or shows an edge cue.
20. The deliverable holds no review scaffolding (`review-scaffolding` clean), and the run stayed within budget
    because no screenshot harness was built.
