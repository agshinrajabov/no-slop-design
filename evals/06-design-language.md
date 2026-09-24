# Eval 06 — Ten industries, one day (the design language)

**Tests:** that pages come out in their category's language, not the skill's. The 1.21 verdict was that ten
industries still looked 50% alike: every page was composed, tinted, one-anchor, one-bold-move — this skill's own
language under different colours. The fix (1.22) measures the market's language on nine axes and converges on it.

## Prompt

Run ten client-style briefs in one day (in parallel where possible, each with `design_log.py plan`), one page each,
Standard mode. Vary the industries so the categories speak different languages; do not tell the agent which
language to use. Suggested set: a developer tool, a family-law practice, a music festival, a paediatric clinic, a
fashion label, a retail bank, a restaurant, a design agency, a documentation site, a children's learning app.
Give each brief a market, a language, what assets exist and one real constraint.

## Rubric (0 / 1 / 2 each)

1. `Market:` line in `DESIGN.md` from `shoot.py --profile` with ≥ 3 competitor pages, ≥ 2 local, each looked at
2. The market line's splits are named as free choices; unanimous axes kept or departed from with a written reason
3. `Design language:` written in Phase 3, nine vocabulary words, before tokens
4. ≤ 3 departures, each naming the axis, the word and the brief's reason; none "to be different"
5. The built page's measured `language` line matches the declared one, or the difference is explained and the
   measured one recorded with `design_log.py add --language`
6. `slop_lint.py` grade A/B **with the language read**: no `design-language-unrecorded` / `-unmeasured`; genre-native
   devices (a centred dev-tool hero, dense documentation rows, raw brutalist controls) not "fixed" into the skill's
   language
7. Nothing from `design-language.md` §7 on the page: no untouched theme values, reflex typeface without a brand line,
   purple gradient, glow, fake proof
8. The bold move, the anchor and the signature interaction are in the page's language (a playground, a live search,
   a picker beside the photograph), not a poster bolted onto a dev tool
9. `design_log.py check` shows no "design language" warning left unanswered: no two unrelated industries in one
   language
10. **The board test.** Each page's first screen beside its own real competitor's first screen and beside the other
    nine pages: a viewer who does not know the skill says which world each page belongs to from the competitor, and
    cannot say which pages came from the same studio. Score 2 when ≥ 8 of 10 pass both halves.

Minimum passing: 16 of 20, with item 10 at 2.

## What to record

The ten `Market:` lines and `Design language:` lines side by side; the count of distinct languages (expect ≥ 7 of
10 on ≥ 4 axes); the board; the studio crit scores. A run where every page lands on one calibration point from
`design-language.md` §6 has turned the calibration table into the next menu — that is a failure of the skill, not
of the run.
