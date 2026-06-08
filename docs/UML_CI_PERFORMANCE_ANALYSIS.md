# Detailed UML + CI → Agile Performance Analysis

This document gives a **detailed UML model** of the Agile AI Simulator, an **annotated map of how Collective Intelligence (CI) connects to agile team performance**, and a **research-paper analysis** showing which paper justifies each link. The percentages shown here are **model weights used for transparent simulation**, not coefficients estimated from empirical Scrum datasets.

All Mermaid blocks can be pasted into [mermaid.live](https://mermaid.live). Standalone copies live in [`diagrams/`](diagrams/).

---

## Table of contents

1. [Detailed UML class diagram](#1-detailed-uml-class-diagram)
2. [How CI connects to agile team performance](#2-how-ci-connects-to-agile-team-performance)
3. [CI → performance impact map (with paper citations)](#3-ci--performance-impact-map-with-paper-citations)
4. [Per-component impact table](#4-per-component-impact-table)
5. [Research-paper analysis](#5-research-paper-analysis)
6. [The conceptual bridge (thesis framing)](#6-the-conceptual-bridge-thesis-framing)

---

## 1. Detailed UML class diagram

```mermaid
classDiagram
    direction TB

    class SimulationConfig {
        <<dataclass — simulation.py>>
        +int team_size
        +int number_of_sprints
        +int number_of_tasks
        +str task_type
        +float ai_support_level
        +float trust_in_ai
        +float ai_reliability
        +float effort_management
        +float skills_knowledge_coordination
        +float task_strategy
        +float female_proportion
        +float team_engagement_baseline
        +float task_complexity
        +float dashboard_quality
        +float collective_memory
        +float collective_attention
        +float collective_reasoning
        +int random_seed
    }

    class TeamMember {
        <<dataclass — team.py>>
        +int member_id
        +str name
        +str gender
        +float skill_level
        +float availability
        +float communication_level
        +float social_sensitivity
        +float trust_in_ai
        +float perceived_ai_reliability
        +float work_speed
        +float error_tendency
    }

    class Task {
        <<dataclass — tasks.py>>
        +int task_id
        +str task_type
        +float difficulty
        +int effort_points
        +int priority
        +float uncertainty
        +float required_skill_level
    }

    class TaskTypeProfile {
        <<lookup — tasks.py>>
        +float coordination_need
        +float defect_risk
        +float uncertainty_modifier
        +float skill_demand
        +float completion_bonus
    }

    class CollectiveIntelligenceComponents {
        <<dataclass — metrics.py>>
        +float transactive_memory
        +float shared_attention
        +float shared_reasoning
        +float social_sensitivity
        +float participation_balance
        +float transactive_coordination
        +float team_engagement
        +float skill_diversity
        +as_dict() dict
    }

    class SprintMetrics {
        <<record — simulation.py>>
        +int sprint_number
        +int planned_points
        +int completed_points
        +float velocity_ratio
        +float completion_rate
        +float defect_rate
        +float decision_quality
        +float collective_intelligence
        +float team_effectiveness
        +float ai_benefit
        +float trust_calibration
        +float team_viability
        +float member_sustainability
        +float overload_pressure
    }

    class SimulationEngine {
        <<module — simulation.py>>
        +run_simulation(config, use_ai) Dict
        -_planned_capacity_points()
        -_task_completion_probability()
        -_task_defect_probability()
        -_update_collective_dimension()
        -_update_team_engagement()
    }

    class MetricsEngine {
        <<module — metrics.py>>
        +compute_collective_intelligence_components()
        +collective_intelligence_score()
        +decision_quality_score()
        +team_effectiveness_score()
        +trust_calibration_score()
        +ai_benefit_score()
    }

    class AISupport {
        <<module — ai_support.py>>
        +allocate_tasks_with_ai()
        +allocate_tasks_without_ai()
        +shared_cognition_assistant()
        +update_team_trust_after_sprint()
    }

    SimulationConfig "1" --> "1" SimulationEngine : configures
    SimulationEngine ..> TeamMember : generates 1..*
    SimulationEngine ..> Task : generates 1..*
    Task "n" --> "1" TaskTypeProfile : profile_of
    SimulationEngine "1" --> "1..*" SprintMetrics : records
    SimulationEngine ..> MetricsEngine : computes scores
    SimulationEngine ..> AISupport : allocates and assists
    TeamMember "1..*" --> "0..*" Task : assigned_to
    TeamMember "1..*" --> CollectiveIntelligenceComponents : contributes
    MetricsEngine ..> CollectiveIntelligenceComponents : builds
    CollectiveIntelligenceComponents ..> SprintMetrics : influences

    note for CollectiveIntelligenceComponents "8 CI subconstructs computed each sprint.\nKommol/Riedl/Woolley: memory, attention,\nand reasoning are core CI systems.\nRiedl/Hackman: effort, skill congruence,\nand strategy are collaboration-process predictors."

    note for SprintMetrics "Agile outcomes: velocity, completion_rate,\ndefect_rate, team_effectiveness.\nHackman framing adds task output,\nteam viability, and member sustainability.\nOutcomes feed back to update CI next sprint."
```

---

## 2. How CI connects to agile team performance

**Core idea:** an agile team is a time-boxed collective that must coordinate, decide, and learn each sprint. CI is the team's capacity to do this well. In the simulator, CI is **both a driver and an outcome** of agile performance.

**Memory terminology:** `collective_memory` is the user-controlled/shared-memory baseline: what the team can retain and reuse across sprints. `transactive_memory` is the computed mechanism: who knows what, whether expertise is recognized, and whether skills/knowledge coordination lets the team access that knowledge. In other words, shared memory is the state; transactive memory is how that state becomes useful in teamwork.

| Agile team reality | CI construct in the model | Paper |
|---|---|---|
| Shared retained knowledge across sprints | `collective_memory` input | Kommol, Riedl & Woolley (2025); Woolley & Mayo (2025) |
| Who knows what on the team | `transactive_memory` | Wegner (1987); Lewis (2003) |
| Everyone focused on the sprint goal | `shared_attention` | Mathieu et al. (2000); Kommol et al. (2025) |
| Good joint planning / technical decisions | `shared_reasoning` | Bahrami et al. (2010); Kommol et al. (2025) |
| Members read and adapt to each other | `social_sensitivity` | Woolley et al. (2010); Engel et al. (2014) |
| No single person dominates | `participation_balance` | Woolley et al. (2010) |
| Coordinating who does what | `transactive_coordination` | Strode et al. (2012); Strode, Dingsøyr & Lindsjørn (2022) |
| Team motivation / involvement | `team_engagement` | Kozlowski & Ilgen (2006); Riedl et al. (2021) |
| Complementary skills | `skill_diversity` | Hong & Page (2004) |
| Scrum-specific effectiveness context | delivery, responsiveness, improvement, autonomy | Verwijs & Russo (2023) |

---

## 3. CI → performance impact map (with paper citations)

```mermaid
flowchart TB
    subgraph predictors["CI and teamwork predictors"]
        effort["effort_management: Riedl2021 and Hackman"]
        skills["skills_knowledge_coordination: Riedl2021 skill congruence"]
        strategy["task_strategy: Riedl2021 strategy"]
        engagement["team_engagement: Riedl2021 and team emergent state"]
        social["social_sensitivity and participation_balance: Woolley2010"]
        diversity["skill_diversity: Hong and Page 2004"]
    end

    subgraph systems["Kommol2025 CI systems"]
        memory["collective/shared memory to transactive_memory"]
        attention["collective attention to shared_attention"]
        reasoning["collective reasoning to shared_reasoning"]
    end

    subgraph ci["Collective Intelligence"]
        aggregate["aggregate CI score: weighted simulation index"]
        decision["decision_quality: reasoning, attention, sensitivity, strategy"]
    end

    subgraph performance["Agile and Scrum performance"]
        completion["completion_probability"]
        defects["defect_probability"]
        velocity["velocity"]
        completionRate["completion_rate"]
        defectRate["defect_rate"]
    end

    subgraph hackman["Hackman team effectiveness"]
        taskOutput["task output: velocity, completion, quality"]
        viability["team_viability: CI, engagement, trust"]
        sustainability["member_sustainability: engagement, effort, low overload"]
        effectiveness["team_effectiveness_score"]
    end

    subgraph agileRefs["Agile theory bridge"]
        verwijs["Verwijs2023: Scrum effectiveness"]
        strode2022["Strode2022 ATEM: shared mental models, communication, trust"]
    end

    predictors --> systems
    social --> aggregate
    diversity --> aggregate
    systems --> aggregate
    reasoning --> decision
    attention --> decision
    social --> decision
    strategy --> decision

    aggregate -->|"direct +10% in task completion formula"| completion
    decision -->|"direct +8% completion and -10% defects"| completion
    decision --> defects
    engagement -->|"direct +5% completion"| completion

    completion --> velocity
    completion --> completionRate
    defects --> defectRate

    velocity --> taskOutput
    completionRate --> taskOutput
    defectRate --> taskOutput
    aggregate --> viability
    engagement --> viability
    effort --> sustainability
    taskOutput --> effectiveness
    viability --> effectiveness
    sustainability --> effectiveness

    verwijs --> performance
    strode2022 --> systems
```

**Three pathways CI affects agile performance:**

1. **Direct via aggregate CI** — the combined CI score raises task completion probability (+10% in the task-completion formula).
2. **Indirect via decision quality** — reasoning, attention, social sensitivity, task strategy, and skills/knowledge coordination raise `decision_quality`, which increases completion (+8%) and reduces defects (-10%).
3. **Direct engagement boost** — `team_engagement` adds +5% to completion on top of its CI contribution.
4. **Hackman effectiveness layer** — team effectiveness now combines task output, team viability, and member sustainability instead of treating velocity as the only success criterion.

Plus a **feedback loop**: good sprint outcomes raise memory, attention, reasoning, and engagement for the next sprint, so CI and agile performance co-evolve.

---

## 4. Per-component impact table

| CI component | CI weight | Main predictors / support | Path to agile performance |
|---|--:|:--:|---|
| Transactive memory | 18% | Collective/shared memory, skill specialization, skills/knowledge coordination | → aggregate CI → completion → velocity/completion → task output and viability |
| Shared attention | 16% | Collective attention, effort management, participation balance, coordination need | → CI **and** decision quality → completion and fewer defects |
| Shared reasoning | 16% | Collective reasoning, task strategy, social sensitivity, skills/knowledge coordination | → CI **and** decision quality → completion, defects, effectiveness |
| Social sensitivity | 16% | Social perceptiveness, female proportion proxy, interpersonal awareness | → CI **and** decision quality → completion and defects |
| Participation balance | 10% | Balanced contribution / communication distribution | → aggregate CI and transactive coordination |
| Transactive coordination | 10% | Memory, coordination need, participation balance | → aggregate CI → completion and viability |
| Team engagement | 8% | Emergent motivation and involvement | → CI **and** direct +5% completion; also team viability/sustainability |
| Skill diversity | 6% | Spread in technical skill levels | → aggregate CI; complementary expertise for complex agile work |

Again, the percentages are **simulation weights** chosen for transparency and sensitivity analysis. They should be presented as model assumptions, not as empirical effect sizes from the cited papers.

---

## 5. Research-paper analysis

### A. Papers linking CI to team performance (general groups)

| Paper | Main finding | Use in simulator |
|---|---|---|
| **Woolley et al. (2010)** *Science* | A general CI factor (c) predicts group performance; driven by social sensitivity and equal participation, not average IQ | Aggregate CI, social sensitivity, participation balance, female proportion |
| **Engel et al. (2014)** *PLOS ONE* | Theory of mind predicts CI online and face-to-face | `social_sensitivity` in distributed agile teams |
| **DeChurch & Mesmer-Magnus (2010)** *JAP* | Meta-analysis: team cognition predicts performance | CI reported separately from delivery metrics |
| **Kozlowski & Ilgen (2006)** *PSPI* | Effectiveness = inputs → processes → emergent states → outcomes | The whole input→process→state→outcome architecture + feedback |
| **Mathieu et al. (2000)** *JAP* | Shared mental models improve process and performance | `shared_attention`, `shared_reasoning`, dashboard |
| **Bahrami et al. (2010)** *Science* | Joint decisions beat individuals when confidence is shared | `decision_quality` as team-level |
| **Hong & Page (2004)** *PNAS* | Diverse solvers beat uniformly high-ability ones | `skill_diversity` in CI |
| **Wegner (1987); Lewis (2003)** | Transactive memory: who knows what + coordination | `collective_memory`, transactive memory subconstruct |

### B. Papers linking team cognition to **agile** performance (closest to your question)

| Paper | Main finding | Use in simulator |
|---|---|---|
| **Moe, Dingsøyr & Dybå (2010)** *IST* | Agile effectiveness depends on trust, shared mental models, coordination | Coordination by task type, trust, CI |
| **Lindsjørn et al. (2016)** *JSS* | Teamwork quality predicts agile project success | `team_effectiveness` as multi-dimensional KPI |
| **Strode et al. (2012)** *JSS* | Agile coordination via synchronization, structure, boundary spanning | `transactive_coordination`, dashboard |
| **Marks, Mathieu & Zaccaro (2001)** *AMR* | Team processes: transition, action, interpersonal | `effort_management`, `task_strategy`, `skills_knowledge_coordination` |
| **Hoda et al. (2013)** *IEEE TSE* | Informal self-organizing roles in agile teams | Future role-based extension |

### C. Strong extensions beyond the original 30-paper set

| Paper | Why it matters |
|---|---|
| **Dingsøyr, Moe et al. (2022)** — Agile Teamwork Effectiveness Model (ATEM), *Empirical Software Engineering* | Formal agile model: effectiveness via shared leadership, adaptability, redundancy, coordinated through shared mental models, communication, trust |
| **Gupta (2022, CMU dissertation)** — CI in open-source software teams | Empirically tests transactive systems (memory, attention, reasoning) on 476 GitHub teams — direct CI + software team evidence |

---

## 6. The conceptual bridge (thesis framing)

The simulator's CI → agile performance link is a **deliberate integration of two literatures**, not a single established empirical result.

```mermaid
flowchart LR
    A["CI literature<br/>Woolley, DeChurch,<br/>Mathieu, Wegner"] --> C["Simulator<br/>CI subconstructs as<br/>mediators of sprint outcomes"]
    B["Agile teamwork literature<br/>Moe, Lindsjørn,<br/>Strode, ATEM"] --> C
    C --> D["Thesis contribution:<br/>explainable CI → agile<br/>performance model"]
```

**Say this (accurate):**
> CI research shows team-level cognition predicts group performance (Woolley 2010; DeChurch & Mesmer-Magnus 2010). Agile research independently shows shared mental models, coordination, and teamwork quality predict Scrum success (Moe 2010; Lindsjørn 2016). This simulator integrates the two by operationalising CI subconstructs as mediators between agile process inputs and sprint outcomes.

**Do not overclaim:**
> Woolley et al. did **not** measure agile velocity. The prototype is theory-driven, not empirically calibrated on agile datasets.

---

## Source files

| Module | Classes / functions |
|---|---|
| `simulation.py` | `SimulationConfig`, `run_simulation`, completion/defect/CI-update logic |
| `team.py` | `TeamMember`, `generate_team` |
| `tasks.py` | `Task`, `TASK_TYPE_PROFILES` |
| `metrics.py` | `CollectiveIntelligenceComponents`, scoring functions |
| `ai_support.py` | Allocation, shared cognition, trust updates |
