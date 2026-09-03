# Evals

Scenarios to test the skill against a model before and after changes. Run each prompt in a fresh session with the
skill loaded, then grade the output with the rubric. A change to `SKILL.md` or a reference should not lower any
score. Keep transcripts and screenshots under `evals/runs/{date}-{model}/` (git-ignored).

| Scenario | Tests | File |
|---|---|---|
| 01 New product landing page | full path: brief → research → moodboard → tokens → compose → review; Persuade mode; honesty; anti-skeleton | `01-new-saas-landing.md` |
| 02 Feature inside an existing design system | detection and adoption; no new visual language; Operate mode; state matrix; drift report | `02-existing-system-feature.md` |
| 03 Native iOS screen | platform posture; HIG; Liquid Glass rules; Dynamic Type; token mapping to SwiftUI | `03-ios-screen.md` |
| Fixture | `fixtures/slop-sample.html` must grade D or F in `scripts/slop_lint.py`; `templates/moodboard.html` must grade A or B | — |

## Grading

Each scenario lists rubric items scored 0 / 1 / 2 (missing / partial / complete). Report the total and the failures.
Also record: did the model load the right references at the right phase, did it ask one intake message (not a
questionnaire), did it fabricate anything, and the `slop_lint.py` grade of whatever it built.

Minimum passing: ≥ 80% of rubric points, zero fabricated content, slop grade A or B, no WCAG AA failure in
`contrast.py --tokens`.
