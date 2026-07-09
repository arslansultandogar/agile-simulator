"""Deterministic smoke tests for the simulation engine."""

import pandas as pd
import pytest

from config_loader import MODEL_VERSION
from simulation import SimulationConfig, run_simulation
from tasks import generate_mixed_backlog, normalize_task_mix, select_sprint_tasks
import numpy as np


def test_deterministic_same_seed():
    config = SimulationConfig(number_of_sprints=6, number_of_tasks=50, random_seed=123)
    first = run_simulation(config, use_ai=True)["results"]
    second = run_simulation(config, use_ai=True)["results"]
    pd.testing.assert_frame_equal(first, second)


def test_summary_has_model_version_and_new_metrics():
    config = SimulationConfig(number_of_sprints=4, number_of_tasks=30, random_seed=1)
    summary = run_simulation(config, use_ai=True)["summary"]
    assert summary["model_version"] == MODEL_VERSION
    for key in ("carry_over_rate", "blocked_tasks", "rework_created", "rework_completed"):
        assert key in summary


def test_completed_never_exceeds_planned():
    config = SimulationConfig(number_of_sprints=8, number_of_tasks=80, random_seed=5)
    results = run_simulation(config, use_ai=True)["results"]
    assert (results["Completed Points"] <= results["Planned Points"]).all()
    assert (results["Carry-Over Points"] >= 0).all()


def test_roles_assigned_to_team():
    config = SimulationConfig(team_size=6, number_of_sprints=2, random_seed=2)
    team = run_simulation(config, use_ai=True)["team"]
    roles = set(team["role"])
    assert "Product Owner" in roles
    assert "Scrum Master" in roles
    assert "Tester" in roles


def test_normalize_task_mix_sums_to_one():
    mix = normalize_task_mix({"feature": 50, "bug": 25, "refactor": 15, "spike": 10})
    assert pytest.approx(sum(mix.values()), abs=1e-9) == 1.0


def test_empty_mix_defaults_to_feature():
    assert normalize_task_mix({}) == {"feature": 1.0}
    assert normalize_task_mix({"feature": 0, "bug": 0}) == {"feature": 1.0}


def test_dependencies_block_until_completed():
    rng = np.random.default_rng(0)
    backlog = generate_mixed_backlog(
        number_of_tasks=10,
        task_complexity=0.5,
        task_mix={"feature": 1.0},
        rng=rng,
        dependency_density=1.0,
    )
    # Every task except the first has a dependency, so with nothing completed
    # only unblocked (dependency-free) tasks can be selected.
    selected = select_sprint_tasks(backlog, sprint_capacity_points=999, completed_ids=set(), sprint_number=1)
    for task in selected:
        assert task.depends_on == []


def test_disabling_rework_creates_no_fix_tasks():
    config = SimulationConfig(
        number_of_sprints=6,
        number_of_tasks=60,
        task_complexity=0.8,
        enable_rework=False,
        random_seed=9,
    )
    summary = run_simulation(config, use_ai=False)["summary"]
    assert summary["rework_created"] == 0.0
