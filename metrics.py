from __future__ import annotations

from dataclasses import dataclass
from statistics import pstdev
from typing import List, TYPE_CHECKING

from config_loader import (
    AGE_DIVERSITY_PENALTY_WEIGHT,
    CI_COMPONENT_WEIGHTS,
    TEAM_EFFECTIVENESS_WEIGHTS,
)

if TYPE_CHECKING:
    from team import TeamMember


def clamp(value: float, minimum: float = 0.0, maximum: float = 1.0) -> float:
    return max(minimum, min(maximum, value))


@dataclass
class CollectiveIntelligenceComponents:
    """Subconstructs that feed the aggregate Collective Intelligence score."""

    transactive_memory: float
    shared_attention: float
    shared_reasoning: float
    social_sensitivity: float
    participation_balance: float
    transactive_coordination: float
    team_engagement: float
    skill_diversity: float
    age_diversity: float

    def as_dict(self) -> dict[str, float]:
        return {
            "transactive_memory": self.transactive_memory,
            "shared_attention": self.shared_attention,
            "shared_reasoning": self.shared_reasoning,
            "social_sensitivity": self.social_sensitivity,
            "participation_balance": self.participation_balance,
            "transactive_coordination": self.transactive_coordination,
            "team_engagement": self.team_engagement,
            "skill_diversity": self.skill_diversity,
            "age_diversity": self.age_diversity,
        }


def participation_balance_score(team_members: List[TeamMember]) -> float:
    """
    Balanced conversational participation improves collective intelligence.

    Higher score when communication levels are more evenly distributed.
    """

    if not team_members:
        return 0.5

    levels = [member.communication_level for member in team_members]
    spread = max(levels) - min(levels)
    return clamp(1.0 - spread)


def average_social_sensitivity(team_members: List[TeamMember]) -> float:
    if not team_members:
        return 0.5

    return clamp(sum(member.social_sensitivity for member in team_members) / len(team_members))


def skill_diversity_score(team_members: List[TeamMember]) -> float:
    """
    Functional diversity proxy based on spread in team member skill levels.
    """

    if len(team_members) < 2:
        return 0.0

    skill_levels = [member.skill_level for member in team_members]
    return clamp(pstdev(skill_levels) * 3.0)


def age_diversity_score(team_members: List[TeamMember]) -> float:
    """
    Age diversity is modeled as a normalized spread and used as a CI penalty.
    """

    if len(team_members) < 2:
        return 0.0

    ages = [member.age for member in team_members]
    return clamp(pstdev(ages) / 12.0)


def transactive_memory_score(
    collective_memory: float,
    team_members: List[TeamMember],
    skills_knowledge_coordination: float,
) -> float:
    """
    Transactive memory combines shared retention with specialization diversity.

    Teams benefit when members know different things and the group can coordinate
    who knows what.
    """

    if not team_members:
        return collective_memory

    skill_levels = [member.skill_level for member in team_members]
    average_individual_skill = clamp(sum(skill_levels) / len(skill_levels))
    skill_diversity = skill_diversity_score(team_members)
    return clamp(
        (0.40 * collective_memory)
        + (0.25 * skills_knowledge_coordination)
        + (0.20 * skill_diversity)
        + (0.15 * average_individual_skill)
    )


def shared_attention_score(
    collective_attention: float,
    effort_management: float,
    consequentiality: float,
    participation_balance: float,
    coordination_need: float,
) -> float:
    """
    Collective attention reflects shared focus and sustained effort allocation.

    Riedl et al. (2021) treat effort and collaboration process as predictors of
    CI; Kommol et al. (2025) frames attention as one of the three core CI systems.
    """

    return clamp(
        (0.42 * collective_attention)
        + (0.18 * effort_management)
        + (0.15 * consequentiality)
        + (0.16 * participation_balance)
        + (0.09 * coordination_need)
    )


def shared_reasoning_score(
    collective_reasoning: float,
    task_strategy: float,
    social_sensitivity: float,
    skills_knowledge_coordination: float,
) -> float:
    """
    Collective reasoning reflects how the team interprets information together.

    Strategy process and knowledge/skills process operationalize Hackman's and
    Riedl et al.'s process criteria for collaborative task performance.
    """

    return clamp(
        (0.50 * collective_reasoning)
        + (0.25 * task_strategy)
        + (0.15 * social_sensitivity)
        + (0.10 * skills_knowledge_coordination)
    )


def transactive_coordination_score(
    collective_memory: float,
    coordination_need: float,
    participation_balance: float,
) -> float:
    return clamp(
        (0.40 * collective_memory)
        + (0.35 * coordination_need)
        + (0.25 * participation_balance)
    )


def compute_collective_intelligence_components(
    collective_memory: float,
    collective_attention: float,
    collective_reasoning: float,
    coordination_need: float,
    effort_management: float,
    skills_knowledge_coordination: float,
    task_strategy: float,
    consequentiality: float,
    team_engagement: float,
    team_members: List[TeamMember],
) -> CollectiveIntelligenceComponents:
    participation_balance = participation_balance_score(team_members)
    social_sensitivity = average_social_sensitivity(team_members)
    skill_diversity = skill_diversity_score(team_members)
    age_diversity = age_diversity_score(team_members)

    return CollectiveIntelligenceComponents(
        transactive_memory=transactive_memory_score(
            collective_memory,
            team_members,
            skills_knowledge_coordination,
        ),
        shared_attention=shared_attention_score(
            collective_attention=collective_attention,
            effort_management=effort_management,
            consequentiality=consequentiality,
            participation_balance=participation_balance,
            coordination_need=coordination_need,
        ),
        shared_reasoning=shared_reasoning_score(
            collective_reasoning=collective_reasoning,
            task_strategy=task_strategy,
            social_sensitivity=social_sensitivity,
            skills_knowledge_coordination=skills_knowledge_coordination,
        ),
        social_sensitivity=social_sensitivity,
        participation_balance=participation_balance,
        transactive_coordination=transactive_coordination_score(
            collective_memory=collective_memory,
            coordination_need=coordination_need,
            participation_balance=participation_balance,
        ),
        team_engagement=clamp(team_engagement),
        skill_diversity=skill_diversity,
        age_diversity=age_diversity,
    )


def collective_intelligence_score(components: CollectiveIntelligenceComponents) -> float:
    """
    Aggregate Collective Intelligence from validated subconstructs.

    Weights remain readable for thesis explanation while reflecting that CI is
    emergent from memory, attention, reasoning, social sensitivity, and balance.
    """

    base_score = (
        (CI_COMPONENT_WEIGHTS["transactive_memory"] * components.transactive_memory)
        + (CI_COMPONENT_WEIGHTS["shared_attention"] * components.shared_attention)
        + (CI_COMPONENT_WEIGHTS["shared_reasoning"] * components.shared_reasoning)
        + (CI_COMPONENT_WEIGHTS["social_sensitivity"] * components.social_sensitivity)
        + (CI_COMPONENT_WEIGHTS["participation_balance"] * components.participation_balance)
        + (CI_COMPONENT_WEIGHTS["transactive_coordination"] * components.transactive_coordination)
        + (CI_COMPONENT_WEIGHTS["team_engagement"] * components.team_engagement)
        + (CI_COMPONENT_WEIGHTS["skill_diversity"] * components.skill_diversity)
    )
    return clamp(base_score - (AGE_DIVERSITY_PENALTY_WEIGHT * components.age_diversity))


def decision_quality_score(
    collective_reasoning: float,
    collective_attention: float,
    coordination_need: float,
    dashboard_quality: float,
    ai_support_level: float,
    use_ai: bool,
    social_sensitivity: float,
    trust_calibration: float,
    task_strategy: float,
    skills_knowledge_coordination: float,
) -> float:
    """
    Decision quality is influenced by team cognition, task coordination demands,
    and calibrated AI trust.
    """

    ai_bonus = ai_support_level * dashboard_quality * trust_calibration if use_ai else 0.0

    return clamp(
        (0.24 * collective_reasoning)
        + (0.16 * collective_attention)
        + (0.14 * coordination_need)
        + (0.10 * dashboard_quality)
        + (0.12 * social_sensitivity)
        + (0.08 * task_strategy)
        + (0.06 * skills_knowledge_coordination)
        + (0.10 * ai_bonus)
    )


def trust_calibration_score(perceived_ai_reliability: float, actual_ai_reliability: float) -> float:
    """
    Calibrated trust is highest when perceived and actual AI reliability align.
    """

    mismatch = abs(perceived_ai_reliability - actual_ai_reliability)
    return clamp(1.0 - mismatch)


def team_effectiveness_score(
    velocity_ratio: float,
    completion_rate: float,
    defect_rate: float,
    decision_quality: float,
    collective_intelligence: float,
    team_viability: float | None = None,
    member_sustainability: float | None = None,
) -> float:
    """
    Hackman-informed team effectiveness.

    The composite keeps the original delivery/quality metrics visible while
    adding proxies for future viability and member sustainability.
    """

    quality_component = 1.0 - defect_rate
    task_output = clamp(
        (0.40 * velocity_ratio)
        + (0.35 * completion_rate)
        + (0.25 * quality_component)
    )
    viability = (
        clamp(team_viability)
        if team_viability is not None
        else clamp((0.60 * collective_intelligence) + (0.40 * decision_quality))
    )
    sustainability = clamp(member_sustainability) if member_sustainability is not None else completion_rate

    return clamp(
        (TEAM_EFFECTIVENESS_WEIGHTS["task_output"] * task_output)
        + (TEAM_EFFECTIVENESS_WEIGHTS["team_viability"] * viability)
        + (TEAM_EFFECTIVENESS_WEIGHTS["member_sustainability"] * sustainability)
    ) * 100.0


def ai_benefit_score(
    use_ai: bool,
    ai_support_level: float,
    allocation_quality: float,
    coordination_gain: float,
    decision_gain: float,
    trust_calibration: float,
) -> float:
    if not use_ai:
        return 0.0

    return clamp(
        ai_support_level
        * trust_calibration
        * (
            (0.45 * allocation_quality)
            + (0.30 * coordination_gain)
            + (0.25 * decision_gain)
        )
    ) * 100.0
