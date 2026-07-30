# Internship Report — Cover Page

**Course code and name:**  
814601S Work Experience in ICT responsibilities (5 ECTS)  
814311A Internship in ICT duties (5 ECTS)

**Report title:** Internship Report — The Simulation of Collective Intelligence in Agile Teams: a Transparent Testbed

**Student name:** Arslan Sultan  
**Student number:** 1.2.246.562.24.35253236476  
**Email:** arslan.sultan@student.oulu.fi  
**Degree programme:** Information Processing Science / Computer Science and Engineering  
**Home university:** University of Oulu, Finland

**Employer:** Universidad Politécnica de Madrid (UPM)  
**Department:** Escuela Técnica Superior de Ingeniería de Sistemas Informáticos (ETSISI)  
**Address:** Calle Alan Turing S/N, 28040 Madrid, Spain  
**Workplace supervisor:** Juan Garbajosa, Professor  
**University contact:** University Lecturer Tonja Molin-Juustila (tonja.molin-juustila@oulu.fi)

**Internship period:** 1 May 2026 – 31 July 2026  
**Working time:** Full-time (40 hours per week; 520 hours total)  
**Type:** University-supported summer trainee scholarship

**Place and date:** Oulu, August 2026

---

# Table of Contents

1. Introduction  
2. Preparation  
3. Employer and internship organization  
4. Duties and assignments  
5. Fulfilment of plans and personal development  
6. The application of skills in the future  
7. Suggestions for improving the degree program  
8. Deliverables  

---

# 1. Introduction

This report describes my practical training at Universidad Politécnica de Madrid (UPM) from 1 May to 31 July 2026 and reflects on how the internship supported my learning goals, personal development, and the connection between university studies and professional ICT work. During the three-month, full-time placement, my main responsibility was the design, implementation, documentation, and iterative refinement of **The Simulation of Collective Intelligence in Agile Teams: a Transparent Testbed**, a Python-based research prototype that models how collective intelligence (CI), agile teamwork, and AI support interact across software development sprints.

The internship was supported by a summer trainee scholarship from the University of Oulu, which required a pre-internship plan, weekly progress reports with documented hours, and this final reflective report. The work was strongly connected to my degree studies and thesis direction. Rather than routine production maintenance, the assignment focused on building an explainable simulation environment, connecting theoretical models from research literature to working software, and producing documentation and experimental outputs suitable for academic evaluation and conference submission.

This report examines the internship in relation to the set learning objectives: applying university knowledge to work assignments, evaluating myself as a learner and worker, planning time systematically, working independently and in collaboration, understanding the work community, and identifying possible future career directions.

---

# 2. Preparation

I found the internship opportunity through academic collaboration between the University of Oulu and Universidad Politécnica de Madrid. Professor Juan Garbajosa at UPM offered a research-oriented placement aligned with my interest in collective intelligence, agile software development, and human–AI teaming. Before starting, I reviewed the learning objectives for practical training at the University of Oulu and agreed on expected duties, reporting rhythm, and deliverables with both my workplace supervisor and the university contact person, Tonja Molin-Juustila.

When preparing for the placement, I used the University of Oulu internship website, the Information Processing Science programme instructions in Peppi, and the Moodle learning environment titled "Internship guidelines and templates." The most useful resources were the separate templates for the internship plan and weekly progress reports, because they clarified what documentation was mandatory for students receiving financial support from the university. I also used earlier course materials from software engineering, research methods, agile development, and data analysis to prepare for the technical scope of the project.

I utilized career services information on supported internships and the Aarresaari network to understand how university-funded placements differ from retrospective work-experience reporting. Because my placement was international and research-linked, I also prepared by reading foundational papers on collective intelligence (Woolley et al., 2010; Riedl et al., 2021) and agile team effectiveness (Verwijs & Russo, 2023; Strode et al., 2022) before the first working week.

In hindsight, I would have appreciated more example reports from research-oriented international internships, because most available examples assume domestic company placements in product development. Once the internship started, regular weekly meetings with Professor Garbajosa and structured progress reporting reduced uncertainty and kept the work aligned with both UPM expectations and University of Oulu requirements.

---

# 3. Employer and internship organization

## 3.1 My role at UPM

During the internship, I worked as a research software development trainee within the Escuela Técnica Superior de Ingeniería de Sistemas Informáticos (ETSISI) at Universidad Politécnica de Madrid. My work supported research and teaching activities related to software engineering, agile methods, and collective intelligence in team settings. A substantial part of the placement involved studying and analysing the scientific background and related work in the literature, including papers on collective intelligence (Woolley et al., 2010; Riedl et al., 2021; Kommol, Riedl & Woolley, 2025), agile and Scrum team effectiveness (Verwijs & Russo, 2023; Strode et al., 2022), and team effectiveness foundations (Hackman, 1987; Wageman et al., 2005). Although the primary deliverable was an academic prototype rather than a commercial product, the work followed a realistic software development process: requirements refinement, iterative implementation, testing, documentation, demo preparation, and revision based on supervisor feedback.

The Simulation of Collective Intelligence in Agile Teams: a Transparent Testbed became the central artifact of the placement. It allows users to compare sprint outcomes with and without AI support, inspect collective intelligence subconstructs, run Monte Carlo experiments, and perform sensitivity analysis on parameters such as AI reliability, trust, process quality, and team composition factors. The tool makes abstract research concepts operational and supports discussion about how team-level performance emerges from shared cognitive and social processes rather than from individual skill alone.

## 3.2 Connection to employer strategy and target groups

The UPM School of Computer Systems Engineering (Escuela Técnica Superior de Ingeniería de Sistemas Informáticos, ETSISI) emphasizes rigorous software engineering education and research that connects theory with practical systems. My assignment supported this direction by creating a transparent tool that helps explain team-level performance beyond velocity metrics alone. The most important target groups were:

- **Researchers and supervisors at UPM**, who needed a concrete model to discuss CI, agile effectiveness, and AI-supported teamwork;
- **Students and academic audiences**, who could use the transparent testbed to explore research questions in a visual and interactive way;
- **Potential conference and demo audiences**, for whom the tool needed to be understandable, reproducible, and scientifically grounded.

I interacted primarily with Professor Garbajosa through weekly supervision meetings, email, and ad hoc discussions about model assumptions and documentation quality. I also coordinated with University of Oulu reporting requirements through the internship Moodle environment. My work did not involve direct commercial customer delivery, but it required translating research feedback into software and documentation changes that would be credible to an academic audience.

## 3.3 Effect of my work

My work produced several concrete outputs that benefited the employer organization:

- a functioning Streamlit-based simulation application (the transparent testbed);
- a modular Python codebase covering simulation, metrics, AI support, experiments, and configuration;
- conceptual and UML documentation linking CI theory to agile performance outcomes;
- experiment support through Monte Carlo replication and one-parameter sensitivity analysis;
- an automated pytest suite and externalized model weights for transparency;
- two conference submissions to the **CI/HCOMP Posters & Demos** track (see Section 8).

These outputs helped make abstract research concepts operational. For example, the distinction between process measures and individual attributes, the role of trust calibration in AI-supported teams, and the Hackman-style view of effectiveness (task output, team viability, member sustainability) became visible through runnable scenarios rather than remaining only in written theory.

## 3.4 Development targets in the organization

I identified several areas where UPM or the research project could develop further:

1. **Empirical validation** — the testbed is theory-driven and would benefit from comparison with real Scrum team survey data or observational studies.
2. **Structured user testing** — although the tool is interactive, feedback from practitioners (Scrum Masters, developers, team leads) would improve usability and ecological validity.
3. **Clearer separation between research prototype and production software** — this would help future contributors understand which parts are stable and which are experimental.
4. **Stronger experiment logging pipeline** — standardized templates for scenario name, parameters, and observed effects would improve research traceability.

Suggested development actions would include running structured demo sessions with software engineering students and practitioners, collecting qualitative feedback, and planning a small validation study using existing agile team effectiveness instruments such as those referenced by Verwijs & Russo (2023) and Strode et al. (2022).

## 3.5 Working environment and social integration

I adapted well to the working environment at UPM after the first two weeks, when the project scope and reporting rhythm became clearer. The placement was hybrid in nature: I worked remotely on implementation and documentation while maintaining regular online supervision with Madrid. This arrangement required disciplined time management but also developed my ability to work independently across time zones.

I participated in regular research discussions with my supervisor and engaged with the broader academic context of the project through literature review and conference submission preparation. The internship created a valuable professional connection with Professor Garbajosa and strengthened the collaboration between UPM and the University of Oulu in the area of agile team research and simulation-based methods.

---

# 4. Duties and assignments

## 4.1 Main duties

My main duties during the internship included the following areas of work.

**Software design and implementation.** I built **The Simulation of Collective Intelligence in Agile Teams: a Transparent Testbed** in Python using Streamlit for the user interface. I implemented the sprint simulation loop, including task selection, allocation, completion and defect modelling, trust learning, and collective intelligence updates. I developed modules for team generation, backlog and task profiles, AI support, metrics, and experiments. I added advanced model features including mixed backlogs, carry-over work, task dependencies, defect rework, sprint-phase modifiers, Scrum roles, externalized weights in YAML configuration, preset scenarios, and CSV/JSON export functions.

**Research modelling and documentation.** I studied and analysed the background and related work in the literature on collective intelligence and agile effectiveness, and mapped research constructs to testbed variables. I created conceptual models, UML diagrams, causal maps, and a detailed CI-to-performance analysis document. I integrated supervisor feedback aligning the model with Riedl et al. (2021), Kommol, Riedl & Woolley (2025), Hackman (1987), Wageman et al. (2005), and agile/Scrum effectiveness literature. I documented simulation weights as transparent assumptions rather than empirically estimated coefficients.

**Testing and validation.** I implemented pytest-based tests for metrics and simulation behaviour. I ran smoke tests, Monte Carlo comparisons, and sensitivity analyses to verify that parameter changes produced logically consistent outcomes. I used reproducible random seeds and exported results for analysis.

**Academic dissemination support.** I submitted **two papers** to the **CI/HCOMP Posters & Demos** conference track under the shared title *Collective Intelligence in Agile Teams: A Transparent Simulation Testbed for Studying Team Decisions Across Sprints* (authors: Arslan Sultan, Juan Garbajosa): one to the **Demo track**, describing testbed architecture and live interaction, and one to the **Poster track**, presenting the conceptual CI-and-agile research argument.

## 4.2 Benefit to the employer

My work benefited UPM by turning a research idea into a usable and explainable prototype. Instead of discussing CI and agile performance only at a theoretical level, the organization now has an interactive tool for exploring scenarios, a transparent formula-based model that can be critiqued and extended, documentation that supports thesis work and publication activities, and a codebase structured for future research iterations. This reduced the gap between conceptual research and demonstrable software artifact.

## 4.3 Development targets in working processes

Within the working process itself, I identified several improvement opportunities. Earlier test automation would have reduced rework on some features that were added quickly and tested later. A more structured experiment logging template would improve research traceability. Externalizing weights to `config/weights.yaml` was a major improvement that should continue for all future model changes. Both thesis writing and implementation advanced in parallel, which was productive but sometimes made prioritization difficult; clearer sprint boundaries between coding and writing weeks would help in future placements.

## 4.4 Leadership styles and independence

During the internship I encountered supportive, coaching-oriented academic supervision. Professor Garbajosa allowed significant independence in implementation details, UI design, and experiment structure, while providing direction on research framing, model correctness, and documentation quality. I was allowed to make independent decisions on code structure and documentation organization, but major model interpretation decisions were discussed before being finalized. This balance developed both autonomy and the ability to accept constructive academic feedback.

---

# 5. Fulfilment of plans and personal development

## 5.1 Internship plan and learning goals

My original plan was to apply software engineering and research skills to a substantive ICT assignment, produce a working prototype, and connect the work to my broader degree project. Overall, the plan was fulfilled successfully across all six learning objectives.

I applied university knowledge to field work by using software architecture, Python development, research literature, simulation design, testing, and technical writing in a real project over thirteen full-time weeks. I evaluated and developed myself as a learner and worker by learning to balance implementation speed with research precision and by improving my ability to accept and integrate detailed academic feedback. I planned and evaluated my use of time through weekly goals, daily work logs, and thirteen progress reports documenting 40 hours per week. I worked systematically and goal-oriented, implementing core modules independently while discussing model assumptions with my supervisor. I learned how research quality, clarity, reproducibility, and academic standards directed priorities at UPM. Finally, I confirmed interest in research-oriented software engineering, simulation and HCI, and agile team effectiveness domains as possible post-graduation directions.

## 5.2 Problems and how I acted

I encountered several challenges during the internship. Translating research papers into code was difficult because constructs such as transactive memory, social perceptiveness, and process criteria do not come with software formulas. I solved this by creating explicit simulation weights, documenting assumptions clearly, and distinguishing theory-backed constructs from implementation choices. Scope growth was another challenge: the project expanded from a basic testbed to include mixed backlogs, dependencies, roles, exports, tests, and multiple documentation layers. I handled this by prioritizing core functionality first and adding enhancements in planned iterations.

Environment and dependency issues arose when local Python environments lacked required packages. I solved this by using virtual environments and separating validation runs from normal development. Feedback integration sometimes required conceptual changes rather than code edits alone; I learned to update documentation, UML diagrams, UI labels, and formulas together so the project remained internally consistent.

## 5.3 Successes and strengths

I think I succeeded most in building a coherent end-to-end prototype rather than isolated scripts; making the model transparent and explainable; producing documentation that connects code, theory, and agile outcomes; responding systematically to feedback across multiple iteration cycles; and validating behaviour through experiments and automated tests.

My main strengths as an employee are analytical thinking, persistence, willingness to learn from feedback, ability to connect theory and implementation, and systematic documentation. I am still developing stronger skills in empirical validation and in estimating research-heavy tasks under fixed time pressure.

---

# 6. The application of skills in the future

## 6.1 Personal development goals

Based on the internship, I would set the following development goals. As a student, I want to strengthen empirical research skills, especially validation and survey or experiment design; improve academic writing efficiency without losing technical precision; and learn more about human–AI interaction and trustworthy AI in team settings. As an employee, I want to develop stronger test-driven development habits, improve presentation of technical work to non-programmer stakeholders, and build experience in research software engineering and reproducible computational models.

## 6.2 Possible future duties

The internship helped me identify future roles that fit my interests and skills: research software engineer; prototype developer in HCI or AI-supported teamwork; software engineer in agile product teams with a strong coordination and decision-support focus; technical analyst or consultant in team effectiveness or AI adoption; and further academic research in collective intelligence, agile software development, or human–AI collaboration.

## 6.3 Study plan, CV, and profiles

The internship influenced my study plan by confirming that courses and thesis work in software engineering, research methods, agile development, and AI ethics are relevant to the direction I want to pursue. I updated my CV to include Python and Streamlit prototype development, simulation and experiment design, research documentation and modelling, software testing, and academic presentation preparation. I updated my LinkedIn and GitHub profiles to reflect the project while keeping any confidential employer information out of public descriptions.

## 6.4 Recommendation of the employer

I would strongly recommend Universidad Politécnica de Madrid to other University of Oulu students who are interested in research-oriented software development, agile methods, or simulation-based team research. The placement was especially suitable for students who can work independently, accept detailed feedback, and connect coding with conceptual modelling. It may be less suitable for students who prefer only routine production tasks with fixed specifications and no research component.

---

# 7. Suggestions for improving the degree program

After completing the internship, I would suggest the following improvements to the Information Processing Science degree program at the University of Oulu.

First, provide example internship reports for research-oriented and international placements. Many examples assume domestic company internships in product development; research and university-collaboration placements have different outputs and should be represented too.

Second, offer a short course or workshop on research software engineering covering reproducibility, experiment logging, externalized configuration, documentation for academic artifacts, and test design. This would have helped me earlier in the placement.

Third, improve the connection between thesis work and practical training planning. When the internship and thesis overlap, clearer guidance on scope boundaries and reporting expectations would reduce uncertainty.

Fourth, include more practice in translating academic literature into models. This was one of the most valuable but difficult parts of my internship; structured exercises in turning papers into variables, assumptions, and diagrams would be useful.

Fifth, strengthen feedback on technical communication. Writing for supervisors, employers, and academic audiences requires different styles; more practice with reports, demo scripts, and concise model explanations would be beneficial.

---

# 8. Deliverables

## 8.1 Main deliverables

| # | Deliverable | Description |
|---|---|---|
| 1 | **The Simulation of Collective Intelligence in Agile Teams: a Transparent Testbed** | Working Python/Streamlit research prototype (model v2.0): sprint simulation, CI metrics, AI support, Monte Carlo and sensitivity experiments, externalized weights, automated tests |
| 2 | **Conceptual and technical documentation** | UML/conceptual models, CI-to-performance analysis, parameter dictionary, presentation report, improvement roadmap |
| 3 | **Internship reporting package** | Internship plan, 13 weekly progress reports, this final report |
| 4 | **Conference submissions** | Two submissions to CI/HCOMP Posters & Demos (see Section 8.2) |

## 8.2 Conference submissions

During the internship I submitted **two papers** to the **CI/HCOMP Posters & Demos** track in July 2026. Both submissions used the same title:

**Collective Intelligence in Agile Teams: A Transparent Simulation Testbed for Studying Team Decisions Across Sprints**

**Authors:** Arslan Sultan (corresponding author), Juan Garbajosa  
**Topic affiliation:** Collective Intelligence (CI); Human–AI Complementarity (HCOMP) — secondary

**Submission 1 — Demo track.** This submission described the transparent testbed architecture, how users interact with the software (single-run comparison, Monte Carlo replication, sensitivity analysis), and how the system would be demonstrated to a conference audience.

**Submission 2 — Poster track.** This submission presented the research concept: why collective intelligence is a useful lens for understanding agile teamwork, and how a transparent simulation testbed supports academic discussion and critique of model assumptions.

Together, these two submissions documented both the research idea and the working testbed produced during the internship.

---

**Student signature:** Arslan Sultan — Date: August 2026  
**Workplace supervisor:** Juan Garbajosa, Professor, UPM
