# Agile AI Simulator

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

Collective Intelligence is represented with three team-level dimensions:

- collective memory
- collective attention
- collective reasoning

These values influence decision quality and are updated slightly from sprint to sprint based
on communication, dashboard quality, and sprint outcomes.

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
├── requirements.txt
└── README.md
```

## What each file does

- `app.py`
  Streamlit user interface with three tabs: Single Run, Monte Carlo Experiments, and Sensitivity Analysis. Results are cached for faster reruns.

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

- `task_complexity`
  Baseline complexity of the work in the backlog.

- `dashboard_quality`
  Quality of the AI-supported shared dashboard and coordination view.

- `collective_memory`
  The team's ability to retain and reuse shared knowledge.

- `collective_attention`
  The team's ability to focus collectively on the right issues.

- `collective_reasoning`
  The team's ability to interpret information and make decisions together.

- `random_seed`
  Seed value used for reproducible results.

### Team member variables

Each simulated team member has:

- `skill_level`
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
- collective attention
- decision support

The effect depends on:

- AI support level
- dashboard quality
- communication quality

This reflects the idea that AI can act as a shared cognition layer that helps teams maintain common situational awareness.

## Output metrics

The app reports:

- sprint velocity
- task completion rate
- defect rate
- decision quality
- collective intelligence score
- transactive memory
- social sensitivity
- participation balance
- trust calibration
- team effectiveness score
- AI benefit score

These metrics are intentionally simple and interpretable. They are meant for conceptual experimentation, not operational forecasting.

## Connection to agile team effectiveness

The prototype models agile team effectiveness as a combination of:

- delivery performance
- work quality
- decision quality
- Collective Intelligence

This aligns with the view that effective agile teams are not only fast, but also adaptive, coordinated, and capable of making good decisions together.

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

- add roles such as Scrum Master, Product Owner, and Developer
- distinguish between planned and emergent work
- simulate task dependencies
- add sprint phases (planning, execution, review, retrospective)
- add different AI agent types
- calibrate formulas with empirical data
- export results for thesis analysis
