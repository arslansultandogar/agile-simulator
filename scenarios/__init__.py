"""CITAS demonstration scenarios (methods paper; target venue JASSS).

Two configurations anchored in published empirical case studies. Each entry is
a dict of ``SimulationConfig`` keyword arguments following the ``PRESETS``
convention in ``run_thesis_experiments.py``; apply with
``dataclasses.replace(SimulationConfig(), **SCENARIOS[name])`` or
``build_config(name)``.

Basis codes are recorded inline for EVERY parameter so provenance survives in
the code rather than only in the paper:

    REP  reported in the anchor source
    DER  derived from a reported figure
    ASS  documented assumption

Baseline arm. The no-AI condition is ``run_simulation(cfg, use_ai=False)``:
the heuristic allocator with no shared-cognition assistant, matching the thesis
``paired_ai_benefit`` convention. It is NOT ``ai_support_level = 0`` with
``use_ai=True``, which still executes ``allocate_tasks_with_ai``,
``shared_cognition_assistant`` and the ``misfit_penalty`` - an AI-enabled team
with the support dial at zero, a model artefact rather than a research
condition. The original scenario specification said ``ai_support_level = 0``;
that was corrected during implementation (see scenarios/README.md).

All results must derive from model v2.1 mechanics; ``run_scenarios.py`` refuses
to run against any other version or anchor setting.

Anchor citations
----------------
Scenario A, quantitative anchor:
  Van Schooenderwoert, N. (2006). Embedded agile project by the numbers with
  newbies. Agile Conference 2006 (AGILE'06), 351-363.
  Caveat: an industry experience report authored by the project's technical
  lead, not an independent controlled study. Its figures are illustrative, not
  ground truth.
Scenario A, process and regulatory characteristics:
  Diebold, P. & Mayer, M. (2017). On the usage and benefits of agile methods &
  practices: a case study at Bosch Chassis Systems Control. XP 2017,
  LNBIP 283, 243-250. DOI 10.1007/978-3-319-57633-6_16
  Heeager, L. T. & Nielsen, P. A. (2020). Meshing agile and plan-driven
  development in safety-critical software: a case study. Empirical Software
  Engineering, 25(2), 1035-1062. DOI 10.1007/s10664-020-09804-z
Scenario B anchor:
  Dingsoyr, T., Moe, N. B. & Seim, E. A. (2018). Coordinating knowledge work in
  multi-team programs: findings from a large-scale agile development program.
  Project Management Journal. Preprint arXiv:1801.08764
Trust calibration grounding:
  Lee, J. D. & See, K. A. (2004). Trust in automation: designing for
  appropriate reliance. Human Factors, 46(1), 50-80.
"""

from __future__ import annotations

from dataclasses import replace
from typing import Dict

from simulation import SimulationConfig
from tasks import normalize_task_mix

# ---------------------------------------------------------------------------
# AI arm, shared by both scenarios so they remain comparable on the AI
# dimension. The baseline arm is use_ai=False, not a change to these values.
# ---------------------------------------------------------------------------
AI_ARM: Dict[str, float] = {
    "ai_support_level": 0.70,   # ASS  shared across scenarios for comparability
    "ai_reliability": 0.78,     # ASS  swept 0.30-0.95 in the Scenario A sensitivity analysis
    "trust_in_ai": 0.65,        # ASS  swept independently to expose mis-calibration (Scenario A)
    "dashboard_quality": 0.70,  # ASS  shared across scenarios
}

# ---------------------------------------------------------------------------
# Parameters the model requires that the scenario specification did not set.
# All three were ADDED during implementation and are coded ASS.
# ---------------------------------------------------------------------------
IMPLEMENTATION_DEFAULTS: Dict[str, float | int] = {
    # ASS  neither anchor reports gender composition; keeping the model default
    #      avoids introducing an unevidenced Woolley-proxy effect on social
    #      sensitivity.
    "female_proportion": 0.50,
    # ASS  model default. Stakes are already carried by consequentiality;
    #      raising both would double-count the same construct.
    "team_engagement_baseline": 0.65,
    # ASS  matches the thesis BASE seed. Replication i uses seed 42 + i; the
    #      same sequence is reused in every paired arm and every grid cell
    #      (common random numbers).
    "random_seed": 42,
}

# ---------------------------------------------------------------------------
# Scenario A - safety-critical embedded: electronic brake control unit (EBCU)
# with a coupled instrument cluster unit (ICU). Brownfield update to a
# certified code base under ISO 26262; hardware-in-the-loop windows scheduled.
# ---------------------------------------------------------------------------
SCENARIO_A: Dict[str, object] = {
    # --- team and schedule -------------------------------------------------
    "team_size": 5,               # REP  anchor reports a team of 4-6 (Van Schooenderwoert 2006)
    "number_of_sprints": 12,      # ASS  representative window; the anchor programme ran ~3 years
    "number_of_tasks": 60,        # DER  from ~230 function points at the anchor's granularity
    # --- backlog -------------------------------------------------------------
    # ASS  feature / bug / refactor / spike; brownfield safety-critical profile
    #      (certified base, revised diagnostics, hardening). Sums to 1.00.
    "task_mix": {"feature": 0.45, "bug": 0.20, "refactor": 0.25, "spike": 0.10},
    "dependency_density": 0.45,   # ASS  EBCU-ICU cross-unit coupling; scheduled HIL integration windows
    "task_complexity": 0.72,      # ASS  anchor reports cyclomatic complexity 6-7, plus real-time constraints
    # --- process quality (Riedl et al. 2021 process predictors) -------------
    "effort_management": 0.75,    # DER  sustained low open-defect count (never >2 open) implies strong effort discipline
    "skills_knowledge_coordination": 0.60,  # ASS  mixed-seniority team; specialists not interchangeable
    "task_strategy": 0.70,        # REP  iteration length actively tuned (2-8 weeks settling to 2)
    "consequentiality": 0.85,     # ASS  ISO 26262 obligations; visible safety stakes
    # --- collective-intelligence baselines ------------------------------------
    # The anchor's newcomer-heavy staffing is operationalised HERE (reduced
    # initial shared knowledge and coordination capability), not through agent
    # skill levels, which the model draws from a fixed distribution.
    "collective_memory": 0.50,    # ASS  newcomer-heavy staffing; low initial shared knowledge (model default 0.62)
    "collective_attention": 0.70, # ASS  small co-located team
    "collective_reasoning": 0.60, # ASS  rises as domain familiarity accumulates (retrospective learning is modelled)
    # --- Scrum mechanics -------------------------------------------------------
    "enable_rework": True,        # REP  59% of generated defects caught internally -> rework loop is live
    "enable_sprint_phases": True, # REP  review discipline is the anchor's distinguishing feature
    **IMPLEMENTATION_DEFAULTS,
    **AI_ARM,
}

# ---------------------------------------------------------------------------
# Scenario B - large-scale enterprise information system: replacement
# case-processing platform for a public-sector pension provider. One
# representative team out of up to twelve running in parallel.
# ---------------------------------------------------------------------------
SCENARIO_B: Dict[str, object] = {
    # --- team and schedule -------------------------------------------------
    "team_size": 7,               # ASS  Scrum norm; programme reports 175 people over 12 teams (Dingsoyr et al. 2018)
    "number_of_sprints": 12,      # DER  three-week cadence over ~9 months
    "number_of_tasks": 200,       # DER  scaled from ~2,500 programme-level stories to one representative team
    # --- backlog -------------------------------------------------------------
    # ASS  green-field enterprise delivery profile. Sums to 1.00.
    "task_mix": {"feature": 0.60, "bug": 0.15, "refactor": 0.15, "spike": 0.10},
    "dependency_density": 0.35,   # DER  inter-team dependencies across 12 parallel teams
    "task_complexity": 0.55,      # ASS  business-logic complexity without real-time constraints
    # --- process quality -------------------------------------------------------
    "effort_management": 0.65,    # ASS  model default; no anchor evidence either way
    "skills_knowledge_coordination": 0.55,  # DER  consultant-heavy staffing (100 of 175 external)
    "task_strategy": 0.65,        # REP  programme reports the full Scrum ceremony set
    "consequentiality": 0.60,     # ASS  public-service obligation; audited, not safety-certified
    # --- collective-intelligence baselines ------------------------------------
    # Consultant-heavy staffing is operationalised through reduced collective
    # memory and coordination capability. skill_diversity is a computed OUTPUT
    # of the model, not an input, so it cannot be set here.
    "collective_memory": 0.45,    # DER  external consultants; knowledge does not persist in the organisation
    "collective_attention": 0.55, # ASS  twelve parallel teams dilute shared focus
    "collective_reasoning": 0.65, # ASS  model default; no anchor evidence either way
    # --- Scrum mechanics -------------------------------------------------------
    "enable_rework": True,        # ASS  no anchor figure; enterprise delivery carries rework
    "enable_sprint_phases": True, # REP  planning, daily and retrospective all reported
    **IMPLEMENTATION_DEFAULTS,
    **AI_ARM,
}

SCENARIOS: Dict[str, Dict[str, object]] = {
    "A_safety_critical_embedded": SCENARIO_A,
    "B_large_scale_enterprise": SCENARIO_B,
}

LABELS: Dict[str, str] = {
    "A_safety_critical_embedded": "Scenario A: safety-critical embedded (EBCU/ICU)",
    "B_large_scale_enterprise": "Scenario B: large-scale enterprise IS (pension)",
}


def build_config(name: str) -> SimulationConfig:
    """Return the SimulationConfig for a named scenario (task mix normalised)."""
    params = dict(SCENARIOS[name])
    params["task_mix"] = normalize_task_mix(params["task_mix"])  # type: ignore[arg-type]
    return replace(SimulationConfig(), **params)
