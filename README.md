# Data

## Dataset used in this project

**U.S. EIA Residential Energy Consumption Survey 2020** — a nationally representative public-domain
survey of ~18,500 U.S. households by the [Energy Information Administration](https://www.eia.gov/consumption/residential/data/2020/),
with detailed building characteristics, energy use by fuel and end use, and demographics.

| | |
|---|---|
| **Source** | https://www.eia.gov/consumption/residential/data/2020/ |
| **Raw download** | [`recs2020_public_v5.csv`](https://www.eia.gov/consumption/residential/data/2020/csv/recs2020_public_v5.csv) — 53 MB, public domain |
| **Codebook** | https://www.eia.gov/consumption/residential/data/2020/index.php?view=microdata |
| **License** | Public Domain (U.S. Government Work) |
| **Processed** | [`recs2020_processed.csv`](recs2020_processed.csv) — 11 columns, 17,196 rows, produced by [`load_recs.py`](load_recs.py) |

The raw RECS CSV is *not* committed to the repo (53 MB). It is re-downloaded automatically by
`load_recs.py` on first run. Only the small processed CSV is versioned.

## Why this dataset

| Property | Why it matters |
|---|---|
| **Real, nationally representative survey** | Avoids the "synthetic-data only" criticism |
| **Has an observable retrofit-like treatment** | `TYPEGLASS` (single vs double/triple-pane windows) — a canonical efficiency measure |
| **Rich covariates** | Building age, floor area, climate zone, housing type, household size, income — exactly the confounders needed for an unconfoundedness-based causal design |
| **n ≈ 17,000** | Plenty of power for Double Machine Learning + Causal Forest |
| **Open & instantly downloadable** | No application or registration needed |

## Schema of `recs2020_processed.csv`

| Column | Role | Description |
|---|---|---|
| `household_id` | id | DOEID renamed |
| `efficient_windows` | **treatment T** | 1 = double/triple-pane, 0 = single-pane (from `TYPEGLASS`) |
| `energy_intensity_kwh_m2` | **outcome Y** | annual total-energy intensity (kWh per m² per year), from `TOTALBTU` ÷ `TOTSQFT_EN` |
| `floor_area_m2` | feature | conditioned floor area in m² (from `TOTSQFT_EN`) |
| `building_age` | feature | age in years (from `YEARMADERANGE` mid-points) |
| `year_built` | feature | construction year (decade mid-point) |
| `housing_type` | feature | Mobile / SF-Detached / SF-Attached / Apt-2to4 / Apt-5plus |
| `climate_zone` | feature | 8 IECC zones (Marine, Hot-Dry, Mixed-Dry, Hot-Humid, Mixed-Humid, Cold, Very-Cold, Subarctic) |
| `cold_climate` | feature | 1 if Cold/Very-Cold/Subarctic else 0 |
| `household_size` | feature | household members (clipped 1-7) |
| `income_bin` | feature | RECS income bin 1-16 (1 = under $5k, 16 = ≥ $200k) |

## Real datasets for further validation (next step / hackathon)

| Dataset | Access | Link | Why |
|---|---|---|---|
| **Smart Meters in London (dToU trial)** | Open, OGL v3 | [data.london.gov.uk](https://data.london.gov.uk/dataset/smartmeter-energy-use-data-in-london-households/) | A real **randomized** Time-of-Use tariff trial — gold-standard for causal identification |
| **CER Irish Smart Metering Trial** | Application | [ISSDA](https://www.ucd.ie/issda/data/commissionforenergyregulationcer/) | RCT with pre/post baseline — ideal for DiD |
| **Building Data Genome Project 2** | Open, CC BY 4.0 | [GitHub](https://github.com/buds-lab/building-data-genome-project-2) | Non-residential buildings, hourly — to mirror the analysis at building level |
| **US DOE Weatherization Retrospective** | On request | [ORNL](https://weatherization.ornl.gov/wap-retrospective/) | The most directly comparable real retrofit pre/post billing data |
