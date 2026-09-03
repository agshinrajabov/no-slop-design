# Design Tokens

Everything visual is a token; nothing visual is a literal. Tokens are the mechanism that makes a design system
portable across web, iOS, Android, Flutter and Figma, makes dark mode and theming cheap, and makes slop detectable
(an inline `#7c3aed` is a lint error). This file defines the format, the tiers, the naming grammar, the mode
strategy, and the build pipeline (`scripts/build_tokens.py`).

## Contents

1. Format: W3C DTCG
2. Tiers: primitive → semantic → component
3. Naming grammar
4. Modes and themes
5. File layout
6. Token categories and required minimums
7. Build pipeline and platform outputs
8. Tailwind v4, Figma Variables, Style Dictionary interop
9. Governance: adding, deprecating, versioning
10. Anti-patterns

---

## 1. Format: W3C DTCG

Use the Design Tokens Community Group format (stable "2025.10" module). Rules that matter:

- A token is an object with `$value` (required) and `$type`. Any object without `$value` is a group. `$type` on a
  group is inherited by its children. `$description`, `$deprecated`, `$extensions` are optional.
- Aliases: `"$value": "{color.brand.9}"`. Resolve recursively; circular references are errors.
- Types: `color`, `dimension`, `fontFamily`, `fontWeight`, `duration`, `cubicBezier`, `number`, and composites
  `shadow`, `typography`, `border`, `transition`, `gradient`, `strokeStyle`.
- 2025.10 value shapes: color may be an object `{"colorSpace":"oklch","components":[0.58,0.17,40],"alpha":1,"hex":"#c8552d"}`;
  dimension may be `{"value":16,"unit":"px"}`. Our build script accepts both object and legacy string forms
  (`"#c8552d"`, `"oklch(0.58 0.17 40)"`, `"16px"`). Prefer strings for readability unless a downstream tool needs objects.
- File extension `.tokens.json` or `.json`; one group of concerns per file.
- Modes/themes: the DTCG "resolver" module is still a draft. Use the file-suffix convention below (`*.dark.json`)
  and keep it trivially convertible.

## 2. Tiers

| Tier | Purpose | Named by | Example | Used in UI code? |
|---|---|---|---|---|
| **Primitive** (global, option) | the palette of raw choices | appearance | `color.neutral.9`, `space.4`, `font.family.text`, `radius.3` | **never** |
| **Semantic** (alias, decision) | roles that carry meaning | role/intent | `color.text.primary`, `color.surface.raised`, `space.inset.md`, `radius.control` | yes — the default |
| **Component** | per-component overrides when semantics aren't enough | component.part.property.state | `button.primary.bg.hover`, `input.border.error` | yes, inside that component |

Rules: semantic aliases primitive (never another semantic); component aliases semantic (may alias primitive only
with a comment). Max chain depth 3. A rebrand changes primitives and a handful of semantic mappings; components
don't move.

Why: `text.secondary` survives a rebrand; `gray-600` doesn't. Slop UIs use primitives directly (`text-gray-500`)
which is why they can't be re-themed and why dark mode is an afterthought.

## 3. Naming grammar

`[namespace.] category . (concept .) property . (variant .) (state .) (scale)` — lowercase, dot-separated in
JSON, hyphen-joined in CSS. Two to four levels for most tokens.

| Segment | Values |
|---|---|
| category | `color`, `space`, `size`, `radius`, `border`, `shadow`, `font`, `typography`, `duration`, `ease`, `opacity`, `z`, `breakpoint` |
| concept (color) | `surface`, `text`, `border`, `action`, `status`, `focus`, `selection`, `scrim`, `skeleton`, `chart` |
| property / role | `primary`, `secondary`, `tertiary`, `inverse`, `on-action`, `raised`, `sunken`, `overlay`, `subtle`, `strong`, `success`, `warning`, `danger`, `info` |
| state | `hover`, `pressed`, `focus`, `disabled`, `selected`, `visited` |
| scale | `xs sm md lg xl` or numeric `1..12` / `50..950` |

Examples: `color.text.primary`, `color.action.primary.hover`, `color.status.danger.surface`, `space.inset.md`,
`space.stack.lg`, `size.control.md`, `radius.card`, `shadow.overlay`, `typography.body`, `duration.fast`, `ease.decelerate`.

Never encode a value in a name (`blue-600` is fine as a *primitive*; `text-blue` as a semantic is wrong). Never
encode a location (`homepage-hero-color`). Keep one grammar across web and native; the build script converts to
`--color-text-primary`, `colorTextPrimary`, `color_text_primary` as needed.

## 4. Modes and themes

A **mode** changes semantic values, not names: light/dark, high-contrast, density (comfortable/compact), brand
(multi-tenant), platform (rare). Implement as override files: `semantic.dark.json` contains only the tokens that
differ. Rules:

- Every semantic color token has a value in every color mode. The build fails otherwise.
- Dark is a separate palette (see `color.md`), not an inversion.
- Density modes change `space.*` semantic aliases and `size.control.*`, never primitives.
- High-contrast mode raises `border.*` and `text.secondary` to stronger steps and thickens focus.
- On the web, emit both `[data-theme="dark"]` (explicit choice) and `@media (prefers-color-scheme: dark)` guarded by
  `:root:not([data-theme="light"])` (system default). The script does this.

## 5. File layout

```
tokens/
  primitives.json        # color scales, space scale, size scale, radius, font families/weights, durations, easings, z, breakpoints
  semantic.json          # roles for light (default) mode
  semantic.dark.json     # dark overrides
  semantic.compact.json  # density overrides (optional)
  components.json        # component tokens (optional, grows with the library)
build/                   # generated, never edited: tokens.css, theme.css, DesignTokens.swift, DesignTokens.kt, design_tokens.dart, tokens.flat.json
design/
  DESIGN.md              # the why (templates/DESIGN.md)
  contrast-pairs.txt     # fg bg label — checked in CI
  design-log.json        # decisions + anti-convergence record
```

Templates for all of these are in `templates/tokens/`.

## 6. Token categories and required minimums

A system is not usable until each category has at least this:

| Category | Minimum | Notes |
|---|---|---|
| color primitives | neutral 12 steps · brand 12 · status ×4 (12 each or 5) | OKLCH; neutrals tinted |
| color semantic | surfaces 5 · text 8 · border 3 · action 3×3 states · status 4×4 · focus · selection · scrim · skeleton | light + dark |
| space | `space.0..24` on 4px base (0 2 4 6 8 12 16 20 24 32 40 48 64 80 96 128) + semantic `inset.{xs..xl}`, `stack.{…}`, `inline.{…}`, `gutter`, `margin.page` | |
| size | `control.{sm,md,lg}` = 32/40/48 · `icon.{sm,md,lg}` = 16/20/24 · `target.min` = 44 · `content.max` (e.g. 1200) · `measure.max` (65ch) | |
| radius | `none 0 · control 6 · card 12 · sheet 20 · pill 9999` (values per direction) | nested inner = outer − padding |
| border | `width.{hairline 1, strong 2}` | |
| shadow | `raised · overlay · modal` (light); dark uses surface steps | tokens may be lists |
| font | `family.{display,text,mono}` · `weight.{regular,medium,semibold,bold}` (only loaded ones) | |
| typography (composite) | `display h1 h2 h3 h4 body-lg body body-sm label caption code` | size, lh, weight, family, tracking |
| duration | `instant 80 · fast 120 · base 200 · slow 320 · slower 480` | |
| ease | `standard · decelerate · accelerate · emphasized` | cubicBezier |
| opacity | `disabled 0.4 · overlay 0.6 · skeleton 0.12` | |
| z | `base 0 · raised 10 · sticky 100 · overlay 1000 · modal 1100 · toast 1200` | |
| breakpoint | content-driven, named by layout change (e.g. `narrow 600 · regular 905 · wide 1240 · max 1440`) | |

## 7. Build pipeline and platform outputs

```bash
python3 scripts/build_tokens.py tokens/*.json --check        # validate, list unresolved aliases and untyped tokens
python3 scripts/build_tokens.py tokens/*.json --out build/    # css, tailwind, swift, kotlin, dart, flat-json
```

| Output | Consumer | Notes |
|---|---|---|
| `build/tokens.css` | any web stack | `:root` vars + `[data-theme="dark"]` + media-query block; composite typography expanded to `--typography-body-size/-lh/-weight/-family/-tracking` |
| `build/theme.css` | Tailwind v4 | `@theme { --color-… --spacing-… --font-… --radius-… --shadow-… --ease-… }` so utilities like `bg-surface-raised`, `text-text-primary`, `p-4`, `rounded-card` exist |
| `build/DesignTokens.swift` | SwiftUI | `enum DesignTokens` with `Color` (dynamic light/dark via UIColor provider), `CGFloat` dimensions, `Font.Weight` |
| `build/DesignTokens.kt` | Compose | `object DesignTokens` with `Color`, `.dp`, floats; feed into `MaterialTheme` + a `LocalDesignTokens` CompositionLocal |
| `build/design_tokens.dart` | Flutter | `abstract final class DesignTokens` with `Color`, doubles; wrap in a `ThemeExtension` |
| `build/tokens.flat.json` | Figma plugins, docs, tests | fully resolved per mode |

The script is stdlib-only and intentionally simple; for large systems switch to Style Dictionary v5 (which reads the
same DTCG files) and keep the file layout.

Wire-up on the web: components reference **only** `var(--color-…)`/`var(--space-…)` (or the Tailwind utilities
generated from them). Lint with `scripts/slop_lint.py` and a grep for raw hex/px in component files.

## 8. Interop

**Tailwind v4:** `@theme` namespaces map to utilities: `--color-*` → `bg-/text-/border-*`; `--spacing-*` → `p-/m-/gap-*`;
`--font-*` → `font-*`; `--text-*` → `text-*` sizes; `--radius-*` → `rounded-*`; `--shadow-*`; `--ease-*`;
`--animate-*`; `--breakpoint-*`. Wipe defaults with `--color-*: initial;` at the top of `@theme` so Tailwind's
blue-500 cannot leak in. Use `@theme inline` when a theme var references another var (needed for `light-dark()` or
`[data-theme]` switching).

**Figma Variables:** collections = tiers (Primitives, Semantic, Components); modes = light/dark (and density); semantic
variables alias primitives across collections. Import/export DTCG via Figma's native import or Tokens Studio. Naming
`color/text/primary` (slash) in Figma ↔ `color.text.primary` in JSON. Code is the source of truth for values; Figma
is the design workspace. If the Figma MCP is available, push `tokens.flat.json` as variables and bind components.

**Style Dictionary v5:** reads DTCG natively; use when you need iOS asset catalogs, Android XML resources, SCSS maps,
or custom transforms. Keep `tokens/` as the single source; SD replaces `build_tokens.py`, not the files.

**shadcn/ui / Radix themes:** regenerate *every* CSS variable from the semantic tokens (`--background`, `--foreground`,
`--primary`, `--ring`, `--radius`, …) so nothing of the default theme remains. Map `--radius` to `radius.control` and
override component classes that hard-code `rounded-xl`/`shadow-sm`.

## 9. Governance

- **Adding:** a new semantic token needs a role name, light+dark values, a contrast check if text/border, and a line
  in `DESIGN.md`. A new primitive needs proof that no existing step works.
- **Deprecating:** set `"$deprecated": "use color.text.secondary"`; keep for one minor version; the build prints
  deprecations.
- **Versioning:** semver for the token package. Value change of a semantic token = minor; rename/remove = major;
  new token = minor; primitive-only tweak that doesn't change any semantic output = patch.
- **Ownership:** `DESIGN.md` lists an owner; changes go through review like code.
- **Testing:** `--check` in CI; `contrast.py --pairs design/contrast-pairs.txt` in CI; snapshot `tokens.flat.json`
  so unintended value changes show up in diffs.

## 10. Anti-patterns

- Primitives in UI code (`text-gray-500`, `#111`, `Colors.blue`).
- Semantic tokens named by value (`color.text.blue`) or by location (`color.header.bg`).
- Alias chains deeper than 3, or semantics aliasing semantics in loops.
- Dark mode generated by inverting lightness.
- A "primary" that exists only as a single hex with no scale (no hover/pressed/surface variants).
- Tokens without `$type`, without descriptions on non-obvious ones, or with arbitrary values off the 4px grid.
- Two grammars in one system (`btnPrimaryBg` next to `color.action.primary`).
- Tokens for one platform only (web vars with no Swift/Kotlin output) when the product is multi-platform.
- Editing `build/` by hand.
