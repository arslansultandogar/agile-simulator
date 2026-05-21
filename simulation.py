from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Dict, List

import pandas as pd
import numpy as np

from ai_support import (
    allocate_tasks_with_ai,
    allocate_tasks_without_ai,
    average_perceived_ai_reliability,
    shared_cognition_assistant,
    update_team_trust_after_sprint,
)
from metrics import (
    ai_benefit_score,
    clamp,
    collective_intelligence_score,
    compute_collective_intelligence_components,
    decision_quality_score,
    team_effectiveness_score,
    trust_calibration_score,
)
from tasks import (
    DEFAULT_TASK_TYPE,
    Task,
    average_coordination_need,
    generate_backlog,
    get_task_type_profile,
    select_sprint_tasks,
)
from team import TeamMember, generate_team


@dataclass
class SimulationConfig:
    team_size: int = 6
    number_of_sprints: int = 8
    number_of_tasks: int = 60
    task_type: str = DEFAULT_TASK_TYPE
    ai_support_level: float = 0.70
    trust_in_ai: float = 0.65
    ai_reliability: float = 0.78
    task_complexity: float = 0.58
    dashboard_quality: float = 0.70
    collective_memory: float = 0.62
    collective_attention: float = 0.60
    collective_reasoning: float = 0.64
    random_seed: int = 42


def _planned_capacity_points(team_members: List[TeamMember]) -> int:
    capacity = 0.0

    for member in team_members:
        capacity += 8.0 * member.availability * member.work_speed * (0.80 + (0.20 * member.skill_level))

    return max(1, int(round(capacity)))


def _find_member(team_members: List[TeamMember], member_id: int) -> TeamMember:
    for member in team_members:
        if member.member_id == member_id:
            return member
    raise ValueError(f"Unknown team member id: {member_id}")


def _task_completion_probability(
    member: TeamMember,
    task: Task,
    workload_points: float,
    planned_capacity_points: int,
    team_size: int,
    collective_intelligence: float,
    decision_quality: float,
    ai_support_level: float,
    dashboard_quality: float,
    use_ai: bool,
    trust_calibration: float,
) -> float:
    profile = get_task_type_profile(task.task_type)
    coordination_need = float(profile["coordination_need"])
    completion_bonus = float(profile["completion_bonus"])

    skill_fit = 1.0 - abs(member.skill_level - task.required_skill_level)
    expected_individual_capacity = planned_capacity_points / max(1, team_size)
    overload_ratio = workload_points / max(1.0, expected_individual_capacity)
    overload_penalty = max(0.0, overload_ratio - 1.0) * 0.12
    ai_bonus = ai_support_level * dashboard_quality * member.trust_in_ai * trust_calibration if use_ai else 0.0

    probability = (
        0.18
        + (0.18 * member.skill_level)
        + (0.10 * member.availability)
        + (0.08 * member.work_speed)
        + (0.10 * member.communication_level)
        + (0.12 * skill_fit)
        + (0.10 * collective_intelligence)
        + (0.08 * decision_quality)
        + (0.06 * coordination_need)
        + completion_bonus
        + (0.08 * ai_bonus)
        - (0.14 * task.difficulty)
        - (0.08 * task.uncertainty)
        - overload_penalty
    )

    return clamp(probability, 0.05, 0.98)


def _task_defect_probability(
    member: TeamMember,
    task: Task,
    decision_quality: float,
    ai_support_level: float,
    dashboard_quality: float,
    use_ai: bool,
    trust_calibration: float,
    skill_fit: float,
) -> float:
    profile = get_task_type_profile(task.task_type)
    defect_risk = float(profile["defect_risk"])

    ai_quality_bonus = ai_support_level * dashboard_quality * trust_calibration if use_ai else 0.0
    misfit_penalty = max(0.0, 0.10 - (0.10 * skill_fit)) if use_ai and trust_calibration < 0.75 else 0.0

    probability = (
        0.08
        + (0.24 * member.error_tendency)
        + (0.18 * task.difficulty)
        + (0.12 * task.uncertainty)
        + (0.10 * defect_risk)
        - (0.10 * decision_quality)
        - (0.08 * ai_quality_bonus)
        + misfit_penalty
    )

    return clamp(probability, 0.01, 0.75)


def _update_collective_dimension(
    current_value: float,
    coordination_need: float,
    dashboard_quality: float,
    decision_quality: float,
    outcome_signal: float,
    use_ai: bool,
    ai_support_level: float,
) -> float:
    ai_learning_bonus = 0.01 * ai_support_level if use_ai else 0.0
    change = (
        0.02 * (coordination_need - 0.5)
        + 0.02 * (dashboard_quality - 0.5)
        + 0.03 * (decision_quality - 0.5)
        + 0.03 * (outcome_signal - 0.5)
        + ai_learning_bonus
    )
    return clamp(current_value + change, 0.0, 1.0)


def run_simulation(config: SimulationConfig, use_ai: bool = True) -> Dict[str, object]:
    rng = np.random.default_rng(config.random_seed)

    team_members = generate_team(
        team_size=config.team_size,
        trust_in_ai=config.trust_in_ai,
        ai_reliability=config.ai_reliability,
        rng=rng,
    )
    backlog = generate_backlog(
        number_of_tasks=config.number_of_tasks,
        task_complexity=config.task_complexity,
        task_type=config.task_type,
        rng=rng,
    )

    collective_memory = config.collective_memory
    collective_attention = config.collective_attention
    collective_reasoning = config.collective_reasoning

    sprint_records: List[Dict[str, float]] = []
    ci_component_history: List[Dict[str, float]] = []

    for sprint_number in range(1, config.number_of_sprints + 1):
        if not backlog:
            break

        sprint_capacity_points = _planned_capacity_points(team_members)
        sprint_tasks = select_sprint_tasks(backlog, sprint_capacity_points)
        planned_points = sum(task.effort_points for task in sprint_tasks)
        sprint_coordination_need = average_coordination_need(sprint_tasks)

        perceived_ai_reliability = average_perceived_ai_reliability(team_members)
        trust_calibration = trust_calibration_score(
            perceived_ai_reliability=perceived_ai_reliability,
            actual_ai_reliability=config.ai_reliability,
        )

        if use_ai:
            assignments, workloads, allocation_quality = allocate_tasks_with_ai(
                tasks=sprint_tasks,
                team_members=team_members,
                ai_support_level=config.ai_support_level,
                ai_reliability=config.ai_reliability,
                rng=rng,
            )
            assistant_effect = shared_cognition_assistant(
                ai_support_level=config.ai_support_level,
                dashboard_quality=config.dashboard_quality,
                coordination_need=sprint_coordination_need,
                collective_attention=collective_attention,
                collective_reasoning=collective_reasoning,
                ai_reliability=config.ai_reliability,
                trust_calibration=trust_calibration,
            )
        else:
            assignments, workloads, allocation_quality = allocate_tasks_without_ai(
                tasks=sprint_tasks,
                team_members=team_members,
            )
            assistant_effect = {
                "visibility_gain": 0.0,
                "coordination_gain": config.dashboard_quality * 0.20,
                "decision_gain": config.dashboard_quality * 0.10,
            }

        ci_components = compute_collective_intelligence_components(
            collective_memory=collective_memory,
            collective_attention=collective_attention,
            collective_reasoning=collective_reasoning,
            coordination_need=sprint_coordination_need,
            team_members=team_members,
        )
        collective_intelligence = collective_intelligence_score(ci_components)

        decision_quality = decision_quality_score(
            collective_reasoning=collective_reasoning,
            collective_attention=collective_attention,
            coordination_need=sprint_coordination_need,
            dashboard_quality=config.dashboard_quality,
            ai_support_level=config.ai_support_level + assistant_effect["decision_gain"],
            use_ai=use_ai,
            social_sensitivity=ci_components.social_sensitivity,
            trust_calibration=trust_calibration,
        )

        completed_tasks = 0
        completed_points = 0
        total_defects = 0
        finished_task_ids: List[int] = []

        for task in sprint_tasks:
            member = _find_member(team_members, assignments[task.task_id])
            workload_points = workloads.get(member.member_id, 0.0)
            skill_fit = 1.0 - abs(member.skill_level - task.required_skill_level)

            completion_probability = _task_completion_probability(
                member=member,
                task=task,
                workload_points=workload_points,
                planned_capacity_points=sprint_capacity_points,
                team_size=config.team_size,
                collective_intelligence=collective_intelligence,
                decision_quality=decision_quality,
                ai_support_level=config.ai_support_level,
                dashboard_quality=config.dashboard_quality,
                use_ai=use_ai,
                trust_calibration=trust_calibration,
            )

            if rng.random() <= completion_probability:
                completed_tasks += 1
                completed_points += task.effort_points
                finished_task_ids.append(task.task_id)

                defect_probability = _task_defect_probability(
                    member=member,
                    task=task,
                    decision_quality=decision_quality,
                    ai_support_level=config.ai_support_level,
                    dashboard_quality=config.dashboard_quality,
                    use_ai=use_ai,
                    trust_calibration=trust_calibration,
                    skill_fit=skill_fit,
                )

                if rng.random() <= defect_probability:
                    total_defects += 1

        backlog = [task for task in backlog if task.task_id not in finished_task_ids]

        completion_rate = completed_tasks / len(sprint_tasks) if sprint_tasks else 0.0
        defect_rate = total_defects / completed_tasks if completed_tasks else 0.0
        velocity_ratio = completed_points / planned_points if planned_points else 0.0

        outcome_signal = clamp(
            (0.45 * completion_rate)
            + (0.35 * velocity_ratio)
            + (0.20 * (1.0 - defect_rate))
        )

        update_team_trust_after_sprint(
            team_members=team_members,
            actual_ai_reliability=config.ai_reliability,
            sprint_outcome_signal=outcome_signal,
            use_ai=use_ai,
        )

        collective_memory = _update_collective_dimension(
            current_value=collective_memory,
            coordination_need=sprint_coordination_need,
            dashboard_quality=config.dashboard_quality,
            decision_quality=decision_quality,
            outcome_signal=outcome_signal,
            use_ai=use_ai,
            ai_support_level=config.ai_support_level,
        )
        collective_attention = _update_collective_dimension(
            current_value=collective_attention,
            coordination_need=sprint_coordination_need,
            dashboard_quality=config.dashboard_quality + assistant_effect["coordination_gain"] * 0.10,
            decision_quality=decision_quality,
            outcome_signal=outcome_signal,
            use_ai=use_ai,
            ai_support_level=config.ai_support_level,
        )
        collective_reasoning = _update_collective_dimension(
            current_value=collective_reasoning,
            coordination_need=sprint_coordination_need,
            dashboard_quality=config.dashboard_quality,
            decision_quality=decision_quality + assistant_effect["decision_gain"] * 0.10,
            outcome_signal=outcome_signal,
            use_ai=use_ai,
            ai_support_level=config.ai_support_level,
        )

        ci_components_after_update = compute_collective_intelligence_components(
            collective_memory=collective_memory,
            collective_attention=collective_attention,
            collective_reasoning=collective_reasoning,
            coordination_need=sprint_coordination_need,
            team_members=team_members,
        )
        collective_intelligence_after_update = collective_intelligence_score(ci_components_after_update)

        team_effectiveness = team_effectiveness_score(
            velocity_ratio=velocity_ratio,
            completion_rate=completion_rate,
            defect_rate=defect_rate,
            decision_quality=decision_quality,
            collective_intelligence=collective_intelligence_after_update,
        )

        ai_benefit = ai_benefit_score(
            use_ai=use_ai,
            ai_support_level=config.ai_support_level,
            allocation_quality=allocation_quality,
            coordination_gain=assistant_effect["coordination_gain"],
            decision_gain=assistant_effect["decision_gain"],
            trust_calibration=trust_calibration,
        )

        ci_component_history.append(
            {
                "Sprint": sprint_number,
                "Scenario": "With AI support" if use_ai else "Without AI support",
                **{key: round(value * 100, 2) for key, value in ci_components_after_update.as_dict().items()},
            }
        )

        sprint_records.append(
            {
                "Sprint": sprint_number,
                "Scenario": "With AI support" if use_ai else "Without AI support",
                "Task Type": config.task_type,
                "Planned Points": planned_points,
                "Completed Points": completed_points,
                "Tasks Selected": len(sprint_tasks),
                "Tasks Completed": completed_tasks,
                "Defects": total_defects,
                "Sprint Velocity": completed_points,
                "Task Completion Rate": round(completion_rate * 100, 2),
                "Defect Rate": round(defect_rate * 100, 2),
                "Decision Quality": round(decision_quality * 100, 2),
                "Collective Intelligence Score": round(collective_intelligence_after_update * 100, 2),
                "Transactive Memory": round(ci_components_after_update.transactive_memory * 100, 2),
                "Social Sensitivity": round(ci_components_after_update.social_sensitivity * 100, 2),
                "Participation Balance": round(ci_components_after_update.participation_balance * 100, 2),
                "Trust Calibration": round(trust_calibration * 100, 2),
                "Team Effectiveness Score": round(team_effectiveness, 2),
                "AI Benefit Score": round(ai_benefit, 2),
                "Backlog Remaining": len(backlog),
            }
        )

    results_df = pd.DataFrame(sprint_records)
    ci_components_df = pd.DataFrame(ci_component_history)

    if results_df.empty:
        summary = {
            "average_velocity": 0.0,
            "completion_rate": 0.0,
            "defect_rate": 0.0,
            "decision_quality": 0.0,
            "collective_intelligence": 0.0,
            "team_effectiveness": 0.0,
            "ai_benefit": 0.0,
            "trust_calibration": 0.0,
            "transactive_memory": 0.0,
            "social_sensitivity": 0.0,
            "participation_balance": 0.0,
        }
    else:
        summary = {
            "average_velocity": float(results_df["Sprint Velocity"].mean()),
            "completion_rate": float(results_df["Task Completion Rate"].mean()),
            "defect_rate": float(results_df["Defect Rate"].mean()),
            "decision_quality": float(results_df["Decision Quality"].mean()),
            "collective_intelligence": float(results_df["Collective Intelligence Score"].mean()),
            "team_effectiveness": float(results_df["Team Effectiveness Score"].mean()),
            "ai_benefit": float(results_df["AI Benefit Score"].mean()),
            "trust_calibration": float(results_df["Trust Calibration"].mean()),
            "transactive_memory": float(results_df["Transactive Memory"].mean()),
            "social_sensitivity": float(results_df["Social Sensitivity"].mean()),
            "participation_balance": float(results_df["Participation Balance"].mean()),
        }

    return {
        "config": asdict(config),
        "team": pd.DataFrame([asdict(member) for member in team_members]),
        "results": results_df,
        "ci_components": ci_components_df,
        "summary": summary,
    }
