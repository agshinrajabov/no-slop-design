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
