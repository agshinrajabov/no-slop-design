#!/usr/bin/env python3
"""
audit_repo.py — keep the skill honest about itself.

Checks that the documentation, the templates and the scripts still describe the same skill:

  1. every `references/*.md` exists, is listed in SKILL.md's reference index, and is reachable from a phase row
  2. every template referenced by SKILL.md / references exists in templates/
  3. README's counted claims (references, tells, lint rules) match reality
  4. version is identical in SKILL.md frontmatter, .claude-plugin/plugin.json and marketplace.json,
     and the top CHANGELOG entry matches it
  5. Standard mode's promises are keepable: the artefacts it says it writes have a template with the
     sections it needs (register, direction, art direction, review of record)
  6. SKILL.md stays under the 500-line progressive-disclosure guidance; references have a table of contents
  7. no reference file names a sibling that does not exist

Usage:
  python3 scripts/audit_repo.py            # human report, exit 1 on any error
  python3 scripts/audit_repo.py --json
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def rel(*p: str) -> str:
    return os.path.join(ROOT, *p)


def read(path: str) -> str:
    with open(rel(path), encoding="utf-8") as fh:
        return fh.read()


def audit() -> tuple[list[str], list[str], dict]:
    errors: list[str] = []
    warnings: list[str] = []
    facts: dict = {}

    refs = sorted(os.path.basename(p) for p in glob.glob(rel("references", "*.md")))
    templates = sorted(os.path.basename(p) for p in glob.glob(rel("templates", "*")))
    skill = read("SKILL.md")
    readme = read("README.md")
    facts["references"] = len(refs)
    facts["templates"] = len(templates)

    # 1. reference index coverage
    listed = set(re.findall(r"references/([a-z0-9-]+\.md)", skill))
    for missing in sorted(set(refs) - listed):
        errors.append(f"references/{missing} exists but SKILL.md never names it")
    for ghost in sorted(listed - set(refs)):
        errors.append(f"SKILL.md names references/{ghost}, which does not exist")

    # 2. templates named by the skill exist
    named_templates = set(re.findall(r"templates/([a-z0-9\-./*]+)", skill + " ".join(read(f"references/{r}") for r in refs)))
    for t in sorted(named_templates):
        if "*" in t:
            continue
        if not os.path.exists(rel("templates", t)):
            errors.append(f"templates/{t} is referenced but missing")

    # 3. README counted claims
    anti = read("references/anti-slop.md")
    rows = [l for l in anti.splitlines() if l.startswith("|") and not re.match(r"^\|[\s:|-]+\|$", l)]
    headers = [l for l in rows if re.search(r"\| *(Tell|Bad|Slop|Pattern|Legitimate only when|Where|Check) *\|", l)]
    tells = len(rows) - len(headers)
    lint_src = read("scripts/slop_lint.py")
    lint_rules = len(re.findall(r'^\s*\("([a-z-]+)", "(HIGH|MED|LOW)"', lint_src, re.M)) + len(
        re.findall(r'out\.append\(\("([a-z-]+)"', lint_src)
    ) + len(re.findall(r'findings\.append\(\{"rule": "([a-z-]+)"', lint_src))
    facts.update(tells=tells, lint_rules=lint_rules)

    def claim(pattern: str, actual: int, label: str, tolerance: int = 0) -> None:
        m = re.search(pattern, readme)
        if not m:
            warnings.append(f"README no longer states the {label} count")
            return
        stated = int(m.group(1))
        if abs(stated - actual) > tolerance:
            errors.append(f"README claims {stated} {label}, actual {actual}")

    claim(r"(\d+) deep references", len(refs), "references")
    claim(r"roughly (\d+) tells", tells, "tells", tolerance=3)
    claim(r"(\d+) of the mechanical ones", lint_rules, "lint rules")

    # 4. version consistency
    versions = {
        "SKILL.md": re.search(r'^\s*version:\s*"([\d.]+)"', skill, re.M),
        "plugin.json": re.search(r'"version":\s*"([\d.]+)"', read(".claude-plugin/plugin.json")),
    }
    vals = {k: (m.group(1) if m else None) for k, m in versions.items()}
    market = read(".claude-plugin/marketplace.json")
    vals["marketplace.json"] = sorted(set(re.findall(r'"version":\s*"([\d.]+)"', market)))
    facts["versions"] = vals
    flat = {vals["SKILL.md"], vals["plugin.json"], *vals["marketplace.json"]} - {None}
    if len(flat) > 1:
        errors.append(f"version mismatch across manifests: {sorted(flat)}")
    top_change = re.search(r"^## ([\d.]+)", read("CHANGELOG.md"), re.M)
    if top_change and vals["SKILL.md"] and top_change.group(1) != vals["SKILL.md"]:
        errors.append(f"CHANGELOG top entry {top_change.group(1)} != version {vals['SKILL.md']}")

    # 5. Standard mode promises are keepable
    design_tpl = read("templates/DESIGN.md")
    for needed, why in [
        ("Expression register", "the register is a non-negotiable"),
        ("Imagery art direction", "Phase 3 writes the art direction here in Standard mode"),
        ("Alternative considered", "Standard mode records the alternative one register away"),
        ("Review of record", "Standard mode writes the review here instead of a separate file"),
    ]:
        if needed not in design_tpl:
            errors.append(f"templates/DESIGN.md has no '{needed}' section — {why}")
    log = json.loads(read("templates/design-log.json"))
    if "register" not in json.dumps(log):
        errors.append("templates/design-log.json does not record the expression register")

    # 6. progressive disclosure
    skill_lines = len(skill.splitlines())
    facts["skill_lines"] = skill_lines
    if skill_lines > 500:
        errors.append(f"SKILL.md is {skill_lines} lines; the spec guidance is under 500")
    elif skill_lines > 400:
        warnings.append(f"SKILL.md is {skill_lines} lines; keep depth in references/")
    for r in refs:
        body = read(f"references/{r}")
        if len(body.splitlines()) > 100 and not re.search(r"^##\s+Contents", body, re.M):
            warnings.append(f"references/{r} is long and has no Contents list")

    # 7. sibling references resolve (token names like `stack.md` are values, not files)
    token_stems = {"stack", "inset", "inline", "control", "card", "sheet", "pill", "base", "raised",
                   "overlay", "modal", "sunken", "fast", "slow", "gutter", "page"}
    for r in refs:
        body = read(f"references/{r}")
        for sib in set(re.findall(r"`([a-z0-9-]+\.md)`", body)):
            if sib[:-3] in token_stems:
                continue
            if sib.endswith(".md") and sib not in refs and sib not in templates and sib not in {"SKILL.md", "README.md", "CHANGELOG.md", "CONTRIBUTING.md"}:
                warnings.append(f"references/{r} names `{sib}`, which is not a reference or template")

    return errors, warnings, facts


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    errors, warnings, facts = audit()
    if args.json:
        print(json.dumps({"errors": errors, "warnings": warnings, "facts": facts}, indent=2))
    else:
        print(f"no-slop-design self-audit — {facts['references']} references, {facts['templates']} templates, "
              f"{facts['tells']} tells, {facts['lint_rules']} lint rules, SKILL.md {facts['skill_lines']} lines")
        print(f"version: {facts['versions']}\n")
        for w in warnings:
            print("warning:", w)
        for e in errors:
            print("ERROR:", e)
        print("\n" + ("FAIL" if errors else "PASS"))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
