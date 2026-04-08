# TEL Issuance at the Application Layer - Stakers: Transition to a Trading Fee Rebate Program

**Submitted by:** TAN Council  
**Date:** 12.8.2025

---

This proposal is based on the recently completed TANIP-1 findings report and presents a refined path forward for application layer incentives across the Telcoin ecosystem. With TANIP-1 paused and the data now fully analyzed, the Council is proposing a shift from issuance-based rewards to a more sustainable rebate-based model that continues to incentivize real activity while removing misaligned incentives observed during the program.

## Overview

TANIP-1 successfully implemented the unified staking model for stakers and demonstrated that issuance can be distributed based on verified on chain behaviour within the Telcoin Platform. Weekly distributions of 3.2M TEL worked reliably, the computation framework performed as intended, and the data was transparent and auditable.

The findings showed, however, that most of the fee activity during TANIP-1 came from short term participants responding directly to issuance. Weekly fees converged around the issuance amount and dropped sharply once the program was paused. Wallet activity remained mostly flat. Referral activity often became circular. These indicators suggest that the program attracted mercenary capital more than long term users of TAN applications.

This proposal introduces a Trading Fee Rebate Program that keeps the core mechanics of TANIP-1 intact while removing the incentive for fee cycling. The goal is to continue rewarding genuine network participation in a way that is sustainable for the current stage of TAN's development.

## Context

TANIP-1 was launched to operationalize user ownership at the application layer. It activated the Stakers miner group, implemented transparent issuance logic, and allowed participants to earn TEL through their own on chain activity and the activity of their referees.

The findings report highlighted key behaviours:

- Fees rose until they matched issuance levels
- Fees dropped immediately when issuance paused
- Weekly active wallet counts remained mostly unchanged
- New wallets followed a churn pattern rather than cumulative growth
- Referral flows often became self-referential

These patterns show that the system worked mechanically, but the economic incentives encouraged fee rotation instead of organic use.

A rebate model preserves the positive aspects of TANIP-1 while aligning incentives more closely with genuine behaviour.

## Proposal: Trading Fee Rebate Program

This proposal aims to replace issuance-based rewards with a capped rebate system that uses the same TANIP-1 architecture and logic but limits rewards to the amount of TEL each wallet actually paid in fees during each period.

### Program Structure

The following elements remain unchanged:

- Stake requirement through the StakingModule
- Referral tree logic
- On chain fee verification through aggregator-to-AmirX transfers
- Deterministic off chain calculation
- Weekly batched uploads to TANIssuanceHistory
- Network-agnostic design that future developers can adopt

The only modification is the introduction of a rebate cap.

### Rebate Formula

```
R = calculated issuance from own and referee fees
    (following same calculation as original TANIP-1 implementation)

F = total TEL fees paid by the wallet during the period

Final rebate = min(R, F)
```

**Meaning:**

If the calculated rebate exceeds the wallet's fee spending, the wallet receives back the amount it paid in fees.

If the calculated rebate is lower than the wallet's fee spending, the wallet receives the full rebate.

This ensures no participant can earn more TEL than they spend, removing the main driver of mercenary volume.

## Governance, Funding and Transparency

The rebate program will be:

- Funded by the existing TAN Council Safe
- Distributed weekly through the existing TANIssuanceHistory contract
- Transparent, auditable, and consistent with past processes
- Fully controlled by the TAN Council with no reliance on app updates

This structure makes the program predictable for users and developers while safeguarding treasury resources.

## Next Steps and Council Role

If approved, the Council will:

- Engage the TAO to make the required changes to the TANIP-1 rewards calculation script
- Activate the rebate program
- Maintain weekly reward uploads
- Track participation trends under the new model
- Review program performance as TAN scales
- Evaluate the potential return to the original issuance model once network maturity increases

No new integrations or technical changes are required for stakers.

## Clarification on Scope

This proposal focuses on the single change of replacing issuance with a capped rebate. It does not alter:

- Referral logic
- Staking logic
- Reward computation methods
- Eligibility rules
- Developer onboarding requirements

Any future updates or enhancements would be submitted through separate proposals.

## Benefits

- Rewards genuine activity instead of fee cycling
- Preserves all existing TANIP-1 infrastructure
- Protects treasury resources
- Removes mercenary incentives
- Scales cleanly with the network
- Keeps TAN's ecosystem user-owned and transparent
- Provides a better foundation for future issuance programs

## Implementation

The TAN Council will work with Telcoin Autonomous Ops LTD. (TAO) to:

Update the TAN issuance off chain script, migrating to the rebate system described above.

The existing `TANIssuanceHistory` contract will be reused, preserving each wallet's full issuance history from the original TANIP-1 implementation. To bring the contract's period index up to date following the pause, one or more periods with zero distributions will be submitted, covering the weeks in which the program was inactive. This advances the contract state without crediting any rewards or altering any accumulated balances.

This approach was tested end-to-end prior to this proposal. The contract accepts zero-value period inputs without error, the off chain script handles them correctly, and subsequent live distribution periods process accurately after the bridge.

## Conclusion

TANIP-1 proved the model and gave the ecosystem valuable data. The rebate program is the logical next step. It maintains user incentives, improves fairness, and positions TAN for sustainable adoption as more developers and users join the network.

The Council invites the community to support this proposal and move TAN application layer incentives into their next phase.
