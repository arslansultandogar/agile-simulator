# Agile AI Simulator — Detailed Presentation Report

**Purpose:** Academic presentation and thesis support document  
**Project:** `agile-ai-simulator`  
**Topic:** Collective Intelligence, agile team effectiveness, and human–AI teaming in software development  
**Date:** May 2026

---

## 1. Executive Summary

The **Agile AI Simulator** is an academic prototype that models how an agile software team performs across multiple sprints under two conditions:

1. **With AI support** — AI assists task allocation and shared team cognition (dashboard/coordination view).
2. **Without AI support** — the team uses simpler heuristics only.

The simulator is **not** designed to predict real company outcomes with precision. It is designed to provide a **transparent, logically consistent experimental environment** for exploring research questions such as:

- How does Collective Intelligence (CI) influence sprint outcomes?
- When does AI support improve team effectiveness?
- When does AI fail because of low reliability or miscalibrated trust?
- How do different **task types** (feature, bug, refactor, spike) change coordination needs and outcomes?

The model uses **readable formulas**, **Monte Carlo replication**, and **sensitivity analysis**, making it suitable for thesis explanation, classroom presentation, and conceptual experimentation.

---

## 2. Research Problem and Contribution

### 2.1 The Problem

Agile teams are expected to deliver quickly, adapt continuously, and maintain quality. Recent AI tools (copilots, planning assistants, dashboards, allocation systems) promise to improve coordination and decision-making. However, research shows that:

- Team performance is **not** just the sum of individual skills.
- AI can help **or harm**, depending on trust, reliability, task type, and team cognition.
- Single-run simulations or anecdotal examples are **not enough** for academic claims.

There is a need for a model that connects **Collective Intelligence theory**, **agile teamwork research**, and **human–AI trust literature** in one explainable framework.

### 2.2 What This Project Contributes

| Contribution | Description |
|---|---|
| **Conceptual bridge** | Links CI theory to agile sprint outcomes and AI support mechanisms |
| **Comparative design** | Runs the same scenario with and without AI to isolate AI benefit |
| **CI subconstructs** | Measures CI through transactive memory, attention, reasoning, social sensitivity, participation balance, and coordination |
| **Trust calibration** | Models actual vs perceived AI reliability and learned trust over sprints |
| **Task-type realism** | Replaces generic “communication quality” with task-type profiles (feature, bug, refactor, spike) |
| **Experimental rigor** | Supports Monte Carlo replications and sensitivity analysis |
| **Thesis-friendly transparency** | Every metric is computed from explicit, inspectable formulas |

---

## 3. Benefits of This Research

### 3.1 Academic Benefits

- Provides a **structured testbed** for thesis hypotheses about CI and AI-supported agile teams.
- Makes assumptions **visible** (unlike black-box ML models).
- Supports **replication** through random seeds and Monte Carlo batches.
- Connects the prototype to **30 foundational papers** across CI, agile teams, simulation methods, and human–AI interaction.
- Enables **what-if analysis**: “What if AI reliability drops?” or “What if the backlog is mostly spikes?”

### 3.2 Practical Benefits (for teams and organizations)

- Helps explain **why AI adoption is not uniformly positive**.
- Shows that **trust calibration** matters as much as AI capability.
- Demonstrates that **task type** changes coordination demand and risk profile.
- Supports discussion of **where AI should assist** (allocation, shared cognition) vs where humans must remain accountable.
- Gives managers and Scrum Masters a **conceptual language** for sprint retrospectives: CI, decision quality, defect rate, trust calibration.

### 3.3 Methodological Benefits

- Combines **agent-based thinking** (team members, tasks, sprints) with **system dynamics** (CI evolves over time).
- Uses **distribution-based reporting** (mean, std dev, 95% CI) instead of one lucky/unlucky seed.
- Supports **sensitivity analysis** to identify which parameters most affect outcomes.

---

## 4. Theoretical Framework Used in the Simulator

The simulator is built on four research layers:

```text
Layer 1: Collective Intelligence
         → team-level memory, attention, reasoning, social sensitivity

Layer 2: Agile Team Effectiveness
         → velocity, completion, defects, coordination by task type

Layer 3: Human–AI Teaming
         → AI allocation assistant, shared cognition dashboard, trust calibration

Layer 4: Simulation Methodology
         → replication, sensitivity analysis, explicit submodels
```

### 4.1 Core hypothesis (implicit in the model)

> Agile team effectiveness is a function of **individual capability**, **Collective Intelligence**, **task characteristics**, and **human–AI coordination quality** — not AI alone.

---

## 5. How the Simulator Works (Sprint Logic)

Each sprint follows this sequence:

1. **Select sprint tasks** from the backlog based on capacity and priority.
2. **Compute sprint coordination need** from the task type profile(s) in the sprint.
3. **Allocate tasks** to team members (with AI or without AI).
4. **Activate AI dashboard / shared cognition assistant** (if AI scenario).
5. **Compute CI subconstructs** and aggregate CI score.
6. **Compute decision quality** from reasoning, attention, coordination need, dashboard, social sensitivity, and trust calibration.
7. **Simulate task completion** using probability formulas (skill fit, overload, CI, decision quality, task difficulty).
8. **Simulate defects** for completed tasks (error tendency, task difficulty, task-type defect risk, AI quality bonus).
9. **Update backlog**, sprint metrics, and **learned trust**.
10. **Update CI dimensions** (memory, attention, reasoning) slightly based on sprint outcomes.

This loop repeats for the configured number of sprints.

---

## 6. Complete Parameter Reference (For Your Presentation)

### 6.1 User-controlled inputs (sidebar parameters)

These are the parameters you set before running the simulation.

| Parameter | UI control | Default | What it does | Presentation tip |
|---|---|---|---|---|
| **Team size** | Slider (3–12) | 6 | Number of developers in the simulated team. Affects capacity, workload spread, and specialization diversity. | Show how larger teams increase capacity but may reduce participation balance. |
| **Number of sprints** | Slider (1–20) | 8 | How many agile sprints to simulate. Allows CI and trust to evolve over time. | Use 8 sprints to show learning effects; use 1–2 for quick demos. |
| **Number of tasks** | Slider (10–200) | 60 | Size of the initial backlog. More tasks = longer project horizon. | Explain backlog pressure and remaining work charts. |
| **Task type** | Dropdown | Feature | Defines the **kind of work** in the backlog: Feature, Bug fix, Refactor, or Spike/Research. Each type has different coordination need, defect risk, uncertainty, and skill demand. | **Key demo:** switch Feature → Spike and compare effectiveness and defects. |
| **AI support level** | Slider (0–100%) | 70% | Intensity of AI involvement in allocation and shared cognition. Higher = stronger AI influence. | Show that AI only helps when other conditions (reliability, trust) are reasonable. |
| **Trust in AI** | Slider (0–100%) | 65% | Baseline willingness of team members to follow AI recommendations. | Compare low trust (under-use) vs high trust with low reliability (misuse). |
| **AI reliability** | Slider (0–100%) | 78% | **Actual** correctness of AI recommendations. Low reliability = wrong task assignments sometimes. | **Best demo parameter:** drop to 40% and show defects / lower benefit. |
| **Effort-related process** | Slider (0–100%) | 65% | Riedl/Hackman process measure for sustaining effort, distributing workload, and tolerating overload. | Raise/lower it to show how process quality affects capacity and completion. |
| **Knowledge / skills process** | Slider (0–100%) | 65% | Riedl/Hackman process measure for matching expertise to task contributions. This is distinct from individual skill. | Use it to explain “who knows what” in agile teams. |
| **Strategy updating process** | Slider (0–100%) | 65% | Riedl/Hackman process measure for selecting, monitoring, and adapting the work approach. | Show how process quality can improve results even with the same team. |
| **Female proportion** | Slider (0–100%) | 50% | Proxy pathway through social perceptiveness when social perceptiveness is not directly measured. | Explain carefully as a proxy, not a biological causal claim. |
| **Initial team engagement** | Slider (0–100%) | 65% | Initial team-level motivation/commitment level. It then evolves from sprint outcomes, decision quality, trust calibration, and consequentiality. | Show engagement as a team emergent state, not individual engagement. |
| **Consequentiality / shared purpose** | Slider (0–100%) | 65% | Hackman/Wageman-style driver: the work feels consequential and gives the team shared purpose. | Show how stronger purpose improves shared attention, engagement, viability, and sustainability. |
| **Task complexity** | Slider (0–100%) | 58% | Baseline difficulty/uncertainty of generated tasks. | Use to simulate an easy vs hard backlog. |
| **Dashboard quality** | Slider (0–100%) | 70% | Quality of the AI-supported shared dashboard / coordination view. | Explain shared cognition: visibility, coordination, decision support. |
| **Collective memory** | Slider (0–100%) | 62% | Team’s ability to retain and reuse shared knowledge across sprints. | Link to transactive memory literature (Wegner, Lewis). |
| **Collective focus of attention** | Slider (0–100%) | 60% | Team’s ability to focus on the right issues together. | Link to shared mental models and coordination. |
| **Collective reasoning** | Slider (0–100%) | 64% | Team’s ability to interpret information and decide together. | Link to decision quality output metric. |
| **Random seed** | Number input | 42 | Makes a single run reproducible. Same seed = same random draws. | Explain difference between one seed and Monte Carlo many seeds. |

---

### 6.2 Task type profiles (selected via **Task type**)

When you choose a task type, the simulator applies this profile to the whole backlog:

| Task type | Coordination need | Defect risk | Uncertainty | Skill demand | Completion bonus | Interpretation |
|---|---:|---:|---:|---:|---:|---|
| **Feature** | 0.75 | 0.55 | +0.10 | 0.65 | +0.02 | New functionality; high coordination, moderate defect risk |
| **Bug fix** | 0.50 | 0.35 | +0.05 | 0.55 | +0.04 | Corrective work; somewhat easier to complete, lower defect risk |
| **Refactor** | 0.60 | 0.45 | +0.08 | 0.70 | +0.01 | Internal quality work; higher skill demand |
| **Spike / Research** | 0.40 | 0.25 | +0.20 | 0.60 | 0.00 | Exploration; low coordination but high uncertainty, lower completion bonus |

**Why this replaced “communication quality”:**  
In agile work, coordination demand depends strongly on **what kind of work** the team is doing. A feature-heavy sprint requires different collective attention and decision patterns than a spike-heavy sprint.

---

### 6.2b Team process, social perceptiveness, and diversity variables

| Construct | Implementation | Research basis | How it is used |
|---|---|---|---|
| **Effort-related process** | Sidebar slider `effort_management` | Riedl et al. (2021), Hackman/Wageman process measures | Feeds shared attention, capacity, overload tolerance, and sustainability |
| **Knowledge / skills process** | Sidebar slider `skills_knowledge_coordination` | Riedl et al. (2021), Wegner (1987), Lewis (2003) | Feeds transactive memory, shared reasoning, and defect reduction |
| **Strategy updating process** | Sidebar slider `task_strategy` | Riedl et al. (2021), Hackman/Wageman process measures | Feeds shared reasoning, allocation quality, decision quality, and completion |
| **Riedl predictor items** | Process sliders + team attributes | Riedl et al. (2021), especially Fig. 2-D | Identifies effort process, knowledge/skills process, strategy process, individual skill, diversity, and social perceptiveness |
| **Scrum team effectiveness context** | Conceptual mapping, not extra sliders | Verwijs & Russo (2023), Strode et al. (2022) | Grounds agile performance in responsiveness, shared mental models, communication, trust, and teamwork effectiveness |
| **Hackman effectiveness criteria** | New summary metrics | Hackman (1987), Wageman et al. (2005) | Team effectiveness includes task output, team viability, and member sustainability |
| **Collective memory, attention, reasoning systems** | CI baseline sliders and computed components | Kommol, Riedl & Woolley (2025), Woolley & Mayo (2025) | Clarifies that CI is structured around memory, attention, and reasoning |
| **Social perceptiveness / social cognition** | Internal `social_sensitivity` per member | Woolley et al. (2010), Engel et al. (2014) | Feeds CI and decision quality |
| **Female proportion** | Sidebar slider `female_proportion` | Woolley et al. (2010), Riedl et al. (2021) | Proxy pathway through social sensitivity when social perceptiveness is not directly measured |
| **Skill diversity** | Computed from team skill spread | Hong & Page (2004) | Adds functional diversity to CI; distinct from individual `skill_level` |
| **Age diversity** | Computed from generated member ages | Supervisor feedback / diversity interpretation | Negative CI predictor |
| **Team engagement** | Initial slider + sprint-by-sprint update | Kozlowski & Ilgen (2006), Riedl et al. (2021) | Team-level engagement improves completion and contributes to CI |
| **Consequentiality / shared purpose** | Sidebar slider `consequentiality` | Hackman (2002), Wageman et al. (2005), supervisor feedback | Upstream driver of team engagement, shared attention, viability, and sustainability |
| **Collective focus of attention** | Sidebar slider `collective_attention` with clearer label | Shared mental model literature | Feeds decision quality and CI |

**NLP / vocal synchrony note:**  
Vocal synchrony is a possible measurement method for social coordination, especially in face-to-face or audio-recorded teams. This simulator does not process audio or text conversations, so it models the underlying construct as `social_sensitivity` instead of implementing NLP.

---

### 6.3 Internal team member variables (generated automatically)

Each team member is created with random variation:

| Variable | Meaning | Used for |
|---|---|---|
| `skill_level` | Technical capability (0–1) | Task fit, completion probability, error reduction |
| `age` | Generated member age | Age diversity calculation |
| `gender` | F/M label derived from the female proportion slider | Social sensitivity baseline and team diversity reporting |
| `availability` | How much capacity the member has this period | Workload capacity, allocation |
| `communication_level` | Individual communication/coordination skill | Completion probability, participation balance |
| `social_sensitivity` | Ability to read and respond to others (CI driver) | CI score, decision quality |
| `trust_in_ai` | Willingness to accept AI advice | AI allocation uptake, AI bonus |
| `perceived_ai_reliability` | What the member *believes* about AI accuracy | Trust calibration |
| `work_speed` | Execution speed | Capacity and completion |
| `error_tendency` | Likelihood of introducing defects | Defect probability |

These are **not** set manually in the UI; they emerge from team generation and evolve (trust) during the simulation.

---

### 6.4 Internal task variables (generated per backlog item)

| Variable | Meaning |
|---|---|
| `task_id` | Unique identifier |
| `task_type` | feature / bug / refactor / spike |
| `difficulty` | How hard the task is (0–1) |
| `effort_points` | Story points (1–13) |
| `priority` | Backlog priority (1–5) |
| `uncertainty` | Requirement/implementation uncertainty |
| `required_skill_level` | Skill needed for good fit |

---

### 6.5 Output metrics (what you present as results)

#### Sprint-level outputs (charts and tables)

| Metric | Meaning | Higher is better? |
|---|---|---|
| **Sprint velocity** | Completed story points in the sprint | Yes |
| **Task completion rate (%)** | Share of sprint tasks finished | Yes |
| **Defect rate (%)** | Defects per completed tasks | No |
| **Decision quality (%)** | Quality of team decisions this sprint | Yes |
| **Collective Intelligence score** | Aggregate CI from subconstructs | Yes |
| **Transactive memory** | CI subcomponent: shared retention + specialization | Yes |
| **Shared attention** | CI subcomponent: collective focus of attention plus effort and participation | Yes |
| **Shared reasoning** | CI subcomponent: collective reasoning plus strategy and knowledge coordination | Yes |
| **Social sensitivity** | CI subcomponent: interpersonal awareness | Yes |
| **Participation balance** | CI subcomponent: even contribution across members | Yes |
| **Team engagement** | Emergent motivational state updated from sprint outcomes | Yes |
| **Skill diversity** | Functional diversity proxy based on skill spread | Context-dependent |
| **Age diversity** | Normalized spread in generated member ages; negative CI predictor | No |
| **Effort-related process** | Process measure input reflected in results | Yes |
| **Knowledge / skills process** | Process measure input reflected in results | Yes |
| **Strategy updating process** | Process measure input reflected in results | Yes |
| **Consequentiality / shared purpose** | Team purpose driver reflected in engagement, viability, and sustainability | Yes |
| **Trust calibration (%)** | Alignment between perceived and actual AI reliability | Yes |
| **Team viability (%)** | Future capacity to keep working well together; based on CI, engagement, trust calibration, and decision quality | Yes |
| **Member sustainability (%)** | Well-being/sustainability proxy based on engagement, effort management, and low overload | Yes |
| **Overload pressure (%)** | Workload strain relative to expected member capacity | No |
| **Team effectiveness score** | Hackman-informed composite of task output, team viability, and member sustainability | Yes |
| **AI benefit score** | Value added by AI this sprint (0 in non-AI scenario) | Yes |
| **Backlog remaining** | Tasks still not done | No |

#### Team effectiveness formula (for thesis explanation)

Team effectiveness is now based on Hackman's broader view that effective teams must produce good work, remain viable for future work, and avoid damaging member sustainability. The simulator computes:

- **Task output** = velocity, completion, and quality (low defect rate)
- **Team viability** = collective intelligence, team engagement, consequentiality/shared purpose, trust calibration, and decision quality
- **Member sustainability** = team engagement, consequentiality/shared purpose, effort-related process, and low overload pressure

The final team effectiveness score uses simulation weights:

- 55% task output
- 25% team viability
- 20% member sustainability

These are transparent model assumptions for simulation and sensitivity analysis, not empirical coefficients estimated from the cited papers.

#### Collective Intelligence formula

CI is computed from eight positively weighted subconstructs plus an age-diversity penalty:

- 18% transactive memory
- 16% shared attention
- 16% shared reasoning
- 16% social sensitivity
- 10% participation balance
- 10% transactive coordination
- 8% team engagement
- 6% skill diversity
- 4% negative adjustment for age diversity

The CI subconstructs are now organized around Kommol, Riedl & Woolley's memory-attention-reasoning structure:

- **Collective/shared memory** is the baseline retained knowledge across sprints.
- **Transactive memory** operationalizes that memory as who knows what, individual skill, skill diversity, and knowledge/skills process.
- **Shared attention** combines collective focus, effort-related process, consequentiality/shared purpose, participation balance, and coordination need.
- **Shared reasoning** combines collective reasoning, strategy updating process, social sensitivity, and knowledge/skills process.
- **Female proportion** is only a proxy pathway through social perceptiveness when social perceptiveness is not measured directly.

As above, these percentages are simulation weights for interpretability, not direct empirical percentages from the papers.

---

### 6.6 Experiment parameters (Monte Carlo & sensitivity tabs)

| Control | Tab | Purpose |
|---|---|---|
| **Repetitions per scenario** | Monte Carlo | How many random seeds to run (e.g., 100) |
| **Parameter to vary** | Sensitivity | Which input to sweep (trust, AI reliability, complexity, etc.) |
| **Min / max / steps** | Sensitivity | Range for the sweep |
| **Repetitions per value** | Sensitivity | Runs averaged at each parameter value |
| **Use AI scenario toggle** | Sensitivity | Whether sensitivity applies to AI or baseline scenario |

---

## 7. AI Support Modules in the Prototype

### 7.1 AI Task Allocation Assistant

**Purpose:** Assign each sprint task to the most suitable team member.

**Considers:**

- Skill fit (member skill vs required skill)
- Availability
- Workload balance
- Trust in AI (uptake of AI advice)
- AI reliability (AI can make mistakes and pick the second-best member)

**Research basis:** Software effort estimation, agile coordination, human–AI trust.

### 7.2 AI Dashboard / Shared Cognition Assistant

**Purpose:** Improve team coordination and decision support through a shared view.

**Produces:**

- Visibility gain
- Coordination gain
- Decision gain

**Attenuated by:** low AI reliability, poor dashboard quality, miscalibrated trust.

**Research basis:** Shared mental models, agile coordination mechanisms, human–AI interaction guidelines.

### 7.3 Trust calibration and learning

Each sprint updates:

- Member `trust_in_ai`
- Member `perceived_ai_reliability`

Trust calibration score = `1 − |perceived − actual|`  
High calibration means the team’s trust matches AI capability.

---

## 8. How to Use the Simulator in Your Presentation

### 8.1 Setup (30 seconds)

```bash
streamlit run app.py
```

Open browser → sidebar parameters → three tabs: **Single Run**, **Monte Carlo Experiments**, **Sensitivity Analysis**.

### 8.2 Recommended live demo script (8–10 minutes)

#### Demo 1 — Baseline comparison (2 min)

1. Keep defaults (Feature tasks, AI reliability 78%, trust 65%).
2. Open **Single Run** tab.
3. Point to summary metrics: velocity, CI, team effectiveness, AI benefit.
4. Say: *“Same team, same backlog — the only difference is AI support in allocation and shared cognition.”*

#### Demo 2 — Task type matters (2 min)

1. Change **Task type** to **Spike / Research**.
2. Show lower effectiveness and different defect/uncertainty behavior.
3. Say: *“CI and coordination depend on what kind of work the sprint contains — not just team skill.”*

#### Demo 2b — Team process criteria matter (1 min)

1. Open the **Team & Process** sidebar section.
2. Raise **Effort-related process**, **Knowledge / skills process**, **Strategy updating process**, and optionally **Consequentiality / shared purpose** from 65% to 85%.
3. Show the changes in completion, decision quality, and CI subcomponents.
4. Say: *“This demonstrates that the model does not treat AI as the only intervention; agile process quality also changes outcomes.”*

#### Demo 3 — AI is not magic (2 min)

1. Set **AI reliability** to 40%.
2. Keep trust high (65%+).
3. Show increased defects, reduced AI benefit, trust calibration effects.
4. Say: *“High trust with low reliability creates misuse — a core human–AI teaming problem.”*

#### Demo 4 — Scientific credibility (2 min)

1. Open **Monte Carlo Experiments**.
2. Run 100 replications.
3. Show mean, std dev, 95% CI for with-AI vs without-AI.
4. Say: *“We don’t rely on one lucky random seed — we compare distributions.”*

#### Demo 5 — Sensitivity (1–2 min)

1. Open **Sensitivity Analysis**.
2. Vary **AI reliability** from 20% to 90%.
3. Show team effectiveness and trust calibration curves.
4. Say: *“This tells us which levers matter most for policy and tool design.”*

---

## 9. Literature Review — All 30 Papers

Below is the full paper set reviewed for this project. For each paper: **citation**, **main finding**, **relevance to the simulator**, and **implemented / partial / future**.

### Additional references added from `new-ref.bib`

| Key | Citation focus | How it changes the simulator |
|---|---|---|
| `Verwijs2023` | Theory of Scrum team effectiveness: responsiveness, stakeholder concern, continuous improvement, autonomy, management support | Grounds agile/Scrum performance interpretation beyond generic velocity |
| `strode2022teamwork` | Agile Teamwork Effectiveness Model: shared leadership, team orientation, redundancy, adaptability, peer feedback, shared mental models, communication, trust | Connects CI systems to agile teamwork mechanisms |
| `Riedl2021` | CI predicts performance; collaboration process is the strongest predictor, especially skill congruence, strategy, and effort | Makes effort management, skills/knowledge coordination, and task strategy explicit CI predictors |
| `woolley2025teams` | Teams as interdependent systems; team capability and CI as dynamic constructs under complexity | Supports the dynamic, feedback-based framing of agile teams |
| `kommol2025structure` | CI structure emerges from collective memory, attention, and reasoning | Reorganizes CI explanation around the three CI systems |
| `Hackman1987` | Team effectiveness includes task output, member well-being/growth, and future team viability | Adds task output, team viability, and member sustainability framing |
| `Wageman2005` | Team Diagnostic Survey and conditions supporting team effectiveness | Supports broad team effectiveness and model diagnostics |

---

### Paper 1 — Woolley et al. (2010)

**Citation:** Woolley, A. W., Chabris, C. F., Pentland, A., Hashmi, N., & Malone, T. W. (2010). Evidence for a collective intelligence factor in the performance of human groups. *Science*, 330(6004), 686–688. https://doi.org/10.1126/science.1193147

**Main finding:** Groups exhibit a general **collective intelligence factor (c)** that predicts performance across tasks. c is not strongly explained by average individual IQ alone; **social sensitivity** and **equal conversational turn-taking** matter.

**Relevance:** Justifies treating CI as a team-level construct in the simulator, not just sum of individual skills.

**In simulator:** Implemented — CI aggregate score, social sensitivity, participation balance, and female proportion as a team diversity input.

---

### Paper 2 — Engel et al. (2014)

**Citation:** Engel, D., Woolley, A. W., Jing, L. X., Chabris, C. F., & Malone, T. W. (2014). Reading the Mind in the Eyes or Reading between the Lines? Theory of Mind Predicts Collective Intelligence Equally Well Online and Face-To-Face. *PLOS ONE*, 9(12), e115212. https://doi.org/10.1371/journal.pone.0115212

**Main finding:** Theory of mind predicts CI in both face-to-face and online teams.

**Relevance:** Supports social sensitivity as a CI driver even in distributed agile contexts.

**In simulator:** Partial — `social_sensitivity` on team members feeds CI and decision quality.

---

### Paper 3 — Malone, Laubacher & Dellarocas (2010)

**Citation:** Malone, T. W., Laubacher, R., & Dellarocas, C. (2010). The Collective Intelligence Genome. *MIT Sloan Management Review*, 51(3). https://sloanreview.mit.edu/article/the-collective-intelligence-genome/

**Main finding:** Collective intelligence systems can be **designed** by specifying what is done, who does it, why, and how.

**Relevance:** Frames AI assistants and sprint processes as designable coordination mechanisms.

**In simulator:** Partial — explicit AI modules (allocation, dashboard) as coordination design choices.

---

### Paper 4 — Hong & Page (2004)

**Citation:** Hong, L., & Page, S. E. (2004). Groups of diverse problem solvers can outperform groups of high-ability problem solvers. *PNAS*, 101(46), 16385–16389. https://doi.org/10.1073/pnas.0403723101

**Main finding:** Diverse problem-solving perspectives can beat teams of uniformly high-ability experts.

**Relevance:** Supports skill specialization and diversity in transactive memory scoring.

**In simulator:** Implemented — skill diversity is computed from team skill spread and contributes to CI.

---

### Paper 5 — Lorenz et al. (2011)

**Citation:** Lorenz, J., Rauhut, H., Schweitzer, F., & Helbing, D. (2011). How social influence can undermine the wisdom of crowd effect. *PNAS*, 108(22), 9020–9025. https://doi.org/10.1073/pnas.1008636108

**Main finding:** Social influence reduces opinion diversity and can **harm** collective accuracy despite increasing confidence.

**Relevance:** Warns against modeling AI/dashboard as always beneficial — groupthink risk.

**In simulator:** Future — conformity / over-reliance when dashboard dominates decisions.

---

### Paper 6 — Bahrami et al. (2010)

**Citation:** Bahrami, B., Olsen, K., Latham, P. E., Roepstorff, A., Rees, G., & Frith, C. D. (2010). Optimally interacting minds. *Science*, 329(5995), 1081–1085. https://doi.org/10.1126/science.1185718

**Main finding:** Two people make better joint decisions when they share confidence and have comparable competence.

**Relevance:** Informs decision quality as a team-level outcome, not purely individual.

**In simulator:** Partial — decision quality combines team reasoning, attention, social sensitivity.

---

### Paper 7 — Wegner (1987)

**Citation:** Wegner, D. M. (1987). Transactive memory: A contemporary analysis of the group mind. In B. Mullen & G. R. Goethals (Eds.), *Theories of Group Behavior* (pp. 185–208). Springer. https://doi.org/10.1007/978-1-4612-4634-3_9

**Main finding:** Groups develop distributed memory systems: who knows what, plus coordination to access knowledge.

**Relevance:** Core theoretical basis for `collective_memory` and transactive memory metric.

**In simulator:** Partial — transactive memory subconstruct; future: full who-knows-what matrix.

---

### Paper 8 — Lewis (2003)

**Citation:** Lewis, K. (2003). Measuring transactive memory systems in the field: Scale development and validation. *Journal of Applied Psychology*, 88(4), 587–594. https://doi.org/10.1037/0021-9010.88.4.587

**Main finding:** TMS can be measured via specialization, credibility, and coordination.

**Relevance:** Validates splitting memory into measurable subconstructs.

**In simulator:** Partial — transactive memory + transactive coordination components.

---

### Paper 9 — Mathieu et al. (2000)

**Citation:** Mathieu, J. E., Heffner, T. S., Goodwin, G. F., Salas, E., & Cannon-Bowers, J. A. (2000). The influence of shared mental models on team process and performance. *Journal of Applied Psychology*, 85(2), 273–283. https://doi.org/10.1037/0021-9010.85.2.273

**Main finding:** Shared team and task mental models improve team process, which improves performance.

**Relevance:** Supports shared attention/reasoning and dashboard/shared cognition assistant.

**In simulator:** Partial — shared attention & reasoning dimensions; AI dashboard as shared cognition aid.

---

### Paper 10 — DeChurch & Mesmer-Magnus (2010)

**Citation:** DeChurch, L. A., & Mesmer-Magnus, J. R. (2010). The cognitive underpinnings of effective teamwork: A meta-analysis. *Journal of Applied Psychology*, 95(1), 32–53. https://doi.org/10.1037/a0017328

**Main finding:** Team cognition strongly predicts team processes, motivation, and performance.

**Relevance:** Justifies reporting CI separately from delivery metrics.

**In simulator:** Implemented — separate CI subconstructs and outcome metrics.

---

### Paper 11 — Marks, Mathieu & Zaccaro (2001)

**Citation:** Marks, M. A., Mathieu, J. E., & Zaccaro, S. J. (2001). A temporally based framework and taxonomy of team processes. *Academy of Management Review*, 26(3), 356–376. https://doi.org/10.5465/amr.2001.4845785

**Main finding:** Team processes unfold over phases: transition, action, interpersonal.

**Relevance:** Supports future sprint-phase modeling (planning, execution, review, retro).

**In simulator:** Partial — effort management, skills/knowledge coordination, and task strategy are modeled as process criteria; full sprint phases remain future work.

---

### Paper 12 — Salas, Sims & Burke (2005)

**Citation:** Salas, E., Sims, D. E., & Burke, C. S. (2005). Is there a “Big Five” in teamwork? *Small Group Research*, 36(5), 555–599. https://doi.org/10.1177/1046496405277134

**Main finding:** Teamwork includes leadership, monitoring, backup behavior, adaptability, and orientation — supported by shared mental models and trust.

**Relevance:** Informs future team mechanism variables (backup behavior, adaptability).

**In simulator:** Future — not yet explicit; partially reflected in coordination and CI.

---

### Paper 13 — Kozlowski & Ilgen (2006)

**Citation:** Kozlowski, S. W. J., & Ilgen, D. R. (2006). Enhancing the effectiveness of work groups and teams. *Psychological Science in the Public Interest*, 7(3), 77–124. https://doi.org/10.1111/j.1529-1006.2006.00030.x

**Main finding:** Team effectiveness emerges from inputs → processes → emergent states → outcomes.

**Relevance:** Architectural blueprint for the simulator’s structure.

**In simulator:** Partial — inputs (config), emergent CI/trust/team engagement, processes (allocation), outcomes (velocity/defects).

---

### Paper 14 — Moe, Dingsoyr & Dyba (2010)

**Citation:** Moe, N. B., Dingsøyr, T., & Dybå, T. (2010). A teamwork model for understanding an agile team: A case study of a Scrum project. *Information and Software Technology*, 52(5), 480–491. https://doi.org/10.1016/j.infsof.2009.11.004

**Main finding:** Agile team effectiveness depends on trust, shared mental models, coordination, and team orientation; specialization can hinder coordination.

**Relevance:** Direct agile grounding for the simulator domain.

**In simulator:** Partial — trust, CI, coordination via task type; future: Scrum roles.

---

### Paper 15 — Strode et al. (2012)

**Citation:** Strode, D. E., Huff, S. L., Hope, B., & Link, S. (2012). Coordination in co-located agile software development projects. *Journal of Systems and Software*, 85(6), 1222–1238. https://doi.org/10.1016/j.jss.2012.02.017

**Main finding:** Agile coordination uses synchronization, structure, and boundary spanning.

**Relevance:** Supports dashboard, sprint planning, and task-type coordination need.

**In simulator:** Partial — coordination need by task type; dashboard quality parameter.

---

### Paper 16 — Hoda, Noble & Marshall (2013)

**Citation:** Hoda, R., Noble, J., & Marshall, S. (2013). Self-organizing roles on agile software development teams. *IEEE Transactions on Software Engineering*, 39(3), 422–444. https://doi.org/10.1109/TSE.2012.30

**Main finding:** Agile teams rely on informal roles (mentor, coordinator, translator, champion, etc.).

**Relevance:** Future extension for role-based and AI-agent specialization.

**In simulator:** Future — no formal/informal roles yet.

---

### Paper 17 — Lindsjørn et al. (2016)

**Citation:** Lindsjørn, Y., Sjøberg, D. I. K., Dingsøyr, T., Bergersen, G. R., & Dybå, T. (2016). Teamwork quality and project success in software development: A survey of agile development teams. *Journal of Systems and Software*, 122, 274–286. https://doi.org/10.1016/j.jss.2016.09.028

**Main finding:** Teamwork quality (communication, coordination, cohesion, mutual support) predicts success in agile teams.

**Relevance:** Validates multi-dimensional team quality rather than velocity alone.

**In simulator:** Partial — team effectiveness combines delivery, quality, CI, decision quality.

---

### Paper 18 — Moløkken-Østvold, Haugen & Benestad (2008)

**Citation:** Moløkken-Østvold, K., Haugen, N. C., & Benestad, H. C. (2008). Using planning poker for combining expert estimates in software projects. *Journal of Systems and Software*, 81(12), 2106–2117. https://doi.org/10.1016/j.jss.2008.03.058

**Main finding:** Planning poker improves estimate discussion and can reduce optimism bias.

**Relevance:** Supports future sprint planning phase and uncertainty reduction.

**In simulator:** Future — no explicit planning poker / estimation round.

---

### Paper 19 — Jørgensen (2007)

**Citation:** Jørgensen, M. (2007). Forecasting of software development work effort: Evidence on expert judgement and formal models. *International Journal of Forecasting*, 23(3), 449–462. https://doi.org/10.1016/j.ijforecast.2007.05.008

**Main finding:** Expert judgment and formal models each work best under different conditions; combining them can help.

**Relevance:** AI allocation should not always override human judgment.

**In simulator:** Partial — AI assists but does not fully replace human allocation; reliability/trust modulate uptake.

---

### Paper 20 — Lee & See (2004)

**Citation:** Lee, J. D., & See, K. A. (2004). Trust in automation: Designing for appropriate reliance. *Human Factors*, 46(1), 50–80. https://doi.org/10.1518/hfes.46.1.50_30392

**Main finding:** Trust drives automation use; **misuse** (over-trust) and **disuse** (under-trust) both harm performance.

**Relevance:** Core basis for trust_in_ai, ai_reliability, and trust calibration.

**In simulator:** Implemented — trust calibration, AI reliability, learned trust.

---

### Paper 21 — Hoff & Bashir (2015)

**Citation:** Hoff, K. A., & Bashir, M. (2015). Trust in automation: Integrating empirical evidence on factors that influence trust. *Human Factors*, 57(3), 407–434. https://doi.org/10.1177/0018720814547570

**Main finding:** Trust has dispositional, situational, and learned components.

**Relevance:** Supports baseline trust + sprint learning updates.

**In simulator:** Partial — baseline trust + learned updates; future: dispositional differences.

---

### Paper 22 — Dzindolet et al. (2003)

**Citation:** Dzindolet, M. T., Peterson, S. A., Pomranky, R. A., Pierce, L. G., & Beck, H. P. (2003). The role of trust in automation reliance. *International Journal of Human-Computer Studies*, 58(6), 697–718. https://doi.org/10.1016/S1071-5819(03)00038-7

**Main finding:** Appropriate reliance requires understanding of both human and automation reliability.

**Relevance:** Supports separate perceived vs actual AI reliability.

**In simulator:** Implemented — `perceived_ai_reliability` vs `ai_reliability`.

---

### Paper 23 — Amershi et al. (2019)

**Citation:** Amershi, S., et al. (2019). Guidelines for Human-AI Interaction. *CHI 2019*. https://doi.org/10.1145/3290605.3300233

**Main finding:** Human-AI systems should set expectations, show uncertainty, enable correction, and support recovery from errors.

**Relevance:** Informs dashboard quality, explainability, and future review checkpoints.

**In simulator:** Partial — dashboard quality; future: explicit explainability and review gates.

---

### Paper 24 — Buçinca, Malaya & Gajos (2021)

**Citation:** Buçinca, Z., Malaya, M. B., & Gajos, K. Z. (2021). To Trust or to Think: Cognitive forcing functions can reduce overreliance on AI in AI-assisted decision-making. *Proceedings of the ACM on Human-Computer Interaction*, 5(CSCW1). https://doi.org/10.1145/3449287

**Main finding:** People over-rely on AI; cognitive forcing functions reduce overreliance.

**Relevance:** Explains why high trust + low reliability increases defects in the simulator.

**In simulator:** Partial — misfit penalty and trust calibration; future: explicit human review step.

---

### Paper 25 — Grimm et al. (2006)

**Citation:** Grimm, V., et al. (2006). A standard protocol for describing individual-based and agent-based models. *Ecological Modelling*, 198(1–2), 115–126. https://doi.org/10.1016/j.ecolmodel.2006.04.023

**Main finding:** ODD protocol standardizes model description: purpose, entities, processes, initialization.

**Relevance:** Thesis documentation standard for reproducibility.

**In simulator:** Future — ODD document not yet written; architecture is ODD-compatible.

---

### Paper 26 — Sargent (2013)

**Citation:** Sargent, R. G. (2013). Verification and validation of simulation models. *Journal of Simulation*, 7(1), 12–24. https://doi.org/10.1057/jos.2012.20

**Main finding:** Validation must match model purpose; stochastic models require distributional comparison.

**Relevance:** Justifies Monte Carlo experiments and confidence intervals.

**In simulator:** Implemented — Monte Carlo tab with mean, std dev, 95% CI.

---

### Paper 27 — Klügl (2008)

**Citation:** Klügl, F. (2008). A validation methodology for agent-based simulations. *SAC 2008*, 39–43. https://doi.org/10.1145/1363686.1363696

**Main finding:** Agent-based models need face validation, sensitivity analysis, calibration, and statistical validation.

**Relevance:** Direct basis for sensitivity analysis tab.

**In simulator:** Implemented — sensitivity analysis for key parameters.

---

### Paper 28 — Park et al. (2023)

**Citation:** Park, J. S., O'Brien, J. C., Cai, C. J., Morris, M. R., Liang, P., & Bernstein, M. S. (2023). Generative Agents: Interactive Simulacra of Human Behavior. *UIST 2023*. https://doi.org/10.1145/3586183.3606763

**Main finding:** LLM agents with memory, reflection, and planning produce believable social behavior.

**Relevance:** Future direction for richer agent-based agile team simulation.

**In simulator:** Future — current model is formula-based, not LLM-agent-based.

---

### Paper 29 — Qian et al. (2023) — ChatDev

**Citation:** Qian, C., et al. (2023). ChatDev: Communicative Agents for Software Development. arXiv:2307.07924. https://arxiv.org/abs/2307.07924

**Main finding:** Multi-agent LLM conversations can coordinate software development phases.

**Relevance:** Supports role-specific AI assistants (planner, reviewer, tester).

**In simulator:** Future — two generic AI modules today (allocator + dashboard).

---

### Paper 30 — Hong et al. (2024) — MetaGPT

**Citation:** Hong, S., et al. (2024). MetaGPT: Meta Programming for A Multi-Agent Collaborative Framework. *ICLR 2024*. https://openreview.net/forum?id=VtmBAGCN7o

**Main finding:** Structured SOPs and role specialization improve multi-agent software collaboration.

**Relevance:** Supports future AI agents producing structured artifacts (requirements, test plans).

**In simulator:** Future — AI outputs are scalar gains, not structured artifacts yet.

---

## 10. Mapping Papers → Simulator Features (Summary Table)

| Research theme | Papers | Implemented now | Planned future |
|---|---|---|---|
| Collective Intelligence | 1–4, 6–10 | CI score + memory, attention, reasoning, social perceptiveness, female proxy pathway, skill diversity, age diversity penalty | Turn-taking, groupthink |
| Transactive memory | 7–8 | Transactive memory/coordination | Knowledge matrix |
| Team process & teamwork | 11–13 | Sprint loop, effort-related process, knowledge/skills process, strategy updating process, consequentiality, team engagement | Sprint phases, Big Five |
| Agile software teams | 14–18 | Task types, CI, trust | Roles, planning poker |
| Effort & estimation | 18–19 | AI-assisted allocation | Estimation rounds |
| Human–AI trust | 20–24 | Trust, reliability, calibration | Review gates, explainability |
| Simulation validation | 25–27 | Monte Carlo, sensitivity | ODD doc, calibration to data |
| LLM multi-agent teams | 28–30 | Conceptual reference | LLM agents, ChatDev-style roles |

---

## 11. Suggested Presentation Structure (Slides)

| Slide | Content |
|---|---|
| 1 | Title: Agile AI Simulator — Collective Intelligence & Human–AI Teaming |
| 2 | Problem: AI in agile teams is promising but inconsistent |
| 3 | Research question: How do CI and AI support shape sprint outcomes? |
| 4 | Theoretical framework (4 layers) |
| 5 | Simulator architecture diagram |
| 6 | Demo screenshot: Single Run comparison |
| 7 | Parameter overview (sidebar inputs) |
| 8 | Task types and why they matter |
| 9 | CI subconstructs explained |
| 10 | Human–AI trust model (reliability vs trust vs calibration) |
| 11 | Live demo or Monte Carlo results |
| 12 | Sensitivity analysis example |
| 13 | Literature grounding (30 papers — show summary table) |
| 14 | Benefits: academic, practical, methodological |
| 15 | Limitations and future work |
| 16 | Conclusion and Q&A |

---

## 12. Key Messages for Q&A

**Q: Is this a real prediction tool?**  
A: No. It is a transparent research prototype for conceptual experimentation and thesis argumentation.

**Q: Why compare with vs without AI?**  
A: To isolate the effect of AI support mechanisms rather than confounding them with team skill or backlog properties.

**Q: Why task type instead of communication quality?**  
A: In agile work, coordination demand is strongly shaped by the kind of work (feature vs spike vs bug). Task type is a more domain-specific lever.

**Q: Why Monte Carlo?**  
A: Because the model is stochastic. One seed can mislead; distributions are academically defensible (Sargent, 2013; Klügl, 2008).

**Q: What's the biggest future improvement?**  
A: Sprint phases, task dependencies, role-based agents, and empirical calibration against real team data.

---

## 13. Limitations (Be Honest in the Presentation)

1. **Simplified formulas** — weights are interpretable but not empirically calibrated to industry data.
2. **No real LLM agents** — AI is modeled as support functions, not conversational agents.
3. **No Scrum roles yet** — Product Owner, Scrum Master, Developer not distinguished.
4. **No task dependencies** — real agile work has blockers and rework chains.
5. **Homogeneous task type per run** — real backlogs mix features, bugs, and spikes.
6. **Single project simulation** — no multi-team or portfolio effects.

---

## 14. Future Research Directions

1. Mixed backlogs with proportional task-type mixes  
2. Sprint phases: planning → execution → review → retrospective  
3. Task dependency graph and blocker simulation  
4. Role-specific human and AI agents (MetaGPT / ChatDev inspired)  
5. ODD protocol documentation for full reproducibility  
6. Calibration using empirical agile team datasets  
7. Groupthink / over-reliance when AI dashboard dominates (Lorenz et al.)  

---

## 15. Conclusion

The Agile AI Simulator provides a **research-grade conceptual laboratory** for exploring how Collective Intelligence and AI support interact in agile software teams. It is grounded in **30 peer-reviewed sources** spanning CI theory, agile teamwork, human–AI trust, and simulation methodology.

**Use it to:**

- Compare AI-supported vs baseline agile teams
- Explain CI as a multi-dimensional team property
- Demonstrate why AI reliability and trust calibration matter
- Show how task type changes coordination and outcomes
- Support thesis claims with replicable experiments

**Command to run:**

```bash
streamlit run app.py
```

---

## 16. Full Reference List (Alphabetical)

1. Amershi, S., et al. (2019). Guidelines for Human-AI Interaction. CHI 2019. https://doi.org/10.1145/3290605.3300233  
2. Bahrami, B., et al. (2010). Optimally interacting minds. Science. https://doi.org/10.1126/science.1185718  
3. Buçinca, Z., Malaya, M. B., & Gajos, K. Z. (2021). To Trust or to Think. PACM HCI. https://doi.org/10.1145/3449287  
4. DeChurch, L. A., & Mesmer-Magnus, J. R. (2010). The cognitive underpinnings of effective teamwork. JAP. https://doi.org/10.1037/a0017328  
5. Dzindolet, M. T., et al. (2003). The role of trust in automation reliance. IJHCS. https://doi.org/10.1016/S1071-5819(03)00038-7  
6. Engel, D., et al. (2014). Theory of Mind Predicts Collective Intelligence. PLOS ONE. https://doi.org/10.1371/journal.pone.0115212  
7. Grimm, V., et al. (2006). ODD protocol. Ecological Modelling. https://doi.org/10.1016/j.ecolmodel.2006.04.023  
8. Hoda, R., Noble, J., & Marshall, S. (2013). Self-organizing roles on agile teams. IEEE TSE. https://doi.org/10.1109/TSE.2012.30  
9. Hoff, K. A., & Bashir, M. (2015). Trust in automation review. Human Factors. https://doi.org/10.1177/0018720814547570  
10. Hong, L., & Page, S. E. (2004). Diverse problem solvers. PNAS. https://doi.org/10.1073/pnas.0403723101  
11. Hong, S., et al. (2024). MetaGPT. ICLR 2024. https://openreview.net/forum?id=VtmBAGCN7o  
12. Jørgensen, M. (2007). Forecasting software development work effort. IJF. https://doi.org/10.1016/j.ijforecast.2007.05.008  
13. Klügl, F. (2008). Validation methodology for agent-based simulations. SAC. https://doi.org/10.1145/1363686.1363696  
14. Lee, J. D., & See, K. A. (2004). Trust in automation. Human Factors. https://doi.org/10.1518/hfes.46.1.50_30392  
15. Lewis, K. (2003). Measuring transactive memory systems. JAP. https://doi.org/10.1037/0021-9010.88.4.587  
16. Lindsjørn, Y., et al. (2016). Teamwork quality in agile teams. JSS. https://doi.org/10.1016/j.jss.2016.09.028  
17. Lorenz, J., et al. (2011). Social influence and wisdom of crowds. PNAS. https://doi.org/10.1073/pnas.1008636108  
18. Malone, T. W., Laubacher, R., & Dellarocas, C. (2010). The Collective Intelligence Genome. SMR.  
19. Marks, M. A., Mathieu, J. E., & Zaccaro, S. J. (2001). Taxonomy of team processes. AMR. https://doi.org/10.5465/amr.2001.4845785  
20. Mathieu, J. E., et al. (2000). Shared mental models and team performance. JAP. https://doi.org/10.1037/0021-9010.85.2.273  
21. Moe, N. B., Dingsøyr, T., & Dybå, T. (2010). Teamwork model for agile teams. IST. https://doi.org/10.1016/j.infsof.2009.11.004  
22. Moløkken-Østvold, K., et al. (2008). Planning poker. JSS. https://doi.org/10.1016/j.jss.2008.03.058  
23. Park, J. S., et al. (2023). Generative Agents. UIST. https://doi.org/10.1145/3586183.3606763  
24. Qian, C., et al. (2023). ChatDev. arXiv:2307.07924.  
25. Salas, E., Sims, D. E., & Burke, C. S. (2005). Big Five in teamwork. SGR. https://doi.org/10.1177/1046496405277134  
26. Sargent, R. G. (2013). Verification and validation of simulation models. JoS. https://doi.org/10.1057/jos.2012.20  
27. Strode, D. E., et al. (2012). Coordination in agile projects. JSS. https://doi.org/10.1016/j.jss.2012.02.017  
28. Kozlowski, S. W. J., & Ilgen, D. R. (2006). Enhancing team effectiveness. PSPI. https://doi.org/10.1111/j.1529-1006.2006.00030.x  
29. Wegner, D. M. (1987). Transactive memory. Springer chapter. https://doi.org/10.1007/978-1-4612-4634-3_9  
30. Woolley, A. W., et al. (2010). Collective intelligence factor. Science. https://doi.org/10.1126/science.1193147  

---

*End of report.*
