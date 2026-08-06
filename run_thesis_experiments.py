"""Run all thesis experiments headlessly against the real simulator.

Reproduces exactly what the Streamlit Monte Carlo and Sensitivity tabs compute,
using the same PRESET_SCENARIOS values defined in app.py.
"""

from __future__ import annotations

import json
from dataclasses import replace
from pathlib import Path

import numpy as np
import pandas as pd

from config_loader import MODEL_VERSION
from experiments import (
    compare_scenarios,
    run_experiments,
    run_sensitivity_analysis,
    sensitivity_stability_summary,
)
from simulation import SimulationConfig
from tasks import normalize_task_mix

OUT = Path("results")
OUT.mkdir(exist_ok=True)

REPS = 200          # Monte Carlo replications per configuration
SENS_REPS = 40      # replications per sensitivity point

# Presets copied verbatim from app.py PRESET_SCENARIOS (percent -> fraction)
PRESETS = {
    "S1_high_trust_high_reliability": dict(
        trust_in_ai=0.85, ai_reliability=0.90, ai_support_level=0.80,
        dashboard_quality=0.80, effort_management=0.70,
        skills_knowledge_coordination=0.72, task_strategy=0.72),
    "S2_over_trust_low_reliability": dict(
        trust_in_ai=0.88, ai_reliability=0.45, ai_support_level=0.80,
        dashboard_quality=0.60, effort_management=0.60,
        skills_knowledge_coordination=0.58, task_strategy=0.58),
    "S3_strong_process_weak_ai": dict(
        trust_in_ai=0.50, ai_reliability=0.55, ai_support_level=0.35,
        dashboard_quality=0.45, effort_management=0.82,
        skills_knowledge_coordination=0.82, task_strategy=0.80),
    "S4_weak_process_strong_ai": dict(
        trust_in_ai=0.75, ai_reliability=0.88, ai_support_level=0.85,
        dashboard_quality=0.82, effort_management=0.45,
        skills_knowledge_coordination=0.45, task_strategy=0.45),
}

BASE = SimulationConfig()  # dataclass defaults = app defaults


def stats_of(config, reps=REPS, use_ai=True, seed_offset=0):
    exp = run_experiments(config, repetitions=reps, use_ai=use_ai, seed_offset=seed_offset)
    return exp["statistics"].set_index("Metric"), exp["results"]


def paired_ai_benefit(config, reps=REPS):
    """Paired with/without-AI difference on identical seeds."""
    rows = []
    for i in range(reps):
        trial = replace(config, random_seed=config.random_seed + i)
        from simulation import run_simulation
        with_ai = run_simulation(trial, use_ai=True)["summary"]
        without = run_simulation(trial, use_ai=False)["summary"]
        rows.append({
            "seed": trial.random_seed,
            "eff_with": with_ai["team_effectiveness"],
            "eff_without": without["team_effectiveness"],
            "eff_delta": with_ai["team_effectiveness"] - without["team_effectiveness"],
            "defect_with": with_ai["defect_rate"],
            "defect_without": without["defect_rate"],
            "defect_delta": with_ai["defect_rate"] - without["defect_rate"],
            "velocity_delta": with_ai["average_velocity"] - without["average_velocity"],
            "completion_delta": with_ai["completion_rate"] - without["completion_rate"],
            "ai_benefit": with_ai["ai_benefit"],
            "trust_calibration": with_ai["trust_calibration"],
        })
    return pd.DataFrame(rows)


def ci95(s):
    s = pd.Series(s).astype(float)
    m = s.mean()
    if len(s) < 2:
        return m, m
    margin = 1.96 * s.std(ddof=1) / np.sqrt(len(s))
    return m - margin, m + margin


report = {"model_version": MODEL_VERSION, "repetitions": REPS,
          "sensitivity_repetitions": SENS_REPS}

# ---------------------------------------------------------------- EXPERIMENT 1
print("=== EXPERIMENT 1: CI baseline levels ===")
exp1 = []
for label, level in [("Low (40%)", 0.40), ("Default (62/60/64%)", None), ("High (80%)", 0.80)]:
    if level is None:
        cfg = BASE
    else:
        cfg = replace(BASE, collective_memory=level, collective_attention=level,
                      collective_reasoning=level)
    st, raw = stats_of(cfg)
    exp1.append({
        "CI baselines": label,
        "Velocity": st.loc["average_velocity", "Mean"],
        "Velocity SD": st.loc["average_velocity", "Std Dev"],
        "Completion": st.loc["completion_rate", "Mean"],
        "Completion SD": st.loc["completion_rate", "Std Dev"],
        "Defect rate": st.loc["defect_rate", "Mean"],
        "Defect SD": st.loc["defect_rate", "Std Dev"],
        "CI score": st.loc["collective_intelligence", "Mean"],
        "Effectiveness": st.loc["team_effectiveness", "Mean"],
        "Effectiveness SD": st.loc["team_effectiveness", "Std Dev"],
        "Eff CI low": st.loc["team_effectiveness", "95% CI Low"],
        "Eff CI high": st.loc["team_effectiveness", "95% CI High"],
    })
exp1_df = pd.DataFrame(exp1)
exp1_df.to_csv(OUT / "exp1_ci_levels.csv", index=False)
print(exp1_df.to_string(index=False))

# ---------------------------------------------------------------- EXPERIMENT 2
print("\n=== EXPERIMENT 2: S1 vs S2 paired AI benefit ===")
exp2 = []
for name in ["S1_high_trust_high_reliability", "S2_over_trust_low_reliability"]:
    cfg = replace(BASE, **PRESETS[name])
    paired = paired_ai_benefit(cfg)
    paired.to_csv(OUT / f"exp2_paired_{name}.csv", index=False)
    lo, hi = ci95(paired["eff_delta"])
    dlo, dhi = ci95(paired["defect_delta"])
    exp2.append({
        "Scenario": name,
        "Eff delta mean": round(paired["eff_delta"].mean(), 3),
        "Eff delta SD": round(paired["eff_delta"].std(ddof=0), 3),
        "Eff delta CI low": round(lo, 3),
        "Eff delta CI high": round(hi, 3),
        "Share runs positive": round((paired["eff_delta"] > 0).mean(), 3),
        "Defect delta mean": round(paired["defect_delta"].mean(), 3),
        "Defect delta CI low": round(dlo, 3),
        "Defect delta CI high": round(dhi, 3),
        "AI benefit score": round(paired["ai_benefit"].mean(), 3),
        "Trust calibration": round(paired["trust_calibration"].mean(), 3),
    })
exp2_df = pd.DataFrame(exp2)
exp2_df.to_csv(OUT / "exp2_trust_scenarios.csv", index=False)
print(exp2_df.to_string(index=False))

# ---------------------------------------------------------------- EXPERIMENT 3
print("\n=== EXPERIMENT 3: backlog composition ===")
mixes = {
    "Feature (100%)": {"feature": 1.0},
    "Bug fix (100%)": {"bug": 1.0},
    "Refactor (100%)": {"refactor": 1.0},
    "Spike (100%)": {"spike": 1.0},
    "Default mix (50/25/15/10)": {"feature": .50, "bug": .25, "refactor": .15, "spike": .10},
}
exp3 = []
for label, mix in mixes.items():
    cfg = replace(BASE, task_mix=normalize_task_mix(mix))
    st, _ = stats_of(cfg)
    exp3.append({
        "Backlog": label,
        "Completion": st.loc["completion_rate", "Mean"],
        "Completion SD": st.loc["completion_rate", "Std Dev"],
        "Defect rate": st.loc["defect_rate", "Mean"],
        "Defect SD": st.loc["defect_rate", "Std Dev"],
        "Velocity": st.loc["average_velocity", "Mean"],
        "Carry-over rate": st.loc["carry_over_rate", "Mean"],
        "Rework created": st.loc["rework_created", "Mean"],
        "Effectiveness": st.loc["team_effectiveness", "Mean"],
        "Effectiveness SD": st.loc["team_effectiveness", "Std Dev"],
    })
exp3_df = pd.DataFrame(exp3)
exp3_df.to_csv(OUT / "exp3_task_types.csv", index=False)
print(exp3_df.to_string(index=False))

# ---------------------------------------------------------------- EXPERIMENT 4
print("\n=== EXPERIMENT 4: process vs AI ===")
exp4 = []
for label, name in [("Default", None),
                    ("S3: Strong process / weak AI", "S3_strong_process_weak_ai"),
                    ("S4: Weak process / strong AI", "S4_weak_process_strong_ai")]:
    cfg = BASE if name is None else replace(BASE, **PRESETS[name])
    st, _ = stats_of(cfg)
    exp4.append({
        "Scenario": label,
        "CI score": st.loc["collective_intelligence", "Mean"],
        "CI SD": st.loc["collective_intelligence", "Std Dev"],
        "Decision quality": st.loc["decision_quality", "Mean"],
        "DQ SD": st.loc["decision_quality", "Std Dev"],
        "Effectiveness": st.loc["team_effectiveness", "Mean"],
        "Eff SD": st.loc["team_effectiveness", "Std Dev"],
        "Viability": st.loc["team_viability", "Mean"],
        "Sustainability": st.loc["member_sustainability", "Mean"],
        "Sustain SD": st.loc["member_sustainability", "Std Dev"],
    })
exp4_df = pd.DataFrame(exp4)
exp4_df.to_csv(OUT / "exp4_process_vs_ai.csv", index=False)
print(exp4_df.to_string(index=False))

# ---------------------------------------------------------------- SENSITIVITY
print("\n=== SENSITIVITY SWEEPS ===")
sweeps = {}
stability_rows = []
sweep_params = ["ai_reliability", "trust_in_ai", "effort_management",
                "skills_knowledge_coordination", "task_strategy",
                "collective_reasoning", "dashboard_quality", "dependency_density"]
for param in sweep_params:
    values = [round(v, 3) for v in np.linspace(0.20, 0.90, 8)]
    df = run_sensitivity_analysis(BASE, param, values, repetitions=SENS_REPS, use_ai=True)
    df.to_csv(OUT / f"sensitivity_{param}.csv", index=False)
    sweeps[param] = df
    stab = sensitivity_stability_summary(df)
    stab.insert(0, "Parameter", param)
    stability_rows.append(stab)
    eff = df["team_effectiveness_mean"]
    print(f"  {param:32s} eff swing {eff.max()-eff.min():.3f}  "
          f"({eff.min():.3f} -> {eff.max():.3f})")

stability_df = pd.concat(stability_rows, ignore_index=True)
stability_df.to_csv(OUT / "sensitivity_stability_all.csv", index=False)

# importance ranking on team_effectiveness
ranking = (stability_df[stability_df["Outcome"] == "team_effectiveness"]
           .sort_values("Range", ascending=False)
           [["Parameter", "Min", "Max", "Range", "Stability"]])
ranking.to_csv(OUT / "sensitivity_importance_ranking.csv", index=False)
print("\nImportance ranking (effectiveness swing):")
print(ranking.to_string(index=False))

# AI reliability sweep with a fixed HIGH trust, to locate the benefit crossing
print("\n=== AI reliability crossing point (paired, trust fixed high) ===")
cross_rows = []
for rel in [round(v, 2) for v in np.linspace(0.20, 0.95, 16)]:
    cfg = replace(BASE, ai_reliability=rel, trust_in_ai=0.85, ai_support_level=0.80,
                  dashboard_quality=0.70)
    paired = paired_ai_benefit(cfg, reps=60)
    lo, hi = ci95(paired["eff_delta"])
    cross_rows.append({
        "ai_reliability": rel,
        "eff_delta": round(paired["eff_delta"].mean(), 4),
        "ci_low": round(lo, 4),
        "ci_high": round(hi, 4),
        "defect_delta": round(paired["defect_delta"].mean(), 4),
        "trust_calibration": round(paired["trust_calibration"].mean(), 3),
        "share_positive": round((paired["eff_delta"] > 0).mean(), 3),
    })
cross_df = pd.DataFrame(cross_rows)
cross_df.to_csv(OUT / "ai_reliability_crossing.csv", index=False)
print(cross_df.to_string(index=False))

report["files"] = sorted(p.name for p in OUT.glob("*.csv"))
(OUT / "run_report.json").write_text(json.dumps(report, indent=2))
print("\nDone. model_version =", MODEL_VERSION)
