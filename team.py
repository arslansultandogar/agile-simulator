from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

import numpy as np

from config_loader import HUMAN_AI_TRUST, PERCEIVED_RELIABILITY_ANCHOR


# Week 4: lightweight role model. Roles act as small behavioral modifiers
# layered on top of the existing per-member attributes; they are not a full
# org model. Order matters for assignment (first members take the lead roles).
ROLES = ("Product Owner", "Scrum Master", "Developer", "Tester")

# Per-role behavioral modifiers (small, additive nudges in 0-1 space).
ROLE_MODIFIERS: Dict[str, Dict[str, float]] = {
    "Product Owner": {
        # Sharpens prioritization and shared purpose / strategy.
        "strategy": 0.06,
        "consequentiality": 0.05,
    },
    "Scrum Master": {
        # Improves coordination, balanced participation, and unblocking.
        "participation": 0.06,
        "coordination": 0.05,
        "blocker_relief": 0.20,
    },
    "Developer": {
        "delivery": 0.03,
    },
    "Tester": {
        # Catches defects before they ship.
        "defect_detection": 0.10,
    },
}


@dataclass
class TeamMember:
    """Represents one agile team member in the simulation."""

    member_id: int
    name: str
    gender: str
    age: int
    role: str
    skill_level: float
    availability: float
    communication_level: float
    social_sensitivity: float
    trust_in_ai: float
    perceived_ai_reliability: float
    work_speed: float
    error_tendency: float


def _clamp(value: float, minimum: float = 0.0, maximum: float = 1.0) -> float:
    return max(minimum, min(maximum, value))


def _assign_role(member_index: int, team_size: int) -> str:
    """Assign a Scrum role.

    One Product Owner and one Scrum Master lead the team; at least one Tester
    is added for teams of four or more; everyone else is a Developer.
    """

    if member_index == 0:
        return "Product Owner"
    if member_index == 1 and team_size >= 3:
        return "Scrum Master"
    if team_size >= 4 and member_index == team_size - 1:
        return "Tester"
    return "Developer"


def generate_team(
    team_size: int,
    trust_in_ai: float,
    ai_reliability: float,
    female_proportion: float,
    rng: np.random.Generator,
) -> List[TeamMember]:
    """
    Create a team with slight variation around baseline trust and skill levels.

    Gender is modeled only as a research variable for Woolley et al. (2010),
    where female proportion relates to collective intelligence partly through
    social sensitivity.
    """

    members: List[TeamMember] = []
    female_count = int(round(team_size * _clamp(female_proportion)))

    for member_id in range(1, team_size + 1):
        gender = "F" if member_id <= female_count else "M"
        role = _assign_role(member_id - 1, team_size)
        age = int(round(_clamp(rng.normal(36, 8), 22, 60)))
        skill_level = _clamp(rng.normal(0.68, 0.12))
        availability = _clamp(rng.normal(0.88, 0.08), 0.55, 1.0)
        communication_level = _clamp(rng.normal(0.72, 0.10))
        social_sensitivity_baseline = 0.66 if gender == "F" else 0.60
        social_sensitivity = _clamp(rng.normal(social_sensitivity_baseline, 0.12))
        member_trust_in_ai = _clamp(rng.normal(trust_in_ai, 0.12))
        # v2.1: initial perceived reliability is a PRIOR BELIEF anchored on the
        # team's trust disposition, not on the AI's true reliability. Anchoring
        # it on actual reliability (the v2.0 behavior, still selectable via
        # config/weights.yaml) makes miscalibration structurally impossible.
        _anchor = (
            member_trust_in_ai
            if PERCEIVED_RELIABILITY_ANCHOR == "trust"
            else ai_reliability
        )
        perceived_ai_reliability = _clamp(
            rng.normal(
                _anchor + HUMAN_AI_TRUST["perceived_optimism_offset"],
                HUMAN_AI_TRUST["perceived_reliability_sd"],
            )
        )
        work_speed = _clamp(rng.normal(0.95, 0.12), 0.55, 1.35)

        # Better skills and communication usually reduce defects, so they lower
        # the member's tendency to introduce errors.
        error_tendency = _clamp(
            0.45
            - (0.20 * skill_level)
            - (0.10 * communication_level)
            + rng.normal(0.0, 0.05),
            0.05,
            0.55,
        )

        members.append(
            TeamMember(
                member_id=member_id,
                name=f"Member {member_id}",
                gender=gender,
                age=age,
                role=role,
                skill_level=skill_level,
                availability=availability,
                communication_level=communication_level,
                social_sensitivity=social_sensitivity,
                trust_in_ai=member_trust_in_ai,
                perceived_ai_reliability=perceived_ai_reliability,
                work_speed=work_speed,
                error_tendency=error_tendency,
            )
        )

    return members


def role_effects(team_members: List[TeamMember]) -> Dict[str, float]:
    """Aggregate role-based behavioral modifiers for the whole team.

    Lead-role effects (Product Owner, Scrum Master) are present when at least
    one such member exists. Composition effects (Developer, Tester) scale with
    the share of the team in that role.
    """

    effects = {
        "strategy": 0.0,
        "consequentiality": 0.0,
        "participation": 0.0,
        "coordination": 0.0,
        "blocker_relief": 0.0,
        "delivery": 0.0,
        "defect_detection": 0.0,
    }
    if not team_members:
        return effects

    team_size = len(team_members)
    roles = [member.role for member in team_members]

    if "Product Owner" in roles:
        for key, value in ROLE_MODIFIERS["Product Owner"].items():
            effects[key] += value
    if "Scrum Master" in roles:
        for key, value in ROLE_MODIFIERS["Scrum Master"].items():
            effects[key] += value

    developer_ratio = roles.count("Developer") / team_size
    tester_ratio = roles.count("Tester") / team_size
    effects["delivery"] += ROLE_MODIFIERS["Developer"]["delivery"] * developer_ratio
    effects["defect_detection"] += ROLE_MODIFIERS["Tester"]["defect_detection"] * tester_ratio

    return effects
