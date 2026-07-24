# /tweet-card-brief

Generate a complete design brief for a single Telcoin Association tweet card graphic.

## Usage
Provide the tweet text (or topic + tier). This skill outputs a Figma-ready design brief that a designer (human or AI) can execute directly.

---

## Telcoin Brand Reference (embedded — no file read required)

### Color palette
| Name | Hex | Role |
|---|---|---|
| TEL Black | #090920 | Dark canvas (primary background) |
| Tel Royal Blue | #3642B2 | Brand anchor, geometric elements |
| TEL Blue | #14C8FF | Highlights, accents, key actions |
| TEL White | #F1F4FF | Primary text on dark |
| TEL Dark Blue | #192E58 | Hero sections, formal backgrounds |
| Tel Indigo Blue | #7393EA | Secondary, soft accents |
| TEL Gray | #424761 | Body text, supporting elements |
| TEL Blue Soft | #C9CFED | Subtle secondary text |

### Gradients
- **Dark gradient** (gravitas): `#192E58 → #090920` (diagonal)
- **Light gradient** (clarity): `#7393EA → #3642B2 → #26195E` (use sparingly, Tier 3/4 only)

### Typography
- **New Hero Bold** — headlines (48-56px at 1200px canvas width)
- **New Hero Regular** — body, labels (24-28px)
- Fallback: Inter or Montserrat. Never serif or decorative.

### Brand signature
- Hexagon is the recurring geometric motif — always present as background overlay, corner accent, or foreground cluster
- Logo: horizontal version, top-left, 1 mark height from top edge, 1.5 mark widths from left edge
- Glass panel: dark overlay (TEL Black at 85-90% opacity) behind text — ensures legibility over any visual

### Content tiers — Telcoin examples
| Tier | Type | Examples | Visual style |
|---|---|---|---|
| 1 | Governance | Council meeting notices, snapshot votes, TIP/TELIP proposals | Type-only or minimal — no decorative elements; dark card, white text |
| 2 | Education | LP2 platform architecture posts, LP3 differentiation, explainer threads | Diagram, abstract concept visual, architecture illustration |
| 3 | Milestone | Adiri testnet launch, mainnet announcement, MNO validator onboarding, exchange listing | Bold, high contrast, controlled — proud but not flashy |
| 4 | Community | Weekly governance roundup, participation invites, third-party wins | Warmer — human element allowed; slightly less formal |

### Entity scope
Cards are for **@telcoinTAO** — Telcoin Association only.
- Safe: Telcoin Network, TELx, TAN, governance, GSMA validator model
- Requires confirmation before use: Telcoin Wallet commercial metrics, eXYZ stablecoin products, TDAB

---

## What you must do

1. Read the tweet text provided via $ARGUMENTS
2. Determine the content tier (see table above)
3. Cross-reference `strategy/BRAND-GUIDE.md` if additional nuance needed (optional — reference above covers essentials)
4. Output the complete design brief in the format below

---

## Output format

## Tweet Card Design Brief

**Tweet text**: [quoted text from input]
**Content tier**: [1 / 2 / 3 / 4 — with label]
**Card type**: [Header 16:9 / Mid-thread insert 1:1 / Standalone 16:9]
**Dimensions**: 1200 x 675px (16:9) OR 1080 x 1080px (1:1)

---

### Canvas

| Element | Spec |
|---|---|
| Background | [TEL Black #090920 / dark gradient #192E58→#090920 / light for Tier 4] |
| Background texture | [none / subtle hexagonal grid overlay at 8% opacity TEL Royal Blue / AI-generated visual at 40% opacity] |
| Card style | [solid / glass panel overlay / gradient overlay] |

### Typography

| Element | Font | Weight | Size | Color | Alignment |
|---|---|---|---|---|---|
| Headline | New Hero | Bold | 48-56px | TEL White #F1F4FF | Left-aligned |
| Body (if any) | New Hero | Regular | 24-28px | TEL Blue Soft #C9CFED | Left-aligned |
| Label/Tag | New Hero | Regular | 18px | TEL Blue #14C8FF | Left-aligned |

### Copy on card
> **Headline**: [max 8 words, extracted or condensed from tweet — no hype language]
> **Supporting text**: [optional — max 1 short sentence, factual]
> **Label**: [optional — e.g., "Governance Update" / "Platform Architecture — LP2" / "TELx" / "Telcoin Network"]

### Brand elements

| Element | Placement | Spec |
|---|---|---|
| Horizontal logo | Top-left | 1 mark height from top; 1.5 mark widths from left |
| Hexagon motif | Background-right or corner cluster | 20-30% opacity, Royal Blue #3642B2, outline only (no fill) |
| Accent line | Bottom edge or left edge | 2px solid, TEL Blue #14C8FF |
| Glass panel | Behind text block | TEL Black #090920 at 88% opacity, slight blur |

### Visual element
> [One of: "type-only card — no visual element (Tier 1)" / "abstract hexagonal node network, glowing TEL Blue, top-right quadrant" / "Figma diagram — see Diagram Spec below" / "AI-generated visual — use /brand-image-prompt [topic]"]

### Diagram spec (if applicable — Tier 2 explainer cards)
> [Describe any structured diagram: e.g., "4-node square arrangement showing Validators, Developers, Liquidity Miners, Stakers. Each node: hexagon shape, 60px, Royal Blue fill, TEL Blue border, label in New Hero Regular 18px TEL White. Lines connecting all four nodes, 1px TEL Blue, 40% opacity."]

### Color usage

| Area | Color | Hex |
|---|---|---|
| Canvas background | TEL Black | #090920 |
| Primary text | TEL White | #F1F4FF |
| Secondary text | TEL Blue Soft | #C9CFED |
| Accent / highlight | TEL Blue | #14C8FF |
| Geometric elements | Tel Royal Blue | #3642B2 |

### Compliance checks
- [ ] No hype language or promotional tone in any on-card copy
- [ ] Logo present, correctly placed (top-left, correct spacing)
- [ ] Font is New Hero (or documented fallback)
- [ ] All hex values match brand palette exactly
- [ ] Tier 1: no emojis, no decorative elements, type-focused only
- [ ] No busy background that interferes with text legibility
- [ ] Text passes contrast ratio (4.5:1 minimum on dark background)
- [ ] No AI-generated text in the visual — all type set in Figma
- [ ] Entity check: no Holdings products depicted (Telcoin Wallet checkout flows, eXYZ consumer products)

### If AI-generated visual is needed
> Run `/brand-image-prompt [topic]` to generate the visual element. Composite in Figma as background layer at 40-60% opacity behind the glass panel.

---

$ARGUMENTS
