# Eval 03 — Native iOS screen (platform posture)

## Prompt

> Design the "Today" screen for Qandil, a prayer-times and reflection app for iOS 26. Brand: dark, warm, a lantern
> motif, display face Marcellus, body Manrope, Arabic support needed. SwiftUI. Show me the screen spec and the
> SwiftUI token file.

## Expected behaviour

Phase 0 reads the brand constraints (existing brand, level 1); brief confirms the memorable thing; short research on
prayer-app patterns (Mobbin/App Store) and the job ("know the next prayer at a glance, log it, read one line");
composition in Operate mode with a Persuade-like hero moment; platform rules from `mobile-ios.md` drive the
structure; tokens mapped to SwiftUI; review.

## Rubric (0 / 1 / 2 each)

1. Respected the brand's typefaces (Manrope is on the watch list; kept because it is a brand constraint, documented) and confirmed Manrope ships weights suitable for Dynamic Type, or proposed SF for UI text with Marcellus/Manrope for display only, with reasoning.
2. Dark palette built as its own scale (surface L≈0.18–0.24, warm-tinted, accent desaturated), not an inverted light palette; contrast verified on every text/surface role.
3. Structure follows HIG: tab bar (≤ 5) or navigation stack decided with reasons; large title or custom header justified; safe areas and the iOS 26 floating tab bar accounted for; swipe-back preserved.
4. Liquid Glass used only on the navigation layer (tab bar/toolbar), never on content cards; no glass-on-glass; tint conveys meaning.
5. 44pt targets, 8pt spacing, 16pt margins; Dynamic Type scaling for all text with `relativeTo:` roles; layout tested at accessibility sizes (describes what reflows).
6. Arabic: fallback chain (Amiri/Noto Naskh) with line-height 1.7–1.9, RTL mirroring of directional elements only, numerals decision (Western vs Eastern Arabic) stated.
7. Next-prayer countdown uses `tabular-nums`/monospaced digits; the hierarchy makes the next prayer the single focal point; the lantern motif appears once, meaningfully, not as a repeated decoration.
8. States: before dawn / between prayers / all logged / notifications off / location denied / offline, each specified.
9. Haptics and motion specified with system springs and purposes; reduced-motion path; no confetti/streak-pressure patterns; empty state copy warm and specific (no emoji, no "Oops").
10. Token file: `DesignTokens.swift` produced via `build_tokens.py` from DTCG tokens (light/dark where relevant), colors as dynamic `Color`, spacing as CGFloat constants; screen spec references tokens, not literals.
11. No Android-isms (FAB, Material ripple, hamburger for primary nav), no web hover states, no emoji tab icons, no gradient buttons.
12. Review gate run with platform section; screenshots or simulator evidence if available, otherwise stated.

Max 24. Pass ≥ 19 with items 2, 4, and 10 at 2.
