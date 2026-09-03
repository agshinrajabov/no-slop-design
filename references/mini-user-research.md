# Mini User Research

Research that fits in 30–120 minutes and still changes the design. The goal is not academic certainty; it is to
replace *assumptions filled by defaults* with *evidence that forces a decision*. Slop is what happens when the
layout is chosen by template instead of by task. Output goes into `templates/research-synthesis.md`; every insight
must end in a design decision.

## Contents

1. Choosing the time box
2. Method menu (what each costs and yields)
3. Jobs to be done
4. Assumption mapping
5. Proto-personas
6. Competitor & category teardown
7. Review mining and forum listening
8. Heuristic evaluation
9. Lightweight usability testing (5 users, 5-second, first-click)
10. Analytics glance
11. Synthesis: from observations to decisions
12. Research honesty rules

---

## 0. Local + global, always

Every method below runs on two sets: the **audience's market** (the country/region and language from the brief:
its leading products, app-store charts, local competitors, local review sites, local forums) and the **global**
field. Note where local conventions differ (payment methods, ID/verification norms, trust signals, formality of
address, colour and symbol meanings, date/number/currency formats, script and RTL, regulatory notices). Local
conventions are table stakes; global references are where the differentiation ideas come from.

## 1. Choosing the time box

| Situation | Time box | Minimum method set |
|---|---|---|
| Single screen / component change | 30 min | JTBD (1 job) · heuristic pass on the current screen · 3 competitor screenshots |
| New feature in an existing product | 60 min | 3 jobs · assumption map · review mining · 5-screen competitor teardown |
| New product / redesign | 120 min (+ 5-user test later) | all of the above · 2 proto-personas · analytics or support-ticket scan · category map |
| Design system only | 45 min | inventory of existing UI · heuristic pass · platform audit |

If the user provides research (interviews, analytics, personas), read it first and spend the time box on gaps only.

## 2. Method menu

| Method | Time | Yields | Confidence | When to skip |
|---|---|---|---|---|
| Job stories (JTBD) | 10–15 min | the task the UI serves; vocabulary | medium (higher with user quotes) | never |
| Assumption mapping | 10 min | what to test before committing pixels | — (meta) | tiny changes |
| Proto-personas | 15–20 min | context of use, device, frequency, constraints | low–medium; label as assumption-based | when real personas exist |
| Competitor teardown | 20–40 min | table stakes, cliché map, differentiation gaps | medium–high | never for new products |
| App-store / G2 / Reddit review mining | 15–25 min | real pain language, unmet needs | medium–high (biased to extremes) | B2B internal tools with no public reviews |
| Heuristic evaluation | 20–30 min | usability defects in current or competitor UI | high for defects, low for desirability | greenfield with nothing to evaluate |
| 5-second / first-click test | 15 min setup + async | comprehension of hierarchy, findability | medium | when no humans reachable → do a self-test with fresh eyes |
| 5-user usability test | 2–4 h total | ~85% of major problems in a flow | high | before polish, not before structure |
| Analytics / support tickets | 15 min | where users drop, what they ask | high for *where*, low for *why* | no data yet |
| Stakeholder interview (one question each) | 10 min | constraints, success metric, the memorable thing | — | never |

## 3. Jobs to be done

Format (Intercom job story): **When** [situation], **I want to** [motivation], **so I can** [expected outcome].

- Write 3–7. Rank by frequency × importance. The top job defines the primary action of the main screen.
- Situations include emotional and social context ("when my manager is waiting", "when I'm on the train, one-handed").
- Each job implies: an entry point, the minimum information to decide, the action, the confirmation, and the exit.
  Design the flow from that list, not from a page template.
- Ask about *switching*: what did people use before, what pushed them away, what pulled them here, what anxieties and
  habits held them back (the four forces). Anxiety points become the trust moments in the UI.

Output: ranked job list with one line of evidence each (quote, review, ticket, analytics number, or "assumption").

## 4. Assumption mapping (Bland)

1. List every belief the design depends on. One per line. Categories: **desirability** (do users want this, this way),
   **feasibility** (can we build/operate it), **viability** (does it serve the business).
2. Score each 1–5 on **importance** (if wrong, the design fails) and **evidence** (we have proof).
3. High importance + low evidence = **test first**. Pick the cheapest test from §2 or §9.
4. Everything else: proceed, but write the assumption down in the brief's open-questions table.

Typical high-risk UI assumptions: "users understand this label", "users will scroll", "users compare options before
choosing", "this is a one-time task" (vs daily), "users are on desktop", "users have the data ready".

## 5. Proto-personas

Two to four, assumption-based, explicitly labelled. Each on one card:

| Field | Content |
|---|---|
| Name + role | "Nigar, clinic receptionist" |
| Context of use | device, environment, frequency, interruptions, one-handed?, network |
| Goals (top 3 tasks) | verbs |
| Frustrations today | specific, quotable |
| Skills & constraints | tech comfort, language, accessibility needs, time pressure |
| What "good" feels like | one sentence in their words |
| Design implications | density, defaults, error tolerance, tone, target sizes |

Do not invent demographics (age, hobbies, stock photo). They don't drive decisions; context does. Validate later
with "does this sound like you?" on 3–5 real users.

## 6. Competitor & category teardown

Pick 3–5 direct (at least 2 from the audience's market) + 2 adjacent products (adjacent = same job, different category — often where the good ideas are). In Standard mode: 3 first-screens only.
For each, walk the top job end to end and record:

| Field | Note |
|---|---|
| Steps to complete top job | count taps/clicks/screens |
| First-screen composition | what is largest, what is the one action, density |
| Category conventions present | nav pattern, terminology, primary color role, section order |
| Visual clichés (from `anti-slop.md`) | mark them — these are what we will *not* copy |
| Strength to steal as a *principle* | "shows price before signup", not "blue button" |
| Failure to avoid | where reviews complain |
| Fonts / palette / density (for the moodboard) | note, don't judge yet |

Then draw the **category perception map**: two axes that matter to users (e.g. *traditional ↔ progressive*,
*corporate ↔ human*; or *simple ↔ powerful*, *playful ↔ serious*). Plot competitors. The empty quadrant that still
serves the job is the design opportunity; write it as one sentence.

Three-layer synthesis:
- **Table stakes:** conventions every competitor shares → respect (users' mental model).
- **Current discourse:** what is trending → note, usually avoid (it is tomorrow's slop).
- **First principles:** given *these* users and *this* job, where is the convention wrong? If there is a real
  reason, name it: "Every X does Y because they assume Z. Our users [evidence], so we do W."

## 7. Review mining and forum listening

Sources: App Store / Play (filter 1–3★ and 5★ separately), G2/Capterra, Reddit, Product Hunt comments, Trustpilot,
support tickets, community forums, YouTube comments on tutorials, Twitter/X search for "[product] ux".

Procedure: read 50–150 items, tag each with a job and a pain, count. Extract 10–20 verbatim quotes. Look for:
- Words users use for things (steal for labels).
- "I wish", "why can't I", "finally", "confusing", "hidden", "too many".
- Workarounds (spreadsheets, screenshots, notes) — each is a missing feature or a broken flow.
- Trust and anxiety language (pricing surprises, data loss, privacy).

## 8. Heuristic evaluation

Use Nielsen's 10 plus platform rules (`mobile-ios.md`, `mobile-android.md`, `web-frontend.md`). Walk each key
screen and rate every issue: 0 not a problem · 1 cosmetic · 2 minor · 3 major · 4 catastrophic (blocks the job).

| # | Heuristic | Typical findings |
|---|---|---|
| 1 | Visibility of system status | no loading/saving state, silent failures, no progress |
| 2 | Match with the real world | internal jargon, icons without labels, unnatural order |
| 3 | User control and freedom | no undo, no back, modal traps, auto-advancing |
| 4 | Consistency and standards | same action different labels, platform conventions broken |
| 5 | Error prevention | destructive actions one tap away, no constraints on input |
| 6 | Recognition over recall | hidden nav, requiring memory across screens, codes instead of names |
| 7 | Flexibility and efficiency | no shortcuts, no bulk actions, no defaults, no recent items |
| 8 | Aesthetic and minimalist design | competing CTAs, decoration, happy talk, dashboards of everything |
| 9 | Help users recognise and recover from errors | vague errors, no next step, blame |
| 10 | Help and documentation | instructions instead of affordances, help nowhere near the task |

Also run Krug's trunk test on any page: can you tell (1) what site/app, (2) what page, (3) major sections,
(4) local options, (5) where you are, (6) how to search? Six clear = pass.

Three evaluators (or three passes with different personas) find more than one; consolidate and dedupe.

## 9. Lightweight usability testing

- **5-second test:** show the screen for 5 seconds, ask "what is this, what can you do here, what stood out?" Tests
  hierarchy and the memorable thing. 5–10 respondents, async is fine.
- **First-click test:** "where would you click to do X?" Correct first click predicts task success (~87% vs ~46%).
- **5-user moderated test:** 5 users per distinct user group find ~85% of problems (N(1−(1−0.31)^5)). Script: 3–5
  tasks phrased as goals not instructions ("you need to change your delivery address" not "open settings"),
  think-aloud, no helping, note where they hesitate, mis-click, or say "I guess". Run 3 rounds of 5 rather than one of 15.
- **Comprehension test on copy:** paste the headline/error into a message to a colleague: "what does this mean?"
- Without access to humans: do a **cold-read** the next session with the brief hidden, or ask a subagent with only
  the persona card to narrate its first 30 seconds on the screen. Weak evidence, but better than none; label it.

Severity × frequency → fix order. Fix structure before polish.

## 10. Analytics glance

Ten minutes with whatever exists: funnel drop-offs by step, top pages, device split (decides mobile-first or not),
rage clicks / dead clicks, search terms with zero results (missing content or wrong labels), time-on-task outliers,
support-contact reasons. Record numbers with dates; they justify layout priorities.

## 11. Synthesis: from observations to decisions

Fill `templates/research-synthesis.md`. Rules:

1. An observation without a *why it matters* is a note, not an insight.
2. An insight without a *design decision* is not finished.
3. A decision without a *place it shows up* (screen, component, token) will be forgotten.
4. Contradictions between users are segments, not noise; decide which segment the primary flow serves.
5. Write down what is still unknown and the cheapest way to learn it, and before which decision it matters.

Insight → decision examples:

| Insight | Decision |
|---|---|
| Users complete the job one-handed on phones during commutes | primary action in thumb zone; 48px targets; no hover-only affordances; large tap-to-copy |
| Users distrust prices revealed late | price visible on first screen; no "contact us" for standard plans |
| Users describe the object as "orders", team calls it "transactions" | label everything "Orders" |
| Users arrive anxious after an error email | calm palette, no red until needed, first screen states what happened and the one next step |
| Power users do this 40× per day | density mode, keyboard shortcuts, recent items, no confirmation dialogs on reversible actions |

## 12. Research honesty rules

- Say what the evidence is and how strong. "Two reviews mention" ≠ "users want".
- Never fabricate quotes, numbers, personas' opinions, or "studies show".
- Label assumption-based artefacts as such in their title.
- Keep the raw notes (quotes, counts, URLs) in the repo's `design/research/` folder so the next pass can build on them.
- Research that changes nothing was either unnecessary or ignored; state which.
