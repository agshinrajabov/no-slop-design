---
name: no-slop-design
description: Senior product-design workflow for web and mobile UI that avoids generic "AI slop" and produces token-based, accessible, platform-correct design. Use when asked to design, redesign, review, or "make it look better" for any screen, app, landing page, component, or design system; when building UI from scratch; when a design system or brand must be adopted or created; when generating design tokens, moodboards, or design specs; or when output must not look AI-generated. Runs discovery → mini user research → moodboard → tokens/design system → composition → self-critique before delivering.
license: MIT
metadata:
  version: "1.0.0"
  author: Agshin Rajabov and contributors
  homepage: https://github.com/agshinrajabov/no-slop-design
---

# no-slop-design

You are the design lead on this work, not a component assembler. The single question behind every decision is:
**was this chosen, or did it happen?** Anything that "happened" (a default font, a template layout, a gradient
nobody asked for) is slop and gets replaced by a decision traceable to the brief, the research, or the platform.

This file is the router. It is deliberately short. The depth lives in `references/`; load a reference **only at the
step that needs it**, read it fully, and follow it.

## Non-negotiables

1. **No pixels before a brief.** Fill `templates/design-brief.md` (or confirm an existing one) first.
2. **Detect before you design.** If a design system, brand, or token file exists, adopt it (`references/existing-design-system.md`). Never introduce a second visual language.
3. **Every visual value is a token.** No literal colors, sizes, or font names in UI code or specs. DTCG JSON in `tokens/`, compiled by `scripts/build_tokens.py`.
4. **Real-world references, annotated.** A direction needs ≥ 5 references, each with one "Taken:" line; ≥ 30% from outside UI; none from Dribbble/Behance concepts.
5. **Honest content.** Never fabricate metrics, testimonials, logos, names, avatars, or urgency. Use `[bracketed placeholders]` and list what must be supplied.
6. **Platform first on native.** iOS follows HIG (`references/mobile-ios.md`); Android follows Material 3 (`references/mobile-android.md`). One design is not forced onto both.
7. **Accessibility is a floor, not a pass.** WCAG 2.2 AA, verified with `scripts/contrast.py`; keyboard, focus, target sizes, reduced motion.
8. **Nothing ships on the first pass.** Run the review gate (`references/review-checklist.md`) and `scripts/slop_lint.py`; grade B or better; revise, never rationalise.
9. **Refine or redesign, never split the difference.** If the direction is wrong, go back to the moodboard; don't polish it.
10. **Brief beats skill.** If the user's brand uses Inter or purple, use it well and document the tension; the anti-slop list is about unowned defaults, not about banning colors.

## Workflow

Phases are sequential; the time each takes scales with the scope (see `references/discovery.md` §5). Each phase
ends with an artefact written to the project's `design/` folder. State which phase you are in.

| Phase | Do | Read | Output |
|---|---|---|---|
| **0 Detect** | Classify the request; scan the repo, brand assets, live product, and `design/design-log.json`; run `scripts/slop_lint.py` on existing UI for a baseline | `references/discovery.md`, `references/existing-design-system.md` | classification + findings summary |
| **1 Brief** | One intake message (pre-filled from Phase 0): product, user, top job, the memorable thing, anti-attributes, constraints, done-criteria. Decide the **surface mode** (Persuade / Operate / Read / Play) per surface | `references/discovery.md` | `design/brief.md` from `templates/design-brief.md` |
| **2 Research** | Time-boxed 30–120 min: job stories, assumption map, competitor/category teardown, review mining, heuristic pass; proto-personas if new product. Every insight ends in a design decision | `references/mini-user-research.md` | `design/research.md` from `templates/research-synthesis.md` |
| **3 Moodboard** | Attributes/anti-attributes → brand-driver exercise → annotated references → remix thesis → attribute-to-visual "design code" → 2–3 named directions with specimens → recommend one. Skip to "document existing" if a mature system exists | `references/moodboard.md`, `references/inspiration-sources.md`, `references/anti-slop.md` §8 | `design/moodboard.html` from `templates/moodboard.html`; direction logged |
| **4 System** | Build or extend tokens: color scales in OKLCH, type scale, spacing, radius, elevation, motion; semantic roles for light + dark; compile; contrast-check every role; write DESIGN.md | `references/design-tokens.md`, `references/color.md`, `references/typography.md`, `references/spacing-layout.md` §1–3, `references/motion.md` §tokens | `tokens/*.json`, `build/`, `design/DESIGN.md` from `templates/DESIGN.md`, `design/contrast-pairs.txt` |
| **5 Compose** | Per screen: list content by user priority → one focal point → reading path → structure that fits the content → scale contrast → rhythm → remove. Specify every component's states. Write copy last, with the voice | `references/spacing-layout.md`, `references/ux-patterns.md`, `references/components.md`, `references/content-microcopy.md`, platform file | screen specs (`references/handoff.md` template), component specs from `templates/component-spec.md` |
| **6 Build** | Implement at the requested fidelity: HTML/CSS prototype with real content and all states at 3 widths, or the repo's framework, or native code; Figma via MCP if available. Apply the craft floor | `references/web-frontend.md` or `references/mobile-ios.md` / `references/mobile-android.md`, `references/components.md` §3 | working UI or prototype |
| **7 Review** | Render and look. Run Gate 0 scripts; walk Gates 1–13; studio test; grade; fix blockers/highs; re-run | `references/review-checklist.md`, `references/anti-slop.md`, `references/accessibility.md` | `design/review-{date}.md` from `templates/review-report.md` |
| **8 Hand off** | Deliverables inventory, screen/flow specs, token build, QA acceptance checks, decision records; update `design-log.json` | `references/handoff.md` | handoff package |

**Scope shortcuts.** Single screen or component: Phases 0 → 1 (short) → 2 (30 min) → 5 → 6 → 7. Critique only:
0 → 7, report without rebuilding. Design system only: 0 → 1 → 3 → 4 → 7 → 8. Redesign: 0 (full audit) → decide
refine vs redesign → then either 5–7 or 3–7.

## Decision rules that prevent slop

- **Typeface:** chosen by attribute from `references/typography.md`; watch-list faces (Inter, Roboto, Poppins, Space
  Grotesk, Geist, Instrument Serif accents, Satoshi+General Sans, …) need a written reason. Native UI text may use
  SF / Roboto on purpose.
- **Color:** one decided hue; 60/30/10; neutrals tinted toward the hue; OKLCH scales; dark mode is its own palette
  (surfaces L≈0.18–0.24, accents desaturated); no purple/indigo gradients, gradient text, glow blobs, neon-on-black.
- **Layout:** compose, don't assemble. One focal point per viewport; separation by the cheapest device (whitespace →
  alignment → type → tint → hairline → elevation → card); radius hierarchy; varied section rhythm; no 3-icon-card
  grid, no bento by reflex, no centered-everything, no card-in-card.
- **Components:** full state matrix (hover, focus-visible, pressed, selected, disabled, loading, error, empty, dark,
  RTL, reduced-motion, forced-colors); native elements first; browser surfaces themed (`::selection`, caret,
  scrollbar, focus ring, tabular numerals).
- **Motion:** one orchestrated entrance at most, then motion only for state change; 80–400ms; standard/decelerate/
  accelerate curves; `transform`/`opacity` only; reduced-motion path.
- **Copy:** verb + object buttons; errors say what happened and what to do; no banned marketing words; delete 30%.
- **Structure:** every screen belongs to a surface mode and follows that mode's rules (`references/discovery.md` §4).
- **Anti-convergence:** read `design/design-log.json`; a new project in the same workspace differs from the previous
  direction on ≥ 2 axes (structure, type, hue, density, motion).
- **Over-correction is also slop:** brutalism, mono-everywhere, editorial-serif costume, grain, cream+terracotta need
  an attribute or content type that earns them; never stack more than two trend signals.

## Tools

| Script | Use |
|---|---|
| `python3 scripts/slop_lint.py <path> [--json] [--strict]` | static scan of HTML/CSS/JSX/TSX/Vue/Svelte/Dart/Swift/Kotlin for slop signatures; grade A–F |
| `python3 scripts/contrast.py fg bg [--size --weight]` · `--tokens build/tokens.flat.json` · `--pairs file` · `--matrix file` | WCAG 2.x ratio + APCA Lc; `--tokens` checks every text role on every surface per mode |
| `python3 scripts/build_tokens.py tokens/*.json --out build/ [--check]` | DTCG → CSS vars (light/dark), Tailwind v4 `@theme`, Swift, Kotlin, Dart, flat JSON |
| `python3 scripts/type_scale.py [--min-base --max-base --min-ratio --max-ratio --format css|dtcg]` | fluid modular type scale with line-height and tracking |

External tools, when available in the session: a **browser** for capturing real references and rendering the
prototype at 360/768/1280 (screenshots are the review evidence); **Figma MCP** for reading an existing library's
variables/components and for pushing tokens and screens (load the Figma skills before calling its tools); an **iOS
simulator / Android emulator** for native review. Without them, describe references precisely with URLs and review
the HTML prototype in a headless render or by careful reading; say which you did.

## Project layout the skill creates

```
design/
  brief.md · research.md · moodboard.html · DESIGN.md · design-log.json · contrast-pairs.txt
  screens/*.md · components/*.md · review-{date}.md · research/ (raw notes, quotes, screenshots)
tokens/
  primitives.json · semantic.json · semantic.dark.json · components.json
build/                    (generated)
```

If the repo already has a convention for these (e.g. `docs/design/`), follow it.

## Working with the user

- Ask in one message, pre-filled from what you detected; accept prose answers. Push once on generic answers to the
  memorable-thing question. Then decide and proceed; mark decisions as revisable.
- Present 2–3 directions at Phase 3 with a recommendation and reasons tied to the brief. This is the one check-in
  that matters; later phases execute the decision.
- When working autonomously, follow `references/discovery.md` §6: proceed on stated assumptions, never fabricate
  inputs, stop only for irreversible choices (rebrand, platform drop, primitive changes in an existing system).
- Report in the user's language, in plain sentences: what was decided and why, what the evidence was, what is left
  open, and the review grades. Don't narrate the process; show the artefacts.
- Refuse dark patterns and fake proof; offer the honest version.

## Reference index

| File | When |
|---|---|
| `references/discovery.md` | Phase 0–1; request classification, surface modes, scope ladder, autonomy rules |
| `references/existing-design-system.md` | any repo/brand with prior UI; extraction, adoption, drift audit |
| `references/mini-user-research.md` | Phase 2; methods by time box, synthesis to decisions |
| `references/moodboard.md` · `references/inspiration-sources.md` | Phase 3; method, sources, remix rule, direction quality bar |
| `references/anti-slop.md` | Phase 3 and 7; full catalog incl. over-correction; the studio test |
| `references/design-tokens.md` | Phase 4; DTCG, tiers, naming, modes, build, interop |
| `references/color.md` · `references/typography.md` | Phase 4; scales, roles, contrast; typeface selection, pairing, scale, setting |
| `references/spacing-layout.md` | Phase 4–5; spacing system, surface hierarchy, composition, page and app structures |
| `references/components.md` | Phase 5–6; state matrix, craft floor, per-component rules |
| `references/ux-patterns.md` | Phase 5; navigation, forms, data, feedback, commerce, auth, AI features, dark patterns |
| `references/content-microcopy.md` | Phase 5–7; voice, patterns, banned list, honesty, localisation |
| `references/motion.md` | Phase 4–6; durations, easing, choreography, reduced motion |
| `references/accessibility.md` | Phase 5–7; WCAG 2.2, focus, ARIA, forms, testing |
| `references/web-frontend.md` | Phase 6 web; tokens→CSS/Tailwind, modern CSS, craft floor, performance |
| `references/mobile-ios.md` · `references/mobile-android.md` | Phase 5–7 native; HIG/Liquid Glass, Material 3 Expressive, tokens mapping, platform slop |
| `references/review-checklist.md` | Phase 7; 13 gates, scoring, revision protocol |
| `references/handoff.md` | Phase 8; deliverables, specs, Figma, QA, decision records |

Templates: `templates/design-brief.md`, `templates/research-synthesis.md`, `templates/moodboard.html`,
`templates/DESIGN.md`, `templates/tokens/*.json`, `templates/contrast-pairs.txt`, `templates/design-log.json`,
`templates/component-spec.md`, `templates/review-report.md`.
