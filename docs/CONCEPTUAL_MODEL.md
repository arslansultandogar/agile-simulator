# Conceptual Model — Agile AI Simulator

This document describes the structure, variables, and causal relationships in the Agile AI Simulator. Each diagram is also available as a standalone Mermaid file under [`docs/diagrams/`](diagrams/) for import into draw.io, Mermaid Live Editor, or presentation tools.

**For your presentation:** use [`PRESENTATION_ONE_PAGE.mmd`](diagrams/PRESENTATION_ONE_PAGE.mmd) or open [`PRESENTATION_ONE_PAGE.html`](PRESENTATION_ONE_PAGE.html) in a browser and export to PDF/image.

---

## Table of contents

1. [One-page overview (presentation)](#1-one-page-overview-presentation)
2. [UML class diagram](#2-uml-class-diagram)
3. [Variable flow / causal model](#3-variable-flow--causal-model)
4. [Entity–relationship view](#4-entityrelationship-view)
5. [Collective Intelligence sub-model](#5-collective-intelligence-sub-model)
6. [Human–AI teaming sub-model](#6-humanai-teaming-sub-model)
7. [Sprint lifecycle (sequence)](#7-sprint-lifecycle-sequence)
8. [Scrum, CI, and team effectiveness bridge](#8-scrum-ci-and-team-effectiveness-bridge)
9. [Variable dictionary](#9-variable-dictionary)

---

## 1. One-page overview (presentation)

Three-panel view: **Inputs & agents → Processes & emergent states → Outcomes**.

See: [`diagrams/PRESENTATION_ONE_PAGE.mmd`](diagrams/PRESENTATION_ONE_PAGE.mmd)

```mermaid
flowchart LR
    subgraph IN["Inputs & Agents"]
        direction TB
        CFG["SimulationConfig<br/>(19 parameters)"]
        TM["TeamMember × N<br/>skill, age, gender, trust, sensitivity"]
        TK["Task × M<br/>effort, difficulty, type"]
        TTP["TaskTypeProfile<br/>feature | bug | refactor | spike"]
        CFG --> TM
        CFG --> TK
        TK --> TTP
    end

    subgraph MID["Processes & Emergent States"]
        direction TB
        CAP["Capacity planning<br/>← effort-related process"]
        ALLOC["Task allocation<br/>← strategy updating process, AI"]
        EXEC["Task execution<br/>← knowledge/skills process"]
        CI["Collective Intelligence<br/>(8 subconstructs + age-diversity penalty)"]
        TE["team_engagement"]
        TC["trust_calibration"]
        DQ["decision_quality"]
        CAP --> ALLOC --> EXEC
        EXEC --> CI
        EXEC --> TE
        EXEC --> TC
        CI --> DQ
    end

    subgraph OUT["Outcomes"]
        direction TB
        VEL["velocity"]
        COMP["completion_rate"]
        DEF["defect_rate"]
        EFF["team_effectiveness"]
        AIB["ai_benefit"]
    end

    IN --> MID --> OUT
```

---

## 2. UML class diagram

See: [`diagrams/01_uml_class_diagram.mmd`](diagrams/01_uml_class_diagram.mmd)

```mermaid
classDiagram
    class SimulationConfig {
        +team_size
        +number_of_sprints
        +number_of_tasks
        +task_type
        +ai_support_level
        +trust_in_ai
        +ai_reliability
        +effort_management
        +skills_knowledge_coordination
        +task_strategy
        +female_proportion
        +team_engagement_baseline
        +consequentiality
        +task_complexity
        +dashboard_quality
        +collective_memory
        +collective_attention
        +collective_reasoning
        +random_seed
    }

    class TeamMember {
        +member_id
        +name
        +gender
        +age
        +skill_level
        +availability
        +communication_level
        +social_sensitivity
        +trust_in_ai
        +perceived_ai_reliability
        +work_speed
        +error_tendency
    }

    class Task {
        +task_id
        +task_type
        +difficulty
        +effort_points
        +priority
        +uncertainty
        +required_skill_level
    }

    class TaskTypeProfile {
        +coordination_need
        +defect_risk
        +uncertainty_modifier
        +skill_demand
        +completion_bonus
    }

    class CollectiveIntelligenceComponents {
        +transactive_memory
        +shared_attention
        +shared_reasoning
        +social_sensitivity
        +participation_balance
        +transactive_coordination
        +team_engagement
        +skill_diversity
        +age_diversity
    }

    class SprintResult {
        +velocity
        +completion_rate
        +defect_rate
        +decision_quality
        +collective_intelligence
        +team_effectiveness
        +ai_benefit
        +trust_calibration
        +team_viability
        +member_sustainability
        +overload_pressure
        +consequentiality
        +age_diversity
    }

    class AISupport {
        <<module>>
        allocate_tasks_with_ai()
        shared_cognition_assistant()
        update_team_trust_after_sprint()
    }

    class MetricsEngine {
        <<module>>
        compute_collective_intelligence_components()
        decision_quality_score()
        team_effectiveness_score()
        trust_calibration_score()
    }

    SimulationConfig "1" --> "1..*" TeamMember : generates
    SimulationConfig "1" --> "1..*" Task : generates
    Task "n" --> "1" TaskTypeProfile : uses
    TeamMember "1..*" --> "0..*" Task : assigned_to
    TeamMember "1..*" --> "1" CollectiveIntelligenceComponents : contributes_to
    CollectiveIntelligenceComponents "1" --> "1" SprintResult : influences
    AISupport ..> TeamMember : updates trust
    AISupport ..> Task : allocates
    MetricsEngine ..> CollectiveIntelligenceComponents : computes
    MetricsEngine ..> SprintResult : computes
```

| Class | Role |
|---|---|
| `SimulationConfig` | All user-controlled inputs (`simulation.py`) |
| `TeamMember` | Individual agents (`team.py`) |
| `Task` | Backlog / sprint work items (`tasks.py`) |
| `TaskTypeProfile` | Lookup table: feature, bug, refactor, spike |
| `CollectiveIntelligenceComponents` | Emergent team cognition state (`metrics.py`) |
| `SprintResult` | Outputs recorded per sprint |
| `AISupport` / `MetricsEngine` | Behavioral modules (`ai_support.py`, `metrics.py`) |

---

## 3. Variable flow / causal model

See: [`diagrams/02_variable_flow_causal.mmd`](diagrams/02_variable_flow_causal.mmd)

```mermaid
flowchart TB
    subgraph inputs [Inputs — SimulationConfig]
        TS[team_size]
        NS[number_of_sprints]
        NT[number_of_tasks]
        TT[task_type]
        TC[task_complexity]
        AI[ai_support_level]
        TR[trust_in_ai]
        AR[ai_reliability]
        DQ[dashboard_quality]
        EM[effort_related_process]
        SK[knowledge_skills_process]
        TS2[strategy_updating_process]
        FP[female_proportion]
        TEB[team_engagement_baseline]
        CON[consequentiality_shared_purpose]
        CM[collective_memory]
        CA[collective_attention]
        CR[collective_reasoning]
    end

    subgraph agents [Agents]
        TM[TeamMember attributes]
        TK[Task attributes]
        TTP[TaskTypeProfile]
    end

    subgraph processes [Team Processes per Sprint]
        CAP[Capacity planning]
        ALLOC[Task allocation]
        EXEC[Task execution]
        REV[Outcome evaluation]
        TRUST[Trust learning]
    end

    subgraph emergent [Emergent States]
        TE[team_engagement]
        CI[CollectiveIntelligenceComponents]
        TC2[trust_calibration]
        DQ2[decision_quality]
    end

    subgraph outcomes [Outcomes]
        VEL[velocity]
        COMP[completion_rate]
        DEF[defect_rate]
        EFF[team_effectiveness]
        TV[team_viability]
        MS[member_sustainability]
        OP[overload_pressure]
        AIB[ai_benefit]
    end

    inputs --> agents
    FP --> TM
    TT --> TTP
    TTP --> TK

    agents --> processes
    EM --> CAP
    CON --> TE
    CON --> MS
    TS2 --> ALLOC
    SK --> EXEC
    AI --> ALLOC
    AR --> ALLOC

    processes --> emergent
    CM --> CI
    CA --> CI
    CR --> CI
    TM --> CI
    TEB --> TE
    REV --> TE
    AR --> TC2
    TM --> TC2

    emergent --> outcomes
    CI --> EFF
    DQ2 --> EFF
    CI --> TV
    TE --> TV
    TE --> MS
    CAP --> OP
    OP --> MS
    TV --> EFF
    MS --> EFF
    TE --> COMP
    SK --> DEF
    AI --> AIB
```

---

## 4. Entity–relationship view

See: [`diagrams/03_entity_relationship.mmd`](diagrams/03_entity_relationship.mmd)

```mermaid
erDiagram
    SIMULATION ||--o{ SPRINT : contains
    SIMULATION ||--|| TEAM : has
    SIMULATION ||--|| BACKLOG : has
    SIMULATION {
        int team_size
        int number_of_sprints
        string task_type
        float ai_support_level
        float trust_in_ai
        float ai_reliability
        float effort_management
        float skills_knowledge_coordination
        float task_strategy
        float female_proportion
        float team_engagement_baseline
        float collective_memory
        float collective_attention
        float collective_reasoning
    }

    TEAM ||--|{ TEAM_MEMBER : comprises
    TEAM {
        int team_size
        float female_proportion
    }

    TEAM_MEMBER {
        int member_id
        string gender
        float skill_level
        float social_sensitivity
        float trust_in_ai
        float perceived_ai_reliability
    }

    BACKLOG ||--|{ TASK : contains
    BACKLOG {
        int number_of_tasks
        string task_type
        float task_complexity
    }

    TASK {
        int task_id
        string task_type
        int effort_points
        float difficulty
        float uncertainty
    }

    SPRINT ||--|{ TASK : selects
    SPRINT ||--|| SPRINT_METRICS : produces
    SPRINT ||--|| CI_STATE : snapshots
    SPRINT {
        int sprint_number
        int planned_points
        int completed_points
    }

    TEAM_MEMBER }o--o{ TASK : assigned
    SPRINT_METRICS {
        float velocity
        float completion_rate
        float defect_rate
        float team_effectiveness
        float ai_benefit
    }

    CI_STATE {
        float transactive_memory
        float shared_attention
        float shared_reasoning
        float social_sensitivity
        float team_engagement
        float skill_diversity
        float collective_intelligence
    }
```

**Cardinality summary**

| Relationship | Cardinality |
|---|---|
| Simulation → Sprint | 1 : many |
| Simulation → Team | 1 : 1 |
| Team → TeamMember | 1 : many |
| Simulation → Backlog | 1 : 1 |
| Backlog → Task | 1 : many |
| Sprint → Task | many : many (subset per sprint) |
| TeamMember → Task | many : many (assignments) |
| Sprint → SprintMetrics | 1 : 1 |
| Sprint → CI State | 1 : 1 (evolving snapshot) |

---

## 5. Collective Intelligence sub-model

See: [`diagrams/04_collective_intelligence.mmd`](diagrams/04_collective_intelligence.mmd)

```mermaid
flowchart LR
    CM[collective_memory] --> TM[transactive_memory]
    SKC[knowledge_skills_process] --> TM
    TMskills[TeamMember.skill_level] --> TM
    SD[skill_diversity] --> TM

    CA[collective_attention] --> SA[shared_attention]
    EM[effort_related_process] --> SA
    CON[consequentiality_shared_purpose] --> SA
    PB --> SA
    CN[coordination_need from task type] --> SA

    CR[collective_reasoning] --> SR[shared_reasoning]
    TS[strategy_updating_process] --> SR
    SKC --> SR

    TMmembers[TeamMember.social_sensitivity] --> SS[social_sensitivity]
    FP[female_proportion] --> TMmembers

    TMcomm[TeamMember.communication_level] --> PB[participation_balance]
    CM --> TC[transactive_coordination]
    CN --> TC
    PB --> TC

    TEB[team_engagement] --> TE[team_engagement in CI]
    SD --> SDout[skill_diversity in CI]
    AD[age_diversity] --> ADP[negative CI predictor]

    TM --> CI[Collective Intelligence Score]
    SA --> CI
    SR --> CI
    SS --> CI
    PB --> CI
    TC --> CI
    TE --> CI
    SDout --> CI
    ADP --> CI
```

**CI component weights** (from `metrics.py`)

| Component | Weight |
|---|--:|
| Transactive memory | 18% |
| Shared attention | 16% |
| Shared reasoning | 16% |
| Social sensitivity | 16% |
| Participation balance | 10% |
| Transactive coordination | 10% |
| Team engagement | 8% |
| Skill diversity | 6% |

---

## 6. Human–AI teaming sub-model

See: [`diagrams/05_human_ai_teaming.mmd`](diagrams/05_human_ai_teaming.mmd)

```mermaid
flowchart TB
    TR[trust_in_ai] --> UPTAKE[AI advice uptake]
    AR[ai_reliability] --> ACTUAL[Actual AI quality]
    PR[perceived_ai_reliability] --> TC[trust_calibration]
    AR --> TC

    AI[ai_support_level] --> ALLOC[AI Task Allocation]
    DQ[dashboard_quality] --> DASH[Shared Cognition Dashboard]
    TC --> ALLOC
    TC --> DASH
    AR --> ALLOC

    ALLOC --> AQ[allocation_quality]
    DASH --> CG[coordination_gain]
    DASH --> DG[decision_gain]

    AQ --> AIB[AI Benefit Score]
    CG --> AIB
    DG --> AIB
    TC --> AIB

    ALLOC --> COMP[Completion probability]
    DASH --> DQout[Decision quality]
    TC --> DEF[Defect probability]
```

**AI benefit weights** (from `metrics.py`)

| Component | Weight |
|---|--:|
| Allocation quality | 45% |
| Coordination gain | 30% |
| Decision gain | 25% |

Multiplied by `ai_support_level × trust_calibration`.

---

## 7. Sprint lifecycle (sequence)

See: [`diagrams/06_sprint_lifecycle.mmd`](diagrams/06_sprint_lifecycle.mmd)

```mermaid
sequenceDiagram
    participant Config as SimulationConfig
    participant Team as TeamMember[]
    participant Backlog as Task[]
    participant AI as AISupport
    participant Metrics as MetricsEngine
    participant State as CI + Engagement

    Config->>Team: generate_team()
    Config->>Backlog: generate_backlog()

    loop Each Sprint
        Backlog->>Backlog: select_sprint_tasks()
        AI->>Team: allocate tasks
        AI->>Metrics: shared_cognition_assistant()
        Metrics->>State: compute CI components
        Metrics->>Metrics: decision_quality

        loop Each Task
            Metrics->>Metrics: completion_probability
            Metrics->>Metrics: defect_probability
        end

        Metrics->>State: update collective_memory/attention/reasoning
        Metrics->>State: update team_engagement
        AI->>Team: update trust_in_ai
        Metrics->>Metrics: team_effectiveness, ai_benefit
    end
```

---

## 8. Scrum, CI, and team effectiveness bridge

See: [`diagrams/08_scrum_ci_team_effectiveness_bridge.mmd`](diagrams/08_scrum_ci_team_effectiveness_bridge.mmd)

This bridge explains how the simulator connects the agile/Scrum literature to Collective Intelligence:

- **Verwijs & Russo (2023)** ground Scrum team effectiveness in responsiveness, stakeholder concern, continuous improvement, autonomy, and management support.
- **Strode, Dingsøyr & Lindsjørn (2022)** connect agile teamwork effectiveness to shared mental models, communication, and trust.
- **Riedl et al. (2021)** identify predictor items, especially effort-related process, strategy updating process, knowledge/skills process, individual skill, diversity, social perceptiveness, and female proportion as a proxy when social perceptiveness is not directly measured.
- **Kommol, Riedl & Woolley (2025)** assign these predictors to collective/shared memory, attention, and reasoning.
- **Hackman (1987)** and **Wageman, Hackman & Lehman (2005)** broaden team effectiveness beyond output to include future viability and member sustainability.
- **Consequentiality/shared purpose** is modeled as an upstream driver of team engagement, shared attention, team viability, and sustainability.

```mermaid
flowchart LR
    riedl["Riedl2021 predictor items"] --> systems["Kommol2025 memory, attention, reasoning"]
    hackman["Hackman/Wageman process criteria"] --> systems
    systems --> ci["Collective Intelligence"]
    ci --> performance["Agile/Scrum performance"]
    performance --> effectiveness["Task output, viability, sustainability"]
    performance --> learning["Sprint learning feedback"]
    learning --> systems
```

**Memory terminology:** `collective_memory` is the shared-memory baseline controlled by the user. `transactive_memory` is the computed CI component that operationalizes how that shared memory is accessed: who knows what, how differentiated the skills are, and how well the team coordinates knowledge.

**Process terminology:** `effort_management`, `skills_knowledge_coordination`, and `task_strategy` are displayed as effort-related process, knowledge/skills process, and strategy updating process. They are process measures, not individual attributes.

**Female proportion note:** because the simulator generates social sensitivity directly, female proportion should be read as a proxy pathway through social perceptiveness, not as a direct causal or biological claim.

**Percentage note:** The weights in the simulator are transparent modeling assumptions for explanation and sensitivity analysis. They are not empirical coefficients estimated from the papers.

---

## 9. Variable dictionary

| Role | Variables |
|---|---|
| **Structural inputs** | `team_size`, `number_of_sprints`, `number_of_tasks`, `task_type`, `task_complexity` |
| **Process measures** (Riedl / Hackman / Wageman) | `effort_management` as effort-related process, `skills_knowledge_coordination` as knowledge/skills process, `task_strategy` as strategy updating process |
| **Purpose and engagement** | `consequentiality`, `team_engagement_baseline`, emergent `team_engagement` |
| **Diversity** (Woolley / Hong & Page / professor feedback) | `female_proportion` through social sensitivity, `gender`, `skill_diversity`, `age`, `age_diversity` |
| **CI system baseline inputs** | `collective_memory` / shared memory, `collective_attention`, `collective_reasoning` |
| **AI inputs** | `ai_support_level`, `trust_in_ai`, `ai_reliability`, `dashboard_quality` |
| **Individual agent state** | `skill_level`, `age`, `availability`, `communication_level`, `social_sensitivity`, `trust_in_ai`, `perceived_ai_reliability`, `work_speed`, `error_tendency` |
| **Task state** | `difficulty`, `effort_points`, `priority`, `uncertainty`, `required_skill_level` |
| **Emergent team state** | `team_engagement`, CI subcomponents, `trust_calibration`, `decision_quality` |
| **Outcomes** | `velocity`, `completion_rate`, `defect_rate`, `team_effectiveness`, `team_viability`, `member_sustainability`, `age_diversity`, `ai_benefit` |

---

## Source files

| Module | Primary classes / functions |
|---|---|
| `simulation.py` | `SimulationConfig`, sprint engine |
| `team.py` | `TeamMember`, `generate_team()` |
| `tasks.py` | `Task`, `TASK_TYPE_PROFILES` |
| `metrics.py` | `CollectiveIntelligenceComponents`, scoring functions |
| `ai_support.py` | Allocation, shared cognition, trust updates |
| `experiments.py` | Monte Carlo, sensitivity analysis |
| `app.py` | Streamlit UI |

---

## Which diagram for which audience?

| Question | Use |
|---|---|
| What are the main building blocks? | UML class diagram (§2) |
| How do variables influence outcomes? | Causal variable graph (§3) |
| What is stored vs. computed? | Entity–relationship view (§4) |
| What is Collective Intelligence here? | CI sub-model (§5) |
| How does AI fit in? | Human–AI sub-model (§6) |
| What happens each sprint? | Sprint lifecycle (§7) |
| How do Scrum, CI, and team effectiveness connect? | Scrum-CI bridge (§8) |
| One slide for the whole model | One-page overview (§1) |
