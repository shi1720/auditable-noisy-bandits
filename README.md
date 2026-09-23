# When Rankings Are Not Enough

**Cost-Sensitive Bandits with Auditable Noisy Feedback**  
Shivam Gupta · Research manuscript · September 2026

A reliable quality ranking need not identify the best tool after execution prices are deducted. This repository studies that distinction in a stochastic Bernoulli bandit with a shared, unknown symmetric feedback channel and optional trusted audits.

The manuscript proves an exact no-audit minimax characterization and matching two-arm regret bounds up to logarithmic factors. The dependence on execution-price spread is the central result; UCB, costly observations, and the generic cube-root rate are established ideas.

For horizon `T`, price spread `D <= 1/4`, reliability at least `1/4`, and expected audit budget `B`, the minimax execution regret is, up to logarithms,

```
sqrt(T) + D*T/sqrt(B+1).
```

At audit price `a in [0,1]`, execution regret plus audit expenditure has minimax rate

```
sqrt(T) + min(D*T, (a*D**2)**(1/3) * T**(2/3)).
```

These are mathematical results for the specified model, not measured guarantees for a deployed language-model evaluator. The manuscript has not been peer reviewed or accepted.

## Paper and contents

- [Author manuscript](output/pdf/when-rankings-are-not-enough.pdf)
- [Anonymous manuscript](output/pdf/when-rankings-are-not-enough-anonymous.pdf)
- `src/auditband/`: readable online policy, model, endpoint certificate, ambiguity LP.
- `scripts/`: simulator, figure generation, independent result verification, PDF build.
- `results/runs.csv`: all 208,896 checkpoint rows from 69,632 policy-environment-seed runs.
- `results/summary.csv`: means and Monte Carlo standard errors for 272 comparisons.
- `results/experiment-manifest.json`: all configurations, seeds, runtime, raw-data hash.
- `figures/`: six vector figures and preview images, regenerated from the analysis script.
- `notes/literature-review.md`: closest prior work and bounded novelty assessment.
- `notes/technical-audit.md`: proof obligations, verification scope, and limitations.
- `paper/`: complete LaTeX sources in the official ALT 2027 style.

## Reproduce

The recorded environment is Python 3.9.6, NumPy 2.0.2, and Numba 0.60.0 on macOS ARM64. The lockfile targets Python 3.9; use that interpreter for an exact reproduction. A CPU is sufficient. No model API, credentials, GPU, or downloaded dataset is required.

```bash
python3.9 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-lock.txt
python -m pip install -e . --no-deps
python -m pytest -q
python scripts/run_experiments.py
python scripts/analyze.py
python scripts/verify_results.py
python scripts/build_paper.py
```

The simulator takes roughly half a minute on the development machine; runtime varies by platform. `run_experiments.py` intentionally overwrites generated results. It records three checkpoints per run and a final, post-update channel estimate; the latter is repeated on the checkpoint rows and is not an intermediate-round estimate. Seeds are paired across methods and reused across configurations. There are 256 independent seeds **within each comparison**, not 69,632 independent units for a pooled significance test. Shaded bands show 1.96 Monte Carlo standard errors; the paper's table reports one standard error.

The paper builder requires Tectonic (tested with version 0.17.0) or a separately configured LaTeX toolchain. Tectonic downloads its TeX support files on first use. The official template files are retained with their original notices. The Python package does not depend on LaTeX.

## Use the online interface

```python
from auditband import ScaleUCB

policy = ScaleUCB(costs=[0.0, 0.2], horizon=8192, audit_budget=407)
arm, audit = policy.choose()
# Execute this arm, observe its binary proxy, and obtain truth only if audit.
policy.update(proxy=1, truth=1 if audit else None)
```

`choose()` must precede `update()`. The interface rejects supplied truth on unaudited rounds and prevents advancing before feedback arrives. Prices and success probabilities must use the same utility units. The theoretical audit request precedes the current proxy observation.

```python
from auditband import ambiguity_lp, robust_winners

mixture, residual_regret = ambiguity_lp([0.5, 0.6], [0.0, 0.2])
assert abs(residual_regret - 1/15) < 1e-10
assert robust_winners([0.5, 0.6], [0.0, 0.2], (0.25, 1.0)) == []
assert robust_winners([0.5, 0.6], [0.0, 0.2], (0.60, 1.0)) == [0]
```

The LP uses floating-point optimization; it is not a machine-checked mathematical proof. The certificate checks a rectangular confidence region and can be conservative.

## Results and limits

At `T=32768`, the calibrated method incurs total regret about 607 and 477 in the two indistinguishable-proxy worlds. Same-budget audit-only explore-then-commit incurs about 286 and 400. These unfavorable comparisons are retained. The proposed policy is proof-oriented and is not claimed to dominate practical routing algorithms on fixed instances.

The model assumes a stationary shared symmetric channel, correct trusted audits, known fixed action prices, and fresh draws. The paper bounds controlled channel deviations but does not establish robustness to arbitrary evaluators. Potential applications include automated tool selection and reliability monitoring when those assumptions can be justified. Production savings and patentability have not been demonstrated.

## Citation and licensing

Use `CITATION.cff` to cite the research manuscript; do not cite it as an accepted ALT paper. Original code is MIT licensed. The manuscript and original figures are copyright Shivam Gupta, 2026; their inclusion here permits access and reproduction of the research, without assigning copyright. Third-party template files retain their existing license notices.
