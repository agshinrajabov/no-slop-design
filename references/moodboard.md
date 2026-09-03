# Moodboard

The moodboard is the decision device that prevents slop. It turns brand strategy and research into a small set of
named visual commitments, backed by real-world references, *before* any screen is drawn. Without it, style is
chosen by reflex, and reflex is the training-data average. Output: `design/moodboard.html` (from
`templates/moodboard.html`) with 2–3 named directions, one of which the user approves; the approved direction feeds
`DESIGN.md` and the tokens.

## Contents

1. What a moodboard is (and is not)
2. Inputs required
3. Step 1 — attributes and anti-attributes
4. Step 2 — the visual brand driver exercise
5. Step 3 — reference gathering (real world, annotated)
6. Step 4 — the remix rule
7. Step 5 — from attributes to visual decisions (the design code)
8. Step 6 — compose 2–3 directions
9. Step 7 — present, decide, record
10. Moodboards for existing brands
11. Moodboard slop
12. Quality bar

---

## 1. What a moodboard is (and is not)

A moodboard **is**: 6–15 annotated references per direction, three attribute words and three anti-words, a color
and type hypothesis, a density and motion posture, a one-sentence visual thesis, and a "not this" list.

A moodboard **is not**: a Pinterest wall of pretty screenshots, a Dribbble scroll, a palette generator output, or a
list of adjectives ("modern, clean, minimal"). Adjectives that could describe any product describe none.

## 2. Inputs required

From `templates/design-brief.md`: product, audience, surface type, the memorable thing, constraints (existing brand
assets, platform). From `templates/research-synthesis.md`: emotional register (arrive feeling → leave feeling),
category clichés, the empty quadrant on the perception map, vocabulary users use.

If any of these are missing, get them first. A moodboard built on an empty brief is decoration.

## 3. Step 1 — attributes and anti-attributes

Pick **three** attributes the product must project and **three** it must never project. Rules:

- Specific over generic: "unhurried" beats "calm"; "engineered" beats "professional"; "hospitable" beats "friendly".
- Each attribute must be *contestable*: some good product could reasonably choose the opposite.
- Anti-attributes are not the antonyms; they are the *nearby failure modes*. For "premium" the anti-attribute is
  "pretentious", not "cheap". For "playful" it is "childish".
- Test: put the six words in front of the user. If they say "yes, obviously", the words are too generic.

| Attribute | Anti-attribute | One product that nails it |
|---|---|---|
| Unhurried | Sleepy | (name a real one) |
| Exacting | Cold | |
| Hospitable | Cute | |

## 4. Step 2 — the visual brand driver exercise

Fast way to surface taste without asking "what colors do you like" (which yields personal preference, not brand).
Ask the user (or answer from the brief) to pick a representative for the *brand*, not for themselves, in each row,
and give 2–3 adjectives per pick:

| Category | Pick | Adjectives |
|---|---|---|
| Vehicle | | |
| Typeface (from a shown set of 8) | | |
| Piece of furniture / architecture | | |
| Material (paper, steel, linen, glass, oak, concrete) | | |
| Drink | | |
| Animal | | |
| A place (city, room, landscape) | | |
| Sound / music | | |

Recurring adjectives across rows become the attributes; the materials and places seed color temperature, texture,
and density.

## 5. Step 3 — reference gathering (real world, annotated)

Minimum **5 references per direction** (Standard: 5–6; Deep: 8–12), from *shipped* products and *non-UI* sources,
**at least 2 from the audience's own market** (its leading brands, signage, print, architecture, local design studios)
and at least 2 global. Use the source
map in `inspiration-sources.md`. For each reference record:

```
Source:      URL / product / screen
Type:        UI · editorial · packaging · architecture · signage · photography · motion
Taken:       ONE thing, named precisely — "the way price sits inside the headline", "12-col grid with 1 breakout image", "warm gray ramp with one hot accent"
Not taken:   what we deliberately leave behind
Serves:      which attribute
```

Rules:
- At least **30% non-UI** references (print, environments, objects, film stills). UI-only boards converge on the
  current UI trend, which is next year's slop.
- At least **2 references from outside the category**. Same-category references reproduce the category's clichés.
- **Dribbble/Behance concepts are not references**; they are unshipped fantasies optimised for peer likes. Use
  Mobbin, Refero, Godly, siteinspire, Fonts In Use, Are.na, and real products.
- If a browser tool is available, capture real screenshots; if not, describe precisely and link. Never invent a
  reference that you have not seen.
- Every reference must have a "Taken:" line. A reference without one is decoration.

## 6. Step 4 — the remix rule

Copying one reference yields a knock-off. The reliable method is to **remix two unrelated references** on
different axes:

> Typography discipline of [A] × color world of [B] × density of [C]

Examples of the shape (invent your own for each project): a Swiss timetable's grid × a ceramics studio's palette;
a broadsheet's hierarchy × a game HUD's motion restraint; a bank's density × a bakery's warmth. Write the remix as
one sentence: this is the **visual thesis**.

## 7. Step 5 — from attributes to visual decisions (the design code)

Translate each attribute into concrete, testable consequences. This table becomes the top of `DESIGN.md`.

| Attribute | Typography | Color | Space & layout | Shape & surface | Motion | Imagery | Voice |
|---|---|---|---|---|---|---|---|
| e.g. Unhurried | text serif with generous x-height; body 18px; LH 1.65 | low chroma, warm neutrals, one deep accent | wide margins, single column, 72ch measure | radius.card 12, no shadows, hairline rules | 250–350ms, decelerate, no entrance choreography | still photography, natural light, no people looking at camera | full sentences, no exclamation marks |
| e.g. Exacting | grotesk with tabular figures; tight display tracking | near-neutral palette, status hues only | 4px grid, dense tables, aligned numerals | radius.control 4, 1px borders, no gradients | 120–200ms, standard curve | diagrams over photos | terse, verb-first |

Fill every cell for every attribute, or state "no consequence" explicitly. Where two attributes conflict in a cell,
decide now and write the tie-breaker.

## 8. Step 6 — compose 2–3 directions

Each direction gets: a name (two words, evocative, not "Modern Clean"), the visual thesis sentence, its reference
set, an **imagery art direction** (anchor type, subject, people, light, treatment, crop — `visual-material.md` §2–3;
"no imagery" is a decision that needs a written reason), a type pairing (display + text, named), a five-swatch palette in OKLCH (surface, surface-raised, text, accent,
accent-strong) for light and, if relevant, dark, one radius/shape statement, a density statement, a motion
posture, an imagery statement, and a **"not this"** list of 5 items specific to this direction.

Directions must differ on at least two axes (e.g. warm/cool, dense/airy, serif/grotesk, still/kinetic). Three
variations of the same idea is one direction.

Include in each direction a **mini-specimen**: a headline, a paragraph, a primary button, an input, and a small data
row rendered with the proposed tokens. This is where "looks nice as swatches" dies or survives.

Coherence check per direction (fail = revise): brutal/minimal × expressive motion? Luxury × neon accent?
Data-dense × 24px radius? Playful × all-caps grotesk with tight tracking? Each is a mismatch unless argued.

## 9. Step 7 — present, decide, record

Present the directions with the same structure so they compare. Recommend one and say why, tied to the memorable
thing and the research. Ask for a decision (or decide, if working autonomously, and state the decision as revisable).

Record in `design/moodboard.html` (approved direction marked) and `design/design-log.json`:
`{ "direction": "Name", "approved": "2026-09-03", "fonts": [...], "hue": 40, "density": "comfortable", "rejected": ["Name B: too cold"] }`.
The log is read at the start of every later session so the design stays coherent and the *next* project in the
same workspace does not repeat the same direction by default (anti-convergence).

## 10. Moodboards for existing brands

When a brand or design system exists (`existing-design-system.md`), the moodboard's job changes: it documents the
*existing* attributes as observed (not as claimed), finds where current UI drifts from them, and proposes a
direction *within* the system. References come from the brand's own best work first. Never propose a new
typeface or primary color for an existing brand unless the brief asks for a rebrand.

## 11. Moodboard slop

- Adjectives only, no references.
- References without "Taken:" lines.
- Only Dribbble/Behance shots; only same-category SaaS.
- Three directions that differ only in accent color.
- Directions named "Modern", "Bold", "Minimal".
- Palettes produced by a generator from a single hex with no temperature or chroma decision.
- Fonts chosen from the watch list in `typography.md` without a written reason.
- The specimen missing (swatches never tested against real text and controls).
- A direction that repeats the last project's direction in this workspace (check `design-log.json`).
- Imagery left as "TBD" or gray boxes; a text-only direction for a business that has rooms, people, products, or places to show.
- The skill's own recurring output (dark surface, serif display, fact table, one button) presented as if it were a decision. It is a template now; treat it as one.
- Serif chosen because the attribute was "warm", "craft", or "heritage" without testing a sans or a slab against the same attribute.

## 12. Quality bar

The moodboard is done when a stranger could look at the approved direction, then at a competitor's screen, and say
in one sentence how ours will look and feel different, and *why that serves the user*.
