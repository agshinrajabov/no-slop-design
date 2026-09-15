#!/usr/bin/env python3
"""
crit_board.py — put the page beside the best pages this skill has made, before calling it done.

Rules catch repeats and mistakes; they cannot say whether a page is any good. Six rounds of fixes proved it: every
check passed while one restaurant page went from a lit floor plan to a booking form with bracketed menu text. A
studio settles that question by pinning the new work next to the best recent work and asking which is stronger.

This renders one board with headless Chrome:
  - this page's first viewport at 1280×800 and its phone first screen at 375×812
  - up to three earlier pages with the highest recorded crit score (`design_log.py add --crit`)
  - the most recent earlier page for the same industry, if there is one
and prints what is on it. Look at the PNG, score the page with review-checklist.md Gate 14, and revise before hand-off
if it is weaker than the best page on the board on idea or memorability.

Usage:
  python3 scripts/crit_board.py index.html --industry restaurant
  python3 scripts/crit_board.py index.html --html-only      # write the board HTML without rendering (CI, no Chrome)
"""
from __future__ import annotations

import argparse
import html
import json
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import design_log  # noqa: E402
import shoot  # noqa: E402


def frame(src: str, label: str, w: int, h: int, scale: float) -> str:
    return (f"<figure><figcaption>{html.escape(label)}</figcaption>"
            f"<div class='f' style='width:{int(w * scale)}px;height:{int(h * scale)}px'>"
            f"<iframe src='{html.escape(src)}' style='width:{w}px;height:{h}px;transform:scale({scale})'></iframe></div></figure>")


def pick(entries: list[dict], here: str, industry: str | None) -> list[tuple[str, dict]]:
    """Up to three best-scored earlier pages plus the latest same-industry page, each with an index.html on disk."""
    def page_of(e):
        p = e.get("page") or (os.path.join(e["dir"], "index.html") if e.get("dir") else None)
        return p if p and os.path.exists(p) and os.path.abspath(os.path.dirname(p)) != here else None

    done = [e for e in entries if e.get("status") != "planned" and page_of(e)]
    best = sorted((e for e in done if e.get("crit")), key=lambda e: -float(e["crit"]))[:3]
    chosen = [("best · crit " + str(e["crit"]), e) for e in best]
    if industry:
        same = [e for e in done if industry.lower() in (e.get("industry") or "").lower() or industry.lower() in (e.get("project") or "")]
        # the best page this industry has had, not only the latest: a 1.20 restaurant run was shown its weakest
        # predecessor and never saw the floor-plan page that scored higher on idea
        scored = sorted((e for e in same if e.get("crit")), key=lambda e: -float(e["crit"]))
        if scored and all(scored[0] is not e for _, e in chosen):
            chosen.append((f"best {industry} · crit {scored[0]['crit']}", scored[0]))
        if same and all(same[-1] is not e for _, e in chosen):
            chosen.append(("latest " + industry + (f" · crit {same[-1]['crit']}" if same[-1].get("crit") else ""), same[-1]))
    return [(label, e) for label, e in chosen]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("page")
    ap.add_argument("--industry", help="to include the latest earlier page for the same industry")
    ap.add_argument("--out", help="output folder (default: <tmp>/nsd-shots/<project>)")
    ap.add_argument("--html-only", action="store_true")
    ap.add_argument("--chrome")
    args = ap.parse_args()

    page = os.path.abspath(args.page)
    if not os.path.exists(page):
        print(f"crit_board.py: {args.page} does not exist")
        return 2
    here = os.path.dirname(page)
    out = os.path.abspath(args.out or os.path.join(tempfile.gettempdir(), "nsd-shots", os.path.basename(here)))
    os.makedirs(out, exist_ok=True)

    others = pick(design_log.load(), here, args.industry)
    tiles = [frame("file://" + page, "this page · desktop", 1280, 800, 0.5),
             frame("file://" + page, "this page · phone", 375, 812, 0.5)]
    for label, e in others:
        p = e.get("page") or os.path.join(e["dir"], "index.html")
        tiles.append(frame("file://" + p, f"{e.get('project', '?')} · {label}", 1280, 800, 0.5))
    board = ("<!doctype html><meta charset='utf-8'><style>body{margin:0;padding:24px;background:#1b1a18;color:#eee;"
             "font:500 15px -apple-system,Helvetica,Arial;display:flex;flex-wrap:wrap;gap:24px;align-items:flex-start}"
             "figure{margin:0}figcaption{margin:0 0 8px}.f{overflow:hidden;border-radius:6px;background:#fff}"
             "iframe{border:0;transform-origin:0 0}</style>" + "".join(tiles))
    board_html = os.path.join(out, "crit-board.html")
    with open(board_html, "w", encoding="utf-8") as fh:
        fh.write(board)

    print(f"crit board: this page beside {len(others)} earlier page(s)")
    for label, e in others:
        print(f"  {e.get('project', '?')}: {label} · {e.get('composition', '?')} · {e.get('result_form', '?')}")
    if not others:
        print("  (no scored earlier pages yet — score this one against Gate 14 alone and record it with --crit)")
    if args.html_only:
        print(f"board html: {board_html}")
        return 0

    binary = shoot.find_chrome(args.chrome)
    if not binary:
        print(f"no Chrome found; open {board_html} in a browser and look at it")
        return 3
    rows = 1 + (len(others) + 1) // 2
    png = os.path.join(out, "crit-board.png")
    if os.path.exists(png):
        os.remove(png)
    shoot.chrome(binary, "file://" + board_html, [f"--window-size=1400,{rows * 470 + 60}", f"--screenshot={png}"])
    if not os.path.exists(png):
        print("the board did not render; open the HTML instead: " + board_html)
        return 2
    print(f"board: {png}")
    print("Look at it. Score this page on Gate 14 (review-checklist.md): idea, first-viewport memorability, imagery and "
          "craft, type and rhythm, content completeness, interaction. Below A+ (every axis ≥ 4, total ≥ 26, and not weaker "
          "than the best page on the board on idea or memorability) → revise the two weakest axes, re-render, re-score. "
          "Record the final score: design_log.py add … --crit <total>.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
