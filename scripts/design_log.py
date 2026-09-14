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
from collections import Counter
from datetime import date

STORE = os.environ.get("NSD_HISTORY") or os.path.expanduser("~/.no-slop-design/history.json")
WINDOW = 5          # how many recent entries count as "lately"
STREAK = 3          # this many in a row on one axis is a streak worth breaking
PLAN_HOURS = 6      # a planned direction counts in `check` for this long, so parallel runs can see each other
RESULT_FORMS = ("figure", "paper", "diagram", "card", "list", "table", "calendar", "map", "media")
# image look, recorded as angle;light;surface;palette from these words only (or "none" for a page without imagery)
LOOK = {
    "angle": ("top-down", "eye-level", "low-angle", "close-up", "wide"),
    "light": ("side-window", "overcast", "hard-sun", "dusk-night", "studio", "artificial"),
    "surface": ("wood", "stone", "metal", "fabric", "paper", "tile", "glass", "plant", "street", "seamless"),
    "palette": ("warm", "cool", "neutral", "saturated", "mono"),
}


def parse_look(value: str) -> str:
    """Validate an --image-look value against LOOK; raises ValueError with the allowed words."""
    v = value.strip().lower()
    if v == "none":
        return v
    parts = [p.strip() for p in v.split(";")]
    if len(parts) != 4:
        raise ValueError("--image-look takes angle;light;surface;palette, e.g. top-down;overcast;stone;neutral")
    for (facet, words), p in zip(LOOK.items(), parts):
        if p not in words:
            raise ValueError(f"--image-look {facet} '{p}' is not one of: {', '.join(words)} (pick the nearest; "
                             "free words hide repeats — limestone and kiln shelf are both stone)")
    return ";".join(parts)


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


def record(path: str | None, project: str | None, warns: list[str]) -> None:
    """Write the warnings a run saw into its project, so they cannot be read and quietly ignored (a 1.16 run kept a
    repeated composition 'deliberately' with no reason on record)."""
    if not path:
        return
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump({"project": project, "date": date.today().isoformat(), "warnings": warns}, fh, indent=2, ensure_ascii=False)
    print(f"warnings recorded in {path}: {len(warns)} — act on each, or answer it under 'Convergence overrides' in DESIGN.md")


def live(entries: list[dict]) -> list[dict]:
    """Finished entries plus planned ones younger than PLAN_HOURS; a finished entry replaces its own plan."""
    import time
    done = {e.get("project") for e in entries if e.get("status") != "planned"}
    now = time.time()
    return [e for e in entries if e.get("status") != "planned"
            or (e.get("project") not in done and now - e.get("planned_at", 0) < PLAN_HOURS * 3600)]


def analyse(entries: list[dict]) -> list[str]:
    recent = live(entries)[-WINDOW:]
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
    # the first-viewport composition measured by shoot.py — a named structure, not free text, so a repeat is exact
    comps = [(e.get("composition"), e.get("industry")) for e in recent if e.get("composition")]
    if len(comps) >= 2 and comps[-1][0] == comps[-2][0]:
        inds = sorted({i for _, i in comps[-2:] if i})
        warns.append(f"composition: the last two first viewports were both '{comps[-1][0]}'"
                     + (f" ({' and '.join(inds)})" if len(inds) > 1 else "")
                     + " — a different industry with the same first viewport is a house style forming; choose another composition")
    elif len(comps) >= 3:
        top, n = Counter(c for c, _ in comps).most_common(1)[0]
        if n >= 3:
            warns.append(f"composition: '{top}' in {n} of the last {len(comps)} runs — choose another first-viewport composition")
    # the page skeleton measured by shoot.py: the device of each section, in order
    def collapse(s):
        out = []
        for part in (s or "").split(">"):
            if part and (not out or out[-1] != part):
                out.append(part)
        return out

    def lcs(a, b):
        t = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
        for i, x in enumerate(a):
            for j, y in enumerate(b):
                t[i + 1][j + 1] = t[i][j] + 1 if x == y else max(t[i][j + 1], t[i + 1][j])
        return t[-1][-1]

    skels = [(collapse(e.get("skeleton")), e.get("industry")) for e in recent if e.get("skeleton")]
    if len(skels) >= 2:
        (a, ia), (b, ib) = skels[-2], skels[-1]
        if len(a) >= 3 and len(b) >= 3 and lcs(a, b) / max(len(a), len(b)) >= 0.75:
            warns.append(f"skeleton: the last two pages ran the same sections in the same order ({' > '.join(b)})"
                         + (f" for {ia} and {ib}" if ia and ib and ia != ib else "")
                         + " — the skill's house skeleton; derive the sections from this content, not from the last page")
    media = [e.get("media") for e in recent if e.get("media") is not None]
    if len(media) >= 3 and all(int(m) == 0 for m in media[-3:]):
        warns.append("imagery: the last 3 pages carried no image at all — 'no assets' is not a direction; consider "
                     "licensed photography, commissioned or generated illustration, and write why it was rejected")
    structures = [(e.get("structure") or "").lower() for e in recent if e.get("structure")]
    if len(structures) >= 2:
        words = [set(s.split()) for s in structures[-2:]]
        shared = words[0] & words[1] - {"a", "the", "with", "and", "of", "+", "one"}
        if len(shared) >= 2:
            warns.append(f"structure: the last two share “{', '.join(sorted(shared))}” — change the composition idea, not just the palette")
    # the interaction's answer given the same physical form: calendar leaf, receipt, solicitor's letter in a row
    forms = [e.get("result_form") for e in recent if e.get("result_form")]
    if len(forms) >= 2 and forms[-1] == forms[-2]:
        warns.append(f"result form: the last two interactions answered as a '{forms[-1]}' — give this answer another form "
                     f"({', '.join(f for f in RESULT_FORMS if f != forms[-1])})")
    elif len(forms) >= 3 and Counter(forms).most_common(1)[0][1] >= 3:
        top = Counter(forms).most_common(1)[0][0]
        warns.append(f"result form: '{top}' in {Counter(forms)[top]} of the last {len(forms)} runs — the paper-artefact "
                     "result is becoming a house style" if top == "paper" else
                     f"result form: '{top}' in {Counter(forms)[top]} of the last {len(forms)} runs — vary it")
    # the cheapest bold move repeated: poster-scale type on every first viewport (1.14 tests: 166, 400, 176, 158, 384 px)
    ratios = [float(e["display_ratio"]) for e in recent if e.get("display_ratio") is not None]
    if len(ratios) >= 3 and all(r >= 8 for r in ratios[-3:]):
        warns.append(f"type scale: the last 3 first viewports set display type at {', '.join(f'{r:g}×' for r in ratios[-3:])} "
                     "body size — oversized type is becoming the default bold move; make this one a photograph, a drawing, "
                     "a colour field or the product itself, and keep the type in proportion")
    # generated or stock imagery sharing one look: wooden table, soft window light, warm browns — or two top-down shots
    # on pale stone. Facets come from a fixed vocabulary so "limestone" and "kiln-shelf-alumina" both read as stone.
    looks = [e["image_look"].split(";") for e in recent
             if e.get("image_look") and e["image_look"] != "none" and len(e["image_look"].split(";")) == 4]
    if len(looks) >= 2:
        a, b = looks[-2], looks[-1]
        same = [f"{facet} {a[i]}" for i, facet in enumerate(LOOK) if a[i] == b[i]]
        if len(same) >= 3 or (a[0] == b[0] and a[2] == b[2]):
            warns.append(f"image look: the last two pages' imagery shared {', '.join(same)} — change the camera angle or "
                         "the surface at least; derive both from this direction, not from the image tool's default")
    # the opening and closing formula: hero then interaction, contact form last
    if len(skels) >= 2 and skels[-1][0][:2] == skels[-2][0][:2] and len(skels[-1][0]) >= 2:
        warns.append(f"opening: the last two pages opened the same way ({' > '.join(skels[-1][0][:2])}) — the interaction "
                     "may sit later (after rooms, menu, doctors) or be the page's spine; open on what this business shows first")
    if len(skels) >= 3 and all(s and s[-1] == "form" for s, _ in skels[-3:]):
        warns.append("closing: the last three pages ended on a contact form — end on the next real step for this business "
                     "(a map and hours, a booking, a phone number, a WhatsApp link, an order)")
    industries = [e.get("industry") for e in recent if e.get("industry")]
    if len(set(industries)) >= 3 and len({e.get("surface") for e in recent if e.get("surface")}) == 1:
        warns.append("three different industries came out with the same surface polarity — that is the skill's own tell, not a house style")
    return warns


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("add", help="record a finished direction")
    pl = sub.add_parser("plan", help="register a chosen direction before building, so runs in parallel see it")
    for p in (a, pl):
        for f in ("project", "register", "surface", "display", "text", "structure", "industry", "market", "anchor", "interaction"):
            p.add_argument(f"--{f}", default=None)
        p.add_argument("--result-form", dest="result_form", default=None, choices=RESULT_FORMS,
                       help="the physical form of the interaction's answer: " + ", ".join(RESULT_FORMS))
        p.add_argument("--display-ratio", dest="display_ratio", type=float, default=None,
                       help="first-viewport display type ÷ body size, from shoot.py's 'first' line (planned: the intended ratio)")
        p.add_argument("--image-look", dest="image_look", default=None,
                       help="angle;light;surface;palette from a fixed vocabulary, e.g. top-down;overcast;stone;neutral, "
                            "or none. Angles: " + ", ".join(LOOK["angle"]) + ". Light: " + ", ".join(LOOK["light"])
                            + ". Surface: " + ", ".join(LOOK["surface"]) + ". Palette: " + ", ".join(LOOK["palette"]))
    pl.add_argument("--composition", default=None)
    pl.add_argument("--skeleton", default=None)
    pl.add_argument("--hue", type=float, default=None)
    a.add_argument("--skeleton", default=None, help="section devices in order, as printed by shoot.py (e.g. interaction>steps>table>form)")
    a.add_argument("--media", type=int, default=None, help="number of images/video on the page, as printed by shoot.py")
    a.add_argument("--composition", default=None,
                   help="first-viewport composition as printed by shoot.py: graphic-hero, result-poster, type-poster, "
                        "field-and-heading, heading-and-panel")
    a.add_argument("--hue", type=float, default=None)
    a.add_argument("--screenshot", nargs="+", default=None,
                   help="full-page PNG(s); surface polarity is measured from the pixels and overrides --surface")

    c = sub.add_parser("check", help="warn about convergence before choosing a direction")
    c.add_argument("--json", action="store_true")
    for p in (c, pl):
        p.add_argument("--record", default=None, metavar="PATH",
                       help="write the warnings to PATH (design/convergence-warnings.json); slop_lint then requires each one "
                            "to be acted on or answered under 'Convergence overrides' in DESIGN.md")

    ms = sub.add_parser("measure", help="measure the surface polarity of full-page screenshot(s)")
    ms.add_argument("png", nargs="+")

    l = sub.add_parser("list", help="show recent entries")
    l.add_argument("--limit", type=int, default=10)

    args = ap.parse_args()
    entries = load()
    if getattr(args, "image_look", None):
        try:
            args.image_look = parse_look(args.image_look)
        except ValueError as err:
            print(err)
            return 2

    if args.cmd == "measure":
        share = dark_share(args.png)
        print(f"dark share {share:.2f} → surface polarity: {polarity(share)}")
        return 0

    keys = ("project", "register", "surface", "display", "text", "structure", "industry", "market", "anchor",
            "interaction", "composition", "skeleton", "result_form", "display_ratio", "image_look")
    if args.cmd == "plan":
        import time
        missing = [f"--{n.replace('_', '-')}" for n in ("project", "composition", "result_form") if not getattr(args, n, None)]
        if missing:
            print(f"plan needs {', '.join(missing)}: a plan without the composition and result form cannot warn the run "
                  "beside it (1.14: two parallel runs both opened on poster type). Compositions: graphic-hero, "
                  "result-poster, type-poster, field-and-heading, heading-and-panel")
            return 2
        entry = {k: getattr(args, k) for k in keys if getattr(args, k, None)}
        if args.hue is not None:
            entry["hue"], entry["hue_family"] = args.hue, hue_family(args.hue)
        entry.update(status="planned", planned_at=time.time(), date=date.today().isoformat())
        # a re-plan replaces this project's earlier plan: a 1.17 run that changed direction twice was warned against
        # its own previous plans in four of six warnings
        entries = [e for e in entries if not (e.get("status") == "planned" and e.get("project") == entry.get("project"))]
        warns = analyse(entries + [entry])
        entries.append(entry)
        save(entries)
        record(args.record, entry.get("project"), warns)
        print(f"planned: {json.dumps(entry, ensure_ascii=False)}")
        for w in warns:
            print("CONVERGENCE:", w)
        return 0

    if args.cmd == "add":
        entry = {k: getattr(args, k) for k in keys if getattr(args, k, None)}
        entries = [e for e in entries if not (e.get("status") == "planned" and e.get("project") == entry.get("project"))]
        if args.media is not None:
            entry["media"] = args.media
        if not args.composition:
            print("note: no --composition recorded; shoot.py prints it ('compose' line) — without it a repeated first "
                  "viewport across industries goes unnoticed")
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
    record(args.record, None, warns)
    registers = [e.get("register") for e in entries[-WINDOW:] if e.get("register")]
    note = None
    if len(registers) >= STREAK and len(set(registers[-STREAK:])) == 1:
        note = (f"the last {STREAK} runs were all {registers[-1]}. That is not a warning: keep the register the brief "
                "calls for, and make the difference on the axes above")
    if args.json:
        print(json.dumps({"entries": len(entries), "recent": entries[-WINDOW:], "warnings": warns, "register_note": note},
                         indent=2, ensure_ascii=False))
        return 0
    view = live(entries)[-WINDOW:]
    print(f"design history: {len(entries)} entries, looking at the last {len(view)} (planned runs in progress included)")
    for e in view:
        print(f"  {'[planned] ' if e.get('status') == 'planned' else ''}{e.get('date','?')}  {e.get('project','?')}: "
              f"{e.get('register','?')} · {e.get('surface','?')} · {e.get('result_form', 'result ?')} · "
              f"{e.get('hue_family','?')} · {e.get('display','?')} · {e.get('composition', 'composition ?')} · "
              f"{e.get('structure','')[:40]}")
    if warns:
        print()
        for w in warns:
            print("CONVERGENCE:", w)
        print("\nBreak at least two axes: surface polarity, hue family, typeface class, first-viewport composition. "
              "Never the register — it comes from the brief.")
    else:
        print("\nno convergence warnings")
    if note:
        print("register:", note)
    return 0


if __name__ == "__main__":
    sys.exit(main())
