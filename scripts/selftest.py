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

    print("slop_lint — imagery performance and provenance")
    with tempfile.TemporaryDirectory() as d:
        os.makedirs(os.path.join(d, "design"))
        open(os.path.join(d, "design", "assets.md"), "w").write("| P1 | hero | street | photo-1608315172253 | Unsplash | ok |\n")
        page = os.path.join(d, "index.html")
        open(page, "w").write(
            "<html><body><main><section><h1>x</h1>"
            "<img src='https://images.unsplash.com/photo-1608315172253?w=1600' loading='lazy' alt='a'>"
            "<img src='https://images.unsplash.com/photo-9999999999999?w=800' width='800' height='600' alt='b'>"
            "</section></main></body></html>")
        rules = {f["rule"] for f in lint_json(page)["findings"]}
        check("lcp-lazy", "lcp-lazy" in rules, f"rules: {sorted(rules)}")
        check("img-no-dimensions", "img-no-dimensions" in rules, f"rules: {sorted(rules)}")
        check("asset-unrecorded", "asset-unrecorded" in rules, f"rules: {sorted(rules)}")

    print("design_log — cross-project convergence")
    with tempfile.TemporaryDirectory() as d:
        env = dict(os.environ, NSD_HISTORY=os.path.join(d, "history.json"))
        for i, (proj, ind) in enumerate([("a", "dental"), ("b", "coffee"), ("c", "law")]):
            subprocess.run([PY, "scripts/design_log.py", "add", "--project", proj, "--register", "R2",
                            "--surface", "dark", "--hue", "40", "--display", "Fraunces",
                            "--structure", "fact ledger beside headline", "--industry", ind],
                           cwd=ROOT, capture_output=True, text=True, env=env)
        out = subprocess.run([PY, "scripts/design_log.py", "check"], cwd=ROOT, capture_output=True, text=True, env=env).stdout
        check("streak on surface polarity is reported", "surface polarity" in out, out.strip()[-200:])
        check("same-surface across industries is called the skill's own tell", "skill's own tell" in out, out.strip()[-200:])
        subprocess.run([PY, "scripts/design_log.py", "add", "--project", "d", "--register", "R3", "--surface", "light",
                        "--hue", "66", "--display", "Archivo Expanded", "--structure", "full-bleed photo",
                        "--industry", "festival"], cwd=ROOT, capture_output=True, text=True, env=env)
        out2 = subprocess.run([PY, "scripts/design_log.py", "check"], cwd=ROOT, capture_output=True, text=True, env=env).stdout
        check("breaking two axes clears the warnings", "no convergence warnings" in out2, out2.strip()[-200:])

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

    print("build_tokens — OKLCH survives into the native emitters")
    with tempfile.TemporaryDirectory() as d:
        base, dark = os.path.join(d, "t.json"), os.path.join(d, "t.dark.json")
        open(base, "w").write(json.dumps({"color": {"$type": "color", "brand": {"9": {"$value": "oklch(0.58 0.17 40)"}},
                                                    "obj": {"1": {"$value": {"colorSpace": "oklch", "components": [0.6, 0.1, 200]}}}},
                                          "space": {"$type": "dimension", "4": {"$value": "16px"}}}))
        open(dark, "w").write(json.dumps({"color": {"$type": "color", "brand": {"9": {"$value": "oklch(0.72 0.13 40)"}}}}))
        run("scripts/build_tokens.py", base, dark, "--out", d, "--format", "swift,kotlin,dart")
        sw = open(os.path.join(d, "DesignTokens.swift")).read()
        kt = open(os.path.join(d, "DesignTokens.kt")).read()
        dt = open(os.path.join(d, "design_tokens.dart")).read()
        check("swift keeps the OKLCH token", "colorBrand9" in sw, sw[:200])
        check("swift emits the dark variant", "userInterfaceStyle" in sw, sw[:200])
        check("kotlin keeps the OKLCH token", "colorBrand9 = Color(0xFFC94C18)" in kt, kt[:200])
        check("dart keeps the OKLCH token", "colorBrand9 = Color(0xFFC94C18)" in dt, dt[:200])
        check("DTCG colour objects resolve too", "colorObj1" in kt, kt[:200])

    print("slop_lint — page rules judge rendered documents, not component source")
    with tempfile.TemporaryDirectory() as d:
        tsx = os.path.join(d, "page.tsx")
        open(tsx, "w").write("<main><section><h1>x</h1><Panel title='a'/></section></main>" + "x" * 4000)
        check("no no-imagery on a .tsx that composes components",
              "no-imagery" not in {f["rule"] for f in lint_json(tsx)["findings"]}, "tsx was flagged")

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
