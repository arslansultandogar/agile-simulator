from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Set

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

# Default proportions for a mixed backlog (Week 2). Proportions are normalized
# before use, so they only need to be relative weights.
DEFAULT_TASK_MIX: Dict[str, float] = {
    "feature": 0.50,
    "bug": 0.25,
    "refactor": 0.15,
    "spike": 0.10,
}


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
    # Week 3: ids of tasks that must be completed before this one can start.
    depends_on: List[int] = field(default_factory=list)
    # Week 3: rework follow-ups created when a completed task ships a defect.
    is_rework: bool = False
    origin_task_id: int | None = None
    # Sprint in which the task became available (rework appears in later sprints).
    available_from_sprint: int = 1


def _clamp(value: float, minimum: float = 0.0, maximum: float = 1.0) -> float:
    return max(minimum, min(maximum, value))


def normalize_task_type(task_type: str) -> str:
    normalized = task_type.lower().strip()
    if normalized not in TASK_TYPE_PROFILES:
        raise ValueError(f"Unsupported task type: {task_type}")
    return normalized


def get_task_type_profile(task_type: str) -> Dict[str, float | str]:
    return TASK_TYPE_PROFILES[normalize_task_type(task_type)]


def normalize_task_mix(task_mix: Dict[str, float] | None) -> Dict[str, float]:
    """Return a task-type mix whose proportions sum to 1.0.

    Unknown types are dropped and missing types default to 0. If the supplied
    mix is empty or sums to zero we fall back to a single-type feature backlog.
    """

    if not task_mix:
        return {"feature": 1.0}

    cleaned: Dict[str, float] = {}
    for task_type, proportion in task_mix.items():
        try:
            normalized_type = normalize_task_type(task_type)
        except ValueError:
            continue
        value = max(0.0, float(proportion))
        cleaned[normalized_type] = cleaned.get(normalized_type, 0.0) + value

    total = sum(cleaned.values())
    if total <= 0.0:
        return {"feature": 1.0}

    return {task_type: value / total for task_type, value in cleaned.items()}


def average_coordination_need(tasks: List[Task]) -> float:
    if not tasks:
        return get_task_type_profile(DEFAULT_TASK_TYPE)["coordination_need"]  # type: ignore[return-value]

    total = sum(float(get_task_type_profile(task.task_type)["coordination_need"]) for task in tasks)
    return _clamp(total / len(tasks))


def _build_task(
    task_id: int,
    task_type: str,
    task_complexity: float,
    rng: np.random.Generator,
) -> Task:
    profile = get_task_type_profile(task_type)
    defect_risk = float(profile["defect_risk"])
    uncertainty_modifier = float(profile["uncertainty_modifier"])
    skill_demand = float(profile["skill_demand"])

    difficulty = _clamp(rng.normal(task_complexity + (defect_risk * 0.10), 0.12))
    uncertainty = _clamp(rng.normal((task_complexity * 0.7) + uncertainty_modifier, 0.12))
    required_skill_level = _clamp(rng.normal((difficulty * 0.8) + (skill_demand * 0.15), 0.10))
    effort_points = int(np.clip(round(1 + (difficulty * 12) + rng.integers(0, 3)), 1, 13))
    priority = int(rng.integers(1, 6))

    return Task(
        task_id=task_id,
        task_type=task_type,
        difficulty=difficulty,
        effort_points=effort_points,
        priority=priority,
        uncertainty=uncertainty,
        required_skill_level=required_skill_level,
    )


def _assign_dependencies(
    backlog: List[Task],
    dependency_density: float,
    rng: np.random.Generator,
) -> None:
    """Assign at most one upstream dependency to some tasks.

    Dependencies always point to an earlier task id, which guarantees an
    acyclic ordering. Density controls the share of tasks that get blocked by
    an upstream item.
    """

    density = _clamp(dependency_density)
    if density <= 0.0 or len(backlog) < 2:
        return

    for index in range(1, len(backlog)):
        if rng.random() < density:
            upstream = backlog[int(rng.integers(0, index))]
            backlog[index].depends_on = [upstream.task_id]


def generate_mixed_backlog(
    number_of_tasks: int,
    task_complexity: float,
    task_mix: Dict[str, float] | None,
    rng: np.random.Generator,
    dependency_density: float = 0.0,
) -> List[Task]:
    """Build a backlog that mixes several task types by proportion (Week 2).

    Optionally wires lightweight task dependencies (Week 3).
    """

    normalized_mix = normalize_task_mix(task_mix)
    types = list(normalized_mix.keys())
    probabilities = np.array([normalized_mix[task_type] for task_type in types], dtype=float)
    probabilities = probabilities / probabilities.sum()

    backlog: List[Task] = []
    for task_id in range(1, number_of_tasks + 1):
        chosen_type = types[int(rng.choice(len(types), p=probabilities))]
        backlog.append(_build_task(task_id, chosen_type, task_complexity, rng))

    _assign_dependencies(backlog, dependency_density, rng)
    return backlog


def generate_backlog(
    number_of_tasks: int,
    task_complexity: float,
    task_type: str,
    rng: np.random.Generator,
) -> List[Task]:
    """Build a single-task-type backlog (kept for backward compatibility)."""

    normalized_type = normalize_task_type(task_type)
    return generate_mixed_backlog(
        number_of_tasks=number_of_tasks,
        task_complexity=task_complexity,
        task_mix={normalized_type: 1.0},
        rng=rng,
        dependency_density=0.0,
    )


def create_fix_task(
    origin: Task,
    new_task_id: int,
    available_from_sprint: int,
    rng: np.random.Generator,
) -> Task:
    """Create a rework/bug-fix follow-up for a completed task that shipped a defect.

    The fix task appears in a later sprint and inherits, in a slightly reduced
    form, the difficulty of the work that produced the defect.
    """

    difficulty = _clamp(origin.difficulty * float(rng.normal(0.85, 0.05)))
    uncertainty = _clamp(origin.uncertainty * 0.8)
    required_skill_level = _clamp(origin.required_skill_level * 0.95)
    effort_points = int(np.clip(round(max(1, origin.effort_points * 0.5)), 1, 8))

    return Task(
        task_id=new_task_id,
        task_type="bug",
        difficulty=difficulty,
        effort_points=effort_points,
        priority=5,  # rework is prioritized highly
        uncertainty=uncertainty,
        required_skill_level=required_skill_level,
        is_rework=True,
        origin_task_id=origin.task_id,
        available_from_sprint=available_from_sprint,
    )


def is_unblocked(task: Task, completed_ids: Set[int]) -> bool:
    """A task can be worked only once all of its dependencies are completed."""

    return all(dependency in completed_ids for dependency in task.depends_on)


def select_sprint_tasks(
    backlog: List[Task],
    sprint_capacity_points: int,
    completed_ids: Set[int] | None = None,
    sprint_number: int = 1,
) -> List[Task]:
    """Select tasks for a sprint, skipping blocked or not-yet-available items."""

    completed_ids = completed_ids or set()

    eligible = [
        task
        for task in backlog
        if task.available_from_sprint <= sprint_number and is_unblocked(task, completed_ids)
    ]

    ordered_backlog = sorted(
        eligible,
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
