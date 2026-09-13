"""Supplementary Scenario A reliability sweep at a different AI support level.

Motivation: the main run (run_scenarios.py) found NO zero crossing of paired AI
benefit for Scenario A at ai_support_level 0.70. The thesis located a crossing
near 48% reliability at support 0.80 on the default process profile. This
script varies ONLY ai_support_level (default 0.80) with every other Scenario A
parameter unchanged, to test whether the crossing re-emerges - i.e. whether the
null over-trust harm in Scenario A is conditional on support level or on the
scenario's stronger process profile.

Same conventions as run_scenarios.py: 200 paired replications per point on
identical seeds (42+i), 95% CI = mean +/- 1.96*SE, v2.1 guard. Writes only new
files into results_scenarios/ (tagged by support level); nothing is overwritten.
"""

from __future__ import annotations

import json
import sys
import time
from dataclasses import replace
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

from config_loader import MODEL_VERSION, PERCEIVED_RELIABILITY_ANCHOR
from scenarios import build_config
from simulation import run_simulation

if MODEL_VERSION != "2.1.0" or PERCEIVED_RELIABILITY_ANCHOR != "trust":
    raise SystemExit(f"Refusing to run: MODEL_VERSION={MODEL_VERSION!r}, anchor={PERCEIVED_RELIABILITY_ANCHOR!r}")

_args = [a for a in sys.argv[1:] if not a.startswith("--")]
SUPPORT = float(_args[0]) if _args else 0.80
# --default-process: isolating test. Reset the four process parameters to the
# thesis/model defaults (0.65) so that, together with support 0.80, the only
# remaining differences from the thesis crossing run are Scenario A's team,
# backlog, schedule and CI-baseline settings.
DEFAULT_PROCESS = "--default-process" in sys.argv
PROCESS_OVERRIDE = ({"effort_management": 0.65, "skills_knowledge_coordination": 0.65,
                     "task_strategy": 0.65, "consequentiality": 0.65} if DEFAULT_PROCESS else {})
TAG = f"support{int(round(SUPPORT * 100)):03d}" + ("_defproc" if DEFAULT_PROCESS else "")
OUT = Path("results_scenarios"); OUT.mkdir(exist_ok=True)
REPS = 200
TRUST_LEVELS = (0.65, 0.85)
GRID_VALUES = [round(0.30 + 0.05 * k, 2) for k in range(14)]
SCENARIO = "A_safety_critical_embedded"


def ci95(s):
    s = pd.Series(s).astype(float); m = s.mean()
    if len(s) < 2: return m, m
    marg = 1.96 * s.std(ddof=1) / np.sqrt(len(s)); return m - marg, m + marg


def paired_runs(config, reps):
    rows = []
    for i in range(reps):
        trial = replace(config, random_seed=config.random_seed + i)
        w = run_simulation(trial, use_ai=True)["summary"]; wo = run_simulation(trial, use_ai=False)["summary"]
        rows.append({"seed": trial.random_seed,
                     "eff_delta": w["team_effectiveness"] - wo["team_effectiveness"],
                     "defect_delta": w["defect_rate"] - wo["defect_rate"],
                     "trust_calibration_with": w["trust_calibration"]})
    return pd.DataFrame(rows)


def summarise(series):
    s = pd.Series(series).astype(float); lo, hi = ci95(s)
    return {"mean": round(s.mean(), 4), "se": round(s.std(ddof=1) / np.sqrt(len(s)), 4),
            "ci_low": round(lo, 4), "ci_high": round(hi, 4), "share_positive": round((s > 0).mean(), 4)}


def zero_crossings(x, y):
    x = np.asarray(x, float); y = np.asarray(y, float); found = []
    for k in range(len(x) - 1):
        if y[k] == 0.0: found.append(float(x[k]))
        elif y[k] * y[k + 1] < 0: found.append(float(x[k] + (x[k + 1] - x[k]) * (-y[k]) / (y[k + 1] - y[k])))
    if len(y) and y[-1] == 0.0: found.append(float(x[-1]))
    return found


t0 = time.perf_counter()
base = replace(build_config(SCENARIO), ai_support_level=SUPPORT, **PROCESS_OVERRIDE)
print(f"=== Scenario A reliability sweep at ai_support_level={SUPPORT}"
      + (f", process reset to defaults {PROCESS_OVERRIDE}" if DEFAULT_PROCESS else "") + f" (N={REPS} paired per point) ===")
crossing_rows = []
for trust in TRUST_LEVELS:
    rows = []
    for rel in GRID_VALUES:
        df = paired_runs(replace(base, ai_reliability=rel, trust_in_ai=trust), REPS)
        e = summarise(df["eff_delta"]); d = summarise(df["defect_delta"])
        rows.append({"ai_support_level": SUPPORT, "trust_in_ai": trust, "ai_reliability": rel, "n": len(df),
                     "eff_delta": e["mean"], "eff_delta_se": e["se"], "ci_low": e["ci_low"], "ci_high": e["ci_high"],
                     "ci_excludes_zero": bool(e["ci_low"] > 0 or e["ci_high"] < 0), "share_positive": e["share_positive"],
                     "defect_delta": d["mean"], "trust_calibration_with": round(df["trust_calibration_with"].mean(), 3)})
    sw = pd.DataFrame(rows)
    ttag = f"trust{int(round(trust * 100)):03d}"
    sw.to_csv(OUT / f"sweep_reliability_A_{TAG}_{ttag}.csv", index=False)
    xs = zero_crossings(sw["ai_reliability"], sw["eff_delta"])
    crossing_rows.append({"ai_support_level": SUPPORT, "trust_in_ai": trust, "n_crossings": len(xs),
                          "first_crossing_reliability": round(xs[0], 4) if xs else None,
                          "all_crossings": ";".join(f"{x:.4f}" for x in xs),
                          "benefit_at_0.30": sw["eff_delta"].iloc[0], "benefit_at_0.95": sw["eff_delta"].iloc[-1],
                          "first_reliability_with_ci_above_zero": next((r for r, lo in zip(sw["ai_reliability"], sw["ci_low"]) if lo > 0), None),
                          "last_reliability_with_ci_below_zero": next((r for r, hi in zip(sw["ai_reliability"][::-1], sw["ci_high"][::-1]) if hi < 0), None)})
    print(f"  trust={trust:.2f}: " + ", ".join(f"{r:.2f}:{e:+.2f}" for r, e in zip(sw["ai_reliability"], sw["eff_delta"])))
    print(f"    zero crossings: {[round(x,3) for x in xs] if xs else 'none in range'}")
pd.DataFrame(crossing_rows).to_csv(OUT / f"sweep_zero_crossing_A_{TAG}.csv", index=False)

elapsed = time.perf_counter() - t0
rep = {"model_version": MODEL_VERSION, "perceived_reliability_anchor": PERCEIVED_RELIABILITY_ANCHOR,
       "scenario": SCENARIO, "ai_support_level": SUPPORT, "process_override": PROCESS_OVERRIDE,
       "changes_vs_main_run": ["ai_support_level"] + sorted(PROCESS_OVERRIDE),
       "repetitions": REPS, "seed_rule": "replication i uses 42 + i, identical within each pair and to the main run",
       "trust_levels": list(TRUST_LEVELS), "reliability_values": GRID_VALUES,
       "simulations_executed": 2 * REPS * len(TRUST_LEVELS) * len(GRID_VALUES),
       "elapsed_seconds": round(elapsed, 1), "finished_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
       "files": sorted(p.name for p in OUT.glob(f"*{TAG}*.csv"))}
(OUT / f"run_report_{TAG}.json").write_text(json.dumps(rep, indent=2, default=str))
print(f"\nDone in {elapsed:.0f}s, {rep['simulations_executed']} simulations, model {MODEL_VERSION}.")
