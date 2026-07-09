from __future__ import annotations

from dataclasses import asdict, replace
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd

from simulation import SimulationConfig, run_simulation

SUMMARY_METRICS = [
    "average_velocity",
    "completion_rate",
    "defect_rate",
    "decision_quality",
    "collective_intelligence",
    "team_effectiveness",
    "ai_benefit",
    "trust_calibration",
    "transactive_memory",
    "shared_attention",
    "shared_reasoning",
    "social_sensitivity",
    "participation_balance",
    "team_engagement",
    "skill_diversity",
    "age_diversity",
    "effort_management",
    "skills_knowledge_coordination",
    "task_strategy",
    "consequentiality",
    "overload_pressure",
    "team_viability",
    "member_sustainability",
    "carry_over_points",
    "carry_over_rate",
    "blocked_tasks",
    "rework_created",
    "rework_completed",
    "defects_caught_in_review",
]

SENSITIVITY_PARAMETERS = {
    "trust_in_ai": "Trust in AI",
    "ai_support_level": "AI support level",
    "ai_reliability": "AI reliability",
    "effort_management": "Effort-related process",
    "skills_knowledge_coordination": "Knowledge / skills process",
    "task_strategy": "Strategy updating process",
    "consequentiality": "Consequentiality / shared purpose",
    "female_proportion": "Female proportion",
    "team_engagement_baseline": "Initial team engagement",
    "dashboard_quality": "Dashboard quality",
    "collective_memory": "Collective / shared memory (CI baseline)",
    "collective_attention": "Collective focus of attention (CI baseline)",
    "collective_reasoning": "Collective reasoning (CI baseline)",
    "task_complexity": "Task complexity",
    "dependency_density": "Dependency density (blockers)",
}

# Outcome metrics tracked across a sensitivity sweep.
SENSITIVITY_OUTPUT_METRICS = (
    "team_effectiveness",
    "collective_intelligence",
    "team_viability",
    "member_sustainability",
    "defect_rate",
    "trust_calibration",
    "carry_over_rate",
    "rework_created",
)


def _confidence_interval(values: pd.Series, confidence: float = 0.95) -> Tuple[float, float]:
    if values.empty:
        return 0.0, 0.0

    mean = float(values.mean())
    if len(values) == 1:
        return mean, mean

    std_error = float(values.std(ddof=1) / np.sqrt(len(values)))
    margin = 1.96 * std_error
    return mean - margin, mean + margin


def summarize_experiment_results(results_df: pd.DataFrame) -> pd.DataFrame:
    rows: List[Dict[str, float | str]] = []

    for metric in SUMMARY_METRICS:
        if metric not in results_df.columns:
            continue

        series = results_df[metric]
        ci_low, ci_high = _confidence_interval(series)
        rows.append(
            {
                "Metric": metric,
                "Mean": round(float(series.mean()), 3),
                "Std Dev": round(float(series.std(ddof=0)), 3),
                "Min": round(float(series.min()), 3),
                "Max": round(float(series.max()), 3),
                "95% CI Low": round(ci_low, 3),
                "95% CI High": round(ci_high, 3),
            }
        )

    return pd.DataFrame(rows)


def run_experiments(
    config: SimulationConfig,
    repetitions: int = 100,
    use_ai: bool = True,
    seed_offset: int = 0,
) -> Dict[str, object]:
    """
    Run many stochastic replications and summarize distributional outcomes.
    """

    rows: List[Dict[str, float | int | bool]] = []

    for index in range(repetitions):
        trial_config = replace(config, random_seed=config.random_seed + seed_offset + index)
        result = run_simulation(trial_config, use_ai=use_ai)
        row = {"seed": trial_config.random_seed, "use_ai": use_ai, **result["summary"]}
        rows.append(row)

    results_df = pd.DataFrame(rows)
    stats_df = summarize_experiment_results(results_df)

    return {
        "config": asdict(config),
        "repetitions": repetitions,
        "use_ai": use_ai,
        "results": results_df,
        "statistics": stats_df,
    }


def compare_scenarios(
    config: SimulationConfig,
    repetitions: int = 100,
) -> Dict[str, object]:
    with_ai = run_experiments(config, repetitions=repetitions, use_ai=True)
    without_ai = run_experiments(config, repetitions=repetitions, use_ai=False, seed_offset=100_000)

    comparison_rows: List[Dict[str, float | str]] = []
    ai_stats = with_ai["statistics"].set_index("Metric")
    baseline_stats = without_ai["statistics"].set_index("Metric")

    for metric in SUMMARY_METRICS:
        if metric not in ai_stats.index or metric not in baseline_stats.index:
            continue

        ai_mean = float(ai_stats.loc[metric, "Mean"])
        baseline_mean = float(baseline_stats.loc[metric, "Mean"])
        comparison_rows.append(
            {
                "Metric": metric,
                "With AI Mean": ai_mean,
                "Without AI Mean": baseline_mean,
                "Difference": round(ai_mean - baseline_mean, 3),
            }
        )

    return {
        "with_ai": with_ai,
        "without_ai": without_ai,
        "comparison": pd.DataFrame(comparison_rows),
    }


def run_sensitivity_analysis(
    base_config: SimulationConfig,
    parameter_name: str,
    values: List[float],
    repetitions: int = 25,
    use_ai: bool = True,
) -> pd.DataFrame:
    """
    Vary one parameter and measure how summary metrics change on average.
    """

    if parameter_name not in SENSITIVITY_PARAMETERS:
        raise ValueError(f"Unsupported sensitivity parameter: {parameter_name}")

    rows: List[Dict[str, float | str]] = []

    for value in values:
        trial_config = replace(base_config, **{parameter_name: value})
        experiment = run_experiments(trial_config, repetitions=repetitions, use_ai=use_ai)
        stats = experiment["statistics"].set_index("Metric")

        row: Dict[str, float | str] = {
            "parameter": parameter_name,
            "parameter_label": SENSITIVITY_PARAMETERS[parameter_name],
            "value": round(value, 3),
            "value_percent": round(value * 100, 1),
        }

        for metric in SENSITIVITY_OUTPUT_METRICS:
            if metric in stats.index:
                row[f"{metric}_mean"] = float(stats.loc[metric, "Mean"])

        rows.append(row)

    return pd.DataFrame(rows)


def sensitivity_stability_summary(sensitivity_df: pd.DataFrame) -> pd.DataFrame:
    """Summarize how stable each outcome is across a sensitivity sweep (Week 4).

    For every tracked outcome metric this reports the swing (max - min), the
    standard deviation, and a normalized stability score in [0, 1] where higher
    means the outcome is less sensitive to the swept parameter.
    """

    if sensitivity_df.empty:
        return pd.DataFrame(
            columns=["Outcome", "Min", "Max", "Range", "Std Dev", "Stability"]
        )

    rows: List[Dict[str, float | str]] = []
    for metric in SENSITIVITY_OUTPUT_METRICS:
        column = f"{metric}_mean"
        if column not in sensitivity_df.columns:
            continue

        series = sensitivity_df[column].astype(float)
        minimum = float(series.min())
        maximum = float(series.max())
        value_range = maximum - minimum
        std_dev = float(series.std(ddof=0))
        scale = max(abs(maximum), abs(minimum), 1e-9)
        stability = round(1.0 - min(1.0, value_range / scale), 3)

        rows.append(
            {
                "Outcome": metric,
                "Min": round(minimum, 3),
                "Max": round(maximum, 3),
                "Range": round(value_range, 3),
                "Std Dev": round(std_dev, 3),
                "Stability": stability,
            }
        )

    return pd.DataFrame(rows)
