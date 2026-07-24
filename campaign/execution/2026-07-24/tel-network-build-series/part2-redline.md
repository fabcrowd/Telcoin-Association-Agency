# Telcoin Network, Part 2: What's Actually Happening Under the Hood

> **REDLINE KEY**: ~~strikethrough~~ = delete · **[ADDED: text]** = insert

---

Last week we covered why Telcoin Network exists and who's running it. This week, the mechanics: what actually happens when a transaction moves across the network, and why the architecture is built the way it is.

## The two jobs a network has to do

Strip away the terminology and every blockchain is solving the same two problems. First, agree on what happened. A payment needs everyone running the network to agree it occurred, in what order, and that it isn't being spent twice. Second, keep a record everyone can check. That record has to be available and verifiable without requiring a central party to vouch for it.

Telcoin Network solves both of those problems with two different kinds of participants doing two different jobs: validators, and relay nodes.

## Validators: the MNOs producing blocks

Validators are the participants who actually produce blocks and agree on the state of the network. As covered last week, on Telcoin Network these are Mobile Network Operators rather than anonymous staking pools. Each validator runs the node software, participates in reaching consensus with the other validators, and is accountable for doing so under its own regulatory standing in its own jurisdiction.

That accountability is the part that's easy to miss if you're used to thinking about validators as an interchangeable, permissionless set. On most chains, a validator is a piece of infrastructure with capital behind it and not much else. On Telcoin Network, a validator is a licensed telecom operator with an existing regulatory relationship, an existing subscriber base, and a reputation it can't afford to put at risk. That changes the incentives in a way that matters more for a payments network than it does for a speculative asset.

## Relay nodes: keeping everyone honest

Not every participant needs to help produce blocks to be useful. Relay nodes (sometimes called observer nodes) sync the full state of the network, serve data to applications and wallets, and give anyone the ability to independently verify what the validators are reporting, without needing to be a validator themselves.

This matters for a simple reason: it means trust in the network doesn't rest entirely on trusting the validator set to self-report honestly. Anyone running a relay node can check the chain's state directly. It's the difference between "trust us" and "verify it yourself," and for a network handling remittances and regulated financial products, that difference is the whole point.

## Why this shape, specifically

Put the two roles together and you get a network where block production is handled by a known, accountable, regulated set of operators, while verification is open to anyone willing to run the software. That's a deliberate trade-off. Fully permissionless validator sets optimize for censorship resistance from anonymous, unaccountable actors. Telcoin Network optimizes for something else: a payments network that regulators, banking partners, and everyday users can actually trust, backed by operators who are already accountable to real oversight in the real world.

It also means the network can scale its validator set the way telecom itself scales, market by market, operator by operator, each one bringing its own local compliance and infrastructure with it, rather than trying to bootstrap trust from nothing the way a typical crypto network has to.

## A more modern kind of L1

~~Here's where Telcoin Network actually breaks from the standard EVM-PoS playbook, and it's worth slowing down for, because this is the part that separates "another chain with telcos as validators" from "an architecture built for this specific job."~~

Most EVM chains you know, Ethereum included, run what's essentially a single-lane system. Validators take turns proposing a block, everyone else votes on it, and the network can't move to the next block until that round finishes. It works, but the lane only gets wider so much before the whole thing backs up. That's the root of most gas spikes and network congestion you've seen anywhere in crypto.

Telcoin Network splits that single lane into two separate jobs, running in parallel instead of in sequence.

**Getting data around the network** is handled by a mempool layer built on a design called Narwhal. Instead of one validator at a time broadcasting a batch of transactions and waiting for everyone else to catch up, every validator disseminates its own batches of transaction data simultaneously and continuously. The network isn't waiting on a single proposer's turn to move data around, so the whole thing can be pushed a lot harder before it feels congested.

**Agreeing on the order of everything** is a separate job, handled on top of that data by a consensus protocol called Bullshark. Rather than the classic back-and-forth vote-and-confirm cycle most PoS chains use, Bullshark works by reading the structure of how validators' data references each other over time (this shape is what's known as a directed acyclic graph, or DAG) and deriving agreement from that structure directly, without needing extra rounds of messaging just to confirm what's already implied by the data.

~~The upshot: transaction~~ **[ADDED: Transaction]** propagation and transaction ordering aren't competing for the same lane anymore, and confirming agreement doesn't need bolt-on communication overhead. That's a meaningfully different shape of network than the block-by-block, one-proposer-at-a-time model most EVM chains still run.

None of this changes what it feels like to build on Telcoin Network day to day. On top of that consensus layer sits a fully EVM-compatible execution layer, so smart contracts, tooling, and wallets all work the way developers already expect from Ethereum. The modern architecture lives underneath; the developer experience on top of it stays familiar. ~~That's deliberate: better~~ **[ADDED: Better]** performance shouldn't cost you the ecosystem of tools people already know how to use.

## Real-time hooks for everything built on top: ExEx

Modern architecture underneath is one thing. Making it easy for wallets, bridges, block explorers, and dapps to actually keep up with what's happening on-chain is a separate problem, and it's one Telcoin Network solves with something called ExEx, short for Execution Extension.

The idea originally comes from Reth: a plugin system that lets external software react to what's happening on the node in real time, instead of constantly polling an RPC endpoint and hoping it's caught up. Reth's own version reacts once a block has been executed. Telcoin Network's version goes further and tracks the entire lifecycle of a transaction rather than just the end of it:

1. **A certificate is accepted** — a peer's data has been verified and is now part of the network's DAG
2. **Consensus is committed** — Bullshark has settled on the order of that data
3. **The chain is executed** — the resulting blocks are run and become part of the canonical record

That gives anything built on top of the network, a bridge, a wallet, a block explorer, visibility into a transaction from the moment it's accepted through to final execution, instead of only finding out once it's already done.

It also means those integrations carry less complexity than they normally would. Because Bullshark reaches consensus with immediate finality, ~~there's no such thing as a reorg on Telcoin Network~~ **[ADDED: there are no reorgs on Telcoin Network]**. Anything an ExEx plugin sees is already final, so there's no waiting to see if a block gets replaced, and no reconciliation logic for chain reorganizations that most Ethereum-style infrastructure has to build in from day one.

And because it's built for production use, a slow or misbehaving plugin can never take the network down with it. Each ExEx runs as its own isolated task; at worst it falls behind and has to catch up, it can't stall consensus or crash the node. That's not the kind of detail that shows up in a pitch deck, but it's exactly what matters when banks, telcos, and wallets are all depending on the same infrastructure staying up.

## What this means in practice

When someone sends digital cash across Telcoin Network, here's the shape of what's happening: the transaction gets broadcast to the network, the validator set reaches consensus on including it and in what order, and that new state gets propagated out to relay nodes, wallets, and applications that need to know about it. All of that happens in the background, in seconds, whether the person sending it is on a laptop or a low-end phone on a patchy mobile connection in a country most crypto infrastructure was never built to serve.

That's the job the architecture is doing. Not speed for its own sake, and not decentralization as a slogan, but a specific, deliberate structure built to make a compliant, trustworthy, mobile-first payments network actually work.

## Next up

~~Building this kind of network is one thing. Shipping major upgrades to it without breaking the trust of exchanges, custodians, and everyday users is another. Next week: a real case study in exactly that, told through Telcoin Network's move from V2 to V3.~~ **[ADDED: Building this kind of network is one thing. What gets built on top of it — and the foundational upgrade happening ahead of mainnet — is next.]**
