"""Monotonicity checks: outcomes should move in the expected direction.

Deterministic metric-level checks are exact. Simulation-level trends are
averaged across several seeds and compared with a margin, because the engine
is stochastic.
"""

from dataclasses import replace

import pytest

from experiments import run_experiments
from metrics import (
    collective_intelligence_score,
    decision_quality_score,
    team_effectiveness_score,
)
from simulation import SimulationConfig
from tests.test_metrics import _components


@pytest.mark.parametrize(
    "component",
    [
        "transactive_memory",
        "shared_attention",
        "shared_reasoning",
        "social_sensitivity",
        "participation_balance",
        "transactive_coordination",
        "team_engagement",
        "skill_diversity",
    ],
)
def test_ci_increases_with_each_positive_component(component):
    low = collective_intelligence_score(_components(**{component: 0.2}))
    high = collective_intelligence_score(_components(**{component: 0.9}))
    assert high > low


def test_decision_quality_increases_with_reasoning():
    def score(reasoning):
        return decision_quality_score(
            collective_reasoning=reasoning,
            collective_attention=0.6,
            coordination_need=0.6,
            dashboard_quality=0.6,
            ai_support_level=0.6,
            use_ai=True,
            social_sensitivity=0.6,
            trust_calibration=0.8,
            task_strategy=0.6,
            skills_knowledge_coordination=0.6,
        )

    assert score(0.9) > score(0.3)


def test_team_effectiveness_increases_with_completion():
    low = team_effectiveness_score(0.5, 0.3, 0.2, 0.6, 0.6, 0.6, 0.6)
    high = team_effectiveness_score(0.5, 0.9, 0.2, 0.6, 0.6, 0.6, 0.6)
    assert high > low


def _mean_metric(config: SimulationConfig, metric: str, use_ai: bool = True) -> float:
    experiment = run_experiments(config, repetitions=12, use_ai=use_ai)
    stats = experiment["statistics"].set_index("Metric")
    return float(stats.loc[metric, "Mean"])


def test_more_dependencies_increase_blocked_tasks():
    # Dependency density manifests as blocked tasks (work that cannot start),
    # which is distinct from carry-over (committed work that did not finish).
    base = SimulationConfig(number_of_sprints=5, number_of_tasks=50, random_seed=7)
    low = _mean_metric(replace(base, dependency_density=0.0), "blocked_tasks")
    high = _mean_metric(replace(base, dependency_density=0.6), "blocked_tasks")
    assert high > low


def test_higher_complexity_increases_defect_rate():
    base = SimulationConfig(number_of_sprints=5, number_of_tasks=50, random_seed=11)
    low = _mean_metric(replace(base, task_complexity=0.3), "defect_rate")
    high = _mean_metric(replace(base, task_complexity=0.85), "defect_rate")
    assert high > low
