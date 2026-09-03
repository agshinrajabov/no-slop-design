# Working Inside an Existing Design System

When a company or person already has a design system, brand guide, token file, Figma library, Tailwind config, or
even just a consistent codebase, the job is **not** to design something new. It is to detect the system, adopt it
faithfully, extend it only where it has a gap, and leave it healthier. Introducing a second visual language into a
product is a slop pattern of its own ("this screen was clearly made by someone else").

## Contents

1. Detection: find what exists
2. Classify the system's maturity
3. Extraction: build the working token set from what you find
4. Adoption rules
5. Extending without breaking
6. When the system is bad
7. Drift audit
8. Deliverables when a system exists
9. Checklist

---

## 1. Detection: find what exists

Run before any design work. Check, in order:

| Where | What to look for | Command / method |
|---|---|---|
| Repo root | `DESIGN.md`, `design/`, `brand/`, `tokens/`, `*.tokens.json`, `style-dictionary.config.*`, `tokens-studio` files | `ls`, `find . -maxdepth 3 -iname "*token*"` |
| CSS | `:root { --… }` custom properties, `@theme` (Tailwind v4), `theme.extend` in `tailwind.config.*`, SCSS `$variables`, CSS-in-JS theme objects, `panda.config`, `stitches.config`, `vanilla-extract` themes | `grep -rn "^\s*--" --include=*.css | head`, `grep -rn "@theme"` |
| Component library | `components/ui/` (shadcn), `packages/ui`, Storybook (`.storybook/`), MUI/Chakra/Mantine/Ant theme providers | look for `ThemeProvider`, `createTheme`, `extendTheme` |
| Native | iOS: `Assets.xcassets` color sets, `Color+Extensions.swift`, `Font+…`, `DesignTokens.swift`; Android: `res/values/colors.xml`, `themes.xml`, `Theme.kt`, `Color.kt`, `Type.kt`; Flutter: `ThemeData`, `ThemeExtension`, `app_colors.dart` | `find . -name "*.xcassets"`, `grep -rn "lightColorScheme\|ThemeData("` |
| Figma | Libraries, Variables collections, Styles, a "Foundations" page | Figma MCP `get_variable_defs`, `get_libraries`, `search_design_system` if available; otherwise ask for the file link |
| Docs | Brand book PDF, Notion/Confluence "design system" pages, logo files, typography licences | ask the user; read fully before designing |
| The live product | Fonts, palette, radius, spacing, density, iconography actually shipped | screenshot and inspect (browser tool); count unique values |

Also read the last 20 commits touching UI and any `CONTRIBUTING`/`README` sections on styling. Ask the user one
question if the picture is unclear: "Is there a design system or brand guide I should follow? Where does it live?"

## 2. Classify the system's maturity

| Level | Signs | Your posture |
|---|---|---|
| **0 — None** | inline values everywhere, 3+ fonts, 40+ unique colors, no docs | Build a new system (`design-tokens.md`, `moodboard.md`), but first extract *implied* preferences from the best existing screens |
| **1 — Implicit** | consistent codebase but no tokens/docs; or a brand guide (logo, colors, font) without UI rules | Reverse-engineer tokens from the code and brand guide; write `DESIGN.md`; do not change the look |
| **2 — Partial** | tokens exist for some categories (colors, spacing) but not others (motion, elevation, typography roles); a Figma library without code parity | Fill gaps in the same naming style; reconcile Figma and code, code wins for values unless told otherwise |
| **3 — Complete** | documented tokens with tiers, component library with states, content guide, versioned | Use only what exists; propose additions through the system's own process (new token PR, component RFC) |

## 3. Extraction: build the working token set from what you find

Goal: a `tokens/` folder (DTCG) that mirrors the existing system so the pipeline in `design-tokens.md` works, even
if the source of truth stays elsewhere.

1. **Colors:** collect every unique color in CSS/theme files and the live product. Cluster near-duplicates (ΔE < 2 in
   OKLCH → same token). Map to the system's names if they exist; otherwise name by role you *observe* (`text.primary`
   is whatever the body text color is). Note light/dark pairs.
2. **Typography:** families actually loaded (network tab / `@font-face`), weights used, size steps used (count
   occurrences; the top 6–8 are the real scale), line-heights.
3. **Spacing:** histogram of paddings/gaps/margins; the base unit is the GCD of the top values (usually 4 or 8).
   Values off the grid are drift, not tokens.
4. **Radius, borders, shadows:** unique values; establish which are hierarchy and which are accidents.
5. **Motion:** durations and easings used; often absent → propose defaults in the system's spirit.
6. **Components:** inventory of existing components with their states coverage (default/hover/focus/active/disabled/
   loading/error/empty). Missing states are gaps to fill, not reasons to build new components.
7. **Voice:** collect 20 strings from the product (buttons, errors, empty states). Match their case, length, tone.
8. **Iconography:** which set, stroke, size grid.

Write the result to `DESIGN.md` under "Observed system (extracted {date})", clearly separating **documented** rules
from **observed** conventions from **your proposals**.

## 4. Adoption rules

- **Use the system's names.** If they call it `brand-primary`, don't introduce `action.primary` in code; alias in
  your tokens file so `build_tokens.py` can emit their names.
- **Use their components before inventing.** A new component needs a written reason ("no existing component covers
  a 3-state selection with a hint").
- **Match density and radius exactly.** These are the first things that betray a foreign screen.
- **Match the typographic scale.** Never add a new size step; choose the nearest existing one.
- **Keep their icon family.** One outlier icon set is instantly visible.
- **Match voice.** Read their strings before writing yours.
- **Respect the brand's own constraints** even when they conflict with this skill's defaults (e.g. their brand face
  is Inter → use Inter, well; their primary is purple → use it, without the gradient).
- **Platform beats system** on native: if the system's web button contradicts iOS conventions, follow HIG and
  document the deviation.

## 5. Extending without breaking

When a real gap exists:

1. Confirm it is a gap, not ignorance: search the system docs and code twice.
2. Extend at the **lowest tier necessary**: a new semantic alias over an existing primitive beats a new primitive; a
   new variant beats a new component.
3. Follow the existing **naming grammar** exactly (case, separators, order of namespace/category/property/modifier).
4. Provide **light and dark** (and any other modes the system has) for every new token.
5. Add the new item to the system's docs/Storybook/Figma, not only to your screen.
6. Mark additions in `DESIGN.md` changelog with rationale, so the system owner can accept or reject.
7. Never fork a component locally with tweaks ("Button2"). Propose the change upstream or use the original.

## 6. When the system is bad

Sometimes the existing system is inconsistent, inaccessible, or itself slop (purple gradient primary, Inter by
reflex, 24px radius everywhere). Options, in order of preference:

1. **Fix inside the system:** raise contrast on the existing roles, tighten the radius scale, add missing states.
   These are improvements, not a new look.
2. **Propose a scoped evolution:** a `DESIGN.md` section "Proposed evolution" with before/after tokens and reasons,
   applied to one flow as a pilot, with the user's decision recorded.
3. **Rebrand** only when the brief asks for it. Then run the full new-system path (`moodboard.md`), and plan
   migration (token aliases from old names to new so code can move gradually).

Never silently mix: a screen that is "70% their system, 30% my taste" is worse than either.

## 7. Drift audit

Existing systems drift. Quick audit (30 min) that produces value even when you were only asked for one screen:

| Check | Method | Report as |
|---|---|---|
| Raw values in components | `grep -rnE "#[0-9a-fA-F]{3,8}\b|[0-9]+px" src/components | grep -v tokens` | count + top offenders |
| Off-scale spacing | histogram vs the base unit | list of values |
| Font count | `@font-face` + computed styles | families × weights loaded vs used |
| Unique colors in the live product | screenshot palette extraction or computed styles | number (>24 non-gray = drift) |
| Contrast failures | `scripts/contrast.py --pairs` on semantic roles | failing pairs |
| Component duplicates | `Button`, `Btn`, `PrimaryButton`… | list |
| Slop tells | `scripts/slop_lint.py src/` | grade + top rules |
| Figma ↔ code parity | compare variables to CSS vars | mismatched names/values |

Fix drift only when asked, or when it blocks the current work; otherwise report it.

## 8. Deliverables when a system exists

- `DESIGN.md` with the observed/documented/proposed split (or an addendum to their existing doc).
- `tokens/` mirroring their names (+ `build/` outputs) if they lack a pipeline; otherwise use theirs.
- Screens/components built **only** from their tokens and components, with any additions listed.
- A short "System notes" section in the handoff: gaps found, additions made, drift observed, recommendations.

## 9. Checklist

- [ ] Searched repo, native asset catalogs, Figma, docs, and the live product for an existing system.
- [ ] Maturity level stated (0–3) and posture chosen accordingly.
- [ ] Tokens extracted and named in the system's grammar; documented vs observed vs proposed separated.
- [ ] No new font, primary color, radius scale, or icon set introduced without a brief-level reason.
- [ ] All new tokens have every mode the system supports.
- [ ] Existing components reused; each new component has a written justification.
- [ ] Voice matched to existing strings.
- [ ] Platform conventions kept on native even where the web system differs; deviations documented.
- [ ] Drift audit run and reported; fixes only where in scope.
- [ ] Additions recorded in the system's own docs/Figma/Storybook and in the `DESIGN.md` changelog.
