# Review Checklist (Self-Critique Gate)

Nothing ships on the first pass. This gate runs **before** presenting any design, prototype, or code to the user,
and again after revisions. It produces `templates/review-report.md`. Be harsher than the user will be; the point of
the gate is that they never have to say "this looks AI-generated".

## Contents

1. How to run the gate
2. Scoring
3. Gate 0 — mechanical checks (scripts)
4. Gate 1 — brief and research fidelity
5. Gate 2 — UX and flow
6. Gate 3 — hierarchy and composition
7. Gate 4 — typography
8. Gate 5 — color and contrast
9. Gate 6 — spacing, layout, responsiveness
10. Gate 7 — components and states
11. Gate 8 — motion
12. Gate 9 — content
13. Gate 10 — accessibility
14. Gate 11 — platform fit
15. Gate 12 — tokens and code hygiene
16. Gate 13 — slop and originality
17. The studio test
18. Revision protocol

---

## 1. How to run the gate

1. Render the work (browser at 3 widths, or simulator/emulator for native, or the prototype) and **look at it**.
   Screenshots, not code, are the primary evidence. Take them at 360, 768, 1280 (web) or the target device.
2. Run Gate 0 scripts.
3. Walk Gates 1–13 with the checklists; record every finding with impact (blocker / high / medium / polish),
   evidence (screenshot ref, line, value), and fix.
4. Write the studio test answers.
5. Grade; decide ship / not yet; execute the revision protocol.

Time: 15–40 minutes. Skipping it is the single most reliable way to ship slop.

## 2. Scoring

Grade each gate A–F. Overall = the **worst** of Gates 1, 2, 10, 13 (they are floors), then the average of the rest.

| Grade | Meaning |
|---|---|
| A | A senior designer would ship it as is |
| B | Ship after the polish list |
| C | Functional, generic; no point of view; needs a revision pass |
| D | Visible template/AI patterns or major UX defects |
| F | Blockers (a11y failures, broken flows, fabricated content) |

Nothing below B ships. C requires a revision pass, not an apology.

## 3. Gate 0 — mechanical checks

```bash
python3 scripts/slop_lint.py <src or file>                 # grade A/B required; annotate remaining hits
python3 scripts/contrast.py --pairs design/contrast-pairs.txt   # exit 0 required
python3 scripts/build_tokens.py tokens/*.json --check      # 0 errors
grep -rnE "#[0-9a-fA-F]{3,8}\b" src/components | grep -v tokens | head   # literal colors → 0
```
Plus, where available: axe-core / Lighthouse accessibility ≥ 95, no console errors, keyboard walkthrough recorded.

## 4. Gate 1 — brief and research fidelity

- [ ] The memorable thing is visible in the first viewport without explanation.
- [ ] Each of the three attributes can be pointed to in a concrete decision; none of the anti-attributes is present.
- [ ] Top job story is the primary path; primary action is where the reading path ends.
- [ ] Every research insight marked "drives a decision" is visible somewhere; list where.
- [ ] Constraints respected (existing system, brand assets, platform, localisation, performance floor).
- [ ] Market and language from the brief are visible in the design (locale formats, script support, local conventions, local references in the moodboard).
- [ ] Mode budget respected (Standard: ≤ 15 min, one direction + alternative, no unrequested documents).
- [ ] Nothing was added that the brief did not ask for and the research did not justify.

## 5. Gate 2 — UX and flow

- [ ] Trunk test passes on every screen (what app, what page, sections, local options, where am I, search).
- [ ] Task can be completed in the minimum sensible number of steps; count them.
- [ ] Every decision point is a "mindless click" (obvious what happens); nothing requires reading instructions.
- [ ] Back/undo exists for every reversible action; irreversible actions confirm or offer undo.
- [ ] Error, empty, loading, offline, partial states designed for every region.
- [ ] No dark patterns (confirmshaming, fake urgency, pre-selected upsells, hidden costs).
- [ ] URL/state: filters, tabs, pagination survive reload and back.
- [ ] Heuristic pass: no severity ≥ 3 findings remain.

## 6. Gate 3 — hierarchy and composition

- [ ] The expression register (R1–R4) is named in the brief and honoured on screen: scale, imagery, motion and
      technique match its row in `expression-register.md` §7; anything off-row is justified in writing.
- [ ] No label/value table is used as the primary layout device in more than two sections; section devices vary.
- [ ] Persuade: a designed visual anchor is present in the first viewport and the prototype contains real image elements (no gray placeholder boxes).
- [ ] Every photograph passes the three-match test (subject, light, material) and was actually looked at.
- [ ] Exactly one focal point per viewport; scale contrast ≥ 2× between tiers.
- [ ] Squint test: hierarchy visible when blurred.
- [ ] Cover-the-logo test: brand still recognisable.
- [ ] Reading path intentional (Z/F/single); primary action at its end.
- [ ] Above the fold communicates purpose in 3 seconds (5-second test).
- [ ] Section rhythm varies; no fixed skeleton; no identical section heights.
- [ ] Whitespace is intentional; no emptiness filled with decoration.

## 7. Gate 4 — typography

- [ ] Typefaces traceable to attributes; watch-list faces justified in writing.
- [ ] ≤ 2 families (+ mono for code); ≥ 2 distinct weights; scale ratio ≥ 1.2.
- [ ] Body ≥ 16px web / 17pt iOS / 14sp Android; line-height 1.5–1.65 body; measure 45–75ch.
- [ ] Display tracking slightly negative; no tracked lowercase; uppercase only on small tracked labels (if at all).
- [ ] `text-wrap: balance` on headings, `pretty` on paragraphs; no orphans in headlines.
- [ ] Real quotes, ellipsis, dashes; `tabular-nums` in numeric columns.
- [ ] Heading levels sequential; heading closer to what follows than what precedes.
- [ ] Fonts subset, self-hosted or preloaded; no FOUT on the display face.

## 8. Gate 5 — color and contrast

- [ ] One dominant hue; 60/30/10 distribution; ≤ 3 hue families + status.
- [ ] `action.primary` sits on the brand scale or within ~40° of the brand hue (`build_tokens.py --check` clean of palette warnings).
- [ ] Neutrals tinted consistently (warm or cool, never mixed).
- [ ] All text/surface pairs pass WCAG 2.2 AA (contrast pairs file); APCA Lc targets met for body (75) and secondary (60).
- [ ] UI boundaries and icons ≥ 3:1 vs adjacent.
- [ ] Dark mode: separate palette, no `#000`, elevation by lightness, accents desaturated, images dimmed.
- [ ] No color-only meaning; visited links differ.
- [ ] No purple/indigo gradients, gradient text, glow blobs, neon-on-black, untouched Tailwind/shadcn defaults.

## 9. Gate 6 — spacing, layout, responsiveness

- [ ] All spacing on the 4px scale; inner gaps < outer gaps.
- [ ] Separation via the cheapest device (whitespace → alignment → type → tint → hairline → elevation → card).
- [ ] Radius hierarchy; nested radii computed; no uniform bubbly radius.
- [ ] Grid consistent; deliberate break-outs; one page container.
- [ ] 320–1920 tested; no horizontal scroll; mobile is a redesign, not a stack.
- [ ] Touch targets ≥ 44/48 with 8px spacing on touch surfaces; ≥ 24 everywhere.
- [ ] `env(safe-area-inset-*)`, `dvh`, `scrollbar-gutter: stable` where relevant.

## 10. Gate 7 — components and states

- [ ] State matrix complete for every interactive component (hover, focus-visible, pressed, selected, disabled, loading, error, empty, dark, RTL, reduced-motion, forced-colors).
- [ ] Craft floor applied (selection, caret, scrollbar, accent-color, focus ring, underline offset, tap highlight, numerals).
- [ ] Controls in a row share height; hit areas exceed visuals.
- [ ] Native elements where possible; ARIA correct where not.
- [ ] No untouched library defaults; no colored left borders, icon tiles, glass cards, gradient buttons, pulsing dots, pill badges.

## 11. Gate 8 — motion

- [ ] Motion has a job (feedback, orientation, attention, signature); count of decorative animations = 0.
- [ ] Durations 80–400ms by size; exits shorter; standard/decelerate/accelerate curves; no bounce on UI.
- [ ] Only `transform`/`opacity` animated; no `transition: all`.
- [ ] One orchestrated entrance at most; no fade-up on every section; no marquee, typewriter, count-up, parallax, tilt.
- [ ] `prefers-reduced-motion` path defined and tested.
- [ ] Loading indicators follow the ladder (nothing < 300ms → skeleton → progress).

## 12. Gate 9 — content

- [ ] No banned words (`content-microcopy.md`); no happy talk; no instructions > 1 sentence.
- [ ] Buttons verb + object; each action names its result; no duplicates ("Get started" ×3).
- [ ] Errors: what happened + what to do; no "Oops".
- [ ] Empty states: what + why + action.
- [ ] No fabricated numbers, logos, testimonials, names, avatars; placeholders clearly marked and listed for the user.
- [ ] Sentence case; active voice; numbers/dates/currency via locale formatting.
- [ ] Delete-30% pass done on every paragraph.

## 13. Gate 10 — accessibility

- [ ] Keyboard: full walkthrough, visible focus, logical order, no traps, Esc closes overlays, focus returns.
- [ ] Names: every control has an accessible name; icon-only has `aria-label` + tooltip.
- [ ] Landmarks and heading outline sensible; one `h1`.
- [ ] Forms: visible labels, `autocomplete`, inline errors with `aria-describedby`, no paste blocking.
- [ ] Zoom 200% and 320px reflow OK; text spacing override OK; no `user-scalable=no`.
- [ ] Live regions for toasts/validation; `aria-busy` on loading regions.
- [ ] Forced-colors mode checked; `prefers-contrast` respected.
- [ ] Automated audit (axe/Lighthouse) clean; screen-reader spot check on the primary flow.

## 14. Gate 11 — platform fit

- [ ] Web: `web-frontend.md` craft floor; Core Web Vitals by design (LCP image priority, no CLS from fonts/skeletons).
- [ ] iOS: HIG navigation, 44pt, Dynamic Type, safe areas, Liquid Glass only on navigation layer, swipe-back works, system components where sensible.
- [ ] Android: M3 shape/type/motion tokens, 48dp, predictive back, edge-to-edge, navigation bar ≤ 5, tonal surfaces in dark.
- [ ] Cross-platform: platform conventions kept per OS (tab bar vs nav bar, back gesture, pickers), not one design forced on both.

## 15. Gate 12 — tokens and code hygiene

- [ ] Zero literal colors/sizes/fonts in components; everything via semantic tokens.
- [ ] Tokens follow the tier/naming grammar; every semantic color has light + dark; build `--check` clean.
- [ ] `DESIGN.md` updated (decisions, changelog); `design-log.json` updated.
- [ ] Existing design system respected (if any): no new fonts/primaries/radius scales; additions documented upstream.
- [ ] Generated `build/` not edited by hand; fonts licensed; assets exported in required densities.

## 16. Gate 13 — slop and originality

- [ ] `slop_lint.py` grade A/B; each remaining hit annotated "earned because …".
- [ ] Walk `anti-slop.md` §1–§9 with the screenshots; zero unannotated tells.
- [ ] Over-correction check (§8): every style signal traceable to an attribute or content type; ≤ 2 trend signals stacked.
- [ ] Anti-convergence: this design differs from the last one logged in `design-log.json` on ≥ 2 axes (structure, type, hue, density, motion) unless it is the same product.
- [ ] Not the skill's own tell: dark surface + serif display + fact table + one button. If the page could be swapped with another industry's page by changing the nouns, the direction failed.
- [ ] Local fit: at least one decision traceable to the audience's market (convention, reference, copy register).
- [ ] Name three decisions no template would have made.
- [ ] Name the brand attribute behind: typeface, primary color, radius, densest screen, the one motion.

## 17. The studio test

Answer in writing in the report:

1. Would a respected studio put its name on this? If not, what would they change first?
2. Cover the logo. Whose product is this?
3. What is the one thing a first-time viewer will remember? Is it the memorable thing from the brief?
4. Where is the boldness spent? (One place. If everywhere, nowhere.)
5. What would you remove if forced to remove one thing? Remove it.

## 18. Revision protocol

- Blockers and highs: fix before presenting. Do not present with a list of known blockers.
- Mediums: fix if < 30 min total; otherwise list in the report with owner and ETA.
- Polish: list; fix in the next pass.
- **Refine or redesign, never split the difference.** If Gate 3 or 13 is D/F, the direction is wrong; go back to the
  moodboard/composition step. Polishing a wrong direction produces expensive slop.
- Re-run the full gate after revisions. Grades must not regress on any gate.
- Record in `design-log.json`: `{ "review": "2026-09-03", "grades": {...}, "slop": "B", "fixed": [...], "open": [...] }`.
