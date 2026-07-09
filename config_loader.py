from __future__ import annotations

"""Loads externalized model weights from ``config/weights.yaml``.

Keeping weights in a YAML file lets the model be tuned and studied without
editing Python source. If the file is missing or malformed the loader falls
back to the documented defaults so the simulator always runs.
"""

from pathlib import Path
from typing import Dict

import yaml

_CONFIG_PATH = Path(__file__).resolve().parent / "config" / "weights.yaml"

_DEFAULT_MODEL_VERSION = "2.0.0"

_DEFAULT_CI_COMPONENT_WEIGHTS: Dict[str, float] = {
    "transactive_memory": 0.18,
    "shared_attention": 0.16,
    "shared_reasoning": 0.16,
    "social_sensitivity": 0.16,
    "participation_balance": 0.10,
    "transactive_coordination": 0.10,
    "team_engagement": 0.08,
    "skill_diversity": 0.06,
}

_DEFAULT_AGE_DIVERSITY_PENALTY_WEIGHT = 0.04

_DEFAULT_TEAM_EFFECTIVENESS_WEIGHTS: Dict[str, float] = {
    "task_output": 0.55,
    "team_viability": 0.25,
    "member_sustainability": 0.20,
}


def _load_raw_config() -> dict:
    try:
        with _CONFIG_PATH.open("r", encoding="utf-8") as handle:
            data = yaml.safe_load(handle)
            return data if isinstance(data, dict) else {}
    except (FileNotFoundError, yaml.YAMLError):
        return {}


_RAW = _load_raw_config()


def _merge_weights(key: str, defaults: Dict[str, float]) -> Dict[str, float]:
    loaded = _RAW.get(key, {})
    if not isinstance(loaded, dict):
        return dict(defaults)
    merged = dict(defaults)
    for name, value in loaded.items():
        if name in merged:
            try:
                merged[name] = float(value)
            except (TypeError, ValueError):
                continue
    return merged


MODEL_VERSION: str = str(_RAW.get("model_version", _DEFAULT_MODEL_VERSION))

CI_COMPONENT_WEIGHTS: Dict[str, float] = _merge_weights(
    "ci_component_weights", _DEFAULT_CI_COMPONENT_WEIGHTS
)

try:
    AGE_DIVERSITY_PENALTY_WEIGHT: float = float(
        _RAW.get("age_diversity_penalty_weight", _DEFAULT_AGE_DIVERSITY_PENALTY_WEIGHT)
    )
except (TypeError, ValueError):
    AGE_DIVERSITY_PENALTY_WEIGHT = _DEFAULT_AGE_DIVERSITY_PENALTY_WEIGHT

TEAM_EFFECTIVENESS_WEIGHTS: Dict[str, float] = _merge_weights(
    "team_effectiveness_weights", _DEFAULT_TEAM_EFFECTIVENESS_WEIGHTS
)
