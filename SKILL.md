---
name: no-slop-design
description: Senior product-design workflow for web and mobile UI that avoids generic "AI slop" and produces token-based, accessible, platform-correct design with real visual material. Use when asked to design, redesign, review, or "make it look better" for any screen, app, landing page, component, or design system; when building UI from scratch; when a design system or brand must be adopted or created; when generating design tokens, moodboards, or design specs; or when output must not look AI-generated. Runs discovery (market, audience, existing design system) → mini research → moodboard → tokens → composition with imagery → self-critique before delivering.
license: MIT
metadata:
  version: "1.1.0"
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
2. **Ask three things before anything else** (one message, pre-filled from what you detected): **(a)** which market,
   country, and language(s) the audience is in; **(b)** whether an existing or preferred design system exists (Figma
   library link, Storybook, tokens file, component library, brand guide) or whether we build one; **(c)** the one
   thing a first-time viewer should remember. If the user is unavailable, state assumptions for all three and proceed.
3. **Local + global.** Research and inspiration always combine the audience's own market (its leading products,
   conventions, script, trust signals, payment and legal norms) with worldwide references. Never design a Spanish
   audience's site from US SaaS references only, or only from Spanish ones.
4. **Detect before you design.** If a design system, brand, or token file exists, adopt it (`references/existing-design-system.md`). Never introduce a second visual language.
5. **Every visual value is a token.** No literal colors, sizes, or font names in UI code. DTCG JSON in `tokens/`, compiled by `scripts/build_tokens.py`.
6. **Visual material is required.** A marketing page has a designed visual anchor in the first viewport
   (photograph, product, illustration, graphic device, color field, or video) and real image elements in the
   prototype. Typographic-only pages, "fact ledger" heroes, and gray placeholder boxes are over-correction slop
   (`references/visual-material.md`).
7. **Real-world references, annotated.** ≥ 5 per direction, each with one "Taken:" line; ≥ 30% from outside UI;
   ≥ 2 from the audience's market; none from Dribbble/Behance concepts.
8. **Honest content.** Never fabricate metrics, testimonials, logos, names, avatars, or urgency. Use `[bracketed placeholders]` and list what must be supplied.
9. **Platform first on native.** iOS follows HIG (`references/mobile-ios.md`); Android follows Material 3 (`references/mobile-android.md`).
10. **Accessibility is a floor.** WCAG 2.2 AA, verified with `scripts/contrast.py`; keyboard, focus, target sizes, reduced motion.
11. **Nothing ships on the first pass.** Render it, look at it, run the review gate (`references/review-checklist.md`) and `scripts/slop_lint.py`; grade B or better.
12. **Anti-convergence.** Do not repeat the previous project's direction, and do not let this skill's own outputs
    become a template (dark surface + serif display + fact table + one button is now a known tell). Different
    industry, different attributes → visibly different structure, type, color, and imagery.
13. **Brief beats skill.** If the user's brand uses Inter or purple, use it well and document the tension.

## Modes and budgets

Default to **Standard**. Use **Deep** only when the user asks for it, or for a new product with no brand where the
direction decision is expensive to reverse. State the mode.

| | Standard (default) | Deep |
|---|---|---|
| Target wall time | 8–15 min | 30–60 min |
| Research | ≤ 15 min, ≤ 8 web fetches: 3 job stories, 3 competitor first-screens (1 local), 1 review-mining pass | full `mini-user-research.md` menu |
| Moodboard | 1 recommended direction fully specified + 1 alternative in 5 lines; 5–6 references | 2–3 full directions, 8–12 references each, specimens |
| Tokens | start from `templates/tokens/`, change hue, faces, radius, density; compile; contrast-check | full custom scales |
| Screens | the one requested screen/page with all states | flows + specs per screen |
| Specs & handoff | `DESIGN.md` + `design-log.json` only | component specs, screen specs, handoff package |
| Review | Gate 0 scripts + Gates 1, 3, 5, 6, 10, 13 + studio test | all 13 gates |
| Reference reading | only the sections named per phase below | full files |

Do not write documents nobody asked for. Do not produce three fully rendered directions when one plus an
alternative answers the question. Do not re-derive tokens from scratch when the template plus five edits will do.

## Workflow

Phases are sequential; each ends with an artefact in the project's `design/` folder. State which phase you are in.

| Phase | Do | Read (Standard: named sections) | Output |
|---|---|---|---|
| **0 Detect** | Classify the request; scan repo, brand assets, live product, `design/design-log.json`; baseline existing UI with `scripts/slop_lint.py` | `discovery.md` §1–2; `existing-design-system.md` §1–2 | findings |
| **1 Brief** | One intake message with the three questions from non-negotiable 2 plus product, user, top job, anti-attributes, constraints, done-criteria. Decide the **surface mode** (Persuade / Operate / Read / Play) | `discovery.md` §3–5 | `design/brief.md` |
| **2 Research** | Time-boxed: job stories, competitor first-screens (local + global), review mining, heuristic pass. Every insight ends in a decision | `mini-user-research.md` §1–3, §6–7, §11 | `design/research.md` |
| **3 Moodboard** | Attributes/anti-attributes → references (local + global, ≥ 30% non-UI) → remix thesis → imagery art direction → direction(s) with specimen → recommend. If a mature system exists, document it instead | `moodboard.md` §3, §5–8; `visual-material.md` §1–3; `inspiration-sources.md` (skim) | `design/moodboard.html`; direction logged |
| **4 System** | Tokens from the template: hue, neutrals, faces, scale, radius, density, motion; light + dark; compile; `contrast.py --tokens` | `design-tokens.md` §2–4; `color.md` §3–5; `typography.md` §1–3 | `tokens/`, `build/`, `design/DESIGN.md` |
| **5 Compose** | Per screen: content by priority → visual anchor → one focal point → reading path → structure that fits the content → scale contrast → rhythm → remove. All component states. Copy last | `spacing-layout.md` §2, §6–8; `visual-material.md` §2, §8; `components.md` §2–3; `content-microcopy.md` (banned list) | screen composition |
| **6 Build** | HTML/CSS prototype with real content, real image elements, all states, 3 widths; or the repo's framework; or native; Figma via MCP if available. Craft floor | `web-frontend.md` §craft floor, or the platform file | working UI |
| **7 Review** | Render at 360/768/1280 in the intended color scheme and **look**; Gate 0 scripts; gates per mode; studio test; fix; re-run | `review-checklist.md`; `anti-slop.md` §8, §12 of `visual-material.md` | `design/review-{date}.md` |
| **8 Hand off** (Deep, or on request) | Deliverables, specs, shot list, QA checks, decision records | `handoff.md` | handoff package |

**Scope shortcuts.** Single component: 0 → 1 (short) → 5 → 6 → 7. Critique only: 0 → 7, report without rebuilding.
Design system only: 0 → 1 → 3 → 4 → 7. Redesign: 0 (full audit) → refine vs redesign → 5–7 or 3–7.

## Decision rules that prevent slop

- **Audience and market:** the brief names country, language(s), script, device mix, and local conventions; research
  includes the market's leading products; the moodboard includes local references; copy and formats follow the locale.
- **Design system:** existing system → adopt and extend only; preferred system named by the user (e.g. "use
  Material", "use our Figma library") → that system's rules win; none → build from the template.
- **Visual anchor first:** choose the anchor type (`visual-material.md` §2) from what the business actually has to
  show; write the art direction; only then compose type around it. Prototypes use real licensed photographs or
  designed placeholders mapped to a shot list, never gray boxes.
- **Typeface:** chosen by attribute from `typography.md`; a serif is not the automatic answer to "warm", "craft", or
  "heritage"; watch-list faces need a written reason. Native UI text may use SF / Roboto on purpose.
- **Color:** one decided hue; 60/30/10; neutrals tinted; OKLCH; light-first for Persuade unless the brief says
  otherwise; dark mode is its own palette; no purple gradients, gradient text, glow blobs, neon-on-black.
- **Layout:** compose, don't assemble; one focal point per viewport; separation by the cheapest device; radius
  hierarchy; varied rhythm; no 3-icon-card grid, bento by reflex, centered-everything, card-in-card.
- **Components:** full state matrix; native elements first; browser surfaces themed.
- **Motion:** one orchestrated entrance at most; 80–400 ms; transform/opacity; reduced-motion path.
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

External tools when present: a **browser** for capturing references and rendering the prototype (screenshots are the
review evidence; render in the color scheme the audience will see); **Figma MCP** for reading an existing library and
pushing tokens/screens (load the Figma skills first); an **image-generation tool** for art-directed hero imagery per
`visual-material.md` §7; simulators/emulators for native. Without them, say what you could not verify.

## Project layout the skill creates

```
design/   brief.md · research.md · moodboard.html · DESIGN.md · design-log.json · contrast-pairs.txt · assets.md
          (Deep: screens/*.md · components/*.md · review-{date}.md · handoff.md · research/)
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
| `references/moodboard.md` · `references/inspiration-sources.md` | Phase 3; method, local and global sources, remix rule |
| `references/visual-material.md` | Phase 3, 5, 6; anchors, art direction, placeholders, sourcing, industry starting points |
| `references/anti-slop.md` | Phase 3 and 7; full catalog incl. over-correction; the studio test |
| `references/design-tokens.md` · `references/color.md` · `references/typography.md` | Phase 4 |
| `references/spacing-layout.md` · `references/components.md` · `references/ux-patterns.md` | Phase 5–6 |
| `references/content-microcopy.md` · `references/motion.md` · `references/accessibility.md` | Phase 5–7 |
| `references/web-frontend.md` · `references/mobile-ios.md` · `references/mobile-android.md` | Phase 6 per platform |
| `references/review-checklist.md` · `references/handoff.md` | Phase 7–8 |

Templates: `templates/design-brief.md`, `templates/research-synthesis.md`, `templates/moodboard.html`,
`templates/DESIGN.md`, `templates/tokens/*.json`, `templates/contrast-pairs.txt`, `templates/design-log.json`,
`templates/component-spec.md`, `templates/review-report.md`.
