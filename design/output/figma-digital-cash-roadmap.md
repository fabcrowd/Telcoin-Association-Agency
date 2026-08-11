# FigJam Diagram Spec — Digital Cash Roadmap

**Purpose**: Timeline flowchart for use in FigJam via Mermaid diagram import.
**Source slide**: MNO deck — Digital Cash Roadmap
**Brand colors**: `#090920` bg / `#14C8FF` TEL Blue / `#3642B2` Royal Blue / `#10B981` green (eUSD)
**Last updated**: 2026-03-18

---

## Mermaid Diagram

```mermaid
%%{init: {
  "theme": "base",
  "themeVariables": {
    "background": "#090920",
    "primaryColor": "#0d0d2a",
    "primaryTextColor": "#FFFFFF",
    "primaryBorderColor": "#3642B2",
    "lineColor": "#14C8FF",
    "secondaryColor": "#111135",
    "tertiaryColor": "#0d0d2a",
    "edgeLabelBackground": "#090920",
    "clusterBkg": "#0d0d2a",
    "clusterBorder": "#3642B2",
    "titleColor": "#14C8FF",
    "nodeBorder": "#3642B2",
    "nodeTextColor": "#FFFFFF"
  }
}}%%

flowchart LR

  %% ── CLASS DEFINITIONS ──────────────────────────────────────────
  classDef launched   fill:#0d1a3a,stroke:#14C8FF,color:#FFFFFF,stroke-width:2px
  classDef eusdNode   fill:#0d2e1e,stroke:#10B981,color:#FFFFFF,stroke-width:3px,font-weight:bold
  classDef expected   fill:#0d0d2a,stroke:#3642B2,color:#C9CFED,stroke-width:1px
  classDef expanding  fill:#090920,stroke:#424761,color:#7393EA,stroke-width:1px,stroke-dasharray:4 3
  classDef headerNode fill:#111135,stroke:#3642B2,color:#14C8FF,stroke-width:2px,font-weight:bold

  %% ── Q1 2025 CLUSTER ────────────────────────────────────────────
  subgraph Q1_2025["Q1 2025 — Actual Release"]
    direction TB
    H1["Q1 2025"]:::headerNode
    eAUD["🇦🇺 eAUD\nAustralian Dollar"]:::launched
    eMXN["🇲🇽 eMXN\nMexican Peso"]:::launched
    eGBP["🇬🇧 eGBP\nPound Sterling"]:::launched
    eNZD["🇳🇿 eNZD\nNew Zealand Dollar"]:::launched
    eSGD["🇸🇬 eSGD\nSingapore Dollar"]:::launched
    eCFA["🌍 eCFA\nAfrican Franc"]:::launched
    eCAD["🇨🇦 eCAD\nCanadian Dollar"]:::launched
    eJPY["🇯🇵 eJPY\nJapanese Yen"]:::launched
    eHKD["🇭🇰 eHKD\nHong Kong Dollar"]:::launched
    eZAR["🇿🇦 eZAR\nSouth African Rand"]:::launched
    eSDR["🌐 eSDR\nSpecial Drawing Right"]:::launched
  end

  %% ── eUSD FOCAL NODE ────────────────────────────────────────────
  eUSD["$ eUSD\nTelcoin Digital Asset Bank\nU.S. Dollar\n▸ Launched Dec 2025"]:::eusdNode

  %% ── Q4 2025 / Q1 2026 CLUSTER ──────────────────────────────────
  subgraph Q4_2025_Q1_2026["Q4 2025 / Q1 2026 — Expected Release"]
    direction TB
    H2["Q4 2025 – Q1 2026"]:::headerNode
    eEUR["🇪🇺 eEUR\nEuro"]:::expected
    eCHF["🇨🇭 eCHF\nSwiss Franc"]:::expected
    eDKK["🇩🇰 eDKK\nDanish Krone"]:::expected
    eINR["🇮🇳 eINR\nIndian Rupee"]:::expected
    eKES["🇰🇪 eKES\nKenyan Shilling"]:::expected
    eSEK["🇸🇪 eSEK\nSwedish Krona"]:::expected
    eCZK["🇨🇿 eCZK\nCzech Koruna"]:::expected
    eHUF["🇭🇺 eHUF\nHungarian Forint"]:::expected
    eISK["🇮🇸 eISK\nIcelandic Krone"]:::expected
    eNOK["🇳🇴 eNOK\nNorwegian Krone"]:::expected
    eTRY["🇹🇷 eTRY\nTurkish Lira"]:::expected
  end

  %% ── Q1 2026+ CLUSTER ───────────────────────────────────────────
  subgraph Q1_2026_plus["Q1 2026+ — Expanding"]
    direction TB
    H3["Q1 2026+"]:::headerNode
    UA["🇺🇦 Ukraine"]:::expanding
    PH["🇵🇭 Philippines"]:::expanding
    BR["🇧🇷 Brazil"]:::expanding
    EG["🇪🇬 Egypt / MENA"]:::expanding
    ID["🇮🇩 Indonesia"]:::expanding
    TZ["🇹🇿 Tanzania"]:::expanding
    CO["🇨🇴 Colombia"]:::expanding
    PK["🇵🇰 Pakistan"]:::expanding
    MORE["+ More in Discussion"]:::expanding
    NOTE["Active discussions with central banks\nand law firms globally."]:::expanding
  end

  %% ── TIMELINE FLOW ───────────────────────────────────────────────
  Q1_2025 -->|"Timeline →"| eUSD
  eUSD -->|"Timeline →"| Q4_2025_Q1_2026
  Q4_2025_Q1_2026 -->|"Expanding →"| Q1_2026_plus
```

---

## FigJam Import Notes

1. Copy the Mermaid block above.
2. In FigJam, insert a new block via **Insert > Diagram > Mermaid**.
3. Paste the code and generate.
4. After import, manually override node colors in FigJam to match brand palette:
   - **Launched nodes**: stroke `#14C8FF`, fill `#0d1a3a`
   - **eUSD node**: stroke `#10B981`, fill `#0d2e1e` — apply green glow effect
   - **Expected nodes**: stroke `#3642B2`, fill `#0d0d2a`
   - **Expanding nodes**: stroke `#424761` dashed, fill `#090920`
   - **Connector arrows**: `#14C8FF`
5. Set canvas background to `#090920` (TEL Black).
6. Apply "New Hero" or Inter typeface to all text nodes.

---

## Design Annotation for Figma Handoff

| Element | Value |
|---|---|
| Canvas size | 1920 × 1080px |
| Background | `#090920` |
| Timeline rail color | `#14C8FF` |
| Launched node stroke | `#14C8FF` |
| eUSD node fill | `#0d2e1e` |
| eUSD node stroke | `#10B981` |
| eUSD glow effect | `0 0 40px rgba(16,185,129,0.35)` |
| Expected node stroke | `#3642B2` |
| Expanding node stroke | `#424761` dashed |
| Primary text | `#FFFFFF` |
| Secondary text | `#C9CFED` |
| Muted text | `#7393EA` |
| Currency code labels | `#14C8FF` Bold |
| Font | New Hero (fallback: Inter) |
| Column header style | Phase badge (pill) + period label |
| Hexagonal motif | Applied to eUSD focal node and currency tokens |
