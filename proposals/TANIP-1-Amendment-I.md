# TANIP-1 Amendment I: Zero-Distribution Period Bridge

**Status:** Draft  
**Type:** Amendment  
**Amends:** [TANIP-1 — Trading Fee Rebate Program](https://forum.telcoin.org/t/tanip-trading-fee-rebate-program/824)  
**Date:** April 2026

---

## Context

TANIP-1 was paused for approximately 16 weeks. The on-chain calculator contract tracks cumulative user balances across sequential weekly periods. To resume, the contract's period index must be brought up to date before live distributions can continue.

## Change

Rather than redeploying new contracts — which would erase users' `total_earned` histories — the program will resume using the **existing contracts**. The paused weeks will be bridged by submitting one or more **periods with zero distributions**, advancing the contract's internal period index to the present without crediting any rewards or altering any user balances.

This was tested end-to-end and confirmed:

1. The smart contract accepts zero-value period inputs without reverting or corrupting state.
2. The off-chain distribution script handles zero-value data correctly, producing no payouts and no errors.
3. Subsequent live distribution periods process correctly after the bridge.

## Effect on the Calculation

No change to the formula defined in TANIP-1. Zero-distribution periods contribute `0` to `R` for all users, so `previously_earned` balances are unaffected. The stake cap resumes correctly from each user's existing history.

## Budget

The paused weeks are not retroactively distributed. The ~51.2M TEL saved during the pause (16 weeks × 3,205,128.205 TEL) is not reallocated by this amendment.

## All Other Terms

All other terms of TANIP-1 remain unchanged. Target relaunch is within 2 weeks of this amendment passing.
