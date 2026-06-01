# Model Definition and Evaluation — *Planned* (final-session deliverable)

> The implemented notebook is reserved for the **final presentation**. This page describes the
> *planned* methodology so that anyone reading this status repo understands what comes next.

## Model Selection (planned)
Two Double Machine Learning estimators from `econml`:
- **`LinearDML`** for the constant **ATE** (most stable estimator for a binary treatment + continuous outcome). Cross-fits a random-forest regressor for `model_y` and a random-forest classifier for `model_t`, then estimates a single average treatment effect.
- **`CausalForestDML`** for the **CATE** (per-household effect τ(X)). Tuned to be smooth: 500 trees, `min_samples_leaf=200`, `max_depth=8`.

### Why Double ML
Robinson's transformation residualises Y and T on the covariates with flexible ML (random forests) —
removing the *non-linear* confounding that the OLS baseline cannot. Cross-fitting prevents the
nuisance models from over-fitting their own data. The estimator is doubly robust and delivers
√n-consistent ATE estimates with valid confidence intervals (Chernozhukov et al. 2018; Wager & Athey 2018; Nie & Wager 2021).

## Feature Engineering
- **Treatment T:** `efficient_windows` (binary).
- **Covariates X:** building age, floor area, climate zone (8 IECC categories → integer code), housing type (5 categories → integer code), household size, income bin.
- **No collider** in this dataset → all listed X are confounders to adjust for.
- Missing values handled in the ETL ([`../data/load_recs.py`](../data/load_recs.py)).

## DAG (structural causal model)

```
   Age ──┐
   Area ──┤
Climate ──┼─► Efficient_Windows ──► Energy_Intensity
   Type ──┤                              ▲
 Income ──┘                              │
        └───────────────────────────────┘
```

Building age, floor area, climate zone, housing type and income all influence **both** the
probability of having efficient windows *and* the energy intensity. That is exactly the back-door
structure Double ML blocks.

## Hyperparameters (planned)
- Nuisance models: `RandomForestRegressor` for `model_y`, `RandomForestClassifier` for `model_t`; `n_estimators=200–300`, `min_samples_leaf=20`.
- Cross-fitting: `cv=5`.
- Causal forest: `n_estimators=500`, `min_samples_leaf=200`, `max_depth=8`.

## What to expect in the final session
1. **ATE from LinearDML** with a 95 % confidence interval — directly comparable to the
   OLS-adjusted baseline of −4.2 kWh/m²·a.
2. **CATE heatmap** by climate × housing type — the actionable targeting view.
3. **Distribution of individual effects** — how heterogeneous the response actually is.
4. **Comparative table** Naive → Adjusted OLS → DML → Causal Forest.
5. **Targeting recommendation** for the energy-manager use case.
6. **Limitations and sensitivity** (E-value), and replication ideas (Smart Meters in London dToU
   trial as a genuine RCT).
