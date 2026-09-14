#!/usr/bin/env python3
"""
shoot.py — the review screenshots in one command, so no run spends ten minutes building its own harness.

The 1.7 field test spent about a third of its time writing iframe wrapper pages and a screenshot script, then left
them in the deliverable. This does the same job with headless Chrome and the standard library, writes everything
outside the project, and turns the two phone checks the review gate asks for into measurements:

  - full-page renders at desktop width and at 375 px, and a JavaScript-disabled render
  - the 375 px editing test: set the signature interaction's inputs, keep the edited control on screen, and report
    whether the result is visible in the same 812 px viewport
  - horizontal overflow at 375 px: the page itself, and every scroll container (a table that scrolls needs a cue)
  - the dark share of the full page, for `design_log.py add --screenshot`

Usage:
  python3 scripts/shoot.py index.html
  python3 scripts/shoot.py index.html --set "#pages=12" --set "#urgent=on"
  python3 scripts/shoot.py index.html --set "#pages=12" --expect ".result"     # name the result if auto-detect misses
  python3 scripts/shoot.py index.html --out /tmp/shots --json

Exit 1 when the edited result is off screen or the page scrolls sideways at 375 px; 3 when Chrome is missing.
Screenshots go to <tmp>/nsd-shots/<project> unless --out says otherwise. Keep them out of the deliverable.
"""
from __future__ import annotations

import argparse
import html
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
MAX_H = 16000          # Chrome refuses larger windows; longer pages are cut and reported
PHONE_W, PHONE_H = 375, 812


def find_chrome(explicit: str | None) -> str | None:
    cands = [explicit, os.environ.get("CHROME"),
             "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
             "/Applications/Chromium.app/Contents/MacOS/Chromium",
             "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"]
    cands += [shutil.which(n) for n in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "chrome", "msedge")]
    for c in cands:
        if c and os.path.exists(c):
            return c
    return None


def parse_set(spec: str) -> tuple[str, str]:
    """'#pages=12' -> ('#pages', '12'). The selector may itself contain '=' inside [attr=value]."""
    m = re.match(r"^(.*[^=\s])\s*=\s*([^=]*)$", spec)
    if not m:
        raise ValueError(f"--set expects selector=value, got {spec!r}")
    return m.group(1).strip(), m.group(2).strip()


PROBE_JS = r"""
const ACTIONS = __ACTIONS__, EXPECT = __EXPECT__, VH = __VH__;
const f = document.getElementById('nsd');
function report(o) { document.getElementById('nsd-out').textContent = JSON.stringify(o); }
f.addEventListener('load', () => setTimeout(() => {
  let d;
  try { d = f.contentDocument; if (!d) throw new Error('no access'); }
  catch (e) { report({error: 'cannot read the page (cross-origin?) — pass a local file'}); return; }
  const w = f.contentWindow, out = {height: d.documentElement.scrollHeight, width: d.documentElement.scrollWidth};
  out.containers = [...d.querySelectorAll('body *')].filter(el => {
    const s = w.getComputedStyle(el);
    return /(auto|scroll)/.test(s.overflowX) && el.scrollWidth > el.clientWidth + 1 && el.clientWidth > 0;
  }).slice(0, 12).map(el => ({
    selector: el.id ? '#' + el.id : el.tagName.toLowerCase() + (el.classList.length ? '.' + [...el.classList].join('.') : ''),
    scrollWidth: el.scrollWidth, clientWidth: el.clientWidth, table: !!el.querySelector('table')
  }));
  if (!ACTIONS.length) { report(out); return; }
  // results can live outside the interaction root (a sticky bar is often a sibling), so watch every live region
  // on the page and prefer the ones whose text the edit changed
  const RESULTS = EXPECT || 'output, [aria-live]';
  const before = new Map([...d.querySelectorAll(RESULTS)].map(el => [el, el.textContent]));
  let last = null; out.set = [];
  for (const [sel, val] of ACTIONS) {
    const el = d.querySelector(sel);
    if (!el) { out.set.push([sel, 'not found']); continue; }
    if (el.type === 'checkbox' || el.type === 'radio') el.checked = /^(1|true|on|yes|checked)$/i.test(val);
    else el.value = val;
    el.dispatchEvent(new Event('input', {bubbles: true}));
    el.dispatchEvent(new Event('change', {bubbles: true}));
    out.set.push([sel, 'ok']); last = el;
  }
  if (last) { last.scrollIntoView({block: 'center'}); last.focus({preventScroll: true}); }
  setTimeout(() => {
    const cands = [...d.querySelectorAll(RESULTS)];
    const shown = el => { const r = el.getBoundingClientRect(), s = w.getComputedStyle(el);
      return r.width > 0 && r.height > 0 && s.visibility !== 'hidden' && s.display !== 'none' && !el.closest('[hidden]')
        && r.bottom > 0 && r.top < VH && (el.textContent || '').trim().length > 0; };
    const changed = cands.filter(el => before.has(el) && before.get(el) !== el.textContent);
    // when the edit changed some result, only a changed one on screen counts; otherwise any visible result
    const vis = (changed.length ? changed : cands).filter(shown);
    out.result = {candidates: cands.length, changed: changed.length, visible: vis.length > 0,
                  text: vis.length ? vis[0].textContent.replace(/\s+/g, ' ').trim().slice(0, 90) : null,
                  edited: last ? (() => { const r = last.getBoundingClientRect(); return r.bottom > 0 && r.top < VH; })() : null};
    report(out);
  }, 400);
}, 600));
"""


def wrapper(src: str, w: int, h: int, actions=None, expect=None, probe=False) -> str:
    body = f'<iframe id="nsd" src="{html.escape(src)}" style="border:0;display:block;width:{w}px;height:{h}px"></iframe>'
    if probe or actions:
        js = (PROBE_JS.replace("__ACTIONS__", json.dumps(actions or []))
              .replace("__EXPECT__", json.dumps(expect)).replace("__VH__", str(h)))
        body += f'<pre id="nsd-out" style="display:none">pending</pre><script>{js}</script>'
    return f'<!doctype html><html><head><meta charset="utf-8"></head><body style="margin:0;overflow:hidden">{body}</body></html>'


def chrome(binary: str, url: str, args: list[str], timeout: int = 40) -> subprocess.CompletedProcess | None:
    """One headless call, retried once: a headless Chrome occasionally stalls on start-up, and a second launch
    is cheaper than a stuck review."""
    cmd = [binary, "--headless", "--disable-gpu", "--no-sandbox", "--hide-scrollbars", "--no-first-run",
           "--allow-file-access-from-files", "--virtual-time-budget=6000", *args, url]
    for _ in range(2):
        try:
            return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        except subprocess.TimeoutExpired:
            continue
    return None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("page", help="local HTML file (or a file:// / http://localhost URL)")
    ap.add_argument("--out", help="output folder (default: <tmp>/nsd-shots/<project>)")
    ap.add_argument("--width", type=int, default=1280, help="desktop width (default 1280)")
    ap.add_argument("--set", action="append", default=[], metavar="SELECTOR=VALUE",
                    help="an input to change for the 375 px editing test; repeat for several; the last one is kept on screen")
    ap.add_argument("--expect", help="selector of the result element (default: every output/[aria-live] on the page, "
                                     "preferring those the edit changed)")
    ap.add_argument("--no-nojs", action="store_true", help="skip the JavaScript-disabled render")
    ap.add_argument("--chrome", help="path to a Chrome/Chromium/Edge binary (or set CHROME)")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    binary = find_chrome(args.chrome)
    if not binary:
        print("shoot.py: no Chrome/Chromium/Edge found. Set CHROME=/path/to/chrome, or take the same shots with Playwright:\n"
              "  page.set_viewport_size({'width': 1280, 'height': 800}); page.screenshot(path='desktop.png', full_page=True)\n"
              "  and at 375x812 after changing the main input. Say in the review what could not be verified.")
        return 3

    if re.match(r"^(https?|file):", args.page):
        src, project = args.page, re.sub(r"\W+", "-", args.page.split("//", 1)[-1]).strip("-")[:40]
        page_dir = None
    else:
        path = os.path.abspath(args.page)
        if not os.path.exists(path):
            print(f"shoot.py: {args.page} does not exist")
            return 2
        src, page_dir = "file://" + path, os.path.dirname(path)
        project = os.path.basename(page_dir) or "page"
    out = os.path.abspath(args.out or os.path.join(tempfile.gettempdir(), "nsd-shots", project))
    if page_dir and (out + os.sep).startswith(page_dir + os.sep) and os.sep + "design" + os.sep not in out + os.sep:
        print(f"shoot.py: {out} is inside the deliverable. Screenshots are review evidence, not product — "
              "use the default temp folder or design/review/")
        return 2
    os.makedirs(out, exist_ok=True)
    try:
        actions = [list(parse_set(s)) for s in args.set]
    except ValueError as e:
        print(f"shoot.py: {e}")
        return 2

    def write(name: str, content: str) -> str:
        p = os.path.join(out, name)
        with open(p, "w", encoding="utf-8") as fh:
            fh.write(content)
        return "file://" + p

    def probe(w: int, h: int, acts=None) -> dict:
        url = write(f"_probe-{w}.html", wrapper(src, w, h, acts, args.expect, probe=True))
        r = chrome(binary, url, ["--dump-dom", f"--window-size={max(w, 500)},{h}"])
        m = re.search(r'<pre id="nsd-out"[^>]*>(.*?)</pre>', r.stdout if r else "", re.S)
        if not m or m.group(1) == "pending":
            return {"error": "the page did not finish loading in time" if r else "Chrome timed out"}
        try:
            return json.loads(html.unescape(m.group(1)))
        except json.JSONDecodeError:
            return {"error": "unreadable probe output"}

    def shot(name: str, w: int, h: int, extra=(), acts=None, scale=1.0) -> str | None:
        url = write(f"_{name}.html", wrapper(src, w, h, acts, args.expect))
        png = os.path.join(out, f"{name}.png")
        if os.path.exists(png):
            os.remove(png)
        chrome(binary, url, [f"--window-size={w},{h}", f"--screenshot={png}", f"--force-device-scale-factor={scale}", *extra])
        return png if os.path.exists(png) else None

    report: dict = {"out": out, "chrome": binary}
    desk = probe(args.width, 900)
    phone = probe(PHONE_W, PHONE_H)
    for label, p in (("desktop", desk), ("phone", phone)):
        if "error" in p:
            print(f"shoot.py: {label} probe failed: {p['error']}")
            return 2
    dh, ph = min(desk["height"], MAX_H), min(phone["height"], MAX_H)
    report["desktop"] = {"size": [args.width, desk["height"]], "png": shot(f"desktop-{args.width}", args.width, dh)}
    report["phone"] = {"size": [PHONE_W, phone["height"]], "png": shot(f"phone-{PHONE_W}", PHONE_W, ph),
                       "page_overflow_px": max(0, phone["width"] - PHONE_W), "scroll_containers": phone["containers"]}
    if not args.no_nojs:
        report["nojs"] = {"png": shot(f"nojs-{args.width}", args.width, min(int(desk["height"] * 1.3), MAX_H),
                                      extra=["--disable-javascript"])}   # blink-settings=scriptEnabled=false writes no PNG
    measure = shot("measure", args.width, dh, scale=0.5)   # half scale: same dark share, a quarter of the decoding
    if measure:
        sys.path.insert(0, HERE)
        import design_log  # noqa: E402
        share = design_log.dark_share([measure])
        report["surface"] = {"dark_share": round(share, 2), "polarity": design_log.polarity(share), "png": measure}
    if actions:
        edit = probe(PHONE_W, PHONE_H, actions)
        report["edit"] = {**edit, "png": shot(f"edit-{PHONE_W}", PHONE_W, PHONE_H, acts=actions)}
    for f in os.listdir(out):
        if f.startswith("_") and f.endswith(".html"):
            os.remove(os.path.join(out, f))

    problems = []
    if report["phone"]["page_overflow_px"]:
        problems.append(f"the page scrolls sideways at 375 px by {report['phone']['page_overflow_px']} px")
    e = report.get("edit")
    if e and "error" not in e and not e.get("result", {}).get("visible"):
        problems.append("after changing the inputs at 375 px no result is visible in the viewport")
    report["problems"] = problems

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(f"screenshots in {out}")
        print(f"  desktop  {args.width}×{desk['height']}  {report['desktop']['png']}")
        print(f"  phone    {PHONE_W}×{phone['height']}  {report['phone']['png']}")
        if "nojs" in report:
            print(f"  no-JS    {report['nojs']['png']}   look: is every section visible, is the static fallback there?")
        if desk["height"] > MAX_H or phone["height"] > MAX_H:
            print(f"  note: the page is taller than {MAX_H}px; renders are cut there")
        conts = report["phone"]["scroll_containers"]
        for c in conts:
            kind = "table" if c["table"] else "content"
            print(f"  scroll   {c['selector']} scrolls {kind} {c['scrollWidth']}>{c['clientWidth']} px at 375 — "
                  "is there a visible edge cue, or should it reflow? (components.md §8)")
        if "surface" in report:
            s = report["surface"]
            print(f"  surface  dark share {s['dark_share']:.2f} → {s['polarity']}; record with "
                  f"design_log.py add ... --screenshot {s['png']}")
        if e:
            if "error" in e:
                print(f"  edit     could not run: {e['error']}")
            else:
                r = e.get("result", {})
                missing = [s for s, st in e.get("set", []) if st != "ok"]
                print(f"  edit     {' '.join(a[0] + '=' + a[1] for a in actions)} at 375×812 → result "
                      f"{'VISIBLE' if r.get('visible') else 'NOT VISIBLE'}"
                      + (f" (“{r['text']}”)" if r.get("text") else "") + f"  {e.get('png')}")
                if missing:
                    print(f"           selectors not found: {', '.join(missing)}")
                if not r.get("candidates"):
                    print("           no output/[aria-live] result found; pass --expect <selector>")
                elif not r.get("changed"):
                    print("           no result changed after the edit — check the selector and value, or pass --expect")
        elif not actions:
            print("  edit     skipped — pass --set '<main input selector>=<value>' to run the 375 px editing test")
        for p in problems:
            print("PROBLEM:", p)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
