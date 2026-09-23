# Research protocol — 23 September 2026

## Question retained after literature screening
When a shared noisy evaluator preserves quality rankings but tool prices enter the objective outside the noise channel, what is the price of learning its unknown scale?

Model: stochastic Bernoulli arm quality, known execution prices, common independent symmetric bit-flip feedback with unknown reliability gamma in [gamma0,1], optional chosen-arm truth audit at price a. All observations arrive after the action. Auditing does not repair the executed action. Audit decisions precede the current feedback.

Proposed contributions to verify before submission:
1. Exact no-audit identification geometry from the proxy means and price envelope.
2. General-K upper bound separating ordinary arm learning from shared calibration.
3. Two-arm lower bounds for a hard audit budget and audit-priced regret, with explicit dependence on price spread D. Match up to logarithms for gamma0=1/4 and D<=1/4.
4. A nonasymptotic certificate for when calibration precision is decision sufficient, and limitations under channel misspecification.

## Experimental plan (fixed before simulation outputs)
- Algebraic checks of indistinguishable environments, joint observation distributions, price-gap identities and KL bounds. Exact rational checks where possible, numerical grid checks clearly labeled numerical.
- Synthetic finite-arm experiments with independent seeds and retained per-seed outputs. These test the mathematical mechanism, not real-world LLM performance.
- Budget sweep to separate policy regret from audit expenditure; price-spread sweep; horizon sweep on both members of the indistinguishable family; stress tests for asymmetric or action-dependent noise.
- Baselines: oracle-channel UCB (information advantage), naive proxy-minus-price UCB, rank-only UCB, audit-only explore-then-commit at the same audit budget, and a separately budgeted audit-only comparator.
- No model API experiment is required by the theory. Do not spend API funds merely to decorate a theoretical paper.
- Primary comparisons use 256 independent seeds. Report Monte Carlo standard errors, not unearned real-world generalization claims. Retain unfavorable results and channel-violation results.

## Scope
No guarantee of priority, patentability or acceptance. Generic noisy feedback, UCB, paid labels, and T^(2/3) costly-feedback rates are established. Claim only the cost-spread-sensitive calibration separation and associated identification geometry after checking closest sources. No human-data collection is involved; the scientific contribution is mathematical.

## Artifacts
All new work remains inside this dedicated directory except the requested named PDF in the research root. Prior projects are read-only. Credentials are neither written to the repository nor included in artifacts. The author copy and anonymous ALT submission copy are distinct; public code must not be linked in the anonymous submission if it identifies the author.

## Implementation amendments recorded during verification
- The sixth baseline is audit-all UCB, which pays for every true reward. The planned separately budgeted audit-only comparator was not implemented. Audit-only ETC uses exactly the same budget as SC-UCB; the paper makes no claim to exhaustive baseline coverage.
- The no-audit geometry was strengthened to an exact endpoint linear-program characterization during proof development. Tests cover the closed-form two-arm case and a numerical multi-arm check.
- Verification found that the diagnostic `final_scale` field described the last decision's estimate before a possible final audit. It now records the estimate after the final update, and the suite was rerun. Action decisions, regrets, audit counts, and the parameter grid were unchanged. The reference replay check now includes full-horizon audits.
