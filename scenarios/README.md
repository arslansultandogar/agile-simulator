# CITAS Demonstration Scenarios — ODD Description

This document describes the two demonstration scenarios used to illustrate
CITAS (Collective Intelligence Testbed for Agile Sprints) *operation* and
*application and use*. It follows the ODD protocol (Overview, Design concepts,
Details) of Grimm et al. (2020), second update, and is intended to become an
appendix of the methods paper. Every scenario parameter carries a basis code:

| Code | Meaning |
|---|---|
| **REP** | reported in the anchor source |
| **DER** | derived from a reported figure |
| **ASS** | documented assumption |

Computed results are **not** reproduced here; they live in
[`../results_scenarios/RESULTS_SUMMARY.md`](../results_scenarios/RESULTS_SUMMARY.md)
and the CSV files alongside it. The configurations themselves are encoded, with
the same basis codes and justifications inline, in [`__init__.py`](__init__.py).

---

## 1. Purpose and patterns

**Purpose.** To demonstrate how CITAS is operated and applied to concrete,
empirically anchored agile development contexts, and to show what the model
can and cannot say about the value of AI decision support under varying trust
calibration. The scenarios are *demonstrations of model behaviour*, not
predictions about the anchor projects: CITAS is a transparent, formula-based
conceptual model whose weights are documented assumptions rather than
coefficients estimated from field data.

**Patterns used for evaluation.** Two qualitative patterns from the literature
are used to judge whether the model behaves plausibly:

1. *Calibrated reliance* — AI benefit should depend on the alignment between
   trust and actual reliability, with over-trust in an unreliable assistant
   producing harm rather than a floor of benefit (Lee & See 2004).
2. *Team process over tooling* — collective-intelligence and process variables
   should account for outcome differences that individual capability alone
   cannot (Woolley et al. 2010; Riedl et al. 2021).

## 2. Entities, state variables, and scales

**Entities.** A *team* of `team_size` members, each with role (Product Owner,
Scrum Master, Developer, Tester), skill level, availability, communication
level, social sensitivity, trust in AI and *perceived* AI reliability. A
*backlog* of `number_of_tasks` tasks of four types (feature, bug, refactor,
spike), each with difficulty, effort points, priority, uncertainty, required
skill, and optional upstream dependencies. An optional *AI assistant*
(allocation recommendations plus a shared-cognition dashboard).

**Team-level state.** Six collective-intelligence subconstructs — transactive
memory, shared attention, shared reasoning, social sensitivity, participation
balance, transactive coordination — plus team engagement and diversity terms,
aggregated by externalised weights (`config/weights.yaml`) into a CI score.

**Scales.** Time is discrete: one step = one sprint. **CITAS abstracts over
calendar time.** Sprints are discrete cycles with a fixed per-member capacity;
iteration length in weeks is not a model parameter (see §8, Design decision 1).

## 3. Process overview and scheduling

Each sprint executes, in order:

1. Select sprint tasks from the backlog under capacity and priority.
2. Compute coordination need from the task-type profiles of the selected work.
3. Allocate tasks — AI arm: recommendation-based allocation whose uptake
   depends on member trust and whose error rate depends on actual reliability;
   baseline arm: a heuristic allocator.
4. AI arm only: activate the shared-cognition dashboard.
5. Compute CI subconstructs and the aggregate CI score.
6. Compute decision quality from reasoning, attention, coordination, dashboard,
   social sensitivity and trust calibration.
7. Simulate task completion and defects; create rework where quality fails.
8. Update backlog, learned trust (perception moves toward actual reliability),
   and CI dimensions — feeding the next sprint.

Scrum roles modify strategy, coordination, blocker relief and defect
detection; sprint-phase modifiers represent planning, review and
retrospective quality.

## 4. Design concepts

- **Basic principles.** Collective intelligence as a group-level capacity only
  weakly predicted by individual ability (Woolley et al. 2010; Kommol, Riedl &
  Woolley 2025); trust calibration as the alignment of perceived and actual
  automation reliability (Lee & See 2004); Hackman's tripartite team
  effectiveness — task output, team viability, member sustainability.
- **Emergence.** Sprint outcomes (velocity, completion, defect rate) and the
  effectiveness composite emerge from the interaction of CI state, task
  structure, role effects and (in the AI arm) reliance on the assistant.
- **Adaptation and learning.** CI dimensions and team engagement update each
  sprint from outcomes, scaled by retrospective quality. Perceived AI
  reliability converges toward actual reliability at a fixed learning rate
  (learned trust). **Agent skill does not learn** (see §8, Design decision 2).
- **Sensing.** The AI allocation recommendation is followed with probability
  proportional to trust; a wrong recommendation is more likely to be followed
  the higher the trust (misuse / over-reliance).
- **Stochasticity.** Team generation, task generation, allocation errors,
  completion and defect draws all use a seeded NumPy generator.
- **Collectives.** The team is the unit of analysis; individuals contribute to
  team-level CI state.
- **Observation.** Per-sprint records and run-level summaries: velocity,
  completion rate, defect rate, decision quality, CI score, trust calibration,
  team effectiveness, viability, sustainability, carry-over, rework.

## 5. Initialization

Teams and backlogs are generated from the scenario parameters using
`random_seed`. Replication *i* uses seed `random_seed + i`. Within a paired
comparison the with-AI and without-AI arms use the **same** seed, so they see
the same team and the same backlog. The model's built-in defaults apply to
anything a scenario does not set; three such parameters are listed explicitly
in §7 because the model requires them.

## 6. Input data

None. The scenarios use no time-series input; all exogenous information enters
through the parameters in §7.

## 7. Submodels and parameterisation

Model equations are documented in `docs/CONCEPTUAL_MODEL.md` and
`docs/PARAMETER_DICTIONARY.md`; weights in `config/weights.yaml`. This section
records the scenario-specific parameter values and their provenance.

### 7.1 Scenario A — safety-critical embedded (brake control unit)

**Narrative.** An incremental release of the software for an electronic brake
control unit (EBCU) developed alongside a coupled instrument cluster unit
(ICU). A functional update to an existing certified code base under ISO 26262,
so every increment carries non-deferrable verification and documentation, and
hardware-in-the-loop integration windows are scheduled rather than on demand.
Cross-unit dependency is the defining structural feature. Five co-located
engineers of mixed seniority; the anchor case was notable for being staffed
largely with engineers new to the domain, with knowledge unevenly distributed
between brake-control and display-layer specialists. Two-week sprints over a
representative twelve-sprint window.

**Quantitative anchor.** Van Schooenderwoert (2006): team of 4–6; iterations
2–8 weeks settling to 2; ~3-year project; 29,500 effective SLOC ≈ 230 function
points; 51 defects generated, 59% found internally, 21 delivered; never more
than 2 open at once; ~1.5 bugs/month; 0.22 defects per function point;
average cyclomatic complexity 6–7; co-located.
*Caveat: this is an industry experience report authored by the project's
technical lead, not an independent controlled study. Its figures are treated
as illustrative, not as ground truth.* Process and regulatory characteristics
from Diebold & Mayer (2017) and Heeager & Nielsen (2020).

| Parameter | Value | Basis | Justification |
|---|---|---|---|
| `team_size` | 5 | REP | anchor reports 4–6 |
| `number_of_sprints` | 12 | ASS | representative window; anchor ran ~3 years |
| `number_of_tasks` | 60 | DER | from ~230 function points at the anchor's granularity |
| `task_mix` | feature .45 / bug .20 / refactor .25 / spike .10 | ASS | brownfield safety-critical profile |
| `dependency_density` | 0.45 | ASS | EBCU–ICU coupling; scheduled HIL windows |
| `task_complexity` | 0.72 | ASS | cyclomatic complexity 6–7 with real-time constraints |
| `effort_management` | 0.75 | DER | sustained low open-defect count implies strong effort discipline |
| `skills_knowledge_coordination` | 0.60 | ASS | mixed seniority; specialists not interchangeable |
| `task_strategy` | 0.70 | REP | iteration length actively tuned over the project |
| `consequentiality` | 0.85 | ASS | ISO 26262 obligations; visible safety stakes |
| `collective_memory` | 0.50 | ASS | newcomer-heavy staffing; low initial shared knowledge (default 0.62) |
| `collective_attention` | 0.70 | ASS | small co-located team |
| `collective_reasoning` | 0.60 | ASS | rises as domain familiarity accumulates |
| `enable_rework` | true | REP | 59% of generated defects caught internally |
| `enable_sprint_phases` | true | REP | review discipline is the anchor's distinguishing feature |

### 7.2 Scenario B — large-scale enterprise information system

**Narrative.** A replacement office-automation and case-processing system for
a public-sector pension provider: benefit calculation, case handling, member
self-service and integrations. Requirements are partly inherited from the
legacy platform and partly renegotiated; correctness is audited rather than
safety-certified. Programme scale: roughly EUR 140 million, January 2008 to
March 2012, ~2,500 user stories under ~300 epics; up to twelve teams in
parallel drawn from 175 people, about 100 of them external consultants
(Dingsøyr, Moe & Seim 2018). One **representative team** of seven developers
plus a product owner is modelled, with architecture and test as programme-level
functions. Three-week cadence, twelve sprints. Coordination need dominates;
consequentiality is moderate.

| Parameter | Value | Basis | Justification |
|---|---|---|---|
| `team_size` | 7 | ASS | Scrum norm; programme reports 175 people over 12 teams |
| `number_of_sprints` | 12 | DER | three-week cadence over ~9 months |
| `number_of_tasks` | 200 | DER | scaled from ~2,500 programme-level stories |
| `task_mix` | feature .60 / bug .15 / refactor .15 / spike .10 | ASS | green-field enterprise delivery profile |
| `dependency_density` | 0.35 | DER | inter-team dependencies across 12 parallel teams |
| `task_complexity` | 0.55 | ASS | business-logic complexity, no real-time constraints |
| `effort_management` | 0.65 | ASS | model default; no anchor evidence |
| `skills_knowledge_coordination` | 0.55 | DER | consultant-heavy staffing (100 of 175) |
| `task_strategy` | 0.65 | REP | full Scrum ceremony set reported |
| `consequentiality` | 0.60 | ASS | public-service obligation; no safety criticality |
| `collective_memory` | 0.45 | DER | external consultants; knowledge does not persist |
| `collective_attention` | 0.55 | ASS | twelve parallel teams dilute shared focus |
| `collective_reasoning` | 0.65 | ASS | model default; no anchor evidence |
| `enable_rework` | true | ASS | no anchor figure |
| `enable_sprint_phases` | true | REP | planning, daily and retrospective all reported |

### 7.3 AI arm (shared by both scenarios)

| Parameter | Value | Basis | Note |
|---|---|---|---|
| `ai_support_level` | 0.70 | ASS | shared so scenarios are comparable on the AI dimension |
| `ai_reliability` | 0.78 | ASS | swept 0.30–0.95 in the Scenario A sensitivity analysis |
| `trust_in_ai` | 0.65 | ASS | swept independently to expose mis-calibration |
| `dashboard_quality` | 0.70 | ASS | shared |

### 7.4 Parameters required by the model but not in the scenario specification

These three were **added during implementation**; all are ASS.

| Parameter | Value | Reason |
|---|---|---|
| `female_proportion` | 0.50 | neither anchor reports gender composition; the default avoids an unevidenced Woolley-proxy effect on social sensitivity |
| `team_engagement_baseline` | 0.65 | stakes are already carried by `consequentiality`; raising both would double-count |
| `random_seed` | 42 | matches the thesis base seed; replication *i* uses 42 + *i* |

### 7.5 Baseline definition — a correction to the original specification

The original scenario specification defined the baseline arm as
`ai_support_level = 0`. **That is not a no-AI condition in CITAS.** With
`use_ai=True`, a support level of zero still executes `allocate_tasks_with_ai`,
still runs `shared_cognition_assistant` (whose coordination gain retains
non-AI terms), and still applies the `misfit_penalty` when calibration is low.
It is an AI-enabled team with the support dial at zero — a model artefact, not
a research condition — and would not be comparable to the thesis results.

**All baseline arms therefore use `run_simulation(cfg, use_ai=False)`**: the
heuristic allocator with no assistant, exactly as in the thesis
`paired_ai_benefit` convention. No `ai_support_level = 0 / use_ai=True`
condition is run.

## 8. Design decisions and stated limitations

**Design decision 1 — calendar time and sprint length.** CITAS represents
sprints as discrete cycles and abstracts over calendar time; iteration length
is not a model parameter (per-member capacity per sprint is a fixed constant).
A planned four-week-increment variant of Scenario A was therefore **dropped**
rather than approximated: halving the sprint count at unchanged capacity would
answer a different question (a half-horizon run, not a longer cadence), and
adding a linear capacity multiplier would encode an unevidenced assumption
that a four-week sprint delivers twice the throughput of a two-week one.
Heeager & Nielsen's (2020) observation that safety-critical contexts strain the
two-week cadence concerns documentation overhead and feedback-cycle frequency,
not raw capacity. It is recorded here as **outside current model scope** and
flagged as future work requiring a documentation-overhead mechanism, not a
capacity multiplier.

**Design decision 2 — agent skill.** Agent skill is drawn from a fixed
distribution at initialisation and has **no learning mechanism**; within-project
skill growth is not represented. Scenario A's inexperienced staffing is
operationalised through reduced initial collective memory (0.50) and
knowledge/skills coordination (0.60), not through agent skill levels. Scenario
B's consultant-heavy staffing is operationalised the same way (collective
memory 0.45, coordination 0.55); `skill_diversity` is a **computed output** of
the model, not an input, and cannot be set.

**Design decision 3 — baseline arm.** See §7.5.

**Model version.** All results derive from model **v2.1** mechanics
(`config/weights.yaml: model_version 2.1.0`, `perceived_reliability_anchor:
trust`). `run_scenarios.py` refuses to run under any other version or anchor
setting. The `anchor: "actual"` switch reverts only the perception anchor, not
the v2.1 misallocation floor or wrong-pick diversion, so it does not restore
v2.0 and is not used.

## 9. Experimental design

| Experiment | Scenarios | Design | Replications |
|---|---|---|---|
| Paired arms | A, B | with-AI vs without-AI on identical seeds | 200 per scenario |
| Reliability sweep | A | `ai_reliability` 0.30–0.95 step 0.05, at `trust_in_ai` 0.65 and 0.85 | 200 paired per point |
| Trust × reliability grid | A | both 0.30–0.95 step 0.05 (14 × 14 = 196 cells) | 40 paired per cell |
| Supplementary reliability sweep | A | as the sweep above but `ai_support_level` 0.80 instead of 0.70 (the thesis crossing run's level); nothing else changed | 200 paired per point |
| Isolating sweep (default process) | A | as the supplementary sweep (support 0.80) but with `effort_management`, `skills_knowledge_coordination`, `task_strategy`, `consequentiality` reset to the model defaults (0.65); team, backlog, schedule and CI baselines remain Scenario A's | 200 paired per point |

**AI benefit** is the paired difference in team effectiveness (with-AI minus
without-AI) on the same seed; 95% CI = mean ± 1.96·SE. The model's internal
`ai_benefit` summary score is a with-AI-only quantity (zero by construction in
the baseline arm) and is reported separately, labelled as such.

**Common random numbers.** The grid and the sweep use the **same seed sequence
in every cell** (`seed = 42 + i`, *i* = 0…N−1), rather than seeds that vary by
cell, so cell-to-cell differences reflect the parameter change rather than
sampling noise. Standard errors are reported per cell so precision is visible.

**Supplementary sweep (support 0.80).** Because the main sweep found no zero crossing for Scenario A, a supplementary sweep repeats it with `ai_support_level` raised to 0.80 - the level at which the thesis located a crossing on the default process profile - with every other Scenario A parameter unchanged. This is a single-factor test of whether the absence of a crossing is attributable to the support level rather than to the scenario's configuration (script `run_scenarios_support_sweep.py`; outputs tagged `support080`). A second, **isolating sweep** additionally resets the four process parameters to the model defaults (`--default-process`; outputs tagged `support080_defproc`), so that the only remaining differences from the thesis crossing run are Scenario A's team size, sprint count, backlog mix, task complexity, dependency density and CI baselines. A positive control confirms that the same harness reproduces the thesis crossing bit-for-bit on the thesis configuration.

**Zero crossing.** For each trust level the reliability at which the AI-benefit
curve crosses zero is found by linear interpolation between adjacent sweep
points; the number of crossings and the sign at both ends of the range are
recorded, and the first reliability at which the 95% CI lies wholly above zero
is reported alongside.

## References

- Diebold, P. & Mayer, M. (2017). On the usage and benefits of agile methods &
  practices: a case study at Bosch Chassis Systems Control. *XP 2017*,
  LNBIP 283, 243–250. DOI 10.1007/978-3-319-57633-6_16
- Dingsøyr, T., Moe, N. B. & Seim, E. A. (2018). Coordinating knowledge work in
  multi-team programs: findings from a large-scale agile development program.
  *Project Management Journal*. Preprint arXiv:1801.08764
- Grimm, V. et al. (2020). The ODD protocol for describing agent-based and
  other simulation models: a second update. *JASSS*, 23(2), 7.
  DOI 10.18564/jasss.4259
- Heeager, L. T. & Nielsen, P. A. (2020). Meshing agile and plan-driven
  development in safety-critical software: a case study. *Empirical Software
  Engineering*, 25(2), 1035–1062. DOI 10.1007/s10664-020-09804-z
- Kommol, E., Riedl, C. & Woolley, A. (2025). The structure of collective
  intelligence: evidence for collective memory, attention, and reasoning.
  *OSF Preprints*.
- Lee, J. D. & See, K. A. (2004). Trust in automation: designing for
  appropriate reliance. *Human Factors*, 46(1), 50–80.
- Riedl, C., Kim, Y. J., Gupta, P., Malone, T. W. & Woolley, A. W. (2021).
  Quantifying collective intelligence in human groups. *PNAS*, 118(21),
  e2005737118.
- Van Schooenderwoert, N. (2006). Embedded agile project by the numbers with
  newbies. *Agile Conference 2006 (AGILE'06)*, 351–363.
- Woolley, A. W., Chabris, C. F., Pentland, A., Hashmi, N. & Malone, T. W.
  (2010). Evidence for a collective intelligence factor in the performance of
  human groups. *Science*, 330(6004), 686–688.
