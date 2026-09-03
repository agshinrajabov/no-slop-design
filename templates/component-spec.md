# Component Spec — {ComponentName}

> One file per component. Everything here is token-referenced — no raw hex, px, or font names.
> Raw values are allowed **only** in the "Primitive tokens introduced" section, and only if no existing token fits.

## Purpose & usage

- **Job:** {what the component does for the user, one sentence}
- **Use when:** {…}
- **Do not use when:** {… → use {OtherComponent} instead}
- **Platform notes:** {web / iOS / Android differences, if any}

## Anatomy

```
┌───────────────────────────────────────────┐
│ [leading icon]  Label text     [trailing] │  ← slot names
└───────────────────────────────────────────┘
```

| Slot | Required | Content rules |
|---|---|---|
| label | yes | verb-first, sentence case, ≤ 3 words for buttons |
| leadingIcon | no | 20px optical size, currentColor |
| trailing | no | badge / chevron / shortcut hint |

## Variants

| Variant | When | Visual difference (tokens) |
|---|---|---|
| primary | the single main action of a view | `bg: {color.action.primary}` `fg: {color.text.on-action}` |
| secondary | supporting action | `bg: {color.surface.raised}` `border: {color.border.strong}` |
| ghost | tertiary / inline | `bg: transparent` `fg: {color.text.secondary}` |
| destructive | irreversible actions | `bg: {color.status.danger}` — requires confirmation or undo |

## Sizes

| Size | Height | Padding-x | Type | Icon | Min target |
|---|---|---|---|---|---|
| sm | `{size.control.sm}` (32) | `{space.3}` | `{text.sm}` | 16 | 24×24 (WCAG 2.5.8) — pad hit area to 44 on touch |
| md | `{size.control.md}` (40) | `{space.4}` | `{text.base}` | 20 | 44×44 |
| lg | `{size.control.lg}` (48) | `{space.5}` | `{text.md}` | 20 | 48×48 |

## States (all mandatory — a component without them is not finished)

| State | Visual (tokens) | Behavior |
|---|---|---|
| default | | |
| hover (pointer only) | `bg: {color.action.primary-hover}` | 120ms `{ease.standard}` |
| focus-visible | `outline: 2px solid {color.focus}; outline-offset: 2px` | never removed, never color-only |
| active / pressed | `bg: {color.action.primary-pressed}` + 1px translate or 98% scale | |
| disabled | `opacity: {opacity.disabled}` + `cursor: not-allowed` | still readable; still in tab order? {decide} |
| loading | label stays, spinner replaces leading icon, width locked | `aria-busy="true"` |
| selected / checked | | |
| error / invalid | `border: {color.status.danger}` + message below, not only color | `aria-invalid`, `aria-describedby` |
| read-only | | |
| dark mode | list every token that changes | |
| RTL | mirrored icons? {yes/no — directional icons only} | |

## Content guidelines

- Label pattern: {Verb + object — "Save changes", not "Submit"}
- Max length before truncation / wrapping: {…}
- Never: {"Click here", "OK", emoji, ALL CAPS unless brand rule}

## Accessibility

- Role / element: `<button>` (never `<div role="button">` unless unavoidable)
- Name: visible label; icon-only → `aria-label` + tooltip
- Keyboard: Enter/Space activates; Esc cancels (menus/dialogs)
- Contrast: label ≥ 4.5:1 (APCA ≥ 60 for this size), boundary/icon ≥ 3:1
- Motion: respects `prefers-reduced-motion` — {what changes}
- Touch: 44×44pt iOS / 48×48dp Android minimum hit area; 8px between adjacent targets

## Motion

| Trigger | Property | Duration | Easing |
|---|---|---|---|
| hover in | background-color | `{duration.fast}` (120ms) | `{ease.standard}` |
| press | transform | `{duration.instant}` (80ms) | `{ease.standard}` |
| appear (in list) | opacity, transform | `{duration.base}` (200ms) | `{ease.emphasized-decelerate}` |

## Token map (complete)

| Property | Token |
|---|---|
| background | `{color.action.primary}` |
| foreground | `{color.text.on-action}` |
| border-radius | `{radius.control}` |
| font | `{typography.label.md}` |
| shadow | none — buttons don't float |
| gap icon–label | `{space.2}` |

## Primitive tokens introduced (should be empty)

| Token | Value | Why nothing existing works |
|---|---|---|
| | | |

## Examples

```html
<button class="btn btn--primary btn--md">
  <svg aria-hidden="true">…</svg> Save changes
</button>
```

## Open questions

- …
