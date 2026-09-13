# CITAS Demonstration Scenarios — Results Summary

Every number below is taken directly from the CSV files in this directory,
produced by `run_scenarios.py` against model **v2.1.0**
(`perceived_reliability_anchor: trust`). Nothing is illustrative.

| Run metadata | |
|---|---|
| Model version | 2.1.0 (anchor `trust`) |
| Simulations executed | 27,680 |
| Wall-clock | 92.5 s |
| Started (UTC) | 2026-09-13T11:04:41 |
| Base seed | 42 — replication *i* uses 42 + *i* |
| Baseline arm | `use_ai=False` (heuristic allocator, no assistant) |
| Paired arms / sweep | 200 paired replications |
| Grid | 40 paired replications per cell, common random numbers |
| Supplementary sweep (support 0.80) | 200 paired replications; 11,200 simulations, 37 s |
| Isolating sweep (support 0.80 + default process) | 200 paired replications; 11,200 simulations, 37 s |
| Positive control | thesis crossing config reproduced bit-for-bit (max diff 0.0) |

**Definitions.** *AI benefit* = paired difference in team effectiveness
(with-AI − without-AI) on the same seed. 95% CI = mean ± 1.96·SE. The model's
internal `ai_benefit` score is a with-AI-only quantity (zero by construction in
the baseline arm); it is reported separately and labelled as such. Metrics are
on the model's 0–100 scale; defect and completion rates are percentages.

---

## 1. Paired baseline vs AI arms (N = 200, identical seeds)

Source: `paired_summary.csv`, `paired_A_safety_critical_embedded.csv`,
`paired_B_large_scale_enterprise.csv`.

| | **Scenario A** safety-critical embedded | **Scenario B** large-scale enterprise |
|---|---|---|
| Team effectiveness, with AI | 77.82 | 75.04 |
| Team effectiveness, without AI | 75.87 | 73.99 |
| **AI benefit (paired Δ effectiveness)** | **+1.95** [+1.40, +2.51] | **+1.06** [+0.63, +1.49] |
| SD / SE of Δ | 4.00 / 0.28 | 3.09 / 0.22 |
| Share of runs with positive Δ | 0.695 | 0.650 |
| Defect rate, with / without AI | 18.49 / 21.95 | 16.16 / 19.65 |
| Δ defect rate (pp) | −3.46 [−4.69, −2.23] | −3.50 [−4.34, −2.65] |
| Δ velocity | +1.12 [+0.62, +1.62] | +0.47 [+0.02, +0.93] |
| Δ completion rate (pp) | +2.50 [+1.30, +3.70] | +0.34 [−0.54, +1.22] |
| Δ decision quality | +9.38 | +9.25 |
| Δ collective intelligence | +1.86 | +2.00 |
| Δ team viability | +1.67 | +1.92 |
| Δ member sustainability | −0.44 | −0.76 |
| Trust calibration, with / without AI (%) | 93.75 / 91.85 | 93.79 / 91.90 |
| Internal `ai_benefit` score (with-AI only) | 41.75 | 40.81 |

**Reading.** AI support yields a positive, statistically clear effectiveness
gain in both scenarios, larger in A (+1.95) than in B (+1.06); the two CIs do
not overlap. The mechanism differs: in **A** the gain is carried by both
quality (−3.5 pp defects) and throughput (+2.5 pp completion, +1.1 velocity);
in **B** it is carried almost entirely by quality and decision quality — the
completion-rate CI includes zero and the velocity gain is marginal. Both
scenarios show a small **negative** effect on member sustainability (−0.44,
−0.76), i.e. AI support slightly raises workload pressure even as it improves
output. Decision quality rises by ~9.3 points in both, the largest single
effect.

---

## 2. Scenario A — AI-reliability sweep (N = 200 paired per point)

Source: `sweep_reliability_A_trust065.csv`, `sweep_reliability_A_trust085.csv`,
`sweep_zero_crossing_A.csv`. Trust held at 0.65 and 0.85; all other Scenario A
parameters unchanged (`ai_support_level` 0.70, `dashboard_quality` 0.70).

### 2.1 Zero crossing — **none found in 0.30–0.95 at either trust level**

| Trust | Crossings in range | Benefit at reliability 0.30 | Benefit at 0.95 | First reliability with CI wholly > 0 |
|---|---|---|---|---|
| 0.65 | 0 | +0.60 [+0.06, +1.15] | +2.10 [+1.54, +2.65] | 0.30 |
| 0.85 | 0 | +0.08 [−0.52, +0.68] | +2.43 [+1.88, +2.97] | 0.45 |

**This is a substantive result and departs from the thesis, which located a
crossing near 48% reliability.** In Scenario A the paired AI benefit never
becomes negative on average. At trust 0.85 it is *indistinguishable from zero*
for reliability ≤ 0.40 (CIs include zero) and becomes reliably positive from
0.45 upward; at trust 0.65 it is already (just) positive at 0.30. The
plausible reason is the scenario itself, not a model fault: Scenario A has
much stronger process discipline than the thesis baseline (`effort_management`
0.75, `task_strategy` 0.70, `consequentiality` 0.85 vs. 0.65 defaults) —
**but two isolating sweeps rule out both obvious explanations.** §2.3 shows
the *support level* (0.70 vs. the thesis crossing run's 0.80) is not the
cause; §2.4 shows the *process profile* is not the cause either (resetting all
four process parameters to defaults still yields no crossing, though it does
lower low-reliability benefit by ~0.1). A positive control (§2.4) confirms the
harness reproduces the thesis crossing bit-for-bit, so the difference is real.
What remains different from the thesis configuration is Scenario A's team
size (5 vs 6), **sprint count (12 vs 8)**, backlog mix, task complexity
(0.72 vs 0.58), **dependency density (0.45 vs 0.25)** and CI baselines. Two
of these have a mechanism that would suppress over-trust harm: more sprints
give learned trust longer to converge perception toward true reliability, and
higher dependency/complexity raise coordination need, which enlarges the
shared-cognition assistant's upside. These are *hypotheses*, not tested
results. The paper should present the null harm as *conditional on the
scenario configuration* and not attribute it to process discipline.

### 2.2 Sweep curves

| Reliability | Δ eff, trust 0.65 [95% CI] | Δ eff, trust 0.85 [95% CI] | Calib. 0.65 (%) | Calib. 0.85 (%) |
|---|---|---|---|---|
| 0.30 | +0.60 [+0.06, +1.15] | +0.08 [−0.52, +0.68] | 68.8 | 55.3 |
| 0.35 | +0.83 [+0.33, +1.32] | +0.39 [−0.18, +0.96] | 72.6 | 59.2 |
| 0.40 | +0.79 [+0.25, +1.34] | +0.42 [−0.17, +1.01] | 76.4 | 63.0 |
| 0.45 | +1.09 [+0.53, +1.65] | +0.99 [+0.46, +1.52] | 80.3 | 66.8 |
| 0.50 | +1.12 [+0.56, +1.68] | +1.12 [+0.58, +1.66] | 84.1 | 70.7 |
| 0.55 | +1.35 [+0.78, +1.92] | +1.26 [+0.70, +1.82] | 87.9 | 74.5 |
| 0.60 | +1.39 [+0.85, +1.94] | +1.30 [+0.77, +1.84] | 91.6 | 78.3 |
| 0.65 | +1.69 [+1.17, +2.21] | +1.34 [+0.78, +1.90] | 94.6 | 82.1 |
| 0.70 | +1.88 [+1.35, +2.42] | +1.63 [+1.08, +2.19] | 96.0 | 86.0 |
| 0.75 | +2.06 [+1.53, +2.59] | +1.78 [+1.23, +2.32] | 95.2 | 89.8 |
| 0.80 | +2.02 [+1.46, +2.58] | +2.15 [+1.60, +2.70] | 92.5 | 93.4 |
| 0.85 | +1.86 [+1.31, +2.41] | +2.24 [+1.70, +2.78] | 89.0 | 96.2 |
| 0.90 | +1.86 [+1.30, +2.42] | +2.28 [+1.75, +2.82] | 85.3 | 96.7 |
| 0.95 | +2.10 [+1.54, +2.65] | +2.43 [+1.88, +2.97] | 81.4 | 94.7 |

Standard errors are 0.25–0.31 throughout. The slight non-monotonicity at
trust 0.65 between 0.75 and 0.90 (2.06 → 1.86) is within one SE and should
not be interpreted.

**Calibration is a ridge, not a monotone curve.** At trust 0.65 calibration
peaks at 96.0% (reliability 0.70) and *falls* to 81.4% at reliability 0.95;
at trust 0.85 it peaks at 96.7% (reliability 0.90). Perception is anchored on
trust and converges toward actual reliability at 0.05 per sprint over 12
sprints, so a moderately trusting team facing a highly reliable assistant
ends up *under-trusting* it. This is the under-reliance regime of Lee & See
(2004) appearing as intended in v2.1 — a feature, not an artefact — and it is
why the grid's calibration surface is diagonal (§3).

### 2.3 Supplementary sweep at `ai_support_level` 0.80 — **still no crossing**

Source: `sweep_reliability_A_support080_trust065.csv`,
`…_trust085.csv`, `sweep_zero_crossing_A_support080.csv`,
`run_report_support080.json`. Single-factor test: Scenario A with support
raised from 0.70 to 0.80 (the thesis crossing run's level), **nothing else
changed**, same seeds.

| Trust | Crossings | Benefit at 0.30 | Benefit at 0.95 | First reliability with CI wholly > 0 | Any point with CI wholly < 0 |
|---|---|---|---|---|---|
| 0.65 | 0 | +0.42 [−0.14, +0.98] | +2.28 [+1.73, +2.83] | 0.35 | none |
| 0.85 | 0 | +0.24 [−0.34, +0.82] | +2.61 [+2.08, +3.14] | 0.40 | none |

Raising support **lifts the benefit ceiling** (mean uplift over the 0.70 run:
+0.16 at trust 0.65, +0.22 at trust 0.85; about +0.18 at reliability 0.95 for
both) **without creating a negative-benefit region**. The support dial scales
both the AI upside and the uptake of bad recommendations
(`uptake = support × trust`), and in Scenario A the former dominates at every
reliability. Conclusion: the absence of a crossing is a property of the
Scenario A configuration, not of the support level. Figure:
`figures/fig_scenarios_reliability_sweep_A_support_compare.png`.

### 2.4 Isolating sweep: support 0.80 **and** default process — **still no crossing**

Source: `sweep_reliability_A_support080_defproc_trust065.csv`, `…085.csv`,
`sweep_zero_crossing_A_support080_defproc.csv`, `run_report_support080_defproc.json`.
Scenario A with `ai_support_level` 0.80 and `effort_management`,
`skills_knowledge_coordination`, `task_strategy`, `consequentiality` all reset
to the model defaults (0.65). Same seeds.

| Trust | Crossings | Benefit at 0.30 | Benefit at 0.95 | First reliability with CI wholly > 0 | Any point with CI wholly < 0 |
|---|---|---|---|---|---|
| 0.65 | 0 | +0.27 [−0.33, +0.88] | +2.29 [+1.75, +2.84] | 0.50 | none |
| 0.85 | 0 | +0.32 [−0.31, +0.95] | +2.86 [+2.30, +3.42] | 0.50 | none |

Resetting process **does** reduce benefit at low reliability relative to
Scenario A's process profile (mean difference −0.14 at trust 0.65, −0.11 at
trust 0.85; the CI-above-zero threshold moves from 0.35–0.40 up to 0.50), so
process discipline contributes a small buffer in the expected direction — but
the benefit never turns negative. Process is therefore **not** what removes
the crossing.

**Positive control.** The same paired harness, run on the thesis crossing
configuration (`SimulationConfig()` defaults, trust 0.85, support 0.80,
dashboard 0.70, N = 60, seeds 42+i), reproduces
`results/ai_reliability_crossing.csv` **exactly** (max absolute difference
0.0): benefit −1.26 [−2.23, −0.29] at reliability 0.30, crossing between 0.45
and 0.50. The absence of a crossing in Scenario A is therefore a property of
the Scenario A configuration, not of the harness.

Figure: `figures/fig_scenarios_reliability_sweep_A_support_compare.png`
(three curves per trust level: support 0.70, support 0.80, support 0.80 +
default process).

---

## 3. Scenario A — trust × reliability grid (14 × 14 = 196 cells, N = 40 per cell, common random numbers)

Source: `grid_trust_x_reliability_A.csv`. Per-cell SE for Δ effectiveness
ranges 0.52–0.76 (median 0.63), so **individual cells are not precise**; the
grid is to be read as a surface.

| Statistic | Value |
|---|---|
| Cells with negative mean benefit | 16 of 196 (8.2%) |
| … among over-trust cells (trust > reliability) | 17.6% |
| … among calibrated / under-trust cells (trust ≤ reliability) | **0.0%** |
| Most negative cell | trust 0.90, reliability 0.35: −0.86 (SE 0.67), calibration 56.3% |
| Most positive cell | trust 0.90, reliability 0.95: +2.45 (SE 0.60), calibration 96.8% |
| Cell nearest Scenario A operating point (trust 0.65, reliability 0.80) | +1.64 (SE 0.65), calibration 93.1%, share positive 0.70 |

(The operating point's exact reliability, 0.78, is not a grid node; the
200-replication sweep point at trust 0.65 / reliability 0.80 gives
+2.02 [+1.46, +2.58].)

**Reading.** The qualitative calibrated-reliance pattern holds cleanly: every
negative-benefit cell lies in the over-trust half of the surface, and none in
the calibrated or under-trust half. Benefit rises with reliability at every
trust level. But the magnitude of over-trust harm in Scenario A is small —
the most negative cell (−0.86) is only ~1.3 SE from zero at N = 40 — so the
finding is the *location* of the negative region, not the significance of any
one cell. This is consistent with §2.1: under Scenario A's strong process
profile, mis-calibrated reliance costs the team little.

Full pivots (rows = trust, columns = reliability) are reproduced in
`grid_trust_x_reliability_A.csv`; the benefit surface is plotted in
`figures/fig_scenarios_trust_x_reliability_A.png`.

---

## 4. Things to look at before this goes into the paper

1. **No zero crossing in Scenario A — and neither support level nor process
   profile explains it (§2.1, §2.3, §2.4).** The harness is validated by a
   bit-for-bit positive control on the thesis configuration. The remaining
   differences from the thesis run are team size, sprint count, backlog mix,
   task complexity, dependency density and CI baselines. The two with a
   plausible mechanism are **sprint count** (12 vs 8 — longer for learned
   trust to converge) and **dependency density / complexity** (higher
   coordination need enlarges the assistant's upside). The paper must not
   attribute the null harm to process discipline; the current evidence only
   supports "conditional on configuration". The next isolating rung — the
   default-process/support-0.80 configuration with `number_of_sprints` 8, and
   separately with `dependency_density` 0.25 — is cheap (~40 s each) and
   would pin the mechanism. Not run; outside the approved plan.
2. **Scenario B's throughput gain is null.** Completion-rate CI includes zero;
   AI benefit in B is a quality/decision effect, not a delivery effect. Worth
   stating rather than letting a single "+1.06" carry the message.
3. **Sustainability is slightly negative in both scenarios.** Small, but
   consistent in sign; a reviewer may ask about it.
4. **Calibration falls at high reliability under moderate trust (§2.2).** Correct
   v2.1 behaviour (under-trust), but a reader expecting "more reliable → better
   calibrated" will be surprised; explain the learning-rate mechanism.
5. **Grid precision.** N = 40 per cell gives SE ≈ 0.63; do not quote individual
   cells as findings. The surface and its sign structure are the result.
6. A single-seed smoke test (seed 42) had shown Scenario B's with-AI defect rate
   *higher* than without; the 200-replication result reverses this
   (−3.50 pp, CI excludes zero). It was seed noise — noted so nobody
   re-discovers it from the raw per-run CSV.

## Files

| File | Contents |
|---|---|
| `paired_summary.csv` | one row per scenario, all paired deltas with CIs |
| `paired_A_…csv`, `paired_B_…csv` | per-replication with/without metrics (200 rows each) |
| `sweep_reliability_A_trust065.csv`, `…085.csv` | reliability sweep, per point |
| `sweep_zero_crossing_A.csv` | crossing detection results |
| `sweep_reliability_A_support080_trust065.csv`, `…085.csv`, `sweep_zero_crossing_A_support080.csv`, `run_report_support080.json` | supplementary sweep at support 0.80 |
| `sweep_reliability_A_support080_defproc_trust065.csv`, `…085.csv`, `sweep_zero_crossing_A_support080_defproc.csv`, `run_report_support080_defproc.json` | isolating sweep: support 0.80 + default process |
| `grid_trust_x_reliability_A.csv` | 196 cells with mean, SE, SD, CI, calibration |
| `run_report.json` | model version, seeds, replication counts, scenario configs, timing |
| `figures/` | `fig_scenarios_paired_benefit.png`, `fig_scenarios_reliability_sweep_A.png`, `fig_scenarios_trust_x_reliability_A.png`, `fig_scenarios_reliability_sweep_A_support_compare.png` |
