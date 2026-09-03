#!/usr/bin/env python3
"""
build_tokens.py — compile W3C DTCG design tokens (JSON) into platform outputs. Stdlib only.

Usage:
  python3 build_tokens.py tokens/*.json --out build/                 # all formats
  python3 build_tokens.py tokens/*.json --format css --out build/
  python3 build_tokens.py tokens/*.json --format css,tailwind,swift,kotlin,dart,flat-json
  python3 build_tokens.py tokens/*.json --check                      # only validate + list unresolved aliases

Input conventions (see references/design-tokens.md):
  • DTCG format: leaf tokens have "$value" and "$type"; groups nest freely; "$description" optional.
  • Aliases: "$value": "{color.primitive.blue.600}" — curly-brace path, resolved recursively.
  • Modes: a file named *.dark.json (or any *.<mode>.json) overrides the same token paths for that mode.
    Base file(s) have no mode suffix. Mode outputs are emitted as
    [data-theme="dark"] { … } and, for "dark" only, also under @media (prefers-color-scheme: dark).
  • Composite types supported for CSS: color, dimension, number, fontFamily, fontWeight, duration,
    cubicBezier, shadow (single or list), typography (expanded to --token-*-size/-lh/-weight/-family/-tracking).

Output naming: token path "color.text.primary" → CSS var --color-text-primary,
Tailwind v4 @theme uses the same var names so `text-text-primary` / `bg-surface-raised` utilities appear.
Swift/Kotlin/Dart emit only color/dimension/number/fontWeight/duration leaves as constants.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from typing import Any

ALIAS_RE = re.compile(r"^\{([^}]+)\}$")
INLINE_ALIAS_RE = re.compile(r"\{([^}]+)\}")


# --------------------------------------------------------------------------- load & flatten
def deep_merge(a: dict, b: dict) -> dict:
    out = dict(a)
    for k, v in b.items():
        if k in out and isinstance(out[k], dict) and isinstance(v, dict) and "$value" not in v:
            out[k] = deep_merge(out[k], v)
        else:
            out[k] = v
    return out


def flatten(node: dict, prefix: tuple = (), inherited_type: str | None = None) -> dict[str, dict]:
    """Return {"a.b.c": {"$value":..., "$type":..., ...}} for every leaf."""
    leaves: dict[str, dict] = {}
    node_type = node.get("$type", inherited_type)
    if "$value" in node:
        leaf = dict(node)
        leaf["$type"] = node_type
        leaves[".".join(prefix)] = leaf
        return leaves
    for k, v in node.items():
        if k.startswith("$"):
            continue
        if isinstance(v, dict):
            leaves.update(flatten(v, prefix + (k,), node_type))
    return leaves


def mode_of(path: str) -> str | None:
    base = os.path.basename(path)
    parts = base.split(".")
    return parts[-2] if len(parts) >= 3 and parts[-1] == "json" else None


def load(files: list[str]) -> tuple[dict[str, dict], dict[str, dict[str, dict]]]:
    base: dict = {}
    modes: dict[str, dict] = {}
    for f in files:
        with open(f, encoding="utf-8") as fh:
            data = json.load(fh)
        m = mode_of(f)
        if m:
            modes[m] = deep_merge(modes.get(m, {}), data)
        else:
            base = deep_merge(base, data)
    base_flat = flatten(base)
    mode_flat = {m: flatten(d) for m, d in modes.items()}
    return base_flat, mode_flat


# --------------------------------------------------------------------------- resolve
class Unresolved(Exception):
    pass


def resolve_value(value: Any, table: dict[str, dict], depth: int = 0) -> Any:
    if depth > 32:
        raise Unresolved("alias loop")
    if isinstance(value, str):
        m = ALIAS_RE.match(value.strip())
        if m:
            target = m.group(1)
            if target not in table:
                raise Unresolved(target)
            return resolve_value(table[target]["$value"], table, depth + 1)
        if "{" in value:  # inline alias inside an expression e.g. "calc({space.4} * 2)"
            def sub(mm):
                t = mm.group(1)
                if t not in table:
                    raise Unresolved(t)
                return str(resolve_value(table[t]["$value"], table, depth + 1))
            return INLINE_ALIAS_RE.sub(sub, value)
        return value
    if isinstance(value, list):
        return [resolve_value(v, table, depth + 1) for v in value]
    if isinstance(value, dict):
        return {k: resolve_value(v, table, depth + 1) for k, v in value.items()}
    return value


def resolve_all(flat: dict[str, dict], overlay: dict[str, dict] | None = None) -> tuple[dict[str, dict], list[str]]:
    table = dict(flat)
    if overlay:
        for k, v in overlay.items():
            merged = dict(table.get(k, {}))
            merged.update(v)
            if not merged.get("$type") and k in flat:
                merged["$type"] = flat[k].get("$type")
            table[k] = merged
    out, errors = {}, []
    for path, leaf in table.items():
        try:
            out[path] = {**leaf, "$resolved": resolve_value(leaf["$value"], table)}
        except Unresolved as e:
            errors.append(f"{path}: unresolved alias {e}")
    return out, errors


# --------------------------------------------------------------------------- serializers
def css_name(path: str) -> str:
    return "--" + re.sub(r"[^a-z0-9-]+", "-", path.lower().replace(".", "-")).strip("-")


def css_value(t: str | None, v: Any) -> str | None:
    if v is None:
        return None
    if t == "color":
        if isinstance(v, dict):  # DTCG 2024+ object color
            comps = v.get("components") or v.get("channels")
            space = v.get("colorSpace", "srgb")
            if comps and space == "srgb":
                r, g, b = (round(c * 255) for c in comps[:3])
                a = v.get("alpha", 1)
                return f"rgb({r} {g} {b}" + (f" / {a})" if a != 1 else ")")
            if comps:
                return f"color({space} {' '.join(str(c) for c in comps)})"
            return v.get("hex")
        return str(v)
    if t == "dimension":
        if isinstance(v, dict):
            return f"{v.get('value')}{v.get('unit', 'px')}"
        return str(v) if not isinstance(v, (int, float)) else f"{v}px"
    if t == "duration":
        if isinstance(v, dict):
            return f"{v.get('value')}{v.get('unit', 'ms')}"
        return str(v) if not isinstance(v, (int, float)) else f"{v}ms"
    if t == "fontFamily":
        fams = v if isinstance(v, list) else [v]
        return ", ".join(f'"{f}"' if " " in f and not f.startswith('"') else f for f in fams)
    if t == "cubicBezier" and isinstance(v, list):
        return f"cubic-bezier({', '.join(str(x) for x in v)})"
    if t == "shadow":
        items = v if isinstance(v, list) else [v]
        parts = []
        for s in items:
            inset = "inset " if s.get("inset") else ""
            parts.append(
                f"{inset}{css_value('dimension', s.get('offsetX', 0))} {css_value('dimension', s.get('offsetY', 0))} "
                f"{css_value('dimension', s.get('blur', 0))} {css_value('dimension', s.get('spread', 0))} {css_value('color', s.get('color'))}"
            )
        return ", ".join(parts)
    if t == "typography":
        return None  # expanded separately
    return str(v)


def emit_css(resolved: dict[str, dict], selector: str) -> list[str]:
    lines = [f"{selector} {{"]
    for path in sorted(resolved):
        leaf = resolved[path]
        t, v = leaf.get("$type"), leaf["$resolved"]
        name = css_name(path)
        if t == "typography" and isinstance(v, dict):
            for key, sub_t in (("fontFamily", "fontFamily"), ("fontSize", "dimension"), ("fontWeight", "fontWeight"),
                               ("lineHeight", "number"), ("letterSpacing", "dimension")):
                if key in v:
                    suffix = {"fontFamily": "family", "fontSize": "size", "fontWeight": "weight",
                              "lineHeight": "lh", "letterSpacing": "tracking"}[key]
                    lines.append(f"  {name}-{suffix}: {css_value(sub_t, v[key])};")
            continue
        val = css_value(t, v)
        if val is not None:
            desc = f" /* {leaf['$description']} */" if leaf.get("$description") else ""
            lines.append(f"  {name}: {val};{desc}")
    lines.append("}")
    return lines


def build_css(base: dict, modes: dict[str, dict]) -> str:
    out = ["/* generated by no-slop-design build_tokens.py — do not edit by hand */"]
    out += emit_css(base, ":root")
    for mode, res in modes.items():
        changed = {k: v for k, v in res.items() if k in base and v["$resolved"] != base[k]["$resolved"]} or res
        out.append("")
        out += emit_css(changed, f'[data-theme="{mode}"]')
        if mode == "dark":
            out.append("")
            out.append("@media (prefers-color-scheme: dark) {")
            out += ["  " + l for l in emit_css(changed, ':root:not([data-theme="light"])')]
            out.append("}")
    return "\n".join(out) + "\n"


def build_tailwind(base: dict) -> str:
    """Tailwind v4 @theme block. Color tokens become bg-*/text-*/border-* utilities, spacing → p-*/m-*/gap-*, etc."""
    lines = ['@import "tailwindcss";', "", "@theme {"]
    for path in sorted(base):
        leaf = base[path]
        t, v = leaf.get("$type"), leaf["$resolved"]
        val = css_value(t, v)
        if val is None:
            continue
        name = css_name(path)
        # Tailwind namespaces: --color-*, --spacing-*, --font-*, --text-*, --radius-*, --shadow-*, --ease-*, --animate-*
        if not re.match(r"--(color|spacing|space|font|text|radius|shadow|ease|duration|breakpoint|leading|tracking)-", name):
            continue
        name = name.replace("--space-", "--spacing-")
        lines.append(f"  {name}: {val};")
    lines.append("}")
    return "\n".join(lines) + "\n"


def const_name(path: str) -> str:
    parts = re.split(r"[.\-_/ ]+", path)
    return parts[0].lower() + "".join(p[:1].upper() + p[1:] for p in parts[1:] if p)


def build_swift(base: dict, modes: dict[str, dict]) -> str:
    def swift_color(hexstr: str) -> str:
        r, g, b = (int(hexstr.lstrip("#")[i:i + 2], 16) / 255 for i in (0, 2, 4))
        return f"Color(red: {r:.4f}, green: {g:.4f}, blue: {b:.4f})"

    lines = ["// generated by no-slop-design build_tokens.py", "import SwiftUI", "", "enum DesignTokens {"]
    dark = modes.get("dark", {})
    for path in sorted(base):
        leaf = base[path]
        t, v = leaf.get("$type"), leaf["$resolved"]
        n = const_name(path)
        if t == "color" and isinstance(v, str) and v.startswith("#"):
            if path in dark and isinstance(dark[path]["$resolved"], str) and dark[path]["$resolved"] != v:
                lines.append(
                    f"    static let {n} = Color(UIColor {{ $0.userInterfaceStyle == .dark ? "
                    f"UIColor({swift_color(dark[path]['$resolved'])}) : UIColor({swift_color(v)}) }})"
                )
            else:
                lines.append(f"    static let {n} = {swift_color(v)}")
        elif t in ("dimension", "number", "duration") and isinstance(v, (int, float, str)):
            num = re.sub(r"[a-z%]+$", "", str(v))
            try:
                lines.append(f"    static let {n}: CGFloat = {float(num)}")
            except ValueError:
                pass
        elif t == "fontWeight":
            lines.append(f"    static let {n}: Font.Weight = {swift_weight(v)}")
    lines.append("}")
    return "\n".join(lines) + "\n"


def swift_weight(v) -> str:
    m = {100: "ultraLight", 200: "thin", 300: "light", 400: "regular", 500: "medium", 600: "semibold",
         700: "bold", 800: "heavy", 900: "black"}
    try:
        return "." + m.get(int(v), "regular")
    except (TypeError, ValueError):
        return ".regular"


def build_kotlin(base: dict, modes: dict[str, dict]) -> str:
    lines = ["// generated by no-slop-design build_tokens.py", "package design.tokens", "",
             "import androidx.compose.ui.graphics.Color", "import androidx.compose.ui.unit.dp", "",
             "object DesignTokens {"]
    dark = modes.get("dark", {})
    for path in sorted(base):
        leaf = base[path]
        t, v = leaf.get("$type"), leaf["$resolved"]
        n = const_name(path)
        if t == "color" and isinstance(v, str) and v.startswith("#"):
            lines.append(f"    val {n} = Color(0xFF{v.lstrip('#').upper()[:6]})")
            if path in dark and isinstance(dark[path]["$resolved"], str) and dark[path]["$resolved"] != v:
                lines.append(f"    val {n}Dark = Color(0xFF{dark[path]['$resolved'].lstrip('#').upper()[:6]})")
        elif t == "dimension" and isinstance(v, (int, float, str)):
            num = re.sub(r"[a-z%]+$", "", str(v))
            try:
                lines.append(f"    val {n} = {float(num)}.dp")
            except ValueError:
                pass
        elif t in ("number", "duration"):
            try:
                lines.append(f"    const val {n} = {float(re.sub(r'[a-z]+$', '', str(v)))}f")
            except ValueError:
                pass
    lines.append("}")
    return "\n".join(lines) + "\n"


def build_dart(base: dict, modes: dict[str, dict]) -> str:
    lines = ["// generated by no-slop-design build_tokens.py", "import 'package:flutter/material.dart';", "",
             "abstract final class DesignTokens {"]
    dark = modes.get("dark", {})
    for path in sorted(base):
        leaf = base[path]
        t, v = leaf.get("$type"), leaf["$resolved"]
        n = const_name(path)
        if t == "color" and isinstance(v, str) and v.startswith("#"):
            lines.append(f"  static const {n} = Color(0xFF{v.lstrip('#').upper()[:6]});")
            if path in dark and isinstance(dark[path]["$resolved"], str) and dark[path]["$resolved"] != v:
                lines.append(f"  static const {n}Dark = Color(0xFF{dark[path]['$resolved'].lstrip('#').upper()[:6]});")
        elif t in ("dimension", "number", "duration"):
            try:
                lines.append(f"  static const double {n} = {float(re.sub(r'[a-z%]+$', '', str(v)))};")
            except ValueError:
                pass
    lines.append("}")
    return "\n".join(lines) + "\n"


def build_flat_json(base: dict, modes: dict[str, dict]) -> str:
    out = {"base": {k: v["$resolved"] for k, v in base.items()}}
    for m, res in modes.items():
        out[m] = {k: v["$resolved"] for k, v in res.items()}
    return json.dumps(out, indent=2) + "\n"


# --------------------------------------------------------------------------- main
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="+", help="DTCG JSON files (mode files: *.dark.json etc.)")
    ap.add_argument("--out", default="build", help="output directory")
    ap.add_argument("--format", default="css,tailwind,swift,kotlin,dart,flat-json")
    ap.add_argument("--check", action="store_true", help="validate only")
    args = ap.parse_args()

    base_flat, mode_flat = load(args.files)
    base, errors = resolve_all(base_flat)
    modes: dict[str, dict] = {}
    for m, flat in mode_flat.items():
        res, errs = resolve_all(base_flat, flat)
        modes[m] = res
        errors += [f"[{m}] {e}" for e in errs]

    untyped = [p for p, l in base.items() if not l.get("$type")]
    print(f"tokens: {len(base)} base, modes: {', '.join(f'{m}({len(r)})' for m, r in modes.items()) or 'none'}")
    if untyped:
        print(f"warning: {len(untyped)} tokens without $type (inherit from group or add one): {untyped[:8]}{' …' if len(untyped) > 8 else ''}")
    for e in errors:
        print("error:", e)
    if args.check or errors:
        return 1 if errors else 0

    os.makedirs(args.out, exist_ok=True)
    fmts = [f.strip() for f in args.format.split(",")]
    writers = {
        "css": ("tokens.css", lambda: build_css(base, modes)),
        "tailwind": ("theme.css", lambda: build_tailwind(base)),
        "swift": ("DesignTokens.swift", lambda: build_swift(base, modes)),
        "kotlin": ("DesignTokens.kt", lambda: build_kotlin(base, modes)),
        "dart": ("design_tokens.dart", lambda: build_dart(base, modes)),
        "flat-json": ("tokens.flat.json", lambda: build_flat_json(base, modes)),
    }
    for f in fmts:
        if f not in writers:
            print("unknown format:", f)
            continue
        name, fn = writers[f]
        path = os.path.join(args.out, name)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(fn())
        print("wrote", path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
