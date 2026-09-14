# Expression Register

Restraint is not a design philosophy; it is one setting on a dial. A skill that only knows "calm, dense, honest"
produces spec tables for a festival and a stone-cold grid for a fashion label. That is as much a failure as a purple
gradient. **Every project picks a register before composition**, and the register decides how much visual and
motion ambition the page carries, which techniques are on the table, and what "good" looks like at review.

## Contents

1. The four registers
2. Choosing the register
3. R1 Utility
4. R2 Composed (4b: the bold move every register above R1 owes its first viewport)
5. R3 Expressive
6. R4 Experimental
7. Technique catalogue by register
8. Guardrails that never move
9. Mixing registers inside one product
10. Register slop, both directions
11. Checks

---

## 1. The four registers

| | **R1 Utility** | **R2 Composed** | **R3 Expressive** | **R4 Experimental** |
|---|---|---|---|---|
| Job | complete tasks | make a clear case | make an impression that lasts | be an experience people share |
| Typical surface | app UI, dashboards, admin, docs | most marketing sites, B2B, services, e-commerce | brand sites, hospitality, fashion, agencies, launches, culture | festivals, portfolios, campaigns, art, games, product theatre |
| First viewport | workspace or facts | poster: one image, one claim, one action | full-bleed image/video/type, brand at full volume | a scene, a moment, or an interaction that has no equivalent elsewhere |
| Type scale ratio | 1.125–1.2 | 1.25–1.333 | 1.4–1.6, display 72–140px | display 120–400px, type as image |
| Imagery | functional only | one anchor; supporting images only if the content needs them | an art-directed anchor at full scale — photography, film, type as image or illustration, whichever the direction chose | media is the interface: video, 3D, generative, sequenced stills |
| Motion budget | state changes only, 80–250 ms | 1 orchestrated entrance + hover/press | entrance choreography, scroll-linked reveals, 1–2 signature moments | motion is the narrative: scroll-driven scenes, physics, transitions between routes |
| Interaction | standard components | standard + one custom affordance | custom sliders, galleries, sticky sequences, drag | bespoke navigation, cursor states, spatial scenes, sound (opt-in) |
| Build cost | 1× | 1.5× | 3–5× | 8–20× |
| Risk if wrong | boring but works | forgettable | pretty but slow or unclear | unusable, expensive, dated in 18 months |
| Fails as | a wall of rows | a template | a mood board with a button | a demo nobody can use |

Registers are not quality levels. R1 done well beats R4 done badly, always. But choosing R1 for a music festival is
a wrong answer, not a safe one.

**Interaction is a separate axis.** The register sets visual scale, imagery and *decorative* motion. It does not set
how much the visitor can do: that is interaction depth (I1–I4, `interaction-depth.md`), and every Persuade page has
one signature interaction whatever its register. An R2 translation agency with a live price estimator is right; an
R2 agency with none is a brochure.

## 2. Choosing the register

Ask, in the brief, and write the answer down. If the user is unavailable, decide from this table and state it.

| Signal | Pushes toward |
|---|---|
| Task frequency: daily, repeated, professional | R1 |
| Purchase or trust decision made by reading facts (clinic, law, finance, logistics, B2B SaaS) | R2 |
| Purchase decision made by *feeling* (hotel, restaurant, fashion, travel, fitness, beauty, property) | R3 |
| The product *is* culture or spectacle (festival, album, film, game, exhibition, agency portfolio) | R4 |
| Audience is time-poor or in a hurry (support, booking under stress, emergency) | R1–R2 |
| Audience is browsing for pleasure, on a big screen, in the evening | R3–R4 |
| Category is saturated with identical sites and the brief says "stand out" | one register above the category norm |
| Brand is new and unknown, needs credibility fast | R2 (R3 only with real assets: photography, film, or a type or illustration system that can carry the page) |
| Brand is established and known for craft | R3–R4 |
| Budget: one page, two days, no assets | R2, or R3 with licensed photography or a typographic direction |
| Budget: real shoot, motion designer, 3–6 weeks | R3–R4 |
| Low-end Android, 3G, or accessibility-critical audience | cap at R2, or R3 with a static fallback |
| Content is dense data or long text | R1–R2 regardless of taste |

**The category-norm rule.** Look at what the audience's market already does (research phase). If every competitor is
R2, going to R3 is the differentiator with the best cost-to-impact ratio. If competitors are already R3 (hospitality,
fashion), R3 is table stakes and the differentiation must come from art direction, not from ambition alone.

**Say it out loud in the moodboard:** "Register: R3 Expressive, because the decision is emotional, the client has
photography, and all six local competitors sit at R2." One sentence, in the direction block.

**Offer the alternative one step away.** In Standard mode the alternative direction is usually the same idea one
register lower or higher, so the user can trade ambition for cost in a single decision.

## 3. R1 Utility

Read `spacing-layout.md` §8 and `ux-patterns.md`. The whole point is that nothing competes with the work: one
accent, calm surfaces, dense but readable, no decorative motion, no hero. Ambition here shows up as speed, keyboard
support, density modes, and states nobody else designs (empty, partial, offline, bulk, error recovery).

## 4. R2 Composed

The default for services and B2B. Poster-like first viewport with one real image, sections with different rhythm,
one orchestrated entrance, honest proof. Craft shows in typography, spacing, and the details in `components.md` §3.
This is where most of this skill's earlier output landed, and why three industries came out looking alike: R2 was
being applied by reflex. Choose it, don't default to it.

### 4b. The bold move (every register above R1)

Composed does not mean forgettable. A 1.9 run chose R2 correctly and shipped a correct, calm first viewport — a 70 px
headline, a thin route line, a form row — that nobody would remember. R2 limits *how many* loud things a page has,
not whether it has one. **Every Persuade first viewport above R1 carries exactly one bold move**, chosen from the
direction's anchor:

| Bold move | What it looks like | R2 floor | R3–R4 floor |
|---|---|---|---|
| **Type at poster scale** | the claim, the product name or the document itself set so large it is the image | display ≥ 6× body size | ≥ 8× |
| **A drawn graphic** | the diagram, product, illustration or photograph at a size that dominates | ≥ 30% of the 1280×800 viewport | ≥ 45% |
| **A colour field** | a saturated brand colour that owns the viewport, with type on it | ≥ 40% of the viewport, type ≥ 3× | ≥ 60% |

**The phone's first screen owes one too.** At 375×812 the floors are type ≥ 4× body (R3–R4: 4.5×), a graphic ≥ 25%
of the screen (35%), or a colour field ≥ 40% with type ≥ 2.5× (55%). A 1.10 run drew its bold graphic beside the
inputs on desktop and let it fall below them on phones, so the phone's first screen was a heading and two selects.
Reorder for the phone: the move first, or the move made of the type.

**Vary the kind of move across projects.** The bold move becomes a house style as fast as the dark ledger did: a
translation agency and a paediatric clinic in a row both set their interaction's answer (a date, a time) huge on a
saturated field. `shoot.py` names the first viewport's composition — `graphic-hero`, `result-poster`, `type-poster`,
`field-and-heading`, `heading-and-panel` — and `design_log.py` warns when the last two match. Pick the move from the
content: a clinic might own its first viewport with a drawn body map, a hotel with a photograph, a law firm with type.

A dark or near-white band is a surface, not a colour field. A graphic under 64 px on either side is an icon. A route
drawn as a 4 px line across the page is a divider, however meaningful: draw the route as the graphic — thick,
tall, with the stops as objects — or set the price or the date as the type. `scripts/shoot.py` measures all three in
the first viewport and fails the review when none reaches the register's floor. The floor is the minimum; the move
still has to be the direction's idea, not a big word chosen to pass.

## 5. R3 Expressive

**What changes versus R2**

- **Scale.** Display type 72–140 px at desktop; images full-bleed or breaking the grid; sections 100 vh where the
  content earns it. Whitespace becomes a compositional element, not padding.
- **Art direction leads.** The anchor (photograph, film, type as image, illustration) is chosen first; the rest is set around it. Overlap type and image,
  crop hard, let a caption sit in the margin. See `visual-material.md`.
- **Layout devices:** asymmetric grids, editorial columns of unequal width, a sticky left column against a scrolling
  right column, an image that persists while text changes, pull quotes, oversized numerals, a horizontal section
  inside a vertical page, deliberate breakout images.
- **Motion:** one entrance choreography (staggered 20–60 ms), scroll-linked reveals used *once per section at most*,
  a signature moment (a mask reveal, an image sequence, a type transition), page transitions if the site is an SPA.
- **Sound:** off by default, opt-in only, never on scroll.
- **Still ships:** `prefers-reduced-motion` path, keyboard operability, LCP under 2.5 s, real content.

**Cost signals to warn the user about:** photography or film is the budget, not the code. Without real assets, R3
becomes stock-photo theatre, which is worse than a good R2, or than a typographic R3, which needs a typeface and a writer rather than a shoot.

**Study (real sites and studios, as of 2026):** Apple product pages (scroll-driven storytelling at scale), Aesop,
Kinfolk, Ace Hotel, Aman, Six Senses (hospitality R3), Stripe Sessions and Linear launch pages (R2 pushed to R3 with
craft rather than spectacle), Studio Freight / Darkroom, 14islands, Locomotive, Hello Monday, Unseen Studio.

## 6. R4 Experimental

Reach for it when the product is the spectacle and the audience came to be impressed: festivals, album and film
launches, agency portfolios, game marketing, exhibitions, hardware reveals, awards submissions.

**What it adds**

- **Bespoke navigation and layout:** horizontal scroll, spatial canvases, a menu that is a scene, non-rectangular
  compositions, type as the primary image.
- **Real-time graphics:** WebGL / Three.js / React Three Fiber scenes, shaders, particle fields, image displacement,
  physics (matter.js, rapier), procedural or generative visuals tied to data or time.
- **Advanced motion:** GSAP + ScrollTrigger or CSS scroll-driven animations, Lenis-style smoothed scroll (with the
  native-scroll caveat below), FLIP transitions, Rive or Lottie characters, Theatre.js sequencing, view transitions
  between routes, cursor-attached elements, magnetic buttons, canvas image sequences.
- **Audio-reactive or interactive systems** where the brief is music or performance.

**The five conditions.** Do not enter R4 unless all five hold, and say so in the moodboard:

1. The brief or the category demands spectacle (culture, entertainment, portfolio, launch).
2. There is a **narrative**: a first thing, a middle, and a payoff. Effects without a story are a screensaver.
3. Assets exist or can be made (film, 3D, illustration, sound).
4. The audience has the device and the patience; measured, not assumed.
5. A static, accessible, indexable version of the content is part of the plan, not an afterthought.

**Non-negotiables inside R4**

| Rule | Detail |
|---|---|
| Content exists without the effect | server-rendered text and images; the WebGL layer is progressive enhancement |
| Reduced motion | full alternative experience, not a broken one: no scroll-jacking, no auto-sequences |
| Keyboard and screen reader | every route and action reachable; canvas gets a real DOM equivalent |
| Performance | budget stated up front (JS ≤ 300 KB gzip for the core, textures compressed, lazy scenes); LCP ≤ 2.5 s on mid-range mobile; test on a real low-end device |
| Smoothed scroll | only if it never fights native scroll on trackpads and touch; must respect reduced motion; many sites are better without it |
| Loading | designed loader with real progress, not a spinner; first paint shows content, not a logo for 4 s |
| Mobile | a designed mobile version, not the desktop scene shrunk; often a different composition |
| Longevity | note in the handoff what will need maintenance (library versions, GPU changes) |

**Study:** Awwwards Site of the Day archive and Awwwards Annual winners, FWA, Godly (typography-led experimental),
studios Active Theory, Resn, Lusion, Basement Studio, Immersive Garden, Bruno Simon's portfolio (bruno-simon.com),
Igloo Inc, Dogstudio, North Kingdom. Read them for *structure and narrative*, not to copy the effect.

**A note on thematic rationalisations.** "The company tours, so the dates scroll"; "it is a record label, so the
sleeves spin"; "they ship worldwide, so the logos move". A metaphor is not a reason: the test is whether the
technique serves the reader's task, and moving text serves nothing except the impression of movement. Transactional
content (dates, prices, addresses, availability) never moves at rest. If the metaphor is worth expressing, express
it somewhere the reader is not trying to read.

**The R4 failure mode:** an effect reel with no argument. If a visitor cannot say what the thing is and what to do
next within 10 seconds, the register was used as decoration and the page fails Gate 2 no matter how impressive it is.

## 7. Technique catalogue by register

| Technique | R1 | R2 | R3 | R4 |
|---|---|---|---|---|
| Full-bleed imagery | no | hero only | yes | yes |
| Video background / film | no | rarely, muted loop | yes, art-directed | yes, sequenced |
| Display type > 72 px | no | headline only | yes | type as image |
| Overlapping type and image | no | no | yes | yes |
| Asymmetric / broken grid | no | one breakout | yes | the grid is bespoke |
| Horizontal scroll section | no | no | one, with a reason | yes |
| Sticky / pinned sequence | no | one, only to explain a process (`interaction-depth.md` §6) | one per page | multiple, narrative |
| Scroll-linked animation | no | entrance, plus one explanatory sequence | reveals, parallax ≤ 20 % | scroll drives the scene |
| Custom cursor | no | no | subtle state only | yes |
| Signature interaction (`interaction-depth.md` §3) | on Persuade surfaces | required | required | required |
| WebGL / 3D / shaders | no | no | one contained moment | yes |
| Page transitions | no | no | optional | yes |
| Sound | no | no | opt-in | opt-in, designed |
| Auto-scrolling marquee / infinite ticker | no | no | no | no — the one technique that is off-row at every register |
| Spec/definition tables | yes, core | yes, supporting | sparingly, styled | rarely |
| Data density | high | medium | low | very low |

Anything marked "no" is not banned by law; it needs a written reason in the moodboard, and it must not cost the
register's job (a dashboard with a WebGL hero is slower to use).

## 8. Guardrails that never move

Independent of register: WCAG 2.2 AA contrast and focus, keyboard operability, 44/48 px touch targets, real content,
honest proof, `prefers-reduced-motion` respected, no dark patterns, tokens for every visual value, and a page that
still communicates with JavaScript disabled or failed. Ambition is bought with craft, never with accessibility.

## 9. Mixing registers inside one product

A brand site can be R3 while the booking flow is R1, and that is correct: the spectacle sells, the utility serves.
Rules for the seam:

- The transition point is explicit (a route, a modal, a step) and the shared tokens carry across.
- The lower register keeps the brand's type and color, drops the motion and the scale.
- Never mix registers inside one viewport (an R4 hero above an R1 table with no transition reads as two websites).
- Document the map in `DESIGN.md`: which surfaces are which register.

## 10. Register slop, both directions

**Too timid** (this skill's own recent failure mode):

- Spec/definition tables as the primary layout device on every section, in every industry.
- A direction that chose photography, then shipped one small photograph on a 9,000 px page.
- Display type capped at 44 px on a brand site; the page reads as a document.
- A correct R2 first viewport with no bold move: medium headline, a thin diagram, a form row. Nothing wrong, nothing
  remembered (§4b).
- No motion anywhere, described as "restraint", on a surface whose job is to excite.
- The same composition (headline left, facts right) applied to a clinic, a café, a hotel and a festival.

**Too loud:**

- Effects with no narrative; scroll-jacking; four signature moments competing.
- WebGL on a page whose job is a phone number.
- Motion that delays content; 6-second logo loaders.
- Register above the client's asset budget, producing stock-photo theatre.
- Photographs in every section because R3 "has imagery". The register sets the scale of the anchor, not the number of images.
- Trend stacking (grain + mono + brutalist borders + custom cursor) with no attribute behind any of it.

## 11. Checks

- The register is named in the brief and the moodboard, with a one-sentence reason tied to the audience's decision
  type and the category norm.
- The alternative direction sits one register away, priced in effort.
- Above R1, the first viewport has one bold move at or above the register's floor (§4b); `shoot.py` reports it.
- Techniques used are on the register's row in §7, or justified in writing.
- For R3: art direction written, real or licensed photography in the prototype, one signature moment, entrance
  choreography, reduced-motion path.
- For R4: all five conditions answered, the non-negotiable table satisfied, static fallback described, performance
  budget stated, mobile composition designed separately.
- No page uses a label/value table as its main layout device in more than two sections.
- Cover the logo: the page could not be swapped into another industry by changing nouns.
