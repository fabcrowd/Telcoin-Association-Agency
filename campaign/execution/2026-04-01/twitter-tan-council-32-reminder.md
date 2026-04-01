# Twitter Post: TAN Council Meeting #32 Reminder
**Account**: @telcoinTAO
**Date**: April 1, 2026
**Tier**: 1 - Governance
**Format**: Single tweet

---

## Marketing Rationale

- **Tier 1 governance format** — no emojis, no enthusiasm language, no conversation prompt; reads as a formal institutional notice consistent with how regulatory or governance bodies communicate publicly
- **Agenda included** — single-meeting reminders benefit from listing agenda items; gives community members enough context to decide whether to observe and what questions to prepare
- **Presenters omitted from tweet** — individual names are in the script, not the public-facing announcement; keeps the post institutional rather than personal
- **EST + UTC** — consistent with prior council posts; UTC serves international community members; EST anchors to the core audience timezone
- **Forum link** — directs to the canonical record; community members can review prior minutes before attending

---

## Tweet Copy

TAN Council Meeting #32 - tomorrow, April 2nd.

5:00 PM EST / 21:00 UTC

Agenda:
- Introduction & Welcome
- Recap of last meeting
- TANIP-1 Fee Rebate Launch
- Remitmap
- TEL Pets
- Open Q&A

Community members may observe via Telcoin Association Discord.

Agenda and minutes: forum.telcoin.org

---

**Character count**: ~250 (under 280 limit)

**Checklist:**
- No emojis
- No contractions
- No enthusiasm language
- No conversation prompt (Tier 1 governance)
- No em dashes (hyphens used throughout)
- EST and UTC times included
- Forum link included
- Discord observation noted
- Institutional tone throughout
- Link placed at end, not at open

---

## Tweet Card Design Brief

**Asset type**: Static image - Tweet card
**Dimensions**: 1200 x 675 px
**Placement**: Attached to tweet above

---

### Purpose

Institutional meeting reminder card for a single TAN Council session. Reads as a formal calendar notice - not a promotional graphic. Design should resemble a structured governance announcement, consistent with prior council schedule cards.

---

### Layout - Figma Spec

**Canvas**
- Width: 1200 px
- Height: 675 px
- Background: TEL Black #090920
- Corner radius: 0 px (full bleed, no card rounding)

---

**Zone 1 - Header (top stripe)**
- Height: 80 px
- Background: TEL Royal Blue #3642B2
- Content, left-aligned with 48 px left padding:
  - Logo: Telcoin Association horizontal lockup (hexagon mark + wordmark) - white version
  - Logo height: 32 px
  - Vertical center within stripe
- Content, right-aligned with 48 px right padding:
  - Label text: "TAN COUNCIL"
  - Font: New Hero Bold (Inter Bold fallback)
  - Size: 11 px
  - Letter spacing: 0.15 em (all caps tracking)
  - Color: TEL White #F1F4FF
  - Opacity: 70%
  - Vertical center within stripe

---

**Zone 2 - Title block (below header)**
- Top padding from header: 40 px
- Left padding: 64 px
- Content:
  - Line 1: "Meeting #32"
    - Font: New Hero Regular (Inter Regular fallback)
    - Size: 14 px
    - Color: TEL Blue #14C8FF
    - Letter spacing: 0.08 em
    - Text transform: uppercase
  - Line 2: "April 2, 2026"
    - Font: New Hero Bold (Inter Bold fallback)
    - Size: 36 px
    - Color: TEL White #F1F4FF
    - Margin top: 6 px
  - Line 3: "5:00 PM EST  /  21:00 UTC"
    - Font: New Hero Regular (Inter Regular fallback)
    - Size: 16 px
    - Color: TEL White #F1F4FF
    - Opacity: 55%
    - Margin top: 8 px

---

**Zone 3 - Agenda list (center body)**
- Top margin from title block: 36 px
- Left padding: 64 px
- Right padding: 64 px

**List structure:**
- 6 rows, one per agenda item
- No outer border
- Row separator: 1 px horizontal line, color TEL Royal Blue #3642B2, opacity 30%
- Row height: 52 px
- Vertical alignment: center

**Row content:**
- Left: agenda item number (01 - 06)
  - Font: New Hero Bold (Inter Bold fallback)
  - Size: 11 px
  - Color: TEL Blue #14C8FF
  - Width: 40 px
- Right of number: agenda item label
  - Font: New Hero Regular (Inter Regular fallback)
  - Size: 15 px
  - Color: TEL White #F1F4FF
  - Opacity: 85%

**Row data:**

| # | Item |
|---|---|
| 01 | Introduction & Welcome |
| 02 | Recap of Last Meeting |
| 03 | TANIP-1 Fee Rebate Launch |
| 04 | Remitmap |
| 05 | TEL Pets |
| 06 | Open Q&A |

---

**Zone 4 - Footer (bottom of canvas)**
- Height: 56 px
- Background: #0D0F1F
- Left-aligned content, 64 px left padding, vertically centered:
  - "Observe via Telcoin Association Discord"
  - Font: New Hero Regular (Inter Regular fallback)
  - Size: 11 px
  - Color: TEL White #F1F4FF
  - Opacity: 45%
- Right-aligned content, 64 px right padding, vertically centered:
  - "forum.telcoin.org"
  - Font: New Hero Regular (Inter Regular fallback)
  - Size: 11 px
  - Color: TEL Blue #14C8FF
  - Opacity: 80%

---

### Visual Accent

- Optional: subtle geometric hexagon motif in lower-right quadrant of Zone 3 background
  - Single large hexagon outline (no fill), opacity 3-5%, color TEL Royal Blue #3642B2
  - Scale: approximately 320 px wide
  - Do not overlap any agenda text
  - Purpose: brand texture only

---

### Typography Summary

| Element | Typeface | Weight | Size | Color |
|---|---|---|---|---|
| Header label | New Hero / Inter | Bold | 11 px | #F1F4FF at 70% |
| Meeting number label | New Hero / Inter | Regular | 14 px | #14C8FF |
| Date | New Hero / Inter | Bold | 36 px | #F1F4FF |
| Time | New Hero / Inter | Regular | 16 px | #F1F4FF at 55% |
| Agenda number | New Hero / Inter | Bold | 11 px | #14C8FF |
| Agenda item | New Hero / Inter | Regular | 15 px | #F1F4FF at 85% |
| Footer text | New Hero / Inter | Regular | 11 px | #F1F4FF at 45% |
| Footer URL | New Hero / Inter | Regular | 11 px | #14C8FF at 80% |

---

### Color Palette Reference

| Token | Hex | Usage |
|---|---|---|
| TEL Black | #090920 | Canvas background |
| TEL Royal Blue | #3642B2 | Header stripe, row dividers, hexagon accent |
| TEL Blue | #14C8FF | Accent labels, agenda numbers, URL |
| TEL White | #F1F4FF | All body text |
| Footer background | #0D0F1F | Footer zone |

---

### Production Notes

- No text inside AI-generated imagery - this card is Figma-native, no AI image required
- All text placed directly in Figma
- Export at 2x (2400 x 1350 px) for retina - compress to under 1 MB for Twitter upload
- No drop shadows, gradients, or glow effects on text - flat typography only
- Hexagon accent (if used) must be a vector shape, not raster
- Logo: use approved horizontal lockup from Figma brand library (white version on dark)

---

## Publishing Notes

- Post date: April 1, 2026 (day before the meeting)
- No scheduling delay required - informational, time-sensitive
- No launch window required for Tier 1 governance posts
- Do not boost or promote as paid post
