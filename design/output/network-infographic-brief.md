# Telcoin Network — Architecture Infographic Brief
## Platform: X/Twitter | Format: 16:9 Landscape | Last updated: March 12, 2026

---

## 1. INFOGRAPHIC LAYOUT BLUEPRINT

### Canvas Overview
**Dimensions**: 1920 x 1080px (16:9)
**Background**: Deep navy gradient — #0A0E1A (near-black) to #0D1526 (dark navy), subtle grain texture to prevent flat digital look
**Grid**: Three horizontal zones stacked; internal padding 72px all edges

---

### Zone 1 — Header Bar (top 14% of canvas, ~152px tall)
**Position**: Full width, flush top
**Content**:
- LEFT: Telcoin Association wordmark / logomark (white, ~48px tall) — placed 72px from left edge
- CENTER: Main headline (see Section 2)
- RIGHT: Chain ID badge — small pill/tag element: "Chain ID: 2017" | "TEL Gas Token" — two stacked pills, white text on #0047FF fill, right-aligned, 72px from right edge
**Divider**: Single 1px horizontal rule in #0047FF at 14% mark, full width, 30% opacity

---

### Zone 2 — Main Architecture Diagram (middle 62% of canvas, ~669px tall)
This is the centrepiece. It renders the two-layer blockchain architecture as a visual stack diagram, flowing left to right.

#### Left Column — "HOW IT'S BUILT" (25% canvas width)
A vertical stack of two clearly labeled layers rendered as stacked rectangular panels with subtle depth/shadow:

**Panel 1 (top) — Consensus Layer**
- Background: #0047FF at 15% opacity with #0047FF border (1.5px)
- Label: "CONSENSUS LAYER" in all-caps, white, 11px tracking
- Icon: DAG graph node cluster — small abstract node-and-edge diagram (3–4 nodes, edges between them, glowing blue nodes)
- Detail text: "Narwhal + Bullshark" (prominent, white, ~18px) | "DAG-based consensus" (secondary, #8BA3C9, 13px) | "Adapted from Mysten Labs / Sui" (tertiary, #8BA3C9, 11px)
- Stack arrow between panels: downward chevron in #0047FF

**Panel 2 (bottom) — Execution Layer**
- Background: #1A2744 with white border (1px, 40% opacity)
- Label: "EXECUTION LAYER" in all-caps, white, 11px tracking
- Icon: Ethereum diamond / EVM hexagonal icon in white outline
- Detail text: "EVM-Compatible" (prominent, white, ~18px) | "Ethereum-standard blocks" (secondary, #8BA3C9, 13px) | "Rust codebase — 99.4%" (tertiary, gold #C9A227, 11px)

#### Center Column — "HOW IT CONNECTS" (50% canvas width)
**Flow diagram**: Shows transaction lifecycle with connecting arrows between layers and out to validators
- Horizontal flow: Transaction → Consensus Layer (orders/confirms) → Execution Layer (processes/executes) → Block finalized
- Each step rendered as a labeled node connected by animated-looking horizontal arrows (dotted lines with chevron ends in #0047FF)
- Communication stack badge (bottom of center): "libp2p · QUIC-v1 · UDP · BLS Keys" — rendered as a subtle dark pill tag row, monospace font, 10px

**Central section label** (top of center column, small caps): "TRANSACTION FLOW"

#### Right Column — "WHO VALIDATES" (25% canvas width)
**Title**: "VALIDATORS" in all-caps, white, 11px tracking

**Visual**: A vertical list of 4–5 abstract MNO validator nodes, each rendered as a small rectangle with a signal tower icon (simplified — two bars and an arc), labeled "MNO Validator" in grey. One node is highlighted in #0047FF to represent an active validator producing a block.

**Key requirement badge** (below node list): Pill-shaped element reading:
"GSMA Full-Member MNOs Only"
— white text on #0047FF background, medium weight, 13px

**Stake requirement note** (below badge): "Must stake TEL to participate" — white, 11px, subtle

**Flywheel note** (bottom of right column): Small 3-item circular arrow icon with label:
"Usage → Fees → MNO Promotion" — gold (#C9A227), 11px, italic

---

### Zone 3 — Footer Bar (bottom 24% of canvas, ~260px tall)
**Divider**: Single 1px rule in white at 76% mark, full width, 20% opacity

**Left section (33%)** — Network status block:
- Label: "NETWORK STATUS" — all-caps, #8BA3C9, 10px
- Content: "Adiri Testnet — Active" — white, 15px
- Sub: "Mainnet: pending security audits + MNO onboarding" — #8BA3C9, 11px

**Center section (34%)** — Tech stack summary:
3-column mini-stat grid, each stat: large number/label on top, descriptor below
- Stat 1: "L1" | "EVM-Compatible Layer 1"
- Stat 2: "Rust 99.4%" | "Codebase language"
- Stat 3: "GSMA MNOs" | "Exclusive validator class"
Each stat separated by a vertical 1px #0047FF rule

**Right section (33%)** — CTA:
- "telcoin.network" — white, 16px, medium weight
- "@telcoinTAO" — #0047FF, 14px
- Small Telcoin logomark repeated, very light, as watermark texture element

---

## 2. COPYWRITING — ALL ON-INFOGRAPHIC TEXT

### Headline (max 8 words)
> **How the Telcoin Network Actually Works**

*(Rendered in white, ~38–42px, medium-bold weight, centered in header bar)*

---

### Architecture Section Labels and 1-Line Descriptions

**CONSENSUS LAYER**
Narwhal + Bullshark DAG-based consensus orders transactions — adapted from Mysten Labs / Sui.

**EXECUTION LAYER**
EVM-compatible blocks execute Ethereum-standard smart contracts — 99.4% written in Rust.

**TRANSACTION FLOW**
Transactions are ordered by consensus, then executed — two layers, one finality.

**COMMUNICATION PROTOCOL**
libp2p · QUIC-v1 · UDP · BLS validator identity keys

---

### Validator Section — GSMA MNO Copy

**Section label**: VALIDATORS

**Primary badge text**:
GSMA Full-Member MNOs Only

**Supporting line**:
Must stake TEL to participate

**Explainer (body text, small — 11px)**:
Only licensed telecom operators can validate blocks and earn network fees. Each MNO validator is also a direct distribution channel to its subscriber base.

**Flywheel label**:
Usage → Fees → MNO Promotion

---

### Network Status Block (footer left)

NETWORK STATUS
Adiri Testnet — Active
Mainnet: pending security audits + MNO onboarding

---

### Center Stats (footer middle)

L1
EVM-Compatible Layer 1

Rust 99.4%
Codebase language

GSMA MNOs
Exclusive validator class

---

### Footer CTA

telcoin.network
@telcoinTAO

---

## 3. MIDJOURNEY PROMPT (v6)

```
Dark tech infographic poster titled "How the Telcoin Network Actually Works",
16:9 landscape format, clean UI diagram aesthetic. Deep navy-black background
(#0A0E1A), TEL blue (#0047FF) accent color, white text, subtle gold (#C9A227)
highlights. Two-layer blockchain architecture diagram showing stacked panels:
top panel labeled "CONSENSUS LAYER — Narwhal + Bullshark DAG" with abstract
glowing node graph, bottom panel labeled "EXECUTION LAYER — EVM Compatible"
with Ethereum hex icon. Central horizontal flow arrows showing transaction
lifecycle. Right section showing validator nodes with signal tower icons,
pill-shaped badge "GSMA Full-Member MNOs Only" in blue. Footer bar with three
stat columns: "L1 / EVM-Compatible", "Rust 99.4% / Codebase", "GSMA MNOs /
Validators". Sans-serif UI typography, monospace code labels for protocol stack
"libp2p · QUIC-v1 · UDP". Ethereum Foundation diagram quality, NOT cartoon,
NOT crypto bro aesthetic. Professional dark-mode developer documentation style.
No photography, no people, no 3D renders. Clean vector-style flat diagram with
subtle glow effects on nodes. --ar 16:9 --v 6 --style raw --quality 2
--no cartoon, photograph, hands, person, globe, coin imagery
```

---

## 4. DALL-E 3 PROMPT

```
Create a professional dark-theme technical infographic in 16:9 landscape format
explaining how the Telcoin Network blockchain works.

Design specifications:
- Background: very dark navy (#0A0E1A), nearly black
- Primary accent: bright blue (#0047FF)
- Text: white and light grey
- Secondary accent: muted gold
- Style: clean, modern developer documentation — similar to Ethereum.org
  architecture diagrams, not illustrative or cartoonish

Layout (left to right, three columns):
LEFT COLUMN — labeled "CONSENSUS LAYER" (top rectangular panel with subtle blue
border, glowing blue DAG node graph icon, white text "Narwhal + Bullshark")
stacked above "EXECUTION LAYER" (dark panel with white Ethereum-style hexagon
icon, text "EVM-Compatible Blocks, 99.4% Rust")

CENTER — horizontal flow arrows connecting the layers with step labels:
"Transaction → Consensus → Execution → Finalized Block". Small monospace text
label: "libp2p · QUIC-v1 · UDP · BLS Keys"

RIGHT COLUMN — labeled "VALIDATORS" with 4-5 small rectangular nodes each
showing a signal/tower icon, one highlighted in blue. Below: pill-shaped button
"GSMA Full-Member MNOs Only". Text: "Must stake TEL to participate." Small text:
"Usage → Fees → MNO Promotion"

HEADER: White bold text "How the Telcoin Network Actually Works", small
blue pill badges "Chain ID: 2017" and "TEL Gas Token"

FOOTER: Left: "Adiri Testnet — Active". Center: three stat boxes (L1,
Rust 99.4%, GSMA MNOs). Right: "telcoin.network" and "@telcoinTAO"

No people, no hands, no stock photo elements. Pure technical diagram.
```

---

## 5. FLUX / IDEOGRAM PROMPT

*(Optimized for Ideogram v2 or Flux — both handle embedded text better than Midjourney)*

```
Technical blockchain architecture infographic, 16:9 widescreen format.

EXACT TEXT TO RENDER ON IMAGE:
- Headline at top center (large, white, bold): "How the Telcoin Network Actually Works"
- Top right pills: "Chain ID: 2017" | "TEL Gas Token"
- Left panel top label (small caps, blue): "CONSENSUS LAYER"
- Left panel top body: "Narwhal + Bullshark" and "DAG-Based Consensus"
- Left panel bottom label (small caps, white): "EXECUTION LAYER"
- Left panel bottom body: "EVM-Compatible" and "Ethereum-Standard Blocks" and "Rust 99.4%"
- Center top label: "TRANSACTION FLOW"
- Center flow nodes (left to right): "Transaction" → "Consensus" → "Execution" → "Finalized"
- Center bottom monospace row: "libp2p · QUIC-v1 · UDP · BLS Keys"
- Right column header: "VALIDATORS"
- Right column badge (blue pill): "GSMA Full-Member MNOs Only"
- Right column note: "Must stake TEL to participate"
- Right column flywheel: "Usage → Fees → MNO Promotion"
- Footer left: "Adiri Testnet — Active"
- Footer center stats: "L1" | "Rust 99.4%" | "GSMA MNOs"
- Footer right: "telcoin.network" and "@telcoinTAO"

VISUAL STYLE:
Dark navy background, nearly black. Primary blue accent (#0047FF).
White and light-grey text. Subtle gold accent text. Clean sans-serif
UI typography throughout. Two stacked rectangular layer panels on left,
horizontal flow diagram in center, vertical validator node stack on right.
Abstract glowing dot-and-line DAG graph inside consensus panel.
Ethereum hex icon inside EVM panel. Signal tower icons on validator nodes.
Professional blockchain developer documentation aesthetic — no cartoons,
no photography, no people, no coins, no globe graphics.
```

---

## 6. COMPANION X POST COPY

*(For @telcoinTAO — post alongside the infographic)*

---

**Option A** (architecture-forward):

> Telcoin Network runs a two-layer architecture: Narwhal + Bullshark DAG consensus on top, EVM-compatible execution below — written 99.4% in Rust.
>
> The validator set is exclusively GSMA full-member MNOs. Not just validators — each one is a live telecom distribution channel.
>
> telcoin.network

---

**Option B** (validator-angle lead):

> On Telcoin Network, only GSMA full-member telecom operators can validate blocks and earn fees.
>
> That's not a restriction — it's the distribution model. Every MNO that validates is also a direct channel to its subscriber base.
>
> Architecture breakdown: telcoin.network

---

**Option C** (technical credibility lead):

> Telcoin Network: EVM-compatible L1, Narwhal + Bullshark DAG consensus, 99.4% Rust, libp2p + QUIC-v1 networking, BLS validator identity, Chain ID 2017.
>
> Validators: exclusively GSMA full-member MNOs staking TEL.
>
> Adiri testnet is live. Mainnet follows final audits and MNO onboarding.
>
> telcoin.network

---

**Recommended**: Option A for general audience. Option C for developer/technical audience days.

---

## PRODUCTION NOTES

- Recommended AI tool for this asset: **Ideogram v2** (best embedded text rendering) or **Flux Dev** with a good text LoRA. Midjourney v6 is third choice — text legibility requires post-processing.
- After generation: bring into Figma or Adobe Illustrator to manually set all text in brand typeface (Inter, Neue Haas Grotesk, or Space Grotesk all work for this aesthetic). AI-generated text on diagrams should always be treated as a layout placeholder, then replaced.
- File to save final asset: `design/output/network-infographic-final.png`
- This brief authored: March 12, 2026
- Authored by: Image Prompt Engineer agent, Telcoin Association Marketing Agency

---

*Brief saved to: `/home/user/Telcoin-Association-Agency/design/output/network-infographic-brief.md`*
