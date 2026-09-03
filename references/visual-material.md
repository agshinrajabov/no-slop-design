# Visual Material

A page made only of type and tables is not "restrained"; on a marketing surface it is unfinished. The first wave of
slop was decoration without decisions; the over-correction is **decisions without material**: serif headline, fact
table, one button, gray boxes labelled "[photo]". Users read that as a wireframe. This file makes visual material a
requirement, tells you how to choose it per industry and attribute, and how to produce it in a prototype without
fabricating anything.

## Contents

1. The rule
2. Choosing the visual anchor
3. Photography: art direction, not "add a photo"
4. Illustration and graphic devices
5. Product and interface imagery
6. Color fields, texture, and material
7. Generated imagery (when an image tool is available)
8. Placeholders that are still designed
9. Sourcing for prototypes (licences)
10. Video and motion imagery
11. Industry starting points
12. Visual-material slop
13. Checks

---

## 1. The rule

- **Persuade surfaces:** the first viewport contains at least one strong non-text visual anchor (photograph, product,
  illustration, graphic device, color field with a mark, or video). A typographic-only first viewport is allowed only
  when the brand is genuinely typographic (a type foundry, a publication, a law firm whose identity *is* a lettermark)
  **and** the moodboard names that as the memorable thing. Even then, later sections carry imagery.
- **Operate surfaces:** imagery is functional (avatars, thumbnails, charts, maps, product images); no hero art.
- **Read surfaces:** figures, diagrams, and one lead image per article.
- **Prototypes must contain real image elements** (`<img>`, `<picture>`, `<video>`, inline SVG), art-directed and
  sized, never empty boxes with captions. Placeholders are allowed only as described in §8.
- **The moodboard decides the imagery direction** (subject, light, color treatment, crop, people or not) before any
  screen is composed. "Imagery: TBD" is not a direction.

## 2. Choosing the visual anchor

| Anchor type | Choose when | Not when |
|---|---|---|
| Full-bleed photograph with type overlaid or beside | place, people, craft, hospitality, food, health, travel, real estate | product is abstract software with nothing to photograph |
| Split: image half, text half | balanced argument (who we are + what to do) | image is weak; then the split exposes it |
| Product-first (the object, the interface, the packaging) | anything with a physical or on-screen product | early-stage with no real product yet (use illustration or diagram) |
| Color field + brand mark + short claim | strong identity color and a mark; fashion, culture, events | no distinctive mark or color |
| Illustration system | abstract services, finance, education, children, when photography would be generic stock | budget/time for a coherent illustration style is absent (do not hand-code mascots) |
| Diagram / data as image | developer tools, logistics, analytics, science | the diagram is decorative rather than explanatory |
| Collage / editorial composition | culture, publishing, fashion, music | corporate trust contexts |
| Video / motion loop | product demos, hospitality, sport, games | bandwidth-sensitive audiences; must have a poster frame |

Decide by asking: what does this business have that a competitor does not have a photograph of? The room, the
people, the product, the process, the place. Then show that.

## 3. Photography: art direction, not "add a photo"

Write the art direction into the moodboard and DESIGN.md; it drives the shot list and the placeholder choice.

| Dimension | Decide |
|---|---|
| Subject | the actual place / team / product / process / customer moment (name them) |
| People | none · hands only · candid at work · portraits looking at camera (rarely) · never stock-smiling-at-laptop |
| Light | daylight, window light, golden hour, overcast, studio; consistent across the set |
| Color treatment | natural · muted (−15% saturation) · warm/cool grade toward the brand hue · black and white; one treatment for the whole site |
| Crop and framing | tight details vs wide establishing; eye-level vs top-down; leave negative space where type sits |
| Ratios | fixed set: 3:2 hero, 4:5 portrait, 1:1 thumbnail, 16:9 video; token them |
| Texture | film grain or clean; matches the material story |
| What is banned | stock clichés (handshake, lightbulb, rocket, team laughing, doctor with folded arms, gavel and scales), AI-generated people with artefacts, duotone washes over everything, dark overlays hiding weak images |

Provide a **shot list** of 6–12 photographs with subject, framing, and where each is used. This is a real deliverable
the client can hand to a photographer.

## 4. Illustration and graphic devices

- Illustration needs a *system*: line weight, palette (from tokens), perspective, level of abstraction, how people are
  drawn (or not). One illustrator, one style. If none is available, do not hand-code SVG scenes; use a graphic device
  instead.
- **Graphic devices** are cheap and ownable: a recurring geometric mark derived from the logo, a rule/grid motif from
  the industry (timetable lines, ledger rules, map contours), large numerals, a signature crop, a color-block
  system, an editorial frame. One device per brand, used consistently, becomes recognisable.
- Icons are not illustration; a page of icons is not visual material.
- Corporate-Memphis flat people, 3D clay renders, isometric offices, gradient blobs: banned (see `anti-slop.md` §5).

## 5. Product and interface imagery

- Show the real product: screenshots at device-correct sizes with real content, or physical product photographed on
  a surface consistent with the palette.
- No re-drawn browser chrome or hand-built phone frames unless an accurate device frame asset is used.
- Interface screenshots get one consistent treatment (flat on surface, slight perspective never; shadow from
  `shadow.overlay`).

## 6. Color fields, texture, and material

Large fields of brand color, paper/linen/concrete textures, or a material photograph can be the anchor when the
brand story is material (a bakery, a print shop, a fabric brand). Texture must be a decision from the moodboard,
subtle (opacity ≤ 8%), and consistent. Noise-over-everything is over-correction slop.

## 7. Generated imagery (when an image tool is available)

If the session has an image-generation tool (an MCP image generator, Figma image tools, or similar):

1. Generate from the **art direction** in §3, not from the headline: subject, light, treatment, crop, negative space,
   "no people" or "hands only", ratio.
2. Never generate recognisable people as if they were the client's staff or customers. Rooms, objects, materials,
   landscapes, abstract material studies are fine.
3. Match the grade to the tokens (warm/cool) in post: a CSS `filter` or the tool's own color controls.
4. Label generated images as such in the handoff; they are placeholders for a real shoot unless the client accepts them.
5. Generate the full ratio set for the hero (3:2 and 4:5) so mobile art direction works with `<picture>`.

## 8. Placeholders that are still designed

When no image tool exists and no client assets are available:

- Use **real, licensed photographs** matching the art direction from Unsplash / Pexels (see §9), chosen with the same
  care as a final image: correct subject, light, and crop. Add `data-placeholder="shot-03"` and a visible small
  caption only in the review build, not in the design.
- If a real photo cannot match, use a **designed placeholder**: a color field from the palette with the brand mark or
  the graphic device, at the exact ratio, with the shot-list caption. Never a gray box with square-bracket text.
- Every placeholder maps to a shot-list item so the client knows exactly what to shoot.

## 9. Sourcing for prototypes (licences)

| Source | Licence | Notes |
|---|---|---|
| Unsplash | Unsplash License (free, commercial, no attribution required, no resale as-is) | search by subject + light ("dental room window light"); avoid the top results, which are overused |
| Pexels | Pexels License (free, commercial) | good for video loops too |
| Wikimedia Commons | per-file (CC BY / CC0) | check attribution requirements |
| Client assets | theirs | always preferred; ask in discovery |
| Stock (Getty, Stocksy, Death to Stock) | paid | Stocksy/Death to Stock for non-cliché imagery; note the cost in handoff |

Hotlinking Unsplash/Pexels URLs is acceptable in a prototype; download and self-host for anything beyond a review
build. Record the source URL for each image in `design/assets.md`.

## 10. Video and motion imagery

Short loops (6–12 s, muted, `autoplay loop playsinline`, poster frame, `prefers-reduced-motion` → poster only) can
be the anchor for hospitality, sport, product, and food. Keep under 2 MB, `preload="metadata"`, never autoplay with
sound.

## 11. Industry starting points

Starting points for the art direction conversation, not templates; each still needs the moodboard.

| Industry | Have (what to show) | Anchor | Avoid |
|---|---|---|---|
| Dental / clinic | the treatment room, daylight, the team at work, the street entrance | full-bleed room photograph with type; team candids further down | folded-arms doctor, tooth icons, blue gradients |
| Coffee roaster | beans, the roaster, bags/packaging, origin landscapes, pour, steam | product-first packaging on a surface; texture of beans; origin photography | latte art stock, brown-on-brown everywhere |
| Law firm | the people, the building/office, the town, documents as material | portraits with real light + place; architectural detail | gavel, scales, columns, handshake, navy + gold by reflex |
| Restaurant / hotel | food, rooms, light at different hours, staff | full-bleed photography, video loop | stock plates, drone shots only |
| SaaS / developer tool | the product UI, diagrams of how it works, real customer artefacts | product-first screenshot at scale; explanatory diagram | dashboard mockups in perspective, blobs |
| E-commerce fashion | product on body, product flat, detail | large product photography, color fields | busy collages, badges |
| Education | students at work, materials, outcomes | photography of the work itself; illustration system if audience is children | graduation caps, lightbulbs |
| Finance | people in context, real statements/charts, the app | product/interface first, calm photography | gradients, vault icons, generic city skyline |
| Real estate / architecture | the buildings, interiors, plans | full-bleed architecture photography, plans as diagrams | drone-only, HDR |
| Nonprofit | the work, the people served (with consent), the place | documentary photography | sad-eyed stock, hands holding seedling |

## 12. Visual-material slop

- No `<img>` on a marketing page; gray boxes with "[Photo: …]" text.
- A "fact ledger" or definition-list table as the hero on every project regardless of industry.
- Serif display + dark background + one green button as a default "honest" look.
- Stock clichés listed in §3; AI-generated people; hand-coded SVG scenes; icon grids as imagery.
- Duotone/dark overlay on every photo; images cropped without regard to where type sits.
- Placeholder captions shipped in the design; alt text missing or "image".

## 13. Checks

- First viewport of every Persuade page has a designed visual anchor; the prototype contains real image elements.
- Art direction written (subject, people, light, treatment, crop, ratios) and reflected in every image.
- Shot list delivered; every placeholder maps to a shot.
- Images sized with `width`/`height`, `srcset`, `loading` (not lazy on the LCP image), alt per `accessibility.md`.
- Sources recorded; licences compatible with the use.
- Imagery treatment consistent site-wide and matched to the token palette.
- The page does not resemble the previous project in this workspace, and does not default to the serif + ledger look.
