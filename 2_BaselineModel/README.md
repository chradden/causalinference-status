# Baseline Model

**Notebooks:** [`baseline_model.ipynb`](baseline_model.ipynb) — open on GitHub (native render),
or use [nbviewer.org](https://nbviewer.org) on the raw GitHub URL if GitHub's preview fails.
An offline HTML copy ([`baseline_model.html`](baseline_model.html)) is included for browser viewing.

## Baseline Model Results

### Model Selection
- **Baseline Model Type:** Ordinary Least Squares (OLS) linear regression — two variants: (A) univariate (treatment only); (B) multivariate (treatment + all observed covariates).
- **Rationale:** OLS is the simplest, most interpretable model and exactly the "correlation" reasoning the causal ML must improve upon. It makes both the magnitude of confounding *and* the limits of linear adjustment visible.

### Model Performance
| | Treatment coefficient | Reading |
|---|---|---|
| **Model A — univariate OLS** | **−12.14** kWh/m²·a | naive contrast; looks like a big saving |
| **Model B — multivariate OLS** | **−4.16** kWh/m²·a, p < 0.001 | shrinks ~3× after linear adjustment for size/age/climate/type/HH/income |
| Predictive R² (Model B, 5-fold CV) | **0.28 ± 0.02** | |

### Evaluation Methodology
- **Data Split:** 5-fold cross-validation for predictive R²; full-sample OLS for coefficient inference.
- **Evaluation Metrics:**
  - **Treatment coefficient** (the causal quantity of interest) — sign, magnitude, p-value
  - **R²** (predictive adequacy) — secondary

### Metric Practical Relevance
The treatment coefficient is the headline number for an energy manager: *"installing efficient
windows changes annual energy intensity by X kWh/m²·a"*. The huge gap between Model A (−12) and
Model B (−4) is the first warning: most of the apparent saving was confounding, not causation.

But even Model B has limits — it imposes (i) a linear functional form and (ii) a single constant
effect for every household. Whether a flexible non-linear ML adjustment will shrink the effect
further, and which subgroups actually benefit, is the open question the next step addresses.

## Next Steps
The [3_Model](../3_Model/README.md) section describes the planned **Double Machine Learning**
(LinearDML) + **Causal Forest** workflow. The full implementation and the resulting ATE / CATE
are presented in the **final session**.
