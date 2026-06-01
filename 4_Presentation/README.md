# Presentation

**[Slides — 2-page PDF](Energy_2-Pager_Presentation.pdf)**

The slides are reproducible from the dataset and baselines via
[`build_slides.py`](build_slides.py) (reads `../data/recs2020_processed.csv`, runs the OLS baselines,
and renders the dashboard + cover image). DML / Causal-Forest results are intentionally left out at
this stage — the slide's "Estimator Pipeline" box shows the cliffhanger.

- **Page 1:** title slide, with a clear "*full causal results coming in the final session*" badge.
- **Page 2:** dashboard — Data & Variables, Naive Contrast, **Estimator Pipeline (in progress)** with
  the two missing methods marked "?", Structural Model (DAG), Status & Next Steps.

A 10-minute speech script is provided in both languages:
[German](../REDESKRIPT_10min.md) · [English](../Speech_10min_EN.md).
