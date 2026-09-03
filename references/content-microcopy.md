# Content and Microcopy

Interface text is part of the design system: it has a voice derived from the brief, tone that flexes by
situation, patterns per UI element, and a banned list. Generated UI fails here in predictable ways (see
`anti-slop.md` §6): hype verbs, "Oops", Submit buttons, fake testimonials, fake urgency. This file gives the
derivation method, Bad to Good tables per pattern, the full banned and watch lists with replacement strategies,
formatting and localization rules, and a review checklist. Component behavior is in `components.md`; error and
form accessibility requirements are in `accessibility.md` §5.

## Contents

1. Voice and tone
2. Principles
3. UI text patterns (Bad to Good)
4. Banned and watch lists
5. Honest content rule
6. Numbers, dates, units
7. Localization readiness
8. Content review checklist
9. Sources

## 1. Voice and tone

Voice is constant (who the product is); tone changes with the user's situation (how it speaks right now). A bank
has one voice and a different tone for "Payment sent" and "Your card was declined".

Derive voice from the brief in three steps:

1. Take the three brand adjectives from the brief (or the moodboard). If the brief has none, pick three from the
   product category and audience and write them into `DESIGN.md`.
2. For each adjective, write a "but not" boundary: *Direct, but not blunt. Warm, but not chatty. Expert, but not
   academic.*
3. Write the "we are not" list (5 items) naming the neighbours you refuse to sound like: *not a startup pitch
   deck, not a chatbot, not a legal notice, not a cheerleader, not a hacker terminal.*

Voice spectrum (set each slider once for the product, then shift tone per situation by at most one notch):

| Dimension | Position (0 to 4) | Same message at two settings |
|---|---|---|
| Formal to casual | e.g. 3 | 1: "Your session has expired. Sign in again to continue." / 3: "You've been signed out. Sign in to pick up where you left off." |
| Serious to funny | e.g. 1 | 1: "No results for 'invoise'. Check the spelling or try a shorter term." / 3: "Nothing for 'invoise'. Typo? Try 'invoice'." |
| Respectful to irreverent | e.g. 0 | 0: "Delete this project? This removes 14 files for everyone on the team." / 3: "Nuke it? 14 files, gone for the whole team." |
| Matter-of-fact to enthusiastic | e.g. 1 | 0: "Export complete. 240 rows saved to orders.csv." / 3: "Done! 240 rows are in orders.csv." |

Tone map by situation (shift from the base setting):

| Situation | Shift | Example |
|---|---|---|
| Error, loss, money, security | More formal, fully serious, matter-of-fact | "Payment failed. Your card was declined by the bank. Try another card or contact your bank." |
| Success after effort | One notch warmer, still specific | "Report published. 32 people on the team can see it now." |
| Empty state, first run | One notch more casual, instructive | "No invoices yet. Create your first one and it will show up here." |
| Legal, consent, permissions | Formal, plain, no persuasion | "Allow location access to show nearby stores. You can change this in Settings." |

## 2. Principles

| Principle | Rule | Bad | Good |
|---|---|---|---|
| Clarity over cleverness | If a joke and a fact compete, the fact wins | "Whoopsie, gremlins ate your upload" | "Upload failed. The file is over 25 MB." |
| Front-load the outcome or verb | First 2 to 3 words carry the meaning; scanning readers stop there | "In order to continue, you will need to verify your email" | "Verify your email to continue" |
| One idea per sentence | <= 25 words per sentence (GOV.UK); split anything with "and" joining two actions | "Enter your address and we'll check delivery options and show pricing" | "Enter your address. We'll show delivery options and prices." |
| Specific numbers only when real | Never round up, never invent | "Trusted by thousands" | "Used by 1,240 teams" (only if the number is supplied) or nothing |
| Sentence case | Buttons, headings, labels, menu items, tabs; capitalise proper nouns only | "Save Your Changes" | "Save changes" |
| Active voice, present tense | The subject acts; the system speaks in "we" when it acts, "you" when the user acts | "Your request has been received and is being processed" | "We received your request. It takes about 2 minutes." |
| No emotional preamble | Delete "we're excited", "we're sorry to see", "great news" | "We're excited to announce dark mode is here!" | "Dark mode is available. Turn it on in Settings > Appearance." |
| Write for scanning | Headings that state the point; lists for 3+ parallel items; bold only for the thing to act on | Paragraph of 80 words explaining three plans | Three labelled rows with price, limit, and one differentiator each |
| Concrete over abstract | Name the object | "Manage your resources" | "Rename, move, or delete folders" |

## 3. UI text patterns (Bad to Good)

### Buttons

Verb + object. The label alone must say what happens. Destructive labels name the thing being destroyed.

| Bad | Good |
|---|---|
| Submit | Create account / Send message / Place order |
| OK / Yes / No | Save / Discard / Keep editing |
| Click here | Download the report (PDF, 2 MB) |
| Learn more | See pricing / Read the setup guide |
| Delete | Delete project |
| Continue (on payment) | Pay 49.00 EUR |
| Get started (as the only CTA) | Start free trial / Create your first invoice |

### Links

| Bad | Good |
|---|---|
| Click here to view the docs | View the API docs |
| More | Show all 12 comments |
| https://example.com/help/2fa | Set up two-factor authentication |
| Read this | Read the refund policy |

Link text is read out of context by screen readers (`accessibility.md`): it must make sense alone, and identical
link text must point to identical destinations.

### Headings

| Bad | Good |
|---|---|
| Welcome to your dashboard | Sales, last 30 days |
| Features | What you can do with webhooks |
| Oops! Something went wrong | Page not found |
| Almost there! | Step 2 of 3: Billing address |

### Labels, placeholders, helper text

| Element | Rule | Bad | Good |
|---|---|---|---|
| Label | Visible, persistent, noun phrase, sentence case, no colon | "Please enter your e-mail address:" | "Email" |
| Placeholder | Optional format hint; never the label; never realistic-looking data | placeholder="john.smith@gmail.com" as the only label | label "Email", placeholder "name@example.com" or none |
| Helper text | Constraint or reason, one sentence, below the field | "Password must contain uppercase, lowercase, number, special character, 8 to 64 chars" | "At least 8 characters. Passphrases work well." |
| Character count | Remaining, updates politely | "Max 160" | "120 characters left" |
| Optional/required | Mark in the label | "*" with no legend | "Phone (optional)" |

### Tooltips

At most one sentence; supplementary only; never the sole place for information a task needs; never on
disabled controls as the only explanation of why. Bad: "Click to configure advanced settings for this item."
Good: "Applies to new orders only."

### Empty states

Formula: what this is + why it is empty + one action.

| Bad | Good |
|---|---|
| No data | No invoices yet. Create one and it will show up here. [Create invoice] |
| Nothing to see here! | No results for "acme corp". Check the spelling or clear the filters. [Clear filters] |
| Your inbox is empty (illustration of a happy mailbox) | Inbox zero. New messages arrive here. |
| Oops, we couldn't find anything | No team members yet. Invite people to start assigning tasks. [Invite] |

### Error messages

Formula: what happened + why (only if it helps) + how to fix it. Never blame ("you entered an invalid"), never
"Oops", never a bare code, never an exclamation mark.

| Bad | Good |
|---|---|
| Oops! Something went wrong. | We couldn't save your changes. Check your connection and try again. |
| Invalid input | Enter a date in the format DD/MM/YYYY. |
| Error 403 | You don't have permission to edit this project. Ask an owner for access. |
| Password incorrect! | The email or password doesn't match our records. Check both, or reset your password. |
| Card declined | Your bank declined the card. Try another card or contact your bank. |
| Upload failed | The file is over 25 MB. Compress it or upload a smaller file. |

Keep the code, if any, at the end in smaller text for support: "Error ref. 5H2K".

### Success and confirmation

State what changed and, if useful, where to see it. No exclamation marks unless the base tone allows one notch.

| Bad | Good |
|---|---|
| Success! | Invoice #1042 sent to ana@acme.com |
| Your changes have been saved successfully | Changes saved |
| Awesome, you're all set! | Account created. Check your email to verify it. |

### Loading

"Saving…" with a real ellipsis character (U+2026), not three periods. Name the operation; for > 10 s add
progress or count: "Uploading 3 of 12". Never "Please wait" alone, never "Hang tight!".

### Destructive confirmation dialogs

Title is the question naming the object. Body states the consequence and scope. Buttons are specific verbs;
the destructive one is on the side the platform expects (`mobile-ios.md`, `mobile-android.md`) and styled as
destructive. No Yes/No, no OK/Cancel.

| Part | Bad | Good |
|---|---|---|
| Title | Are you sure? | Delete "Q3 forecast"? |
| Body | This action cannot be undone. | This removes the file and its 6 comments for everyone on the team. You can't undo this. |
| Buttons | Yes / No | Delete file / Cancel |
| Type-to-confirm (high stakes only) | "Type DELETE" | "Type the project name to confirm" |

### Permission prompts (camera, location, notifications, contacts)

Ask in context, at the moment the feature needs it, with the benefit stated. Use a pre-permission screen in
your own UI first so a denial of the system prompt (which you cannot re-show easily on iOS) is avoided. State how
to change it later.

| Bad | Good |
|---|---|
| System prompt on first launch: "App would like to send you notifications" | After the first order: "Get a notification when your order ships? You can turn this off in Settings." [Notify me] [Not now] |
| "We need your location" | "Show stores near you. We use your location only while the app is open." |

### Notifications and push

Specific, time-bound, actionable, honest. One notification per event. Lead with the fact.

| Bad | Good |
|---|---|
| We miss you! Come back [sad emoji] | (do not send) |
| Don't miss out on amazing deals!! | Your saved item "Field jacket" is 20% off until Sunday. |
| You have a new notification | Ana commented on "Q3 forecast": "Can we move the deadline?" |
| Limited time offer, act now | Annual plan is 20% off until 30 Sept. |

### Onboarding

Three screens maximum, each with one benefit stated as what the user can do, a skip link, and progress. No
"Welcome to X", no feature tour of the whole product. Prefer doing (first task guided inline) over telling.

| Bad | Good |
|---|---|
| Welcome to Ledgerly, the all-in-one finance platform! | Connect a bank account to see your first report in about 2 minutes. |
| Swipe to learn about our amazing features | Skip (link) / Next (button) with 1 of 3 indicator |

### Pricing copy

Every claim verifiable. "Most popular" only with data. Show the full price with billing period and currency;
show what happens at trial end; list limits as numbers, not adjectives.

| Bad | Good |
|---|---|
| Unlimited power for growing teams | 10 projects, 5 members, 50 GB storage |
| From $9 | 12.00 USD per member per month, billed yearly (144.00 USD per year) |
| Most popular (arbitrary) | Remove, or label the plan with the real differentiator: "For teams of 5 to 20" |
| Free trial! | 14-day free trial, no card required. Then 12.00 USD per month. |

### 404 and 500 pages

| Page | Title | Body | Actions |
|---|---|---|---|
| 404 | Page not found | The address may be mistyped or the page moved. | Search box, link to home, link to the section the URL implies |
| 500 | Something broke on our side | We've been notified. Try again in a few minutes. | Retry, status page link, support email, error reference |

No puns, no astronauts, no "lost in space" illustrations unless the base voice is set to funny 3 or above.

### Forms

Labels above fields; required marked in the label; helper text before the error slot; validate on blur;
re-validate on each input after an error; on submit, focus the error summary and list every error with links.
Group long forms into steps with a progress label ("Step 2 of 4: Delivery"). Never clear the form on error.

### Legal and consent

Plain language, short sentences, the choice presented neutrally. Equal visual weight for accept and decline.
No confirmshaming ("No thanks, I don't want to save money"), no pre-ticked marketing boxes, no "By continuing
you agree" hidden below the fold.

| Bad | Good |
|---|---|
| Accept all (primary) / Manage preferences (grey link) | Accept all / Reject all (equal buttons) / Choose what to allow |
| I agree to the Terms and Privacy Policy (pre-checked) | Unchecked box: "I agree to the Terms of Service and Privacy Policy" with both linked |
| No thanks, I like paying full price | No thanks |

### AI feature copy

Describe what the feature does, in the same voice as the rest of the product. No "magic", no sparkle emoji, no
"AI-powered" as a headline, no anthropomorphising ("I think", "I'm sorry", "let me"). Show uncertainty and
provenance honestly; make review and undo obvious.

| Bad | Good |
|---|---|
| [sparkle emoji] AI Magic: Let our AI write it for you! | Draft a reply. You can edit it before sending. |
| I've analysed your data and I believe… | Summary generated from 42 reviews. Check dates and figures before publishing. |
| Powered by advanced AI | Suggestions come from your last 90 days of orders. |
| Ask me anything | Ask a question about this document |
| (no confidence signal) | "Likely a duplicate (matches 3 of 4 fields)" |
| Auto-applied silently | "3 tags suggested" with Apply / Dismiss per tag |

## 4. Banned and watch lists

Banned in UI, marketing, and docs. Each has a replacement strategy; most reduce to "say the concrete thing".

| Banned | Replacement strategy |
|---|---|
| unlock, unleash | Name the capability: "Export to CSV" |
| elevate, supercharge, empower, transform, revolutionize, game-changing | State the measurable change or the action: "Cuts report time from 40 min to 5" (only if true) |
| streamline, leverage, harness, optimize (as vague verb) | Name the mechanism: "Fills in the address from the postcode" |
| seamless, seamlessly, effortless, effortlessly, frictionless | Delete; describe the step count: "Two taps" |
| robust, powerful, world-class, enterprise-grade, best-in-class, cutting-edge, next-generation, state-of-the-art | Delete; give the spec: "99.95% uptime, SOC 2 Type II" |
| skyrocket, future-proof, scalable (in UI) | Delete or give the number |
| delightful, magical, beautiful (about ourselves) | Delete; let the UI be it |
| "in today's fast-paced world", "in the digital age", "now more than ever" | Delete the sentence |
| "whether you're a X or a Y" | Address the reader directly: "You" |
| "say goodbye to X, say hello to Y" | State the change: "No more manual entry: receipts are read automatically" |
| "Welcome to X" (onboarding headline) | Lead with the first action |
| "your all-in-one", "everything you need to", "one platform for" | List the 3 actual things |
| "built for X, designed for Y", "designed with you in mind" | Delete; show it |
| "the future of X is here" | Delete |
| "trusted by 10,000+", "loved by teams everywhere" | Real number with source, or nothing |
| "made with [heart emoji] in Berlin" | Delete or "Company, Berlin" in the footer |
| "get started for free" as the only CTA | Verb + object: "Create your first project" |
| "not just X, it's Y" / "it's not about X, it's about Y" | State Y |
| rule-of-three adjective triplets ("fast, simple, secure") | One specific claim per adjective or delete |
| em-dash aphorisms ("Less noise — more signal.") | One plain sentence |
| "it's important to note", "it's worth mentioning", "note that" | Delete; state the point |
| "picture this", "imagine a world where" | Delete; state the fact |
| "dive in", "deep dive", "let's explore" | "Read", "See", "Open" |
| "Oops", "Uh-oh", "Whoops", "Yikes" | State what happened |
| "Please wait", "Hang tight", "Sit back and relax" | Name the operation with progress |
| "We're excited to", "We're thrilled", "Great news" | Delete the preamble |
| "Simply", "just", "easily" before an instruction | Delete; if it is not simple the word insults, if it is the word is redundant |

Watch list (allowed with care):

| Word | Watch for |
|---|---|
| "free" | Must be true with no card required, or qualify: "Free for 14 days" |
| "instant", "real-time" | Only if < 1 s and < 5 s respectively; otherwise give the time |
| "secure", "private" | Pair with the mechanism: "end-to-end encrypted" |
| "new" badges | Remove after 30 days or first use |
| "recommended", "best value" | Only with a stated reason |
| Exclamation marks | Max one per screen, never in errors or money contexts |
| "Please" | Once per form at most; commands in UI do not need it |

## 5. Honest content rule

Never fabricate metrics, testimonials, customer logos, names, avatars, ratings, review counts, stock levels
("Only 3 left"), countdown timers, "X people are viewing this", awards, or press quotes. Not in mockups, not in
demos, not in "we'll replace it later" placeholders.

Use clearly marked placeholders that cannot be mistaken for content: `[Customer name]`, `[Quote from a real
customer, 20 to 40 words]`, `[Metric: source and date]`, `[Logo: client with written permission]`. Use the
`sr-only`-safe convention of square brackets so a lint (`scripts/slop_lint.py`) can find them. Avatars are
initials on a neutral surface, not stock photos. In the handoff, list every placeholder and what the user must
supply; if nothing real exists, remove the section (a testimonial block with no testimonials is a design
problem, not a copy problem). Scarcity and urgency appear only when generated from live inventory or a real
deadline, and always with the number and end date shown.

## 6. Numbers, dates, units

| Rule | Value | Implementation |
|---|---|---|
| Never hard-code formats | Locale decides separators, order, symbols | `Intl.NumberFormat`, `Intl.DateTimeFormat`, `Intl.RelativeTimeFormat`, `Intl.PluralRules`, `Intl.ListFormat`; iOS `FormatStyle`; Android `java.text`/`android.icu` |
| Thousands and decimals | 1,234.56 (en-US), 1.234,56 (de-DE), 1 234,56 (fr-FR) | `new Intl.NumberFormat(locale).format(n)` |
| Currency | Symbol placement, spacing, and minor units vary; always show the ISO code when the audience is multi-currency | `Intl.NumberFormat(locale, { style: "currency", currency: "EUR" })`; store amounts as integer minor units |
| Tabular figures in tables, timers, prices | `font-variant-numeric: tabular-nums` (see `typography.md`) | Digits align; counts do not jitter |
| Relative vs absolute time | Relative ("2 minutes ago") for < 24 h in feeds; absolute date for anything older or anything legal, financial, or scheduled; hover/tooltip with the full timestamp on relative times | `Intl.RelativeTimeFormat`; `<time datetime="2026-09-03T14:05:00Z">` |
| 12 h vs 24 h | Follow the locale and OS setting, not the market | `hour12` left undefined in `Intl.DateTimeFormat` |
| Date order | Never write ambiguous 03/09/2026; spell the month in prose ("3 Sept 2026") or use ISO 8601 in data | `dateStyle: "medium"` |
| Units | Locale-aware (km/mi, °C/°F, kg/lb); one space between number and unit; SI symbols not pluralised | `Intl.NumberFormat(locale, { style: "unit", unit: "kilometer" })` |
| Large numbers | Compact only in charts and badges ("1.2K"), full in tables and money | `notation: "compact"` |
| Rounding | Display rounding never changes stored values; show the precision the decision needs (money 2 decimals, percentages 0 or 1) | |

## 7. Localization readiness

| Rule | Value | Why |
|---|---|---|
| Budget for expansion | Short strings (up to 10 chars) grow 200 to 300%; 11 to 20 chars 180 to 200%; paragraphs about 130% (W3C, IBM data). German and Finnish are the usual worst case for width, CJK for height (taller glyphs, more line-height) and often 30 to 50% fewer characters | Buttons, tabs, and nav labels break first |
| No concatenated strings | Never `"You have " + n + " items"` or `t("hello") + name` | Word order differs; plural and gender rules differ |
| ICU MessageFormat for plurals and selects | `{count, plural, =0 {No files} one {# file} other {# files}}`; CLDR categories zero/one/two/few/many/other (Arabic uses all six, Russian one/few/many/other) | English two-form plurals do not translate |
| Variables with names | `{userName} shared {fileName}` not `%s shared %s` | Translators reorder |
| No text in images | Text as live text over images, or localized image variants | Cannot translate a PNG |
| No idioms, puns, sports or culture metaphors | "Home run", "hit the ground running", "bells and whistles" | Untranslatable or mistranslated |
| RTL-safe copy and layout | Use logical CSS (`margin-inline-start`, `text-align: start`); avoid directional words ("on the right") in instructions; mirror directional icons (back, next), not universal ones (play, clock) | Arabic, Hebrew, Persian, Urdu |
| Sentence case helps | Title Case has no equivalent in most languages | One less rule to localize |
| Do not truncate | Wrap or reflow; if a limit is unavoidable, set the limit in the source string and tell translators | Truncated translations lose the verb |
| Context for translators | Every string carries a description: where it appears, max length, what variables mean, screenshot | "Book" the verb vs "Book" the noun |
| Dates, numbers, sorting | See §6; sort with `Intl.Collator`, never `localeCompare` defaults or byte order | "ä" sorts differently in de and sv |
| Pseudo-localization in dev | Run a pseudo-locale (`[Ĥéļļö ŵöŕļð one two]`) with 40% expansion before the first real translation | Catches hard-coded and clipped strings early |

## 8. Content review checklist

- [ ] Voice: three adjectives with "but not" boundaries and a "we are not" list exist in `DESIGN.md` and the copy matches them
- [ ] Tone shifts by situation: errors and money are serious and matter-of-fact; no exclamation marks in errors
- [ ] Every button is verb + object; no Submit, OK, Yes/No, Click here, Learn more
- [ ] Every link makes sense out of context; no "here", "more", raw URLs
- [ ] Headings state the point; no "Welcome to", no "Oops"
- [ ] Every field has a visible label; placeholders are format hints only and never realistic data
- [ ] Errors say what happened and how to fix it; no blame, no bare codes, code (if any) last and small
- [ ] Empty states: what it is + why empty + one action
- [ ] Destructive dialogs: title is a question naming the object; buttons are specific verbs
- [ ] Permission prompts appear in context with the benefit and a "Not now"
- [ ] Notifications are specific, time-bound, and free of fake urgency
- [ ] Pricing states full price, period, currency, trial end, and numeric limits; "Most popular" only with data
- [ ] Consent UI gives accept and decline equal weight; no confirmshaming; no pre-ticked boxes
- [ ] AI copy describes function, shows uncertainty, offers review and undo; no sparkle, no "magic", no first person for the model
- [ ] Zero banned-list words (run `scripts/slop_lint.py`); watch-list words each have their qualifier
- [ ] Zero fabricated metrics, quotes, logos, names, avatars, stock counts; every placeholder is `[bracketed]` and listed in the handoff
- [ ] Numbers, dates, currency, units formatted through Intl or platform formatters; tabular figures in tables
- [ ] Sentence case everywhere; active voice; second person; one idea per sentence; sentences <= 25 words
- [ ] Reading-level heuristic: a 12-year-old could act on every instruction; no sentence needs re-reading; Flesch-Kincaid grade <= 8 for UI text, <= 10 for docs
- [ ] "Delete 30%" pass done: every sentence shortened once, every adverb and intensifier ("very", "really", "simply", "just") removed, every preamble cut; the meaning survived

## 9. Sources

- Nielsen Norman Group, The Four Dimensions of Tone of Voice: https://www.nngroup.com/articles/tone-of-voice-dimensions/
- Nielsen Norman Group, Error-Message Guidelines: https://www.nngroup.com/articles/error-message-guidelines/
- Nielsen Norman Group, How to Report Errors in Forms: https://www.nngroup.com/articles/errors-forms-design-guidelines/
- Nielsen Norman Group, Confirmation Dialogs: https://www.nngroup.com/articles/confirmation-dialog/
- Nielsen Norman Group, Empty States: https://www.nngroup.com/articles/empty-state-interface-design/
- GOV.UK Design System, Content style guide and patterns: https://design-system.service.gov.uk/styles/
- GOV.UK, Writing for GOV.UK (sentence length, reading age): https://www.gov.uk/guidance/content-design/writing-for-gov-uk
- Mailchimp Content Style Guide, Voice and Tone: https://styleguide.mailchimp.com/voice-and-tone/
- Material Design 3, Writing (UX writing guidance): https://m3.material.io/foundations/content-design/overview
- Apple Human Interface Guidelines, Writing: https://developer.apple.com/design/human-interface-guidelines/writing
- Apple Human Interface Guidelines, Privacy (permission requests): https://developer.apple.com/design/human-interface-guidelines/privacy
- Android Developers, Notifications design and best practices: https://developer.android.com/design/ui/mobile/guides/home-screen/notifications
- Shopify Polaris, Content guidelines (actionable language, error messages): https://polaris.shopify.com/content
- Google People + AI Guidebook (AI feature copy, explaining uncertainty): https://pair.withgoogle.com/guidebook/
- W3C Internationalization, Text size in translation: https://www.w3.org/International/articles/article-text-size
- W3C Internationalization, Working with composite messages (no concatenation): https://www.w3.org/International/articles/composite-messages/
- Unicode CLDR, Language Plural Rules: https://www.unicode.org/cldr/charts/latest/supplemental/language_plural_rules.html
- ICU MessageFormat: https://unicode-org.github.io/icu/userguide/format_parse/messages/
- MDN, `Intl` namespace: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl
- Deceptive Design (dark patterns catalogue, confirmshaming): https://www.deceptive.design/types
- European Data Protection Board, Guidelines 03/2022 on deceptive design patterns: https://www.edpb.europa.eu/our-work-tools/our-documents/guidelines/guidelines-032022-deceptive-design-patterns-social-media_en
