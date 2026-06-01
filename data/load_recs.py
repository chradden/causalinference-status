"""ETL: turn the raw EIA RECS 2020 microdata into the project's working dataset.

Source: U.S. Energy Information Administration (EIA), Residential Energy Consumption Survey 2020.
Download URL: https://www.eia.gov/consumption/residential/data/2020/csv/recs2020_public_v5.csv
Codebook:    https://www.eia.gov/consumption/residential/data/2020/index.php?view=microdata

Treatment:   `efficient_windows` (1 = double/triple-pane, 0 = single-pane) - recoded from TYPEGLASS.
             Replacing single-pane windows is one of the most common energy-efficiency retrofits.
Outcome:     `energy_intensity_kwh_m2` (total annual household energy use per m^2 of floor area).
Confounders: floor area, climate zone, year built, housing type, household size, income bin.

Run from Praxisprojekt/ :  python3 data/load_recs.py
"""
import os, sys, urllib.request
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "recs2020_public_v5.csv")           # ~53 MB - NOT in repo, downloaded on demand
OUT = os.path.join(HERE, "recs2020_processed.csv")           # small, committed to the repo
URL = "https://www.eia.gov/consumption/residential/data/2020/csv/recs2020_public_v5.csv"

if not os.path.exists(RAW):
    print(f"downloading raw RECS 2020 microdata ({URL}) ...")
    urllib.request.urlretrieve(URL, RAW)
    print(f"  -> {RAW}  ({os.path.getsize(RAW)//1024} KB)")

df = pd.read_csv(RAW, low_memory=False)
print(f"raw: {df.shape}")

# --- TREATMENT: efficient windows (binary) -------------------------------------------------
# TYPEGLASS: 1 = single-pane, 2 = double/triple-pane, 3 = other
df = df[df["TYPEGLASS"].isin([1, 2])].copy()
df["efficient_windows"] = (df["TYPEGLASS"] == 2).astype(int)

# --- OUTCOME: energy intensity (kWh per m^2 per year) --------------------------------------
# TOTALBTU is in *thousand* BTU (kBtu) -> kWh = TOTALBTU * 1000 / 3412.14
# TOTSQFT_EN ft^2 -> m^2: * 0.0929030
df = df[(df["TOTSQFT_EN"] > 100) & (df["TOTALBTU"] > 0)].copy()
df["floor_area_m2"] = df["TOTSQFT_EN"] * 0.0929030
df["energy_intensity_kwh_m2"] = (df["TOTALBTU"] * 1000 / 3412.14) / df["floor_area_m2"]

# Trim extreme tails (e.g. mansions with implausibly low intensity, or tiny apartments)
lo, hi = df["energy_intensity_kwh_m2"].quantile([0.005, 0.995])
df = df[(df["energy_intensity_kwh_m2"] >= lo) & (df["energy_intensity_kwh_m2"] <= hi)].copy()

# --- FEATURES (confounders / effect modifiers) ---------------------------------------------
# YEARMADERANGE codes: 1=<1950, 2=1950s, 3=1960s, 4=1970s, 5=1980s, 6=1990s, 7=2000s, 8=2010-20
year_mid = {1: 1945, 2: 1955, 3: 1965, 4: 1975, 5: 1985, 6: 1995, 7: 2005, 8: 2015}
df["year_built"] = df["YEARMADERANGE"].map(year_mid)
df["building_age"] = 2020 - df["year_built"]

# Housing type: 1 mobile, 2 single-family detached, 3 single-family attached, 4 apt 2-4, 5 apt 5+
hu_map = {1: "Mobile", 2: "SF-Detached", 3: "SF-Attached", 4: "Apt-2to4", 5: "Apt-5plus"}
df["housing_type"] = df["TYPEHUQ"].map(hu_map)

# Climate (already a clean string in BA_climate)
df["climate_zone"] = df["BA_climate"]
df["cold_climate"] = df["climate_zone"].isin(["Cold", "Very-Cold", "Subarctic"]).astype(int)

# Household size and income bin
df["household_size"] = df["NHSLDMEM"].clip(lower=1, upper=7)
df["income_bin"] = df["MONEYPY"].clip(lower=1, upper=16)  # 1=<5k ... 16=>=200k

# Final tidy frame
cols = ["DOEID", "efficient_windows", "energy_intensity_kwh_m2", "floor_area_m2",
        "building_age", "year_built", "housing_type", "climate_zone", "cold_climate",
        "household_size", "income_bin"]
out = df[cols].dropna(subset=cols).rename(columns={"DOEID": "household_id"}).reset_index(drop=True)
out.to_csv(OUT, index=False)

print(f"\nprocessed: {out.shape}  ->  {OUT}")
print(out.head().to_string())
print("\nTreatment balance:")
print(out["efficient_windows"].value_counts().rename({0: "single-pane (T=0)", 1: "efficient (T=1)"}))
print("\nNaive mean outcome by treatment:")
print(out.groupby("efficient_windows")["energy_intensity_kwh_m2"].agg(["mean", "std", "count"]).round(2))
