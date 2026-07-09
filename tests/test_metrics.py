"""Unit tests for the scoring formulas in metrics.py."""

import numpy as np
import pytest

from config_loader import CI_COMPONENT_WEIGHTS
from metrics import (
    CollectiveIntelligenceComponents,
    age_diversity_score,
    clamp,
    collective_intelligence_score,
    decision_quality_score,
    participation_balance_score,
    skill_diversity_score,
    team_effectiveness_score,
    trust_calibration_score,
)
from team import generate_team


def _components(**overrides) -> CollectiveIntelligenceComponents:
    base = dict(
        transactive_memory=0.6,
        shared_attention=0.6,
        shared_reasoning=0.6,
        social_sensitivity=0.6,
        participation_balance=0.6,
        transactive_coordination=0.6,
        team_engagement=0.6,
        skill_diversity=0.6,
        age_diversity=0.0,
    )
    base.update(overrides)
    return CollectiveIntelligenceComponents(**base)


def test_ci_positive_weights_sum_to_one():
    assert pytest.approx(sum(CI_COMPONENT_WEIGHTS.values()), abs=1e-9) == 1.0


def test_clamp_bounds():
    assert clamp(-0.5) == 0.0
    assert clamp(1.5) == 1.0
    assert clamp(0.3) == 0.3
    assert clamp(5.0, 0.0, 2.0) == 2.0


def test_collective_intelligence_uniform_components():
    # With all subconstructs at 0.6 and zero age penalty, the weighted average
    # equals 0.6 because the positive weights sum to 1.0.
    components = _components()
    assert pytest.approx(collective_intelligence_score(components), abs=1e-9) == 0.6


def test_age_diversity_penalty_reduces_ci():
    without_penalty = collective_intelligence_score(_components(age_diversity=0.0))
    with_penalty = collective_intelligence_score(_components(age_diversity=1.0))
    assert with_penalty < without_penalty


def test_trust_calibration_is_one_when_aligned():
    assert trust_calibration_score(0.8, 0.8) == 1.0
    assert trust_calibration_score(0.9, 0.5) == pytest.approx(0.6)


def test_decision_quality_within_bounds():
    score = decision_quality_score(
        collective_reasoning=0.7,
        collective_attention=0.7,
        coordination_need=0.6,
        dashboard_quality=0.7,
        ai_support_level=0.7,
        use_ai=True,
        social_sensitivity=0.6,
        trust_calibration=0.9,
        task_strategy=0.6,
        skills_knowledge_coordination=0.6,
    )
    assert 0.0 <= score <= 1.0


def test_team_effectiveness_is_percentage_scale():
    perfect = team_effectiveness_score(
        velocity_ratio=1.0,
        completion_rate=1.0,
        defect_rate=0.0,
        decision_quality=1.0,
        collective_intelligence=1.0,
        team_viability=1.0,
        member_sustainability=1.0,
    )
    assert perfect == pytest.approx(100.0)


def test_skill_and_age_diversity_handle_small_teams():
    rng = np.random.default_rng(0)
    solo = generate_team(1, 0.6, 0.8, 0.5, rng)
    assert skill_diversity_score(solo) == 0.0
    assert age_diversity_score(solo) == 0.0


def test_participation_balance_perfect_when_equal():
    rng = np.random.default_rng(1)
    team = generate_team(5, 0.6, 0.8, 0.5, rng)
    for member in team:
        member.communication_level = 0.7
    assert participation_balance_score(team) == pytest.approx(1.0)
