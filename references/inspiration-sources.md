# Inspiration Sources

Where to look, what each source is good for, and how to use it without importing its biases. Use with
`moodboard.md`. General rule: prefer **shipped** products and **non-UI** sources; treat concept galleries as
entertainment, not evidence.

## Contents

1. Real product UI (shipped)
2. Web design curation
3. Typography
4. Color
5. Non-UI sources
6. Motion
7. Mobile platform references
8. Design systems to study
9. Sources to treat with caution
10. How to search
11. Recording a reference

---

## 1. Real product UI (shipped)

| Source | Best for | How to use |
|---|---|---|
| Mobbin (mobbin.com) | Real iOS/Android/web app flows, screenshots by pattern (onboarding, settings, paywall, empty state) | Search by pattern, not by brand; compare 5 apps' *same* screen; note step counts and states |
| Refero (refero.design) | Real web products by page type and component | Compare density and hierarchy of the same component across products |
| Page Flows (pageflows.com) | Video walkthroughs of real flows incl. loading, error, edge states | Study transitions and the states screenshots miss |
| Screenlane → redirects to Page Flows | — | — |
| UI Sources, Nicelydone, SaaS Interface | Product UI screenshots | Secondary; overlap with Mobbin/Refero |
| App Store / Play Store screenshots | Current competitor UI, positioning copy | Free, always current; read the reviews while there |
| Product Hunt launches | New patterns, current copy clichés | Note what to *avoid* copying |
| Real accounts | The product itself | Sign up; nothing beats using it. Record step counts |

## 2. Web design curation

| Source | Best for | Bias to correct for |
|---|---|---|
| siteinspire (siteinspire.com) | Hand-curated, restrained, often studio/agency/editorial | Skews minimal and European |
| Godly (godly.website) | Typography-led, award-tier, experimental | Skews motion-heavy and portfolio |
| Land-book, SaaSFrame, Saaspo, Lapa Ninja | Shipped marketing pages by industry | The slop skeleton is everywhere here; use for structure *counter*-examples too |
| Awwwards, FWA, CSS Design Awards | Interaction and motion ceiling | Not a usability benchmark; steal one idea, not the approach |
| Httpster, Minimal Gallery, Dark Mode Design | Niche aesthetics | Reference for a direction, not for a default |
| Are.na (are.na) | Building your own reference corpus; other people's curated channels | Slow; the best source for non-obvious connections |
| Web Design Museum, Version Museum | Historical UI, pre-trend patterns | Timeless structures; era styles need a reason |

## 3. Typography

| Source | Best for |
|---|---|
| Fonts In Use (fontsinuse.com) | Real-world usage indexed by typeface, industry, format; the best signal-to-noise for pairings |
| Typewolf (typewolf.com) | Reviewed site typography, font recommendations, "what's trending" (i.e. what to be careful with) |
| Google Fonts, Fontshare, Fontsource, Velvetyne, Collletttivo, Uncut.wtf, The League of Moveable Type | Open-source faces; check axes, language coverage, licence |
| Klim, Grilli Type, Commercial Type, Dinamo, ABC Dinamo, Pangram Pangram, Displaay, Colophon, Sharp Type | Foundry specimens and case studies (paid faces; also the best reading on *why* a face works) |
| Type specimen sites (e.g. foundry "in use" pages) | How a face behaves at scale, in paragraphs, with numerals |
| Practical Typography (practicaltypography.com), The Elements of Typographic Style | Rules and rationale |

## 4. Color

| Source | Best for |
|---|---|
| oklch.com, Huetone, Leonardo (Adobe), Accessible Palette | Building perceptual scales with contrast targets |
| Radix Colors docs | The 12-step semantic scale model |
| APCA contrast calculator (apcacontrast.com) | Lc values by size/weight |
| Real-world material: paint decks (Farrow & Ball, RAL), textile swatches, film stills, ceramics, maps | Palettes with history and temperature; extract in OKLCH |
| Pantone/Coloro trend reports | Know what is trending so you can decide not to |
| Museum collections (Rijksmuseum, Met open access) | Historical palettes with proven harmony |

## 5. Non-UI sources (minimum 30% of any moodboard)

| Domain | What it teaches | Where |
|---|---|---|
| Editorial design (magazines, newspapers) | Hierarchy, rhythm, grids, measure | Magculture, It's Nice That, Fonts In Use editorial section |
| Wayfinding & signage | Legibility at speed, icon systems, contrast | Signage archives, transit maps (Transit Maps blog), airport systems |
| Packaging | Restraint, materials, one-idea composition | The Dieline, Packaging of the World (filter agency work) |
| Architecture & interiors | Proportion, material palettes, light | ArchDaily, Dezeen, The Modern House |
| Product/industrial design | Affordances, tolerances, tactility | Dieter Rams archive, Teenage Engineering, Muji |
| Instrument panels, dashboards (cars, aviation, medical) | Dense information with hierarchy | Manufacturer manuals, aviation HMI standards |
| Cartography | Layering, labels, color as data | David Rumsey Map Collection |
| Film & photography | Color grading, framing, emotional register | Shotdeck, film stills, photographer monographs |
| Games (HUD, menus) | Motion restraint, state feedback, iconography | Game UI Database (gameuidatabase.com), Interface In Game |
| Data visualisation | Encoding, ink ratio | Information is Beautiful Awards, Tufte, Datawrapper blog |

## 6. Motion

| Source | Best for |
|---|---|
| Apple WWDC sessions (design), Material Motion docs | Platform motion systems with reasoning |
| Emil Kowalski's writing/course, Rauno Freiberg (rauno.me, ui.land) | Web interaction craft, easing, timing |
| Game UI Database (motion tags) | State feedback patterns |
| Linear, Vercel, Arc, Family, Things, Notion changelogs | Restrained product motion in the wild |
| Dribbble motion tags | Ceiling only; most are unimplementable |

## 7. Mobile platform references

| Source | Best for |
|---|---|
| Apple Human Interface Guidelines (developer.apple.com/design) + Apple Design Resources (Figma/Sketch kits) | Current iOS/iPadOS/watchOS/visionOS components, Liquid Glass |
| Apple Design Award winners | Native craft benchmarks |
| Material 3 (m3.material.io) + Material Design kit | Components, tokens, motion, M3 Expressive |
| Google Play "Editors' Choice", Android Excellence | Android-native craft benchmarks |
| Mobbin (platform filter) | Real implementations of platform patterns |

## 8. Design systems to study (for structure, not to copy visuals)

Polaris (Shopify), Carbon (IBM), Atlassian, Primer (GitHub), Spectrum (Adobe), Fluent 2 (Microsoft), Lightning
(Salesforce), GOV.UK Design System (content and forms), USWDS, Base Web (Uber), Orbit (Kiwi), Gestalt (Pinterest),
Wise Design, Porsche Design System, Audi UI, Volvo, Nord (Nordhealth), Radix Themes, Ant Design (density),
Chakra/Panda (token architecture), Tailwind Catalyst (component API). Read their token naming, state coverage,
content guidelines, and "when to use" sections.

## 9. Sources to treat with caution

| Source | Why | If you must |
|---|---|---|
| Dribbble, Behance UI concepts | Unshipped, optimised for likes, converge into one look; "the Dribbblisation of design" | Motion or illustration ceiling only; never for layout or flows |
| Pinterest | Recycled, unattributed, algorithmic sameness | Non-UI mood only |
| Template marketplaces (ThemeForest, Framer/Webflow templates, Tailwind UI blocks) | The literal source of the slop skeleton | Study as *anti*-references |
| AI-generated design galleries (v0, Lovable, Claude Design showcases, Stitch outputs) | The distribution mean; whatever looks fresh there is already saturated | Anti-references |
| "Top 10 UI trends 2026" articles | Trends are next year's slop | Know them to avoid stacking them |
| Component library default showcases (shadcn examples, MUI demos) | Default look | Structure and API only |

## 10. How to search

- Search by **pattern and context**, not by adjective: "settings screen banking app" beats "clean UI".
- Search **outside the category** with the attribute: "unhurried" → "slow living magazine layout", "ceramics studio website".
- Search **older**: "2008 newspaper website", "1970s transit signage" — pre-trend structures.
- Use image search on a *material* or *place* from the brand-driver exercise.
- For type: search Fonts In Use by the industry, then by the attribute's adjacent industries.
- Record the URL and date; galleries rot.

## 11. Recording a reference

```
[R07] Source: https://…  (captured 2026-09-03)
Type: editorial / print
Taken: numerals set in the display face at 1/3 column width as the section anchor
Not taken: the paper texture, the justified body
Serves: "Exacting"
Direction: A "Ledger Light"
```

References without a "Taken:" line, or with more than one thing taken, are not references.
