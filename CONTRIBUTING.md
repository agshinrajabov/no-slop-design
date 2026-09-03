# Contributing

## What helps most

1. **New tells** for `references/anti-slop.md` — include where you saw it (URL/screenshot) and the "do instead".
2. **Linter accuracy** — false positives/negatives in `scripts/slop_lint.py` with a minimal snippet.
3. **Platform updates** — HIG, Material, WCAG, DTCG changes with a source and date.
4. **Eval scenarios** in `evals/` that expose a weak spot, with a rubric.
5. **Translations of the README** (the skill itself stays in English so every model reads it the same way).

## Style

- Dense, numeric, tables over prose. No marketing language; the banned list in `references/content-microcopy.md` applies to this repo too.
- `SKILL.md` stays under 500 lines and only routes; depth goes into `references/`, one level deep, each with a table of contents.
- Every reference is actionable by an agent: exact values, exact attribute names, "use when / avoid when".
- Scripts: Python 3.9+, standard library only, `--help` text, exit codes usable in CI.

## Checks before a PR

```bash
python3 scripts/build_tokens.py templates/tokens/*.json --check
python3 scripts/build_tokens.py templates/tokens/*.json --out /tmp/nsd --format flat-json && python3 scripts/contrast.py --tokens /tmp/nsd/tokens.flat.json
python3 scripts/slop_lint.py evals/fixtures/slop-sample.html          # must grade D or F
python3 scripts/slop_lint.py templates/moodboard.html                  # must grade A or B
claude plugin validate .                                               # if Claude Code is installed
```

## Versioning

Semver on `SKILL.md` metadata, `.claude-plugin/plugin.json`, and `.claude-plugin/marketplace.json` together.
Changes to workflow phases or non-negotiables = minor; reference-only additions = patch; renamed files or scripts = major.
