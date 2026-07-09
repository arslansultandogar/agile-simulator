# Agile AI Simulator

> **Model version 2.0** — externalized weights, preset scenarios, exports, mixed
> backlogs with carry-over, task dependencies and rework spillover, sprint-phase
> modifiers, Scrum roles, broadened sensitivity analysis, and a pytest suite.
> See [What's new in model v2.0](#whats-new-in-model-v20).

## What this simulator does

`agile-ai-simulator` is a first-version academic prototype built with Python and Streamlit.
It simulates an agile team working through multiple sprints and compares two scenarios:

- with AI support
- without AI support

The purpose is not to predict real company outcomes with precision. Instead, it provides a
simple and logically consistent experimental environment for exploring how AI support might
affect agile team effectiveness, sprint performance, and Collective Intelligence.

The model uses readable formulas so the logic can be explained clearly in an academic thesis.

## Core idea

The simulator treats team performance as a combination of:

- individual capability
- coordination quality
- task difficulty
- AI-supported task allocation
- AI-supported shared cognition
- Collective Intelligence

Collective Intelligence is represented with team-level cognitive and process dimensions:

- collective memory
- collective focus of attention
- collective reasoning
- social sensitivity
- participation balance
- team engagement
- skill diversity
- age diversity
- transactive coordination

These values influence decision quality and are updated slightly from sprint to sprint based
on task coordination needs, dashboard quality, trust calibration, and sprint outcomes.

## How to install dependencies

Create and activate a virtual environment if you want:

```bash
python -m venv .venv
source .venv/bin/activate
```

Then install dependencies:

```bash
pip install -r requirements.txt
```

## How to run it

Run the Streamlit app with:

```bash
streamlit run app.py
```

## Project structure

```text
agile-ai-simulator/
├── app.py
├── simulation.py
├── experiments.py
├── team.py
├── tasks.py
├── ai_support.py
├── metrics.py
├── config_loader.py
├── config/
│   └── weights.yaml
├── tests/
│   ├── test_metrics.py
│   ├── test_monotonic.py
│   └── test_simulation.py
├── docs/
│   ├── PARAMETER_DICTIONARY.md
│   ├── UML_CI_PERFORMANCE_ANALYSIS.md
│   └── diagrams/
├── requirements.txt
└── README.md
```

## What each file does

- `app.py`
  Streamlit user interface with four tabs: Single Run, Monte Carlo Experiments, Sensitivity Analysis, and Assumptions. Includes preset scenarios, task-mix sliders, and CSV/JSON exports. Results are cached for faster reruns.

- `config_loader.py` and `config/weights.yaml`
  Externalized model weights (CI component weights, age-diversity penalty, team-effectiveness layer, and `model_version`). Edit the YAML to tune the model without touching Python source.

- `simulation.py`
  Main simulation engine. It runs the model sprint by sprint, calculates completions and defects, updates Collective Intelligence subcomponents, trust calibration, and returns the results.

- `experiments.py`
  Monte Carlo replication runner, confidence-interval summaries, scenario comparison, and one-parameter sensitivity analysis.

- `team.py`
  Defines the `TeamMember` dataclass and creates the simulated agile team.

- `tasks.py`
  Defines the `Task` dataclass, creates the backlog, and selects sprint tasks.

- `ai_support.py`
  Contains the AI support modules:
  1. AI Task Allocation Assistant
  2. AI Dashboard / Shared Cognition Assistant
  3. Trust calibration and learned trust updates

- `metrics.py`
  Contains helper formulas for CI subcomponents, decision quality, trust calibration, team effectiveness, and AI benefit.

- `requirements.txt`
  Lists the required Python packages.

## Main variables and what they mean

### User-controlled simulation inputs

- `team_size`
  Number of people in the agile team.

- `number_of_sprints`
  Number of simulated sprints.

- `number_of_tasks`
  Number of backlog tasks generated at the start.

- `ai_support_level`
  Overall intensity of AI support in the scenario.

- `trust_in_ai`
  Baseline level of team trust in AI recommendations.

- `ai_reliability`
  Actual reliability of AI recommendations. Lower values increase allocation mistakes and reduce AI benefit unless trust is calibrated.

- `task_type`
  Type of work in the backlog: feature, bug, refactor, or spike. Each type has different coordination need, defect risk, uncertainty, and skill demand.

- `effort_management`
  Effort-related process measure for sustaining and allocating effort. It affects capacity and overload tolerance.

- `skills_knowledge_coordination`
  Knowledge / skills process measure for matching expertise to contributions. It is distinct from individual `skill_level`.

- `task_strategy`
  Strategy updating process measure for selecting and adapting the work approach. It is not a static strategy attribute.

- `female_proportion`
  Proportion of women in the simulated team. It is modeled as a proxy pathway through social sensitivity when social perceptiveness is not directly measured.

- `team_engagement_baseline`
  Initial team-level engagement. Engagement then evolves from sprint outcomes, decision quality, trust calibration, and consequentiality.

- `consequentiality`
  Consequentiality / shared purpose. It strengthens team engagement, shared attention, viability, and sustainability.

- `task_complexity`
  Baseline complexity of the work in the backlog.

- `dashboard_quality`
  Quality of the AI-supported shared dashboard and coordination view.

- `collective_memory`
  The team's ability to retain and reuse shared knowledge.

- `collective_attention`
  The team's collective focus of attention on the right issues.

- `collective_reasoning`
  The team's ability to interpret information and make decisions together.

- `random_seed`
  Seed value used for reproducible results.

### Team member variables

Each simulated team member has:

- `skill_level`
- `age`
- `gender`
- `availability`
- `communication_level`
- `social_sensitivity`
- `trust_in_ai`
- `perceived_ai_reliability`
- `work_speed`
- `error_tendency`

### Task variables

Each backlog task has:

- `task_type`
- `difficulty`
- `effort_points`
- `priority`
- `uncertainty`
- `required_skill_level`

## AI support in the prototype

### 1. AI Task Allocation Assistant

This module assigns tasks to the most suitable team member using a simple score based on:

- skill fit
- availability
- workload balance
- trust in AI

This reflects the idea that AI can improve coordination by helping the team match work to people more effectively.

### 2. AI Dashboard / Shared Cognition Assistant

This module improves:

- coordination
- collective focus of attention
- decision support

The effect depends on:

- AI support level
- dashboard quality
- task coordination need
- task strategy
- trust calibration

This reflects the idea that AI can act as a shared cognition layer that helps teams maintain common situational awareness.

## Connection to process criteria and diversity

The current model includes three team process criteria inspired by Marks, Mathieu, and Zaccaro (2001) and aligned with Riedl et al. (2021):

- `effort_management`
  Represents the effort-related process: how well the team sustains and distributes effort during the sprint.

- `skills_knowledge_coordination`
  Represents the knowledge / skills process: how well the team knows who has the relevant expertise and uses that knowledge. It is different from individual `skill_level`.

- `task_strategy`
  Represents the strategy updating process: how well the team selects, monitors, and adapts its work approach.

The model also includes `female_proportion` as a proxy route through social sensitivity following Woolley et al. (2010), `skill_diversity` as a functional diversity proxy inspired by Hong and Page (2004), and `age_diversity` as a negative CI predictor following the supervisor feedback. The CI system is explained through collective/shared memory, attention, and reasoning following Kommol, Riedl, and Woolley (2025). The simulator does not implement vocal synchrony or NLP-based audio analysis; instead, `social_sensitivity` represents the underlying social perceptiveness construct.

## Output metrics

The app reports:

- sprint velocity
- task completion rate
- defect rate
- decision quality
- collective intelligence score
- transactive memory
- shared attention
- shared reasoning
- social sensitivity
- participation balance
- team engagement
- skill diversity
- age diversity
- effort-related process
- knowledge / skills process
- strategy updating process
- consequentiality / shared purpose
- trust calibration
- team viability
- member sustainability
- overload pressure
- team effectiveness score
- AI benefit score

Backlog-realism and workflow metrics (Weeks 2–3):

- carry-over points and carry-over rate
- blocked tasks (from dependencies)
- rework created and rework completed
- defects caught in review

These metrics are intentionally simple and interpretable. They are meant for conceptual experimentation, not operational forecasting.

## What's new in model v2.0

The simulator was extended with a balanced set of tooling, realism, depth, and
validation improvements (see `docs/PARAMETER_DICTIONARY.md` for full definitions):

- **Config-driven weights** — CI weights, the age-diversity penalty, and the
  team-effectiveness layer live in `config/weights.yaml` with a `model_version`.
- **Preset scenarios** — high-trust/high-reliability, over-trust/low-reliability,
  strong-process/weak-AI, and weak-process/strong-AI.
- **Exports** — CSV and JSON downloads for single-run, Monte Carlo, and
  sensitivity results.
- **Charts** — viability, sustainability, overload pressure, CI subcomponents
  over time, and a planned-vs-completed/carry-over backlog chart.
- **Assumptions panel** — process vs attribute assumptions and the female-proportion
  proxy framing.
- **Mixed backlogs and carry-over** — configurable feature/bug/refactor/spike mix,
  planned-vs-completed tracking, and carry-over as a first-class metric.
- **Dependencies and rework** — `depends_on` blocker propagation and defect
  rework spillover that appears in later sprints.
- **Sprint phases** — planning (strategy), review (defect detection), and
  retrospective (learning rate) modifiers layered on the update functions.
- **Roles** — Product Owner, Scrum Master, Developer, and Tester behavioral modifiers.
- **Validation** — broadened sensitivity coverage, a sensitivity-stability summary,
  and a `pytest` suite (metrics formulas, monotonic checks, deterministic smoke test).

## Running the tests

```bash
pip install -r requirements.txt
pytest
```

## Connection to agile team effectiveness

The prototype models agile team effectiveness with a Hackman-inspired structure:

- task output: delivery performance and work quality
- team viability: Collective Intelligence, engagement, trust calibration, and decision quality
- member sustainability: engagement, effort management, and low overload pressure

This aligns with the view that effective agile teams are not only fast, but also adaptive, coordinated, sustainable, and capable of working together in future sprints. The Scrum/teamwork interpretation is grounded in Verwijs and Russo (2023) and Strode, Dingsøyr, and Lindsjørn (2022).

## Connection to Collective Intelligence

Collective Intelligence is the theoretical baseline of the simulator.

Instead of treating performance as only the sum of individual skills, the prototype assumes
that teams perform better when they can:

- remember relevant information together
- focus attention together
- reason together

These team-level capabilities influence sprint results and also evolve over time.

## Connection to human-AI teaming

This prototype treats AI as a support mechanism rather than a replacement for human work.
The AI agents do not execute tasks themselves. Instead, they improve:

- task allocation
- shared awareness
- coordination
- decision support

This makes the model useful for discussing human-AI teaming in agile environments, especially in early-stage academic research.

## Important limitations

- This is an academic prototype, not a production system.
- The formulas are simplified on purpose.
- The results are illustrative, not validated predictions.
- No external APIs are used.
- No real company data is used.

## Experiment features

The app now supports:

- **Single Run**: one deterministic comparison using the selected random seed
- **Monte Carlo Experiments**: many replications with mean, standard deviation, and 95% confidence intervals
- **Sensitivity Analysis**: vary one parameter and observe average changes in effectiveness, CI, defects, and trust calibration

100 Monte Carlo replications typically finish in a few seconds at the default simulation size.

## Suggested future extensions

Several previously-suggested extensions are now implemented in model v2.0:
roles (Scrum Master / Product Owner / Developer / Tester), planned-vs-emergent
work via carry-over and rework, task dependencies, sprint phases, and result
exports. Remaining directions include:

- add different AI agent types
- calibrate formulas with empirical data
- richer dependency graphs (multiple upstream tasks, critical-path effects)
- per-role capacity and specialization instead of behavioral modifiers only
