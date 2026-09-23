# Literature and contribution audit

Search and primary-source inspection date: 23 September 2026. This is a documented literature screen, not a proof of worldwide priority or an exhaustive patent search.

## Question

For Bernoulli action quality, known prices outside a shared unknown symmetric observation channel, and optional chosen-action truth audits, what regret is forced specifically by uncertainty about the channel scale? How does that extra regret vanish as the execution-price spread goes to zero?

## Closest comparisons

| Primary source | Established result or model | Distinction in this manuscript |
|---|---|---|
| [Resler and Mansour, ICML 2019](https://proceedings.mlr.press/v97/resler19a.html) | Online binary learning under noisy feedback; constant symmetric noise can be unknown. | Correct ranking suffices for unpriced rewards. Known prices outside the corruption channel make its unknown scale decision-relevant. |
| [Gajane, Urvoy, and Kaufmann, ALT 2018](https://proceedings.mlr.press/v83/gajane18a.html) | Stochastic bandits with known corruption functions, motivated by local privacy. | The correction scale here is unknown and must be learned through optional audits. |
| [Tucker et al., UAI 2023](https://proceedings.mlr.press/v216/tucker23a.html) | Costly reward observations; cube-root observation-cost dependence and a two-thirds horizon exponent. | The generic exponent is prior work. Free ranking-preserving observations here remain available, and the added difficulty vanishes with execution-price spread. |
| [Schur, Lago, and Fiez, UAI 2026](https://proceedings.mlr.press/v337/schur26a.html) | Costly bandits with heterogeneous observation costs and correlations. | Their observation-cost structure is different from an unknown shared proxy channel plus execution prices. Our bounds isolate shared calibration rather than replacing their general costly-bandit results. |
| [Reyzin, Saha, and Wu, UAI 2026](https://proceedings.mlr.press/v337/reyzin26a.html) | Expert advice with costly observations. | The feedback and comparator differ; this is stochastic chosen-arm learning with free corrupted outcomes and paid truth. |
| [Ghasemi and Crowley, 2026, v2](https://arxiv.org/abs/2603.13356v2) | Sparse trusted audits, contextual evaluator trust, and unidentifiability from unaudited feedback. | Audits and indistinguishability are already studied. Here every evaluator response is positively informative and ranking preserving; the obstruction is the scalar conversion between quality differences and prices. |
| [Natarajan et al., JMLR 18(155)](https://jmlr.org/papers/v18/15-226.html) | Cost-sensitive supervised learning with noisy labels. | Different statistical target and feedback protocol. Here the objective is cumulative sequential regret plus optional audit expenditure. The official JMLR page gives 2018; the bibliography follows that page. |
| [Ji et al., 2026, v2](https://arxiv.org/abs/2506.16658v2) | Bandits with ML-generated surrogate rewards and true/surrogate observations during online learning. | In this manuscript true outcomes are unavailable unless an audit is purchased. |
| [Sridhar et al., 2026, v1](https://arxiv.org/html/2607.09015v1) | Cost-aware contextual LLM routing, chosen-arm true rewards, and surrogate feedback for graph-selected arms. Section 3 and the algorithm observe the chosen arm's true reward each round. | The proposed problem removes automatic access to that reward and prices its acquisition. This manuscript does not claim to introduce surrogate-based LLM routing. |
| [Angelopoulos et al., Science 2023](https://arxiv.org/abs/2301.09633) | Prediction-powered inference combines predictions and trusted outcomes. | Valid inference and the use of trusted labels are established. Our target is a regret/audit frontier in a shared-channel bandit model. |
| [Saha, Bhat, and Luo, 2026](https://arxiv.org/abs/2602.14474) | Source selection with heterogeneous unknown noise variances. | Estimating variance to select an informative source differs from recovering an unknown mean scale to compare quality against known prices. Screened; not needed in the manuscript's central comparison. |
| [Bartok et al., 2014](https://doi.org/10.1287/moor.2014.0663) | Partial-monitoring classifications and regret algorithms. | Information-bearing versus uninformative actions and testing-based lower bounds belong to established theory. Our model and price-sensitive construction are a specialization. |

Foundational techniques are attributed to [Auer, Cesa-Bianchi, and Fischer (2002)](https://doi.org/10.1023/A:1013689704352) for UCB and [Lattimore and Szepesvari (2020)](https://tor-lattimore.com/downloads/book/book.pdf) for standard bandit information inequalities. No new concentration inequality is claimed.

## Search record

Search families included noisy/corrupted bandits; unknown symmetric noise; costly reward observations; surrogate rewards; paid verification; contextual trust and audits; tool/model routing with quality and execution cost; partial monitoring; and heteroscedastic feedback. A final targeted screen used:

- `bandits unknown common noise rate action costs costly audits calibration`
- `bandits noisy feedback unknown scale heterogeneous execution costs regret`
- `"bandits" "calibration" "audits" "cost" regret`
- `"bandits" "unknown corruption" "cost" symmetric noise`
- `"bandits" "unknown" "symmetric noise" cost`
- `"bandits" "calibration" "price spread"`
- `"bandits" "shared" "costly" "surrogate"`

Publisher pages, proceedings PDFs, and versioned author preprints were used to verify central comparisons. Search snippets and third-party summaries were treated as discovery aids, not sufficient evidence for a claim. The closest model sections and relevant lower-bound statements were read, rather than relying only on paper titles.

## Retained contribution and limits

The screened sources did not supply the same price-spread-dependent frontier for this shared symmetric-channel audit protocol or its exact endpoint ambiguity LP. That supports investigating and submitting this specific result; it does not establish an absolute first-ever claim. The paper therefore uses explicit comparative statements and avoids claims of unprecedented audits, surrogate feedback, UCB, or a new two-thirds exponent.

The contribution is a focused theoretical characterization, not an industry-defining empirical breakthrough. Its commercial motivation is selective verification and priced tool choice under an applicable statistical model. Patentability, deployment savings, and superiority to current production routing methods remain unestablished.
