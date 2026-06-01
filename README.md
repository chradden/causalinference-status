# Dataset Characteristics

**Notebooks:** [`exploratory_data_analysis.ipynb`](exploratory_data_analysis.ipynb) — open on
GitHub (native render), or use [nbviewer.org](https://nbviewer.org) on the raw GitHub URL if
GitHub's preview fails. An offline HTML copy
([`exploratory_data_analysis.html`](exploratory_data_analysis.html)) is included for browser viewing.

## Dataset Information

### Dataset Source
- **Dataset Link:** [`../data/recs2020_processed.csv`](../data/recs2020_processed.csv) — processed extract of the **U.S. EIA Residential Energy Consumption Survey 2020**; produced by [`../data/load_recs.py`](../data/load_recs.py). Raw source: [eia.gov](https://www.eia.gov/consumption/residential/data/2020/) (public domain).
- **Dataset Owner/Contact:** U.S. Energy Information Administration (public-domain survey).

### Dataset Characteristics
- **Number of Observations:** **17,196 U.S. households** (cross-sectional; one record per household, calendar year 2020)
- **Number of Features:** 11 columns (1 id, 1 treatment, 1 outcome, 8 covariates) extracted from the full 789-variable RECS file
- **National scope:** representative of all U.S. residential occupied housing units (sampling weights available in the raw file; not used in this baseline analysis but a natural future extension)

### Target Variable/Label
- **Label Name:** `energy_intensity_kwh_m2`
- **Label Type:** Regression (continuous); the *estimand* is a causal treatment effect, not a prediction
- **Label Description:** annual total household energy use (all fuels) per m² of conditioned floor area
- **Label Values:** continuous, roughly 30–500 kWh/m²·a (mean ≈ 150)
- **Label Distribution:** right-skewed; highest in Cold/Very-Cold climate zones

### Feature Description
- **Treatment — `efficient_windows`** (binary): 1 = double/triple-pane, 0 = single-pane (from RECS `TYPEGLASS`). Window replacement is a canonical retrofit measure.
- **Confounders / effect modifiers**:
  - `building_age`, `year_built` — newer homes tend to have efficient windows AND lower intensity (heavy confounding)
  - `floor_area_m2` — larger homes ≠ random sample
  - `climate_zone`, `cold_climate` — efficient windows much more common in cold zones; energy use too
  - `housing_type` — single-family vs apartment vs mobile home: different intervention exposure and consumption
  - `household_size`, `income_bin` — demographics correlated with both retrofit adoption and consumption

## Exploratory Data Analysis

Conducted in [`exploratory_data_analysis.ipynb`](exploratory_data_analysis.ipynb):

- **Dataset overview** — `info()`, `describe()`, head
- **Missing values** — none after ETL (raw missing handled in `load_recs.py`)
- **Outcome distribution** — right-skewed, mean ≈ 150 kWh/m²·a
- **Treatment balance** — ~11,700 with efficient windows vs ~5,500 with single-pane (good overlap)
- **Feature distributions** — energy intensity by climate zone (boxplot), by housing type (boxplot), and the building-age / floor-area distributions
- **Correlations** — numeric correlation heatmap
- **The confounding picture** — three-panel figure showing (i) the naive treatment contrast, (ii) the share of efficient windows by climate zone, (iii) by building-age band — making vivid why naive comparison overstates the effect
- **Insights** — efficient-window share **doubles** from older to newer buildings and is strongly tied to climate → these confounders must be adjusted for
