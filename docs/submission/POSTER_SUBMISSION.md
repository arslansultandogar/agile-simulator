# Poster Track Submission

**Title:** Collective Intelligence in Agile Teams: A Transparent Simulation Testbed for Studying Team Decisions Across Sprints

**Track:** Posters
**Topic affiliation:** Collective Intelligence (CI) — primary; Human–AI Complementarity and Alignment (HCOMP) — secondary
**Authors:** Arslan Sultan¹ (corresponding author), Juan Garbajosa²
*¹ [affiliation, email — to confirm] · ² [affiliation, email — to confirm]*
**Date:** July 2026

> **Scope of this paper.** This poster is the *conceptual* companion to the demo. It develops the argument — why collective intelligence is the right lens for agile teamwork, and what a transparent testbed adds — and treats the software only briefly. The tool's architecture and operation are described in the demo paper ([`DEMO_SUBMISSION.md`](DEMO_SUBMISSION.md)).

---

## Abstract

Agile software teams make repeated collective decisions across sprints — planning work, allocating it against expertise, coordinating dependencies, and adapting from outcomes. We argue that this is, first and foremost, a *collective-intelligence* (CI) process: performance emerges from shared memory, shared attention, shared reasoning, and social sensitivity rather than from the sum of individual skills [Woolley et al. 2010; Riedl et al. 2021; Kommol, Riedl & Woolley 2025]. Yet CI, agile team effectiveness, and human–AI teaming are usually studied in separate literatures. We present a transparent simulation testbed that models CI subconstructs as they drive team decisions across sprints, and — as a secondary contribution — lets researchers compare outcomes with and without AI decision support under varying trust and reliability. Every formula and weight is inspectable, so the model is a shared object for interdisciplinary critique rather than a black box. The testbed is intended for conceptual experimentation and conversation, not predictive forecasting.

## 1. Motivation: agile teamwork *is* a collective-intelligence process

Two decades ago the *Agile Manifesto* reframed software development as a human, interaction-intensive activity, valuing "individuals and interactions over processes and tools" and "customer collaboration over contract negotiation" — explicitly *against* a document-driven world with infrequent human contact [Beck et al. 2001]. That shift is significant for our purposes: the manifesto locates the sources of performance in *interaction and shared understanding*, which is precisely the territory of collective intelligence.

Collective intelligence is the general capacity of a group to perform across a wide range of tasks, and it is only weakly predicted by the average or maximum individual ability of members [Woolley et al. 2010]. Recent work decomposes this capacity into measurable subconstructs — collective (transactive) memory, collective attention, and collective reasoning — and shows they have distinct structure and consequences [Kommol, Riedl & Woolley 2025; Riedl et al. 2021]. Even at the dyad level, two minds combine to outperform the better individual only when their communication and confidence are well calibrated [Bahrami et al. 2010]. Social perceptiveness and balanced participation are consistent correlates of higher collective performance [Woolley et al. 2010; Woolley & Mayo 2025].

An agile sprint exercises exactly these mechanisms, repeatedly and with measurable outcomes (velocity, defect rate, completion). This gives agile work something abstract CI lab tasks lack — ecological validity for how software teams actually decide — while retaining the emergent, group-level character that CI research studies. **Our position: agile team effectiveness is best understood as an emergent collective-intelligence process, and simulation is a transparent way to study how CI, task structure, and AI support interact over time.**

## 2. From agile values to Scrum structure

Where the manifesto states values, *Scrum* supplies structure. It is worth being precise about what Scrum contributes: in its origins Scrum was a lightweight framework for **project planning and management** — roles, a backlog, and time-boxed iterations — and the now-familiar Scrum *values* and *principles* were articulated by the community later rather than being present from the start [Schwaber & Sutherland 2020]. We therefore treat Scrum not as the theory but as the concrete apparatus through which agile teams enact collective decisions: Product Owner, Scrum Master, Developer, and Tester roles; planning, review, and retrospective events; and a backlog of mixed work. Empirical models of agile and Scrum team effectiveness converge on the same emergent factors CI research emphasizes — shared mental models, communication, trust, responsiveness, and continuous improvement [Verwijs & Russo 2023; Strode, Dingsøyr & Lindsjørn 2022]. Scrum, in short, is where collective intelligence becomes observable at the cadence of a sprint.

## 3. A secondary lens: AI support and trust calibration

AI tools for planning, allocation, and shared dashboards are entering agile workflows. Whether they help is not settled by their raw capability: human–AI teaming research shows that benefit depends on *calibrated trust* — the alignment between perceived and actual reliability — so that over-trust in an unreliable assistant can be worse than no assistant at all. This is the HCOMP dimension of our testbed: AI is modeled as one input to collective decision quality, whose value is conditional on reliability and on how the team calibrates its reliance over successive sprints.

## 4. Modeling approach and core hypothesis

The testbed runs the same team and backlog through multiple sprints. Each sprint computes CI subconstructs, converts them (with task structure and AI support) into a decision-quality score, simulates completion and defects, and then updates learned trust and CI dimensions — so CI is a *dynamic* construct that evolves with outcomes, not a static team attribute. Team-level outcomes are summarized using a three-part effectiveness view — task output, team viability, and member sustainability — following Hackman's account that a team's success is not output alone [Hackman 1987; Wageman, Hackman & Lehman 2005].

> **Core hypothesis.** Agile team effectiveness is a function of individual capability, **collective intelligence**, task characteristics, and human–AI coordination quality — not of AI alone.

## 5. Illustrative findings from simulation experiments

These are conceptual demonstrations of the model's behavior, not empirical estimates (see §7).

| Configuration | Observed pattern in the model |
|---|---|
| High CI + calibrated trust + reliable AI | Higher velocity, lower defect rate, higher team viability |
| Over-trust + low AI reliability | More defects, negative AI benefit, trust miscalibration |
| Spike-heavy vs. feature-heavy backlog | Higher coordination need and a different defect profile |
| Strong process (effort, knowledge, strategy) | CI and decision quality improve even without strong AI |

The last row matters for the CI reading: process quality lifts outcomes *through* collective intelligence, independently of the AI assistant — consistent with the process predictors emphasized in CI measurement work [Riedl et al. 2021].

## 6. Why this is interesting to the CI/HCOMP community

- It operationalizes CI subconstructs — memory, attention, reasoning, social sensitivity, participation balance — as levers that *drive* decisions in an ecologically grounded agile setting, not as post-hoc correlates [Woolley et al. 2010; Kommol, Riedl & Woolley 2025].
- It models CI as *dynamic*, evolving across sprints with coordination demand, dashboard quality, trust calibration, and outcomes.
- It makes every assumption inspectable, turning the model into a shared artifact reviewers can challenge, re-parameterize, and extend — the kind of transparent object interdisciplinary CI/HCOMP conversation needs.

## 7. Limitations

The testbed is a conceptual prototype, not an empirically calibrated predictive model. Weights are transparent simulation assumptions, not coefficients estimated from Scrum datasets. Future work includes empirical validation against team data, richer coordination measurement, and modeling conformity and over-reliance when shared-cognition tools dominate decisions.

## 8. Interaction at the poster session

Attendees can run the live tool at the poster (see the demo paper): adjust CI, trust, AI reliability, and task mix; run counterfactual scenarios; and discuss which assumptions they would challenge or extend. The accompanying architecture figure and screenshots make the model concrete.

## References

- Bahrami, B., Olsen, K., Latham, P. E., Roepstorff, A., Rees, G., & Frith, C. D. (2010). Optimally interacting minds. *Science*, 329(5995), 1081–1085.
- Beck, K., et al. (2001). *Manifesto for Agile Software Development.* https://agilemanifesto.org
- Hackman, J. R. (1987). The design of work teams. In J. W. Lorsch (Ed.), *Handbook of Organizational Behavior* (pp. 315–342). Prentice-Hall.
- Kommol, E., Riedl, C., & Woolley, A. (2025). The structure of collective intelligence: Evidence for collective memory, attention, and reasoning. *OSF Preprints.*
- Riedl, C., Kim, Y. J., Gupta, P., Malone, T. W., & Woolley, A. W. (2021). Quantifying collective intelligence in human groups. *PNAS*, 118(21), e2005737118.
- Schwaber, K., & Sutherland, J. (2020). *The Scrum Guide.* https://scrumguides.org
- Strode, D., Dingsøyr, T., & Lindsjørn, Y. (2022). A teamwork effectiveness model for agile software development. *Empirical Software Engineering*, 27(2), 56.
- Verwijs, C., & Russo, D. (2023). A theory of Scrum team effectiveness. *ACM Transactions on Software Engineering and Methodology*, 32(3), 74.
- Wageman, R., Hackman, J. R., & Lehman, E. (2005). Team diagnostic survey. *Journal of Applied Behavioral Science*, 41(4), 373–398.
- Woolley, A. W., Chabris, C. F., Pentland, A., Hashmi, N., & Malone, T. W. (2010). Evidence for a collective intelligence factor in the performance of human groups. *Science*, 330(6004), 686–688.
- Woolley, A. W., & Mayo, A. T. (2025). Teams. In *The Handbook of Social Psychology* (6th ed.). Situational Press.

## Related Documents

- Demo (tool operation): [`DEMO_SUBMISSION.md`](DEMO_SUBMISSION.md)
- Submission decisions: [`SUBMISSION_DECISIONS.md`](SUBMISSION_DECISIONS.md)
- Pre-submission checklist: [`SUBMISSION_CHECKLIST.md`](SUBMISSION_CHECKLIST.md)
