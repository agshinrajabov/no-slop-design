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
sys.path.insert(0, HERE)
from design_log import LANGUAGE  # noqa: E402 — the nine axes and their vocabulary live with the recorder
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


REVEAL_JS = r"""
document.getElementById('nsd').addEventListener('load', function () {
  try { const d = this.contentDocument, st = d.createElement('style');
    st.textContent = '*{opacity:1!important;transform:none!important;animation:none!important;visibility:visible!important}';
    d.head.appendChild(st); } catch (e) {}
});
"""

PROBE_JS = r"""
const ACTIONS = __ACTIONS__, EXPECT = __EXPECT__, VH = __VH__, REVEAL = __REVEAL__;
const f = document.getElementById('nsd');
function report(o) { document.getElementById('nsd-out').textContent = JSON.stringify(o); }
f.addEventListener('load', () => setTimeout(() => {
  let d;
  try { d = f.contentDocument; if (!d) throw new Error('no access'); }
  catch (e) { report({error: 'cannot read the page (cross-origin?) — pass a local file'}); return; }
  if (REVEAL) { const st = d.createElement('style'); st.textContent = '*{opacity:1!important;transform:none!important;animation:none!important;visibility:visible!important}'; d.head.appendChild(st); }
  const w = f.contentWindow, out = {height: d.documentElement.scrollHeight, width: d.documentElement.scrollWidth};
  out.containers = [...d.querySelectorAll('body *')].filter(el => {
    const s = w.getComputedStyle(el);
    return /(auto|scroll)/.test(s.overflowX) && el.scrollWidth > el.clientWidth + 1 && el.clientWidth > 0;
  }).slice(0, 12).map(el => ({
    selector: el.id ? '#' + el.id : el.tagName.toLowerCase() + (el.classList.length ? '.' + [...el.classList].join('.') : ''),
    scrollWidth: el.scrollWidth, clientWidth: el.clientWidth, table: !!el.querySelector('table')
  }));
  // the first viewport's boldest move: display type against body type, the largest graphic, the largest colour field
  {
    const vw = w.innerWidth, vh = Math.min(w.innerHeight, VH), area = vw * vh;
    const clip = r => Math.max(0, Math.min(r.right, vw) - Math.max(r.left, 0)) * Math.max(0, Math.min(r.bottom, vh) - Math.max(r.top, 0));
    const sizes = new Map(); let display = 0, displayInResult = false;
    for (const el of d.body.querySelectorAll('*')) {
      const own = [...el.childNodes].filter(n => n.nodeType === 3).map(n => n.textContent.trim()).join('');
      if (!own) continue;
      const r = el.getBoundingClientRect(), s = w.getComputedStyle(el);
      if (r.width === 0 || s.visibility === 'hidden' || s.display === 'none') continue;
      const fs = parseFloat(s.fontSize);
      sizes.set(fs, (sizes.get(fs) || 0) + own.length);
      if (r.top < vh && r.bottom > 0 && fs > display) { display = fs; displayInResult = !!el.closest('output, [aria-live]'); }
    }
    const body = [...sizes].sort((a, b) => b[1] - a[1])[0]?.[0] || 16;
    let graphic = 0, field = 0, graphicEl = null, fieldEl = null;
    const name = el => el.tagName.toLowerCase() + (el.id ? '#' + el.id : '') + (el.classList.length ? '.' + [...el.classList].slice(0, 2).join('.') : '');
    // real media only: a wrapper that carries data-nsd-anchor is a container, and an icon is not a graphic
    for (const el of d.body.querySelectorAll('svg, img, video, canvas')) {
      if (el.parentElement && el.parentElement.closest('svg')) continue;
      const r = el.getBoundingClientRect();
      if (r.width < 64 || r.height < 64) continue;
      const share = clip(r) / area;
      if (share > graphic) { graphic = share; graphicEl = name(el); }
    }
    // a colour field is a saturated colour; a near-black or near-white band is a surface, not a bold move
    // computed colours come back as oklch()/color() when the tokens are OKLCH; a 1×1 canvas turns any of them into sRGB
    const cv = document.createElement('canvas'); cv.width = cv.height = 1;
    const cx = cv.getContext('2d', {willReadFrequently: true});
    const rgba = css => { cx.clearRect(0, 0, 1, 1); cx.fillStyle = '#000'; cx.fillStyle = css; cx.fillRect(0, 0, 1, 1);
                          return cx.getImageData(0, 0, 1, 1).data; };
    for (const el of [d.body, ...d.body.querySelectorAll('header, section, div, main, article, aside, figure')]) {
      const st = w.getComputedStyle(el);
      // alpha is read from the canvas (a regex on ", 0)" once dropped rgb(233, 178, 0)); a field can also be painted as
      // a one-colour gradient, which is how the 1.6 page drew its amber hero
      let css = st.backgroundColor;
      if (rgba(css)[3] < 128 && /gradient/.test(st.backgroundImage)) {
        const stops = st.backgroundImage.match(/(?:oklch|oklab|lab|lch|rgba?|hsla?|color)\([^()]*\)|#[0-9a-f]{3,8}\b/gi) || [];
        if (stops.length && stops.every(s => s === stops[0])) css = stops[0];
      }
      if (!css || css === 'transparent') continue;
      const [r, g, b, a] = rgba(css);
      if (a < 128) continue;
      const hi = Math.max(r, g, b), lo = Math.min(r, g, b);
      const sat = hi === 0 ? 0 : (hi - lo) / hi;
      if (sat < 0.35 || hi < 60) continue;
      const share = clip(el.getBoundingClientRect()) / area;
      if (share > field) { field = share; fieldEl = name(el); }
    }
    out.firstView = {display, displayInResult, body, ratio: +(display / body).toFixed(1), graphic: +graphic.toFixed(2), graphicEl,
                     field: +field.toFixed(2), fieldEl};
  }
  // the page's skeleton: which device each top-level section uses, in order. Six test pages in a row came out as
  // interaction > steps > table > form with no image; the first-viewport check could not see it.
  {
    const vw0 = w.innerWidth;
    const secs = [...d.querySelectorAll('section, header, article')].filter(el =>
      !(el.parentElement && el.parentElement.closest('section, header, article')) && el.getBoundingClientRect().height > 120);
    const kind = el => {
      if (el.matches('[data-nsd-interaction]') || el.querySelector('[data-nsd-interaction]')) return 'interaction';
      if (el.querySelector('form')) return 'form';
      if (el.querySelector('table')) return 'table';
      if (el.querySelector('img, picture, video')) return 'media';
      const box = el.getBoundingClientRect();
      if ([...el.querySelectorAll('svg')].some(s => { const r = s.getBoundingClientRect(); return r.width * r.height > 0.2 * box.width * box.height; })) return 'graphic';
      const lists = [...el.querySelectorAll('ol, ul, dl')].filter(l => l.children.length >= 3 && !l.closest('nav'));
      if (lists.length || el.querySelectorAll('[class*="step"]').length >= 3) return 'steps';
      return 'text';
    };
    out.skeleton = secs.map(kind);
    const bg = [...d.body.querySelectorAll('*')].filter(el => /url\(/.test(w.getComputedStyle(el).backgroundImage)
      && el.getBoundingClientRect().width > vw0 * 0.2).length;
    out.media = d.querySelectorAll('img, picture, video').length + bg;
    // the UI dialect: how controls, dividers, labels, section headers and the display face are drawn
    const ctrls = [...d.querySelectorAll('button, .btn, a[class*="button"], input:not([type=hidden]), select')]
      .filter(el => el.getBoundingClientRect().width > 0).slice(0, 40);
    const radii = ctrls.map(el => parseFloat(w.getComputedStyle(el).borderTopLeftRadius) || 0).sort((a, b) => a - b);
    const r = radii.length ? radii[Math.floor(radii.length / 2)] : 0;
    const shape = r < 3 ? 'square' : r <= 10 ? 'soft' : r <= 24 ? 'round' : 'pill';
    const ruled = secs.filter(el => { const s = w.getComputedStyle(el); return parseFloat(s.borderTopWidth) > 0 || parseFloat(s.borderBottomWidth) > 0
      || [...el.querySelectorAll('hr, li, tr')].some(x => parseFloat(w.getComputedStyle(x).borderBottomWidth) > 0 || parseFloat(w.getComputedStyle(x).borderTopWidth) > 0); }).length;
    const edges = secs.length && ruled / secs.length >= 0.4 ? 'ruled' : 'open';
    const caps = [...d.body.querySelectorAll('*')].filter(el => el.children.length === 0 && (el.textContent || '').trim().length > 2
      && w.getComputedStyle(el).textTransform === 'uppercase' && parseFloat(w.getComputedStyle(el).fontSize) < 15).length;
    const labels = caps >= 5 ? 'caps-labels' : 'plain-labels';
    let split = 0;
    for (const h of d.querySelectorAll('h2')) {
      const p = h.parentElement && [...h.parentElement.parentElement.querySelectorAll('p')].find(x => !h.parentElement.contains(x));
      if (!p) continue;
      const a = h.getBoundingClientRect(), b = p.getBoundingClientRect();
      if (Math.abs(a.top - b.top) < a.height && Math.abs(a.left - b.left) > 200) split++;
    }
    const headers = split >= 2 ? 'split-headers' : 'stacked-headers';
    const big = [...d.querySelectorAll('h1, h2')].sort((x, y) => parseFloat(w.getComputedStyle(y).fontSize) - parseFloat(w.getComputedStyle(x).fontSize))[0];
    const fam = big ? w.getComputedStyle(big).fontFamily.toLowerCase() : '';
    const display = /mono/.test(fam) ? 'mono' : /condensed|compressed|narrow|oswald|bebas|anton|league gothic|big shoulders|saira extra/.test(fam)
      ? 'condensed' : /serif/.test(fam.split(',')[0]) && !/sans/.test(fam.split(',')[0]) ? 'serif'
      : /(garamond|caslon|baskerville|fraunces|playfair|lora|newsreader|source serif|bitter|roboto slab|zilla|domine|spectral|cormorant|dm serif|instrument serif|libre bask)/.test(fam) ? 'serif' : 'grotesk';
    out.dialect = [shape, edges, labels, headers, display].join(';');
  }
  // the design language (design-language.md): nine axes from a closed vocabulary, measured over the first two
  // viewports so a competitor's site and this page are read the same way. Chroma is measured from pixels in Python.
  {
    const vw = w.innerWidth, region = Math.min(d.documentElement.scrollHeight, 1600), vh = Math.min(w.innerHeight, VH);
    const clipR = r => Math.max(0, Math.min(r.right, vw) - Math.max(r.left, 0)) * Math.max(0, Math.min(r.bottom, region) - Math.max(r.top, 0));
    const vis = el => { const s = w.getComputedStyle(el); return s.display !== 'none' && s.visibility !== 'hidden' && s.opacity !== '0'; };
    // density: the share of the region covered by lines of text (range rects of every text node, no double counting)
    let textArea = 0;
    const walker = d.createTreeWalker(d.body, NodeFilter.SHOW_TEXT);
    for (let n = walker.nextNode(); n; n = walker.nextNode()) {
      if (!n.textContent.trim() || !n.parentElement || /^(SCRIPT|STYLE|NOSCRIPT|TEMPLATE)$/.test(n.parentElement.tagName)) continue;
      if (!vis(n.parentElement)) continue;
      const rg = d.createRange(); rg.selectNode(n);
      for (const r of rg.getClientRects()) textArea += clipR(r);
    }
    const textShare = textArea / (vw * region);
    const density = textShare >= 0.16 ? 'tight' : textShare >= 0.07 ? 'medium' : 'airy';
    // type: the display face, finer than the dialect line
    const big = [...d.querySelectorAll('h1, h2')].filter(vis).sort((x, y) => parseFloat(w.getComputedStyle(y).fontSize) - parseFloat(w.getComputedStyle(x).fontSize))[0];
    const fam = big ? w.getComputedStyle(big).fontFamily.toLowerCase() : '';
    const first = fam.split(',')[0].replace(/["']/g, '').trim();
    const type = /^(system-ui|-apple-system|blinkmacsystemfont|helvetica( neue)?|arial|segoe ui|ui-sans-serif)$/.test(first) ? 'system'
      : /mono|courier|consolas|menlo/.test(first) ? 'mono'
      : /condensed|compressed|narrow|oswald|bebas|anton|league gothic|big shoulders|saira extra|barlow condensed|archivo narrow/.test(fam) ? 'condensed'
      : /slab|rockwell|arvo|zilla|bitter|roboto slab|josefin slab|crete|aleo|hepta/.test(fam) ? 'slab'
      : /(garamond|caslon|baskerville|fraunces|playfair|lora|newsreader|source serif|domine|spectral|cormorant|dm serif|instrument serif|libre bask|young serif|times|georgia|merriweather|crimson|literata|eb garamond|bodoni|didot|tiempos|freight|canela|editorial|ogg|reckless|romie|migra)/.test(first) || (/serif/.test(first) && !/sans/.test(first)) ? 'serif'
      : /(source sans|lato|open sans|pt sans|fira sans|noto sans|nunito|cabin|ubuntu|merriweather sans|mulish|hind|karla|alegreya sans|frutiger|myriad|verdana|tahoma|trebuchet|gill sans|optima|calibri)/.test(first) ? 'humanist'
      : 'grotesk';
    // imagery: what the first two viewports show that is not text
    let imagery = 'none', best = 0;
    const declared = d.querySelector('[data-nsd-anchor]');
    if (d.querySelector('canvas')) imagery = '3d';
    else {
      for (const el of d.body.querySelectorAll('svg, img, video, picture')) {
        if (el.parentElement && el.parentElement.closest('svg')) continue;
        const r = el.getBoundingClientRect();
        if (r.width < 64 || r.height < 64 || !vis(el)) continue;
        const a = clipR(r);
        if (a > best) { best = a; imagery = el.tagName.toLowerCase() === 'svg' ? 'illustration' : 'photo'; }
      }
      for (const el of d.body.querySelectorAll('*')) {
        if (!/url\(/.test(w.getComputedStyle(el).backgroundImage)) continue;
        const r = el.getBoundingClientRect(); const a = clipR(r);
        if (r.width >= 64 && r.height >= 64 && a > best) { best = a; imagery = 'photo'; }
      }
      if (best === 0) imagery = (out.firstView && out.firstView.ratio >= 6) ? 'type' : 'none';
      else if (declared && /product|interface|screenshot|packaging|object/.test((declared.getAttribute('data-nsd-anchor') || '').toLowerCase())) imagery = 'product';
    }
    // layout: where the first viewport's largest heading sits
    let layout = 'asymmetric';
    const grids = [...d.body.querySelectorAll('*')].filter(el => { const s = w.getComputedStyle(el); if (s.display !== 'grid') return false;
      const r = el.getBoundingClientRect(); return r.top < vh && r.bottom > 0 && r.width * Math.min(r.height, vh) > 0.4 * vw * vh
        && s.gridTemplateColumns.split(' ').filter(t => t !== '0px').length >= 3; });
    const h = [...d.body.querySelectorAll('h1, h2, [role=heading]')].filter(el => { const r = el.getBoundingClientRect(); return vis(el) && r.top < vh && r.bottom > 0 && r.width > 0; })
      .sort((x, y) => parseFloat(w.getComputedStyle(y).fontSize) - parseFloat(w.getComputedStyle(x).fontSize))[0];
    if (grids.length) layout = 'grid';
    else if (h) {
      const r = h.getBoundingClientRect(), ta = w.getComputedStyle(h).textAlign;
      const centre = (r.left + r.right) / 2;
      if (Math.abs(centre - vw / 2) < vw * 0.06 && (ta === 'center' || Math.abs(r.left - (vw - r.right)) < vw * 0.06)) layout = 'centered';
      else if (r.left < vw * 0.14) layout = 'left';
    }
    // motion: what moves, read from the stylesheets and scripts this page loads
    let keyframes = 0, transitions = 0, cross = false;
    for (const sh of d.styleSheets) {
      try { for (const rule of sh.cssRules) { if (rule instanceof w.CSSKeyframesRule) keyframes++; else if (rule.style && rule.style.transitionProperty && rule.style.transitionProperty !== 'all' && rule.style.transitionProperty !== '') transitions++;
        else if (rule.style && rule.style.transition) transitions++; } } catch (e) { cross = true; }
    }
    const scripts = [...d.scripts].map(sc => (sc.src || '') + ' ' + (sc.textContent || '').slice(0, 20000)).join(' ');
    const motion = (d.querySelector('canvas') || /three(\.min)?\.js|gsap|scrolltrigger|lenis|locomotive|webgl|@react-three|rive|lottie/i.test(scripts)) ? 'scene'
      : (keyframes >= 2 || /IntersectionObserver|data-reveal|\.reveal\b|aos\.js|animate-on-scroll|animation-timeline/i.test(scripts + [...d.styleSheets].map(s => { try { return [...s.cssRules].map(r => r.cssText).join(' ').slice(0, 20000); } catch (e) { return ''; } }).join(' '))) ? 'choreographed'
      : (transitions > 0 || [...d.querySelectorAll('a, button')].slice(0, 30).some(el => { const t = w.getComputedStyle(el).transitionDuration; return t && t !== '0s'; })) ? 'functional' : 'none';
    // controls: how the main button is drawn
    let controls = 'solid';
    const btns = [...d.querySelectorAll('button, a[class*="btn"], a[class*="button"], input[type=submit], [role=button]')]
      .filter(el => { const r = el.getBoundingClientRect(); return vis(el) && r.top < region && r.width > 40 && r.height > 24; })
      .sort((x, y) => { const a = x.getBoundingClientRect(), b = y.getBoundingClientRect(); return b.width * b.height - a.width * a.height; });
    if (btns.length) {
      const b = btns[0], s = w.getComputedStyle(b);
      const bw = parseFloat(s.borderTopWidth) || 0, rad = parseFloat(s.borderTopLeftRadius) || 0;
      const cv2 = document.createElement('canvas'); cv2.width = cv2.height = 1; const cx2 = cv2.getContext('2d', {willReadFrequently: true});
      const px = css => { cx2.clearRect(0, 0, 1, 1); cx2.fillStyle = '#000'; cx2.fillStyle = css; cx2.fillRect(0, 0, 1, 1); return cx2.getImageData(0, 0, 1, 1).data; };
      const bg = px(s.backgroundColor);
      const hardShadow = /rgba?\([^)]*\)\s+\d+px\s+\d+px\s+0(px)?/.test(s.boxShadow) && !/0px 0px/.test(s.boxShadow);
      if ((bw >= 2 && rad < 3) || hardShadow) controls = 'raw';
      else if (bg[3] < 128 && !/gradient/.test(s.backgroundImage)) controls = 'hairline';
    }
    out.language = {density: +textShare.toFixed(3), densityWord: density, type, imagery, layout, motion, controls,
                    crossOriginStyles: cross};
  }
  if (!ACTIONS.length) { report(out); return; }
  // results can live outside the interaction root (a sticky bar is often a sibling), so watch every live region
  // on the page and prefer the ones whose text the edit changed
  const RESULTS = EXPECT || 'output, [aria-live]';
  const before = new Map([...d.querySelectorAll(RESULTS)].map(el => [el, el.textContent]));
  // a mobile dock often repeats the result without being a live region (aria-hidden, to avoid a double announcement)
  const leaves = () => [...d.body.querySelectorAll('*')].filter(el => el.children.length === 0
    && !/^(SCRIPT|STYLE|INPUT|SELECT|OPTION|TEXTAREA|BUTTON)$/.test(el.tagName));
  const beforeLeaf = new Map(leaves().map(el => [el, el.textContent]));
  const numbers = el => (el.textContent.match(/\d[\d\s.,  ]*\d|\d/g) || []).map(s => s.replace(/[\s  ]/g, ''));
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
    let vis = (changed.length ? changed : cands).filter(shown), via = vis.length ? 'live region' : null;
    if (!vis.length && !EXPECT) {
      // no live region on screen: accept any visible text the edit changed that repeats a number from the result
      const nums = new Set(changed.flatMap(numbers));
      vis = [...beforeLeaf].filter(([el, t]) => el.isConnected && el.textContent !== t && !(last && last.contains(el)))
        .map(([el]) => el).filter(el => shown(el) && (!nums.size || numbers(el).some(n => nums.has(n))));
      via = vis.length ? 'a copy of the result outside the live region (e.g. a sticky dock)' : null;
    }
    out.result = {candidates: cands.length, changed: changed.length, visible: vis.length > 0, via,
                  text: vis.length ? vis[0].textContent.replace(/\s+/g, ' ').trim().slice(0, 90) : null,
                  edited: last ? (() => { const r = last.getBoundingClientRect(); return r.bottom > 0 && r.top < VH; })() : null};
    report(out);
  }, 400);
}, 600));
"""


# The bold move every register above R1 owes its first viewport (expression-register.md §4b). Any one of these passes.
BOLD = {  # register: (display type ÷ body type, largest graphic share, saturated colour-field share with type ≥ 3×)
    "R2": (6.0, 0.30, 0.40),
    "R3": (8.0, 0.45, 0.60),
    "R4": (8.0, 0.45, 0.60),
}


# A phone's 375×812 first screen: type scales down harder than the body, so the type floor is lower, and a colour field
# needs less type on it. Calibrated on five translation runs: 1.6 (field 92%) and 1.8 (type 4.6×) pass; 1.7.1 (2×),
# 1.9 (3.5×) and 1.10 (2.4×, its seal graphic pushed below the inputs) fail.
BOLD_PHONE = {
    "R2": (4.0, 0.25, 0.40, 2.5),
    "R3": (4.5, 0.35, 0.55, 2.5),
    "R4": (4.5, 0.35, 0.55, 2.5),
}


def bold_move(first_view: dict, register: str | None, phone: bool = False, relax: float = 1.0) -> tuple[bool, str]:
    """Judge the first viewport against the register's bold-move thresholds. R1 (or unknown) always passes. `relax`
    scales the floors for a design language whose first screen is the product or dense text (relax_for)."""
    key = (register or "").upper()[:2]
    t = BOLD_PHONE.get(key) if phone else BOLD.get(key)
    if t and relax != 1.0:
        t = tuple(round(v * relax, 2) for v in t[:3]) + tuple(t[3:])
    field_type = t[3] if t and len(t) > 3 else 3
    fv = first_view or {}
    ratio, graphic, field = fv.get("ratio", 0), fv.get("graphic", 0), fv.get("field", 0)
    facts = (f"display type {fv.get('display', 0):.0f}px = {ratio}× body · largest graphic {graphic:.0%}"
             + (f" ({fv['graphicEl']})" if fv.get("graphicEl") else "")
             + f" · saturated colour field {field:.0%}" + (f" ({fv['fieldEl']})" if fv.get("fieldEl") else ""))
    if not t:
        return True, facts
    ok = ratio >= t[0] or graphic >= t[1] or (field >= t[2] and ratio >= field_type)
    need = (f"{key}{' on a phone' if phone else ''} needs one of: type ≥ {t[0]:g}× body, a graphic ≥ {t[1]:.0%} of the "
            f"viewport, or a colour field ≥ {t[2]:.0%} with type ≥ {field_type:g}×"
            + (" (floors scaled for this design language)" if relax != 1.0 else ""))
    return ok, facts + ("" if ok else f" — {need}")


COMPOSITIONS = {
    "graphic-hero": "a drawn graphic or photograph owns the first viewport",
    "result-poster": "the interaction's answer (a time, a date, a price) set as the poster, usually on a colour field",
    "type-poster": "a claim or name set at poster scale",
    "field-and-heading": "a saturated colour field with a heading and the controls on it",
    "heading-and-panel": "a heading beside or above a panel of controls or facts",
}


def composition(first_view: dict | None) -> str:
    """Name the first viewport's structure from the measurements, so the history log records what the page is, not
    what the agent says it is. Two different industries came out as 'result-poster' in a row (1.11 translation, 1.11
    clinic) and the word-overlap check on free-text structure notes did not notice."""
    fv = first_view or {}
    if fv.get("graphic", 0) >= 0.30:
        return "graphic-hero"
    if fv.get("displayInResult") and (fv.get("field", 0) >= 0.40 or fv.get("ratio", 0) >= 6):
        return "result-poster"
    if fv.get("ratio", 0) >= 6:
        return "type-poster"
    if fv.get("field", 0) >= 0.40:
        return "field-and-heading"
    return "heading-and-panel"




def chroma_share(png: str, step: int = 4) -> float:
    """Share of sampled pixels that carry colour (saturation ≥ 0.25 on a value ≥ 60): achromatic pages sit near 0,
    a page with a photograph or a colour field well above 0.25."""
    sys.path.insert(0, HERE)
    import design_log  # noqa: E402
    w, h, bpp, rows = design_log.read_png(png)
    hit = total = 0
    for y in range(0, h, step):
        row = rows[y]
        for x in range(0, w, step):
            o = x * bpp
            r, g, b = row[o], row[o + 1], row[o + 2]
            hi, lo = max(r, g, b), min(r, g, b)
            total += 1
            hit += hi >= 60 and (hi - lo) / hi >= 0.25
    return hit / total if total else 0.0


def chroma_word(share: float) -> str:
    return "achromatic" if share < 0.05 else "low" if share < 0.30 else "saturated"


def language_profile(desk: dict, surface: str | None, chroma: str | None) -> str:
    """The nine-axis profile string shoot.py prints and design_log.py records, in LANGUAGE order."""
    lang, dial = desk.get("language") or {}, (desk.get("dialect") or ";;;;").split(";")
    return ";".join([surface or "?", chroma or "?", lang.get("type", "?"), lang.get("densityWord", "?"), dial[0] or "?",
                     lang.get("imagery", "?"), lang.get("layout", "?"), lang.get("motion", "?"), lang.get("controls", "?")])


def market_profile(profiles: list[str]) -> tuple[str, list[str]]:
    """The market fingerprint: per axis, the most common word across the measured pages, with a note per axis where
    the pages disagree (so a split market is visible, not averaged away)."""
    from collections import Counter
    cols = [p.split(";") for p in profiles if p and len(p.split(";")) == len(LANGUAGE)]
    if not cols:
        return "", []
    words, notes = [], []
    for i, axis in enumerate(LANGUAGE):
        c = Counter(col[i] for col in cols if col[i] != "?")
        if not c:
            words.append("?"); continue
        top, n = c.most_common(1)[0]
        words.append(top)
        if n < len(cols) and len(c) > 1:
            notes.append(f"{axis}: {', '.join(f'{k} ×{v}' for k, v in c.most_common())}")
    return ";".join(words), notes


def language_from(page_dir: str | None) -> str | None:
    """The 'Design language:' profile written in design/DESIGN.md next to the page, if it is valid."""
    for base in filter(None, [page_dir, page_dir and os.path.dirname(page_dir)]):
        p = os.path.join(base, "design", "DESIGN.md")
        if os.path.exists(p):
            m = re.search(r"Design language\**\s*(?:\|\s*|:\**\s*|\([^)]*\)\**:?\s*)\**\s*`?([a-z0-9;?-]+)", open(p, encoding="utf-8", errors="ignore").read(), re.I)
            if m and len(m.group(1).split(";")) == len(LANGUAGE):
                return m.group(1).lower()
    return None


def relax_for(language: str | None) -> float:
    """Bold-move floors are scaled for languages whose first viewport is the product or dense text: a developer tool
    or a documentation site owns its first screen with the interface, at 20–25% of the viewport, not a poster."""
    if not language:
        return 1.0
    parts = language.split(";")
    if len(parts) != len(LANGUAGE):
        return 1.0
    imagery, density = parts[5], parts[3]
    return 0.66 if imagery == "product" or density == "tight" else 1.0


def register_from(page_dir: str | None) -> str | None:
    """The register written in design/DESIGN.md (or the brief) next to the page."""
    for base in filter(None, [page_dir, page_dir and os.path.dirname(page_dir)]):
        for name in ("DESIGN.md", "brief.md"):
            p = os.path.join(base, "design", name)
            if os.path.exists(p):
                m = re.search(r"Expression register\**\s*(?:\|\s*|:\**\s*)\**\s*(R[1-4])", open(p, encoding="utf-8", errors="ignore").read())
                if m:
                    return m.group(1)
    return None


def wrapper(src: str, w: int, h: int, actions=None, expect=None, probe=False, fetched=False) -> str:
    """A fetched competitor page runs with its scripts off (sandbox) and its reveal states forced visible: hydration
    errors, reveal-on-scroll and consent scripts otherwise leave a blank or broken first screen to measure."""
    sandbox = ' sandbox="allow-same-origin"' if fetched else ""
    body = f'<iframe id="nsd" src="{html.escape(src)}"{sandbox} style="border:0;display:block;width:{w}px;height:{h}px"></iframe>'
    if probe or actions:
        js = (PROBE_JS.replace("__ACTIONS__", json.dumps(actions or []))
              .replace("__EXPECT__", json.dumps(expect)).replace("__VH__", str(h)).replace("__REVEAL__", json.dumps(fetched)))
        body += f'<pre id="nsd-out" style="display:none">pending</pre><script>{js}</script>'
    elif fetched:
        body += f'<script>{REVEAL_JS}</script>'
    return f'<!doctype html><html><head><meta charset="utf-8"></head><body style="margin:0;overflow:hidden">{body}</body></html>'


SCHEME = "light"      # set from --scheme; headless Chrome otherwise inherits the machine's dark mode


def chrome(binary: str, url: str, args: list[str], timeout: int = 40) -> subprocess.CompletedProcess | None:
    """One headless call, retried once: a headless Chrome occasionally stalls on start-up, and a second launch
    is cheaper than a stuck review. The colour scheme is always explicit: a 1.9 run measured a light page as 79%
    dark because the Mac it ran on was in dark mode."""
    cmd = [binary, "--headless", "--disable-gpu", "--no-sandbox", "--hide-scrollbars", "--no-first-run",
           "--allow-file-access-from-files", "--virtual-time-budget=6000",
           f"--blink-settings=preferredColorScheme={0 if SCHEME == 'dark' else 1}", *args, url]
    for _ in range(2):
        try:
            return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        except subprocess.TimeoutExpired:
            continue
    return None


def fetch(url: str, dest: str) -> str | None:
    """Download a competitor page and pin its relative URLs with <base>, so the same-origin probe can read it."""
    import urllib.request
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Macintosh) AppleWebKit/537.36 Chrome/128 Safari/537.36",
                                               "Accept": "text/html,*/*"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            body = r.read().decode("utf-8", errors="ignore")
    except Exception as err:  # noqa: BLE001 — any failure means "judge by eye"
        print(f"shoot.py: could not fetch {url} ({err.__class__.__name__}) — open it in a browser and write its profile by eye")
        return None
    body = re.sub(r"<meta[^>]+http-equiv=[\"']?content-security-policy[^>]*>", "", body, flags=re.I)
    base = f'<base href="{html.escape(url)}">'
    body = re.sub(r"(<head[^>]*>)", r"\1" + base, body, count=1, flags=re.I) if re.search(r"<head[^>]*>", body, re.I) else base + body
    with open(dest, "w", encoding="utf-8") as fh:
        fh.write(body)
    return "file://" + dest


def profile_mode(args, binary: str) -> int:
    """Measure the design language of one or more pages — usually the category's competitors — and print the market
    fingerprint (the most common word per axis). Renders nothing for review."""
    out = os.path.abspath(args.out or os.path.join(tempfile.gettempdir(), "nsd-shots", "profile"))
    os.makedirs(out, exist_ok=True)
    sys.path.insert(0, HERE)
    import design_log  # noqa: E402
    results = []
    for i, target in enumerate(args.page):
        if re.match(r"^https?:", target):
            src = fetch(target, os.path.join(out, f"_fetch-{i}.html"))
            if not src:
                results.append({"page": target, "error": "fetch failed"}); continue
        elif re.match(r"^file:", target):
            src = target
        else:
            path = os.path.abspath(target)
            if not os.path.exists(path):
                results.append({"page": target, "error": "does not exist"}); continue
            src = "file://" + path
        fetched = bool(re.match(r"^https?:", target))
        purl = os.path.join(out, f"_probe-{i}.html")
        with open(purl, "w", encoding="utf-8") as fh:
            fh.write(wrapper(src, args.width, 800, None, None, probe=True, fetched=fetched))
        r = chrome(binary, "file://" + purl, ["--dump-dom", f"--window-size={max(args.width, 500)},800"])
        m = re.search(r'<pre id="nsd-out"[^>]*>(.*?)</pre>', r.stdout if r else "", re.S)
        try:
            desk = json.loads(html.unescape(m.group(1))) if m and m.group(1) != "pending" else {"error": "did not load"}
        except json.JSONDecodeError:
            desk = {"error": "unreadable probe output"}
        if "error" in desk:
            results.append({"page": target, "error": desk["error"]}); continue
        surl = os.path.join(out, f"_shot-{i}.html")
        with open(surl, "w", encoding="utf-8") as fh:
            fh.write(wrapper(src, args.width, 1600, fetched=fetched))
        png = os.path.join(out, f"language-{i}.png")
        if os.path.exists(png):
            os.remove(png)
        chrome(binary, "file://" + surl, [f"--window-size={args.width},1600", f"--screenshot={png}", "--force-device-scale-factor=0.5"])
        surf = chroma = None
        if os.path.exists(png):
            surf = design_log.polarity(design_log.dark_share([png]))
            chroma = chroma_word(chroma_share(png))
        prof = language_profile(desk, surf, chroma)
        results.append({"page": target, "language": prof, "text_share": (desk.get("language") or {}).get("density"),
                        "display_ratio": (desk.get("firstView") or {}).get("ratio"), "png": png if os.path.exists(png) else None,
                        "cross_origin_styles": (desk.get("language") or {}).get("crossOriginStyles")})
    for f in os.listdir(out):
        if f.startswith("_"):
            os.remove(os.path.join(out, f))
    market, notes = market_profile([r.get("language", "") for r in results if "language" in r])
    if args.json:
        print(json.dumps({"axes": list(LANGUAGE), "pages": results, "market": market, "split": notes}, indent=2, ensure_ascii=False))
        return 0 if market else 2
    print(f"design language per page ({';'.join(LANGUAGE)}):")
    for r in results:
        if "error" in r:
            print(f"  {r['page']}: {r['error']}")
        else:
            print(f"  {r['language']:<75} {r['page']}" + ("  (styles cross-origin: motion may read low)" if r.get("cross_origin_styles") else ""))
            if r.get("png"):
                print(f"           look: {r['png']} — a page rendered without its scripts can be wrong (a menu left open, a hero missing); "
                      "then judge that page by eye in a browser with the same words")
    if market:
        print(f"market   {market}")
        for n in notes:
            print(f"  split  {n}")
        print(f"  write in DESIGN.md: Market: {market} — from {sum('language' in r for r in results)} pages; "
              "then choose this page's language and name the axes it departs on (design-language.md §4)")
    else:
        print("no page could be measured — write the market profile by eye with the vocabulary in design-language.md §2")
    return 0 if market else 2


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("page", nargs="+", help="local HTML file (or a file:// / http:// URL); several, or --profile, measures the "
                    "design language of each and the market fingerprint (design-language.md §3)")
    ap.add_argument("--profile", action="store_true", help="only measure the design-language profile of each page (no review renders)")
    ap.add_argument("--language", help="the nine-axis design language written in DESIGN.md, for the bold-move floors "
                    "(default: read from design/DESIGN.md)")
    ap.add_argument("--out", help="output folder (default: <tmp>/nsd-shots/<project>)")
    ap.add_argument("--width", type=int, default=1280, help="desktop width (default 1280)")
    ap.add_argument("--set", action="append", default=[], metavar="SELECTOR=VALUE",
                    help="an input to change for the 375 px editing test; repeat for several; the last one is kept on screen")
    ap.add_argument("--expect", help="selector of the result element (default: every output/[aria-live] on the page, "
                                     "preferring those the edit changed)")
    ap.add_argument("--scheme", choices=("light", "dark"), default="light",
                    help="prefers-color-scheme for every render (default light — the machine's own mode is never used). "
                         "Render the scheme the audience will see; run twice for pages that support both")
    ap.add_argument("--register", help="R1–R4 for the bold-move check (default: read from design/DESIGN.md)")
    ap.add_argument("--no-nojs", action="store_true", help="skip the JavaScript-disabled render")
    ap.add_argument("--chrome", help="path to a Chrome/Chromium/Edge binary (or set CHROME)")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    global SCHEME
    SCHEME = args.scheme

    binary = find_chrome(args.chrome)
    if not binary:
        print("shoot.py: no Chrome/Chromium/Edge found. Set CHROME=/path/to/chrome, or take the same shots with Playwright:\n"
              "  page.set_viewport_size({'width': 1280, 'height': 800}); page.screenshot(path='desktop.png', full_page=True)\n"
              "  and at 375x812 after changing the main input. Say in the review what could not be verified.")
        return 3

    if args.profile or len(args.page) > 1:
        return profile_mode(args, binary)
    args.page = args.page[0]
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
    out = os.path.abspath(args.out or os.path.join(tempfile.gettempdir(), "nsd-shots", project + ("-dark" if args.scheme == "dark" else "")))
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

    report: dict = {"out": out, "chrome": binary, "scheme": args.scheme}
    desk = probe(args.width, 800)
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
    lang_png = shot("language", args.width, min(1600, dh), scale=0.5)   # the first two viewports: the same region profile mode reads
    if lang_png:
        sys.path.insert(0, HERE)
        import design_log  # noqa: E402
        lsurf = design_log.polarity(design_log.dark_share([lang_png]))
        lchroma = chroma_word(chroma_share(lang_png))
        os.remove(lang_png)
    else:
        lsurf = lchroma = None
    report["language"] = language_profile(desk, lsurf, lchroma)
    if actions:
        edit = probe(PHONE_W, PHONE_H, actions)
        report["edit"] = {**edit, "png": shot(f"edit-{PHONE_W}", PHONE_W, PHONE_H, acts=actions)}
    for f in os.listdir(out):
        if f.startswith("_") and f.endswith(".html"):
            os.remove(os.path.join(out, f))

    problems = []
    register = args.register or register_from(page_dir)
    declared_lang = args.language or language_from(page_dir)
    relax = relax_for(declared_lang)
    report["declared_language"] = declared_lang
    bold_ok, bold_facts = bold_move(desk.get("firstView"), register, relax=relax)
    comp = composition(desk.get("firstView"))
    skeleton = ">".join(desk.get("skeleton") or [])
    report["skeleton"], report["media"], report["dialect"] = skeleton, desk.get("media", 0), desk.get("dialect")
    report["first_view"] = {**(desk.get("firstView") or {}), "register": register, "bold_move": bold_ok, "summary": bold_facts,
                            "composition": comp}
    phone_ok, phone_facts = bold_move(phone.get("firstView"), register, phone=True, relax=relax)
    report["phone"]["first_view"] = {**(phone.get("firstView") or {}), "bold_move": phone_ok, "summary": phone_facts}
    if not phone_ok:
        problems.append(f"the phone's first screen (375×812) has no bold move for {register} ({phone_facts.split(' — ')[0]}) "
                        "— a graphic that falls below the inputs on a phone does not count; expression-register.md §4b")
    if not bold_ok:
        problems.append(f"the first viewport at {args.width}×800 has no bold move for {register} ({bold_facts.split(' — ')[0]}) "
                        "— expression-register.md §4b")
    if report["phone"]["page_overflow_px"]:
        problems.append(f"the page scrolls sideways at 375 px by {report['phone']['page_overflow_px']} px")
    e = report.get("edit")
    if e and "error" not in e and not e.get("result", {}).get("visible"):
        problems.append("after changing the inputs at 375 px no result is visible in the viewport")
    report["problems"] = problems

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(f"screenshots in {out}  (prefers-color-scheme: {args.scheme})")
        print(f"  desktop  {args.width}×{desk['height']}  {report['desktop']['png']}")
        print(f"  phone    {PHONE_W}×{phone['height']}  {report['phone']['png']}")
        if "nojs" in report:
            print(f"  no-JS    {report['nojs']['png']}   look: is every section visible, is the static fallback there?")
        if desk["height"] > MAX_H or phone["height"] > MAX_H:
            print(f"  note: the page is taller than {MAX_H}px; renders are cut there")
        print(f"  first    {report['first_view']['register'] or 'register unknown'}: {bold_facts}"
              + ("" if bold_ok else "  ← NO BOLD MOVE"))
        print(f"  first375 {phone_facts}" + ("" if phone_ok else "  ← NO BOLD MOVE ON THE PHONE"))
        print(f"  compose  {comp} — {COMPOSITIONS[comp]}; record with design_log.py add ... --composition {comp}")
        print(f"  skeleton {skeleton or '(no top-level sections found)'} · {desk.get('media', 0)} image(s); record with "
              f"--skeleton {skeleton} --media {desk.get('media', 0)} --display-ratio {(desk.get('firstView') or {}).get('ratio', 0)}")
        print(f"  dialect  {desk.get('dialect', '?')} (controls;dividers;labels;section headers;display face); record with "
              f"--dialect '{desk.get('dialect', '')}'")
        print(f"  language {report.get('language', '?')} ({';'.join(LANGUAGE)}); record with --language '{report.get('language', '')}'"
              + (f" · DESIGN.md declares {declared_lang}" if declared_lang else " · no 'Design language:' line in DESIGN.md"))
        if declared_lang and report.get("language") and declared_lang != report["language"]:
            diff = [ax for ax, a, b in zip(LANGUAGE, declared_lang.split(";"), report["language"].split(";")) if a != b and a != "?" and b != "?"]
            if diff:
                print(f"           measured differs from the declared language on {', '.join(diff)} — record the measured one, or fix the page")
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
                if r.get("visible") and r.get("via") and r["via"] != "live region":
                    print(f"           seen via {r['via']}")
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
