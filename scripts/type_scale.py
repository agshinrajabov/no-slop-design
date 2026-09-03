#!/usr/bin/env python3
"""
type_scale.py — modular + fluid type scale generator (Utopia-style clamp()).

Usage:
  python3 type_scale.py                                   # defaults: 16→18px base, 1.2→1.25 ratio, 320→1240 viewport
  python3 type_scale.py --min-base 16 --max-base 19 --min-ratio 1.2 --max-ratio 1.333
  python3 type_scale.py --steps -2 6 --format css        # css | dtcg | table
  python3 type_scale.py --format dtcg > tokens/typography.json

How it works: each step i has min size = minBase * minRatio^i and max size = maxBase * maxRatio^i.
The fluid value is a linear interpolation between the two viewports, emitted as
clamp(min, preferred, max) with the preferred part in rem + vw. Uses rem (16px root).

Also prints recommended line-heights and letter-spacing per step:
  - line-height tightens as size grows (1.6 body → 1.05 display)
  - letter-spacing goes slightly negative above ~24px for most sans/serif faces; never positive on lowercase
"""
from __future__ import annotations

import argparse
import json

STEP_NAMES = {
    -2: "2xs", -1: "xs", 0: "base", 1: "md", 2: "lg", 3: "xl", 4: "2xl", 5: "3xl", 6: "4xl", 7: "5xl", 8: "6xl",
}


def line_height_for(px: float) -> float:
    if px <= 14:
        return 1.6
    if px <= 18:
        return 1.55
    if px <= 24:
        return 1.4
    if px <= 32:
        return 1.25
    if px <= 48:
        return 1.15
    if px <= 72:
        return 1.05
    return 1.0


def tracking_for(px: float) -> str:
    if px < 14:
        return "0.01em"
    if px <= 20:
        return "0"
    if px <= 32:
        return "-0.01em"
    if px <= 56:
        return "-0.02em"
    return "-0.03em"


def clamp_expr(min_px: float, max_px: float, min_vw: float, max_vw: float) -> str:
    if abs(max_px - min_px) < 0.01:
        return f"{min_px / 16:.4g}rem"
    slope = (max_px - min_px) / (max_vw - min_vw)
    intercept = min_px - slope * min_vw
    preferred = f"{intercept / 16:.4g}rem + {slope * 100:.4g}vw"
    lo, hi = (min_px, max_px) if min_px < max_px else (max_px, min_px)
    return f"clamp({lo / 16:.4g}rem, {preferred}, {hi / 16:.4g}rem)"


def build(args):
    rows = []
    for i in range(args.steps[0], args.steps[1] + 1):
        mn = args.min_base * (args.min_ratio ** i)
        mx = args.max_base * (args.max_ratio ** i)
        rows.append(
            {
                "step": i,
                "name": STEP_NAMES.get(i, f"step{i}"),
                "min_px": round(mn, 2),
                "max_px": round(mx, 2),
                "clamp": clamp_expr(mn, mx, args.min_vw, args.max_vw),
                "line_height": line_height_for((mn + mx) / 2),
                "tracking": tracking_for((mn + mx) / 2),
            }
        )
    return rows


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--min-base", type=float, default=16)
    ap.add_argument("--max-base", type=float, default=18)
    ap.add_argument("--min-ratio", type=float, default=1.2, help="minor third 1.2 / major third 1.25 / perfect fourth 1.333 / aug fourth 1.414")
    ap.add_argument("--max-ratio", type=float, default=1.25)
    ap.add_argument("--min-vw", type=float, default=320)
    ap.add_argument("--max-vw", type=float, default=1240)
    ap.add_argument("--steps", type=int, nargs=2, default=[-2, 6], metavar=("FROM", "TO"))
    ap.add_argument("--format", choices=["table", "css", "dtcg"], default="table")
    ap.add_argument("--prefix", default="text", help="css variable prefix (default --text-*)")
    args = ap.parse_args()

    rows = build(args)

    if args.format == "table":
        print(f"{'step':>5} {'name':>5} {'min px':>8} {'max px':>8}  {'lh':>4} {'track':>7}  clamp()")
        for r in rows:
            print(f"{r['step']:>5} {r['name']:>5} {r['min_px']:>8} {r['max_px']:>8}  {r['line_height']:>4} {r['tracking']:>7}  {r['clamp']}")
    elif args.format == "css":
        print(":root {")
        for r in rows:
            print(f"  --{args.prefix}-{r['name']}: {r['clamp']};")
            print(f"  --{args.prefix}-{r['name']}--lh: {r['line_height']};")
            print(f"  --{args.prefix}-{r['name']}--tracking: {r['tracking']};")
        print("}")
    else:
        out = {"font-size": {}, "line-height": {}, "letter-spacing": {}}
        for r in rows:
            out["font-size"][r["name"]] = {
                "$type": "dimension",
                "$value": r["clamp"],
                "$description": f"{r['min_px']}px → {r['max_px']}px fluid",
            }
            out["line-height"][r["name"]] = {"$type": "number", "$value": r["line_height"]}
            out["letter-spacing"][r["name"]] = {"$type": "dimension", "$value": r["tracking"]}
        print(json.dumps({"typography": out}, indent=2))


if __name__ == "__main__":
    main()
