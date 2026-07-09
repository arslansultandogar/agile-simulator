# Parameter Dictionary

A single reference for every tunable parameter, output metric, and config value
in the Agile AI Simulator. All percentages are **transparent simulation
assumptions**, not empirically estimated coefficients.

Model version is surfaced at `run_simulation(...)["summary"]["model_version"]`
and loaded from `config/weights.yaml`.

---

## 1. SimulationConfig inputs (`simulation.py`)

| Parameter | Type | Default | Range | Meaning |
|---|---|---|---|---|
| `team_size` | int | 6 | 3–12 | Number of agile team members. |
| `number_of_sprints` | int | 8 | 1–20 | Number of simulated sprints. |
| `number_of_tasks` | int | 60 | 10–200 | Initial backlog size (before rework). |
| `task_type` | str | `feature` | feature/bug/refactor/spike | Single-type fallback when a mix is not used. |
| `task_mix` | dict | 50/25/15/10 | proportions | Relative share of each task type; normalized to sum to 1.0 (Week 2). |
| `ai_support_level` | float | 0.70 | 0–1 | Intensity of AI support in the scenario. |
| `trust_in_ai` | float | 0.65 | 0–1 | Baseline team trust in AI recommendations. |
| `ai_reliability` | float | 0.78 | 0–1 | Actual AI reliability; low values cause allocation mistakes. |
| `effort_management` | float | 0.65 | 0–1 | Effort-related process: sustaining/allocating effort. |
| `skills_knowledge_coordination` | float | 0.65 | 0–1 | Knowledge/skills process: matching expertise to work. |
| `task_strategy` | float | 0.65 | 0–1 | Strategy updating process: adapting the work approach. |
| `female_proportion` | float | 0.50 | 0–1 | Proxy pathway through social perceptiveness (not a causal claim). |
| `team_engagement_baseline` | float | 0.65 | 0–1 | Initial team-level engagement. |
| `consequentiality` | float | 0.65 | 0–1 | Shared purpose; strengthens engagement, attention, viability, sustainability. |
| `task_complexity` | float | 0.58 | 0–1 | Baseline difficulty of generated work. |
| `dashboard_quality` | float | 0.70 | 0–1 | Quality of the AI shared-cognition dashboard. |
| `collective_memory` | float | 0.62 | 0–1 | CI baseline: retained/reused shared knowledge. |
| `collective_attention` | float | 0.60 | 0–1 | CI baseline: shared focus of attention. |
| `collective_reasoning` | float | 0.64 | 0–1 | CI baseline: joint interpretation/decision-making. |
| `dependency_density` | float | 0.25 | 0–1 | Share of tasks that depend on an upstream task (Week 3). |
| `enable_rework` | bool | True | — | Shipped defects spawn follow-up fix tasks (Week 3). |
| `enable_sprint_phases` | bool | True | — | Planning/review/retrospective modifiers (Week 3). |
| `random_seed` | int | 42 | 0–999999 | Seed for reproducible runs. |

## 2. TeamMember attributes (`team.py`)

| Attribute | Meaning |
|---|---|
| `member_id`, `name` | Identity. |
| `gender` | Research variable for the Woolley female-proportion proxy only. |
| `age` | Feeds the age-diversity penalty. |
| `role` | Product Owner / Scrum Master / Developer / Tester (Week 4). |
| `skill_level` | Individual technical skill. |
| `availability` | Share of capacity available. |
| `communication_level` | Feeds participation balance. |
| `social_sensitivity` | Social perceptiveness; feeds CI and decision quality. |
| `trust_in_ai` | Member trust, updated each sprint. |
| `perceived_ai_reliability` | Member belief about AI reliability; feeds trust calibration. |
| `work_speed` | Throughput multiplier. |
| `error_tendency` | Propensity to introduce defects. |

### Role modifiers (`team.role_effects`)

| Role | Behavioral modifier |
|---|---|
| Product Owner | +strategy, +consequentiality (sharper prioritization / shared purpose). |
| Scrum Master | +participation, +coordination, +blocker_relief (clears impediments). |
| Developer | +delivery (small completion nudge, scales with developer share). |
| Tester | +defect_detection (more defects caught in review, scales with tester share). |

## 3. Task attributes (`tasks.py`)

| Attribute | Meaning |
|---|---|
| `task_id`, `task_type` | Identity and type. |
| `difficulty`, `uncertainty` | Drive completion and defect probability. |
| `effort_points` | Story points consumed from sprint capacity. |
| `priority` | Selection ordering. |
| `required_skill_level` | Compared with member skill for skill fit. |
| `depends_on` | Upstream task ids that must complete first (Week 3). |
| `is_rework`, `origin_task_id` | Marks a defect follow-up and its source task. |
| `available_from_sprint` | Earliest sprint the task can be selected (rework appears later). |

## 4. Output metrics (`run_simulation` summary + per-sprint records)

| Metric | Meaning |
|---|---|
| `average_velocity` | Mean completed points per sprint. |
| `completion_rate` | % of selected tasks completed. |
| `defect_rate` | % of completed tasks shipping a defect. |
| `decision_quality` | Team decision-quality score. |
| `collective_intelligence` | Aggregate CI score. |
| `team_effectiveness` | Hackman-style composite (output/viability/sustainability). |
| `ai_benefit` | AI contribution score. |
| `trust_calibration` | Alignment of perceived vs actual AI reliability. |
| `transactive_memory` … `age_diversity` | CI subcomponents. |
| `effort_management`, `skills_knowledge_coordination`, `task_strategy` | Process measures (strategy reflects planning phase). |
| `consequentiality` | Effective shared purpose (incl. PO role effect). |
| `overload_pressure` | Average member overload. |
| `team_viability`, `member_sustainability` | Future capacity and burnout risk. |
| `carry_over_points` | Committed points not finished (Week 2). |
| `carry_over_rate` | Carry-over points / planned points (%). |
| `blocked_tasks` | Tasks blocked by unmet dependencies (summed, Week 3). |
| `rework_created`, `rework_completed` | Defect follow-ups generated/finished (Week 3). |
| `defects_caught_in_review` | Defects caught before shipping by the review phase. |

## 5. Externalized weights (`config/weights.yaml`)

| Key | Meaning |
|---|---|
| `model_version` | Version surfaced in run summaries. |
| `ci_component_weights` | Aggregate CI weights (positive weights sum to 1.0). |
| `age_diversity_penalty_weight` | Small negative CI adjustment for age spread. |
| `team_effectiveness_weights` | task_output / team_viability / member_sustainability split. |
