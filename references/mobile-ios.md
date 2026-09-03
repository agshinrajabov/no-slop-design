# iOS (iOS 26, Liquid Glass) — platform reference

Purpose: give an agent the exact numbers, component choices and rules needed to produce an iOS app that reads as a designed product rather than a stock template or a web page in a WebView. It covers iOS 26 / Liquid Glass (WWDC25), SwiftUI-first component selection, Dynamic Type, semantic color, navigation, haptics, motion, and how DTCG tokens from `design-tokens.md` land in SwiftUI. Cross-platform mapping (Flutter, React Native) lives in `mobile-android.md`; brand color math in `color.md`; contrast and a11y requirements in `accessibility.md`; generic motion principles in `motion.md`; generic slop tells in `anti-slop.md`.

## Contents

1. Platform posture: system vs custom
2. Liquid Glass rules
3. Layout numbers, safe areas, targets
4. Typography and Dynamic Type
5. Color and dark mode
6. Navigation patterns
7. Components and haptics
8. Motion
9. Token mapping (DTCG to SwiftUI)
10. App icon and App Store assets
11. iOS-specific slop
12. Review checklist
13. Sources

## 1. Platform posture: system vs custom

Default to the system control. Replace it only when the brand needs a behaviour the system control cannot express, and then keep the system control's size, gesture and accessibility contract.

| Surface | Use system | Go custom when | Never |
|---|---|---|---|
| Navigation bar, tab bar, toolbar, sheet chrome | Always (`NavigationStack`, `TabView`, `.toolbar`, `.sheet`) | Only branded content inside them (title view, accessory) | Rebuild the bar; you lose swipe-back, Liquid Glass, minimize-on-scroll, VoiceOver rotor |
| Buttons | `Button` with `.bordered` / `.borderedProminent` / `.glass` / `.glassProminent`, `.tint(brand)` | Marketing CTA, hero cards | Gradient fills, drop shadows, 12pt labels |
| Lists, forms, settings | `List` `.insetGrouped`, `Form`, `Section` | Feed / media grids | Custom rows under 44pt or without `.listRowSeparator` control |
| Toggles, pickers, steppers, sliders, date pickers | `Toggle`, `Picker` (`.menu`, `.wheel`, `.segmented`), `DatePicker` | Never for the control itself; style via `.tint` | Custom toggle drawn from scratch (fails Switch Control, Reduce Motion, Increase Contrast) |
| Alerts, confirmation | `.alert`, `.confirmationDialog` | Rich onboarding or paywall (sheet) | Custom alert overlays |
| Search | `.searchable` (+ `Tab(role: .search)` in iOS 26) | Never | A text field styled to look like search |
| Context actions | `.contextMenu`, `.swipeActions` | Never | Long-press custom pop-ups |
| Typography | SF Pro / SF Compact / New York via text styles | Brand face for display styles only (see 4) | Brand face for body text without Dynamic Type scaling |

Typeface posture: SF Pro (UI), SF Compact (watch, narrow), New York (editorial serif) are legitimate defaults for all UI text, ship with every device, cost zero bytes, and carry optical sizing plus the full Dynamic Type contract. A brand face is allowed for display and title styles; for body/label text it must ship with a `relativeTo:` mapping and be tested at AX5 (see 4). Using SF is not "unbranded"; brand identity on iOS comes from color, icon, motion, illustration and copy, not from replacing the system UI font.

## 2. Liquid Glass rules (iOS 26)

Liquid Glass is a material for the navigation layer that floats above content: tab bars, toolbars, navigation bars, sheets' chrome, floating action groups. It is not a surface for content.

| Rule | Value | Why / source |
|---|---|---|
| Where glass goes | Only on controls and navigation floating above the content layer | HIG Materials; WWDC25 "Meet Liquid Glass" |
| Where glass never goes | Lists, tables, cards, cells, media, text blocks, backgrounds | Content on glass cuts legibility; glass-on-glass produces visual noise |
| Variant default | `.regular` | Adaptive: adds dimming/tint automatically, legible at any size over any content |
| Variant `.clear` | Only when all three hold: (1) sits over media-rich content (photo, video, map), (2) a dimming layer under the glass will not harm that content, (3) the content placed on the glass is bold and bright | Clear has no adaptive behaviour; Apple's session warns legibility degrades without a dimming layer |
| Glass on glass | Never stack a glass element on another glass element | HIG; the material is meant to be one layer thick |
| Grouping | Wrap sibling glass controls in one `GlassEffectContainer(spacing:)`; use `glassEffectID(_:in:)` for morphing on show/hide | Shared rendering, correct blending, morph transitions |
| Corner geometry | `.rect(cornerRadius: .containerConcentric)` for glass shapes nested in a rounded container; `ConcentricRectangle()` for custom shapes | Inner radius = outer radius minus inset; mismatched radii read as sloppy |
| Tint | `.glassEffect(.regular.tint(color))` only when the tint carries meaning (primary action, destructive, selected state) | HIG: tint conveys meaning, not decoration; a tinted glass bar for "brand feel" is slop |
| Interactive | `.glassEffect(.regular.interactive())` on tappable custom glass | Enables press scale/shimmer matching system controls |
| Reduce Transparency | Glass becomes a frosted, near-opaque surface; layout must still work | Test in Settings > Accessibility > Display & Text Size |
| Increase Contrast | Glass gains solid borders and higher-contrast fills | Do not draw your own borders on glass; they double up |
| Reduce Motion | Morph and lensing animations are cut back or removed | Never gate function behind a morph |
| iOS 26.1 user setting | Settings > Display & Brightness > Liquid Glass: Clear (default look) or Tinted (more opaque, more contrast) | Design for both; verify text on the Tinted setting and under Reduce Transparency |
| Scroll edge | Use `.scrollEdgeEffectStyle(.soft / .hard)` rather than custom gradient fades under bars | System keeps content legible as it passes under glass |
| Backgrounds under glass | Give the content layer real contrast: solid or gently varied backgrounds, no busy patterns directly under bars | Glass samples what is under it |
| Custom glass views | Reserve for a small number of floating controls (a map action cluster, a player transport) | Everything else: system components already render glass |

Branded without looking like a template: keep every system bar and control, then spend brand budget on (a) a single accent color applied through `.tint` and to selection states, (b) one display typeface for large titles and hero numbers, (c) distinctive iconography inside SF Symbols' grid (custom symbols via SF Symbols app, weights matched), (d) illustration/photography in the content layer, (e) motion signatures (a specific spring for your key transition), (f) copy voice. What does not work: recoloring bars, restyling toggles, gradient buttons, custom tab bars. A user should recognise the brand from a screenshot of the content area alone, and recognise iOS from the chrome alone.

## 3. Layout numbers, safe areas, targets

| Rule | Value | Why / source |
|---|---|---|
| Design canvas (portrait) | 390×844pt (iPhone 15/16 base); check 402×874 (16 Pro/17), 440×956 (Pro Max), 375×667 (SE) | Covers the current fleet; design at 390, verify at 375 and 440 |
| Minimum tap target | 44×44pt | HIG; controls smaller visually still need a 44pt hit area (`.contentShape`, `.frame(minWidth:44,minHeight:44)`) |
| Spacing between adjacent targets | 8pt minimum | Prevents mis-taps; HIG |
| Horizontal screen margin | 16pt (compact width); 20pt acceptable for editorial | Matches inset-grouped list margins |
| Base spacing unit | 4pt; use 4/8/12/16/20/24/32 | Aligns with system components |
| Status bar | 54pt on Dynamic Island devices; top safe-area inset 59–62pt (Pro: 62), 47 on notch devices, 20 on SE | Read `safeAreaInsets`; never hardcode |
| Bottom safe-area inset | 34pt iPhone (home indicator), 20pt iPad, 0 on SE/home-button devices | Home indicator bar itself is 5pt tall, 134pt wide; keep any interactive element at least 21pt above the indicator, in practice: respect the 34pt inset |
| Navigation bar | 44pt compact; large title adds 52pt (96pt total) | System sets; do not fake |
| Tab bar (iOS 26) | Floating glass capsule with its own margins; height is system-managed (about 49pt of content plus inset); minimizes on scroll with `.tabBarMinimizeBehavior(.onScrollDown)` | Use `.safeAreaInset` / Scaffold-free layout so content scrolls under it |
| Toolbar | 44pt row; glass on iOS 26 | System |
| List row | 44pt minimum; 60pt with subtitle; inset-grouped corner radius set by system (larger on iOS 26, do not hardcode 10pt) | HIG Lists |
| Sheet corner radius | System (concentric with device); detents `.medium`, `.large`, `.fraction`, `.height` | `.presentationDetents` |
| Card / container radius | 12–20pt in content layer; match `.containerConcentric` when nested | Consistent with system inset-grouped shapes |
| Icon sizes | SF Symbols scale with text style; toolbar icons 17pt @ semibold weight equivalent; tab icons ~25pt | Use `.imageScale` and text styles, not fixed point sizes |
| Line length | 45–75 characters at body size | Readability |
| Keyboard | Use `.safeAreaInset`/`ScrollView` with keyboard avoidance; toolbar above keyboard via `.toolbar(placement: .keyboard)` | Content must not hide behind keyboard |
| iPad | 20pt margins minimum, readable-content width 672pt for text columns, `NavigationSplitView` | HIG Layout |

## 4. Typography and Dynamic Type

Default (Large) sizes. Every text element must be bound to one of these styles so it scales with the user's setting; the scale runs xSmall (body 14pt) to AX5 (body 53pt).

| Text style | Size/leading (pt) | Weight | Use |
|---|---|---|---|
| Large Title | 34/41 | Regular (Bold in nav bar) | Screen title at top of scroll |
| Title 1 | 28/34 | Regular | Section hero, onboarding headline |
| Title 2 | 22/28 | Regular | Card title, grouped section title |
| Title 3 | 20/25 | Regular | Sub-section |
| Headline | 17/22 | Semibold | Row primary text, emphasized body |
| Body | 17/22 | Regular | Default text; the floor for reading text |
| Callout | 16/21 | Regular | Secondary paragraphs |
| Subheadline | 15/20 | Regular | Row secondary text |
| Footnote | 13/18 | Regular | Metadata, timestamps |
| Caption 1 | 12/16 | Regular | Labels under icons, tab labels |
| Caption 2 | 11/13 | Regular | Smallest legal size; badges, legal |

| Rule | Value | Why / source |
|---|---|---|
| Body floor | 17pt at default size; do not set reading text below Body | HIG Typography |
| Absolute minimum | 11pt (Caption 2); nothing smaller anywhere | Caption 2 does not scale below 11 |
| Custom fonts | `Font.custom("Brand", size: 17, relativeTo: .body)` (SwiftUI) or `UIFontMetrics(forTextStyle:).scaledFont(for:)` (UIKit) | Fixed-size custom fonts break Dynamic Type; App Review and a11y audits flag it |
| Max scale for display type | Cap hero text with `.dynamicTypeSize(...DynamicTypeSize.accessibility2)` only for decorative headlines; never cap body or controls | Layout survives AX5 |
| Layout at AX sizes | Switch `HStack` to `VStack` with `ViewThatFits` or `@Environment(\.dynamicTypeSize)` at `.accessibility1`+ | HIG; rows must reflow, not truncate |
| Truncation | Body copy wraps; single-line labels get `.lineLimit(1)` + `.minimumScaleFactor(0.8)` only for numerics | Ellipsized body text is a defect |
| Weight for emphasis | Semibold for headlines, Bold for large titles; avoid Light/Thin under 20pt | Legibility on glass and in dark mode |
| Monospaced digits | `.monospacedDigit()` for counters, prices, timers | Prevents jitter |
| Letter spacing | Leave SF tracking alone; it is optical-size tuned | Manual tracking on SF reads as web CSS |
| Line height | Do not override system leading except in editorial long-form (+2 to +4pt) | Consistency with system rows |

## 5. Color and dark mode

Use semantic system colors for all UI text and backgrounds; use brand colors only through `.tint` and in content-layer surfaces defined as tokens with light/dark/high-contrast variants (see `color.md`).

| Semantic color | Light | Dark | Use |
|---|---|---|---|
| `label` | #000000 | #FFFFFF | Primary text |
| `secondaryLabel` | #3C3C43 @60% | #EBEBF5 @60% | Subtitles, metadata (still passes 4.5:1) |
| `tertiaryLabel` | #3C3C43 @30% | #EBEBF5 @30% | Placeholders; not for essential text |
| `quaternaryLabel` | #3C3C43 @18% | #EBEBF5 @16% | Disabled, watermarks |
| `systemBackground` | #FFFFFF | #000000 (base) / #1C1C1E (elevated) | Screen background (plain lists) |
| `secondarySystemBackground` | #F2F2F7 | #1C1C1E / #2C2C2E elevated | Grouped content over primary |
| `tertiarySystemBackground` | #FFFFFF | #2C2C2E / #3A3A3C elevated | Content inside secondary |
| `systemGroupedBackground` | #F2F2F7 | #000000 / #1C1C1E | Inset-grouped list background |
| `secondarySystemGroupedBackground` | #FFFFFF | #1C1C1E / #2C2C2E | Inset-grouped cells |
| `separator` | #3C3C43 @29% | #545458 @60% | Hairlines (1px, not 1pt) |
| `systemFill` … `quaternarySystemFill` | tinted grays | tinted grays | Thin/thick control fills |
| `tint` / `accentColor` | brand | brand adjusted | Interactive elements only |

| Rule | Value | Why / source |
|---|---|---|
| Dark mode elevation | Elevated contexts (sheets, popovers, iPad slide-over) automatically use the elevated set (#1C1C1E base, #2C2C2E, #3A3A3C); do not build depth with shadows in dark | HIG Dark Mode: brighten to bring forward |
| Accent in dark | Raise luminance and lower saturation of the brand accent (system blue: #007AFF light → #0A84FF dark; system green #34C759 → #30D158); target ≥ 4.5:1 for text-on-accent and ≥ 3:1 for accent-on-background | Saturated brand hues on black bloom and fail contrast |
| Accent for text on white | If brand accent fails 4.5:1 as text, keep it as fill and use `label` on top | `accessibility.md` |
| Increase Contrast | Provide high-contrast variants in the asset catalog (Any/Dark × Normal/High) | System swaps automatically |
| Color as sole signal | Never; pair with SF Symbol, weight or text | WCAG 1.4.1 |
| Gradients | Content-layer illustration only; not on controls, bars or text | Reads as generic AI output |
| Pure black backgrounds | Fine for OLED media apps; for productivity use `systemBackground` and let the system pick base vs elevated | HIG |

## 6. Navigation patterns

| Pattern | Use when | Numbers / API | Do not |
|---|---|---|---|
| Tab bar | 2–5 top-level, peer destinations | `TabView` with `Tab(title, systemImage:)`; ≤5 tabs; iOS 26: `Tab(role: .search)` floats search bottom-right; `.tabViewBottomAccessory` for a mini player | 6+ tabs, "More" tab, hamburger as replacement, tabs that open modals |
| Navigation stack | Hierarchical drill-down | `NavigationStack(path:)` + `navigationDestination`; push preserves interactive swipe-back | Custom back buttons that break the edge swipe; hidden nav bar without restoring the gesture |
| Large title | Top of a root or major list screen | `.navigationBarTitleDisplayMode(.large)`; collapses to inline on scroll | Large titles on every pushed detail screen |
| Sheet with detents | Task in the current context, dismissible, non-destructive | `.sheet` + `.presentationDetents([.medium, .large])`, `.presentationDragIndicator(.visible)`, `.presentationBackgroundInteraction` for non-modal | Full-screen cover for a 2-option choice |
| Full-screen cover | Immersive flows (camera, player, onboarding) | `.fullScreenCover` with an explicit Close | Anything with a nav hierarchy inside |
| Confirmation dialog | 2–5 actions on an object | `.confirmationDialog`; destructive with `role: .destructive` | Custom bottom sheets for this |
| Alert | Blocking, ≤2 buttons, rarely 3 | `.alert`; Cancel left/bottom | Marketing or non-critical info |
| Popover | iPad and Mac; on iPhone becomes sheet | `.popover` with `.presentationCompactAdaptation(.sheet)` | Custom tooltip overlays |
| Split view | iPad, regular width | `NavigationSplitView` 2–3 columns; sidebar 320pt default | Stretching an iPhone layout to 1024pt |
| Search | Lists and browse screens | `.searchable(text:placement:)`; iOS 26 bottom placement or search tab | Search field pinned in a custom header |
| Toolbar | Screen-level actions | `.toolbar { ToolbarItem(placement: .primaryAction / .bottomBar) }`; `ToolbarSpacer` groups glass items | More than 3 icon actions in one bar; text + icon mix without reason |
| Modal vs push | Push = deeper in the same hierarchy; Modal = separate task with its own completion (Create, Edit, Filter) | Modal needs explicit Done/Cancel; push needs Back | Modal for browsing, push for editing |
| Back behaviour | Swipe-back must always work on pushed screens | Do not override `interactivePopGestureRecognizer`; if using `.navigationBarBackButtonHidden`, restore the gesture | Custom chevron + "Back" text labels drawn by hand |
| Deep links / state restoration | `NavigationPath` codable, `onOpenURL`, `SceneStorage` | Restore stack, not just the leaf | Opening deep links as modals over an empty root |

## 7. Components and haptics

| Component | System choice | Notes |
|---|---|---|
| Primary action | `Button` `.buttonStyle(.borderedProminent)` (in content) or `.glassProminent` (floating); `.controlSize(.large)` → 50pt height | One prominent button per screen region |
| Secondary | `.bordered` / `.glass`; tertiary: `.borderless` (text) | Same height, same corner radius family |
| Destructive | `Button(role: .destructive)` | System red, no custom |
| Lists | `List` `.listStyle(.insetGrouped)` for settings/forms; `.plain` for feeds | Use `Section(header:footer:)`, `.swipeActions`, `.refreshable` |
| Forms | `Form` with `LabeledContent`, `TextField`, `Toggle`, `Picker` | Labels leading, values trailing |
| Pickers | `.menu` (≤ ~10 options), `.wheel` (dates, long lists inline), `.segmented` (2–5 short peers, view switching) | Segmented is for views/filters, not for actions |
| Text input | `TextField`/`SecureField` with `.textContentType`, `.keyboardType`, `.submitLabel`, `.textInputAutocapitalization` | Autofill works only with content types set |
| Context menu | `.contextMenu` with SF Symbols and `Divider()` | Preview via `.contextMenu(menuItems:preview:)` |
| Badges | `.badge()` on tab and list rows | Numbers only |
| Progress | `ProgressView` (indeterminate spinner, linear) | Skeletons only for content that takes >1s |
| Empty states | `ContentUnavailableView` (`.search` variant for no results) | System spacing and type |
| Share | `ShareLink` | Never a custom share sheet |
| Payment | `PayWithApplePayButton`, `SignInWithAppleButton` | Exact system buttons, no restyle |

Haptics: one haptic per user-perceived event, always paired with a visible state change. SwiftUI: `.sensoryFeedback(_, trigger:)`; UIKit generators listed.

| Generator | When | Not for |
|---|---|---|
| `UIImpactFeedbackGenerator(.light)` | Small element snaps, toggles flipping, reordering pick-up | Every button |
| `.medium` | Standard confirmation of a discrete action (drop, add to cart) | Scroll events |
| `.heavy` | Big physical events (large item drops, end-of-drag collision); rare | Repeated use |
| `.rigid` | Crisp snap to a fixed position (ruler tick, detent, alignment guide) | Soft UI |
| `.soft` | Gentle, elastic feedback (pull-to-refresh threshold, rubber-band) | Errors |
| `UINotificationFeedbackGenerator(.success)` | Task completed (payment, upload, save) | Every network response |
| `.warning` | Action needs attention before proceeding | Validation typos |
| `.error` | Action failed or rejected (wrong passcode) | Form field errors while typing |
| `UISelectionFeedbackGenerator` | Selection changing through a continuous control (picker wheel, slider detents, segmented) | Button taps |

Call `prepare()` before an expected interaction; never trigger haptics on timers, on screen appearance, or during scrolling. System components already emit their own haptics; do not double them.

## 8. Motion

| Rule | Value | Why / source |
|---|---|---|
| Curve family | Springs, not cubic-bezier | Every system transition on iOS 17+ is a spring; mixing curves is visible |
| Default spring | `.spring(response: 0.35, dampingFraction: 0.8)` or presets `.snappy` (short UI), `.smooth` (no bounce), `.bouncy` (playful, use sparingly) | Matches nav push (~0.35s) and sheet (~0.5s, dampingFraction ≈ 0.85) feel |
| Micro (toggle, checkmark, button press) | `.snappy(duration: 0.2)` or `.spring(response: 0.2, dampingFraction: 0.9)` | Under 250ms reads as immediate |
| Layout changes | `withAnimation(.smooth)` + `.animation(_, value:)` scoped to one value | Unscoped `.animation` animates everything |
| Interruptible | All gestures drive springs that can be reversed mid-flight (`.gesture` + `@GestureState`) | HIG: motion must never block input |
| Shared element | `matchedGeometryEffect(id:in:)` within a view tree; `NavigationLink` + `.navigationTransition(.zoom(sourceID:in:))` (iOS 18+) for push | System zoom transition already respects Reduce Motion |
| Glass morph | `glassEffectID` inside `GlassEffectContainer`, animate with `withAnimation(.smooth)` | System-defined morph |
| Duration ceiling | 0.5s for anything the user waits on; 0.7s only for full-screen hero | Longer feels slow on a phone |
| Reduce Motion | Read `@Environment(\.accessibilityReduceMotion)`; replace slides/zooms with opacity crossfade; keep durations, drop bounce | HIG Accessibility |
| Loading | Do not animate skeletons with shimmer at high contrast; simple pulse or `ProgressView` | Shimmer over glass looks like a rendering bug |
| Continuous animation | Only for state that is actually changing (live audio meter); never for decoration | Battery and distraction |
| Scroll-driven | `scrollTransition` and `visualEffect` for parallax within ±10% scale/opacity | Larger values feel like a landing page |

## 9. Token mapping (DTCG to SwiftUI)

Source of truth is the DTCG JSON in `design-tokens.md`. `build_tokens.py` emits `DesignTokens.swift` plus, optionally, an `.xcassets` color set per color token. Expected shape of the generated file:

```swift
// DesignTokens.swift (generated — do not edit)
import SwiftUI

enum DT {
    enum Color {
        static let brandPrimary = SwiftUI.Color("dt/brand/primary")      // asset catalog: Any, Dark, High Contrast
        static let surface      = SwiftUI.Color(uiColor: .systemBackground)
        static let textSecondary = SwiftUI.Color(uiColor: .secondaryLabel)
    }
    enum Space { static let s1: CGFloat = 4, s2: CGFloat = 8, s3: CGFloat = 12, s4: CGFloat = 16, s6: CGFloat = 24, s8: CGFloat = 32 }
    enum Radius { static let sm: CGFloat = 8, md: CGFloat = 12, lg: CGFloat = 20 }
    enum Type {
        static let display = Font.custom("BrandDisplay-Semibold", size: 34, relativeTo: .largeTitle)
        static let body    = Font.body            // SF, Dynamic Type
        static let label   = Font.subheadline
    }
    enum Motion {
        static let snappy = Animation.spring(response: 0.25, dampingFraction: 0.9)
        static let standard = Animation.spring(response: 0.35, dampingFraction: 0.8)
    }
}
```

| DTCG token type | SwiftUI target | Rule |
|---|---|---|
| `color` with light/dark (and hc) modes | Asset catalog Color Set (Appearances: Any, Dark; High Contrast checkbox) referenced by name | Catalog, not code, so the system swaps for dark/Increase Contrast without a redraw |
| `color` that aliases a system role | `Color(uiColor: .label)` etc. | Never hex-copy system colors; they change per OS |
| `dimension` (spacing, radius) | `CGFloat` statics | Multiples of 4 |
| `fontFamily` + `fontSize` + text style ref | `Font.custom(_, size:, relativeTo:)` | `relativeTo` is mandatory; no `.fixedSize` fonts |
| `fontWeight` | `.weight(.semibold)` on SF; named face for custom | Map 600 → semibold, 700 → bold |
| `duration` + `cubicBezier` | Convert to spring (`response`, `dampingFraction`) | Do not use `.timingCurve` to mirror web easings |
| `shadow` | `.shadow(color:radius:x:y:)` in content layer only | None on bars; none in dark mode |
| Opacity ramps | `.opacity()` constants | Secondary text uses system labels instead |

Asset catalog vs code: colors and images → catalog; numbers, fonts, motion → code. Set `AccentColor` in the catalog to the brand primary so all system controls tint correctly. Keep semantic aliases (`surface`, `textPrimary`) mapped to system colors unless the brand requires otherwise; brand-specific colors get their own catalog entries with all four appearance variants.

## 10. App icon and App Store assets

| Item | Value | Why / source |
|---|---|---|
| Icon source | One 1024×1024 PNG (no alpha) for App Store; Xcode 26 `.icon` file from Icon Composer for layered rendering | Apple; Icon Composer bundled with Xcode 26 |
| Layers | Up to 4 depth groups; foreground vector (SVG) preferred; background as flat or 2-stop gradient | Liquid Glass lighting, specular highlights and tinted/clear modes are generated from the layers |
| Appearance modes | Design Default, Dark, Mono; system derives Clear Light/Dark and Tinted Light/Dark | Mono layer must survive as a single-colour silhouette |
| Mask | Do not round corners yourself; provide a full-bleed square | System applies the superellipse |
| Content | One glyph or mark, centred on the Apple icon grid; no text, no screenshots, no photos, no thin strokes under 8px at 1024 | HIG App Icons; text becomes illegible at 29pt |
| Contrast | Foreground vs background ≥ 3:1 in Default and Dark | Tinted mode collapses to one hue plus luminance |
| Screenshots | 6.9" (1320×2868) and 13" iPad (2064×2752) are the required sets; ≤10 per locale; first three carry the message | App Store Connect; device frames optional |
| Screenshot content | Real UI at real Dynamic Type default, real data, one caption line per shot in the brand display face | Mock data with "Lorem" or repeated names is a rejection risk and a slop tell |

## 11. iOS-specific slop

| Tell | Do instead |
|---|---|
| Emoji as tab bar or toolbar icons | SF Symbols (or custom symbols on the SF grid) with `Label` text |
| Gradient-filled buttons with drop shadows | `.borderedProminent` / `.glassProminent` with `.tint` |
| Android-style FAB on iOS | Toolbar `primaryAction`, a prominent button in the nav bar, or an iOS 26 floating glass button group |
| Hamburger menu instead of tab bar | 2–5 tabs; overflow goes into a Profile/Settings tab |
| Custom nav bar that kills swipe-back | System `NavigationStack`; customise the title view, not the bar |
| Full-screen modal for a simple choice | `.confirmationDialog` or `.sheet` with `.medium` detent |
| Custom toggles/checkbox squares | `Toggle` (`.switch`); multi-select lists with checkmarks via `List(selection:)` |
| Glass on cards, cells or backgrounds | Solid semantic backgrounds; glass only on floating chrome |
| Web hover states, cursor-pointer thinking | Pressed states via `ButtonStyle` `isPressed`; hover only on iPad pointer via `.hoverEffect` |
| 12px / 13px body text | Body 17pt; Footnote 13pt only for metadata |
| Hex-coded grays for text | `label`, `secondaryLabel` |
| Card-inside-card-inside-card | One container level; inset-grouped list sections |
| Bottom sheet reinvented with a `ZStack` | `.sheet` + detents |
| Pill "chips" as primary navigation | Segmented control (≤5) or a filter menu |
| Onboarding carousel with 5 gradient slides | ≤3 screens, or contextual tips (`TipKit`) |
| Custom pull-to-refresh spinner | `.refreshable` |
| Splash screen with logo animation | Static launch storyboard matching the first screen |
| Toast notifications | Inline status, `.alert`, or system banners; iOS has no toast idiom |
| Rounded 8pt everywhere from a web system | Match system radii; concentric nesting |
| Uppercase tracked section headers in brand face | System `Section` headers (Footnote, secondaryLabel, uppercase already handled by style choice) |

## 12. Review checklist

1. Every tappable element has a 44×44pt hit area; adjacent targets ≥ 8pt apart.
2. Screen renders correctly at Dynamic Type xSmall, Large, AX3 and AX5 with no clipped or overlapping text.
3. No text below 11pt; no reading text below Body (17pt).
4. Every font is bound to a text style (`relativeTo:` or system style).
5. All UI text uses `label`/`secondaryLabel`/`tertiaryLabel`; no hard-coded grays.
6. Brand accent is set via `AccentColor` and passes 4.5:1 (text) / 3:1 (UI) in light and dark.
7. Dark mode uses base vs elevated backgrounds; no shadows used to build depth in dark.
8. Increase Contrast and Reduce Transparency both produce a usable, legible screen.
9. Reduce Motion replaces zoom/slide/morph with crossfade; nothing is unreachable.
10. Liquid Glass appears only on floating chrome; no glass on lists, cards, media or backgrounds.
11. No glass-on-glass; grouped glass controls sit in one `GlassEffectContainer`.
12. `.clear` glass is used only over media with a dimming layer and bright foreground content.
13. Glass tint is used only to carry meaning (primary/destructive/selected).
14. Nested corner radii are concentric.
15. Tab bar has 2–5 tabs, SF Symbols icons, and text labels; no hamburger as primary nav.
16. Swipe-back works on every pushed screen; no custom back button that breaks it.
17. Modals have explicit Done/Cancel; pushes have Back; simple choices use dialogs or medium-detent sheets.
18. Large title only on root/major screens; inline elsewhere.
19. Search uses `.searchable` (or iOS 26 search tab); keyboard has correct type and return key.
20. Forms use system `Form`/`List(.insetGrouped)` rows with system pickers and toggles.
21. Haptics fire once per event, paired with visible change, using the correct generator.
22. All animations are springs, scoped with `value:`, interruptible, ≤ 0.5s.
23. Safe areas respected: nothing interactive under the home indicator or Dynamic Island; content scrolls under bars.
24. iPad: `NavigationSplitView` or readable-width column; landscape checked.
25. VoiceOver: every image button has `accessibilityLabel`; custom views have traits; reading order is logical.
26. Empty, loading and error states use `ContentUnavailableView`/`ProgressView`, not custom illustrations by default.
27. App icon: single mark, no text, layered `.icon` with Default/Dark/Mono verified in Clear and Tinted modes.
28. Tokens are consumed from `DesignTokens.swift` and the asset catalog; no literal hex or magic numbers in views.
29. Screenshots show real data at default type size.
30. A screenshot of the content layer reads as the brand; a screenshot of the chrome reads as iOS.

## 13. Sources

- Apple HIG — Materials / Liquid Glass: https://developer.apple.com/design/human-interface-guidelines/materials
- Apple HIG — Layout: https://developer.apple.com/design/human-interface-guidelines/layout
- Apple HIG — Typography: https://developer.apple.com/design/human-interface-guidelines/typography
- Apple HIG — Color and Dark Mode: https://developer.apple.com/design/human-interface-guidelines/color , https://developer.apple.com/design/human-interface-guidelines/dark-mode
- Apple HIG — Tab bars, Navigation bars, Sheets, App icons: https://developer.apple.com/design/human-interface-guidelines/tab-bars , https://developer.apple.com/design/human-interface-guidelines/sheets , https://developer.apple.com/design/human-interface-guidelines/app-icons
- WWDC25 "Meet Liquid Glass" (Regular vs Clear conditions): https://developer.apple.com/videos/play/wwdc2025/219/
- SwiftUI GlassEffectContainer / containerConcentric: https://developer.apple.com/documentation/swiftui/glasseffectcontainer , https://developer.apple.com/forums/thread/787615 , https://nilcoalescing.com/blog/ConcentricRectangleInSwiftUI/
- iOS 26 tab bars (minimize, search role, accessory): https://www.donnywals.com/exploring-tab-bars-on-ios-26-with-liquid-glass/
- iOS 26.1 Liquid Glass Clear/Tinted setting: https://www.macrumors.com/how-to/ios-26-1-reduce-liquid-glass-effects/
- Dynamic Type sizes: https://developer.apple.com/design/human-interface-guidelines/typography#Specifications , https://sarunw.com/posts/scaling-custom-fonts-automatically-with-dynamic-type/
- iPhone screen sizes and safe-area insets: https://useyourloaf.com/blog/iphone-16-screen-sizes/
- Dark mode base/elevated backgrounds: https://contagious.dev/blog/ins-and-outs-of-ios-system-grouped-background-colors/ , https://sarunw.com/posts/dark-color-cheat-sheet/
- UIKit haptics: https://developer.apple.com/documentation/uikit/uiimpactfeedbackgenerator , https://developer.apple.com/design/human-interface-guidelines/playing-haptics
- Icon Composer and iOS 26 icons: https://www.createwithswift.com/crafting-liquid-glass-app-icons-with-icon-composer/
- App Store screenshot specifications: https://developer.apple.com/help/app-store-connect/reference/screenshot-specifications
- DTCG format 2025.10: https://www.designtokens.org/tr/2025.10/
