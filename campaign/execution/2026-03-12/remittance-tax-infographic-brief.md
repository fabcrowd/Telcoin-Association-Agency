# Remittance Tax Infographic Brief + Companion Tweets
**Campaign**: U.S. Remittance Tax — Fee Comparison & Telcoin Wallet Positioning
**Created**: March 12, 2026
**Author**: Image Prompt Engineer Agent
**Status**: Draft — pending client verification (see checklist below)

---

## PUBLISH-READY CHECKLIST

Flag every figure below before approving for publication. The research file documents ranges, not single verified figures for a $200 Mexico-specific transfer. Client must supply or confirm point-in-time fees before the infographic goes live.

### Figures Requiring Client Verification

| Data Point | Source in Research File | Status | Action Required |
|---|---|---|---|
| Western Union fee on $200 to Mexico | "3–8% typical" (TELCOIN-RESEARCH.md §6) | NOT VERIFIED — range only | Client to provide current quoted fee on telcoin.org/western-union for $200 USD → MXN corridor |
| MoneyGram fee on $200 to Mexico | "4–6%" (TELCOIN-RESEARCH.md §6) | NOT VERIFIED — range only | Client to pull current moneygram.com quote for $200 USD → Mexico cash pickup |
| International bank wire flat fee | "$25–$45" (TELCOIN-RESEARCH.md §6) | NOT VERIFIED — range only | Client to confirm which institution and wire type; specify whether this includes correspondent bank fees |
| Telcoin Wallet fee on $200 to Mexico | "2% or less total (vs. 6–10%)" (TELCOIN-RESEARCH.md §3) | NOT VERIFIED — stated as a target, not a confirmed live rate | Client to confirm current live fee for $200 USD → Mexico corridor (Tigo Money not listed for Mexico; Guatemala only) |
| Mexico listed as active Telcoin corridor | Mexico NOT in the 16-corridor table (TELCOIN-RESEARCH.md §3) | DISCREPANCY | Mexico is not in the active corridor list — Guatemala uses Tigo Money but Mexico is absent. Client must confirm whether Mexico is a live corridor or whether the infographic should use a different destination country |
| 1% remittance tax scope | "cash-funded international remittances" (intel-market-2026-03-12.md §4) | VERIFIED from intel file | Apply to Western Union + MoneyGram cash-funded columns only |
| Bank-linked transfer exemption | "bank-linked digital transfers are fully exempt" (intel-market-2026-03-12.md §4) | VERIFIED from intel file | Apply to Telcoin Wallet column as exempt |

### Critical Discrepancy — Mexico Corridor

The infographic concept specifies Mexico as the destination. Mexico does not appear in the 16-country active corridor list in TELCOIN-RESEARCH.md. Guatemala (Tigo Money) is listed, not Mexico. Before designing or publishing this infographic, confirm one of the following with the client:

- Mexico is a live corridor not yet documented in the research file (update research file if confirmed)
- The destination country for the infographic should be changed to a confirmed active corridor (e.g., Philippines via Coins, Kenya via Equitel Money, or Bangladesh via BKash — all high-remittance-volume markets)

---

## OUTPUT 1 — IMAGE BRIEF + AI IMAGE PROMPTS

### Creative Brief: Fee Comparison Infographic

**Project title**: "What a $200 Remittance Actually Costs"
**Format**: Vertical infographic, optimized for mobile (1080 x 1920 px) with a secondary horizontal crop for desktop/Twitter card (1200 x 675 px)
**Platform**: X/Twitter, Telcoin forum, potentially LinkedIn
**Deliverable type**: Static data visualization
**Brand**: Telcoin Association (@telcoinTAO)

---

### Visual Concept

A clean, dark-background fee comparison showing the true total cost of sending $200 internationally across four channels. The visual hierarchy leads with the cost gap, not with product branding. The tax label is factual and prominent — this is an educational piece, not an advertisement.

**Recommended format**: Horizontal bar chart (not a table) — bars read faster on mobile and allow proportional cost comparisons to be absorbed at a glance. Four bars, one per channel, extending left to right from $0 to maximum effective cost. Each bar is segmented to show base fee versus the remittance tax surcharge where applicable.

---

### Four Columns / Bars

Use these placeholders until client verifies exact figures. The infographic template should be built with variable data fields so verified numbers can be dropped in without redesigning.

**Column 1: Western Union (cash pickup)**
- Base fee: [CLIENT TO VERIFY — documented range: $6.00–$16.00 on $200, derived from 3–8%]
- 1% federal excise tax: [CLIENT TO VERIFY — $2.00 on $200 base amount]
- Total effective cost: [CLIENT TO VERIFY]
- Label beneath bar: "includes 1% federal excise tax"
- Bar color: muted warm gray (neutral — not red/green; avoid editorializing)

**Column 2: MoneyGram (cash pickup)**
- Base fee: [CLIENT TO VERIFY — documented range: $8.00–$12.00 on $200, derived from 4–6%]
- 1% federal excise tax: [CLIENT TO VERIFY — $2.00 on $200 base amount]
- Total effective cost: [CLIENT TO VERIFY]
- Label beneath bar: "includes 1% federal excise tax"
- Bar color: muted warm gray

**Column 3: International Bank Wire**
- Flat fee: [CLIENT TO VERIFY — documented range: $25–$45]
- No remittance tax (bank-linked, exempt)
- Total effective cost: [CLIENT TO VERIFY — flat fee only; high relative to transfer size]
- Label beneath bar: "bank wire — no excise tax, but high flat fee"
- Bar color: cool neutral gray

**Column 4: Telcoin Wallet**
- Fee: [CLIENT TO VERIFY — target is ≤2%, or ≤$4.00 on $200]
- No remittance tax (bank-linked transfer, structurally exempt)
- Total effective cost: [CLIENT TO VERIFY]
- Label beneath bar: "exempt — bank-linked transfer"
- Bar color: cyan (#00D4FF or nearest brand equivalent) — the only bar in brand color

---

### Typography & Layout Direction

- Background: deep navy / near-black (#0A0E1A or equivalent dark indigo)
- Primary text: white (#FFFFFF)
- Secondary text / labels: light gray (#B0B8C8)
- Accent / highlight: cyan (#00D4FF) — used only on Telcoin bar and tax-exempt label
- Infographic title: white, bold, large — top of frame
- Tax notation labels: small caps or label style beneath each bar — factual, not emphatic
- Source attribution: bottom of frame, small text — "Source: Telcoin Association research, March 2026 / One Big Beautiful Bill Act (2025)"
- Telcoin wordmark: bottom right corner — small, not dominant
- No decorative icons, no cartoon elements, no human figures, no country flags

---

### Mobile-First Layout Specification

- Top: Title — "What it costs to send $200"
- Sub-header: "Including 1% U.S. federal excise tax on cash-funded transfers (effective Jan 1, 2026)"
- Chart area: horizontal bar chart, four bars stacked vertically, with dollar labels at end of each bar
- Below chart: two-line callout box in cyan border — "Telcoin Wallet uses a bank-linked transfer. Not subject to the federal excise tax."
- Bottom: source attribution + Telcoin wordmark

---

### AI Image Prompts

All three prompts target the same core visual. They are written for different generation approaches: one structured/technical, one atmospheric/editorial, one explicit negative-prompt-focused for clean execution.

---

**Prompt 1 — Structured Technical (Midjourney / Flux)**

```
Dark-background data visualization infographic, horizontal bar chart comparing remittance fees across four payment channels: Western Union cash, MoneyGram cash, bank wire, and Telcoin Wallet, deep navy background (#0A0E1A), four horizontal bars extending left to right, three bars in muted cool gray, one bar in vivid cyan representing Telcoin Wallet, clean sans-serif typography in white and light gray, dollar amounts displayed at bar endpoints in white text, small label beneath each bar indicating tax status, cyan accent highlight on tax-exempt label, subtle grid lines in near-invisible dark gray, Telcoin wordmark in bottom right corner, financial data visualization aesthetic, Bloomberg terminal meets editorial design, professional and austere, no decorative elements --ar 9:16 --style raw --v 6.1
```

Negative prompt: `--no cartoon, icons, human figures, faces, hands, country flags, neon glow effects, gradient explosions, drop shadows, 3D perspective, decorative borders, stock photo texture, warm tones, red color, green color, orange color`

---

**Prompt 2 — Editorial Dark Data Viz (DALL-E / Flux)**

```
Professional financial infographic on a deep indigo near-black background. A horizontal bar chart showing four rows: "Western Union (cash)", "MoneyGram (cash)", "Bank Wire", and "Telcoin Wallet". The first three bars are rendered in cool neutral gray. The Telcoin Wallet bar is rendered in electric cyan. Each bar has a precise dollar amount label in white sans-serif text at the right endpoint. Below the first two bars, a small label reads "includes 1% federal excise tax" in light gray italics. Below the Telcoin Wallet bar, a small cyan label reads "exempt — bank-linked transfer". Chart title in large white bold text at top: "What it costs to send $200". A thin cyan-bordered callout box below the chart. Telcoin logotype in small white text at bottom right. The visual language is infrastructure, precision, and institutional credibility. No human figures, no illustrations, no decorative flourishes.
```

Negative prompt: `cartoon, clipart, emoji, human faces, hands, flags, neon glows, sparkles, confetti, warm color palette, orange, red, green, gradient backgrounds, radial gradients, 3D chart style, isometric design, drop shadows`

---

**Prompt 3 — High-Contrast Minimalist (Stable Diffusion / Flux)**

```
Minimalist financial data visualization, dark mode, deep navy background, horizontal bar chart with four data rows, three bars in desaturated steel gray, one bar in bright cyan, white sans-serif typography, no decorative elements, Bloomberg-style data display aesthetic, clean grid structure, single accent color (cyan #00D4FF) applied only to the fourth bar and associated text label, professional financial publication quality, infographic proportioned for mobile vertical format, sharp clean edges, zero visual noise, institutional design language, flat design with no depth effects
```

Negative prompt: `human figure, face, hand, body, flag, icon, symbol, emoji, illustration, cartoon, warm colors, yellow, red, orange, green, gradient, glow, bloom, radial light, 3D, isometric, perspective distortion, drop shadow, bokeh, photography, photorealistic texture, paper texture, grunge`

---

## OUTPUT 2 — COMPANION TWEETS

All three tweets are written for @telcoinTAO. Tone: factual, direct. No price talk. No hype language. Character counts estimated; verify before scheduling.

---

### Tweet 1 — The Tax: What It Is and What It Applies To

```
As of January 1, 2026, a 1% federal excise tax applies to cash-funded international remittances sent from the United States.

The tax is applied to the transfer amount — not the fee — and affects services like Western Union and MoneyGram where the sender uses cash.

Bank-linked digital transfers are exempt.
```

Character count: ~280 (verify)
Attach: infographic (full vertical crop for mobile)
No hashtags on first publish — add only if platform strategy calls for it

---

### Tweet 2 — Telcoin Wallet Exemption: Structural, Not Incidental

```
Telcoin Wallet processes transfers through Telcoin Digital Asset Bank — a state-chartered U.S. bank.

That structure matters: bank-linked transfers are explicitly exempt from the 1% federal remittance excise tax enacted in 2026.

This is not a workaround. It is how the regulation was written.
```

Character count: ~272 (verify)
Attach: no image (text-forward; let tweet 1 carry the visual)
Note: "Telcoin Digital Asset Bank — a state-chartered U.S. bank" phrasing is verified. Charter date November 12, 2025. Nebraska DADI.

---

### Tweet 3 — Active Corridor Data: The Network That Exists Today

```
Telcoin Wallet operates across 16 active remittance corridors — Bangladesh, Ethiopia, Fiji, Ghana, Guatemala, Indonesia, Kenya, Sri Lanka, Malawi, Nepal, Pakistan, Philippines, El Salvador, Tonga, Uganda, and Samoa.

23+ mobile money platforms. One wallet.

The network is live. No mainnet required.
```

Character count: ~274 (verify)
Attach: no image — optionally link to telco.in
Note: Corridor list is verified from TELCOIN-RESEARCH.md §3. Do not add Mexico until confirmed (see checklist above).

---

## THREAD SEQUENCING NOTE

If publishing as a thread: Tweet 1 → Tweet 2 → Tweet 3 in that order. The infographic attaches to Tweet 1 (the factual anchor). Tweet 2 deepens the structural argument. Tweet 3 closes with proof of existing infrastructure.

If publishing as standalone tweets across multiple days: Tweet 1 and infographic first (highest standalone value). Tweet 2 second (policy/compliance audience). Tweet 3 third (product/network audience).

---

## DESIGN SYSTEM REFERENCE

Per TELCOIN-RESEARCH.md and CLAUDE.md brand guidelines:

| Element | Spec |
|---|---|
| Background | Deep navy / near-black — #0A0E1A or equivalent |
| Primary text | White — #FFFFFF |
| Secondary text | Light gray — #B0B8C8 |
| Brand accent | Cyan — #00D4FF (Telcoin brand cyan) |
| Neutral bars | Cool steel gray — #4A5568 or similar |
| Typography style | Clean sans-serif (Inter, IBM Plex Sans, or equivalent) |
| No | Cartoon elements, human figures, country flags, decorative icons |
| No | Warm color palette, gradient explosions, 3D chart styles |

---

*File saved: /home/user/Telcoin-Association-Agency/campaign/execution/2026-03-12/remittance-tax-infographic-brief.md*
*Branch: claude/campaign-iLgt5*
