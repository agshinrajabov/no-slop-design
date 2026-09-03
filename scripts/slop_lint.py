#!/usr/bin/env python3
"""
slop_lint.py — static scan for "AI slop" UI signatures in web + mobile source.

Usage:
  python3 slop_lint.py src/                       # scan a tree
  python3 slop_lint.py index.html style.css       # specific files
  python3 slop_lint.py src/ --json                # machine-readable
  python3 slop_lint.py src/ --strict              # exit 1 on any HIGH finding

Scans: .html .htm .css .scss .jsx .tsx .js .ts .vue .svelte .astro .mdx .dart .swift .kt .xml
Heuristic by design: every hit is a question ("is this earned?"), not a verdict.
Findings map to references/anti-slop.md sections so you can read the "why" and the fix.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import Counter, defaultdict

EXTS = {".html", ".htm", ".css", ".scss", ".jsx", ".tsx", ".js", ".ts", ".vue", ".svelte", ".astro", ".mdx",
        ".dart", ".swift", ".kt", ".xml"}
SKIP_DIRS = {"node_modules", ".git", "dist", "build", ".next", ".nuxt", "out", "coverage", "vendor", ".dart_tool",
             "Pods", "DerivedData", "__pycache__"}

# (id, severity, regex, message, anti-slop section)
RULES = [
    # ---------------------------------------------------------------- color
    ("purple-gradient", "HIGH",
     r"(from-(violet|purple|indigo|fuchsia)-\d+|to-(violet|purple|indigo|fuchsia|pink)-\d+|"
     r"linear-gradient\([^)]*#(7c3aed|8b5cf6|a855f7|6366f1|4f46e5|c084fc|d946ef|ec4899)|"
     r"linear-gradient\([^)]*(violet|purple|indigo|fuchsia))",
     "purple/indigo/violet gradient — the single most recognisable AI-UI tell", "§1 Color"),
    ("gradient-text", "HIGH", r"bg-clip-text\s+text-transparent|text-transparent\s+bg-clip-text|-webkit-background-clip:\s*text",
     "gradient text on headline", "§1 Color"),
    ("glow-blob", "HIGH", r"blur-(2xl|3xl)|filter:\s*blur\((6|7|8|9)\d px\)|filter:\s*blur\(1\d\dpx\)",
     "giant blurred glow blob / background orb", "§1 Color"),
    ("neon-on-black", "MED", r"#0a0a0a|#000000\b|bg-black\b|#0b0b0f|#09090b",
     "pure black background — check it isn't the 'AI dark mode' with neon accents", "§1 Color"),
    ("tailwind-default-primary", "MED", r"\b(bg|text|border|ring)-(blue|indigo|violet)-(500|600)\b",
     "Tailwind default blue/indigo as brand color — define a real brand token", "§1 Color"),
    # ---------------------------------------------------------------- typography
    ("default-font", "HIGH", r"font-family:[^;]*\b(Inter|Roboto|Poppins|Open Sans|Montserrat|Lato)\b|"
                             r"fonts\.googleapis\.com/css2?\?family=(Inter|Roboto|Poppins|Open\+Sans|Montserrat|Lato)\b|"
                             r"GoogleFonts\.(inter|roboto|poppins|openSans|montserrat|lato)\(",
     "default-reflex typeface (Inter/Roboto/Poppins/Open Sans/Montserrat/Lato) — choose on purpose, see typography.md", "§2 Typography"),
    ("system-ui-primary", "MED", r"font-family:\s*(system-ui|-apple-system|ui-sans-serif)\b",
     "system-ui as PRIMARY typeface (fine as fallback, and fine for native iOS/Android UI; a tell on the web)", "§2 Typography"),
    ("startup-default-font", "MED", r"Space Grotesk|Space\+Grotesk|Plus Jakarta|Plus\+Jakarta|Sora\b|Outfit\b|Manrope\b|DM Sans|DM\+Sans",
     "2023-2026 'startup default' typeface — only if the moodboard actually calls for it", "§2 Typography"),
    ("tracking-widest-caps", "LOW", r"tracking-(wider|widest)\s+uppercase|uppercase\s+tracking-(wider|widest)",
     "spaced uppercase eyebrow label — the 'FEATURES' eyebrow cliché", "§2 Typography"),
    # ---------------------------------------------------------------- layout & components
    ("three-col-grid", "MED", r"grid-cols-3\b|grid-template-columns:\s*repeat\(3,|md:grid-cols-3\b|lg:grid-cols-3\b",
     "3-column grid — is it the icon+title+blurb feature grid?", "§3 Layout"),
    ("icon-circle", "HIGH", r"(rounded-full|rounded-(xl|2xl))\s+[^\"']*bg-(\w+)-(50|100)|bg-(\w+)/10\s+[^\"']*rounded-(full|xl|2xl)|"
                            r"\.icon-(wrap|box|circle)|w-1[02]\s+h-1[02]\s+[^\"']*rounded-(full|xl)",
     "icon in a tinted circle/rounded square — SaaS starter template look", "§3 Layout"),
    ("accent-left-border", "HIGH", r"border-l-(2|4|8)\s|border-left:\s*[2-6]px\s+solid",
     "colored left border on card/quote", "§3 Layout"),
    ("everything-centered", "LOW", r"text-center", "text-center (density check — count below)", "§3 Layout"),
    ("uniform-radius", "LOW", r"rounded-(2xl|3xl)", "large radius (density check — is every element bubbly?)", "§3 Layout"),
    ("glassmorphism", "MED", r"backdrop-blur(-\w+)?\s+[^\"']*bg-(white|black|\w+)/\d+|bg-(white|black|\w+)/\d+\s+[^\"']*backdrop-blur|"
                             r"backdrop-filter:\s*blur",
     "glass card (blur + translucent fill) — earned only over real imagery", "§4 Components"),
    ("bento", "LOW", r"bento|col-span-2\s+row-span-2", "bento grid — the 2023 Apple-keynote homage", "§3 Layout"),
    ("wavy-divider", "MED", r"<path[^>]*d=\"M0,\d+\s*C|wave-divider|shape-divider|clip-path:\s*ellipse",
     "wavy SVG section divider", "§3 Layout"),
    ("dashed-border-decor", "LOW", r"border-dashed", "dashed border decoration", "§4 Components"),
    ("card-in-card", "LOW", r"shadow-(lg|xl|2xl)\s+[^\"']*rounded-(xl|2xl)\s+[^\"']*shadow-", "nested shadow cards", "§4 Components"),
    ("badge-pill-new", "MED", r"rounded-full[^>]*>\s*(✨|🚀|New|NEW|Beta|Introducing)", "pill badge 'New ✨' above hero headline", "§4 Components"),
    # ---------------------------------------------------------------- iconography / emoji
    ("emoji-ui", "HIGH", r"[\U0001F300-\U0001FAFF✨⭐⚡✅✔❌❤]",
     "emoji used as UI element / bullet / heading decoration", "§5 Iconography"),
    ("sparkles-icon", "HIGH", r"<Sparkles\b|lucide-sparkles|IconSparkles|sparkles-icon|Icons\.auto_awesome|sparkles\b",
     "the ✨ 'AI feature' sparkle icon", "§5 Iconography"),
    ("rocket-icon", "MED", r"<Rocket\b|lucide-rocket|rocket_launch|IconRocket", "rocket icon", "§5 Iconography"),
    # ---------------------------------------------------------------- copy
    ("slop-copy", "HIGH",
     r"\b(Unlock the power|Unleash|Supercharge|Elevate your|Seamless(ly)?|Effortless(ly)?|Revolutioni[sz]e|"
     r"Take your \w+ to the next level|all-in-one (solution|platform)|Welcome to|Empower(ing)? (your|teams)|"
     r"Built for the future|Next-generation|Cutting-edge|Game-chang(er|ing)|Say goodbye to|Say hello to|"
     r"In today's fast-paced|Streamline your|Transform (the way|your)|Experience the|Discover the|Join thousands|"
     r"Trusted by \d[\d,]*\+? (companies|teams|users)|Get started for free|Lightning[- ]fast|Blazing[- ]fast|"
     r"Your (journey|success) starts here|Made with ❤|Powered by AI)\b",
     "generic marketing copy — see content-microcopy.md banned list", "§6 Copy"),
    ("lorem", "MED", r"lorem ipsum|Lorem Ipsum", "placeholder text", "§6 Copy"),
    ("fake-social-proof", "MED", r"(Acme|Globex|Initech|Umbrella|Hooli|Stark Industries)\b|logo-cloud|trusted-by",
     "placeholder logo cloud / fake social proof", "§6 Copy"),
    # ---------------------------------------------------------------- motion
    ("fade-up-everything", "LOW", r"animate-fade-in-up|fade-in-up|whileInView|data-aos=",
     "scroll fade-up (density check — is every section doing it?)", "§7 Motion"),
    ("transition-all", "MED", r"transition:\s*all\b|transition-all\b", "transition: all — list properties explicitly", "§7 Motion"),
    ("outline-none", "HIGH", r"outline-none(?!\s+[^\"']*focus-visible)|outline:\s*none(?![^}]*focus-visible)",
     "focus outline removed — must be replaced with focus-visible ring", "§9 Accessibility"),
    ("hover-scale", "LOW", r"hover:scale-1\d\d|hover:-translate-y-[12]\b", "hover lift/scale on cards", "§7 Motion"),
    # ---------------------------------------------------------------- imagery / structure
    ("stock-avatar", "MED", r"randomuser\.me|pravatar\.cc|i\.pravatar|unsplash\.com/photo-\w+.*(?:face|portrait|person)|placeholder\.com|placehold\.co",
     "placeholder avatar/image service", "§8 Imagery"),
    ("hero-3cards-testimonials", "LOW", r"id=\"(features|testimonials|pricing|faq|cta)\"",
     "canonical section ids — is the page the hero→features→testimonials→pricing→CTA template?", "§3 Layout"),
    ("shadcn-default-theme", "MED", r"--primary:\s*222\.2 47\.4% 11\.2%|--ring:\s*215 20\.2% 65\.1%|--radius:\s*0\.5rem;\s*\}",
     "untouched shadcn/ui default theme values", "§1 Color"),
    ("mobile-emoji-tab", "MED", r"(BottomNavigationBarItem|Tab\()[^)]*[\U0001F300-\U0001FAFF]", "emoji in mobile tab bar", "§5 Iconography"),
    ("mobile-gradient-button", "MED", r"LinearGradient\([^)]*Colors\.(purple|deepPurple|indigo)|gradient:\s*LinearGradient",
     "gradient-filled button (Flutter/SwiftUI)", "§4 Components"),
    ("placeholder-box", "HIGH", r"\[(Photo|Image|Photograph|Illustration|Video|Hero image)[:\s][^\]]{0,160}\]",
     "bracketed image caption in a box instead of a real or designed placeholder image (visual-material.md §8)", "§8 Imagery"),
]

# File-level rules: evaluated once per HTML document
def file_rules(path: str, text: str):
    out = []
    if not path.lower().endswith((".html", ".htm", ".astro", ".vue", ".svelte", ".jsx", ".tsx", ".mdx")):
        return out
    base = os.path.basename(path).lower()
    if any(k in base for k in ("moodboard", "review", "spec", "storybook", "handoff")) or "data-nsd-doc" in text:
        return out  # working documents, not product pages
    is_page = re.search(r"<(main|section|header)\b", text, re.I) and len(text) > 3000
    has_media = re.search(r"<(img|picture|video|canvas)\b|<svg[^>]*(viewBox=\"0 0 (?!2[04] 2[04])[^\"]+\"|width=\"(?!1[0-9]|2[0-9]|3[0-2])\d{3,})", text, re.I)
    if is_page and not has_media:
        out.append(("no-imagery", "HIGH", "page-level document with no image, picture, video, or illustration element — text-only pages read as unfinished (visual-material.md §1)", "§8 Imagery"))
    dl_hero = re.search(r"<(header|section)[^>]*>(?:(?!</(header|section)>).){0,4000}<dl\b", text, re.I | re.S)
    if dl_hero and not has_media:
        out.append(("ledger-hero", "MED", "definition-list / fact table as the first-viewport composition with no visual anchor — the 'honest ledger' over-correction (anti-slop.md §8)", "§3 Layout"))

    # the "ledger site": label/value rows as the layout device across the page
    dl_count = len(re.findall(r"<dl\b", text, re.I))
    rowish = len(re.findall(r'class="[^"]*\b(fact|facts|ledger|spec|specs|meta-row|label-value|kv|detail-row)\b', text, re.I))
    if is_page and dl_count + rowish >= 3:
        out.append(("ledger-site", "MED", f"label/value tables used as the layout device in {dl_count + rowish} places — vary the device per section; this is the skill's own tell (expression-register.md §10)", "§3 Layout"))

    if is_page:
        img_count = len(re.findall(r"<img\b|<picture\b|<video\b", text, re.I))
        if 0 < img_count < 2 and len(text) > 12000:
            out.append(("thin-imagery", "MED", f"long page ({len(text) // 1000} kB of markup) carrying only {img_count} image element — imagery is treated as an obligation, not the argument (visual-material.md §1)", "§8 Imagery"))
    return out

COMPILED = [(i, s, re.compile(p, re.IGNORECASE if i not in ("emoji-ui", "mobile-emoji-tab") else 0), m, sec) for i, s, p, m, sec in RULES]
DENSITY_RULES = {  # id: (threshold per 100 lines, message)
    "everything-centered": (2.5, "text-center density is high — centred layouts read as 'template'; left-align body/section copy"),
    "uniform-radius": (2.0, "rounded-2xl/3xl density is high — establish a radius hierarchy (see spacing-layout.md)"),
    "fade-up-everything": (1.0, "scroll-triggered fade on most sections — motion should be 2-3 intentional moments"),
    "three-col-grid": (0.6, "many 3-col grids — layout is component-first, not composition-first"),
}


def iter_files(paths):
    for p in paths:
        if os.path.isfile(p):
            yield p
            continue
        for root, dirs, files in os.walk(p):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
            for f in files:
                if os.path.splitext(f)[1].lower() in EXTS:
                    yield os.path.join(root, f)


REVEAL_HIDE = re.compile(r"\.(reveal|fade-?in|animate-?in|scroll-?reveal|gsap|aos)[^{]*\{[^}]*opacity:\s*0", re.I)
REVEAL_SHOW = re.compile(r"\.(is-in|is-visible|in-view|revealed|is-revealed|aos-animate|active)\b", re.I)
NOJS_GUARD = re.compile(r"<noscript|\.no-js\b|html\.js\b|documentElement\.classList\.add\(['\"]js", re.I)


def scan(paths):
    findings, counts, total_lines = [], Counter(), 0
    reveal_hides, nojs_guard = [], False
    for path in iter_files(paths):
        try:
            text = open(path, encoding="utf-8", errors="ignore").read()
        except OSError:
            continue
        lines = text.splitlines()
        total_lines += len(lines)
        if REVEAL_HIDE.search(text) and REVEAL_SHOW.search(text):
            reveal_hides.append(path)
        if NOJS_GUARD.search(text):
            nojs_guard = True
        for rid, sev, msg, sec in file_rules(path, text):
            counts[rid] += 1
            findings.append({"rule": rid, "severity": sev, "file": path, "line": 1, "section": sec, "message": msg, "snippet": ""})
        is_native = path.endswith((".swift", ".kt", ".dart"))
        for ln, line in enumerate(lines, 1):
            if line.strip().startswith(("//", "#", "*", "/*")) and "font" not in line.lower():
                continue
            for rid, sev, rx, msg, sec in COMPILED:
                if rid == "system-ui-primary" and is_native:
                    continue
                if rx.search(line):
                    counts[rid] += 1
                    if rid in DENSITY_RULES:
                        continue  # aggregated below
                    findings.append({"rule": rid, "severity": sev, "file": path, "line": ln, "section": sec,
                                     "message": msg, "snippet": line.strip()[:140]})
    if reveal_hides and not nojs_guard:
        counts["reveal-no-fallback"] += 1
        findings.append({"rule": "reveal-no-fallback", "severity": "HIGH", "file": reveal_hides[0], "line": 0,
                         "section": "§7 Motion",
                         "message": "scroll-reveal styles hide content at rest (opacity: 0) with no no-JS fallback — "
                                    "if the script fails the page is blank. Add a <noscript> reset or gate the hiding "
                                    "behind a `js` class set by script (motion.md, anti-slop.md §7)",
                         "snippet": ""})
    for rid, (thr, msg) in DENSITY_RULES.items():
        if total_lines and counts[rid] / max(total_lines, 1) * 100 >= thr:
            findings.append({"rule": rid, "severity": "MED", "file": "(aggregate)", "line": 0,
                             "section": dict((r[0], r[4]) for r in RULES)[rid],
                             "message": f"{msg} ({counts[rid]} hits / {total_lines} lines)", "snippet": ""})
    return findings, counts, total_lines


def slop_score(findings, total_lines) -> tuple[str, int]:
    weight = {"HIGH": 3, "MED": 1.5, "LOW": 0.5}
    raw = sum(weight[f["severity"]] for f in findings)
    per_kloc = raw / max(total_lines / 1000, 0.25)
    grade = "A" if per_kloc < 1 else "B" if per_kloc < 4 else "C" if per_kloc < 10 else "D" if per_kloc < 20 else "F"
    return grade, round(per_kloc, 1)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--strict", action="store_true", help="exit 1 if any HIGH finding")
    args = ap.parse_args()

    findings, counts, total = scan(args.paths)
    findings.sort(key=lambda f: ({"HIGH": 0, "MED": 1, "LOW": 2}[f["severity"]], f["file"], f["line"]))
    grade, density = slop_score(findings, total)

    if args.json:
        print(json.dumps({"grade": grade, "weighted_per_kloc": density, "lines": total, "findings": findings}, indent=2))
    else:
        by_sev = defaultdict(list)
        for f in findings:
            by_sev[f["severity"]].append(f)
        print(f"no-slop-design slop lint — {total} lines scanned\n")
        for sev in ("HIGH", "MED", "LOW"):
            if not by_sev[sev]:
                continue
            print(f"== {sev} ({len(by_sev[sev])})")
            for f in by_sev[sev]:
                loc = f"{f['file']}:{f['line']}" if f["line"] else f["file"]
                print(f"  [{f['rule']}] {loc}\n      {f['message']}  ({f['section']})")
                if f["snippet"]:
                    print(f"      > {f['snippet']}")
            print()
        print(f"SLOP GRADE: {grade}   (weighted findings per 1k lines: {density})")
        print("A = no tells · B = a few earned choices to confirm · C = template-flavoured · D/F = reads as generated")
    if args.strict and any(f["severity"] == "HIGH" for f in findings):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
