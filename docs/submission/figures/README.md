# Submission Figures

**Figure 1 (architecture)** is embedded in the demo paper's 2-page body. The **screenshots** are
**supplemental materials** — per the CI/HCOMP rules, anything inside the submission PDF counts
toward the 2-page limit, so screenshots are uploaded *separately* in the form's supplemental
section, not embedded in the paper. Capture them with the filenames below for a tidy bundle.

| Filename | Role | What to capture |
|---|---|---|
| `fig1_architecture.svg` / `.png` | **Figure 1 — in the paper body** | **Provided** — tool architecture diagram (already here) |
| `screenshot_single_run.png` | Supplemental | The **Single Run** tab: the summary metric cards (velocity, defect rate, CI score, effectiveness, AI benefit…) with the with-AI vs. without-AI deltas. Ideally include the sidebar controls on the left. |
| `screenshot_montecarlo.png` | Supplemental | The **Monte Carlo Experiments** tab after ~100 replications: the summary table (mean / std / 95% CI) and/or an outcome distribution. |
| `screenshot_sensitivity.png` | Supplemental | The **Sensitivity Analysis** tab: a sweep curve, e.g. team effectiveness (and trust calibration) vs. AI reliability. |

## How to capture

1. `streamlit run app.py` from the project root.
2. Set a clear preset (e.g. *High-trust / high-reliability* for Fig. 2; *Over-trust / low-reliability* is also a good contrast).
3. Screenshot each tab. Full-window captures at a wide browser width read best in print.
4. Save with the filenames above (PNG). No further edits needed — the papers already link them.

Illustrative is fine — these do not need to be exhaustive.
