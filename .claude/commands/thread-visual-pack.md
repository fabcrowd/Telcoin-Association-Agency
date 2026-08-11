# /thread-visual-pack

Generate a coordinated set of visual briefs for an entire tweet thread — header card, supporting inserts, and a visual system that reads as a coherent series.

## Usage
Provide the thread file path or paste the thread content via $ARGUMENTS. This skill produces a complete visual pack: one header card brief + briefs for 2-3 supporting insert cards + AI image prompts for each.

---

## Telcoin Brand Reference (embedded — no file read required)

### Color palette
| Name | Hex | Role |
|---|---|---|
| TEL Black | #090920 | Dark canvas (primary) |
| Tel Royal Blue | #3642B2 | Brand anchor, geometric elements |
| TEL Blue | #14C8FF | Highlights, electric accents |
| TEL White | #F1F4FF | Primary text on dark |
| TEL Dark Blue | #192E58 | Hero sections, gradient base |
| Tel Indigo Blue | #7393EA | Secondary, soft accents |
| TEL Gray | #424761 | Supporting elements, subtle text |
| TEL Blue Soft | #C9CFED | Secondary body text |

### Typography
- **New Hero Bold** — headlines, card titles
- **New Hero Regular** — body text, labels, card numbers
- Fallback: Inter or Montserrat. Never serif or decorative.

### Brand signature
- **Hexagon** is the recurring geometric motif — must appear consistently across all cards in a thread
- Logo appears on Card 1 (header) only — omit from insert cards
- Glass panel behind all text — TEL Black at 85-90% opacity for legibility
- Card numbering: subtle "1/N", "2/N" in lower-right corner using TEL Gray #424761, New Hero Regular 16px

### Content tier visual direction — Telcoin thread types
| Thread type | Tier | Visual style | Hex grid? | Logo on inserts? |
|---|---|---|---|---|
| Governance notice or recap | 1 | Type-only or dark minimal — no decorative illustration | No | No |
| LP2 platform architecture explainer | 2 | Abstract network diagram, infrastructure render, layered architecture | Yes (8%) | No |
| LP3 differentiation thread | 2 | Comparative diagrams, abstract concept renders | Yes (8%) | No |
| Milestone / Adiri launch | 3 | Bold announcement visual, high contrast, controlled energy | Light (12%) | No |
| Community roundup | 4 | Warmer — human element allowed, slightly less formal | No | No |

### Safe and unsafe visual metaphors
**Safe**: MNO data centers, fiber optic infrastructure, hexagonal node networks, governance documents, mobile devices in emerging-market contexts (not staged), DAG consensus layers, parallel transaction lanes, telecom towers, formal institutional settings.

**Never use**: Rocket ships, moons, upward arrows, confetti, smiling models, price charts, green candles, consumer checkout flows, eXYZ stablecoin product mockups.

### Entity scope — @telcoinTAO
Threads represent **Telcoin Association** only.
- In-scope: Telcoin Network, TELx, TAN, governance, GSMA model
- Never depict Holdings products as the subject: Telcoin Wallet commercial UI, eXYZ consumer flows, TDAB

---

## What you must do

1. Read the thread content from $ARGUMENTS (file path or pasted text)
2. Analyze the thread structure:
   - Identify the opening tweet (always gets a header card, 1200 x 675px)
   - Identify 2-3 tweets that benefit from a supporting visual (data points, architecture claims, key stats, comparisons)
   - Identify the content tier using the table above
3. Define a **visual system** — a single consistent look that ties all cards together
4. Generate individual design briefs for each card
5. Generate AI image prompts for cards requiring generated visuals (use `/brand-image-prompt` approach)
6. Cross-reference `strategy/BRAND-GUIDE.md` if additional brand nuance needed (optional — reference above covers essentials)

---

## Output format

## Thread Visual Pack

**Thread**: [title or first tweet excerpt, max 12 words]
**Content tier**: [1 / 2 / 3 / 4 — with label]
**Thread type**: [LP2 architecture explainer / Governance recap / Milestone announcement / etc.]
**Total cards**: [N]
**Visual theme**: [1-sentence description of the visual system tying all cards together]

---

### Visual System Definition

The visual system ensures all cards in the thread read as a series.

| Element | System-wide spec |
|---|---|
| Background | [e.g., TEL Black #090920 consistent across all cards] |
| Background texture | [e.g., hexagonal grid overlay at 8% opacity Royal Blue — or "none" for Tier 1] |
| Accent color | [e.g., TEL Blue #14C8FF as consistent highlight] |
| Geometric motif | [e.g., hexagonal node cluster — lower-right on header, lower-left on inserts, 25% opacity] |
| Glass panel | TEL Black #090920 at 88% opacity behind all text blocks |
| Typography | New Hero Bold for headlines, New Hero Regular for body — consistent sizing |
| Logo | Card 1 header only — top-left, 1 mark height from top, 1.5 mark widths from left |
| Card numbering | Lower-right corner, TEL Gray #424761, New Hero Regular 16px, format "2/5" |
| Accent line | 2px TEL Blue #14C8FF on left edge — consistent across all cards |

---

### Card 1 — Header (Tweet 1)

**Tweet**: [quoted text]
**Purpose**: Set the visual identity of the thread; signal institutional quality; hook the reader

**Canvas**: 1200 x 675px (16:9)
**Background**: [spec — e.g., dark gradient #192E58 → #090920]
**Headline on card**: [max 8 words — extracted or condensed from tweet, no hype language]
**Label**: [optional — e.g., "Platform Architecture" / "TELx Governance" / "Telcoin Network"]
**Visual element**: [description or "type-only card"]
**AI image prompt**:
```
[full Midjourney/Flux prompt — follows brand-image-prompt structure: subject, style, lighting, geometry, colors, composition, aspect ratio, quality flags, negative prompt]
```

---

### Card 2 — Insert (Tweet [N])

**Tweet**: [quoted text]
**Purpose**: [why this tweet gets a visual — e.g., "visualize the 4-miner governance structure" / "illustrate the parallel fee lane architecture" / "show the 3-layer platform stack"]

**Canvas**: 1080 x 1080px (1:1)
**Background**: [must match visual system]
**Headline on card**: [if any — max 6 words]
**Visual element**: [description]
**AI image prompt** (if generated visual):
```
[full prompt, or "N/A — use diagram template"]
```
**Diagram spec** (if a structured diagram is better than AI generation):
> [Describe the diagram precisely: shapes, sizes, colors, labels, layout. E.g., "3-column stack diagram: bottom row 'Telcoin Network (L1)', middle row 'TELx (DeFi)', top row 'TAN (Applications)'. Each row: full-width rectangle, 120px height, left border 4px TEL Blue #14C8FF, background Royal Blue #3642B2 at 20% opacity, label New Hero Bold 24px TEL White, left-aligned with 20px padding."]

---

### Card 3 — Insert (Tweet [N])

[same format as Card 2]

---

### Card 4 — Insert (Tweet [N]) [if applicable]

[same format as Card 2]

---

### Production checklist

- [ ] All cards use the same background color/gradient
- [ ] All cards use New Hero font (or documented fallback)
- [ ] Hexagonal motif present and consistent across all cards
- [ ] Logo only on Card 1 header
- [ ] Card numbers in lower-right, consistent position and size
- [ ] No text rendered inside AI-generated images (all type set in Figma)
- [ ] All hex values match brand palette exactly
- [ ] No promotional language in any on-card copy
- [ ] All cards pass the institutional test: appropriate in a regulatory newsletter
- [ ] Tier 1: type-only, no decorative elements, no emojis
- [ ] Entity check: no Holdings products depicted (Wallet checkout, eXYZ consumer flows, TDAB)

### Figma workflow
1. Start with brand template (TEL Black background, hexagon motif layer, logo top-left)
2. Generate AI visuals using prompts above
3. Import AI visual as background layer; reduce opacity to 40-60% if too busy
4. Add glass panel overlay (TEL Black #090920 at 88% opacity) behind all text
5. Place copy in New Hero — never use AI-generated text
6. Add card number, accent line, logo (header only)
7. Export at 2x resolution: 2400x1350px for headers, 2160x2160px for inserts

---

$ARGUMENTS
