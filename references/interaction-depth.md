# Interaction Depth

The expression register decides how loud a page *looks*. It must not decide whether the page lets the visitor *do*
anything. A translation agency is rightly R2 in its visuals and still needs a price estimator; a clinic is R2 and
still needs a slot picker. A page that answers the visitor's question only in prose sells less than one that answers
it with a result they produced themselves. This file defines a second axis, independent of the register, and one
rule: **every Persuade page ships one signature interaction that performs the visitor's top job.**

## Contents

1. The two axes
2. The four depths
3. The rule: one signature interaction (3b: it does not replace the direction)
4. Choosing the depth
5. Catalogue by category
6. Motion with a job: explanatory sequences
7. Build guardrails
8. Interaction slop
9. Checks

---

## 1. The two axes

| Axis | Decides | Chosen from |
|---|---|---|
| **Expression register** (R1–R4, `expression-register.md`) | visual ambition: scale, imagery, decorative motion | the decision type, the category norm, the asset budget |
| **Interaction depth** (I1–I4, this file) | how much the visitor can do and see respond | the top job, and whether its answer depends on the visitor's inputs |

They combine freely. R1 + I2 is a tool. **R2 + I3 is a service with a live demo — often the strongest choice for
services.** R3 + I2 is a hotel with an availability picker. R4 + I4 is a festival scene. The register caps
decoration; it never caps the signature interaction.

## 2. The four depths

| | **I1 Static** | **I2 Functional** | **I3 Demonstrative** | **I4 Immersive** |
|---|---|---|---|---|
| The visitor | reads, follows links, submits a form | filters, sorts, calculates, picks, checks availability | experiences the value itself before committing | explores a space or system that responds continuously |
| Examples | a brochure page | store locator, slot picker, table filter | estimator with a live price and date, before/after slider, a sample that pairs lines on hover, sandbox demo, configurator with preview | WebGL product viewer, spatial festival map, audio-reactive scene |
| JS budget | 0 | ≤ 10 KB | ≤ 30 KB, no framework needed | stated up front, lazy-loaded |
| No-JS fallback | — | the static table or list | a static result: the table, the final state | a complete static page |
| Registers | any | any | R1–R3 | R3–R4 |

## 3. The rule: one signature interaction

Every Persuade page (landing, marketing, pricing, service) has **one** signature interaction, chosen from the first
job story in the brief. It is:

- **job-performing** — it answers the question the visitor arrived with (what does it cost, when is it ready, is it
  free on my dates, will it fit, what will it look like) with a result they can see;
- **close** — within the first three sections and reachable from the first viewport (a button or link jumps to it),
  a result in ≤ 2 steps. In the first viewport itself **only when the market's language is `product` or `tight`**
  (a developer tool, documentation, a utility: the tool is what the category opens on). Everywhere else the first
  screen belongs to what the market opens on — the photograph, the collection, the room, the name — and the
  interaction is section 2 or 3. Four different businesses in a row put it directly under the hero, and the 1.22 test
  put it in the first viewport of seven pages out of ten, whatever the market showed;
- **in the page's language** — its form follows the design language the market set (`design-language.md` §5): a
  playground in a developer tool, a live search in documentation, the scene itself in an immersive launch, a picker
  beside the photograph in a hospitality page, a raw calculator in a brutalist one. A panel of form controls beside a
  heading is one form, not the form;
- **connected** — its result carries into the next action: it prefills the form, the WhatsApp message, the booking;
- **honest** — estimates say "estimate", assumptions are visible, fees are not hidden, nothing asks for sign-up
  before showing the result;
- **not the whole design** — the interaction answers the question; the direction's anchor still carries the page. A
  form panel beside a heading is not a composition, and a page where the estimator is the only idea reads as a
  booking tool. See §3b.

### 3b. The interaction does not replace the direction

The 1.7 run of a translation brief fixed everything the review asked for — the result stayed on screen on phones,
the prices used the market's locale — and lost what the 1.6 run had: a bold colour field and a drawn route of the
document's working days. What remained was a dark panel of form controls, a large heading, an empty half of the
first viewport, and two data tables for the rest of the page. Fixing the interaction is not permission to drop the
expression.

- **The anchor is executed at full weight in the first viewport.** "Type as image" means type that *is* the
  image — set at a scale, crop or arrangement a heading would never get, occupying a real share of the viewport —
  not a large `h1` beside a form. A colour field fills its field. A diagram is drawn.
- **The result is designed, not printed.** Give the result a visual form that explains it: the route of working
  days drawn as a timeline, the document redrawn in both languages, the price as a composed figure. A sticky bar
  on phones is the minimum, not the design.
- **No dead half.** An empty column next to the interaction is a composition failure unless the emptiness is the
  stated idea.
- **One table.** Beyond the no-JS fallback or a price list, the page's other sections use other devices: a sequence,
  a worked example, a diagram (`slop_lint.py` flags `tables-as-sections`).
- **The result's form comes from the content, and varies.** Record it as `--result-form` in `design_log.py`:

  | Form | Fits when the answer is… | Example |
  |---|---|---|
  | `figure` | one number or time that matters most | "Bu gün 16:40" |
  | `diagram` | a change in a thing the visitor can picture | windows lighting up, a body region taped, seals redrawn |
  | `calendar` | dates or slots | free nights shaded on a month |
  | `map` | a place or a route | the walk from the tram stop |
  | `card` / `list` / `table` | a comparison of options | three plans priced for 8 people |
  | `media` | what it will look like | before/after, a room photo per choice |
  | `paper` | a document the business really hands over | a quote the client signs |

  A paper artefact (receipt, solicitor's letter, calendar leaf, ticket) answered three different businesses in a
  row. Use it only when the business actually hands that paper over, and never twice running; the log warns.
- **The page does not end on a contact form by habit.** End on this business's next real step: a map and hours for
  a shop, a booking for a hotel, a phone number for an urgent service, the order for a bakery.
- **The interaction does not dictate the page's order.** The signature interaction is one region, not a page
  template. Six runs in a row built the same skeleton around it — interaction → steps → price table → form — for a
  translation agency and two clinics. Where the interaction sits (first viewport, directly after it, or as the page's
  spine) and what follows it come from the content: a hotel's rooms, a restaurant's menu, a clinic's doctors. The
  history log compares skeletons (`shoot.py` "skeleton" line).
- **A rerun is compared with the run before it.** Put the previous screenshots beside the new ones; a fix that loses
  the previous version's expression is a regression, whatever the gate grades say.

Operate surfaces are already interactions. Read surfaces rarely need one beyond search or a tracking table of
contents. Say which applies in the brief.

**Not a signature interaction:** a language switcher, a carousel, hover effects, tabs that only hide copy, an FAQ
accordion, a chatbot bubble, a newsletter field.

## 4. Choosing the depth

| Signal | Depth |
|---|---|
| The price depends on inputs (pages, size, dates, options) | I3 estimator |
| Availability decides the purchase (rooms, slots, seats, tables) | I2–I3 availability picker |
| The result is visual and hard to imagine (renovation, retouching, colour, fit) | I3 before/after or configurator |
| The product is software | I3 live demo or sandbox — not a video of one |
| Trust depends on process quality (translation, legal, medical, logistics) | I3 sample that proves the process, plus one explanatory sequence (§6) |
| Audience in a hurry, low-end devices, poor connections | I2, with no dependency on animation |
| Content-only brand (publication, archive) | I1–I2 |

## 5. Catalogue by category

Starting points, not templates. Each still goes through the brief's top job.

| Category | Top job | Signature interaction | Result carries into |
|---|---|---|---|
| Translation, legal documents | what it costs, when it is ready | estimator: document type, pages, language pair, urgency, notary/apostille → price and ready date | prefilled quote form or WhatsApp message |
| Clinic, dental, beauty | when can I come, roughly how much | service + day → open slots with a price range | booking |
| Hotel, rental | is it free on my dates, total cost | dates + guests → available rooms with the full total | booking engine |
| Restaurant | a table tonight, what I can eat | party size + time → free slots; menu filtered by diet | reservation |
| Removals, courier, logistics | price for my move or parcel | from–to + size → price and date | booking |
| Renovation, architecture, interiors | what it will look like, rough cost | before/after slider; room-size cost estimate | consultation request |
| SaaS, developer tools | does it do my thing | live sandbox on sample data | sign-up that keeps the demo state |
| E-commerce, D2C | will it fit or look right | configurator or size finder with live preview | cart with the configuration |
| Finance, loans, insurance | what will I pay | calculator with editable, visible assumptions | prefilled application |
| Education, courses | which level, what I will learn | 3–5 question level check → a recommended course | enrolment |
| Fitness, studios | which class, when | schedule filter by class and time | trial booking |
| Events, festivals | who plays when, my plan | lineup filter, schedule builder, saved picks | tickets for the chosen days |
| Recruitment | is there a role for me | role and salary explorer | application |
| Food, coffee, wine | which one will I like | 2–4 question taste finder | cart |
| B2B services | is it worth it | ROI or savings calculator with editable assumptions | sales call with the numbers attached |
| Nonprofit | what my money does | amount → a concrete outcome | donation |

## 6. Motion with a job: explanatory sequences

A pinned or scroll-linked sequence is allowed at **any** register when it explains a process the visitor has to
trust — how a document is translated and certified, how a parcel moves, how a treatment proceeds. Bounds:

- one section, at most four states, each readable when the scroll stops;
- scroll position drives state; scroll speed is never taken over;
- `prefers-reduced-motion` → the states shown as a static sequence;
- no JavaScript → the final state, with the steps as text;
- the register still caps *decorative* motion everywhere else.

## 7. Build guardrails

| Rule | Detail |
|---|---|
| Declare it | `data-nsd-interaction="estimator"` (or the type) on the root element, so review and `slop_lint.py` can find it |
| Native controls first | `select`, `input type=number/range/date`, radio, checkbox before any custom widget |
| Results are announced | `<output>` or `aria-live="polite"` on the result |
| Keyboard | every control reachable and operable; visible focus; order follows the reading order |
| Reduced motion | state changes without transforms or parallax |
| No JavaScript | the static equivalent is on the page: the price table, the final state, the form |
| Budget | per §2; no library for I2–I3 unless the project already uses one |
| Numbers | `Intl` formatting in the **market's** locale, not the page language (az-AZ writes `80,00 ₼`, not `AZN 80.00`); dates in working days; assumptions shown; the word "estimate" |
| A real answer | when the top job is "what does it cost / when is it ready", the result shows a number and a date. Without the client's rates, use **sample rates labelled as samples** on the page and list the real ones as an open item — never `[n]`, `—` or "after we see the document" as the whole answer. Reframing the question (which seals, which steps) is welcome as long as price and date still answer. `slop_lint.py` flags `placeholder-result` |
| Honest deltas | when an option changes nothing (express cannot move a date the apostille decides), say so beside the result; never let a label promise what the result does not show |
| Mobile | the result stays visible while the visitor changes inputs: a sticky result bar, a bottom sheet, or the result above the inputs. Verify at 375 px by changing the main input — the new result is on screen without scrolling. A dock that appears only after the result has scrolled past does not count when the inputs come first: it is hidden exactly while the visitor is editing. Targets ≥ 44 px |
| Handoff | name the analytics events: started, result shown, carried into conversion |

## 8. Interaction slop

**Too little:** a brochure page for a business whose price or availability *is* the question; "contact us for a
quote" as the only path; a language switch counted as the interaction; an FAQ accordion as the only thing that moves.

**Wrong or too much:** a chatbot bubble on load; carousels; hover effects on everything; a multi-step quiz wall
before any information; fake live counters ("12 people are viewing this"); estimates that hide fees; results behind
sign-up; scroll-jacking; custom cursors on service sites; three competing interactions where one would do.

**Interaction as the whole design:** the estimator panel is the only visual idea; the anchor shrank to a heading;
half the first viewport is empty; the sections after it are data tables (§3b).

## 9. Checks

- The brief names the top job, the interaction depth with a reason, and the signature interaction.
- The signature interaction answers the top job with a visible result in ≤ 2 steps, in or right after the first
  viewport, and its result carries into the conversion.
- Keyboard, announced result, reduced motion and the no-JS fallback are verified, not assumed.
- At 375 px, changing the main input shows the new result without scrolling:
  `scripts/shoot.py index.html --set "#main-input=value"` measures it and saves the frame.
- The anchor is visible at full weight in the first viewport, the result has a designed form, and no more than one
  data table appears outside the interaction (§3b).
- `data-nsd-interaction` is on the page; `slop_lint.py` reports no `no-signature-interaction`.
- Nothing from §8 is on the page.
