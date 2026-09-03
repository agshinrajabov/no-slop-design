# Android (Material 3 / Material 3 Expressive) — platform reference

Purpose: give an agent the numbers, tokens and component decisions needed to produce an Android app that is recognisably Material 3 (2021) or Material 3 Expressive (May 2025, shipped with Android 16) while carrying a brand, and to map DTCG tokens from `design-tokens.md` into Jetpack Compose, XML Views, Flutter and React Native. Android-agnostic color math is in `color.md`, type rules in `typography.md`, contrast in `accessibility.md`, motion principles in `motion.md`, generic tells in `anti-slop.md`. iOS rules are in `mobile-ios.md`; the cross-platform section at the end of this file covers keeping both platforms native from one token set.

## Contents

1. Material 3 vs Material 3 Expressive
2. Layout numbers, targets, shape, elevation
3. Type scale
4. Color: roles, tonal palettes, dynamic color
5. Navigation
6. Components: system vs custom
7. Motion tokens
8. Token mapping (DTCG to Compose, XML)
9. Cross-platform: Flutter and React Native
10. Android-specific slop
11. Review checklist
12. Sources

## 1. Material 3 vs Material 3 Expressive

Expressive is an extension of M3, not a replacement: same color roles, same type tokens, same layout grid. It adds shape, motion and emphasis tools plus new components. Compose Material 3 1.4.0 (stable 24 Sept 2025, BOM 2025.12.00 and later) ships the APIs; `MaterialExpressiveTheme` opts in.

| Area | M3 (2021–2024) | M3 Expressive (2025+) | Agent action |
|---|---|---|---|
| Shape | 7-step corner scale, static | 10-step corner scale (adds large-increased 20, extra-large-increased 32, extra-extra-large 48) + 35-shape `MaterialShapes` library + shape morphing between states | Morph selected/pressed states of FAB, chips, avatars; keep containers on the corner scale |
| Motion | Duration + easing tokens | Physics springs: `MotionScheme` with spatial × effects specs, each in fast/default/slow; `standard()` and `expressive()` schemes | Use `MaterialTheme.motionScheme.defaultSpatialSpec()` for bounds/position; `defaultEffectsSpec()` for color/alpha |
| Type | 15 styles | Same 15 + emphasized variants (`bodyLargeEmphasized`, `headlineMediumEmphasized`…) with heavier weight | Emphasized only for one focal element per screen |
| Buttons | 1 height (40dp), 5 styles | 5 sizes (XS 32, S 40, M 56, L 96, XL 136dp), round vs square shape, `ButtonGroup` (connected/standard), `SplitButton`, toggle buttons | Default S 40 for lists, M 56 for primary CTA |
| FAB | FAB 56, small 40, large 96, extended | Adds medium 80, `FloatingActionButtonMenu`, `FloatingToolbar` (docked/floating, horizontal/vertical) | One FAB or one toolbar per screen, never both |
| Progress | Linear / circular indicators | `LoadingIndicator` (morphing shapes) for indeterminate; wavy determinate indicators | Loading indicator ≤ 48dp; determinate stays linear/circular |
| App bars | Small/medium/large top app bar | Flexible top app bars, `NavigationBar` short (64dp) and tall (80dp) | Short nav bar on phones with ≤4 destinations |
| Navigation | Bar 80dp, rail 80dp wide | Expanded navigation rail (collapsible to 220–360dp with labels) | Rail on ≥600dp width |
| Research | — | Google reports 46 studies, 18k+ participants; eye-tracking: key actions found up to 4× faster in expressive layouts; older users' comprehension parity | Use the emphasis tools, not novel layouts |

Caution: "expressive" is not "unfamiliar". The research gain came from stronger visual hierarchy (size, shape, color contrast of the primary action) inside conventional layouts. Moving the back affordance, inventing a navigation model or animating everything measured worse. Expressive budget per screen: one hero shape/size, one emphasized type style, one spring signature.

## 2. Layout numbers, targets, shape, elevation

| Rule | Value | Why / source |
|---|---|---|
| Design canvas | 360×800dp (compact); verify 412×915 (Pixel 8/9), 600 (small tablet), 840+ (expanded) | M3 window size classes: compact <600, medium 600–839, expanded ≥840 |
| Minimum touch target | 48×48dp; visual glyph may be 24dp inside it | M3 Accessibility, Android a11y scanner flags <48 |
| Spacing between targets | 8dp minimum | M3 |
| Screen margins | 16dp compact, 24dp medium/expanded | M3 Layout |
| Grid | 4dp base; 8dp for component spacing; 12/16/24/32 | M3 |
| Gutters | 16dp (compact), 24dp (≥600dp) | M3 responsive grid |
| Icon size | 24dp system icons; 20dp in dense controls; 18dp inside chips/buttons | M3 Icons |
| List item height | 56dp one-line, 72dp two-line, 88dp three-line | M3 Lists |
| Top app bar | 64dp small, 112 medium, 152 large | M3 Top app bar |
| Navigation bar | 80dp (tall), 64dp (short, Expressive) | M3 Navigation bar |
| Navigation rail | 80dp wide collapsed; 220–360 expanded | M3 Navigation rail |
| Bottom sheet | Top corners extra-large (28dp); drag handle 32×4dp, 22dp from top | M3 Bottom sheets |
| Dialog | Width 280–560dp, corner extra-large (28), padding 24dp | M3 Dialogs |
| Text field | 56dp height; label 12sp when floated | M3 Text fields |
| Snackbar | 48dp min height, 4–10 s, one action, bottom margin 16dp above nav bar | M3 Snackbar |
| Chips | 32dp height, 8dp corner (small), 16dp horizontal padding | M3 Chips |
| Card padding | 16dp; card grid gutter 8dp | M3 Cards |
| Divider | 1dp `outlineVariant` | M3 Divider |
| System bars | Edge-to-edge is mandatory at targetSdk 35+ (opt-out removed at 36); status bar ~24dp, gesture nav bar ~48dp (3-button) or ~24 (gesture) — read `WindowInsets`, never hardcode | Android 15/16 behaviour changes |

Shape scale (corner radius, dp):

| Token | Value | Typical use |
|---|---|---|
| none | 0 | Full-bleed media, banners |
| extra-small | 4 | Snackbars, tooltips, text field (top) |
| small | 8 | Chips, small cards, menus |
| medium | 12 | Cards, list containers |
| large | 16 | Cards (Expressive default), FAB, sheets on tablet |
| large-increased | 20 | Hero cards (Expressive) |
| extra-large | 28 | Dialogs, bottom sheets, large FAB |
| extra-large-increased | 32 | Expressive containers |
| extra-extra-large | 48 | XL buttons, hero containers |
| full | 50% | Buttons (M3 default pill), badges, sliders |

Elevation levels (M3): 0 → 0dp, 1 → 1dp, 2 → 3dp, 3 → 6dp, 4 → 8dp, 5 → 12dp. Shadows in light theme only for level ≥ 2 on floating elements (FAB, menus, dialogs). In dark theme depth is expressed through `surfaceContainer*` tones, not shadows; do not stack `shadowElevation` and `tonalElevation`.

## 3. Type scale

Sizes in sp; line height in sp; weight; tracking. Roboto / Roboto Flex is the reference face; Google Sans Flex in Expressive Google apps. Brand faces are allowed when loaded through `FontFamily` and mapped to these tokens.

| Token | Size/line | Weight | Tracking | Use |
|---|---|---|---|---|
| displayLarge | 57/64 | 400 | -0.25 | Hero numerals, splash headlines |
| displayMedium | 45/52 | 400 | 0 | |
| displaySmall | 36/44 | 400 | 0 | |
| headlineLarge | 32/40 | 400 | 0 | Screen headline (large app bar) |
| headlineMedium | 28/36 | 400 | 0 | |
| headlineSmall | 24/32 | 400 | 0 | Dialog title |
| titleLarge | 22/28 | 400 | 0 | Top app bar title, card title |
| titleMedium | 16/24 | 500 | 0.15 | List item headline, section title |
| titleSmall | 14/20 | 500 | 0.1 | Dense titles |
| bodyLarge | 16/24 | 400 | 0.5 | Primary reading text |
| bodyMedium | 14/20 | 400 | 0.25 | Default body, list supporting text |
| bodySmall | 12/16 | 400 | 0.4 | Captions, helper text |
| labelLarge | 14/20 | 500 | 0.1 | Buttons, tabs, nav labels |
| labelMedium | 12/16 | 500 | 0.5 | Chips, small buttons |
| labelSmall | 11/16 | 500 | 0.5 | Badges, timestamps; absolute floor |

| Rule | Value | Why / source |
|---|---|---|
| Body floor | 14sp; prefer 16sp for reading | M3; a11y scanner flags <12sp |
| Label floor | 11sp (labelSmall); nothing smaller | M3 |
| Units | sp for text, dp for everything else; never `fontSize = 16.dp` | Font scaling |
| Font scaling range | Users scale 85%–200% (Android 14+ non-linear scaling: large text grows less than small); layouts must survive 200% | Android 14 font scale changes |
| Emphasized (Expressive) | One per screen; weight bump (e.g. 400 → 500/600) via `*Emphasized` tokens | Hierarchy, not decoration |
| Custom font | `FontFamily(Font(R.font.brand_regular, FontWeight.Normal), …)` then `Typography(bodyLarge = TextStyle(fontFamily=brand, fontSize=16.sp, lineHeight=24.sp))` | Keep the token sizes; change only family |
| Line length | 40–60 characters on phones | Readability |
| All caps | Not in M3 (M2 did); buttons are sentence case | M3 Buttons |

## 4. Color: roles, tonal palettes, dynamic color

M3 color = 5 key colors (primary, secondary, tertiary, neutral, neutral-variant, plus error) each expanded into a 13-step tonal palette (tones 0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 95, 99, 100; HCT color space). Roles pick tones; contrast comes from tone distance: Δ40 ≈ 3:1, Δ50 ≈ 4.5:1.

| Role | Light tone | Dark tone | Use |
|---|---|---|---|
| primary / onPrimary | 40 / 100 | 80 / 20 | Filled button, FAB, active states |
| primaryContainer / onPrimaryContainer | 90 / 30 | 30 / 90 | Tonal button, selected chips, FAB (default) |
| secondary / onSecondary | 40 / 100 | 80 / 20 | Less prominent actions |
| secondaryContainer / onSecondaryContainer | 90 / 30 | 30 / 90 | Nav bar active indicator, filter chips |
| tertiary / tertiaryContainer | 40 / 90 | 80 / 30 | Accents, contrasting highlights |
| error / errorContainer | 40 / 90 | 80 / 30 | Validation, destructive |
| surface | 98 | 6 | Screen background |
| surfaceContainerLowest | 100 | 4 | Recessed |
| surfaceContainerLow | 96 | 10 | Cards at rest |
| surfaceContainer | 94 | 12 | Nav bar, sheets |
| surfaceContainerHigh | 92 | 17 | Menus, dialogs |
| surfaceContainerHighest | 90 | 22 | Text field fill, top-most containers |
| onSurface / onSurfaceVariant | 10 / 30 | 90 / 80 | Primary / secondary text |
| outline | 50 | 60 | Outlined button/field borders (3:1 vs surface) |
| outlineVariant | 80 | 30 | Dividers, decorative borders |
| inverseSurface / inverseOnSurface | 20 / 95 | 90 / 20 | Snackbar |
| surfaceTint | = primary | = primary | Tonal overlay (legacy) |

| Decision | Enable dynamic color (Material You) | Brand-locked scheme |
|---|---|---|
| App type | Utilities, system-adjacent tools, note/calendar/launcher, apps whose identity is content | Brands where color is the identity (banking, retail, media brands), apps with strict marketing consistency |
| Implementation | `if (Build.VERSION.SDK_INT >= 31) dynamicLightColorScheme(ctx) else lightColorScheme(…)` | `lightColorScheme(primary = …, …)` generated from the brand seed |
| Brand presence | Keep brand in icon, illustration, type and one fixed accent (`tertiary` or a custom role) | Full scheme |
| Fallback | Always ship a seed-generated static scheme for API <31 and for users who disable wallpaper colors | — |
| Content color | Never dynamic for data viz, status colors or brand marks | Same |

Generating from a brand seed: run the brand hex through Material Theme Builder (or `material-color-utilities` in the build) with scheme `TonalSpot` (default), `Vibrant` for saturated brands, `Neutral`/`Monochrome` for editorial; then override only where the generated primary drifts from the brand hex by more than a small ΔE and keep the overridden tone at 40 (light) / 80 (dark). Override rule: change a role, not an individual hex; check `onX` contrast after every override; write the final scheme as DTCG tokens (see 8). Do not override surfaces; brand surfaces in dark mode are where most contrast failures come from.

Dark theme: background `surface` at tone 6 (not #000000 unless OLED media app); containers step up 4→10→12→17→22; text `onSurface` tone 90 (not pure white); accent `primary` tone 80 (a lighter, less saturated version of the brand); error tone 80. Avoid saturated brand hues at tone 40 on dark surfaces.

## 5. Navigation

| Pattern | Use when | Numbers / API | Do not |
|---|---|---|---|
| Navigation bar | 3–5 top-level destinations, compact width | `NavigationBar` + `NavigationBarItem(icon, label)`; always show labels; active indicator pill 64×32dp in `secondaryContainer` | 2 or 6+ destinations; icons without labels; iOS-proportion tab bars |
| Navigation rail | Medium width (600–839dp), tablets, foldables | `NavigationRail` 80dp; optional FAB at top; `NavigationSuiteScaffold` switches bar/rail/drawer per size class | Bottom bar on a 10" tablet |
| Navigation drawer | Expanded width (≥840) or >5 destinations of secondary importance | `ModalNavigationDrawer` / `PermanentNavigationDrawer` 360dp wide | Hamburger as default on phones |
| Top app bar | Every screen except immersive | Small (64dp) default; center-aligned for root screens; medium/large for scrollable headers with `TopAppBarDefaults.exitUntilCollapsedScrollBehavior()`; up arrow (`Icons.AutoMirrored.Filled.ArrowBack`) never a chevron with text | "Back" text label next to the arrow (iOS idiom) |
| Back vs Up | System back = chronological (gesture/button); Up = hierarchical parent; they must agree for in-app navigation | Navigation Compose handles both; deep-link entry synthesizes back stack via `NavDeepLinkBuilder` | Up that exits the app; back that skips screens |
| Predictive back | Must be supported (default for targetSdk 36) | `android:enableOnBackInvokedCallback="true"`; Compose `PredictiveBackHandler` / `BackHandler`; Navigation Compose 2.8+ animates; custom sheets/drawers must handle `BackEventCompat.progress` | Overriding `onBackPressed()`; custom back stacks that ignore the gesture |
| Edge-to-edge | Always (enforced) | `enableEdgeToEdge()` in `onCreate`; `Scaffold(contentWindowInsets = ScaffoldDefaults.contentWindowInsets)`; apply `WindowInsets.safeDrawing` to floating elements; `imePadding()` for keyboard | Opaque status/nav bar colors; content hidden under 3-button nav |
| System bars | Transparent; icons auto light/dark via `isAppearanceLightStatusBars`; no `statusBarColor` | Contrast comes from your surface behind the bar | Brand-colored status bar |
| Sheets vs dialogs | Bottom sheet = multi-option, contextual, in-flow; dialog = interruptive confirmation, ≤2 actions, short text | `ModalBottomSheet` (28dp top corners); `AlertDialog` (280–560dp) | Dialogs for pickers/menus; sheets for a Yes/No |
| Tabs | Secondary navigation within a destination | `PrimaryTabRow` (≤5 fixed) / `SecondaryScrollableTabRow` | Tabs as top-level navigation instead of the nav bar |
| Deep links | Every destination reachable by URL | `navDeepLink { uriPattern = "app://x/{id}" }`; App Links verified | Deep links opening a modal over an empty root |
| Search | Root of browse destinations | `SearchBar` / `DockedSearchBar` (56dp, full corner); `expanded` state for suggestions | Text field styled as search |

## 6. Components: system vs custom

Use the Material component; adjust via theme (color scheme, shapes, typography, motion scheme), never by re-implementing.

| Component | Choice | Notes |
|---|---|---|
| Button hierarchy | Filled (1 per screen region) > Filled tonal > Elevated (only over patterned/photo backgrounds) > Outlined > Text | Height 40dp (S); primary CTA 56dp (M) in Expressive; label `labelLarge`, sentence case; icon 18dp with 8dp gap |
| Button group / split button | Expressive: `ButtonGroup` for 2–5 related actions or toggles; `SplitButton` for primary action + related menu | Replaces custom "pill row" toggles |
| FAB | Single most common constructive action on a screen (Compose, New, Add); `primaryContainer` default; 16dp from edges, above nav bar; `ExtendedFloatingActionButton` when the verb is unclear | Never for navigation or destructive actions; no gradient; no FAB on every screen |
| Chips | Assist (action from content), Filter (toggle, multi), Input (removable), Suggestion | 32dp; `FilterChip(selected)`; never as navigation |
| Cards | Elevated (over colored/photo bg), Filled (default, `surfaceContainerHighest`), Outlined (dense lists). Use a card only when the whole card is one tappable unit or a distinct object; lists of homogeneous rows use `ListItem` with dividers | No card-in-card; 16dp padding; corner medium 12 (M3) / large 16 (Expressive) |
| Lists | `ListItem(headlineContent, supportingContent, leadingContent, trailingContent)`; `HorizontalDivider` | 56/72/88dp; 3-line max |
| Text fields | Filled (default; dense forms, on `surface`) or Outlined (on colored/photo backgrounds, or when fields sit among cards); never mix in one form; `supportingText` for help, `isError` + error text (`bodySmall`, `error`) | 56dp; leading icon 24dp; trailing clear/visibility |
| Selection | Switch = instant on/off setting; Checkbox = multi-select in lists/forms with a submit; Radio = single choice from 2–5 visible options; Segmented button = 2–5 mutually exclusive views or short filters | Switch never needs a Save button; checkbox does |
| Dialogs | `AlertDialog(title, text, confirmButton, dismissButton)`; text buttons; max 2 actions, confirm on the right; full-screen dialog for create/edit flows | No custom dialog chrome; no three stacked buttons |
| Bottom sheets | Modal (`ModalBottomSheet`) for task/options; Standard (`BottomSheetScaffold`) for persistent secondary content | Drag handle visible; predictive back handled |
| Snackbar | `SnackbarHost` in `Scaffold`; one optional action; 4–10 s | No stacking; no snackbar for errors requiring a decision (use dialog) |
| Menus | `DropdownMenu` / `ExposedDropdownMenuBox`; 8dp corner; 48dp items | Never a bottom sheet for ≤5 items on tablets |
| Date / time | `DatePicker` (modal, or `DatePickerDialog`), `TimePicker` (dial) / `TimeInput` | No custom wheel pickers (iOS idiom) |
| Progress | `LinearProgressIndicator` / `CircularProgressIndicator`; Expressive `LoadingIndicator` for indeterminate ≤ 3 s waits; pull-to-refresh via `PullToRefreshBox` | No custom spinners |
| Badges | `Badge` on nav items / icons; 6dp dot or 16dp with number | Numbers ≤ 999+ |
| Sliders | `Slider` / `RangeSlider`; Expressive wide track with stop indicator | Custom sliders only for media scrubbing |
| Tooltips | `PlainTooltip` / `RichTooltip` via `TooltipBox` | No web hover cards |

Branded app rule: keep every component above; put the brand into the color scheme (seed + overrides), one custom shape family via `Shapes`, one display font in `displayLarge`–`headlineSmall`, custom icons drawn on the 24dp Material grid at 2dp stroke, and illustration in content. A custom component is justified only for domain objects Material has no equivalent for (a seat map, a waveform, a game board), and it still consumes `MaterialTheme` tokens and `MotionScheme`.

## 7. Motion tokens

Duration tokens (ms):

| Token group | Values | Use |
|---|---|---|
| short1–4 | 50, 100, 150, 200 | Selection, ripple, small fades, icon toggles |
| medium1–4 | 250, 300, 350, 400 | Bottom sheet, dialogs, expanding cards within a screen |
| long1–4 | 450, 500, 550, 600 | Full-screen transitions, container transform, large shared axis |
| extraLong1–4 | 700, 800, 900, 1000 | Ambient/hero only; avoid on user-blocking paths |

Easing tokens:

| Token | Curve | Pair with | Use |
|---|---|---|---|
| standard | cubic-bezier(0.2, 0, 0, 1) | medium2 (300) | Default for simple, small, in-place changes |
| standard-decelerate | (0, 0, 0, 1) | short4–medium1 | Elements entering the screen |
| standard-accelerate | (0.3, 0, 1, 1) | short3–short4 | Elements leaving |
| emphasized | piecewise: (0.05, 0.7, 0.1, 1) approximated | long2 (500) | Large, attention-worthy transitions (container transform, expanding FAB) |
| emphasized-decelerate | (0.05, 0.7, 0.1, 1) | medium4 (400) | Entering with emphasis |
| emphasized-accelerate | (0.3, 0, 0.8, 0.15) | short4 (200) | Exiting with emphasis |

Expressive springs (`MotionScheme`, Compose M3 1.4; verify against `MotionSchemeKeyTokens` for your version):

| Scheme | Spatial (bounds/position) fast / default / slow | Effects (color/alpha) fast / default / slow | When |
|---|---|---|---|
| `MotionScheme.standard()` | damping 0.9, stiffness 1400 / 700 / 300 | damping 1.0, stiffness 3800 / 1600 / 800 | Productivity, dense data, enterprise |
| `MotionScheme.expressive()` | damping 0.6, stiffness 800 / 0.8, 380 / 0.8, 200 | same as standard (no overshoot on color) | Consumer, media, social; hero moments only |

Rules: effects specs never overshoot (alpha/color bounce looks like flicker); spatial springs apply to size, offset, shape morph; use `animateFloatAsState(spec = MaterialTheme.motionScheme.fastSpatialSpec())` rather than literal `tween()`; respect `Settings.Global.ANIMATOR_DURATION_SCALE` = 0 (animations must be skippable) and `LocalReduceMotion`-style flags from `accessibility.md`.

Transition patterns:

| Pattern | Relationship | Implementation |
|---|---|---|
| Container transform | Parent element expands into child screen (card → detail, FAB → compose) | `SharedTransitionLayout` + `sharedBounds` (Compose 1.7+); long2 emphasized |
| Shared axis (X/Y/Z) | Spatial or sequential relationship (onboarding steps X, tabs X, parent-child Z) | `slideIntoContainer` + `fadeIn` in Navigation Compose `enterTransition`; medium3 |
| Fade through | Unrelated destinations (nav bar switches) | `fadeOut(short2)` then `fadeIn(medium1)` with 92% → 100% scale on incoming |
| Fade | Elements entering/exiting within bounds (snackbar, dialog scrim, FAB show/hide) | `AnimatedVisibility(fadeIn/fadeOut + scale)`; short4 |

## 8. Token mapping (DTCG to Compose, XML)

`build_tokens.py` emits `DesignTokens.kt` from the DTCG JSON in `design-tokens.md`. Material roles flow into `MaterialTheme`; anything outside M3's vocabulary (spacing scale, brand-only colors, radii aliases, durations) goes through a `CompositionLocal`.

```kotlin
// DesignTokens.kt (generated — do not edit)
object DT {
    object Space { val s1 = 4.dp; val s2 = 8.dp; val s3 = 12.dp; val s4 = 16.dp; val s6 = 24.dp; val s8 = 32.dp }
    object Radius { val sm = 8.dp; val md = 12.dp; val lg = 16.dp; val xl = 28.dp }
    object Brand { val accent = Color(0xFF2D6A4F); val accentDark = Color(0xFF95D5B2) }
    object Motion { const val short4 = 200; const val medium2 = 300; const val long2 = 500 }
}

@Immutable data class DesignTokens(val space: DT.Space = DT.Space, val radius: DT.Radius = DT.Radius, val brandAccent: Color)
val LocalDesignTokens = staticCompositionLocalOf<DesignTokens> { error("No DesignTokens provided") }
val MaterialTheme.tokens: DesignTokens @Composable @ReadOnlyComposable get() = LocalDesignTokens.current

@Composable fun AppTheme(dynamic: Boolean = false, dark: Boolean = isSystemInDarkTheme(), content: @Composable () -> Unit) {
    val ctx = LocalContext.current
    val scheme = when {
        dynamic && Build.VERSION.SDK_INT >= 31 -> if (dark) dynamicDarkColorScheme(ctx) else dynamicLightColorScheme(ctx)
        dark -> darkColorScheme(primary = Color(0xFF95D5B2), onPrimary = Color(0xFF00391F), /* … generated roles … */)
        else -> lightColorScheme(primary = Color(0xFF2D6A4F), onPrimary = Color.White, /* … */)
    }
    CompositionLocalProvider(LocalDesignTokens provides DesignTokens(brandAccent = if (dark) DT.Brand.accentDark else DT.Brand.accent)) {
        MaterialExpressiveTheme(colorScheme = scheme, typography = AppTypography, shapes = AppShapes,
            motionScheme = MotionScheme.expressive(), content = content)
    }
}
```

| DTCG token | Compose target | XML Views target | Rule |
|---|---|---|---|
| `color.sys.primary` etc. (M3 roles) | `lightColorScheme()/darkColorScheme()` args | `values/colors.xml` + `values-night/colors.xml`, `Theme.Material3.DayNight` attrs (`colorPrimary`, `colorSurfaceContainer`…) | One source: DTCG modes light/dark generate both files |
| `color.ref.*` tonal palette | Not referenced in UI code; only feeds roles | same | Palette steps never appear in composables |
| Brand-only colors | `LocalDesignTokens` | `colors.xml` with `brand_` prefix | Provide light and dark values |
| `dimension.space.*` | `DT.Space` (`Dp`) | `dimens.xml` (`@dimen/space_4`) | 4dp multiples |
| `dimension.radius.*` | `Shapes(extraSmall = RoundedCornerShape(4.dp), … extraLarge = 28.dp)` + `DT.Radius` | `ShapeAppearance.Material3.Corner.*` overlays | Map to the M3 shape scale first, custom aliases second |
| `typography.*` (family, size, line height, weight, tracking) | `Typography(bodyLarge = TextStyle(fontFamily, 16.sp, 24.sp, FontWeight.Normal, 0.5.sp))` | `TextAppearance.Material3.BodyLarge` overlays with `android:fontFamily`, `textSize` in sp | Sizes in sp; never dp |
| `duration.*` / `cubicBezier.*` | `DT.Motion` ints + `CubicBezierEasing(0.2f,0f,0f,1f)`; prefer `MotionScheme` specs | `@integer/motion_duration_medium2`, `@interpolator/m3_sys_motion_easing_standard` | Springs beat tweens in Expressive |
| `elevation.*` | `shadowElevation`/`tonalElevation` `Dp` | `app:elevation` | Levels 0/1/3/6/8/12 only |
| Font scale, contrast | Not tokens; read `LocalConfiguration.fontScale`, `UiModeManager.contrast` (API 34) | same | Test 200% and high-contrast |

## 9. Cross-platform: Flutter and React Native

One token file, two visual dialects. Share color math, type scale ratios and spacing; do not share navigation chrome, back behaviour or typeface defaults.

| Concern | iOS build | Android build |
|---|---|---|
| Top-level nav | Bottom tab bar (SF Symbols, 49pt content, floating glass on iOS 26) | `NavigationBar` 80/64dp with labels and active pill |
| Back | Swipe from left edge + top-left chevron | System back gesture/button + predictive back; Up arrow in app bar |
| Modal choice | Action sheet / medium-detent sheet | Bottom sheet / dialog |
| Body typeface | SF Pro 17pt | Roboto/Flex 14–16sp (or brand mapped to tokens) |
| Toggle | `UISwitch` proportions | M3 `Switch` with icon-in-thumb |
| Date picker | Wheel / inline calendar | M3 dialog calendar |
| Haptics | Impact/selection/notification generators | `HapticFeedbackConstants` (CONFIRM, REJECT, CLOCK_TICK, etc.), lighter usage |
| Fonts scaling | Dynamic Type text styles | sp + `fontScale` |

Flutter:

| Item | Implementation | Rule |
|---|---|---|
| Theme | `ThemeData(useMaterial3: true, colorScheme: ColorScheme.fromSeed(seedColor: brand, brightness: …), textTheme: …)`; `dynamic_color` package for Material You with a seed fallback | Generate `ColorScheme` once from DTCG, do not hand-pick per widget |
| Custom tokens | `class AppTokens extends ThemeExtension<AppTokens>` with `copyWith`/`lerp`; register in `ThemeData(extensions: [AppTokens.light])`; read via `Theme.of(context).extension<AppTokens>()!` | Spacing, radii, brand colors, durations live here |
| Generated file | `design_tokens.dart` from `build_tokens.py`: `abstract final class DT { static const space4 = 16.0; static const radiusMd = 12.0; static const brandAccent = Color(0xFF2D6A4F); }` | Views import `DT`, never literals |
| Per-platform widgets | `Theme.of(context).platform == TargetPlatform.iOS` → `CupertinoPageScaffold`/`CupertinoTabScaffold`, `CupertinoSwitch`, `showCupertinoModalPopup`; else Material. `Switch.adaptive`, `Slider.adaptive`, `CircularProgressIndicator.adaptive`, `showAdaptiveDialog` | One `AdaptiveScaffold` decision point, not per-screen `if`s |
| Navigation | `go_router` with `CupertinoPage` on iOS (swipe-back) and `MaterialPage` on Android; predictive back via `PopScope` (`canPop`, `onPopInvokedWithResult`) and `android:enableOnBackInvokedCallback` | Do not disable swipe-back with a custom `WillPopScope` |
| Edge-to-edge | `SystemChrome.setEnabledSystemUIMode(SystemUiMode.edgeToEdge)`, transparent `SystemUiOverlayStyle`, `SafeArea`/`MediaQuery.paddingOf` | Required for Android 15+ targets |
| M3 Expressive | Not implemented in the Flutter SDK as of 2026 (Flutter team stated it is not actively developing it); community packages (`material_3_expressive`, `m3e_design`) provide `ThemeExtension` tokens and components | Ship M3 (2023 tokens) as the baseline; add Expressive components only where a package is maintained |
| Text scaling | `MediaQuery.textScalerOf(context)`; never `textScaleFactor: 1.0` to "fix" layouts | Same 200% test |
| Fonts | `TextTheme` from tokens; `fontFamily` per platform via `Platform.isIOS ? '.SF Pro Text' : 'Roboto'` or the brand face for display only | iOS body stays SF unless brand face ships Dynamic Type |

React Native:

| Item | Implementation | Rule |
|---|---|---|
| Tokens | `design_tokens.ts` generated (`export const DT = { space: {...}, radius: {...}, color: { light: {...}, dark: {...} } } as const`); `ThemeProvider` via React context + `useColorScheme()`; `StyleSheet.create` consumes `DT`, no inline literals | One provider at root; hooks `useTheme()`/`useTokens()` |
| Platform split | `Platform.select({ ios: …, android: … })` for values; `.ios.tsx` / `.android.tsx` files for whole components (tab bar, header, switch) | Split at the component boundary, not in every style |
| Navigation | React Navigation native stack (`@react-navigation/native-stack`) for platform headers, swipe-back and predictive back (via `react-native-screens`); native bottom tabs (`react-native-bottom-tabs`) so iOS gets `UITabBarController` (Liquid Glass on iOS 26) and Android gets `BottomNavigationView` | JS-drawn tab bars lose glass, minimize-on-scroll and platform a11y |
| Edge-to-edge | RN 0.81+ targets Android 16 and is edge-to-edge by default; use `react-native-safe-area-context` (`useSafeAreaInsets`) and `react-native-edge-to-edge` for system bar style | No `StatusBar backgroundColor` |
| Typography | `fontSize` in unitless dp/pt with `allowFontScaling` left on; cap only decorative text with `maxFontSizeMultiplier`; `Platform.select` for family (`System` on iOS, `Roboto`/`sans-serif` on Android) | Never disable scaling app-wide |
| Motion | `react-native-reanimated` `withSpring({ damping, stiffness })` mirroring iOS springs / M3 `MotionScheme` per platform; `withTiming` + bezier only on Android for standard easing | Reduce Motion via `AccessibilityInfo.isReduceMotionEnabled()` |
| Components | `Switch`, `Pressable` with platform ripple (`android_ripple`), `ActionSheetIOS` / bottom sheet on Android, `DateTimePickerAndroid` vs `DatePickerIOS`-style modal | Don't ship an iOS-looking custom switch to Android or vice versa |
| Glass (iOS 26) | `expo-glass-effect` / `GlassView` only on floating chrome, same rules as `mobile-ios.md` §2; Android fallback = `surfaceContainer` | No blur views on Android as "glass" |

## 10. Android-specific slop

| Tell | Do instead |
|---|---|
| iOS chevron with "Back" text in the app bar | Material Up arrow, no label; rely on system back |
| Bottom tab bar with iOS proportions (49pt, no active pill, icon-only) | `NavigationBar` 80/64dp, labels always, `secondaryContainer` indicator |
| Ignoring predictive back (custom `onBackPressed`, JS back handlers that swallow the gesture) | `PredictiveBackHandler`/`BackHandler`, Navigation Compose transitions |
| Hamburger drawer by default on phones | Nav bar for 3–5 destinations; drawer only ≥840dp or for secondary sections |
| Gradient FAB / gradient buttons | `primaryContainer` FAB, filled button with scheme colors |
| Flat #121212 or #000 dark theme with shadows for depth | `surface` tone 6 with `surfaceContainer*` steps; no shadows |
| 5+ destinations in the nav bar, or 2 | 3–5; move extras to a Profile/More destination or drawer |
| Custom font sized in dp or scaling disabled | sp sizes mapped to type tokens; test 200% |
| Dialogs for everything (pickers, menus, filters) | Menus, bottom sheets, `DatePicker`; dialog only for interruptive confirmation |
| Emoji as icons | Material Symbols (outlined/rounded/sharp, one style per app) |
| Cards around every list row | `ListItem` + dividers; card only for discrete objects |
| iOS-style wheel pickers, grouped-inset settings look, iOS switches | M3 pickers, `ListItem` settings, M3 `Switch` |
| Opaque brand-colored status bar / nav bar | Transparent bars, edge-to-edge content, `surface` behind |
| Text buttons in ALL CAPS | Sentence case (`labelLarge`) |
| Snackbars stacking as a toast system | One `SnackbarHost`; errors needing decisions go to dialogs |
| Rounded 8dp on everything from a web system | M3 shape scale: pill buttons, 12–16 cards, 28 sheets/dialogs |
| Web hover/focus rings and cursor logic | Ripple (`indication = ripple()`), 48dp targets, focus handled by system |
| Full-bleed hero gradients with white display text on every screen | One display moment per flow; content on `surface` |
| Splash with animated logo | `SplashScreen` API (icon on `surface`, ≤ 1 s, no custom activity) |
| Toolbar + FAB + bottom bar all on one screen | One primary action affordance per screen |

## 11. Review checklist

1. Every interactive element has a 48×48dp touch target; adjacent targets ≥ 8dp apart.
2. Layout survives font scale 200% and display size "Largest" with no clipping or overlap.
3. All text sizes are in sp and mapped to type tokens; nothing below 11sp; body ≥ 14sp.
4. Colors come from `MaterialTheme.colorScheme` roles or `LocalDesignTokens`; no literal hex in composables.
5. `onX` on `X` contrast ≥ 4.5:1 for text, ≥ 3:1 for icons/borders, in both themes (see `accessibility.md`).
6. Dark theme uses `surface` tone 6 + `surfaceContainer*` steps; no shadow-based depth; accent at tone 80.
7. Dynamic color decision is explicit; a seed-generated static scheme exists for API <31 and for brand-locked mode.
8. Edge-to-edge enabled; system bars transparent; insets applied via `WindowInsets`/`Scaffold`; keyboard handled with `imePadding`.
9. Predictive back works on every screen, sheet and drawer (test with developer option "Predictive back animations").
10. Navigation bar has 3–5 labelled destinations; rail on ≥600dp; drawer only where justified.
11. Top app bar uses Up arrow without text; Up and Back are consistent; deep links synthesize the back stack.
12. One filled/primary button per screen region; button sizes from the M3/Expressive size set; sentence-case labels.
13. FAB (if any) is the single most common constructive action, `primaryContainer`, 16dp inset; no FAB+toolbar duplication.
14. Cards used only for discrete tappable objects; lists use `ListItem` with dividers; no card-in-card.
15. Text fields are all filled or all outlined within a form; errors use `isError` + supporting text.
16. Switch vs checkbox vs radio vs segmented chosen per the selection rules.
17. Bottom sheets have drag handles, 28dp top corners, and handle back; dialogs are ≤2 actions.
18. Snackbar via a single `SnackbarHost`; no toast stacks.
19. Shapes come from the M3 shape scale; Expressive morphs limited to FAB/chips/avatars/selection.
20. Motion uses duration/easing tokens or `MotionScheme` springs; effects specs never overshoot; animations skippable at scale 0.
21. Container transform / shared axis / fade through chosen by relationship, not by preference.
22. At most one emphasized type style, one hero shape and one spring signature per screen.
23. Icons are Material Symbols in one style; custom icons on the 24dp grid, 2dp stroke.
24. TalkBack: every icon button has `contentDescription`; decorative images pass `null`; focus order is logical; state (`selected`, `checked`) exposed.
25. Splash uses the `SplashScreen` API; no custom splash activity.
26. Tablet/foldable: `NavigationSuiteScaffold` or explicit size-class layouts; verified at 600 and 840dp.
27. Flutter/RN builds: iOS gets iOS chrome, Android gets Material chrome, from one token file.
28. Tokens consumed from generated `DesignTokens.kt` / `design_tokens.dart` / `design_tokens.ts`; DTCG JSON is the only hand-edited source.
29. Screenshots for Play use real data, `surface` backgrounds, default font scale.
30. A screenshot of the content reads as the brand; a screenshot of the chrome reads as Android.

## 12. Sources

- Material 3 Expressive overview and research figures: https://m3.material.io/blog/building-with-m3-expressive , https://design.google/library/expressive-material-design-google-research
- Material 3 Expressive shape library and shape morph: https://m3.material.io/styles/shape/shape-morph , https://m3.material.io/styles/shape/corner-radius-scale
- Material 3 motion tokens (duration, easing): https://m3.material.io/styles/motion/easing-and-duration/tokens-specs
- Material 3 motion physics / MotionScheme (Compose): https://m3.material.io/styles/motion/overview , https://developer.android.com/reference/kotlin/androidx/compose/material3/MotionScheme
- Compose Material 3 releases (1.4.0 stable, 24 Sept 2025; December '25 BOM): https://developer.android.com/jetpack/androidx/releases/compose-material3 , https://android-developers.googleblog.com/2025/12/whats-new-in-jetpack-compose-december.html
- Material 3 in Compose (theming, dynamic color): https://developer.android.com/develop/ui/compose/designsystems/material3
- Material 3 type scale tokens: https://m3.material.io/styles/typography/type-scale-tokens
- Material 3 color roles and tonal palettes: https://m3.material.io/styles/color/roles , https://m3.material.io/styles/color/system/how-the-system-works
- Material 3 layout, accessibility targets: https://m3.material.io/foundations/layout/applying-layout/window-size-classes , https://m3.material.io/foundations/accessible-design/accessibility-basics
- Material 3 navigation bar / rail / drawer: https://m3.material.io/components/navigation-bar/guidelines , https://m3.material.io/components/navigation-rail/guidelines
- Android 15 edge-to-edge and Android 16 behaviour changes (opt-out removed, predictive back default): https://developer.android.com/about/versions/15/behavior-changes-15 , https://developer.android.com/about/versions/16/behavior-changes-16
- Predictive back: https://developer.android.com/guide/navigation/custom-back/predictive-back-gesture
- Android 14 non-linear font scaling: https://developer.android.com/about/versions/14/features#non-linear-font-scaling
- Material Theme Builder / material-color-utilities: https://material-foundation.github.io/material-theme-builder/ , https://github.com/material-foundation/material-color-utilities
- Flutter Material 3 and Expressive status: https://docs.flutter.dev/ui/design/material , https://github.com/flutter/flutter/issues/168813
- Flutter ThemeExtension: https://api.flutter.dev/flutter/material/ThemeExtension-class.html
- React Native and Android 16 edge-to-edge: https://github.com/react-native-community/discussions-and-proposals/discussions/921
- DTCG format 2025.10: https://www.designtokens.org/tr/2025.10/
