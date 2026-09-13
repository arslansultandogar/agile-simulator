"""Run the CITAS demonstration scenarios headlessly against the real simulator.

Follows the conventions of run_thesis_experiments.py: paired with/without-AI
runs on identical seeds, 95% CIs as mean +/- 1.96*SE, CSV outputs plus a
run_report.json recording model version, replication counts and seeds.

Writes ONLY to results_scenarios/. Never touches results/ or results_v20/.

Executes, per the scenario brief:
  1. Paired baseline (use_ai=False) and AI (use_ai=True) arms for Scenarios A
     and B - 200 replications, identical seeds within each pair.
  2. Scenario A AI-reliability sweep, 0.30-0.95 step 0.05, at trust 0.65 and
     0.85 - 200 paired replications per point; zero-crossing identified.
  3. Scenario A trust x reliability grid, both 0.30-0.95 step 0.05 - 40 paired
     replications per cell with common random numbers (the SAME seed sequence
     42+i in every cell) so cell-to-cell differences reflect the parameter
     change, not sampling noise. Standard errors reported per cell.
"""

from __future__ import annotations

import json
import time
from dataclasses import asdict, replace
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

from config_loader import MODEL_VERSION, PERCEIVED_RELIABILITY_ANCHOR
from scenarios import LABELS, SCENARIOS, build_config
from simulation import run_simulation

# ---------------------------------------------------------------- v2.1 guard
# All valid results derive from v2.1 mechanics. Refuse anything else, including
# the anchor="actual" setting, which reverts only part of v2.1 and produces a
# hybrid matching neither version.
if MODEL_VERSION != "2.1.0" or PERCEIVED_RELIABILITY_ANCHOR != "trust":
    raise SystemExit(
        f"Refusing to run: MODEL_VERSION={MODEL_VERSION!r}, "
        f"perceived_reliability_anchor={PERCEIVED_RELIABILITY_ANCHOR!r}. "
        "Scenarios require model 2.1.0 with anchor='trust'."
    )

OUT = Path("results_scenarios")
OUT.mkdir(exist_ok=True)

REPS = 200        # paired replications: arms and 1-D reliability sweep
GRID_REPS = 40    # paired replications per grid cell (matches thesis SENS_REPS)
SWEEP_TRUST_LEVELS = (0.65, 0.85)
# 0.30 .. 0.95 inclusive in steps of 0.05 (14 values), built without float drift
GRID_VALUES = [round(0.30 + 0.05 * k, 2) for k in range(14)]
SWEEP_SCENARIO = "A_safety_critical_embedded"


def ci95(s):
    s = pd.Series(s).astype(float)
    m = s.mean()
    if len(s) < 2:
        return m, m
    margin = 1.96 * s.std(ddof=1) / np.sqrt(len(s))
    return m - margin, m + margin


def paired_runs(config, reps):
    """With/without-AI runs on identical seeds (seed_i = random_seed + i)."""
    rows = []
    for i in range(reps):
        trial = replace(config, random_seed=config.random_seed + i)
        w = run_simulation(trial, use_ai=True)["summary"]
        wo = run_simulation(trial, use_ai=False)["summary"]
        rows.append({
            "seed": trial.random_seed,
            "eff_with": w["team_effectiveness"],
            "eff_without": wo["team_effectiveness"],
            "eff_delta": w["team_effectiveness"] - wo["team_effectiveness"],
            "defect_with": w["defect_rate"],
            "defect_without": wo["defect_rate"],
            "defect_delta": w["defect_rate"] - wo["defect_rate"],
            "velocity_delta": w["average_velocity"] - wo["average_velocity"],
            "completion_delta": w["completion_rate"] - wo["completion_rate"],
            "carry_over_delta": w["carry_over_rate"] - wo["carry_over_rate"],
            "dq_delta": w["decision_quality"] - wo["decision_quality"],
            "ci_delta": w["collective_intelligence"] - wo["collective_intelligence"],
            "viability_delta": w["team_viability"] - wo["team_viability"],
            "sustainability_delta": w["member_sustainability"] - wo["member_sustainability"],
            "ai_benefit_score": w["ai_benefit"],          # internal with-AI-only score
            "trust_calibration_with": w["trust_calibration"],
            "trust_calibration_without": wo["trust_calibration"],
        })
    return pd.DataFrame(rows)


def summarise_delta(series):
    s = pd.Series(series).astype(float)
    lo, hi = ci95(s)
    return {
        "mean": round(s.mean(), 4),
        "sd": round(s.std(ddof=0), 4),
        "se": round(s.std(ddof=1) / np.sqrt(len(s)), 4),
        "ci_low": round(lo, 4),
        "ci_high": round(hi, 4),
        "share_positive": round((s > 0).mean(), 4),
    }


def zero_crossings(x, y):
    """Reliability values where the AI-benefit curve crosses zero (linear interp)."""
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    found = []
    for k in range(len(x) - 1):
        if y[k] == 0.0:
            found.append(float(x[k]))
        elif y[k] * y[k + 1] < 0:
            found.append(float(x[k] + (x[k + 1] - x[k]) * (-y[k]) / (y[k + 1] - y[k])))
    if len(y) and y[-1] == 0.0:
        found.append(float(x[-1]))
    return found


t_start = time.perf_counter()
report = {
    "model_version": MODEL_VERSION,
    "perceived_reliability_anchor": PERCEIVED_RELIABILITY_ANCHOR,
    "baseline_arm": "use_ai=False (heuristic allocator, no shared-cognition assistant)",
    "repetitions_paired_arms": REPS,
    "repetitions_reliability_sweep": REPS,
    "repetitions_grid_cell": GRID_REPS,
    "seed_rule": "replication i uses random_seed + i; identical within each pair "
                 "and identical across all grid cells (common random numbers)",
    "sweep_trust_levels": list(SWEEP_TRUST_LEVELS),
    "grid_values": GRID_VALUES,
    "scenarios": {name: build_config(name).__dict__ | {"task_mix": build_config(name).task_mix}
                  for name in SCENARIOS},
    "started_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
}

# ---------------------------------------------------------- 1. PAIRED ARMS
print("=== 1. Paired baseline vs AI arms (N=%d, identical seeds) ===" % REPS)
paired_summary = []
for name in SCENARIOS:
    cfg = build_config(name)
    df = paired_runs(cfg, REPS)
    df.to_csv(OUT / f"paired_{name}.csv", index=False)
    e = summarise_delta(df["eff_delta"])
    d = summarise_delta(df["defect_delta"])
    v = summarise_delta(df["velocity_delta"])
    c = summarise_delta(df["completion_delta"])
    row = {
        "scenario": name,
        "label": LABELS[name],
        "n": len(df),
        "base_seed": cfg.random_seed,
        "eff_with_mean": round(df["eff_with"].mean(), 3),
        "eff_without_mean": round(df["eff_without"].mean(), 3),
        "eff_delta_mean": e["mean"], "eff_delta_sd": e["sd"], "eff_delta_se": e["se"],
        "eff_delta_ci_low": e["ci_low"], "eff_delta_ci_high": e["ci_high"],
        "eff_share_positive": e["share_positive"],
        "defect_with_mean": round(df["defect_with"].mean(), 3),
        "defect_without_mean": round(df["defect_without"].mean(), 3),
        "defect_delta_mean": d["mean"], "defect_delta_ci_low": d["ci_low"], "defect_delta_ci_high": d["ci_high"],
        "velocity_delta_mean": v["mean"], "velocity_delta_ci_low": v["ci_low"], "velocity_delta_ci_high": v["ci_high"],
        "completion_delta_mean": c["mean"], "completion_delta_ci_low": c["ci_low"], "completion_delta_ci_high": c["ci_high"],
        "dq_delta_mean": round(df["dq_delta"].mean(), 3),
        "ci_delta_mean": round(df["ci_delta"].mean(), 3),
        "viability_delta_mean": round(df["viability_delta"].mean(), 3),
        "sustainability_delta_mean": round(df["sustainability_delta"].mean(), 3),
        "ai_benefit_score_mean": round(df["ai_benefit_score"].mean(), 3),
        "trust_calibration_with_mean": round(df["trust_calibration_with"].mean(), 3),
        "trust_calibration_without_mean": round(df["trust_calibration_without"].mean(), 3),
    }
    paired_summary.append(row)
    print(f"  {name:28s} eff delta {e['mean']:+.3f} [{e['ci_low']:+.3f}, {e['ci_high']:+.3f}]  "
          f"share>0 {e['share_positive']:.2f}  defect delta {d['mean']:+.3f}  "
          f"calib(with) {row['trust_calibration_with_mean']:.2f}")
paired_df = pd.DataFrame(paired_summary)
paired_df.to_csv(OUT / "paired_summary.csv", index=False)

# ---------------------------------------------- 2. RELIABILITY SWEEP (A)
print(f"\n=== 2. Scenario A AI-reliability sweep (N={REPS} paired per point) ===")
base_A = build_config(SWEEP_SCENARIO)
crossing_rows = []
for trust in SWEEP_TRUST_LEVELS:
    rows = []
    for rel in GRID_VALUES:
        cfg = replace(base_A, ai_reliability=rel, trust_in_ai=trust)
        df = paired_runs(cfg, REPS)
        e = summarise_delta(df["eff_delta"])
        d = summarise_delta(df["defect_delta"])
        rows.append({
            "trust_in_ai": trust, "ai_reliability": rel, "n": len(df),
            "eff_delta": e["mean"], "eff_delta_se": e["se"],
            "ci_low": e["ci_low"], "ci_high": e["ci_high"],
            "ci_excludes_zero": bool(e["ci_low"] > 0 or e["ci_high"] < 0),
            "share_positive": e["share_positive"],
            "defect_delta": d["mean"], "defect_delta_ci_low": d["ci_low"], "defect_delta_ci_high": d["ci_high"],
            "trust_calibration_with": round(df["trust_calibration_with"].mean(), 3),
            "trust_calibration_without": round(df["trust_calibration_without"].mean(), 3),
        })
    sweep_df = pd.DataFrame(rows)
    tag = f"trust{int(round(trust * 100)):03d}"
    sweep_df.to_csv(OUT / f"sweep_reliability_A_{tag}.csv", index=False)
    xs = zero_crossings(sweep_df["ai_reliability"], sweep_df["eff_delta"])
    sign_low = "positive" if sweep_df["eff_delta"].iloc[0] > 0 else "negative"
    sign_high = "positive" if sweep_df["eff_delta"].iloc[-1] > 0 else "negative"
    crossing_rows.append({
        "trust_in_ai": trust,
        "n_crossings": len(xs),
        "first_crossing_reliability": round(xs[0], 4) if xs else None,
        "all_crossings": ";".join(f"{x:.4f}" for x in xs) if xs else "",
        "benefit_at_lowest_reliability": sweep_df["eff_delta"].iloc[0],
        "benefit_at_highest_reliability": sweep_df["eff_delta"].iloc[-1],
        "sign_at_0.30": sign_low, "sign_at_0.95": sign_high,
        "first_reliability_with_ci_above_zero":
            next((r for r, ok, lo in zip(sweep_df["ai_reliability"], sweep_df["ci_excludes_zero"], sweep_df["ci_low"]) if ok and lo > 0), None),
    })
    print(f"  trust={trust:.2f}: " + ", ".join(f"{r:.2f}:{e:+.2f}" for r, e in zip(sweep_df["ai_reliability"], sweep_df["eff_delta"])))
    print(f"    zero crossings: {xs if xs else 'none in range'}  ({sign_low} at 0.30, {sign_high} at 0.95)")
crossing_df = pd.DataFrame(crossing_rows)
crossing_df.to_csv(OUT / "sweep_zero_crossing_A.csv", index=False)

# ------------------------------------------- 3. TRUST x RELIABILITY GRID (A)
print(f"\n=== 3. Scenario A trust x reliability grid ({len(GRID_VALUES)}x{len(GRID_VALUES)} cells, "
      f"N={GRID_REPS} paired per cell, common random numbers) ===")
grid_rows = []
for trust in GRID_VALUES:
    for rel in GRID_VALUES:
        cfg = replace(base_A, ai_reliability=rel, trust_in_ai=trust)   # same base seed -> CRN
        df = paired_runs(cfg, GRID_REPS)
        e = summarise_delta(df["eff_delta"])
        d = summarise_delta(df["defect_delta"])
        tc = pd.Series(df["trust_calibration_with"]).astype(float)
        grid_rows.append({
            "trust_in_ai": trust, "ai_reliability": rel, "n": len(df),
            "eff_delta_mean": e["mean"], "eff_delta_se": e["se"], "eff_delta_sd": e["sd"],
            "eff_delta_ci_low": e["ci_low"], "eff_delta_ci_high": e["ci_high"],
            "share_positive": e["share_positive"],
            "defect_delta_mean": d["mean"], "defect_delta_se": d["se"],
            "trust_calibration_mean": round(tc.mean(), 3),
            "trust_calibration_se": round(tc.std(ddof=1) / np.sqrt(len(tc)), 4),
            "trust_gap": round(trust - rel, 2),   # >0 over-trust, <0 under-trust
        })
    done = [g for g in grid_rows if g["trust_in_ai"] == trust]
    print(f"  trust={trust:.2f}  eff delta across reliability: "
          f"{min(g['eff_delta_mean'] for g in done):+.2f} .. {max(g['eff_delta_mean'] for g in done):+.2f}")
grid_df = pd.DataFrame(grid_rows)
grid_df.to_csv(OUT / "grid_trust_x_reliability_A.csv", index=False)

# ----------------------------------------------------------------- REPORT
elapsed = time.perf_counter() - t_start
report["finished_utc"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
report["elapsed_seconds"] = round(elapsed, 1)
report["simulations_executed"] = int(
    2 * REPS * len(SCENARIOS)
    + 2 * REPS * len(SWEEP_TRUST_LEVELS) * len(GRID_VALUES)
    + 2 * GRID_REPS * len(GRID_VALUES) ** 2
)
report["files"] = sorted(p.name for p in OUT.glob("*.csv"))
(OUT / "run_report.json").write_text(json.dumps(report, indent=2, default=str))
print(f"\nDone in {elapsed:.0f}s. model_version = {MODEL_VERSION}, "
      f"{report['simulations_executed']} simulations. Outputs in {OUT}/")
