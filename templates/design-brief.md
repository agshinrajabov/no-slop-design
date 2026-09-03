# Design Brief — {Project name}

> Fill every field. "TBD" is allowed only with an owner and a date. A brief with empty fields
> produces generic design, because the gaps get filled with defaults — and defaults are slop.

## 1. The product in one breath

| Field | Answer |
|---|---|
| What it is | {one sentence, no adjectives} |
| Who it is for | {primary user — role, context, device, frequency of use} |
| The job they hire it for | When I {situation}, I want to {motivation}, so I can {outcome}. |
| Business goal for this piece of work | {activation / retention / conversion / trust / speed / …} |
| Market & audience locale | {country/region · language(s) & script · device mix · local conventions: payments, trust signals, regulation, formats, RTL} |
| Platform(s) | {web marketing · web app · iOS · Android · cross-platform (Flutter/RN) · desktop} |
| Mode | {Standard (default) · Deep} |
| Surface type | {landing / marketing · product UI (data-dense) · editorial · e-commerce · tool · hybrid} |
| Scope of this engagement | {new product · new feature · redesign · single screen · design system only} |

## 2. The memorable thing

> "What is the ONE thing someone should remember after seeing this for the first time?"

{one sentence — a feeling, a visual, a claim, or a posture. Every later decision serves this.}

## 3. Constraints (real ones)

- **Existing or preferred design system?** {none → we build one · partial (list: Figma library link / Storybook / tokens.json / Tailwind config / component lib) · complete (link) · preferred external system (Material 3 / HIG / shadcn / other)}
- **Visual assets available:** {photography · product shots · logo files · illustration · video · none → shot list + designed placeholders}
- **Brand assets that are fixed:** {logo · brand colors · typeface · voice guide · none}
- **Tech stack:** {Next.js + Tailwind v4 · SwiftUI · Jetpack Compose · Flutter · Vue · plain CSS · unknown}
- **Accessibility target:** {WCAG 2.2 AA (default) · AAA for {areas} · platform HIG only}
- **Localization:** {languages · RTL? · script mix (Latin/Arabic/Cyrillic/CJK)}
- **Performance / device floor:** {low-end Android · 3G · older Safari · none}
- **Legal / regulated content:** {finance · health · children · none}
- **Timeline & fidelity expected:** {wireframe · hi-fi mock · production code · tokens + spec}

## 4. Users (from mini research — see `templates/research-synthesis.md`)

| Proto-persona | Context of use | Top 3 tasks | Top frustration today | What "good" feels like to them |
|---|---|---|---|---|
| {name / role} | | | | |
| {name / role} | | | | |

## 5. Competitive & reference landscape (3–7 entries; at least 2 from the audience's market, at least 2 global)

| Product | What they do well (steal the principle, not the pixels) | Where they fail users | Visual cliché they share |
|---|---|---|---|
| | | | |

**Category conventions we must respect (table stakes):** {…}
**Category conventions we will deliberately break, and why:** {…}

## 6. Brand attributes → visual consequences

Three attributes and three anti-attributes. Each attribute must translate into at least one concrete visual decision.

| Attribute | Anti-attribute (what we are NOT) | Visual consequence |
|---|---|---|
| e.g. *Calm* | *Loud* | low-chroma palette, generous line-height, no motion on load |
| | | |
| | | |

## 7. Success criteria

- Design is done when: {measurable — task completion, time-on-task, comprehension in 5-second test, conversion delta, a11y audit pass}
- Slop check: passes `scripts/slop_lint.py` with grade A/B and the human review in `references/review-checklist.md`.

## 8. Open questions & assumptions

| # | Question | Assumption if unanswered | Risk if wrong | Owner |
|---|---|---|---|---|
| 1 | | | | |
