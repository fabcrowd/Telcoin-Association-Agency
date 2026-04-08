# TANIP-1 Amendment I: Resumption via Zero-Distribution Period Bridge

**Status:** Draft  
**Type:** Amendment  
**Amends:** TANIP-1 — Trading Fee Rebate Program  
**Date:** April 2026

---

## Summary

This amendment proposes resuming TANIP-1 using the **existing smart contracts**, bridging the paused period by inserting zero-distribution entries for the weeks in which the program was inactive. This preserves all users' earned reward histories and avoids any need to redeploy contracts or migrate state.

---

## Background

TANIP-1 (the Trading Fee Rebate Program) was paused approximately 16 weeks ago. During the pause, no weekly allocations were distributed, resulting in an estimated budget saving of ~51.2M TEL (16 weeks × 3,205,128.205 TEL).

The on-chain calculator contract and off-chain distribution script track cumulative user balances — specifically each user's **total earned** amount — across sequential weekly periods. When the program resumes, the calculator must be brought up to date with the current week before any new distributions can be processed. Without an explicit bridging mechanism, the contract's internal period index falls behind real time, which could corrupt future reward calculations.

---

## Problem Statement

The calculator contract processes distributions period by period. Because the program was paused mid-sequence, the contract's period index no longer reflects the current week. Simply resuming distributions without addressing the gap would cause the contract to apply new distribution data against stale period state, potentially miscalculating users' time-weighted stakes and earned totals.

Two approaches were considered:

| Approach | Pros | Cons |
|---|---|---|
| **A. Redeploy new contracts** | Clean slate | Erases all users' earned history; requires migration |
| **B. Insert zero-distribution periods (this proposal)** | Preserves full user history | Requires testing to confirm contract accepts zero inputs |

---

## Proposed Solution

Insert one or more **zero-distribution periods** into the contract to cover the paused weeks, advancing the period index to the present without crediting any rewards. This can be implemented as:

- A single zero-distribution period spanning the entire paused interval, **or**
- Individual zero-distribution entries for each of the ~16 paused weeks

Either approach advances the contract's internal state to the current period cleanly, with no effect on users' accumulated balances.

### Calculation Unchanged

The rebate calculation defined in TANIP-1 is **not modified** by this amendment:

```
R = (user_fees / total_fees) × period_allocation

rebate = min(R, stake_cap)        # where stake_cap = TWAS − previously_earned
rebate = min(rebate, fees_paid)   # final fee cap (TANIP-1 rule)
```

Zero-distribution periods contribute 0 to `R` for all users, leaving `previously_earned` balances unchanged.

---

## Testing & Validation

Prior to this proposal being formalised, the approach was tested end-to-end. The following was confirmed:

1. **Smart contract accepts zero inputs** — The calculator contract processes a period with a zero allocation value without reverting or corrupting state.
2. **Off-chain script handles zero distributions** — The distribution script runs successfully when passed zero-value period data, producing no payouts and no errors.
3. **System continues normally after bridging** — Following the zero-distribution bridge, a subsequent live distribution period was processed correctly, with accurate reward calculations and no balance drift.

All three tests passed. The approach is confirmed safe to implement.

---

## Rationale for Using Existing Contracts

Redeploying contracts would erase every user's `total_earned` history. Under the stake cap formula:

```
stake_cap = time_weighted_average_stake − total_earned
```

Resetting `total_earned` to zero would artificially inflate each user's reward cap in the first period after relaunch, potentially allowing outsized payouts inconsistent with their actual staking history. Preserving the existing contract state ensures the program resumes with accurate, fair caps for all participants.

---

## Budget Impact

The pause period represents a budget saving of approximately **51.2M TEL**. This amendment does not propose reimbursing or retroactively distributing rewards for the paused weeks. The zero-distribution bridge is a technical continuity mechanism only; it carries no cost.

Going forward, the weekly allocation of **3,205,128.205 TEL per week** resumes as defined in TANIP-1.

---

## Implementation Timeline

| Step | Description |
|---|---|
| Amendment approval | Governance vote to ratify this approach |
| Zero-distribution bridge | Insert bridging periods to bring contract up to date |
| Resumption | Begin live weekly distributions |

Target relaunch: **within 2 weeks of amendment approval.**

---

## Amendment Scope

This amendment changes **only** the mechanism used to resume the program after the pause. No changes are made to:

- The rebate formula
- The weekly allocation amount
- Eligibility rules
- Referee reward structure
- The stake cap or fee cap logic

All other terms of TANIP-1 remain in full effect.

---

## References

- [TANIP-1: Trading Fee Rebate Program](https://forum.telcoin.org/t/tanip-trading-fee-rebate-program/824)
- [Snapshot vote — TANIP-1 ratification](https://snapshot.org/#/s:telcointancouncil.eth/proposal/0xe8557885f5cade3a008e720e0507c272f13b9a6bdb6a52920dadc39269aa754e)
