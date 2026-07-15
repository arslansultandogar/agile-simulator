# Demo Track Submission

**Title:** Collective Intelligence in Agile Teams: A Transparent Simulation Testbed for Studying Team Decisions Across Sprints

**Project:** Agile AI Simulator (`agile-ai-simulator`)
**Track:** Demos · **Topic affiliation:** Collective Intelligence (CI)
**Authors:** Arslan Sultan¹ (corresponding author), Juan Garbajosa²
*¹ [affiliation, email — to confirm] · ² [affiliation, email — to confirm]*
**Date:** July 2026

> **Scope & format.** This is the *demo* paper (main body under 2 pages): it describes the **system**, the **nature of interaction**, and the **expected audience engagement**. The conceptual argument — why collective intelligence is the right lens for agile teamwork — is developed in the companion poster ([`POSTER_SUBMISSION.md`](POSTER_SUBMISSION.md)). The video walkthrough and screenshots are provided as separate **supplemental materials**.

---

## Abstract

We demonstrate an interactive testbed that models agile software teams as a **collective-intelligence (CI) process** across multiple sprints. Collective intelligence — collective memory, shared attention, shared reasoning, social sensitivity, participation balance — is only weakly predicted by individual skill [Woolley et al. 2010; Kommol, Riedl & Woolley 2025], yet it drives how teams plan, allocate, and adapt. Our tool makes these subconstructs adjustable levers: a researcher moves them (and, secondarily, AI decision support and its trust calibration) and watches velocity, defect rate, decision quality, and Hackman-style team effectiveness respond, sprint by sprint. It supports single scenarios, Monte Carlo replication, and one-parameter sensitivity sweeps. Every weight and formula is externalized and inspectable, so the demo is an invitation to interrogate assumptions rather than trust a black box.

## 1. Why collective intelligence, briefly

Agile teamwork is a repeated collective decision process — planning, allocating against expertise, coordinating dependencies, learning from retrospectives. The *Agile Manifesto* already located performance in "individuals and interactions over processes and tools" [Beck et al. 2001], and CI research shows group performance emerges from shared cognitive and social processes, not the sum of individual ability [Woolley et al. 2010; Riedl et al. 2021]; empirical agile/Scrum models point to the same emergent factors [Verwijs & Russo 2023; Strode et al. 2022]. The poster develops this argument; the demo makes the process **manipulable and visible**.

## 2. The system

A modular Python application with a Streamlit front end, organized in four layers (Figure 1): a **presentation layer** (parameter controls, result views), an **orchestration layer** (single run, Monte Carlo, sensitivity), a **simulation engine** running the per-sprint loop, and an **externalized configuration layer** holding every weight in a versioned YAML file — nothing hard-coded out of sight.

![Figure 1: Four-layer architecture of the Agile AI Simulator — a Streamlit UI drives an orchestration layer that repeatedly calls the sprint engine, which draws on team, backlog, human–AI, and metrics modules, all parameterized by an externalized weights file.](figures/fig1_architecture.png)

*Figure 1. Tool architecture. `app.py` collects ~20 parameters and renders four result tabs; `experiments.py` runs the engine once, N times (Monte Carlo), or across a swept parameter; `simulation.py` executes the sprint loop, drawing on `team.py` (members, role modifiers), `tasks.py` (mixed backlog, task-type profiles), `ai_support.py` (allocation, shared cognition, trust update), and `metrics.py` (CI subconstructs, decision quality, Hackman effectiveness, trust calibration). All weights live in `config/weights.yaml`.*

**Each sprint** is a transparent loop, readable end-to-end in `simulation.py`: select tasks under capacity and priority → compute coordination need from task-type profiles (feature, bug, refactor, spike) → allocate with the AI assistant *or* a heuristic baseline → activate the shared-cognition dashboard (AI only) → aggregate CI and decision quality → simulate completion, defects, and rework → update learned trust and CI dimensions, feeding the next sprint. Scrum realism sits on top of this loop — roles (PO, SM, Developer, Tester), sprint-phase modifiers, dependencies/blockers, defect rework, and trust calibration — and effectiveness is scored three ways (output + viability + sustainability), since agile success is not velocity alone [Hackman 1987].

## 3. Nature of interaction with users

The interface is a control **sidebar** plus **four tabs**:

| Control / view | What the user does and sees |
|---|---|
| **Sidebar** | Pick a preset (e.g. *High-trust/high-reliability*, *Over-trust/low-reliability*) or move ~20 sliders — team & diversity, task mix & complexity, CI dimensions, process quality, and human–AI settings. A fixed seed makes any run reproducible. |
| **Single Run** | With-AI and without-AI on the *same* team/backlog; summary metric cards with with-vs-without deltas, then sprint-by-sprint charts; JSON export. |
| **Monte Carlo** | N replications with mean, std dev, and 95% CI — comparison by distribution, not one lucky seed. |
| **Sensitivity** | Sweep one parameter (e.g. AI reliability, trust) and read how effectiveness and trust calibration respond. |
| **Assumptions** | Every formula and externalized weight, shown in-app. |

*Screenshots of each tab are supplied as supplemental material (see [`figures/README.md`](figures/README.md)).*

## 4. Expected audience engagement

At the table, attendees drive the tool themselves. A guided 8–10 minute path: (1) **baseline** — same team/backlog, only AI differs; (2) **CI drives outcomes** — move collective memory/attention/reasoning and watch decision quality and defects shift *without touching the AI*; (3) **task type matters** — switch feature-heavy → spike-heavy; (4) **AI is not magic** — drop AI reliability while trust stays high and watch defects rise and calibration fall; (5) **credibility** — run 100 Monte Carlo replications; (6) **sensitivity** — sweep AI reliability and read the curves. Attendees then take the controls, run counterfactuals, and name the assumptions they would challenge — the transparent weights make that a concrete conversation.

## 5. Running the tool

Python 3.11+ with `requirements.txt` (Streamlit, pandas, PyYAML); launch with `streamlit run app.py`. It opens in a browser with no external services. Weights in `config/weights.yaml` take effect on reload.

## 6. Limitations

A conceptual prototype, not an empirically calibrated predictive model; weights are transparent assumptions, not coefficients estimated from Scrum data. The poster gives the fuller discussion and validation roadmap.

## Supplemental materials (uploaded separately)

- Video walkthrough (3–5 min) — *to be recorded*
- Screenshots of the four tabs — `docs/submission/figures/` (see `figures/README.md`)
- Runnable source (`agile-ai-simulator`) and `config/weights.yaml`
- Supporting docs: `docs/CONCEPTUAL_MODEL.md`, `docs/UML_CI_PERFORMANCE_ANALYSIS.md`, `docs/PARAMETER_DICTIONARY.md`

## References

- Beck, K., et al. (2001). *Manifesto for Agile Software Development.* https://agilemanifesto.org
- Hackman, J. R. (1987). The design of work teams. In J. W. Lorsch (Ed.), *Handbook of Organizational Behavior* (pp. 315–342). Prentice-Hall.
- Kommol, E., Riedl, C., & Woolley, A. (2025). The structure of collective intelligence. *OSF Preprints.*
- Riedl, C., Kim, Y. J., Gupta, P., Malone, T. W., & Woolley, A. W. (2021). Quantifying collective intelligence in human groups. *PNAS*, 118(21), e2005737118.
- Strode, D., Dingsøyr, T., & Lindsjørn, Y. (2022). A teamwork effectiveness model for agile software development. *Empirical Software Engineering*, 27(2), 56.
- Verwijs, C., & Russo, D. (2023). A theory of Scrum team effectiveness. *ACM TOSEM*, 32(3), 74.
- Woolley, A. W., Chabris, C. F., Pentland, A., Hashmi, N., & Malone, T. W. (2010). Evidence for a collective intelligence factor in the performance of human groups. *Science*, 330(6004), 686–688.
