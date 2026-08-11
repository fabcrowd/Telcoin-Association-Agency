# /brand-image-prompt

Generate a production-ready AI image prompt for a Telcoin Association tweet graphic.

## Usage
Provide the tweet text or topic. This skill outputs a complete prompt formatted for Midjourney, Flux, or DALL-E 3, using the official brand guidelines.

---

## Telcoin Brand Reference (embedded — no file read required)

### Color palette
| Name | Hex | Role |
|---|---|---|
| TEL Black | #090920 | Dark backgrounds (primary canvas) |
| Tel Royal Blue | #3642B2 | Brand anchor, geometric elements, stability |
| TEL Blue | #14C8FF | Highlights, electric accents, key actions |
| TEL White | #F1F4FF | Text on dark, openness |
| TEL Dark Blue | #192E58 | Hero sections, formal backgrounds |
| Tel Indigo Blue | #7393EA | Secondary, accessibility |
| TEL Gray | #424761 | Supporting elements, body text |
| TEL Blue Soft | #C9CFED | Subtle backgrounds |

### Typography
- New Hero Bold — headlines
- New Hero Regular — body text
- Fallback: Inter or Montserrat (same geometric feel, never serif or decorative)

### Brand signature
- Shape: **hexagon** — use as recurring geometric motif in all visuals
- Aesthetic: deep navy/black backgrounds, glowing blue light, glass panels, high contrast
- Tone: institutional infrastructure, not consumer product

### Entity scope — @telcoinTAO
These images represent **Telcoin Association** only.
- In-scope: Telcoin Network (L1 blockchain), TELx (DeFi liquidity layer), governance, GSMA validator model, TAN protocol
- Out-of-scope: Telcoin Wallet commercial imagery, eXYZ stablecoins as consumer products, TDAB banking products

### Safe visual metaphors
- Network nodes and validator infrastructure (MNO data centers, fiber optic, bare-metal servers, antenna towers)
- Mobile devices in real-world emerging-market use — markets, transit, public spaces (not staged ad photography)
- Governance settings: formal chambers, council tables, institutional documents, digital signatures
- Hexagonal geometry — Telcoin's visual DNA; use as overlay, background grid, or foreground element
- Transaction flows as light paths through dark infrastructure
- Abstract consensus architecture: DAG structures, parallel lanes, layered protocol stacks
- Telecom infrastructure: cell towers, fiber cables, satellite uplinks, global data routes

### Unsafe visual metaphors — never use
- Rocket ships, moons, upward arrows, confetti, explosions
- Green candles, price charts, trading screens
- Smiling people holding phones in advertisement-style staging
- Consumer banking checkout flows or mobile wallet UI mockups
- Neon/meme aesthetic, rainbow gradients, cartoon style

---

## What you must do

1. Read the tweet text or topic provided via $ARGUMENTS
2. Cross-reference with `strategy/BRAND-GUIDE.md` if additional brand nuance is needed (optional — reference above covers the essentials)
3. Generate THREE prompt variants:
   - **Variant A**: Dark background (primary) - TEL Black #090920 base with glowing TEL Blue elements
   - **Variant B**: Abstract/conceptual - pure visual metaphor for the tweet topic, no literal depiction
   - **Variant C**: Human-focused - use only when the topic involves financial inclusion, mobile users, or real-world adoption

## Prompt structure (apply to all variants)

Each prompt must include in order:
1. **Subject**: What the image depicts, tied to the tweet topic
2. **Style**: "digital art, institutional brand photography, governance aesthetic, photorealistic render"
3. **Lighting**: "glowing electric blue light, deep shadows, high contrast, volumetric rays"
4. **Geometry**: "hexagonal geometric shapes, crystalline structure, layered glass panels, tessellated grid"
5. **Color palette** (mandatory, exact):
   - Background: deep navy to near-black (#090920 TEL Black)
   - Primary accent: Royal Blue (#3642B2)
   - Highlight: Electric cyan-blue (#14C8FF)
   - Text-safe areas: dark glass panels with subtle translucency
6. **Composition**: "left-aligned layout, rule of thirds, negative space on right for text overlay, generous breathing room"
7. **Aspect ratio**: `--ar 16:9` for tweet header; `--ar 1:1` for tweet card insert
8. **Quality**: `--v 6 --style raw --q 2` (Midjourney) or equivalent quality flags for Flux/DALL-E
9. **Negative prompt**: `--no text, watermark, logo, cartoon, anime, neon, rainbow, busy background, cluttered, stock photo, advertising, smiling models, upward arrows, rockets, confetti, price charts`

## Brand rules for image content

- No text rendered inside the AI-generated image (text is placed in post-production via Figma)
- Never generate images that look promotional or consumer-brand
- Human subjects (Variant C only): diverse, professional, real-world contexts in emerging markets — not staged
- Scale: these are governance and infrastructure images, not product ads

## Output format

Return:

### Variant A — Dark/Glowing (PRIMARY)
```
[full prompt text]
```
**Tool**: Midjourney / Flux / DALL-E 3
**Best for**: Tweet header image, thread opener, governance posts

### Variant B — Abstract/Conceptual
```
[full prompt text]
```
**Best for**: Mid-thread visual break, data point illustration, architecture explainers

### Variant C — Human-Focused (if applicable)
```
[full prompt text]
```
**Best for**: Financial inclusion narrative, LP education posts about real-world use cases

### Post-production notes
- Import into Figma with brand template (dark background, logo top-left, hexagon motif layer)
- Place New Hero Bold for headline over dark glass panel area
- Logo: top-left, horizontal version, 1 mark height from top, 1.5 mark widths from left
- Color-correct to match exact hex values if AI output drifts
- No AI-generated text in the image — set all type in Figma post-production

$ARGUMENTS
