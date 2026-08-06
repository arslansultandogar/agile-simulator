from __future__ import annotations

from collections import defaultdict
from typing import Dict, List, Tuple

import numpy as np

from config_loader import AI_ALLOCATION, HUMAN_AI_TRUST
from team import TeamMember
from tasks import Task


def _clamp(value: float, minimum: float = 0.0, maximum: float = 1.0) -> float:
    return max(minimum, min(maximum, value))


def average_perceived_ai_reliability(team_members: List[TeamMember]) -> float:
    if not team_members:
        return 0.5

    return _clamp(
        sum(member.perceived_ai_reliability for member in team_members) / len(team_members)
    )


def update_team_trust_after_sprint(
    team_members: List[TeamMember],
    actual_ai_reliability: float,
    sprint_outcome_signal: float,
    use_ai: bool,
) -> None:
    """
    Learned trust moves toward actual AI reliability when outcomes are positive.
    """

    if not use_ai:
        return

    for member in team_members:
        outcome_effect = 0.04 * (sprint_outcome_signal - 0.5)
        calibration_effect = 0.03 * (actual_ai_reliability - member.perceived_ai_reliability)
        member.trust_in_ai = _clamp(member.trust_in_ai + outcome_effect + calibration_effect)
        # Learned trust: experience moves perception toward the AI's actual
        # reliability across sprints (Hoff & Bashir 2015). Miscalibration is
        # therefore a trajectory that self-corrects, not a fixed state.
        member.perceived_ai_reliability = _clamp(
            member.perceived_ai_reliability
            + (HUMAN_AI_TRUST["perceived_learning_rate"]
               * (actual_ai_reliability - member.perceived_ai_reliability))
        )


def allocate_tasks_with_ai(
    tasks: List[Task],
    team_members: List[TeamMember],
    ai_support_level: float,
    ai_reliability: float,
    rng: np.random.Generator,
) -> Tuple[Dict[int, int], Dict[int, float], float]:
    """
    AI Task Allocation Assistant.

    Allocation quality is reduced when AI reliability is imperfect. Low trust
    can also reduce uptake of AI advice.
    """

    assignments: Dict[int, int] = {}
    workloads = defaultdict(float)
    assignment_scores: List[float] = []

    ordered_tasks = sorted(
        tasks,
        key=lambda task: (-task.priority, -task.required_skill_level, task.uncertainty),
    )

    for task in ordered_tasks:
        ranked_members = []

        for member in team_members:
            skill_fit = 1.0 - abs(member.skill_level - task.required_skill_level)
            load_penalty = workloads[member.member_id] / max(1.0, member.availability * 14.0)
            balance_factor = max(0.0, 1.0 - load_penalty)

            score = (
                (0.45 * skill_fit)
                + (0.20 * member.availability)
                + (0.15 * balance_factor)
                + (0.20 * member.trust_in_ai)
            )
            ranked_members.append((score, member))

        ranked_members.sort(key=lambda item: item[0], reverse=True)
        if not ranked_members:
            continue

        best_score, best_member = ranked_members[0]
        chosen_member = best_member

        if len(ranked_members) > 1 and ai_reliability < 1.0:
            # Uptake is how strongly the team acts on the recommendation. High
            # trust means a wrong recommendation is more likely to be followed
            # (misuse / over-reliance: Parasuraman & Riley 1997; Bucinca 2021).
            uptake = ai_support_level * best_member.trust_in_ai
            mistake_probability = (1.0 - ai_reliability) * uptake
            if rng.random() < mistake_probability:
                # v2.1: a wrong recommendation picks from anywhere below the top
                # candidate, not merely the runner-up. Always choosing the
                # second-best made unreliable AI nearly as good as reliable AI.
                _, chosen_member = ranked_members[int(rng.integers(1, len(ranked_members)))]

        assignments[task.task_id] = chosen_member.member_id
        workloads[chosen_member.member_id] += task.effort_points
        assignment_scores.append(
            _clamp(
                best_score
                if chosen_member == best_member
                else best_score * AI_ALLOCATION["wrong_pick_score_factor"]
            )
        )

    average_quality = sum(assignment_scores) / len(assignment_scores) if assignment_scores else 0.0
    boosted_quality = _clamp(average_quality * (0.70 + (0.30 * ai_support_level)))
    # v2.1: the misallocation fallback sits BELOW the no-AI baseline quality, so
    # relying on an unreliable assistant can be worse than not using one. In
    # v2.0 this fallback was 0.45 against a 0.40 baseline, which floored AI
    # benefit positive regardless of reliability.
    reliability_adjusted_quality = _clamp(
        (ai_reliability * boosted_quality)
        + ((1.0 - ai_reliability) * AI_ALLOCATION["misallocation_quality"])
    )
    return assignments, dict(workloads), reliability_adjusted_quality


def allocate_tasks_without_ai(tasks: List[Task], team_members: List[TeamMember]) -> Tuple[Dict[int, int], Dict[int, float], float]:
    assignments: Dict[int, int] = {}
    workloads = defaultdict(float)

    ordered_members = sorted(team_members, key=lambda member: member.member_id)

    for task in sorted(tasks, key=lambda item: (-item.priority, item.effort_points)):
        best_member = min(
            ordered_members,
            key=lambda member: workloads[member.member_id] / max(0.5, member.availability),
        )
        assignments[task.task_id] = best_member.member_id
        workloads[best_member.member_id] += task.effort_points

    return assignments, dict(workloads), AI_ALLOCATION["baseline_quality"]


def shared_cognition_assistant(
    ai_support_level: float,
    dashboard_quality: float,
    coordination_need: float,
    collective_attention: float,
    collective_reasoning: float,
    ai_reliability: float,
    trust_calibration: float,
) -> Dict[str, float]:
    """
    AI Dashboard / Shared Cognition Assistant.

    Shared cognition gains are attenuated when trust is miscalibrated or AI
    reliability is low.
    """

    reliability_factor = _clamp((0.60 * ai_reliability) + (0.40 * trust_calibration))
    visibility_gain = ai_support_level * dashboard_quality * reliability_factor
    coordination_gain = _clamp(
        (0.45 * visibility_gain)
        + (0.25 * coordination_need)
        + (0.15 * collective_attention)
        + (0.15 * collective_reasoning)
    )
    decision_gain = _clamp(
        (0.60 * visibility_gain)
        + (0.20 * collective_attention)
        + (0.20 * coordination_need)
    )

    return {
        "visibility_gain": visibility_gain,
        "coordination_gain": coordination_gain,
        "decision_gain": decision_gain,
    }
