# Telcoin Network, Part 3: What Gets Built On It, and the Upgrade Behind It

The first two parts covered why Telcoin Network exists and how it runs. This week starts with the part that matters most: what gets built on it. Then it covers a foundational piece of work happening ahead of mainnet — the TEL token upgrade, and why it needed to happen first.

## What actually gets built on Telcoin Network

Infrastructure is only useful if people build on it. Because Telcoin Network is a public, EVM-compatible blockchain, it supports the same kind of applications you'd expect on any modern EVM chain: lending markets, exchanges, payment tools, wallets, and beyond. But because of who's validating it and who it's built for, the more interesting question is what gets built specifically for mobile-first, regulated financial access. A few concrete examples:

- **Merchant payment tools** for markets where card infrastructure never took hold, letting a shop accept digital cash directly through a phone
- **Remittance and savings apps** built around a phone number instead of a bank account, for the roughly 1.4 billion adults globally who remain unbanked
- **Lending and credit products** that can plug into the kind of usage and payment data telcos already hold on their subscribers — data traditional finance never had access to
- **Cross-border payroll tools** for businesses paying distributed or migrant workforces, settling in seconds instead of days
- **Airtime and mobile-money on-ramps**, converting existing prepaid balances directly into on-chain digital cash without a separate onboarding step
- **Compliance and identity tooling**, built on top of the KYC relationships MNOs already have with their subscriber base, that other developers can plug into rather than rebuild from scratch
- **DeFi primitives** like liquidity pools and swaps through TELx, giving any of the above products a liquidity layer to draw on

One more worth flagging, further out on the horizon: AI agents making payments on someone's behalf. Across the wider industry, stablecoins are emerging as the natural rail for this — an agent doesn't need a bank account, can hold value directly, and can settle instantly and around the clock, none of which is true of a card network built for humans clicking "buy." Telcoin Network isn't announcing an agent-specific product, but the pieces are the same ones already discussed in this series: TDAB issuing regulated, redeemable stablecoins, and a network built for instant, low-cost settlement. That combination positions the network well if and when agent-initiated payments become mainstream — a foundation worth noting, not a confirmed roadmap item to expect imminently.

There are two distinct routes to build any of this on Telcoin Network, and they serve different purposes.

**The open route.** Because it's a public EVM-compatible chain, any developer, anywhere, can deploy a smart contract or build an application on Telcoin Network the same way they would on any other EVM chain. No special registration, no gatekeeping. If you can build for Ethereum, you can build here.

**The GSMA Application Developer route.** This is specific to Telcoin's ecosystem, and it's broader than just the telcos validating the network. Any company holding GSMA membership — not only Mobile Network Operators — can register as an Application Developer within the Telcoin Platform's formal structure. That comes with advantages the open route doesn't: a seat inside the Telcoin Application Network's governance and incentive programs, network rewards and TEL earned for building and operating on the platform, and the ability to build customized financial products tailored to a specific local market. For an MNO specifically, that also means launching on top of a subscriber base and regulatory relationships it already has, rather than building trust and distribution from zero the way a typical crypto app has to.

Put together, that's the shape of the ecosystem: open enough that any developer can build here, and structured enough that GSMA members — telcos and beyond — have a dedicated, incentivized path to build the applications this network was designed to carry.

## Why TEL is being upgraded, not migrated

The word "upgrade" here is deliberate. This isn't a migration to a new chain or a new token. TEL keeps its name, its ticker, and every holder's balance stays exactly where it is. What's changing is the token standard underneath it, and the reason is straightforward: the current TEL contract wasn't built for the job it's about to do.

TEL today uses 2 decimal places. Almost the entire EVM ecosystem — exchanges, decentralized exchanges, lending markets, wallets — standardized on 18 decimals years ago, and that standard has only gotten more rigid over time. A non-standard decimal count means custom engineering for anyone who wants to integrate the token, and plenty of potential integrations simply don't get built rather than take on that extra work.

It matters even more once Telcoin Network goes live, because TEL becomes the network's native gas token. A blockchain needs to price transactions in fractions far smaller than 0.01, and a 2-decimal token can't do that. There's a second problem: moving TEL from a chain where it has 18 decimals back to one where it only has 2 truncates anything past the second decimal place, permanently. At scale, across millions of transactions, that's real value quietly lost every time someone bridges out.

The upgrade fixes this cleanly: a standards-compliant, 18-decimal TEL contract, deployed with the same address across every supported chain, with mint-and-burn capability that replaces the older lock-and-release bridging model. Every holder upgrades one-for-one, in a single transaction, whenever they choose. Balances don't change. The ticker doesn't change. Nothing is taken from anyone's wallet.

This is currently working through the Telcoin Association's governance process — Council review and approval, ahead of formal ratification — so treat this as the plan rather than a finished upgrade. It's a plan worth understanding now, though, because it's the foundation everything above depends on: none of what gets built on this network runs well on native gas that can't be priced correctly.

## Next up

Every claim about architecture and design only means something once it's tested under real load. Next week: what scale actually looks like on Telcoin Network, with real performance numbers.
