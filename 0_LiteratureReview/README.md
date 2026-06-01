# Literature Review

Approaches and solutions that have been tried before on similar problems — estimating the *causal*
effect of energy-efficiency interventions on building/household energy consumption, and the
*heterogeneity* of that effect.

**Summary of Each Work**:

- **Source 1**: Fowlie, Greenstone & Wolfram (2018), *Do Energy Efficiency Investments Deliver?
  Evidence from the Weatherization Assistance Program*, **Quarterly Journal of Economics** 133(3).

  - **[Link](https://doi.org/10.1093/qje/qjy005)**
  - **Objective**: Causally measure realised energy savings of the largest US residential retrofit program.
  - **Methods**: Randomised controlled trial, ~30,000 households; compares realised vs engineering-projected savings.
  - **Outcome**: Upfront costs ≈ 2× realised savings; engineering models over-predicted savings by ~2.5–3×.
  - **Relation to the Project**: The cautionary benchmark — *projected ≠ realised* savings; motivates estimating effects from data and targeting high-return buildings.

- **Source 2**: Knittel & Stolper (2021), *Machine Learning about Treatment Effect Heterogeneity:
  The Case of Household Energy Use*, **AEA Papers and Proceedings** 111.

  - **[Link](https://doi.org/10.1257/pandp.20211090)**
  - **Objective**: Map heterogeneity in household response to energy-feedback reports.
  - **Methods**: **Causal forests** on a Home Energy Report RCT.
  - **Outcome**: Mean −9 kWh/month but a wide range (−40 to +10); baseline use and home value most predictive.
  - **Relation to the Project**: The closest methodological template — causal forests for heterogeneity + targeting, exactly my portfolio-prioritisation goal.

- **Source 3**: Burlig, Knittel, Rapson, Reguant & Wolfram (2020), *Machine Learning from Schools
  about Energy Efficiency*, **JAERE** 7(6).

  - **[Link](https://doi.org/10.1086/710606)**
  - **Objective**: Estimate realised retrofit savings in California K-12 schools.
  - **Methods**: ML on high-frequency smart-meter panel data to build counterfactual baselines.
  - **Outcome**: Realised savings well below projections; ML improves prediction-based counterfactuals.
  - **Relation to the Project**: The most direct analogue — **non-residential building** retrofits + meter data + ML, matching a building-portfolio setting.

- **Source 4**: Wager & Athey (2018), *Estimation and Inference of Heterogeneous Treatment Effects
  Using Random Forests*, **JASA** 113(523).

  - **[Link](https://doi.org/10.1080/01621459.2017.1319839)**
  - **Objective / Methods**: Introduces **causal forests** with asymptotic normality and valid pointwise confidence intervals for CATEs under unconfoundedness.
  - **Outcome**: Consistent, inferentially valid heterogeneous-effect estimation.
  - **Relation to the Project**: The core estimator used in `3_Model` for portfolio-level CATE.

- **Source 5**: Chernozhukov et al. (2018), *Double/Debiased Machine Learning for Treatment and
  Structural Parameters*, **Econometrics Journal** 21(1).

  - **[Link](https://doi.org/10.1111/ectj.12097)**
  - **Objective / Methods**: Neyman-orthogonal scores + cross-fitting to remove ML regularisation bias.
  - **Outcome**: √n-consistent, valid treatment-effect estimates with many covariates.
  - **Relation to the Project**: Underpins the DML residualisation that removes building-age confounding.

- **Source 6**: Miller et al. (2020), *The Building Data Genome Project 2*, **Scientific Data** 7:368.

  - **[Link](https://doi.org/10.1038/s41597-020-00712-x)**
  - **Objective / Methods**: Open dataset — 3,053 meters / 1,636 non-residential buildings, hourly, with type/area/climate metadata.
  - **Outcome**: Benchmark dataset for building energy prediction and measurement & verification.
  - **Relation to the Project**: The real, openly-licensed (CC BY 4.0) dataset I will use to validate the synthetic results.

**Further references** (methods & context): Nie & Wager (2021, R-learner, Biometrika); Künzel et al.
(2019, metalearners, PNAS); Allcott (2011, OPower RCT, J Public Econ); Christensen et al. (2023,
projected-vs-realised wedge, REStat); Prest (2020, causal ML on TOU pricing, JAERE).
