#!/usr/bin/env python3
"""
design_log.py — cross-project memory, so the skill stops repeating itself.

The per-project `design/design-log.json` is empty on every new project, which is exactly when convergence
happens: four fresh directories in a row produced four dark pages. This keeps a short fingerprint of each
finished direction in one place and answers a single question before the next direction is chosen:
**what have I been doing lately, and what am I about to repeat?**

Store: `~/.no-slop-design/history.json` (override with NSD_HISTORY).

Usage:
  python3 scripts/design_log.py check                      # read at Phase 0/3; prints convergence warnings
  python3 scripts/design_log.py add --project qala-house \\
      --register R3 --surface dark --hue 66 --display "Archivo Expanded" --text Archivo \\
      --structure "full-bleed photo + horizontal timetable" --industry festival --market DE
  python3 scripts/design_log.py list --limit 10
  python3 scripts/design_log.py check --json

An entry is a fingerprint, not a portfolio: register, surface polarity, brand hue, typefaces, the structural
idea in a few words, industry, market. `check` warns when the last few entries share an axis, and names the
axes that must differ this time.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import date

STORE = os.environ.get("NSD_HISTORY") or os.path.expanduser("~/.no-slop-design/history.json")
WINDOW = 5          # how many recent entries count as "lately"
STREAK = 3          # this many in a row on one axis is a streak worth breaking


def load() -> list[dict]:
    if not os.path.exists(STORE):
        return []
    try:
        with open(STORE, encoding="utf-8") as fh:
            data = json.load(fh)
        return data.get("entries", []) if isinstance(data, dict) else data
    except (json.JSONDecodeError, OSError):
        return []


def save(entries: list[dict]) -> None:
    os.makedirs(os.path.dirname(STORE), exist_ok=True)
    with open(STORE, "w", encoding="utf-8") as fh:
        json.dump({"$schema": "no-slop-design/history v1", "entries": entries[-100:]}, fh, indent=2, ensure_ascii=False)


def hue_family(h) -> str:
    try:
        h = float(h) % 360
    except (TypeError, ValueError):
        return "unknown"
    for lo, hi, name in [(0, 45, "red-orange"), (45, 95, "amber-yellow"), (95, 165, "green"),
                         (165, 215, "teal-cyan"), (215, 265, "blue"), (265, 315, "violet-magenta"), (315, 360, "pink-red")]:
        if lo <= h < hi:
            return name
    return "unknown"


def analyse(entries: list[dict]) -> list[str]:
    recent = entries[-WINDOW:]
    warns: list[str] = []
    if len(recent) < 2:
        return warns

    def streak(key, label, fmt=lambda v: v):
        vals = [e.get(key) for e in recent if e.get(key)]
        if len(vals) < STREAK:
            return
        tail = vals[-STREAK:]
        if len(set(tail)) == 1:
            warns.append(f"{label}: the last {STREAK} directions were all {fmt(tail[0])} — vary this one or write down why not")

    streak("surface", "surface polarity")
    streak("register", "expression register")
    streak("display", "display typeface")
    hues = [hue_family(e.get("hue")) for e in recent if e.get("hue") is not None]
    if len(hues) >= STREAK and len(set(hues[-STREAK:])) == 1 and hues[-1] != "unknown":
        warns.append(f"brand hue family: the last {STREAK} were all {hues[-1]} — a different family is the cheapest way to look different")
    structures = [(e.get("structure") or "").lower() for e in recent if e.get("structure")]
    if len(structures) >= 2:
        words = [set(s.split()) for s in structures[-2:]]
        shared = words[0] & words[1] - {"a", "the", "with", "and", "of", "+", "one"}
        if len(shared) >= 2:
            warns.append(f"structure: the last two share “{', '.join(sorted(shared))}” — change the composition idea, not just the palette")
    industries = [e.get("industry") for e in recent if e.get("industry")]
    if len(set(industries)) >= 3 and len({e.get("surface") for e in recent if e.get("surface")}) == 1:
        warns.append("three different industries came out with the same surface polarity — that is the skill's own tell, not a house style")
    return warns


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("add", help="record a finished direction")
    for f in ("project", "register", "surface", "display", "text", "structure", "industry", "market", "anchor"):
        a.add_argument(f"--{f}", default=None)
    a.add_argument("--hue", type=float, default=None)

    c = sub.add_parser("check", help="warn about convergence before choosing a direction")
    c.add_argument("--json", action="store_true")

    l = sub.add_parser("list", help="show recent entries")
    l.add_argument("--limit", type=int, default=10)

    args = ap.parse_args()
    entries = load()

    if args.cmd == "add":
        entry = {k: getattr(args, k) for k in ("project", "register", "surface", "display", "text", "structure",
                                               "industry", "market", "anchor") if getattr(args, k)}
        if args.hue is not None:
            entry["hue"] = args.hue
            entry["hue_family"] = hue_family(args.hue)
        entry["date"] = date.today().isoformat()
        entries.append(entry)
        save(entries)
        print(f"recorded: {json.dumps(entry, ensure_ascii=False)}")
        for w in analyse(entries):
            print("note:", w)
        return 0

    if args.cmd == "list":
        for e in entries[-args.limit:]:
            print(f"  {e.get('date','?')}  {e.get('project','?'):<20} {e.get('register','?'):<3} "
                  f"{e.get('surface','?'):<6} {e.get('hue_family','?'):<12} {e.get('display','?'):<22} {e.get('structure','')[:44]}")
        if not entries:
            print("  (no history yet)")
        return 0

    warns = analyse(entries)
    if args.json:
        print(json.dumps({"entries": len(entries), "recent": entries[-WINDOW:], "warnings": warns}, indent=2, ensure_ascii=False))
        return 0
    print(f"design history: {len(entries)} entries, looking at the last {min(len(entries), WINDOW)}")
    for e in entries[-WINDOW:]:
        print(f"  {e.get('date','?')}  {e.get('project','?')}: {e.get('register','?')} · {e.get('surface','?')} · "
              f"{e.get('hue_family','?')} · {e.get('display','?')} · {e.get('structure','')[:40]}")
    if warns:
        print()
        for w in warns:
            print("CONVERGENCE:", w)
        print("\nBreak at least two axes: register, surface polarity, hue family, typeface class, structural idea.")
    else:
        print("\nno convergence warnings")
    return 0


if __name__ == "__main__":
    sys.exit(main())
