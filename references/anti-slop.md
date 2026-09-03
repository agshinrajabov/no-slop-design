# Anti-Slop Catalog

**Read this before designing and again before delivering.** Every pattern below is a *tell*: a visual or verbal
choice that appears in generated UI not because anyone decided it, but because it is the statistical average of
the training data. The test for each is the same:

> **Was this chosen, or did it happen?** If you cannot name the brand attribute, content type, or user need that
> justifies it, it is slop. Replace it with a decision.

Why slop exists: models converge on the median of every Tailwind tutorial and SaaS template ever scraped. Tailwind
UI's `bg-indigo-500` placeholder became "what buttons look like"; shadcn's default card became "what a card looks
like"; the pattern then fed the next training set. Tools built on that stack (v0, Lovable, Bolt, Claude Design,
Stitch, Claude Code's own defaults) all inherit the same look. The look is not ugly. It is **unowned**, and users
read unowned as untrustworthy, cheap, and forgettable.

The catalog is organised by category. `scripts/slop_lint.py` catches the mechanical subset; the rest needs eyes.

## Contents

- §1 Color · §2 Typography · §3 Layout & composition · §4 Components & surfaces · §5 Iconography & imagery
- §6 Copy & microcopy · §7 Motion · §8 Over-correction slop · §9 Accessibility as a slop signal · §10 Process slop
- The studio test (the final gate)

---

## §1 Color

| Tell | Why it reads as generated | Do instead |
|---|---|---|
| Purple / violet / indigo → blue or → pink gradient (hero, buttons, badges) | The single most recognisable AI-UI signature; Tailwind indigo lineage | Pick ONE brand hue from the moodboard. Gradients only if the brand is literally about light, energy, or spectrum, and then in OKLCH, subtle, on one surface |
| Gradient text on headlines / big numbers | Reduces scannability; "AI startup" costume | Solid text color; hierarchy via size, weight, spacing |
| Giant blurred glow blobs / radial spotlights / orbs behind hero | Filler for an empty composition | Fill the space with content, product, or nothing |
| Pure `#000` background + neon cyan/violet + glowing borders | The "AI dark mode" | Dark surfaces L≈0.18–0.24 (OKLCH, ≈ #121212–#1e1e1e), elevation via lightness steps, accents desaturated 15–25% |
| Dark mode by reflex | Chosen because "tech"; makes long-form reading worse | Choose light or dark from user context (ambient light, session length, content type) |
| Tailwind default blue/indigo-500/600 as "primary" | Not a decision | Brand token derived from the moodboard |
| Untouched shadcn theme values (`--primary: 222.2 47.4% 11.2%`) | Template detection in one line | Regenerate the full semantic palette from tokens |
| Timid, evenly-distributed palette (5 pastel accents, none dominant) | No hierarchy of attention | 60/30/10: one dominant surface family, one supporting, one sharp accent |
| Cream/beige surface + terracotta accent as "tasteful default" | 2025's over-correction; now a tell itself | Fine only if warmth is a named brand attribute |
| Gray text on colored backgrounds | Washed out, fails contrast | Tinted near-black or near-white text on color |
| Mixed warm and cool neutrals | Looks accidental | Tint every neutral toward the brand hue, consistently |
| Teal `#16d5e6` accent + blinking status dot | Claude Design fingerprint | Remove the dot unless something is literally live |

## §2 Typography

| Tell | Why | Do instead |
|---|---|---|
| Inter / Roboto / Arial / system-ui / Open Sans / Poppins / Montserrat / Lato as the primary face | "I gave up on typography"; the median of the web | Choose from `typography.md` by attribute; native apps may use SF / Roboto **on purpose** |
| Space Grotesk, Geist, Plus Jakarta, Sora, Outfit, Manrope, DM Sans as the "I tried" upgrade | The 2023–2026 startup default tier | Allowed only if the moodboard names the attribute they serve |
| Instrument Serif italic accent word inside an Inter headline | The 2025 formula ("Space Grotesk + Instrument Serif") | One display voice, one text voice; no single-word costume |
| Oversized italic serif display for any product whatsoever | Universal "premium" costume | Serif needs a reason: editorial, heritage, long reading, luxury |
| All-medium weights, single family, flat scale (< 1.2 ratio) | No hierarchy | Ratio ≥ 1.25 between steps; at least two clearly distinct weights |
| Tracked uppercase eyebrow ("FEATURES", "HOW IT WORKS") above every heading | Template rhythm | Delete or replace with a real subhead |
| Letter-spacing on lowercase body; crushed tracking on display beyond −0.04em | Amateur typesetting | 0 on body; −0.01 to −0.03em on display |
| Body < 16px web / < 17pt iOS / < 14sp Android; line-height < 1.4; measure > 80ch | Unreadable | 16–18px, 1.5–1.65, 45–75ch |
| Straight quotes, `...` instead of `…`, hyphens as dashes | Unedited | Real punctuation |
| Monospace for decoration ("hacker vibe") on non-code content | Costume | Mono only where data, code, or measurement lives |
| Full-sentence 64px headline that fills the viewport | Weightless copy | Shorter headline, real supporting sentence |

## §3 Layout & composition

| Tell | Why | Do instead |
|---|---|---|
| Centered hero: pill badge → H1 → subtitle → two buttons → screenshot | The universal skeleton | Compose the first viewport as a poster: brand, one headline, one action, one image, asymmetric if it helps |
| **3-column feature grid**: icon-in-tinted-circle + bold title + two lines, ×3 | THE most recognisable AI layout | Lead with the product itself; explain features in context, with real UI, one per section if needed |
| hero → 3 features → logo strip → testimonials → pricing → FAQ → CTA, all same height | Cookie-cutter section rhythm | Each section has one job and its own scale; vary density and rhythm deliberately |
| Bento grid / 2×2 bento by reflex | 2023 Apple-keynote homage | Only when the content is truly a set of unequal, related facts |
| Stat banner ("10k+ users · 99.9% · 4.9★") with gradient numbers | Weightless proof | Real, specific proof or nothing |
| "1 · 2 · 3" numbered step rows | Template | Show the steps as the product, or as one flow illustration |
| Everything centered (`text-align:center` on all copy) | Reads as "template" | Left-align body and most headings; center only short display moments |
| Everything in a card; cards inside cards ("cardocalypse"); nested containers 3+ deep | Layout by containment instead of by spacing | Whitespace first → 3–5% surface lightness shift → border → shadow, in that order |
| Identical `rounded-2xl` on every element | Bubbly uniform radius | Radius hierarchy: controls < cards < sheets; nested inner = outer − padding |
| Wavy SVG dividers, floating circles, dotted-grid backgrounds | Decoration to hide emptiness | Better content, or honest emptiness |
| Full-width dashboard of KPI cards as an app's first screen | "Dashboard-card mosaic" | Primary workspace first; secondary context beside it; one accent |
| Sidebar + topbar + card grid admin template | Unowned app shell | Navigation shaped by the product's actual object model |

## §4 Components & surfaces

| Tell | Why | Do instead |
|---|---|---|
| Glassmorphism (blur + translucent fill) on ordinary cards | Decoration with no layering purpose | Glass only over real imagery, for navigation layers (as iOS 26 intends) |
| Colored left border on cards / quotes (`border-l-4`) | "The single most reliable AI tell" per several audits | Remove; use type hierarchy or a small mark |
| Colored top border, hairline border + wide diffuse shadow on every card | Shadcn default costume | One elevation system, applied rarely |
| Icon tile above heading; icon in tinted square/circle | SaaS starter look | Inline 20px icons next to text, or none |
| Pill badge "New ✨" / "Now in beta" above headline | Fake urgency | Remove unless the badge links to something |
| Pulsing green "live" dot | Claude Design tell | Only if something is literally live |
| Gradient-filled buttons; buttons with glow shadows | Costume | Solid fill, clear pressed state |
| Dashed borders as decoration; "upload here" dashed box outside upload contexts | Misused affordance | Dashed = drop zone only |
| Skeletons that don't match content shapes; spinners for < 300ms waits | Sloppy loading | Shape-matched skeletons; no indicator under 300ms |
| Auto-scrolling logo marquee | Template motion | Static, honest logo row, or none |
| Toggle switches for non-instant settings; tabs for sequential steps | Wrong affordance | Checkbox + save; stepper |

## §5 Iconography & imagery

| Tell | Why | Do instead |
|---|---|---|
| Emoji as icons, bullets, or heading decoration | Inconsistent across OS, unstylable, screen-reader noise | One icon family, functional only |
| ✨ Sparkles for "AI", 🚀 for "launch", ⚡ for "fast" | 2023–2026 iconography reflex | Name the feature; if an icon is needed, draw the actual concept |
| Default Lucide / Heroicons / Font Awesome everywhere at 24px in tinted circles | Unowned | Pick weight/style to match the typeface; consider custom marks for the 3–5 icons that matter |
| Abstract 3D blobs, "plastic" renders, isometric people-at-desks, floating UI cards in perspective | Stock-AI imagery | Real product screenshots, real photography with a direction, or typographic composition |
| Stock avatars (randomuser, pravatar) in testimonials; "Acme / Globex" logos | Fake proof | Real or none |
| Shape-assembled SVG mascots; hand-coded illustration by an agent | Amateur | Skip illustration until a real illustrator or a real style is available |
| Raster hero under 80% dark wash with white text | Hides a weak image | Choose an image that works, or drop the image |

## §6 Copy & microcopy

| Tell | Do instead |
|---|---|
| Unlock, unleash, elevate, supercharge, empower, streamline, leverage, harness, seamless(ly), effortless(ly), robust, cutting-edge, next-generation, game-changing, revolutionize, transform, skyrocket, future-proof, "in today's fast-paced world", "whether you're a … or a …", "say goodbye to", "Welcome to", "Your all-in-one", "Get started for free", "Trusted by 10,000+ teams", "Made with ❤" | Name a specific outcome per sentence; one adjective maximum; the founder's actual voice |
| "Build faster. Ship smarter." / "Not X. Y." manufactured contrasts | Say the concrete thing |
| Same label used in three slots ("Get started" ×3) | Each action names its result ("Create workspace", "See pricing") |
| Happy talk: "Welcome to our platform where…" | Delete. If deleting 30% improves it, keep deleting |
| Instructions longer than one sentence | Fix the interaction the instruction compensates for |
| "Oops! Something went wrong 😅" | What happened + what to do next, no mascot voice |
| "No items." | Warm, specific empty state with the primary action |
| Em-dash cadence and aphorisms in UI copy | Plain sentences |
| Button: Submit / OK / Continue / Click here | Verb + object: "Save changes", "Send invoice" |

## §7 Motion

| Tell | Do instead |
|---|---|
| Fade-up on every section on scroll (`whileInView` everywhere, AOS) | One orchestrated entrance with staggered delays; then motion only for state change |
| Content invisible at rest (opacity 0 until JS) | Never; progressive enhancement |
| Bounce / elastic easing on UI; hover lift + scale on every card | Standard/decelerate curves; hover changes color or underline |
| `transition: all` | Explicit properties, `transform` and `opacity` only for movement |
| 500ms+ UI transitions; spinners under 300ms | 80–250ms for controls, 300–400ms for sheets |
| Decorative blinking cursor; typewriter headline | Remove |
| Parallax for its own sake | Remove unless it explains spatial relationship |
| Ignoring `prefers-reduced-motion` | Reduce to opacity or nothing |

## §8 Over-correction slop (the anti-default that became a default)

Reacting to the purple-gradient look, a second wave of tells appeared. They are slop for the same reason: chosen for
"not looking AI" rather than for the brand.

| Tell | Legitimate only when |
|---|---|
| Brutalism: black 2px borders, hard shadows, raw system type, hot-pink accents | Counter-cultural, art, architecture, zine, or deliberately provocative positioning |
| "Technical mono" / terminal-core: mono everywhere, `[ ]` brackets, `//` labels, code-brutalism | Developer tooling with real data/code content, and even then mono only for that content |
| Editorial serif costume: Instrument Serif / Editor New italics, big numerals, thin rules, "Vol. 01" | Publishing, heritage, long-form reading, luxury |
| Grain / noise overlays, paper textures | Physical, analog, print-rooted brand story |
| Cream + terracotta + "warm minimal" | Warmth is an explicit attribute and the category isn't already saturated with it |
| Frutiger-Aero / Y2K chrome / lo-fi pixel nostalgia | Youth, gaming, music, or an ironic brand voice |
| Swiss-grid hyper-minimal with 12px labels everywhere | Design-literate audience, information-dense product |
| Neon-brutalist dark ("Warp × Sentry") | Dev tools, and only once |
| **Label/value spec table as the layout device** for most sections of a page ("the ledger site") | Genuine spec content: a technical datasheet, a pricing comparison, a timetable, an app's settings |
| **Register mismatch**: a festival, hotel, fashion or agency page built at the density and scale of a B2B document | Never; pick the register first (`expression-register.md`) |
| **Text-only "honest" page**: serif display, fact table / definition list as the hero, one button, no imagery | A brand that is genuinely typographic (type foundry, publication) and names it as the memorable thing; never for a clinic, café, firm, hotel, shop |
| Dark surface by default on a marketing page | Night-time or screen-native contexts (cinema, music, dev tools) |
| Gray placeholder boxes with "[Photo: …]" captions in a delivered prototype | Never; use real licensed placeholders or designed placeholders mapped to a shot list |
| Serif chosen by reflex for "warm / craft / heritage" | Only after testing a sans and a slab against the same attribute |

Rule: **a style must be traceable to a brand attribute or a content type.** Never stack more than two trend
signals. And a second rule: **the absence of material is also a style choice**, and usually the wrong one; see
`visual-material.md`. Match trend intensity to brand stage (an unknown startup can't carry an "understated" look; a bank can't
carry glitch).

## §9 Accessibility as a slop signal

Generated UI fails accessibility in predictable ways. Treat these as tells too:

- `outline: none` without a `:focus-visible` replacement
- Placeholder as the only label
- Color-only status (red/green with no icon or text)
- Touch targets < 24px (WCAG 2.2) / < 44pt (iOS) / < 48dp (Android)
- Icon-only buttons without `aria-label`
- `user-scalable=no`
- Auto-playing motion with no reduced-motion path
- Visited links indistinguishable from unvisited
- Contrast that "looks fine" but measures 3.8:1 on body text

## §10 Process slop (how it happens upstream)

- **No brief.** Missing fields get filled with defaults. Defaults are slop. → `templates/design-brief.md`
- **No moodboard.** Style chosen by reflex. → `moodboard.md`
- **No research.** Layout chosen by template, not by task. → `mini-user-research.md`
- **Component-first layout.** Assembling a page from a component library instead of composing it. → `spacing-layout.md`
- **One pass.** Generated, not revised. Every professional design is a fourth draft. → `review-checklist.md`
- **Raw values.** `#7c3aed`, `24px`, `Inter` typed inline. → `design-tokens.md`
- **Cloning one reference.** Yields a knock-off. → remix two unrelated references (e.g. Linear's type discipline × a magazine's color)

---

## The studio test (final gate)

Before delivering, answer in writing:

1. Would a respected studio put its name on this? If not, what would they change first?
2. Cover the logo. Can you still tell whose product this is?
3. Name three decisions in this design that no template would have made.
4. Name the brand attribute behind: the typeface, the primary color, the radius, the densest screen, the one motion.
5. Run `python3 scripts/slop_lint.py <path>`. Grade A or B, and every remaining hit annotated "earned because …".

If any answer is missing, the design is not finished.
