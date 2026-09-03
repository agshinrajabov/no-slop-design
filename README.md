# no-slop-design

An open-source [Agent Skill](https://agentskills.io) that turns a coding agent into a senior product designer:
one that researches before it draws, builds a moodboard from real references, works in design tokens, respects the
platform it ships on, and refuses to produce the generic "AI-generated" look.

Works with Claude Code (as a skill or a plugin) and with any agent that reads the `SKILL.md` format
(Codex, Cursor, Copilot, OpenClaw, and others).

## What it does

When you ask the agent to design, redesign, or review UI, the skill runs a real design process instead of emitting a
template:

| Phase | What happens | Artefact |
|---|---|---|
| 0 Detect | Classifies the request; finds any existing design system, brand, tokens, or prior direction; baselines the current UI with the slop linter | findings |
| 1 Brief | One pre-filled intake message: product, user, top job, the memorable thing, anti-attributes, constraints; picks a surface mode (Persuade / Operate / Read / Play) | `design/brief.md` |
| 2 Research | 30–120 min mini research: job stories, assumption map, competitor teardown, review mining, heuristic pass; each insight ends in a decision | `design/research.md` |
| 3 Moodboard | Attributes → brand-driver exercise → annotated real-world references → remix thesis → 2–3 named directions with live specimens | `design/moodboard.html` |
| 4 System | OKLCH color scales, fluid type scale, spacing, radius, elevation, motion; semantic roles for light and dark; compiled to CSS, Tailwind v4, Swift, Kotlin, Dart; every role contrast-checked | `tokens/`, `build/`, `design/DESIGN.md` |
| 5 Compose | Per screen: content by priority, one focal point, reading path, structure that fits the content; full component state matrix; copy last | screen and component specs |
| 6 Build | HTML/CSS prototype with real content and all states at three widths, the repo's framework, or native code; Figma via MCP when available | working UI |
| 7 Review | 13-gate self-critique, slop linter, contrast check, studio test; grade B or better or it goes back | `design/review-{date}.md` |
| 8 Hand off | Deliverables, specs, QA checks, decision records | handoff package |

Short requests take the short path (a single component is detect → short brief → 30-minute research → compose →
build → review). A critique request produces a report without a rebuild.

## What "no slop" means here

Slop is not a style. It is what happens when a visual decision is *not made*: the default font, the purple gradient,
the three icon cards, the card inside a card, the fade-up on every section, the "Unlock the power of…" headline.
The skill treats every one of these as a question ("was this chosen?") and ships a catalog of roughly 86 tells across
color, type, layout, components, iconography, copy, motion, imagery, accessibility, and process, including the
**over-correction** tells (brutalism-for-no-reason, mono-everywhere, editorial-serif costume, cream + terracotta)
that replaced the first wave. 35 of the mechanical ones are checked by the linter.

The catalog is enforced three ways: by the moodboard method (decisions traceable to attributes and references), by
the review gate (13 gates, graded), and mechanically by `scripts/slop_lint.py`.

The brief always beats the catalog. If your brand uses Inter or purple, the skill uses them well and documents the
tension.

## Install

**Claude Code, as a plugin (recommended):**

```bash
claude plugin marketplace add agshinrajabov/no-slop-design
```

```bash
claude plugin install no-slop-design@no-slop-design
```

Or in a session: `/plugin marketplace add agshinrajabov/no-slop-design`, then `/plugin install no-slop-design@no-slop-design`.

**Claude Code, as a plain skill:**

```bash
git clone https://github.com/agshinrajabov/no-slop-design ~/.claude/skills/no-slop-design
```

**Try without installing:**

```bash
claude --plugin-dir ./no-slop-design
```

**Other agents:** copy the directory into wherever your agent loads `SKILL.md` skills from (for example
`.agents/skills/`, `.cursor/skills/`, or the project root). The scripts need only Python 3.9+ and the standard library.

## Use

Just ask for design work. The skill triggers on requests like:

- "Design the onboarding flow for this app."
- "This landing page looks AI-generated. Fix it."
- "Create a design system for our product; we have a logo and a brand color."
- "Review this screen."
- "Build the settings page in our existing design system."

Explicitly: `/no-slop-design` (skill) or `/no-slop-design:no-slop-design` (plugin), followed by the request.

## Scripts

All stdlib Python; no installs.

| Script | Purpose |
|---|---|
| `scripts/slop_lint.py <path>` | Scans HTML, CSS, JSX/TSX, Vue, Svelte, Dart, Swift, Kotlin for slop signatures (purple gradients, default fonts, icon tiles, left-border cards, glass cards, emoji icons, banned copy, `transition: all`, removed focus outlines, …). Prints findings with the catalog section to read, and a grade A–F. `--json`, `--strict` for CI. |
| `scripts/contrast.py` | WCAG 2.x ratio and APCA Lc for a pair, a pairs file, every pair in a file, or, with `--tokens build/tokens.flat.json`, every text role on every surface role per mode. Exit 1 on AA failure. |
| `scripts/build_tokens.py tokens/*.json --out build/` | Compiles W3C DTCG tokens (with aliases and `*.dark.json` mode files) to CSS custom properties (light + dark), Tailwind v4 `@theme`, SwiftUI, Jetpack Compose, Flutter, and flat JSON. `--check` validates. |
| `scripts/type_scale.py` | Fluid modular type scale (`clamp()`), with line-height and tracking per step; outputs table, CSS, or DTCG. |

## Layout

```
no-slop-design/
  SKILL.md                     the router (what to do, when to read what)
  references/                  20 deep references, loaded per phase
    discovery.md · existing-design-system.md · mini-user-research.md · moodboard.md · inspiration-sources.md
    anti-slop.md · design-tokens.md · color.md · typography.md · spacing-layout.md · components.md
    ux-patterns.md · content-microcopy.md · motion.md · accessibility.md · web-frontend.md
    mobile-ios.md · mobile-android.md · review-checklist.md · handoff.md
  templates/                   brief, research synthesis, moodboard.html, DESIGN.md, DTCG token starter set,
                               contrast pairs, design log, component spec, review report
  scripts/                     slop_lint.py · contrast.py · build_tokens.py · type_scale.py
  evals/                       scenarios and rubrics to test the skill against a model
  .claude-plugin/              plugin and marketplace manifests
```

## How it compares

Existing design skills each cover a slice: taste briefings with no workflow, searchable style databases that still
recommend glassmorphism, browser-audit monoliths with heavy dependencies, anti-slop catalogs with no research or
tokens, token pipelines with no aesthetic opinion, UX method libraries with no visual opinion. This skill's bet is
that slop is a *process* failure, so the fix is a complete, spec-compliant process: research → moodboard → tokens →
composition → review, with mechanical checks, for web **and** native, inside an existing system **or** from scratch.
The closest neighbours (project-memory design-engineering skills, craft-scoring detectors) are strong on consistency and
linting; this skill adds the upstream half they skip: user research, an annotated real-reference moodboard, platform
HIG/Material rules, and a DTCG token pipeline that compiles to five platforms.

## Contributing

Issues and pull requests are welcome, especially: new tells for `references/anti-slop.md` (with a source or a
screenshot), false positives in `scripts/slop_lint.py`, platform updates (HIG, Material), and eval scenarios that
expose weak spots. Keep additions in the existing style: dense, numeric, tables over prose, no marketing language.
See `CONTRIBUTING.md`.

## License

MIT. See `LICENSE`.
