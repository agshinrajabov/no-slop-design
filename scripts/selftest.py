#!/usr/bin/env python3
"""
selftest.py — prove the tools still catch what they claim to catch.

Runs the four scripts against the fixtures in `evals/fixtures/` and the starter tokens in `templates/tokens/`,
and asserts on the findings, not just on exit codes. A rule that stops firing is a silent regression: the skill
would keep grading its own output A while shipping the thing the rule exists to catch.

Usage:
  python3 scripts/selftest.py        # prints one line per case, exit 1 on failure
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY = sys.executable or "python3"
failures: list[str] = []
passes = 0


def run(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run([PY, *args], cwd=ROOT, capture_output=True, text=True)


def check(name: str, condition: bool, detail: str = "") -> None:
    global passes
    if condition:
        passes += 1
        print(f"  ok   {name}")
    else:
        failures.append(f"{name}: {detail}")
        print(f"  FAIL {name} — {detail}")


def lint_json(*paths: str) -> dict:
    p = run("scripts/slop_lint.py", *paths, "--json")
    return json.loads(p.stdout)


def main() -> int:
    print("slop_lint — the classic tells still fire")
    slop = lint_json("evals/fixtures/slop-sample.html")
    rules = {f["rule"] for f in slop["findings"]}
    for r in ("purple-gradient", "default-font", "icon-circle", "emoji-ui", "slop-copy"):
        check(f"{r} on slop-sample", r in rules, f"rules found: {sorted(rules)}")
    check("slop-sample graded D or F", slop["grade"] in ("D", "F"), f"grade {slop['grade']}")

    print("slop_lint — the over-correction tells fire")
    ledger = lint_json("evals/fixtures/ledger-site.html")
    lrules = {f["rule"] for f in ledger["findings"]}
    check("ledger-site", "ledger-site" in lrules, f"rules found: {sorted(lrules)}")
    check("thin-imagery", "thin-imagery" in lrules, f"rules found: {sorted(lrules)}")

    print("slop_lint — reveal without a no-JS fallback fires, and a guarded one does not")
    with tempfile.TemporaryDirectory() as d:
        bad = os.path.join(d, "reveal-bad.html")
        good = os.path.join(d, "reveal-good.html")
        css = "@media (prefers-reduced-motion: no-preference){.reveal{opacity:0}.reveal.is-in{opacity:1}}"
        open(bad, "w").write(f"<html><head><style>{css}</style></head><body><main><section class='reveal'>x</section></main></body></html>")
        open(good, "w").write(
            f"<html><head><script>document.documentElement.classList.add('js')</script><style>{css}</style>"
            f"<noscript><style>.reveal{{opacity:1!important}}</style></noscript></head>"
            f"<body><main><section class='reveal'>x</section></main></body></html>")
        b = lint_json(bad)
        g = lint_json(good)
        check("reveal-no-fallback on unguarded reveal", "reveal-no-fallback" in {f["rule"] for f in b["findings"]},
              f"rules: {sorted({f['rule'] for f in b['findings']})}")
        check("no false positive on guarded reveal", "reveal-no-fallback" not in {f["rule"] for f in g["findings"]},
              "guarded page was flagged")

    print("slop_lint — working documents are exempt")
    mood = lint_json("templates/moodboard.html")
    check("moodboard template grades A", mood["grade"] == "A", f"grade {mood['grade']}, rules "
          f"{sorted({f['rule'] for f in mood['findings']})}")

    print("build_tokens — palette sanity")
    indigo = run("scripts/build_tokens.py", "evals/fixtures/indigo-accent.json", "--check")
    check("imported indigo accent warns", "blue/indigo/violet band" in indigo.stdout, indigo.stdout.strip()[:120])
    check("untinted neutrals warn", "pure gray" in indigo.stdout, indigo.stdout.strip()[:120])

    starter = run("scripts/build_tokens.py", *[f"templates/tokens/{f}" for f in
                                               ("primitives.json", "semantic.json", "semantic.dark.json", "components.json")],
                  "--check")
    check("starter tokens have no errors", starter.returncode == 0, starter.stdout.strip()[:200])
    check("starter tokens have no palette warnings", "warning: palette" not in starter.stdout,
          starter.stdout.strip()[:200])

    print("build_tokens — .tokens.json is the DTCG extension, not a mode")
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "x.tokens.json")
        open(p, "w").write(json.dumps({"color": {"$type": "color", "a": {"$value": "#123456"}}}))
        out = run("scripts/build_tokens.py", p, "--check").stdout
        check("no phantom 'tokens' mode", "modes: none" in out, out.strip()[:120])

    print("contrast — the starter palette passes in both modes")
    with tempfile.TemporaryDirectory() as d:
        run("scripts/build_tokens.py", *[f"templates/tokens/{f}" for f in
                                         ("primitives.json", "semantic.json", "semantic.dark.json", "components.json")],
            "--out", d, "--format", "flat-json")
        c = run("scripts/contrast.py", "--tokens", os.path.join(d, "tokens.flat.json"))
        check("no WCAG AA failures in the starter palette", c.returncode == 0,
              "\n".join(l for l in c.stdout.splitlines() if "FAIL" in l)[:300])
    fail = run("scripts/contrast.py", "#8f8f8f", "#ffffff")          # 3.4:1 — below AA for body text
    check("contrast exits 1 on a failing pair at 16px", fail.returncode == 1, fail.stdout.strip()[:120])
    edge = run("scripts/contrast.py", "#767676", "#ffffff")           # 4.54:1 — passes AA, APCA still says large-only
    check("contrast exits 0 on a barely-passing pair", edge.returncode == 0, edge.stdout.strip()[:120])

    print("type_scale — emits a fluid scale")
    ts = run("scripts/type_scale.py", "--format", "css")
    check("type_scale css output", "clamp(" in ts.stdout and "--text-base" in ts.stdout, ts.stdout[:120])

    print("repo audit")
    a = run("scripts/audit_repo.py")
    check("audit_repo passes", a.returncode == 0, a.stdout.strip()[-400:])

    print(f"\n{passes} passed, {len(failures)} failed")
    for f in failures:
        print("  -", f)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
