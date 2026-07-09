from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Dict, List, Set

import pandas as pd
import numpy as np

from ai_support import (
    allocate_tasks_with_ai,
    allocate_tasks_without_ai,
    average_perceived_ai_reliability,
    shared_cognition_assistant,
    update_team_trust_after_sprint,
)
from config_loader import MODEL_VERSION
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
    DEFAULT_TASK_MIX,
    DEFAULT_TASK_TYPE,
    Task,
    average_coordination_need,
    create_fix_task,
    generate_mixed_backlog,
    get_task_type_profile,
    is_unblocked,
    normalize_task_mix,
    select_sprint_tasks,
)
from team import TeamMember, generate_team, role_effects


@dataclass
class SimulationConfig:
    team_size: int = 6
    number_of_sprints: int = 8
    number_of_tasks: int = 60
    task_type: str = DEFAULT_TASK_TYPE
    task_mix: Dict[str, float] = field(default_factory=lambda: dict(DEFAULT_TASK_MIX))
    ai_support_level: float = 0.70
    trust_in_ai: float = 0.65
    ai_reliability: float = 0.78
    effort_management: float = 0.65
    skills_knowledge_coordination: float = 0.65
    task_strategy: float = 0.65
    female_proportion: float = 0.50
    team_engagement_baseline: float = 0.65
    consequentiality: float = 0.65
    task_complexity: float = 0.58
    dashboard_quality: float = 0.70
    collective_memory: float = 0.62
    collective_attention: float = 0.60
    collective_reasoning: float = 0.64
    # Week 3 controls.
    dependency_density: float = 0.25
    enable_rework: bool = True
    enable_sprint_phases: bool = True
    random_seed: int = 42


def _planned_capacity_points(team_members: List[TeamMember], effort_management: float) -> int:
    capacity = 0.0
    effort_multiplier = 0.90 + (0.20 * effort_management)

    for member in team_members:
        capacity += (
            8.0
            * member.availability
            * member.work_speed
            * (0.80 + (0.20 * member.skill_level))
            * effort_multiplier
        )

    return max(1, int(round(capacity)))


def _find_member(team_members: List[TeamMember], member_id: int) -> TeamMember:
    for member in team_members:
        if member.member_id == member_id:
            return member
    raise ValueError(f"Unknown team member id: {member_id}")


def _sprint_phase_modifiers(
    task_strategy: float,
    skills_knowledge_coordination: float,
    team_engagement: float,
    role_fx: Dict[str, float],
    enabled: bool,
) -> Dict[str, float]:
    """Lightweight sprint-phase modifiers (Week 3).

    * Planning phase strengthens the work strategy.
    * Review phase determines how many defects are caught before shipping.
    * Retrospective phase scales how fast the team learns (CI + engagement).

    When phases are disabled, planning falls back to the raw strategy value,
    review catches nothing extra, and learning runs at its normal rate.
    """

    if not enabled:
        return {
            "planning_quality": clamp(task_strategy),
            "review_quality": 0.0,
            "retro_quality": 1.0,
        }

    planning_quality = clamp(task_strategy + role_fx.get("strategy", 0.0))
    review_quality = clamp(
        (0.25 * skills_knowledge_coordination) + (4.0 * role_fx.get("defect_detection", 0.0))
    )
    # Retrospective learning multiplier centered on 1.0 (0.85 - 1.30 range).
    retro_quality = clamp(
        0.85 + (0.30 * team_engagement) + (0.15 * role_fx.get("coordination", 0.0)),
        0.85,
        1.30,
    )
    return {
        "planning_quality": planning_quality,
        "review_quality": review_quality,
        "retro_quality": retro_quality,
    }


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
    effort_management: float,
    task_strategy: float,
    team_engagement: float,
    role_delivery_bonus: float,
) -> float:
    profile = get_task_type_profile(task.task_type)
    coordination_need = float(profile["coordination_need"])
    completion_bonus = float(profile["completion_bonus"])

    skill_fit = 1.0 - abs(member.skill_level - task.required_skill_level)
    expected_individual_capacity = planned_capacity_points / max(1, team_size)
    overload_ratio = workload_points / max(1.0, expected_individual_capacity)
    overload_penalty = max(0.0, overload_ratio - 1.0) * (0.15 - (0.06 * effort_management))
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
        + (0.05 * task_strategy)
        + (0.05 * team_engagement)
        + (0.08 * ai_bonus)
        + role_delivery_bonus
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
    skills_knowledge_coordination: float,
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
        - (0.05 * skills_knowledge_coordination)
        + misfit_penalty
    )

    return clamp(probability, 0.01, 0.75)


def _update_collective_dimension(
    current_value: float,
    coordination_need: float,
    dashboard_quality: float,
    decision_quality: float,
    outcome_signal: float,
    process_support: float,
    use_ai: bool,
    ai_support_level: float,
    learning_multiplier: float = 1.0,
) -> float:
    ai_learning_bonus = 0.01 * ai_support_level if use_ai else 0.0
    change = (
        0.02 * (coordination_need - 0.5)
        + 0.02 * (dashboard_quality - 0.5)
        + 0.02 * (process_support - 0.5)
        + 0.03 * (decision_quality - 0.5)
        + 0.03 * (outcome_signal - 0.5)
        + ai_learning_bonus
    ) * learning_multiplier
    return clamp(current_value + change, 0.0, 1.0)


def _update_team_engagement(
    current_value: float,
    outcome_signal: float,
    decision_quality: float,
    trust_calibration: float,
    consequentiality: float,
    learning_multiplier: float = 1.0,
) -> float:
    change = (
        0.04 * (outcome_signal - 0.5)
        + 0.03 * (decision_quality - 0.5)
        + 0.02 * (trust_calibration - 0.5)
        + 0.03 * (consequentiality - 0.5)
    ) * learning_multiplier
    return clamp(current_value + change, 0.0, 1.0)


def _task_mix_label(task_mix: Dict[str, float]) -> str:
    return ", ".join(
        f"{task_type}:{round(proportion * 100)}%"
        for task_type, proportion in task_mix.items()
    )


def run_simulation(config: SimulationConfig, use_ai: bool = True) -> Dict[str, object]:
    rng = np.random.default_rng(config.random_seed)

    team_members = generate_team(
        team_size=config.team_size,
        trust_in_ai=config.trust_in_ai,
        ai_reliability=config.ai_reliability,
        female_proportion=config.female_proportion,
        rng=rng,
    )

    role_fx = role_effects(team_members)
    # Scrum Master clears impediments, lowering the effective blocker density.
    effective_dependency_density = clamp(
        config.dependency_density * (1.0 - role_fx.get("blocker_relief", 0.0))
    )
    # Product Owner sharpens shared purpose and strategy.
    effective_consequentiality = clamp(config.consequentiality + role_fx.get("consequentiality", 0.0))

    normalized_mix = normalize_task_mix(config.task_mix)
    backlog = generate_mixed_backlog(
        number_of_tasks=config.number_of_tasks,
        task_complexity=config.task_complexity,
        task_mix=normalized_mix,
        rng=rng,
        dependency_density=effective_dependency_density,
    )

    collective_memory = config.collective_memory
    collective_attention = config.collective_attention
    collective_reasoning = config.collective_reasoning
    team_engagement = clamp(
        (0.75 * config.team_engagement_baseline)
        + (0.25 * effective_consequentiality)
    )

    completed_ids: Set[int] = set()
    next_task_id = config.number_of_tasks + 1

    sprint_records: List[Dict[str, float]] = []
    ci_component_history: List[Dict[str, float]] = []

    for sprint_number in range(1, config.number_of_sprints + 1):
        if not backlog:
            break

        sprint_capacity_points = _planned_capacity_points(
            team_members,
            effort_management=config.effort_management,
        )
        sprint_tasks = select_sprint_tasks(
            backlog,
            sprint_capacity_points,
            completed_ids=completed_ids,
            sprint_number=sprint_number,
        )

        # Tasks that are available this sprint but cannot start because an
        # upstream dependency is not done yet (Week 3 blocker propagation).
        blocked_tasks = [
            task
            for task in backlog
            if task.available_from_sprint <= sprint_number
            and not is_unblocked(task, completed_ids)
        ]

        if not sprint_tasks:
            # Everything available is blocked this sprint; record an empty sprint
            # so blockers are visible, then move on.
            sprint_records.append(
                _empty_sprint_record(
                    sprint_number=sprint_number,
                    use_ai=use_ai,
                    task_mix_label=_task_mix_label(normalized_mix),
                    blocked_tasks=len(blocked_tasks),
                    backlog_remaining=len(backlog),
                )
            )
            continue

        planned_points = sum(task.effort_points for task in sprint_tasks)
        sprint_coordination_need = average_coordination_need(sprint_tasks)

        phases = _sprint_phase_modifiers(
            task_strategy=config.task_strategy,
            skills_knowledge_coordination=config.skills_knowledge_coordination,
            team_engagement=team_engagement,
            role_fx=role_fx,
            enabled=config.enable_sprint_phases,
        )
        # Planning phase: the effective work strategy used downstream.
        effective_task_strategy = phases["planning_quality"]

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

        # Scrum Master coordination helps the dashboard / shared cognition.
        assistant_effect["coordination_gain"] = clamp(
            assistant_effect["coordination_gain"] + role_fx.get("coordination", 0.0)
        )

        allocation_quality = clamp((0.85 * allocation_quality) + (0.15 * effective_task_strategy))
        expected_member_capacity = sprint_capacity_points / max(1, config.team_size)
        overload_pressure = clamp(
            sum(
                max(0.0, (workload / max(1.0, expected_member_capacity)) - 1.0)
                for workload in workloads.values()
            )
            / max(1, len(team_members))
        )

        ci_components = compute_collective_intelligence_components(
            collective_memory=collective_memory,
            collective_attention=collective_attention,
            collective_reasoning=collective_reasoning,
            coordination_need=sprint_coordination_need,
            effort_management=config.effort_management,
            skills_knowledge_coordination=config.skills_knowledge_coordination,
            task_strategy=effective_task_strategy,
            consequentiality=effective_consequentiality,
            team_engagement=team_engagement,
            team_members=team_members,
        )
        collective_intelligence = collective_intelligence_score(ci_components)

        decision_quality = decision_quality_score(
            collective_reasoning=ci_components.shared_reasoning,
            collective_attention=ci_components.shared_attention,
            coordination_need=sprint_coordination_need,
            dashboard_quality=config.dashboard_quality,
            ai_support_level=config.ai_support_level + assistant_effect["decision_gain"],
            use_ai=use_ai,
            social_sensitivity=ci_components.social_sensitivity,
            trust_calibration=trust_calibration,
            task_strategy=effective_task_strategy,
            skills_knowledge_coordination=config.skills_knowledge_coordination,
        )
        # Scrum Master participation/coordination nudges decision quality.
        decision_quality = clamp(
            decision_quality
            + (0.5 * (role_fx.get("coordination", 0.0) + role_fx.get("participation", 0.0)))
        )

        completed_tasks = 0
        completed_points = 0
        total_defects = 0
        caught_defects = 0
        rework_created = 0
        rework_completed = 0
        finished_task_ids: List[int] = []
        new_rework_tasks: List[Task] = []

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
                effort_management=config.effort_management,
                task_strategy=effective_task_strategy,
                team_engagement=team_engagement,
                role_delivery_bonus=role_fx.get("delivery", 0.0),
            )

            if rng.random() <= completion_probability:
                completed_tasks += 1
                completed_points += task.effort_points
                finished_task_ids.append(task.task_id)
                if task.is_rework:
                    rework_completed += 1

                defect_probability = _task_defect_probability(
                    member=member,
                    task=task,
                    decision_quality=decision_quality,
                    ai_support_level=config.ai_support_level,
                    dashboard_quality=config.dashboard_quality,
                    use_ai=use_ai,
                    trust_calibration=trust_calibration,
                    skill_fit=skill_fit,
                    skills_knowledge_coordination=config.skills_knowledge_coordination,
                )

                if rng.random() <= defect_probability:
                    # Review phase may catch the defect before it ships.
                    if rng.random() <= phases["review_quality"]:
                        caught_defects += 1
                    else:
                        total_defects += 1
                        if config.enable_rework:
                            rework_task = create_fix_task(
                                origin=task,
                                new_task_id=next_task_id,
                                available_from_sprint=sprint_number + 1,
                                rng=rng,
                            )
                            new_rework_tasks.append(rework_task)
                            next_task_id += 1
                            rework_created += 1

        completed_ids.update(finished_task_ids)
        backlog = [task for task in backlog if task.task_id not in finished_task_ids]
        backlog.extend(new_rework_tasks)

        tasks_selected = len(sprint_tasks)
        carry_over_tasks = tasks_selected - completed_tasks
        carry_over_points = max(0, planned_points - completed_points)

        completion_rate = completed_tasks / tasks_selected if tasks_selected else 0.0
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

        # Retrospective phase scales how strongly the team learns this sprint.
        learning_multiplier = phases["retro_quality"]
        team_engagement = _update_team_engagement(
            current_value=team_engagement,
            outcome_signal=outcome_signal,
            decision_quality=decision_quality,
            trust_calibration=trust_calibration,
            consequentiality=effective_consequentiality,
            learning_multiplier=learning_multiplier,
        )

        collective_memory = _update_collective_dimension(
            current_value=collective_memory,
            coordination_need=sprint_coordination_need,
            dashboard_quality=config.dashboard_quality,
            decision_quality=decision_quality,
            outcome_signal=outcome_signal,
            process_support=config.skills_knowledge_coordination,
            use_ai=use_ai,
            ai_support_level=config.ai_support_level,
            learning_multiplier=learning_multiplier,
        )
        collective_attention = _update_collective_dimension(
            current_value=collective_attention,
            coordination_need=sprint_coordination_need,
            dashboard_quality=config.dashboard_quality + assistant_effect["coordination_gain"] * 0.10,
            decision_quality=decision_quality,
            outcome_signal=outcome_signal,
            process_support=config.effort_management,
            use_ai=use_ai,
            ai_support_level=config.ai_support_level,
            learning_multiplier=learning_multiplier,
        )
        collective_reasoning = _update_collective_dimension(
            current_value=collective_reasoning,
            coordination_need=sprint_coordination_need,
            dashboard_quality=config.dashboard_quality,
            decision_quality=decision_quality + assistant_effect["decision_gain"] * 0.10,
            outcome_signal=outcome_signal,
            process_support=effective_task_strategy,
            use_ai=use_ai,
            ai_support_level=config.ai_support_level,
            learning_multiplier=learning_multiplier,
        )

        ci_components_after_update = compute_collective_intelligence_components(
            collective_memory=collective_memory,
            collective_attention=collective_attention,
            collective_reasoning=collective_reasoning,
            coordination_need=sprint_coordination_need,
            effort_management=config.effort_management,
            skills_knowledge_coordination=config.skills_knowledge_coordination,
            task_strategy=effective_task_strategy,
            consequentiality=effective_consequentiality,
            team_engagement=team_engagement,
            team_members=team_members,
        )
        collective_intelligence_after_update = collective_intelligence_score(ci_components_after_update)
        team_viability = clamp(
            (0.40 * collective_intelligence_after_update)
            + (0.20 * team_engagement)
            + (0.20 * effective_consequentiality)
            + (0.15 * trust_calibration)
            + (0.05 * decision_quality)
        )
        member_sustainability = clamp(
            (0.35 * team_engagement)
            + (0.25 * effective_consequentiality)
            + (0.25 * config.effort_management)
            + (0.15 * (1.0 - overload_pressure))
        )

        team_effectiveness = team_effectiveness_score(
            velocity_ratio=velocity_ratio,
            completion_rate=completion_rate,
            defect_rate=defect_rate,
            decision_quality=decision_quality,
            collective_intelligence=collective_intelligence_after_update,
            team_viability=team_viability,
            member_sustainability=member_sustainability,
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
                "Task Mix": _task_mix_label(normalized_mix),
                "Planned Points": planned_points,
                "Completed Points": completed_points,
                "Carry-Over Points": carry_over_points,
                "Carry-Over Tasks": carry_over_tasks,
                "Blocked Tasks": len(blocked_tasks),
                "Rework Created": rework_created,
                "Rework Completed": rework_completed,
                "Defects Caught In Review": caught_defects,
                "Tasks Selected": tasks_selected,
                "Tasks Completed": completed_tasks,
                "Defects": total_defects,
                "Sprint Velocity": completed_points,
                "Task Completion Rate": round(completion_rate * 100, 2),
                "Defect Rate": round(defect_rate * 100, 2),
                "Decision Quality": round(decision_quality * 100, 2),
                "Collective Intelligence Score": round(collective_intelligence_after_update * 100, 2),
                "Transactive Memory": round(ci_components_after_update.transactive_memory * 100, 2),
                "Shared Attention": round(ci_components_after_update.shared_attention * 100, 2),
                "Shared Reasoning": round(ci_components_after_update.shared_reasoning * 100, 2),
                "Social Sensitivity": round(ci_components_after_update.social_sensitivity * 100, 2),
                "Participation Balance": round(ci_components_after_update.participation_balance * 100, 2),
                "Team Engagement": round(ci_components_after_update.team_engagement * 100, 2),
                "Skill Diversity": round(ci_components_after_update.skill_diversity * 100, 2),
                "Age Diversity": round(ci_components_after_update.age_diversity * 100, 2),
                "Effort Process": round(config.effort_management * 100, 2),
                "Knowledge Skills Process": round(config.skills_knowledge_coordination * 100, 2),
                "Strategy Process": round(effective_task_strategy * 100, 2),
                "Consequentiality": round(effective_consequentiality * 100, 2),
                "Planning Quality": round(phases["planning_quality"] * 100, 2),
                "Review Quality": round(phases["review_quality"] * 100, 2),
                "Retro Learning Multiplier": round(phases["retro_quality"], 3),
                "Overload Pressure": round(overload_pressure * 100, 2),
                "Trust Calibration": round(trust_calibration * 100, 2),
                "Team Viability": round(team_viability * 100, 2),
                "Member Sustainability": round(member_sustainability * 100, 2),
                "Team Effectiveness Score": round(team_effectiveness, 2),
                "AI Benefit Score": round(ai_benefit, 2),
                "Backlog Remaining": len(backlog),
            }
        )

    results_df = pd.DataFrame(sprint_records)
    ci_components_df = pd.DataFrame(ci_component_history)

    summary = _summarize_results(results_df)

    return {
        "config": asdict(config),
        "model_version": MODEL_VERSION,
        "team": pd.DataFrame([asdict(member) for member in team_members]),
        "results": results_df,
        "ci_components": ci_components_df,
        "summary": summary,
    }


def _empty_sprint_record(
    sprint_number: int,
    use_ai: bool,
    task_mix_label: str,
    blocked_tasks: int,
    backlog_remaining: int,
) -> Dict[str, float]:
    """A sprint where everything available was blocked by dependencies."""

    record = {key: 0 for key in _SPRINT_NUMERIC_COLUMNS}
    record.update(
        {
            "Sprint": sprint_number,
            "Scenario": "With AI support" if use_ai else "Without AI support",
            "Task Mix": task_mix_label,
            "Blocked Tasks": blocked_tasks,
            "Backlog Remaining": backlog_remaining,
            "Retro Learning Multiplier": 1.0,
        }
    )
    return record


_SPRINT_NUMERIC_COLUMNS = [
    "Planned Points",
    "Completed Points",
    "Carry-Over Points",
    "Carry-Over Tasks",
    "Blocked Tasks",
    "Rework Created",
    "Rework Completed",
    "Defects Caught In Review",
    "Tasks Selected",
    "Tasks Completed",
    "Defects",
    "Sprint Velocity",
    "Task Completion Rate",
    "Defect Rate",
    "Decision Quality",
    "Collective Intelligence Score",
    "Transactive Memory",
    "Shared Attention",
    "Shared Reasoning",
    "Social Sensitivity",
    "Participation Balance",
    "Team Engagement",
    "Skill Diversity",
    "Age Diversity",
    "Effort Process",
    "Knowledge Skills Process",
    "Strategy Process",
    "Consequentiality",
    "Planning Quality",
    "Review Quality",
    "Overload Pressure",
    "Trust Calibration",
    "Team Viability",
    "Member Sustainability",
    "Team Effectiveness Score",
    "AI Benefit Score",
]


def _summarize_results(results_df: pd.DataFrame) -> Dict[str, object]:
    empty_keys = [
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

    if results_df.empty:
        summary: Dict[str, object] = {key: 0.0 for key in empty_keys}
        summary["model_version"] = MODEL_VERSION
        return summary

    planned_total = float(results_df["Planned Points"].sum())
    carry_over_total = float(results_df["Carry-Over Points"].sum())

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
        "shared_attention": float(results_df["Shared Attention"].mean()),
        "shared_reasoning": float(results_df["Shared Reasoning"].mean()),
        "social_sensitivity": float(results_df["Social Sensitivity"].mean()),
        "participation_balance": float(results_df["Participation Balance"].mean()),
        "team_engagement": float(results_df["Team Engagement"].mean()),
        "skill_diversity": float(results_df["Skill Diversity"].mean()),
        "age_diversity": float(results_df["Age Diversity"].mean()),
        "effort_management": float(results_df["Effort Process"].mean()),
        "skills_knowledge_coordination": float(results_df["Knowledge Skills Process"].mean()),
        "task_strategy": float(results_df["Strategy Process"].mean()),
        "consequentiality": float(results_df["Consequentiality"].mean()),
        "overload_pressure": float(results_df["Overload Pressure"].mean()),
        "team_viability": float(results_df["Team Viability"].mean()),
        "member_sustainability": float(results_df["Member Sustainability"].mean()),
        "carry_over_points": carry_over_total,
        "carry_over_rate": round((carry_over_total / planned_total) * 100, 2) if planned_total else 0.0,
        "blocked_tasks": float(results_df["Blocked Tasks"].sum()),
        "rework_created": float(results_df["Rework Created"].sum()),
        "rework_completed": float(results_df["Rework Completed"].sum()),
        "defects_caught_in_review": float(results_df["Defects Caught In Review"].sum()),
        "model_version": MODEL_VERSION,
    }
    return summary
