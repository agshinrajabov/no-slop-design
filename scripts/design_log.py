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
  python3 scripts/design_log.py add ... --screenshot full-page.png   # surface polarity measured from pixels
  python3 scripts/design_log.py measure full-page.png                 # just print the dark share
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
import struct
import sys
import zlib
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



# --------------------------------------------------------------------------- surface polarity from a screenshot
# A declared surface is often wrong: a light hero over a mostly dark page gets recorded as "light". The pixels are
# what the visitor sees, so measure them. Stdlib PNG reader for 8-bit RGB/RGBA non-interlaced files, which is what
# headless Chrome and Playwright write. Use a 1x full-page screenshot; 2x works but is four times slower.
DARK_L = 0.18          # relative luminance below which a pixel reads as dark (sRGB ~#767676 sits at 0.18)


def read_png(path: str):
    data = open(path, "rb").read()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"{path}: not a PNG")
    pos, idat, w = 8, [], None
    while pos < len(data):
        ln, typ = struct.unpack(">I4s", data[pos:pos + 8])
        chunk = data[pos + 8:pos + 8 + ln]
        pos += 12 + ln
        if typ == b"IHDR":
            w, h, depth, ctype, _, _, interlace = struct.unpack(">IIBBBBB", chunk)
            if depth != 8 or interlace or ctype not in (2, 6):
                raise ValueError(f"{path}: unsupported PNG (depth {depth}, colour type {ctype}, interlace {interlace})")
            bpp = 3 if ctype == 2 else 4
        elif typ == b"IDAT":
            idat.append(chunk)
        elif typ == b"IEND":
            break
    raw = zlib.decompress(b"".join(idat))
    stride, prev, rows, i = w * bpp, bytearray(w * bpp), [], 0
    for _ in range(h):
        f, line = raw[i], bytearray(raw[i + 1:i + 1 + stride])
        i += 1 + stride
        if f == 1:
            for x in range(bpp, stride):
                line[x] = (line[x] + line[x - bpp]) & 255
        elif f == 2:
            for x in range(stride):
                line[x] = (line[x] + prev[x]) & 255
        elif f == 3:
            for x in range(stride):
                line[x] = (line[x] + ((line[x - bpp] if x >= bpp else 0) + prev[x]) // 2) & 255
        elif f == 4:
            for x in range(stride):
                a = line[x - bpp] if x >= bpp else 0
                b, c = prev[x], (prev[x - bpp] if x >= bpp else 0)
                p = a + b - c
                pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                line[x] = (line[x] + (a if pa <= pb and pa <= pc else b if pb <= pc else c)) & 255
        rows.append(line)
        prev = line
    return w, h, bpp, rows


def dark_share(paths: list[str], step: int = 4) -> float:
    lin = [((v / 255) / 12.92 if v / 255 <= 0.04045 else ((v / 255 + 0.055) / 1.055) ** 2.4) for v in range(256)]
    dark = total = 0
    for path in paths:
        w, h, bpp, rows = read_png(path)
        for y in range(0, h, step):
            row = rows[y]
            for x in range(0, w, step):
                o = x * bpp
                total += 1
                dark += (0.2126 * lin[row[o]] + 0.7152 * lin[row[o + 1]] + 0.0722 * lin[row[o + 2]]) < DARK_L
    return dark / total if total else 0.0


def polarity(share: float) -> str:
    return "dark" if share >= 0.6 else "light" if share <= 0.35 else "mixed"


def analyse(entries: list[dict]) -> list[str]:
    recent = entries[-WINDOW:]
    warns: list[str] = []
    if len(recent) < 2:
        return warns

    def streak(key, label, n=STREAK, fmt=lambda v: v):
        vals = [e.get(key) for e in recent if e.get(key)]
        if len(vals) < n:
            return
        tail = vals[-n:]
        if len(set(tail)) == 1:
            warns.append(f"{label}: the last {n} directions were all {fmt(tail[0])} — vary this one or write down why not")

    # surface polarity is the first thing anyone sees, so two in a row already count
    streak("surface", "surface polarity", n=2)
    streak("display", "display typeface")
    # the register is not an axis to break: it comes from the brief (decision type, category norm, asset budget).
    # A 1.8 run moved a translation agency to R3 because the last three runs were R2 — history deciding ambition.
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
    for f in ("project", "register", "surface", "display", "text", "structure", "industry", "market", "anchor", "interaction"):
        a.add_argument(f"--{f}", default=None)
    a.add_argument("--hue", type=float, default=None)
    a.add_argument("--screenshot", nargs="+", default=None,
                   help="full-page PNG(s); surface polarity is measured from the pixels and overrides --surface")

    c = sub.add_parser("check", help="warn about convergence before choosing a direction")
    c.add_argument("--json", action="store_true")

    ms = sub.add_parser("measure", help="measure the surface polarity of full-page screenshot(s)")
    ms.add_argument("png", nargs="+")

    l = sub.add_parser("list", help="show recent entries")
    l.add_argument("--limit", type=int, default=10)

    args = ap.parse_args()
    entries = load()

    if args.cmd == "measure":
        share = dark_share(args.png)
        print(f"dark share {share:.2f} → surface polarity: {polarity(share)}")
        return 0

    if args.cmd == "add":
        entry = {k: getattr(args, k) for k in ("project", "register", "surface", "display", "text", "structure",
                                               "industry", "market", "anchor", "interaction") if getattr(args, k)}
        if args.hue is not None:
            entry["hue"] = args.hue
            entry["hue_family"] = hue_family(args.hue)
        if args.screenshot:
            share = dark_share(args.screenshot)
            measured = polarity(share)
            if args.surface and args.surface != measured:
                print(f"note: surface was declared '{args.surface}' but the screenshot is {share:.0%} dark; recording '{measured}'")
            entry["surface"], entry["dark_share"], entry["surface_source"] = measured, round(share, 2), "measured"
        elif args.surface:
            entry["surface_source"] = "declared"
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
    registers = [e.get("register") for e in entries[-WINDOW:] if e.get("register")]
    note = None
    if len(registers) >= STREAK and len(set(registers[-STREAK:])) == 1:
        note = (f"the last {STREAK} runs were all {registers[-1]}. That is not a warning: keep the register the brief "
                "calls for, and make the difference on the axes above")
    if args.json:
        print(json.dumps({"entries": len(entries), "recent": entries[-WINDOW:], "warnings": warns, "register_note": note},
                         indent=2, ensure_ascii=False))
        return 0
    print(f"design history: {len(entries)} entries, looking at the last {min(len(entries), WINDOW)}")
    for e in entries[-WINDOW:]:
        print(f"  {e.get('date','?')}  {e.get('project','?')}: {e.get('register','?')} · {e.get('surface','?')} · "
              f"{e.get('hue_family','?')} · {e.get('display','?')} · {e.get('structure','')[:40]}")
    if warns:
        print()
        for w in warns:
            print("CONVERGENCE:", w)
        print("\nBreak at least two axes: surface polarity, hue family, typeface class, structural idea. "
              "Never the register — it comes from the brief.")
    else:
        print("\nno convergence warnings")
    if note:
        print("register:", note)
    return 0


if __name__ == "__main__":
    sys.exit(main())
