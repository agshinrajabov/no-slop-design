# Eval 02 — Feature inside an existing design system (Operate mode)

## Setup

A repo with: `tailwind.config.js` extending colors (`brand.500 = #2563eb`, gray scale), `components/ui/` with
shadcn Button/Input/Card/Dialog lightly themed, `Inter` loaded via `next/font`, an `app/(dashboard)/` with a
sidebar layout, no `DESIGN.md`, no tokens file. (Create this fixture or point at a comparable real project.)

## Prompt

> Add a "Team members" settings page: list members with role, invite by email, change role, remove member. Match
> our existing UI.

## Expected behaviour

Phase 0 detection finds the implicit system (level 1–2), extracts tokens and conventions, adopts them; short
brief; 30-minute research on the job (invite/role/remove flows in comparable products); composition in Operate
mode; build with existing components; review; a short system-notes section. It must **not** introduce a new
typeface, a new primary, a new radius scale, or a second icon set, even though Inter and blue are on the watch list.

## Rubric (0 / 1 / 2 each)

1. Detected the existing system and stated its maturity level; listed what was found (fonts, colors, radius, components, icon set).
2. Kept Inter and `brand.500`; documented the tension with the anti-slop list instead of "fixing" the brand.
3. Extracted tokens into `tokens/` mirroring the existing names (or aliased to them) and wrote a `DESIGN.md` addendum separating documented / observed / proposed.
4. Reused existing Button/Input/Dialog; any new component has a written justification.
5. Research: job stories for admin inviting/removing; competitor flows (3+) with step counts; decision on invite UX (single email vs bulk; pending state; resend).
6. Layout: workspace-first, table/list with text left / status aligned / `tabular-nums` for dates; no KPI cards; no card-in-card; density matches existing screens.
7. Full state matrix: empty (no members yet), loading skeleton matching row shapes, error, pending invite, last-owner-cannot-be-removed, offline; remove = confirmation or undo; role change = immediate with feedback.
8. Accessibility: visible labels, `autocomplete="email"`, inline validation on blur, focus management in the invite dialog, row actions keyboard-reachable, 24px+ targets.
9. Copy: "Invite member", "Remove {name}?" with specific buttons; errors say what to do; no "Oops"; matches existing string tone.
10. No literal values in the new code; uses the extracted tokens/utilities only.
11. Drift audit reported (raw values, off-scale spacing, duplicate components, slop grade of existing UI) without unrequested fixes.
12. Review gate run; grades reported; `slop_lint.py` on the new files A/B with annotations for inherited tells (Inter, blue) marked "brand constraint".
13. Final message: what was built, what was reused, what was added and why, drift findings as recommendations.

Max 26. Pass ≥ 21 with items 2, 4, and 10 at 2.
