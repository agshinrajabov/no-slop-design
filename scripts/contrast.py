#!/usr/bin/env python3
"""
contrast.py — WCAG 2.x contrast ratio + APCA (WCAG 3 draft) lightness contrast.

Usage:
  python3 contrast.py "#1a1a1a" "#fafaf7"              # text, background
  python3 contrast.py "#1a1a1a" "#fafaf7" --size 16 --weight 400
  python3 contrast.py --matrix tokens.css              # every color pair found in a CSS/JSON file
  python3 contrast.py --pairs pairs.txt                # one "fg bg [label]" per line
  python3 contrast.py --tokens build/tokens.flat.json  # auto-check text/surface roles per mode (from build_tokens.py)

Exit code 1 when any checked pair fails WCAG AA (text) — handy in CI.

APCA notes: Lc is polarity-aware (dark-on-light vs light-on-dark). Rough targets from the
APCA readability criterion (0.1.9 / 4g):
  Lc 90  body text at 14px/400 or preferred for long reading
  Lc 75  minimum for body text (16px/400)
  Lc 60  minimum for content text ~18px/400 or 14px/700
  Lc 45  large headlines (24px+/700), non-text UI that must be read
  Lc 30  placeholder / disabled text, non-essential UI
  Lc 15  minimum for any visible non-text element
These are guidance, not a certification. WCAG 2.x AA is still the legal baseline in most places.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from itertools import permutations

HEX_RE = re.compile(r"#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})\b")
OKLCH_RE = re.compile(r"oklch\(\s*([\d.]+%?)\s+([\d.]+)\s+([\d.]+)(?:deg)?\s*(?:/\s*[\d.]+%?)?\s*\)")


# --------------------------------------------------------------------------- parsing
def parse_hex(s: str) -> tuple[float, float, float]:
    s = s.strip().lstrip("#")
    if len(s) == 3:
        s = "".join(c * 2 for c in s)
    if len(s) == 8:
        s = s[:6]
    if len(s) != 6:
        raise ValueError(f"bad hex: {s}")
    return tuple(int(s[i : i + 2], 16) for i in (0, 2, 4))  # type: ignore


def oklch_to_srgb(L: float, C: float, h_deg: float) -> tuple[float, float, float]:
    """OKLCH -> sRGB 0..255 (gamut-clipped). Good enough for contrast checks."""
    import math

    h = math.radians(h_deg)
    a = C * math.cos(h)
    b = C * math.sin(h)
    l_ = L + 0.3963377774 * a + 0.2158037573 * b
    m_ = L - 0.1055613458 * a - 0.0638541728 * b
    s_ = L - 0.0894841775 * a - 1.2914855480 * b
    l, m, s = l_**3, m_**3, s_**3
    r = 4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s
    g = -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s
    bb = -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s

    def gam(c: float) -> float:
        c = max(0.0, min(1.0, c))
        return 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055

    return tuple(round(gam(c) * 255) for c in (r, g, bb))  # type: ignore


def parse_color(s: str) -> tuple[float, float, float]:
    s = s.strip()
    m = OKLCH_RE.fullmatch(s)
    if m:
        L = float(m.group(1).rstrip("%"))
        if m.group(1).endswith("%"):
            L /= 100
        return oklch_to_srgb(L, float(m.group(2)), float(m.group(3)))
    return parse_hex(s)


def to_hex(rgb) -> str:
    return "#%02x%02x%02x" % tuple(int(c) for c in rgb)


# --------------------------------------------------------------------------- WCAG 2.x
def wcag_luminance(rgb) -> float:
    def lin(c: float) -> float:
        c /= 255
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

    r, g, b = (lin(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def wcag_ratio(fg, bg) -> float:
    l1, l2 = wcag_luminance(fg), wcag_luminance(bg)
    hi, lo = max(l1, l2), min(l1, l2)
    return (hi + 0.05) / (lo + 0.05)


def wcag_grade(ratio: float, size_px: float = 16, weight: int = 400) -> str:
    large = size_px >= 24 or (size_px >= 18.66 and weight >= 700)
    if large:
        return "AAA" if ratio >= 4.5 else "AA" if ratio >= 3 else "FAIL"
    return "AAA" if ratio >= 7 else "AA" if ratio >= 4.5 else "FAIL"


# --------------------------------------------------------------------------- APCA 0.1.9 (4g)
def _apca_y(rgb) -> float:
    r, g, b = ((c / 255) ** 2.4 for c in rgb)
    return 0.2126729 * r + 0.7151522 * g + 0.0721750 * b


def apca_lc(txt, bg) -> float:
    blkThrs, blkClmp = 0.022, 1.414
    normBG, normTXT, revTXT, revBG = 0.56, 0.57, 0.62, 0.65
    scale, loOffset, loClip, deltaYmin = 1.14, 0.027, 0.1, 0.0005

    def soft_clamp(y: float) -> float:
        return y + (blkThrs - y) ** blkClmp if y < blkThrs else y

    ytxt, ybg = soft_clamp(_apca_y(txt)), soft_clamp(_apca_y(bg))
    if abs(ybg - ytxt) < deltaYmin:
        return 0.0
    if ybg > ytxt:  # dark text on light background
        sapc = (ybg**normBG - ytxt**normTXT) * scale
        lc = 0.0 if sapc < loClip else sapc - loOffset
    else:  # light text on dark background
        sapc = (ybg**revBG - ytxt**revTXT) * scale
        lc = 0.0 if sapc > -loClip else sapc + loOffset
    return lc * 100


def apca_verdict(lc: float, size_px: float = 16, weight: int = 400) -> str:
    a = abs(lc)
    if size_px >= 24 and weight >= 700:
        need = 45
    elif size_px >= 18 or weight >= 700:
        need = 60
    else:
        need = 75
    if a >= 90:
        tier = "excellent"
    elif a >= need:
        tier = "ok"
    elif a >= 45:
        tier = "large-text-only"
    elif a >= 30:
        tier = "non-essential-only"
    elif a >= 15:
        tier = "non-text-only"
    else:
        tier = "invisible"
    return f"{tier} (need ≥{need} for this size/weight)"


# --------------------------------------------------------------------------- reporting
def report(fg_s: str, bg_s: str, size: float, weight: int, label: str = "") -> bool:
    fg, bg = parse_color(fg_s), parse_color(bg_s)
    ratio = wcag_ratio(fg, bg)
    grade = wcag_grade(ratio, size, weight)
    lc = apca_lc(fg, bg)
    tag = f"[{label}] " if label else ""
    print(
        f"{tag}{to_hex(fg)} on {to_hex(bg)}  WCAG {ratio:.2f}:1 {grade:>4}   "
        f"APCA Lc {lc:+.1f} → {apca_verdict(lc, size, weight)}"
    )
    return grade != "FAIL"


def extract_colors(text: str) -> list[str]:
    found = HEX_RE.findall(text) + [m.group(0) for m in OKLCH_RE.finditer(text)]
    seen, out = set(), []
    for c in found:
        key = to_hex(parse_color(c))
        if key not in seen:
            seen.add(key)
            out.append(c)
    return out


def check_tokens(path: str, size: float, weight: int) -> bool:
    """Check semantic roles from build/tokens.flat.json: text.* on surface.*, on-action on action.*, status text on status surface."""
    data = json.load(open(path, encoding="utf-8"))
    ok = True
    for mode, table in data.items():
        colors = {k: v for k, v in table.items() if k.startswith("color.") and isinstance(v, str) and (v.startswith("#") or v.startswith("oklch"))}
        surfaces = {k: v for k, v in colors.items() if k.startswith("color.surface.") and "inverse" not in k}
        texts = {k: v for k, v in colors.items() if k.startswith("color.text.") and not k.startswith("color.text.on-") and "disabled" not in k}
        print(f"\n== mode: {mode}  ({len(texts)} text roles × {len(surfaces)} surfaces)")
        for t, tv in sorted(texts.items()):
            for s_, sv in sorted(surfaces.items()):
                ok &= report(tv, sv, size, weight, f"{t.removeprefix('color.')} on {s_.removeprefix('color.')}")
        on_action = colors.get("color.text.on-action")
        on_destructive = colors.get("color.text.on-destructive", on_action)
        for a, av in sorted(colors.items()):
            if not a.startswith("color.action.") or "secondary" in a:
                continue
            fg, name = (on_destructive, "text.on-destructive") if "destructive" in a else (on_action, "text.on-action")
            if fg:
                ok &= report(fg, av, size, weight, f"{name} on {a.removeprefix('color.')}")
        on_inverse = colors.get("color.text.on-inverse")
        if on_inverse and "color.surface.inverse" in colors:
            ok &= report(on_inverse, colors["color.surface.inverse"], size, weight, "text.on-inverse on surface.inverse")
        for st in ("success", "warning", "danger", "info"):
            tx, sf = colors.get(f"color.status.{st}.text"), colors.get(f"color.status.{st}.surface")
            if tx and sf:
                ok &= report(tx, sf, size, weight, f"status.{st}.text on status.{st}.surface")
        for b in ("color.border.strong", "color.border.focus"):
            if b in colors and "color.surface.base" in colors:
                fg, bg = parse_color(colors[b]), parse_color(colors["color.surface.base"])
                r = wcag_ratio(fg, bg)
                flag = "ok" if r >= 3 else "FAIL (UI ≥ 3:1)"
                print(f"[{b.removeprefix('color.')} vs surface.base] WCAG {r:.2f}:1 {flag}")
                ok &= r >= 3
    return ok


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("fg", nargs="?", help="text/foreground color (#hex or oklch())")
    ap.add_argument("bg", nargs="?", help="background color")
    ap.add_argument("--size", type=float, default=16, help="font size in px (default 16)")
    ap.add_argument("--weight", type=int, default=400, help="font weight (default 400)")
    ap.add_argument("--matrix", help="file to scan for colors; prints every pair passing AA")
    ap.add_argument("--pairs", help="file with 'fg bg [label]' per line")
    ap.add_argument("--tokens", help="build/tokens.flat.json from build_tokens.py — checks semantic roles per mode")
    ap.add_argument("--min-ratio", type=float, default=4.5, help="matrix filter threshold")
    args = ap.parse_args()

    ok = True
    if args.tokens:
        return 0 if check_tokens(args.tokens, args.size, args.weight) else 1
    if args.matrix:
        colors = extract_colors(open(args.matrix, encoding="utf-8").read())
        print(f"{len(colors)} unique colors in {args.matrix}; pairs with WCAG ≥ {args.min_ratio}:\n")
        for a, b in permutations(colors, 2):
            if wcag_ratio(parse_color(a), parse_color(b)) >= args.min_ratio:
                report(a, b, args.size, args.weight)
        return 0
    if args.pairs:
        for line in open(args.pairs, encoding="utf-8"):
            parts = line.split()
            if len(parts) < 2 or line.lstrip().startswith("#!"):
                continue
            ok &= report(parts[0], parts[1], args.size, args.weight, " ".join(parts[2:]))
        return 0 if ok else 1
    if not (args.fg and args.bg):
        ap.print_help()
        return 2
    ok = report(args.fg, args.bg, args.size, args.weight)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
