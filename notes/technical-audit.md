# Technical verification record

This record describes internal checks. It is not an independent peer review, a formal proof-assistant certificate, or an acceptance prediction.

## Proof obligations checked

1. **Identification.** For supplied proxy means, feasibility of every latent Bernoulli mean gives `g >= max_i |2 lambda_i - 1|`. A no-audit transcript has the same law at every compatible scale. Its average mixture is scale-independent. Regret is convex in `1/g`, so only endpoint constraints are needed. Zero regret requires a common endpoint maximizer; mixtures cannot cancel positive regret. The two-arm closed form follows by balancing the two endpoint losses.
2. **Upper bound.** Per-arm Hoeffding bounds hold simultaneously over sample counts. Agreement has range length two and common mean gamma, including when selected actions are adaptive. No independence between these two estimators is used. The per-step scaled regret is at most the selected arm's twice-radius plus `D` times scale error. Summing radii gives `2 sqrt(2 K T L)`. Prefix calibration gives the stated `S_n`; initialization and the failure event are charged explicitly.
3. **Budget lower bound.** The hard pair has exactly the same proxy means, opposite optimal actions, and valid latent means. An audited pair is equivalent to independent success and agreement variables. The Bernoulli KL bounds sum to `71936/4875 < 16` times `h^2`. The adaptive transcript chain rule charges only audited rounds. Pinsker and testing yield `D T/(20 sqrt(B+1))` for every policy satisfying the uniform expected-budget constraint.
4. **Ordinary exploration lower bound.** At gamma=1 audits reveal no additional information. The two nearby success means give KL at most `1/7`, even for adaptive actions, and regret at least `sqrt(T)/64`. Combining lower bounds uses `max(x,y) >= (x+y)/2`; it does not incorrectly assume their hard instances coincide.
5. **Paid lower bound.** For each candidate policy, either expected audits exceed `1/(32 h^2)` or the testing lower bound applies. Selecting the clipped cube-root `h` gives the stated minimum. The argument includes adaptive/random audit schedules. The upper bound compares zero audits with the clipped prefix budget and handles the full-horizon, zero-price, and zero-spread boundaries.
6. **Decision certificate.** Pairwise score gaps are affine in scale. The proxy confidence-box worst case is explicit. The margin statement accounts for both proxy error and the distance from true scale to either confidence endpoint.
7. **Misspecification.** Proxy-mean bias is at most epsilon; signed-agreement conditional bias is at most twice epsilon. Martingale Hoeffding handles the adaptively selected arm. Two bias contributions yield the additional `2(1+D) epsilon T/gamma0` term. This is an algorithmic upper bound, not a universal impossibility result.

The main sharpness claim concerns two arms, a fixed reliability floor, and `D <= 1/4`. A matching general-K lower bound, optimal gamma0 dependence, contextual generalization, and an optimal adaptive audit trigger are not proved.

## Executed computational checks

- 33 automated tests: exact rational hard-pair identities, Bernoulli joint-law normalization/expectations, KL checks, confidence certificate checks, LP endpoint reduction, interface access restrictions, and online/reference simulator agreement.
- The replay comparison covers audit budgets 0, 1, 37, 299, and 300 at a 300-round horizon. This includes a final-round audit.
- `scripts/verify_results.py` independently reads all retained rows and checks unique keys, nonnegative execution regret, per-method audit budgets, total-cost accounting, group sizes, reported means/standard errors, and the raw-data SHA-256 digest.
- It evaluates 12,500 audited-law KL comparisons on a grid, independently of the package's joint-law and KL functions, and checks the conservative KL constant with rational arithmetic.
- Grid checks are numerical diagnostics. The analytic arguments in the paper establish claims between grid points.

## Experimental interpretation

The experiment grid was specified before its outcome was inspected. The protocol records implementation amendments separately. The study includes 46 parameter configurations, 272 method/configuration comparisons, 256 seeds in each comparison, 69,632 policy/environment/seed runs, and three saved checkpoints per run. Reused seeds create cross-comparison dependence; they are not counted as independent replications of a pooled test.

The fixed-gap experiment is not evidence for the asymptotic minimax exponent. The action-count sweep also changes utility gaps. The zero-spread point in the paired family has equal-quality actions, so its zero regret is not evidence that every equal-price problem is trivial. The oracle has an information advantage. The misspecification suite deliberately violates the shared-channel model.

The strongest practical baseline in several fixed instances is same-budget audit-only ETC. This result is reported in the main table and text. No hyperparameter search was used to replace unfavorable outcomes.

## Submission format

The author manuscript identifies Shivam Gupta as an independent researcher. The submission manuscript uses the official ALT 2027 anonymous class option, removes identifying metadata and repository links, and includes executable reference code. All principal theorem statements and their proofs occur before the end of the first 12 non-reference pages. The complete source and experiment release are public separately; no unprovided supplementary upload is asserted.
