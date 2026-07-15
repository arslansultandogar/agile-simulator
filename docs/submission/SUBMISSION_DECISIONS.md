# Submission Decisions and Rationale

**Project:** Agile AI Simulator (`agile-ai-simulator`)  
**Prepared for:** CI/HCOMP Posters & Demos track  
**Date:** July 2026

---

## Track Decision: Demo

| Factor | Rationale |
|---|---|
| **Interactive testbed** | The project is a working simulation environment with live parameter controls, sprint-by-sprint outputs, and exportable results—not a static poster |
| **Hands-on engagement** | Attendees can adjust trust, AI reliability, task mix, and process parameters and immediately see CI, decision quality, and effectiveness respond |
| **Video walkthrough** | Demo track requires a video; the recommended 8–10 minute demo script is ready to record |
| **High visibility** | Demo track offers a table, power, and Wi-Fi for live interaction at the conference |

**Fallback:** If video recording is not feasible, use [`POSTER_SUBMISSION.md`](POSTER_SUBMISSION.md) instead, with optional screenshots.

## Topic Affiliation Decision: Collective Intelligence (CI), with HCOMP secondary

| Factor | Rationale |
|---|---|
| **Core contribution** | The simulator's primary research question is how CI subconstructs (memory, attention, reasoning, social sensitivity) influence agile sprint outcomes |
| **Theoretical grounding** | Model weights and structure follow Woolley (2010), Riedl et al. (2021), and Kommol, Riedl & Woolley (2025) |
| **Dynamic CI** | CI evolves across sprints based on coordination need, dashboard quality, trust calibration, and outcomes |
| **HCOMP angle** | AI support and trust calibration provide a strong secondary connection to human–AI complementarity—especially the misuse vs under-use dynamic |

## Submission Focus

**Title:** Collective Intelligence in Agile Teams: A Transparent Simulation Testbed for Studying Team Decisions Across Sprints

*Title rationale (per reviewer feedback):* Collective Intelligence leads, since this is a CI conference and CI is the primary contribution. "Agile" stays in the title as the setting; **Scrum is deliberately introduced later in the body** rather than the title — leaving both "agile" and "scrum" in the title would dilute the CI framing, and Scrum's values/principles were articulated by the community after Scrum's origins as a planning framework. The body opens from the Agile Manifesto (interaction and collaboration over documentation) and then narrows to Scrum as the concrete apparatus.

**Authors:** Arslan Sultan (first / corresponding author), Juan Garbajosa. Affiliations and emails to be confirmed.

**Two-paper split:** The **demo** paper carries the tool (architecture + operation); the **poster** paper carries the concept (the CI argument, evidence-backed). Content that "explains the subject well" was moved into the poster; the demo now describes tool operation, with an architecture figure and screenshots.

**Core claim:** Agile team effectiveness is an emergent collective-intelligence process, and simulation gives us a transparent way to study how CI, task complexity, AI support, trust, and sprint decisions interact over time.

## Why Agile + CI Is Worth Studying Together

1. **Agile is a natural CI laboratory.** Sprints are repeated collective decision cycles with measurable outcomes (velocity, defects, viability). Unlike abstract CI lab tasks, agile work has ecological validity for software teams.

2. **CI explains what velocity alone cannot.** Two teams with identical individual skills can differ in sprint outcomes because of shared attention, transactive memory, and participation balance. The simulator makes these mechanisms explicit.

3. **AI adoption is not uniformly positive.** The simulator shows that high trust with low AI reliability increases defects and reduces benefit—a core HCOMP insight with practical implications for tool design and team training.

4. **Task type changes coordination demand.** Feature-heavy vs spike-heavy sprints require different CI profiles. Studying agile and CI together reveals that "team effectiveness" is context-dependent.

5. **Simulation enables transparent critique.** Every formula and weight is inspectable. Reviewers and attendees can challenge assumptions, run counterfactuals, and propose alternative models—supporting the interdisciplinary CI/HCOMP conversation.

## Expected Audience Engagement at the Conference

| Activity | Duration | Goal |
|---|---|---|
| **Live demo: baseline comparison** | 2 min | Show with-AI vs without-AI on same team/backlog |
| **Live demo: trust miscalibration** | 2 min | Drop AI reliability; show harm from over-trust |
| **Attendee hands-on** | 5–10 min | Let attendees adjust parameters and explore preset scenarios |
| **Q&A on model assumptions** | Open | Discuss weights, limitations, and future validation |
| **Export for follow-up** | — | Offer exported results for interested researchers |

## Suitability for Emerging / Late-Breaking Work

- **Recent findings:** Model v2.0 adds Scrum roles, sprint phases, dependencies, rework, and externalized weights (May 2026)
- **Innovative idea:** First transparent testbed bridging CI theory, agile/Scrum effectiveness, and human–AI trust calibration
- **Early proof-of-concept:** Functional simulation with Monte Carlo and sensitivity analysis; not yet empirically validated
- **Productive conversation potential:** Invites critique of assumptions, comparison with field data, and extension to other team contexts

## Related Documents

- Demo writeup: [`DEMO_SUBMISSION.md`](DEMO_SUBMISSION.md)
- Poster alternative: [`POSTER_SUBMISSION.md`](POSTER_SUBMISSION.md)
- Pre-submission checklist: [`SUBMISSION_CHECKLIST.md`](SUBMISSION_CHECKLIST.md)
