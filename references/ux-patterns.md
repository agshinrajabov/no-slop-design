# UX Patterns

Decision rules for choosing interaction patterns by user task. This file covers structure and behaviour, not visual styling: for styling see `components.md`, `color.md`, `typography.md`, `spacing-layout.md`, `motion.md`. Every rule below is falsifiable; when a project has research that contradicts one, the research wins and the deviation is logged in `DESIGN.md`. For copy inside these patterns see `content-microcopy.md`; for platform-specific behaviour see `mobile-ios.md` and `mobile-android.md`.

## Contents

1. How to use
2. Navigation and information architecture
3. Onboarding and activation
4. Forms
5. Data display
6. Search and filtering
7. Feedback and status
8. Settings and preferences
9. Commerce and conversion
10. Authentication
11. Notifications and permissions
12. Collaboration and AI features
13. Mobile-specific notes
14. Dark patterns: refuse list
15. Sources

## 1. How to use

Pick a pattern from the user's task (find, compare, enter, decide, monitor, recover) and the surface mode. Persuade = marketing and landing pages: fewest patterns, one action per screen. Operate = product and app UI: density, keyboard, undo, state persistence. Read = docs and editorial: linear flow, wayfinding, search. Play = immersive or game UI: custom patterns allowed, but system dialogs, purchases and permissions still follow platform rules. When a pattern below says "Operate only", using it in Persuade is a defect.

## 2. Navigation and information architecture

Derive navigation from the object model, not the feature list. List the nouns users already use (orders, patients, projects, invoices), then the 1–3 verbs per noun. Top-level nav items are nouns; verbs live inside the object. Feature names ("Insights Hub", "Smart Tools") fail card sorts because nobody arrives looking for them.

| Pattern | Use when | Avoid when | Details |
|---|---|---|---|
| Top nav (horizontal) | Persuade, Read; ≤7 destinations | Operate with >7 objects or nested workspaces | Labels ≤2 words; current item marked by more than colour (underline, weight) |
| Sidebar | Operate; 6–20 destinations; grouped by object | Marketing sites; mobile widths | Collapsible to icons only if every icon is unambiguous; otherwise collapse to a drawer |
| Tab bar (mobile bottom) | 3–5 primary destinations, equal rank | Destinations >5, or a single-task app | Never hide primary destinations in a hamburger; see `mobile-ios.md`, `mobile-android.md` |
| Command palette (⌘K) | Operate; power users; >30 reachable actions or objects | As the only navigation; Persuade | Fuzzy match on nouns and verbs; show shortcut hints; recent items first |
| Breadcrumbs | Hierarchy depth ≥3; Read and Operate | Flat sites; as a replacement for a back button | Last crumb = current page, not a link; truncate middle crumbs on narrow widths |
| Mega menu | Catalogue with >40 categories and known taxonomy | Anything else | Open on click, not hover; group into ≤4 columns; each column ≤8 items |
| Hub page / dashboard | Multiple objects needing orientation | Single-object apps | Keep it a list of objects with status, not a card mosaic |

Depth rule: global navigation ≤2 levels. Anything deeper is reached through the object (detail page tabs, breadcrumbs, search), not through the menu.

Krug's trunk test. Drop onto any page cold; within 2 seconds you must find: (1) site or product ID, (2) page name, (3) sections and subsections, (4) local navigation, (5) "you are here" indicator, (6) search. A page failing two of six needs an IA fix, not a visual polish.

Wayfinding: the page `<h1>` matches the nav label that led there (same words, same order). Document `<title>` = page name + product name. Current-location signal in every nav level.

Search vs browse: browse when the taxonomy has ≤3 levels and users know the category; search when items >200 or users arrive with a name; both when unsure. Search box placement is covered in section 6.

URL state (web): filters, tabs, sort, page, selected item all live in the URL (`?status=open&sort=-updated&page=3`). Rules: back button restores previous state; refresh preserves state; a copied URL reproduces the view for another user with the same permissions; ephemeral UI (open menus, hover) stays out of the URL. Mobile deep links map to the same object identifiers.

Checks:
- Every top-level nav item is a noun users said in research, or a canonical verb (Search, Settings).
- No destination is more than 2 clicks from any page via nav plus one in-page link.
- Trunk test passes on 3 random deep pages.
- Copying the URL of a filtered table and pasting in a new window reproduces it.
- Mobile primary destinations are visible without opening a menu.

## 3. Onboarding and activation

A product tour is a signal that the UI failed to explain itself. Prefer progressive onboarding: teach at the moment of need, one concept per moment, dismissible, never blocking.

| Pattern | Use when | Avoid when | Details |
|---|---|---|---|
| Empty state as onboarding | Any list, board or canvas that starts empty | Never avoid; every collection view needs one | Explain what will appear, one primary action to create the first item, optional sample data |
| Checklist (3–6 items) | Setup has ordered prerequisites (connect, import, invite) | Consumer apps with one core action | Persist progress; show remaining count; auto-complete items detected from real usage |
| Contextual hint | New affordance at the point of use | >1 hint on screen | One sentence, one target, dismissed by acting or by closing; never a carousel |
| Upfront tour (≥3 steps) | Regulated or safety-critical UI where a mistake is costly | Everything else | Skippable at every step; never repeat after skip |
| Sample or demo data | Value depends on populated views (analytics, CRM) | Data entry apps | Label clearly; one-click clear |

Time-to-first-value target: set a number per product (for example, first chart in <3 minutes, first message sent in <60 seconds) and instrument it. Define the "aha" event as a measurable action, log it, and track median time from sign-up.

Account creation friction: allow use before sign-up where data loss is acceptable (lazy sign-up; prompt at the first save or share). Offer passkeys and one or two social providers that match the audience; do not list six. Ask only what is needed for the first session; defer profile fields.

Permission priming (mobile): explain why in your own UI before triggering the OS prompt; trigger it at the moment of use (camera when the user taps the camera button), never on launch. A denied OS prompt is expensive to recover; a declined in-app primer costs nothing.

Checks:
- Every collection view has a designed empty state with one action.
- No tour on first launch unless a documented reason exists.
- "Aha" event and time-to-first-value are defined and instrumented.
- Sign-up asks ≤3 fields or uses passkey/social.
- OS permission prompts are preceded by in-context explanation.

## 4. Forms

Layout: one column. Labels above fields, left-aligned, always visible (placeholder text is not a label). Group related fields under a heading; 3–7 fields per group. Field width approximates expected input (postal code short, address long). Required is the default; mark optional fields "(optional)" rather than marking required ones with asterisks.

| Decision | Rule | Details |
|---|---|---|
| Single page vs steps | Steps when >7 fields or ≥2 distinct topics (shipping, payment) | One topic per step; show step count "2 of 4"; allow back without data loss |
| Validation timing | Validate on blur; after the first error on a field, re-validate on input | Never validate on keystroke before the user has finished; never validate untouched fields on load |
| Error placement | Inline under the field, plus a summary at the top for ≥2 errors on submit | Summary links to each field; move focus to the summary; keep the field's value |
| Submit button state | Never disabled as a validation strategy | Submit, then show errors; disabled buttons hide why and fail contrast |
| Button placement | Primary action last in reading order, right-aligned in Operate dialogs on web/iOS/Android; left-aligned on full-page GOV.UK-style forms | Destructive actions separated from primary by space or placed in a different region |
| Save and resume | Forms >2 steps or requiring documents | Autosave drafts; show "Saved" timestamp; resume from the same step |
| Smart defaults | Prefill from account, locale, previous entries, geolocation with consent | Default the common case, never the profitable case |

Input specifics:

```html
<input type="email" inputmode="email" autocomplete="email" autocapitalize="off" spellcheck="false">
<input type="tel" inputmode="tel" autocomplete="tel">
<input type="text" inputmode="numeric" pattern="[0-9]*" autocomplete="one-time-code">
<input type="text" inputmode="numeric" autocomplete="cc-number">
<input type="text" autocomplete="postal-code">
```

- Phone: one field, accept any formatting, show country selector only when international is real; format on blur.
- Address: autocomplete first with a manual fallback; country first because it changes the remaining fields; never force a state or province where the country has none.
- Dates: known dates (birthday) as three separate fields or a masked text input, never a calendar picker; near-future dates (booking) as a calendar; always show the expected format.
- Numbers and money: `inputmode="decimal"`; show currency; no spinner arrows.
- Passwords: show/hide toggle, no forced composition rules, minimum length ≥8, allow paste, check against breached lists server-side, offer passkeys before passwords.

Checks:
- One column; labels above; no placeholder-as-label.
- Every field has the correct `type`, `inputmode`, `autocomplete`.
- Errors appear on blur and clear live after correction.
- Submit is never disabled; errors are announced and focused.
- Multi-step forms preserve data on back and on reload.

## 5. Data display

| Pattern | Use when | Avoid when | Details |
|---|---|---|---|
| Table | ≥3 comparable attributes per item, users scan or sort | Items are heterogeneous or mostly images | Text left, numbers right, `font-variant-numeric: tabular-nums`; header sticky; first column sticky when >6 columns |
| List | 1–2 attributes per item, sequential reading | Comparison across attributes | Primary text plus one line of metadata; trailing action or chevron |
| Card grid | Item identity is visual (products, photos, templates) | Tabular data made "friendly" | Uniform card height per row; ≤3 metadata lines |
| Master–detail | Users move between many items and one item's detail | Narrow widths (collapse to list then detail) | Keep list scroll position and selection on return |
| Detail view | One object, all attributes | As a wall of label–value pairs | Header with identity plus status plus primary actions; sections by task; related objects as tables |
| Timeline / activity feed | Chronological events with actors | As the primary work surface | Group by day; collapse repeated events ("3 edits"); relative time under 7 days, absolute after |

Table rules:
- Density modes: comfortable (row 48–56px) and compact (32–40px), user-selectable in Operate, persisted.
- Sorting: one column at a time by default; indicate direction; default sort is the most task-relevant column (usually recency).
- Pagination vs infinite scroll: pagination for tables and anything users return to or share; infinite scroll only for feeds with no destination at the bottom; "Load more" as the middle ground. Page size 25–50 default, selectable.
- Bulk actions: checkbox column; action bar appears on selection with count and "Select all N matching"; destructive bulk action requires confirm (section 7).
- Inline edit: for single-cell corrections in Operate; enter edit on click or Enter, commit on Enter or blur, cancel on Escape; show a save indicator per row.
- Row states: loading (skeleton rows sized like real rows), empty (message plus action within the table body), error (message plus retry inside the table), partial (banner above table stating which source failed).
- Responsive: assign each column a priority (1 = always, 2 = ≥768px, 3 = ≥1024px); hide low-priority columns and expose them in a row expander. Do not convert every table to cards; a 2-column key–value table is still a table.

Dashboards:
- Above the fold answers 1–3 named questions ("Are we on plan this month?"). Write the questions in the spec.
- Each KPI shows value, trend (delta versus a stated period), and comparison (target or previous period). A number without a comparison is decoration.
- Layout: one primary workspace (the chart or table that answers question 1) plus secondary context; no equal-sized card mosaic.
- No decorative sparklines: a sparkline exists only when the trend is the answer.

Chart selection:

| Question | Chart |
|---|---|
| How does it change over time | Line (≤5 series) or area for stacked totals |
| How do categories compare | Horizontal bar, sorted |
| What is the composition | Stacked bar; pie only for 2–3 parts summing to 100% |
| How are two measures related | Scatter |
| How is a value distributed | Histogram or box plot |
| Where is it | Map only if geography is the question |

Checks:
- Numeric columns are right-aligned with tabular figures.
- Table has designed loading, empty, error and partial rows.
- Dashboard spec lists the questions each region answers.
- No chart type chosen for looks; each maps to a question above.
- Column priorities defined for ≤768px.

## 6. Search and filtering

Search box: top of page or top of the list it searches; width ≥240px on desktop, full-width on mobile; visible input, not just an icon, when search is a primary task. Placeholder states scope ("Search orders"). Submit on Enter; show suggestions after 2 characters with a 150–300ms debounce; ≤8 suggestions; arrow keys navigate; Escape clears.

Results page anatomy: query echoed in an editable field; result count; sort control; facets (left rail on desktop, sheet on mobile); results with the matched term highlighted; pagination. Zero results: state what was searched, offer spelling correction, relax filters one at a time with counts ("Remove 'In stock' to see 12 more"), and offer browse categories.

Faceted filters:
- Show counts per option when computable in <200ms; hide options with zero count or disable them.
- Applied filters render as removable chips above results with a "Clear all" when ≥2 applied.
- Apply immediately on desktop; on mobile batch changes behind an "Show N results" button.
- Persist in URL (section 2). Saved views for Operate: name, share, set as default.

Sorting defaults: relevance for text queries; recency for feeds and work items; user's last choice when persisted.

Command palette rules (Operate): opens with ⌘K / Ctrl+K; lists recent and suggested; matches commands and objects; shows shortcut for each command; executes in place; never the only path to an action.

Checks:
- Zero-results state offers at least two recovery paths.
- Applied filters are visible as chips and survive refresh.
- Suggestions are keyboard-navigable.
- Sorting default is documented per view.
- Search scope is stated in the placeholder or label.

## 7. Feedback and status

| Message type | Use when | Avoid when | Details |
|---|---|---|---|
| Inline (next to element) | Field errors, per-row status, validation | System-wide events | Persistent until resolved |
| Toast | Confirm a completed action; offer undo | Errors that need action; anything the user must read | 4–8s; 8s when it carries an action; pause on hover and focus; stack ≤3; bottom-left or bottom-centre on desktop, above the tab bar on mobile |
| Banner (page-level) | Persistent condition: offline, trial ending, degraded service | Success confirmations | Dismissible only if the condition is non-blocking; one banner at a time |
| Dialog (modal) | Irreversible action confirmation; input required to continue | Information the user can read later; success messages | Title states the decision; buttons name the outcome ("Delete 3 files", not "OK") |
| Status page / system banner | Multi-user outage | Single-user errors | Link to status page; timestamp updates |

Confirmation vs undo: reversible actions get undo (toast with Undo for 8s, or an Undo entry in a history), no confirm. Irreversible actions (delete permanently, send, pay, publish to many) get a dialog. Catastrophic and irreversible (delete workspace, drop database) get type-to-confirm with the object name. Never confirm and undo the same action.

Loading ladder:

| Expected wait | Show |
|---|---|
| <300ms | Nothing; changing the cursor or button state is enough |
| 300ms–2s | Skeleton sized like the final content (prevents layout shift); indeterminate spinner only for tiny regions |
| 2–10s | Determinate progress with percentage or step count; allow cancel |
| >10s | Background job: return control, show status in a jobs list, notify on completion |

Optimistic UI: apply for actions that succeed >99% and are cheap to reverse (like, rename, reorder, toggle). Roll back with an inline error and the previous value on failure. Never optimistic for payments, sends or deletes.

Offline and retry: detect and state offline with a banner; queue writes where safe and show "Will sync"; retry reads with exponential backoff (1s, 2s, 4s, cap 30s) and a manual Retry button; never lose typed input.

Error pages: 404 states the page does not exist, offers search and the 3–5 most used destinations, and keeps global nav; 403 says access is missing and how to request it; 500 apologises once, gives a reference ID, a retry, and a status link. All keep the header so the user is not stranded.

Checks:
- No error is delivered only by toast.
- Reversible actions use undo, not confirm.
- Skeletons match final dimensions (CLS check in `web-frontend.md`).
- Waits >10s go to background with notification.
- Error pages keep navigation and give a next step.

## 8. Settings and preferences

Group settings by the object they change, in canonical order: Account (profile, email, password, passkeys, sessions), Preferences (language, region, appearance, accessibility), Notifications (per channel × per event), Privacy and security (data export, visibility, 2FA), Billing (plan, payment method, invoices), Workspace or team (members, roles, integrations), Advanced or developer (API keys, webhooks). Add search within settings when total items >20.

Apply rules: a switch or select applies immediately and shows a brief confirmation inline; a group of text fields uses an explicit Save with a dirty-state indicator and a discard prompt on navigation. Never mix within one group. Destructive zone (delete account, transfer ownership, leave workspace) is last, visually separated, each action individually confirmed.

Checks:
- Every setting is in one of the canonical groups.
- Immediate-apply and save-button groups are not mixed.
- Settings with >20 items have search.
- Destructive actions are last and isolated.

## 9. Commerce and conversion

Pricing page: ≤4 plans; one plan marked recommended only when data shows most buyers pick it; monthly/annual toggle with the annual saving stated as a number; price per unit stated with the unit; a collapsed full comparison table below the cards; FAQ of the real objections (cancellation, tax, seat changes); enterprise contact as text link, not a fourth card with "Custom".

Checkout: guest checkout as the most prominent path (Baymard: 18–19% of US shoppers abandon when account creation is required; 62% of sites still bury guest checkout); account offer after payment. Progress indicator for ≥3 steps; address autocomplete with manual fallback; express pay (Apple Pay, Google Pay, PayPal) above the form when available; order summary visible on every step; errors fixed in place without reloading the form; total including tax and shipping visible before the payment step. Trust signals only when they are real and verifiable (actual security badges, real return policy link); no invented "trusted by" logos.

Cart: editable quantities, remove with undo, saved-for-later, subtotal and estimated shipping, persistent across sessions, no forced sign-in to view.

Product page: images first on mobile; price, availability and the buy action within the first screen; variant selection with disabled-but-visible unavailable options; delivery estimate; reviews with distribution and date; specifications as a table.

Paywall and upgrade moments: show in context at the moment the limit is hit; state what is locked and what the plan gives in one sentence; keep the free path visible; no countdown timers unless the offer really expires; the close control is visible and works on the first tap.

Landing page anatomy without the slop skeleton: hero as a poster (product name or claim, one supporting line, one action, a real product image or the product itself, no stock illustration); proof only when real (named customers with permission, numbers with sources); each subsequent section has one job (explain, show, compare, answer, ask) and a varied rhythm (text-only section, full-bleed image, two-column, table); one closing action. Delete any section you cannot name the job of. Feature grids of 3×2 icon cards, testimonial carousels and logo walls are defaults, not decisions; see `anti-slop.md`.

Checks:
- Guest checkout is the primary path.
- Total cost is visible before payment details are requested.
- Every proof element is verifiable.
- Each landing section has a written job in the spec.
- Paywall close control is visible and functional.

## 10. Authentication

Merge sign-in and sign-up: one screen, "Continue with email" or a passkey or provider button; the system determines whether the account exists and routes accordingly. Passkeys first when the platform supports them; email magic link as the passwordless fallback; password as the last option. Show the identifier on the second step with a change link.

MFA: offer authenticator app and passkeys before SMS; accept codes with or without spaces; `autocomplete="one-time-code"`; remember trusted devices for a stated period; recovery codes shown once with a download and a copy action.

Session expiry: warn 2 minutes before expiry in Operate with an extend action; on expiry, preserve the current form state and return to the same URL after re-auth; never lose unsaved input.

Password reset: request by email; the response is identical whether or not the account exists ("If an account exists for this address, we sent a link"); link expires in ≤1 hour and is single-use; after reset, sign the user in and invalidate other sessions with a notice.

Error messages: do not confirm account existence at sign-in ("Email or password is incorrect"); do help with fixable problems (caps lock detected, this email uses Google sign-in, code expired: request a new one).

Checks:
- One entry screen for sign-in and sign-up.
- Passkey or magic link available; password not the only path.
- Reset flow does not leak account existence.
- Session expiry preserves work.
- OTP fields accept paste and autofill.

## 11. Notifications and permissions

| Channel | Use when | Avoid when |
|---|---|---|
| In-app inbox | Anything the user may act on later; audit trail | Time-critical alerts while the app is closed |
| Push | User-relevant, time-sensitive, actionable (message received, order shipped) | Marketing by default; anything already visible in-app |
| Email | Records (receipts, invoices), digests, security events | Real-time collaboration |
| SMS | Security codes, delivery day-of | Anything else |

Rules: frequency cap per channel (for example, ≤1 marketing push per week, digests for activity >5 per day); granular controls per event type × channel, on by default only for security and direct-address events; quiet hours defaulted to local 22:00–08:00 for non-critical; every notification links to the exact object; batch similar events; prime before the OS permission prompt (section 3) and never re-prompt after denial except from a settings entry the user opens.

Checks:
- Each notification type has a channel, a default state and a cap documented.
- Every notification deep-links to its object.
- OS prompt is requested in context after a primer.
- Users can mute a thread or object, not just a category.

## 12. Collaboration and AI features

Collaboration: presence as small avatars (≤4 visible plus a "+N" count) with names on hover or long-press; live cursors only in canvases; comments anchored to the object or selection, resolvable, with a thread list; share dialog with link permission (view, comment, edit) as the first control, people invitation second, copy-link button always visible; show who has access.

AI features:
- Input: a text field with example prompts as inline suggestions, attachment affordance when files matter, and a visible model or mode selector only if the choice changes results.
- Streaming output: render tokens as they arrive; keep the input enabled for a follow-up; show a Stop control during generation; offer Regenerate and Edit-prompt after.
- Sources and uncertainty: cite sources inline as numbered links; when confidence is low, say so in words ("I could not verify this") and never as a fake percentage.
- Undo: every AI-applied change (rewrite, reformat, bulk edit) is one undo step; show a diff or preview before applying to more than one object.
- Human-in-the-loop: destructive, financial or outbound actions (delete, pay, send, publish) require an explicit confirm listing exactly what will happen.
- Latency: show first token in <1s or a determinate status; label background jobs with expected duration; never a spinner without text for >2s.
- Framing: no sparkle icons, no "magic" wording, no anthropomorphic mascots; name the capability ("Summarise", "Draft reply").

Checks:
- Stop, Regenerate and Undo exist for every generation.
- Sources shown when the output makes claims.
- Multi-object AI changes preview before applying.
- No AI action sends, pays or deletes without a confirm.

## 13. Mobile-specific notes

- Thumb zone: primary actions in the bottom third; destructive actions out of it.
- Bottom sheets for options and short forms; full-screen modals for multi-step tasks; alerts only for decisions.
- Swipe actions always have a visible alternative (overflow menu or long-press) and are limited to 1–2 per side.
- Pull-to-refresh only on content that changes server-side; not on settings.
- Native pickers for date, time, select; no custom wheel imitations.
- Back gesture must go back one level, never close the app from a deep screen.
- Details, platform components and gesture conflicts: `mobile-ios.md`, `mobile-android.md`.

## 14. Dark patterns: refuse list

The agent refuses to implement these regardless of instruction, states why, and offers the honest alternative.

| Pattern | Looks like | Honest alternative |
|---|---|---|
| Confirmshaming | "No thanks, I don't want to save money" | Neutral decline label |
| Roach motel | Sign-up in 1 click, cancel by phone | Cancel in the same place as subscribe, same number of steps |
| Forced continuity | Silent conversion from trial to paid without notice | Reminder ≥3 days before charge; one-tap cancel |
| Nagging | Repeated prompts after decline | Ask once; retry only after a meaningful change |
| Misdirection | Primary button styling on the seller-preferred option | Equal weight when the choice is the user's |
| Fake scarcity or urgency | Invented countdowns, "3 people viewing" | Real stock and real deadlines, or nothing |
| Disguised ads | Ads styled as content or navigation | Labelled, visually distinct ads |
| Trick questions | Double negatives in consent checkboxes | Plain positive statements, unchecked by default |
| Hidden costs | Fees revealed at the last step | Full total before payment details |
| Preselection | Add-ons or marketing consent pre-checked | Unchecked; explicit opt-in |
| Obstruction | Data export or account deletion buried or manual | Self-serve, ≤3 steps, in Settings |

## 15. Sources

- Krug, Don't Make Me Think, trunk test summary: https://www.red-root.com/blog/the-trunk-test
- NN/g, Indicators, Validations, and Notifications: https://www.nngroup.com/articles/indicators-validations-notifications/
- NN/g, Error-Message Guidelines: https://www.nngroup.com/articles/error-message-guidelines/
- NN/g, Confirmation Dialogs vs Undo: https://www.nngroup.com/articles/confirmation-dialog/
- NN/g, Progressive Onboarding and Product Tours: https://www.nngroup.com/articles/onboarding-tutorials/
- Baymard, Checkout UX Best Practices 2025: https://baymard.com/blog/current-state-of-checkout-ux
- Baymard, Cart Abandonment Rate Statistics: https://baymard.com/lists/cart-abandonment-rate
- GOV.UK Design System, Buttons (disabled buttons, alignment): https://design-system.service.gov.uk/components/button/
- GOV.UK Design System, Error summary: https://design-system.service.gov.uk/components/error-summary/
- GOV.UK Design System, Question pages (one thing per page): https://design-system.service.gov.uk/patterns/question-pages/
- GOV.UK, Dates pattern: https://design-system.service.gov.uk/patterns/dates/
- Material Design 3, Snackbar: https://m3.material.io/components/snackbar/guidelines
- Material Design 3, Navigation bar: https://m3.material.io/components/navigation-bar/guidelines
- Apple HIG, Tab bars: https://developer.apple.com/design/human-interface-guidelines/tab-bars
- Apple HIG, Onboarding: https://developer.apple.com/design/human-interface-guidelines/onboarding
- Apple HIG, Privacy (permission requests): https://developer.apple.com/design/human-interface-guidelines/privacy
- MDN, autocomplete attribute values: https://developer.mozilla.org/en-US/docs/Web/HTML/Attributes/autocomplete
- MDN, inputmode: https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/inputmode
- W3C WAI, Forms tutorial (validation, error placement): https://www.w3.org/WAI/tutorials/forms/
- Adam Silver, The problem with toast messages: https://adamsilver.io/blog/the-problem-with-toast-messages-and-what-to-do-instead/
- Deceptive Design pattern catalogue (Brignull): https://www.deceptive.design/types
- FIDO Alliance, Passkeys UX guidelines: https://fidoalliance.org/ux-guidelines/
