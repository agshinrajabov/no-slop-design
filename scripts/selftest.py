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

    print("slop_lint — imagery follows the direction, not a quota")
    rules_of = lambda p: {f["rule"] for f in lint_json(p)["findings"]}
    check("no thin-imagery when no photographic anchor was declared", "thin-imagery" not in lrules,
          "the linter still demands images from an undeclared page")
    fixture = open(os.path.join(ROOT, "evals/fixtures/ledger-site.html"), encoding="utf-8").read()
    long_copy = "<p>" + "Real body copy for a real page. " * 400 + "</p>"
    with tempfile.TemporaryDirectory() as d:
        os.makedirs(os.path.join(d, "design"))
        open(os.path.join(d, "design", "DESIGN.md"), "w").write("Anchor type: full-bleed photograph.\n")
        p = os.path.join(d, "index.html"); open(p, "w").write(fixture)
        check("thin-imagery when the direction chose photography", "thin-imagery" in rules_of(p), sorted(rules_of(p)))
    with tempfile.TemporaryDirectory() as d:
        os.makedirs(os.path.join(d, "design"))
        open(os.path.join(d, "design", "DESIGN.md"), "w").write("**Anchor type:** type as image.\n")
        typo = f"<html><body><header><h1>Brød</h1></header><main><section>{long_copy}</section></main></body></html>"
        p = os.path.join(d, "index.html"); open(p, "w").write(typo)
        check("typographic anchor needs no photographs", "no-imagery" not in rules_of(p), sorted(rules_of(p)))
        photos = "".join(f"<img src='https://images.unsplash.com/photo-{i}' width='800' height='600' alt='x'>" for i in range(4))
        p2 = os.path.join(d, "stuffed.html"); open(p2, "w").write(typo.replace("</main>", photos + "</main>"))
        check("photographs against a typographic direction are flagged", "images-contradict-direction" in rules_of(p2),
              sorted(rules_of(p2)))
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "index.html")
        open(p, "w").write(f"<html><body><header data-nsd-anchor='colour field'><h1>x</h1></header><main><section>{long_copy}</section></main></body></html>")
        check("data-nsd-anchor on the page is honoured", "no-imagery" not in rules_of(p), sorted(rules_of(p)))
        q = os.path.join(d, "undecided.html")
        open(q, "w").write(f"<html><body><header><h1>x</h1></header><main><section>{long_copy}</section></main></body></html>")
        check("an undecided text-only page is still flagged", "no-imagery" in rules_of(q), sorted(rules_of(q)))
    with tempfile.TemporaryDirectory() as d:
        secs = "".join(f"<section><h2>s{i}</h2><img src='https://images.unsplash.com/photo-{i}' width='800' height='600' alt='x'><p>copy</p></section>" for i in range(6))
        p = os.path.join(d, "index.html"); open(p, "w").write(f"<html><body><main>{secs}{long_copy}</main></body></html>")
        check("photo-stuffing on an image in every section", "photo-stuffing" in rules_of(p), sorted(rules_of(p)))

    print("slop_lint — a persuasive page needs a signature interaction")
    with tempfile.TemporaryDirectory() as d:
        brochure = (f"<html><body><header><nav><button type='button'>AZ</button></nav></header><main><section>{long_copy}</section>"
                    "<form><input name='n'><output aria-live='polite'></output><button type='submit'>Send</button></form></main></body></html>")
        p = os.path.join(d, "brochure.html"); open(p, "w", encoding="utf-8").write(brochure)
        check("brochure page (switcher + contact form only) is flagged", "no-signature-interaction" in rules_of(p), sorted(rules_of(p)))
        est = brochure.replace("</section>", "</section><section><label>Pages <input type='number' value='1'></label><output aria-live='polite'>20 AZN</output></section>", 1)
        p2 = os.path.join(d, "estimator.html"); open(p2, "w", encoding="utf-8").write(est)
        check("an estimator with an announced result passes", "no-signature-interaction" not in rules_of(p2), sorted(rules_of(p2)))
        p3 = os.path.join(d, "declared.html"); open(p3, "w", encoding="utf-8").write(brochure.replace("<main>", "<main data-nsd-interaction='availability'>"))
        check("data-nsd-interaction is honoured", "no-signature-interaction" not in rules_of(p3), sorted(rules_of(p3)))

    print("design_log — two same-surface runs in a row already count")
    with tempfile.TemporaryDirectory() as d:
        env = dict(os.environ, NSD_HISTORY=os.path.join(d, "h.json"))
        for proj in ("x", "y"):
            subprocess.run([PY, "scripts/design_log.py", "add", "--project", proj, "--surface", "dark", "--register", "R2",
                            "--hue", "30", "--interaction", "I1"], cwd=ROOT, capture_output=True, text=True, env=env)
        out = subprocess.run([PY, "scripts/design_log.py", "check"], cwd=ROOT, capture_output=True, text=True, env=env).stdout
        check("surface streak warns after two runs", "surface polarity" in out, out.strip()[-160:])

    print("design_log — surface polarity is measured from pixels, not declared")
    import struct as _st, zlib as _zl

    def png(path, w, h, dark_rows):
        raw = b"".join(b"\x00" + (b"\x10\x10\x10" if y < dark_rows else b"\xf0\xf0\xf0") * w for y in range(h))
        chunk = lambda t, data: _st.pack(">I", len(data)) + t + data + _st.pack(">I", _zl.crc32(t + data) & 0xFFFFFFFF)
        open(path, "wb").write(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", _st.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
                               + chunk(b"IDAT", _zl.compress(raw)) + chunk(b"IEND", b""))

    with tempfile.TemporaryDirectory() as d:
        env = dict(os.environ, NSD_HISTORY=os.path.join(d, "h.json"))
        shot = os.path.join(d, "page.png"); png(shot, 40, 40, 28)
        m = subprocess.run([PY, "scripts/design_log.py", "measure", shot], cwd=ROOT, capture_output=True, text=True, env=env).stdout
        check("measure reads a mostly dark page as dark", "surface polarity: dark" in m, m.strip())
        a = subprocess.run([PY, "scripts/design_log.py", "add", "--project", "p", "--surface", "light", "--screenshot", shot],
                           cwd=ROOT, capture_output=True, text=True, env=env).stdout
        check("a declared 'light' over a dark screenshot is corrected", "recording 'dark'" in a, a.strip()[-200:])

    print("slop_lint — the interaction result must stay on screen on phones")
    with tempfile.TemporaryDirectory() as d:
        page = (f"<html><body><main data-nsd-interaction='estimator'><section><select></select><input type='number'><input type='date'><input type='checkbox'><output aria-live='polite'>1</output>"
                f"</section><section>{long_copy}</section></main></body></html>")
        p = os.path.join(d, "a.html"); open(p, "w", encoding="utf-8").write(page)
        check("no sticky result is flagged", "interaction-result-offscreen" in rules_of(p), sorted(rules_of(p)))
        open(os.path.join(d, "s.css"), "w").write(".result{position:sticky;bottom:0}")
        linked = page.replace("<body>", "<head><link rel='stylesheet' href='s.css'></head><body>")
        p2 = os.path.join(d, "b.html")
        open(p2, "w", encoding="utf-8").write(linked.replace("</main>", "<div class='result'>AZN 1</div></main>"))
        check("a visible sticky result in the linked stylesheet passes", "interaction-result-offscreen" not in rules_of(p2), sorted(rules_of(p2)))
        p3 = os.path.join(d, "c.html")
        open(p3, "w", encoding="utf-8").write(linked.replace("</main>", "<div class='result' hidden>AZN 1</div></main>"))
        check("a sticky result hidden by default is still flagged", "interaction-result-offscreen" in rules_of(p3), sorted(rules_of(p3)))
        p4 = os.path.join(d, "e.html")
        open(p4, "w", encoding="utf-8").write(page.replace("<body>", "<head><style>.site-header{position:sticky;top:0}</style></head><body><header class='site-header'>x</header>"))
        check("a sticky header alone does not count", "interaction-result-offscreen" in rules_of(p4), sorted(rules_of(p4)))

    print("slop_lint — neon-on-black means a black background, not a token primitive")
    with tempfile.TemporaryDirectory() as d:
        tok = os.path.join(d, "tokens.css"); open(tok, "w").write(":root{--color-black:#000000;--color-white:#fff}")
        check("a black primitive in a token file is not a black page", "neon-on-black" not in rules_of(tok), sorted(rules_of(tok)))
        bg = os.path.join(d, "page.css"); open(bg, "w").write("body{background:#000000;color:#39ff14}")
        check("a black page background still fires", "neon-on-black" in rules_of(bg), sorted(rules_of(bg)))

    print("slop_lint — tables on phones, and tables as the page")
    with tempfile.TemporaryDirectory() as d:
        tbl = "<table><tr><th>a</th><th>b</th></tr><tr><td>1</td><td>2</td></tr></table>"
        base = (f"<html><head><style>.scroll{{overflow-x:auto}}</style></head><body><main>"
                f"<section data-nsd-interaction='estimator'><input type='number'><output aria-live='polite'>1</output>{tbl}</section>"
                f"<section>{long_copy}<div class='scroll'>{tbl}</div></section></main></body></html>")
        p = os.path.join(d, "a.html"); open(p, "w", encoding="utf-8").write(base)
        check("a scrolling table with no cue is flagged", "table-scroll-no-cue" in rules_of(p), sorted(rules_of(p)))
        check("one table outside the interaction is not tables-as-sections", "tables-as-sections" not in rules_of(p), sorted(rules_of(p)))
        cued = base.replace(".scroll{overflow-x:auto}", ".scroll{overflow-x:auto;background:linear-gradient(#fff,#fff) left/2rem 100% no-repeat local}")
        p2 = os.path.join(d, "b.html"); open(p2, "w", encoding="utf-8").write(cued)
        check("scroll shadows count as a cue", "table-scroll-no-cue" not in rules_of(p2), sorted(rules_of(p2)))
        reflow = base.replace(".scroll{overflow-x:auto}", ".scroll{overflow-x:auto}@media (max-width:480px){.scroll tr{display:grid}}")
        p3 = os.path.join(d, "c.html"); open(p3, "w", encoding="utf-8").write(reflow)
        check("a narrow reflow counts as a cue", "table-scroll-no-cue" not in rules_of(p3), sorted(rules_of(p3)))
        two = base.replace("</main>", f"<section>{tbl}</section></main>")
        p4 = os.path.join(d, "d.html"); open(p4, "w", encoding="utf-8").write(two)
        check("two tables outside the interaction are flagged", "tables-as-sections" in rules_of(p4), sorted(rules_of(p4)))
        os.makedirs(os.path.join(d, "design"))
        open(os.path.join(d, "design", "DESIGN.md"), "w").write("| Surface mode | Operate |\n")
        check("an Operate surface may be tables", "tables-as-sections" not in rules_of(p4), sorted(rules_of(p4)))

    print("slop_lint — review scaffolding stays out of the deliverable")
    with tempfile.TemporaryDirectory() as d:
        page = f"<html><body><main><section data-nsd-anchor='colour field'>{long_copy}</section></main></body></html>"
        p = os.path.join(d, "index.html"); open(p, "w", encoding="utf-8").write(page)
        check("a clean project has no scaffolding finding", "review-scaffolding" not in rules_of(p), sorted(rules_of(p)))
        frame = os.path.join(d, "frame-375.html")
        open(frame, "w").write("<html><body style='margin:0'><iframe src='index.html' style='width:375px;height:812px'></iframe></body></html>")
        check("a wrapper page framing the product is flagged", "review-scaffolding" in rules_of(frame), sorted(rules_of(frame)))
        os.makedirs(os.path.join(d, "shots")); open(os.path.join(d, "shots", "desktop.png"), "wb").write(b"x")
        check("a shots/ folder beside the page is flagged", "review-scaffolding" in rules_of(p), sorted(rules_of(p)))

    print("slop_lint — the page speaks the market's language")
    with tempfile.TemporaryDirectory() as d:
        os.makedirs(os.path.join(d, "design"))
        open(os.path.join(d, "design", "DESIGN.md"), "w").write("| Primary language | az — Azerbaijani, RU as switcher |\n")
        body = f"<body><main><section data-nsd-anchor='colour field'>{long_copy}</section></main></body></html>"
        en = os.path.join(d, "en.html"); open(en, "w", encoding="utf-8").write("<html lang='en'>" + body)
        check("an English page for a declared Azerbaijani market is flagged", "page-language" in rules_of(en), sorted(rules_of(en)))
        az = os.path.join(d, "az.html"); open(az, "w", encoding="utf-8").write("<html lang=\"az-Latn-AZ\">" + body)
        check("lang='az-Latn-AZ' matches 'az'", "page-language" not in rules_of(az), sorted(rules_of(az)))
        nolang = os.path.join(d, "nolang.html"); open(nolang, "w", encoding="utf-8").write("<html>" + body)
        check("a page without lang is flagged", "page-language" in rules_of(nolang), sorted(rules_of(nolang)))

    print("slop_lint — the estimate is a number, and the design record is complete")
    with tempfile.TemporaryDirectory() as d:
        page = (f"<html lang='az'><body><main><section data-nsd-interaction='estimator' data-nsd-anchor='diagram'>"
                f"<select id='doc'></select><output aria-live='polite'>müddət: [n] iş günü</output></section>"
                f"<section>{long_copy}</section></main></body></html>")
        p = os.path.join(d, "index.html"); open(p, "w", encoding="utf-8").write(page)
        check("[n] in the estimator's result is flagged", "placeholder-result" in rules_of(p), sorted(rules_of(p)))
        open(p, "w", encoding="utf-8").write(page.replace("[n] iş günü", "5 iş günü (nümunə tarif)"))
        check("a labelled sample number passes", "placeholder-result" not in rules_of(p), sorted(rules_of(p)))
        os.makedirs(os.path.join(d, "design")); open(os.path.join(d, "design", "DESIGN.md"), "w").write("x")
        check("a design/ folder without the brief is incomplete", "design-record-incomplete" in rules_of(p), sorted(rules_of(p)))
        for n in ("design/brief.md", "design/assets.md", "design/design-log.json", "design/contrast-pairs.txt"):
            open(os.path.join(d, n), "w").write("x")
        os.makedirs(os.path.join(d, "tokens"))
        for n in ("tokens/primitives.json", "tokens/semantic.json"):
            open(os.path.join(d, n), "w").write("{}")
        check("a complete design record passes", "design-record-incomplete" not in rules_of(p), sorted(rules_of(p)))

    print("design_log — the same first-viewport composition in two industries is a house style")
    with tempfile.TemporaryDirectory() as d:
        env = dict(os.environ, NSD_HISTORY=os.path.join(d, "h.json"))
        for proj, ind, hue, surf in [("t", "translation", 25, "light"), ("c", "clinic", 90, "dark")]:
            subprocess.run([PY, "scripts/design_log.py", "add", "--project", proj, "--industry", ind, "--hue", str(hue),
                            "--surface", surf, "--composition", "result-poster"], cwd=ROOT, capture_output=True, text=True, env=env)
        out = subprocess.run([PY, "scripts/design_log.py", "check"], cwd=ROOT, capture_output=True, text=True, env=env).stdout
        check("two result-posters in a row warn across industries", "composition" in out and "result-poster" in out, out.strip()[-240:])
        subprocess.run([PY, "scripts/design_log.py", "add", "--project", "h", "--industry", "hotel", "--hue", "200",
                        "--surface", "light", "--composition", "graphic-hero"], cwd=ROOT, capture_output=True, text=True, env=env)
        out2 = subprocess.run([PY, "scripts/design_log.py", "check"], cwd=ROOT, capture_output=True, text=True, env=env).stdout
        check("a different composition clears it", "composition:" not in out2, out2.strip()[-240:])

    print("design_log — the house skeleton and a run of imageless pages are warned")
    with tempfile.TemporaryDirectory() as d:
        env = dict(os.environ, NSD_HISTORY=os.path.join(d, "h.json"))
        for proj, ind, comp in [("a", "translation", "type-poster"), ("b", "clinic", "graphic-hero"), ("c", "law", "field-and-heading")]:
            subprocess.run([PY, "scripts/design_log.py", "add", "--project", proj, "--industry", ind, "--composition", comp,
                            "--skeleton", "interaction>steps>table>form", "--media", "0"], cwd=ROOT, capture_output=True, text=True, env=env)
        out = subprocess.run([PY, "scripts/design_log.py", "check"], cwd=ROOT, capture_output=True, text=True, env=env).stdout
        check("the same skeleton twice is warned", "skeleton:" in out, out.strip()[-300:])
        check("three imageless pages are warned", "imagery:" in out, out.strip()[-300:])
        subprocess.run([PY, "scripts/design_log.py", "add", "--project", "d", "--industry", "hotel", "--composition", "graphic-hero",
                        "--skeleton", "media>text>interaction>media", "--media", "7"], cwd=ROOT, capture_output=True, text=True, env=env)
        out2 = subprocess.run([PY, "scripts/design_log.py", "check"], cwd=ROOT, capture_output=True, text=True, env=env).stdout
        check("a different skeleton with images clears both", "skeleton:" not in out2 and "imagery:" not in out2, out2.strip()[-300:])

    print("design_log — result forms, openings, endings, and runs in parallel")
    with tempfile.TemporaryDirectory() as d:
        env = dict(os.environ, NSD_HISTORY=os.path.join(d, "h.json"))
        log = lambda *a: subprocess.run([PY, "scripts/design_log.py", *a], cwd=ROOT, capture_output=True, text=True, env=env).stdout
        log("add", "--project", "bakery", "--result-form", "paper", "--skeleton", "media>interaction>text>form")
        log("add", "--project", "law", "--result-form", "paper", "--skeleton", "media>interaction>table>form")
        out = log("check")
        check("two paper results in a row warn", "result form:" in out, out.strip()[-300:])
        check("the same opening twice warns", "opening:" in out, out.strip()[-300:])
        refused = subprocess.run([PY, "scripts/design_log.py", "plan", "--project", "x", "--result-form", "map"],
                                 cwd=ROOT, capture_output=True, text=True, env=env)
        check("plan refuses without a composition", refused.returncode == 2 and "--composition" in refused.stdout, refused.stdout[-160:])
        planned = log("plan", "--project", "hotel", "--result-form", "paper", "--composition", "graphic-hero")
        check("plan warns before building", "result form:" in planned, planned.strip()[-300:])
        check("a planned run is visible to check", "[planned]" in log("check"), "not listed")
        log("add", "--project", "hotel", "--result-form", "calendar", "--skeleton", "media>text>interaction>map")
        after = log("check")
        check("finishing a run replaces its plan", "[planned]" not in after, after.strip()[-300:])

    print("design_log — poster type as a habit, and the image model's house look")
    with tempfile.TemporaryDirectory() as d:
        env = dict(os.environ, NSD_HISTORY=os.path.join(d, "h.json"))
        log = lambda *a: subprocess.run([PY, "scripts/design_log.py", *a], cwd=ROOT, capture_output=True, text=True, env=env).stdout
        for proj, ratio, look in [("law", "9.2", "none"), ("bakery", "33.3", "eye-level;side-window;wood;warm"),
                                  ("restaurant", "8.8", "close-up;side-window;wood;warm")]:
            log("add", "--project", proj, "--display-ratio", ratio, "--image-look", look)
        out = log("check")
        check("three oversized-type openings warn", "type scale:" in out, out.strip()[-300:])
        check("two pages with the same image look warn", "image look:" in out, out.strip()[-300:])
        bad = subprocess.run([PY, "scripts/design_log.py", "add", "--project", "y", "--image-look", "top-down;overcast;limestone;neutral"],
                             cwd=ROOT, capture_output=True, text=True, env=env)
        check("free words outside the look vocabulary are refused", bad.returncode == 2 and "stone" in bad.stdout, bad.stdout[-200:])
        log("add", "--project", "rest2", "--display-ratio", "4.7", "--image-look", "top-down;overcast;stone;warm")
        log("add", "--project", "ceram2", "--display-ratio", "3.5", "--image-look", "top-down;overcast;stone;neutral")
        check("two top-down shots on stone warn even with different palettes", "image look:" in log("check"), "not warned")
        log("add", "--project", "hotel", "--display-ratio", "4.5", "--image-look", "wide;dusk-night;street;cool")
        out2 = log("check")
        check("a proportionate type and a different look clear both", "type scale:" not in out2 and "image look:" not in out2,
              out2.strip()[-300:])

    print("slop_lint — brand-fixed fonts are the brief's choice, portraits are not colour slabs")
    with tempfile.TemporaryDirectory() as d:
        os.makedirs(os.path.join(d, "design"))
        page = (f"<html lang='de'><head><style>body{{font-family: Inter, sans-serif}}</style></head><body><main>"
                f"<section data-nsd-anchor='colour field'>{long_copy}</section></main></body></html>")
        p = os.path.join(d, "index.html"); open(p, "w", encoding="utf-8").write(page)
        check("Inter without a brand decision is flagged", "default-font" in rules_of(p), sorted(rules_of(p)))
        open(os.path.join(d, "design", "brief.md"), "w").write("- **Brand assets fixed:** colour `#0F766E`, typeface Inter.\n")
        check("Inter fixed by the brand passes", "default-font" not in rules_of(p), sorted(rules_of(p)))
        slab = page.replace("</main>", "<section><div class='portrait' role='img' aria-label='Portrait to come'>Divorce</div></section></main>")
        open(p, "w", encoding="utf-8").write(slab)
        check("a portrait colour slab is flagged", "people-placeholder-slab" in rules_of(p), sorted(rules_of(p)))
        open(p, "w", encoding="utf-8").write(slab.replace(">Divorce</div>", "><svg viewBox='0 0 40 50'><circle cx='20' cy='16' r='10'/></svg></div>"))
        check("a silhouette placeholder passes", "people-placeholder-slab" not in rules_of(p), sorted(rules_of(p)))

    print("slop_lint — menu and product photographs are content, and warnings need an answer")
    with tempfile.TemporaryDirectory() as d:
        os.makedirs(os.path.join(d, "design"))
        open(os.path.join(d, "design", "DESIGN.md"), "w").write("Anchor type: diagram\n")
        dishes = "".join(f"<li class='dish'><img src='d{i}.jpg' width='400' height='500' alt='dish'></li>" for i in range(3))
        page = (f"<html lang='az'><body><main><section><svg viewBox='0 0 800 600' width='800'></svg><h1>40 yer</h1></section>"
                f"<section id='menu'><ul class='dishes'>{dishes}</ul></section><section>{long_copy}</section></main></body></html>")
        p = os.path.join(d, "index.html"); open(p, "w", encoding="utf-8").write(page)
        check("menu photos on a diagram-anchored page are content", "images-contradict-direction" not in rules_of(p), sorted(rules_of(p)))
        stray = page.replace("<h1>40 yer</h1>", "<h1>40 yer</h1>" + "".join(f"<img src='h{i}.jpg' width='800' height='600' alt='x'>" for i in range(3)))
        open(p, "w", encoding="utf-8").write(stray)
        check("photos outside the content sections still contradict", "images-contradict-direction" in rules_of(p), sorted(rules_of(p)))
        open(p, "w", encoding="utf-8").write(page)
        env = dict(os.environ, NSD_HISTORY=os.path.join(d, "h.json"))
        wf = os.path.join(d, "design", "convergence-warnings.json")
        for proj in ("a", "b"):
            subprocess.run([PY, "scripts/design_log.py", "add", "--project", proj, "--composition", "graphic-hero"],
                           cwd=ROOT, capture_output=True, text=True, env=env)
        rec = subprocess.run([PY, "scripts/design_log.py", "check", "--record", wf], cwd=ROOT, capture_output=True, text=True, env=env)
        check("check --record writes the warnings", os.path.exists(wf) and "composition" in open(wf).read(), rec.stdout[-200:])
        check("an unanswered warning is flagged", "convergence-unanswered" in rules_of(p), sorted(rules_of(p)))
        open(os.path.join(d, "design", "DESIGN.md"), "a").write(
            "\n**Convergence overrides**\n- composition: the floor plan is the booking itself, and no other run drew a room\n")
        check("a written answer clears it", "convergence-unanswered" not in rules_of(p), sorted(rules_of(p)))

    print("design_log — a re-plan replaces the project's own plan; slop_lint — proposals are marked")
    with tempfile.TemporaryDirectory() as d:
        env = dict(os.environ, NSD_HISTORY=os.path.join(d, "h.json"))
        log = lambda *a: subprocess.run([PY, "scripts/design_log.py", *a], cwd=ROOT, capture_output=True, text=True, env=env).stdout
        log("plan", "--project", "shop", "--composition", "type-poster", "--result-form", "card", "--image-look", "eye-level;hard-sun;paper;warm")
        second = log("plan", "--project", "shop", "--composition", "graphic-hero", "--result-form", "card", "--image-look", "eye-level;hard-sun;paper;warm")
        check("re-planning does not warn against its own plan", "result form:" not in second and "image look:" not in second, second[-300:])
        stored = json.load(open(os.path.join(d, "h.json")))["entries"]
        check("only one plan per project is kept", sum(1 for e in stored if e.get("project") == "shop") == 1, str(len(stored)))
    with tempfile.TemporaryDirectory() as d:
        os.makedirs(os.path.join(d, "design"))
        open(os.path.join(d, "design", "DESIGN.md"), "w").write(
            "Anchor type: product\n\n**Proposals to confirm**\n- Signed paulownia box per piece — answers breakage — studio\n"
            "- Remake if broken within 7 days — trust — studio\n")
        page = f"<html lang='en'><body><main><section data-nsd-anchor='colour field'><p>Every piece ships in a signed box.</p>{long_copy}</section></main></body></html>"
        p = os.path.join(d, "index.html"); open(p, "w", encoding="utf-8").write(page)
        check("unmarked proposals are flagged", "proposal-unmarked" in rules_of(p), sorted(rules_of(p)))
        marked = page.replace("<p>Every piece", "<p data-nsd-proposed>Proposed: every piece").replace("</section>",
                              "<p data-nsd-proposed>Proposed: a remake if it arrives broken.</p></section>", 1)
        open(p, "w", encoding="utf-8").write(marked)
        check("marked proposals pass", "proposal-unmarked" not in rules_of(p), sorted(rules_of(p)))

    print("design_log — plans by folder, parallel runs, habits that swing back")
    with tempfile.TemporaryDirectory() as d:
        env = dict(os.environ, NSD_HISTORY=os.path.join(d, "h.json"))
        log = lambda *a: subprocess.run([PY, "scripts/design_log.py", *a], cwd=ROOT, capture_output=True, text=True, env=env).stdout
        rec_a = os.path.join(d, "shop", "design", "convergence-warnings.json")
        log("plan", "--project", "shop-v1", "--composition", "type-poster", "--result-form", "card", "--record", rec_a)
        again = log("plan", "--project", "shop-renamed", "--composition", "graphic-hero", "--result-form", "card", "--record", rec_a)
        stored = json.load(open(os.path.join(d, "h.json")))["entries"]
        check("a renamed re-plan from the same folder replaces the plan", len(stored) == 1 and "result form:" not in again, again[-300:])
        rec_b = os.path.join(d, "cafe", "design", "convergence-warnings.json")
        par = log("plan", "--project", "cafe", "--composition", "graphic-hero", "--result-form", "map", "--surface", "dark", "--record", rec_b)
        check("a parallel plan with the same composition is warned", "in progress:" in par, par[-300:])
    with tempfile.TemporaryDirectory() as d:
        env = dict(os.environ, NSD_HISTORY=os.path.join(d, "h.json"))
        log = lambda *a: subprocess.run([PY, "scripts/design_log.py", *a], cwd=ROOT, capture_output=True, text=True, env=env).stdout
        for proj, r in [("a", "15"), ("b", "5"), ("c", "9"), ("d", "6"), ("e", "12")]:
            log("add", "--project", proj, "--display-ratio", r, "--dir", os.path.join(d, proj))
        check("poster type that swings back is warned over six runs", "type scale:" in log("check"), "not warned")

    print("slop_lint — a result directly under its control is on screen")
    with tempfile.TemporaryDirectory() as d:
        page = (f"<html lang='en'><body><main><section data-nsd-interaction='estimator' data-nsd-anchor='colour field'>"
                f"<select id='ship'><option>DE</option></select><output aria-live='polite'>24–27 Sep</output></section>"
                f"<section>{long_copy}</section></main></body></html>")
        p = os.path.join(d, "index.html"); open(p, "w", encoding="utf-8").write(page)
        check("result right after the select passes", "interaction-result-offscreen" not in rules_of(p), sorted(rules_of(p)))

    print("crit board and placeholder overload — the A+ bar")
    with tempfile.TemporaryDirectory() as d:
        env = dict(os.environ, NSD_HISTORY=os.path.join(d, "h.json"))
        best = os.path.join(d, "best"); os.makedirs(best)
        open(os.path.join(best, "index.html"), "w").write("<html><body>best</body></html>")
        subprocess.run([PY, "scripts/design_log.py", "add", "--project", "best", "--industry", "restaurant", "--crit", "28",
                        "--page", os.path.join(best, "index.html")], cwd=ROOT, capture_output=True, text=True, env=env)
        bad = subprocess.run([PY, "scripts/design_log.py", "add", "--project", "x", "--crit", "40"], cwd=ROOT, capture_output=True, text=True, env=env)
        check("a crit outside 6–30 is refused", bad.returncode == 2, bad.stdout[-120:])
        new = os.path.join(d, "new"); os.makedirs(new)
        open(os.path.join(new, "index.html"), "w").write("<html><body>new</body></html>")
        b = subprocess.run([PY, "scripts/crit_board.py", os.path.join(new, "index.html"), "--industry", "restaurant",
                            "--html-only", "--out", os.path.join(d, "board")], cwd=ROOT, capture_output=True, text=True, env=env)
        board = open(os.path.join(d, "board", "crit-board.html")).read() if os.path.exists(os.path.join(d, "board", "crit-board.html")) else ""
        check("the crit board pins the best earlier page beside this one", "best/index.html" in board and "crit 28" in board, b.stdout[-200:])
    with tempfile.TemporaryDirectory() as d:
        filler = "".join(f"<p>[Description of dish {i}: ingredients]</p>" for i in range(8))
        page = f"<html lang='en'><body><main><section data-nsd-anchor='colour field'>{filler}{long_copy}</section><footer>[address] [phone]</footer></main></body></html>"
        p = os.path.join(d, "index.html"); open(p, "w", encoding="utf-8").write(page)
        check("eight bracketed placeholders in the main path are flagged", "placeholder-overload" in rules_of(p), sorted(rules_of(p)))
        open(p, "w", encoding="utf-8").write(page.replace(filler, "<p>[Menu prices]</p>"))
        check("brackets kept to the contact block and one fact pass", "placeholder-overload" not in rules_of(p), sorted(rules_of(p)))

    print("slop_lint — a result above the inputs is on screen without a sticky bar")
    with tempfile.TemporaryDirectory() as d:
        above = (f"<html lang='az'><body><main><section data-nsd-interaction='availability' data-nsd-anchor='colour field'>"
                 f"<output aria-live='polite'>Bu gün 16:40</output><select id='x'></select></section>"
                 f"<section>{long_copy}</section></main></body></html>")
        p = os.path.join(d, "index.html"); open(p, "w", encoding="utf-8").write(above)
        check("result before the inputs passes interaction-result-offscreen", "interaction-result-offscreen" not in rules_of(p), sorted(rules_of(p)))
        below = above.replace("<output aria-live='polite'>Bu gün 16:40</output><select id='x'></select>",
                              "<select id='x'></select><select></select><input type='date'><input type='number'><output aria-live='polite'>Bu gün 16:40</output>")
        open(p, "w", encoding="utf-8").write(below)
        check("result after the inputs with nothing sticky still fires", "interaction-result-offscreen" in rules_of(p), sorted(rules_of(p)))

    print("design_log — the register is never an axis to break")
    with tempfile.TemporaryDirectory() as d:
        env = dict(os.environ, NSD_HISTORY=os.path.join(d, "h.json"))
        for proj, surf, hue, face, struct in [("a", "dark", 30, "Fraunces", "photo hero grid"),
                                              ("b", "light", 150, "Archivo", "timeline sequence"),
                                              ("c", "dark", 250, "Bitter", "estimator poster")]:
            subprocess.run([PY, "scripts/design_log.py", "add", "--project", proj, "--register", "R2", "--surface", surf,
                            "--hue", str(hue), "--display", face, "--structure", struct], cwd=ROOT, capture_output=True, text=True, env=env)
        out = subprocess.run([PY, "scripts/design_log.py", "check"], cwd=ROOT, capture_output=True, text=True, env=env).stdout
        check("three R2 runs raise no convergence warning", "CONVERGENCE" not in out, out.strip()[-240:])
        check("the register streak is reported as keep-the-brief", "keep the register the brief" in out, out.strip()[-240:])

    print("shoot — parses its arguments without a browser")
    sys.path.insert(0, os.path.join(ROOT, "scripts"))
    import shoot
    check("--set splits selector and value", shoot.parse_set("#pages=12") == ("#pages", "12"), str(shoot.parse_set("#pages=12")))
    check("--set keeps '=' inside an attribute selector", shoot.parse_set("[name=pages]=3") == ("[name=pages]", "3"),
          str(shoot.parse_set("[name=pages]=3")))
    calm = {"display": 70, "ratio": 5.0, "graphic": 0.0, "field": 0.0}
    check("a calm R2 first viewport has no bold move", not shoot.bold_move(calm, "R2")[0], shoot.bold_move(calm, "R2")[1])
    check("R1 needs no bold move", shoot.bold_move(calm, "R1")[0], "R1 failed")
    check("a saturated field with 4.7× type passes R2", shoot.bold_move({"ratio": 4.7, "graphic": 0, "field": 0.9}, "R2")[0], "field failed")
    check("poster type passes R3", shoot.bold_move({"display": 195, "ratio": 13.9, "graphic": 0.06, "field": 1.0}, "R3")[0], "type failed")
    check("a 35% graphic passes R2 but not R3", shoot.bold_move({"ratio": 3, "graphic": 0.35, "field": 0}, "R2")[0]
          and not shoot.bold_move({"ratio": 3, "graphic": 0.35, "field": 0}, "R3")[0], "graphic thresholds")
    check("a phone first screen with 2.4× type and its graphic below the fold fails R2",
          not shoot.bold_move({"ratio": 2.4, "graphic": 0, "field": 0}, "R2", phone=True)[0], "phone passed")
    check("a phone first screen owned by a colour field passes R2",
          shoot.bold_move({"ratio": 2.9, "graphic": 0, "field": 0.92}, "R2", phone=True)[0], "phone field failed")
    check("4.6× type on a phone passes R3", shoot.bold_move({"ratio": 4.6, "graphic": 0.02, "field": 0}, "R3", phone=True)[0], "phone type failed")
    check("a time set huge on a colour field is a result-poster",
          shoot.composition({"displayInResult": True, "ratio": 8.5, "graphic": 0, "field": 1.0}) == "result-poster", "result")
    check("a 43% drawing is a graphic-hero", shoot.composition({"ratio": 5.9, "graphic": 0.43, "field": 0}) == "graphic-hero", "graphic")
    check("a heading beside controls is heading-and-panel", shoot.composition({"ratio": 5, "graphic": 0, "field": 0}) == "heading-and-panel", "panel")
    with tempfile.TemporaryDirectory() as d:
        os.makedirs(os.path.join(d, "design"))
        open(os.path.join(d, "design", "DESIGN.md"), "w").write("| **Expression register** | R2 Composed — because facts |\n")
        check("register is read from DESIGN.md", shoot.register_from(d) == "R2", str(shoot.register_from(d)))
    h = run("scripts/shoot.py", "--help")
    check("shoot.py --help", h.returncode == 0 and "--set" in h.stdout, h.stderr[-200:])
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "index.html"); open(p, "w").write("<html><body>x</body></html>")
        inside = run("scripts/shoot.py", p, "--out", os.path.join(d, "shots"), "--chrome", PY)
        check("shoot.py refuses to write screenshots into the deliverable", inside.returncode == 2 and "inside the deliverable" in inside.stdout,
              inside.stdout.strip()[-200:])

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

    print("slop_lint — the marquee the catalog bans")
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "m.html")
        open(p, "w").write("<html><body><main><div class='marquee'><ul class='marquee__track'><li>date</li></ul></div>"
                           "<style>.marquee__track{animation:scroll 30s linear infinite}</style></main></body></html>")
        check("marquee flagged", "marquee" in {f["rule"] for f in lint_json(p)["findings"]}, "not flagged")

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
