# Discovery & Brief

The first 10–20 minutes of any engagement. Discovery decides what kind of work this is, what already exists, and
what must be true for the result to be good. Its output is a filled `templates/design-brief.md`. Skipping it is how
defaults (slop) get in: every unanswered question is answered by the training-data average.

## Contents

1. Classify the request
2. Detect what exists
3. The intake conversation
4. Surface modes
5. Scope ladder and deliverables
6. Autonomy rules (when the user is not available)
7. Brief quality bar
8. Red flags that stop the work

---

## 1. Classify the request

| Request type | Signals | Path |
|---|---|---|
| **New product / brand** | no repo or empty repo; "build me a…"; no brand assets | full path: research → moodboard → tokens → system → screens → review |
| **New feature in an existing product** | repo with UI; screens exist | detect system (`existing-design-system.md`) → mini research on the job → screens in the system → review |
| **Redesign** | "make it look better", "modernise", "it looks AI-generated" | audit (review gate + slop lint on current) → decide refine vs redesign → moodboard if redesign → rebuild |
| **Single screen / component** | narrow ask | detect system → 30-min research → compose → review; never introduce new tokens without reason |
| **Design system only** | "tokens", "design system", "theme" | inventory → moodboard (if new) → tokens → components → DESIGN.md |
| **Critique / review only** | "review", "audit", "what's wrong" | `review-checklist.md` + `anti-slop.md`; report, don't rebuild unless asked |
| **Marketing page** | landing, pricing, launch | Persuade mode; `spacing-layout.md` §7; strict honesty rules on proof |
| **Mobile app** | iOS/Android/Flutter/RN | platform file first; system components posture decided before visuals |

State the classification to the user in one sentence and proceed; ask only if two paths would produce materially
different work.

## 2. Detect what exists

Before asking anything, look (5 minutes):

- Repo: `DESIGN.md`, `design/`, `tokens/`, CSS variables, Tailwind config/`@theme`, component library, Storybook,
  fonts loaded, `README`, recent UI commits. Run `python3 scripts/slop_lint.py <src>` on the current UI for a baseline.
- Brand: logos, brand guide PDFs, color/font mentions in docs.
- Product: run it or open it; screenshot the main screens; note density, fonts, palette, navigation.
- Prior work in this workspace: `design/design-log.json` (direction, decisions, previous reviews, anti-convergence log).
- Platform: package files (`package.json` → framework; `Podfile`/`*.xcodeproj` → iOS; `build.gradle` → Android;
  `pubspec.yaml` → Flutter).

Write what you found into the brief's constraints section before the conversation, so the user confirms instead of
dictates.

## 3. The intake conversation

One message, not a questionnaire. Pre-fill everything inferable; ask only the gaps. The essential questions:

1. **What is it, for whom, and what job do they hire it for?** (product, primary user, top task)
2. **What should someone remember after seeing it once?** (the memorable thing — a feeling, a visual, a claim, a posture)
3. **What must it never feel like?** (anti-attributes; also "which competitors do you *not* want to resemble")
4. **What exists that I must respect?** (design system, brand assets, platform, tech stack, localisation, a11y target)
5. **What does done look like?** (fidelity, deliverables, metric, deadline)
6. Optional accelerators: 2–3 products (any category) whose *feel* you admire and why; 2–3 you dislike and why.

Tell the user they can answer in prose; you will structure it. If they have no opinions, say you will decide and
mark decisions as revisable in the brief.

If the answer to question 2 is generic ("clean, modern"), push once: "Clean and modern describes most products.
If a friend used it for a week, what would they say about it?"

## 4. Surface modes

Every screen belongs to one mode; the mode sets the rules that apply. Decide per surface, not per product.

| Mode | Purpose | Layout posture | Type & color | Motion | Copy |
|---|---|---|---|---|---|
| **Persuade** (marketing, landing, pricing, onboarding pitch) | make a case, one action | poster-like first viewport, varied rhythm, brand loudest | expressive display face, brand color dominant | 1 orchestrated entrance, 1–2 signature moments | product language, specific claims, real proof |
| **Operate** (app UI, dashboards, admin, settings, tools) | complete tasks repeatedly | workspace + nav + context, calm surfaces, dense but readable | text face for everything, few colors, accent for action/selection | functional only, 80–250ms | utility language: orientation, status, action |
| **Read** (docs, articles, help, legal) | sustain reading | single column, 60–70ch, generous leading | text serif or humanist sans, high contrast | none beyond navigation | plain, structured, scannable |
| **Play** (games, media, immersive, kiosks) | engage, entertain | full-bleed, custom chrome allowed | brand-driven, may break conventions | signature motion is the product | in-world voice |

Hybrids exist (a marketing site with an interactive demo; an app with an onboarding pitch); apply the mode per
region.

## 5. Scope ladder and deliverables

| Level | Deliverables | When enough |
|---|---|---|
| L1 Critique | `review-report.md` with findings and fixes | user wants opinion, not work |
| L2 Direction | brief + research synthesis + moodboard (2–3 directions) | before any pixels on a new product |
| L3 System | + `tokens/` + `build/` + `DESIGN.md` + core component specs | foundation for a team or agent to build on |
| L4 Screens | + screen specs + HTML/framework prototype (real content, real states) at 3 widths or the device | what most feature requests need |
| L5 Production | + implemented UI in the repo's stack, tests, a11y audit, Figma sync if MCP available | when asked to ship |

Default for "design X for me" with no further instruction: **L4** for features, **L2→L3→L4** sequentially for new
products with a check-in after L2 (the direction decision).

## 6. Autonomy rules (when the user is not available)

- Proceed on stated assumptions; write each assumption in the brief with its risk.
- Decide the direction yourself, but produce 2 directions in the moodboard and mark the recommended one; the user
  can swap later without redoing research.
- Never fabricate research inputs (quotes, numbers, users). Mark assumption-based artefacts as such.
- Never introduce content that must be real (logos, testimonials, metrics); use `[bracketed placeholders]` and list them.
- Stop and ask only when a decision is irreversible or expensive (rebrand of an existing product, dropping a
  platform, changing an existing system's primitives).

## 7. Brief quality bar

The brief is complete when:
- every field in `templates/design-brief.md` is filled or has an owner/date;
- the memorable thing is one specific sentence;
- attributes/anti-attributes are contestable (a good product could choose the opposite);
- constraints list what exists (system level 0–3) and what is fixed;
- success criteria include at least one user-observable measure and the slop gate;
- open questions have assumptions and risks.

## 8. Red flags that stop the work

- The request is to copy a specific competitor's UI ("make it look exactly like X"). Offer a remix instead; explain why
  a clone underperforms and may be a legal problem.
- The request asks for dark patterns (fake urgency, confirmshaming, hidden costs, pre-checked upsells). Decline that
  part; propose the honest version.
- The request asks for fake proof (invented testimonials, logos, numbers). Decline; use placeholders and say what
  must be supplied.
- The user's existing brand is fixed and conflicts with this skill's defaults. The brand wins; document the tension.
