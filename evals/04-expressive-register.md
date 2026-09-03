# Eval 04 — Register choice under an ambiguous brief (Persuade, R3/R4 territory)

## Prompt

> Design a website for an independent contemporary dance company in Lyon. They tour three productions a year,
> sell tickets through the venues, and want people to feel the work before they read about it. They have a
> photographer on retainer and rehearsal footage. I'm not available for questions.

## Why this eval exists

1.0 and 1.1 answered every brief at the same restrained register, so a dance company came out looking like a
clinic. This scenario has an emotional decision, real assets, and a category (arts) whose norm is already
expressive, so a correct run must reach R3 (or argue R4 against its five conditions) and must not produce a
document.

**Mode:** Standard.

## Rubric (0 / 1 / 2 each)

**Register**
1. Named the register in `design/brief.md` and `DESIGN.md` with a reason tied to the decision type (emotional),
   the category norm (arts sites are already expressive), and the asset budget (photographer + footage exist).
2. Chose R3 or argued R4 explicitly against the five conditions in `expression-register.md` §6 — not "R2 to be safe".
3. Recorded the alternative one register away with what it would cost.
4. Techniques used are on the chosen register's row in §7; anything off-row is justified in writing.

**Visual material**
5. First viewport is a designed anchor (full-bleed photograph, film loop, or type as image), not a headline over a
   flat surface.
6. Art direction written (subject, people, light, treatment, crop, ratios) and every image matches it on all three
   of subject, light, material; `design/assets.md` records provenance and a shot list.
7. Video, if used, is muted, has a poster frame, and has a reduced-motion path.
8. No label/value table as the layout device in more than two sections; section devices vary.

**Craft**
9. Display type is at the register's scale; the page could not be swapped into another industry by changing nouns.
10. Local fit: French language or a stated language decision, French/European arts conventions (tour dates, venue
    partners, tarif réduit), at least two references from that market.
11. Motion: one entrance choreography plus at most one signature moment; reduced-motion path; **reloading with
    JavaScript disabled still shows every section** (`reveal-no-fallback` clean).
12. Accessibility unchanged by the register: contrast passes both modes, focus visible, targets ≥ 44 px, captions
    or transcripts for footage.

**Discipline**
13. `slop_lint.py` grade A or B with any remaining hits annotated; `contrast.py --tokens` exit 0;
    `build_tokens.py --check` free of palette warnings (accent derived from the brand hue).
14. Standard budget respected: finished inside ~15 minutes, 4–6 sections, no unrequested documents.
15. Honest content: no invented reviews, no fabricated audience numbers, dancers' names bracketed unless supplied.

## Failure signatures to watch for

- R2 chosen by reflex, or the register named but not reached on screen.
- A "programme" table doing the work a photograph should do.
- Stock dance photography that contradicts the written art direction (wrong light, wrong style, obvious stock).
- Dark surface + serif display + one accent, i.e. the skill's own tell reappearing.
- The page reading identically to eval 01's SaaS landing page in structure.
