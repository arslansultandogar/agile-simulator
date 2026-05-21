from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

import numpy as np


TASK_TYPE_PROFILES: Dict[str, Dict[str, float | str]] = {
    "feature": {
        "label": "Feature",
        "coordination_need": 0.75,
        "defect_risk": 0.55,
        "uncertainty_modifier": 0.10,
        "skill_demand": 0.65,
        "completion_bonus": 0.02,
    },
    "bug": {
        "label": "Bug fix",
        "coordination_need": 0.50,
        "defect_risk": 0.35,
        "uncertainty_modifier": 0.05,
        "skill_demand": 0.55,
        "completion_bonus": 0.04,
    },
    "refactor": {
        "label": "Refactor",
        "coordination_need": 0.60,
        "defect_risk": 0.45,
        "uncertainty_modifier": 0.08,
        "skill_demand": 0.70,
        "completion_bonus": 0.01,
    },
    "spike": {
        "label": "Spike / Research",
        "coordination_need": 0.40,
        "defect_risk": 0.25,
        "uncertainty_modifier": 0.20,
        "skill_demand": 0.60,
        "completion_bonus": 0.00,
    },
}

DEFAULT_TASK_TYPE = "feature"


@dataclass
class Task:
    """Represents one backlog item."""

    task_id: int
    task_type: str
    difficulty: float
    effort_points: int
    priority: int
    uncertainty: float
    required_skill_level: float


def _clamp(value: float, minimum: float = 0.0, maximum: float = 1.0) -> float:
    return max(minimum, min(maximum, value))


def normalize_task_type(task_type: str) -> str:
    normalized = task_type.lower().strip()
    if normalized not in TASK_TYPE_PROFILES:
        raise ValueError(f"Unsupported task type: {task_type}")
    return normalized


def get_task_type_profile(task_type: str) -> Dict[str, float | str]:
    return TASK_TYPE_PROFILES[normalize_task_type(task_type)]


def average_coordination_need(tasks: List[Task]) -> float:
    if not tasks:
        return get_task_type_profile(DEFAULT_TASK_TYPE)["coordination_need"]  # type: ignore[return-value]

    total = sum(float(get_task_type_profile(task.task_type)["coordination_need"]) for task in tasks)
    return _clamp(total / len(tasks))


def generate_backlog(
    number_of_tasks: int,
    task_complexity: float,
    task_type: str,
    rng: np.random.Generator,
) -> List[Task]:
    """
    Build an abstract backlog for a selected task type.

    Task type shapes coordination need, defect risk, uncertainty, and required skill.
    """

    normalized_type = normalize_task_type(task_type)
    profile = get_task_type_profile(normalized_type)
    defect_risk = float(profile["defect_risk"])
    uncertainty_modifier = float(profile["uncertainty_modifier"])
    skill_demand = float(profile["skill_demand"])

    backlog: List[Task] = []

    for task_id in range(1, number_of_tasks + 1):
        difficulty = _clamp(rng.normal(task_complexity + (defect_risk * 0.10), 0.12))
        uncertainty = _clamp(rng.normal((task_complexity * 0.7) + uncertainty_modifier, 0.12))
        required_skill_level = _clamp(rng.normal((difficulty * 0.8) + (skill_demand * 0.15), 0.10))
        effort_points = int(np.clip(round(1 + (difficulty * 12) + rng.integers(0, 3)), 1, 13))
        priority = int(rng.integers(1, 6))

        backlog.append(
            Task(
                task_id=task_id,
                task_type=normalized_type,
                difficulty=difficulty,
                effort_points=effort_points,
                priority=priority,
                uncertainty=uncertainty,
                required_skill_level=required_skill_level,
            )
        )

    return backlog


def select_sprint_tasks(backlog: List[Task], sprint_capacity_points: int) -> List[Task]:
    ordered_backlog = sorted(
        backlog,
        key=lambda task: (-task.priority, task.uncertainty, task.effort_points),
    )

    selected: List[Task] = []
    used_points = 0

    for task in ordered_backlog:
        if used_points >= sprint_capacity_points and selected:
            break

        selected.append(task)
        used_points += task.effort_points

    return selected
