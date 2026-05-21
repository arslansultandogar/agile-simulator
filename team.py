from __future__ import annotations

from dataclasses import dataclass
from typing import List

import numpy as np


@dataclass
class TeamMember:
    """Represents one agile team member in the simulation."""

    member_id: int
    name: str
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


def generate_team(
    team_size: int,
    trust_in_ai: float,
    ai_reliability: float,
    rng: np.random.Generator,
) -> List[TeamMember]:
    """
    Create a team with slight variation around baseline trust and skill levels.
    """

    members: List[TeamMember] = []

    for member_id in range(1, team_size + 1):
        skill_level = _clamp(rng.normal(0.68, 0.12))
        availability = _clamp(rng.normal(0.88, 0.08), 0.55, 1.0)
        communication_level = _clamp(rng.normal(0.72, 0.10))
        social_sensitivity = _clamp(rng.normal(0.62, 0.12))
        member_trust_in_ai = _clamp(rng.normal(trust_in_ai, 0.12))
        perceived_ai_reliability = _clamp(rng.normal(ai_reliability + 0.05, 0.10))
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
