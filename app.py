from __future__ import annotations

import json
from dataclasses import asdict

import numpy as np
import pandas as pd
import streamlit as st

from config_loader import MODEL_VERSION
from experiments import (
    SENSITIVITY_PARAMETERS,
    compare_scenarios,
    run_sensitivity_analysis,
    sensitivity_stability_summary,
)
from simulation import SimulationConfig, run_simulation
from tasks import TASK_TYPE_PROFILES, normalize_task_mix


# Week 1: preset scenarios. Each preset is a partial set of sidebar values.
PRESET_SCENARIOS: dict[str, dict[str, object]] = {
    "High-trust / high-reliability": {
        "trust_in_ai": 85,
        "ai_reliability": 90,
        "ai_support_level": 80,
        "dashboard_quality": 80,
        "effort_management": 70,
        "skills_knowledge_coordination": 72,
        "task_strategy": 72,
    },
    "Over-trust / low-reliability": {
        "trust_in_ai": 88,
        "ai_reliability": 45,
        "ai_support_level": 80,
        "dashboard_quality": 60,
        "effort_management": 60,
        "skills_knowledge_coordination": 58,
        "task_strategy": 58,
    },
    "Strong-process / weak-AI": {
        "trust_in_ai": 50,
        "ai_reliability": 55,
        "ai_support_level": 35,
        "dashboard_quality": 45,
        "effort_management": 82,
        "skills_knowledge_coordination": 82,
        "task_strategy": 80,
    },
    "Weak-process / strong-AI": {
        "trust_in_ai": 75,
        "ai_reliability": 88,
        "ai_support_level": 85,
        "dashboard_quality": 82,
        "effort_management": 45,
        "skills_knowledge_coordination": 45,
        "task_strategy": 45,
    },
}

MIX_KEYS = {
    "feature": "mix_feature",
    "bug": "mix_bug",
    "refactor": "mix_refactor",
    "spike": "mix_spike",
}


def normalize_percent(value: int) -> float:
    return value / 100.0


def comparison_delta(ai_value: float, baseline_value: float, inverse: bool = False) -> str:
    delta = ai_value - baseline_value
    if inverse:
        delta = baseline_value - ai_value
    return f"{delta:.2f}"


def current_task_mix() -> dict[str, float]:
    return {
        task_type: float(st.session_state[key]) for task_type, key in MIX_KEYS.items()
    }


def apply_preset(preset_name: str) -> None:
    preset = PRESET_SCENARIOS.get(preset_name, {})
    for key, value in preset.items():
        st.session_state[key] = value


def build_config_from_sidebar() -> SimulationConfig:
    return SimulationConfig(
        team_size=st.session_state["team_size"],
        number_of_sprints=st.session_state["number_of_sprints"],
        number_of_tasks=st.session_state["number_of_tasks"],
        task_type=st.session_state["task_type"],
        task_mix=normalize_task_mix(current_task_mix()),
        ai_support_level=normalize_percent(st.session_state["ai_support_level"]),
        trust_in_ai=normalize_percent(st.session_state["trust_in_ai"]),
        ai_reliability=normalize_percent(st.session_state["ai_reliability"]),
        effort_management=normalize_percent(st.session_state["effort_management"]),
        skills_knowledge_coordination=normalize_percent(st.session_state["skills_knowledge_coordination"]),
        task_strategy=normalize_percent(st.session_state["task_strategy"]),
        female_proportion=normalize_percent(st.session_state["female_proportion"]),
        team_engagement_baseline=normalize_percent(st.session_state["team_engagement_baseline"]),
        consequentiality=normalize_percent(st.session_state["consequentiality"]),
        task_complexity=normalize_percent(st.session_state["task_complexity"]),
        dashboard_quality=normalize_percent(st.session_state["dashboard_quality"]),
        collective_memory=normalize_percent(st.session_state["collective_memory"]),
        collective_attention=normalize_percent(st.session_state["collective_attention"]),
        collective_reasoning=normalize_percent(st.session_state["collective_reasoning"]),
        dependency_density=normalize_percent(st.session_state["dependency_density"]),
        enable_rework=st.session_state["enable_rework"],
        enable_sprint_phases=st.session_state["enable_sprint_phases"],
        random_seed=int(st.session_state["random_seed"]),
    )


@st.cache_data(show_spinner=False)
def cached_run_simulation(config_dict: dict, use_ai: bool) -> dict:
    config = SimulationConfig(**config_dict)
    return run_simulation(config, use_ai=use_ai)


@st.cache_data(show_spinner="Running Monte Carlo experiments...")
def cached_compare_scenarios(config_dict: dict, repetitions: int) -> dict:
    config = SimulationConfig(**config_dict)
    return compare_scenarios(config, repetitions=repetitions)


@st.cache_data(show_spinner="Running sensitivity analysis...")
def cached_sensitivity_analysis(
    config_dict: dict,
    parameter_name: str,
    values_tuple: tuple[float, ...],
    repetitions: int,
    use_ai: bool,
) -> pd.DataFrame:
    config = SimulationConfig(**config_dict)
    return run_sensitivity_analysis(
        base_config=config,
        parameter_name=parameter_name,
        values=list(values_tuple),
        repetitions=repetitions,
        use_ai=use_ai,
    )


def single_run_json(with_ai: dict, without_ai: dict) -> str:
    payload = {
        "model_version": with_ai.get("model_version", MODEL_VERSION),
        "config": with_ai["config"],
        "with_ai": {
            "summary": with_ai["summary"],
            "results": with_ai["results"].to_dict(orient="records"),
        },
        "without_ai": {
            "summary": without_ai["summary"],
            "results": without_ai["results"].to_dict(orient="records"),
        },
    }
    return json.dumps(payload, indent=2, default=str)


def render_summary_metrics(with_ai: dict, without_ai: dict) -> None:
    st.subheader("Summary Metrics")
    metric_columns = st.columns(4)
    metric_columns[0].metric(
        "Average Velocity",
        f"{with_ai['summary']['average_velocity']:.2f}",
        comparison_delta(with_ai["summary"]["average_velocity"], without_ai["summary"]["average_velocity"]),
    )
    metric_columns[1].metric(
        "Task Completion Rate (%)",
        f"{with_ai['summary']['completion_rate']:.2f}",
        comparison_delta(with_ai["summary"]["completion_rate"], without_ai["summary"]["completion_rate"]),
    )
    metric_columns[2].metric(
        "Defect Rate (%)",
        f"{with_ai['summary']['defect_rate']:.2f}",
        comparison_delta(with_ai["summary"]["defect_rate"], without_ai["summary"]["defect_rate"], inverse=True),
    )
    metric_columns[3].metric(
        "Decision Quality (%)",
        f"{with_ai['summary']['decision_quality']:.2f}",
        comparison_delta(with_ai["summary"]["decision_quality"], without_ai["summary"]["decision_quality"]),
    )

    metric_columns = st.columns(4)
    metric_columns[0].metric(
        "Collective Intelligence Score",
        f"{with_ai['summary']['collective_intelligence']:.2f}",
        comparison_delta(with_ai["summary"]["collective_intelligence"], without_ai["summary"]["collective_intelligence"]),
    )
    metric_columns[1].metric(
        "Trust Calibration (%)",
        f"{with_ai['summary']['trust_calibration']:.2f}",
        comparison_delta(with_ai["summary"]["trust_calibration"], without_ai["summary"]["trust_calibration"]),
    )
    metric_columns[2].metric(
        "Team Effectiveness Score",
        f"{with_ai['summary']['team_effectiveness']:.2f}",
        comparison_delta(with_ai["summary"]["team_effectiveness"], without_ai["summary"]["team_effectiveness"]),
    )
    metric_columns[3].metric(
        "AI Benefit Score",
        f"{with_ai['summary']['ai_benefit']:.2f}",
        f"{with_ai['summary']['ai_benefit']:.2f}",
    )

    metric_columns = st.columns(4)
    metric_columns[0].metric(
        "Team Viability (%)",
        f"{with_ai['summary']['team_viability']:.2f}",
        comparison_delta(with_ai["summary"]["team_viability"], without_ai["summary"]["team_viability"]),
    )
    metric_columns[1].metric(
        "Member Sustainability (%)",
        f"{with_ai['summary']['member_sustainability']:.2f}",
        comparison_delta(
            with_ai["summary"]["member_sustainability"],
            without_ai["summary"]["member_sustainability"],
        ),
    )
    metric_columns[2].metric(
        "Consequentiality (%)",
        f"{with_ai['summary']['consequentiality']:.2f}",
        comparison_delta(with_ai["summary"]["consequentiality"], without_ai["summary"]["consequentiality"]),
    )
    metric_columns[3].metric(
        "Overload Pressure (%)",
        f"{with_ai['summary']['overload_pressure']:.2f}",
        comparison_delta(
            with_ai["summary"]["overload_pressure"],
            without_ai["summary"]["overload_pressure"],
            inverse=True,
        ),
    )

    st.caption("Backlog realism and workflow metrics (Weeks 2-3)")
    backlog_columns = st.columns(4)
    backlog_columns[0].metric(
        "Carry-Over Rate (%)",
        f"{with_ai['summary']['carry_over_rate']:.2f}",
        comparison_delta(with_ai["summary"]["carry_over_rate"], without_ai["summary"]["carry_over_rate"], inverse=True),
    )
    backlog_columns[1].metric(
        "Blocked Tasks (sum)",
        f"{with_ai['summary']['blocked_tasks']:.0f}",
        comparison_delta(with_ai["summary"]["blocked_tasks"], without_ai["summary"]["blocked_tasks"], inverse=True),
    )
    backlog_columns[2].metric(
        "Rework Created (sum)",
        f"{with_ai['summary']['rework_created']:.0f}",
        comparison_delta(with_ai["summary"]["rework_created"], without_ai["summary"]["rework_created"], inverse=True),
    )
    backlog_columns[3].metric(
        "Defects Caught in Review (sum)",
        f"{with_ai['summary']['defects_caught_in_review']:.0f}",
    )


def render_single_run_tab(with_ai: dict, without_ai: dict) -> None:
    ai_results = with_ai["results"]
    baseline_results = without_ai["results"]
    comparison_results = pd.concat([ai_results, baseline_results], ignore_index=True)

    render_summary_metrics(with_ai, without_ai)

    st.subheader("Collective Intelligence Subcomponents")
    ci_columns = st.columns(4)
    ci_columns[0].metric("Transactive Memory", f"{with_ai['summary']['transactive_memory']:.2f}")
    ci_columns[1].metric("Shared Attention", f"{with_ai['summary']['shared_attention']:.2f}")
    ci_columns[2].metric("Shared Reasoning", f"{with_ai['summary']['shared_reasoning']:.2f}")
    ci_columns[3].metric("Social Sensitivity", f"{with_ai['summary']['social_sensitivity']:.2f}")

    process_columns = st.columns(4)
    process_columns[0].metric("Participation Balance", f"{with_ai['summary']['participation_balance']:.2f}")
    process_columns[1].metric("Team Engagement", f"{with_ai['summary']['team_engagement']:.2f}")
    process_columns[2].metric("Skill Diversity", f"{with_ai['summary']['skill_diversity']:.2f}")
    process_columns[3].metric("Age Diversity", f"{with_ai['summary']['age_diversity']:.2f}")

    predictor_columns = st.columns(3)
    predictor_columns[0].metric("Effort-Related Process", f"{with_ai['summary']['effort_management']:.2f}")
    predictor_columns[1].metric("Knowledge / Skills Process", f"{with_ai['summary']['skills_knowledge_coordination']:.2f}")
    predictor_columns[2].metric("Strategy Updating Process", f"{with_ai['summary']['task_strategy']:.2f}")

    st.subheader("Collective Intelligence Subcomponents Over Time")
    ci_long = with_ai["ci_components"]
    if not ci_long.empty:
        component_columns = [
            "transactive_memory",
            "shared_attention",
            "shared_reasoning",
            "social_sensitivity",
            "participation_balance",
            "transactive_coordination",
            "team_engagement",
            "skill_diversity",
        ]
        ci_subcomponent_chart = ci_long.set_index("Sprint")[
            [column for column in component_columns if column in ci_long.columns]
        ]
        st.line_chart(ci_subcomponent_chart)

    st.subheader("Sprint Trends")
    velocity_chart = comparison_results.pivot(index="Sprint", columns="Scenario", values="Sprint Velocity")
    st.write("Sprint velocity over time")
    st.line_chart(velocity_chart)

    st.write("Team viability over time")
    st.line_chart(comparison_results.pivot(index="Sprint", columns="Scenario", values="Team Viability"))

    st.write("Member sustainability over time")
    st.line_chart(comparison_results.pivot(index="Sprint", columns="Scenario", values="Member Sustainability"))

    st.write("Overload pressure over time")
    st.line_chart(comparison_results.pivot(index="Sprint", columns="Scenario", values="Overload Pressure"))

    st.write("Team effectiveness over time")
    st.line_chart(comparison_results.pivot(index="Sprint", columns="Scenario", values="Team Effectiveness Score"))

    st.write("Trust calibration over time")
    st.line_chart(comparison_results.pivot(index="Sprint", columns="Scenario", values="Trust Calibration"))

    st.subheader("Backlog Realism: Planned vs Completed and Carry-Over")
    backlog_chart = ai_results.set_index("Sprint")[
        [column for column in ["Planned Points", "Completed Points", "Carry-Over Points"] if column in ai_results]
    ]
    st.bar_chart(backlog_chart)

    st.subheader("Sprint-by-Sprint Results")
    st.dataframe(comparison_results, width="stretch")

    st.subheader("Export single-run results")
    export_columns = st.columns(2)
    export_columns[0].download_button(
        label="Download results CSV",
        data=comparison_results.to_csv(index=False),
        file_name="single_run_results.csv",
        mime="text/csv",
    )
    export_columns[1].download_button(
        label="Download results JSON",
        data=single_run_json(with_ai, without_ai),
        file_name="single_run_results.json",
        mime="application/json",
    )

    st.subheader("Team Profile Used in the Simulation")
    st.dataframe(with_ai["team"], width="stretch")


def render_experiments_tab(config: SimulationConfig) -> None:
    st.subheader("Monte Carlo Experiments")
    st.write(
        "Run many stochastic replications to compare distributions instead of relying on a single random seed."
    )

    repetitions = st.slider("Repetitions per scenario", min_value=20, max_value=500, value=100, step=10)
    run_button = st.button("Run Monte Carlo comparison", type="primary")

    if not run_button:
        st.info("Click the button to run experiments. Results are cached for the same parameters.")
        return

    comparison = cached_compare_scenarios(asdict(config), repetitions=repetitions)
    with_ai_stats = comparison["with_ai"]["statistics"]
    without_ai_stats = comparison["without_ai"]["statistics"]
    scenario_comparison = comparison["comparison"]

    st.write("With AI support — summary statistics")
    st.dataframe(with_ai_stats, width="stretch")

    st.write("Without AI support — summary statistics")
    st.dataframe(without_ai_stats, width="stretch")

    st.write("Scenario comparison (mean values)")
    st.dataframe(scenario_comparison, width="stretch")

    chart_df = scenario_comparison.set_index("Metric")[["With AI Mean", "Without AI Mean"]]
    st.write("Mean outcomes by scenario")
    st.bar_chart(chart_df)

    st.subheader("Export Monte Carlo results")
    export_columns = st.columns(3)
    export_columns[0].download_button(
        label="With-AI raw runs (CSV)",
        data=comparison["with_ai"]["results"].to_csv(index=False),
        file_name="monte_carlo_with_ai.csv",
        mime="text/csv",
    )
    export_columns[1].download_button(
        label="Without-AI raw runs (CSV)",
        data=comparison["without_ai"]["results"].to_csv(index=False),
        file_name="monte_carlo_without_ai.csv",
        mime="text/csv",
    )
    comparison_payload = {
        "model_version": MODEL_VERSION,
        "repetitions": repetitions,
        "comparison": scenario_comparison.to_dict(orient="records"),
        "with_ai_statistics": with_ai_stats.to_dict(orient="records"),
        "without_ai_statistics": without_ai_stats.to_dict(orient="records"),
    }
    export_columns[2].download_button(
        label="Comparison (JSON)",
        data=json.dumps(comparison_payload, indent=2, default=str),
        file_name="monte_carlo_comparison.json",
        mime="application/json",
    )


def render_sensitivity_tab(config: SimulationConfig) -> None:
    st.subheader("Sensitivity Analysis")
    st.write("Vary one parameter and observe how average outcomes change across repeated runs.")

    parameter_name = st.selectbox(
        "Parameter to vary",
        options=list(SENSITIVITY_PARAMETERS.keys()),
        format_func=lambda key: SENSITIVITY_PARAMETERS[key],
    )
    min_value = st.slider("Minimum value (%)", 0, 100, 20)
    max_value = st.slider("Maximum value (%)", 0, 100, 90)
    steps = st.slider("Number of steps", 3, 12, 6)
    repetitions = st.slider("Repetitions per value", 10, 100, 25, step=5)
    use_ai = st.toggle("Use AI support scenario", value=True)
    run_button = st.button("Run sensitivity analysis", type="primary")

    if not run_button:
        st.info("Choose a parameter range and click the button to run the analysis.")
        return

    if min_value >= max_value:
        st.error("Minimum value must be lower than maximum value.")
        return

    values = tuple(round(value, 3) for value in np.linspace(min_value / 100.0, max_value / 100.0, steps))

    sensitivity_df = cached_sensitivity_analysis(
        asdict(config),
        parameter_name,
        values,
        repetitions,
        use_ai,
    )
    st.dataframe(sensitivity_df, width="stretch")

    chart_columns = [
        "team_effectiveness_mean",
        "collective_intelligence_mean",
        "team_viability_mean",
        "member_sustainability_mean",
        "defect_rate_mean",
        "trust_calibration_mean",
        "carry_over_rate_mean",
        "rework_created_mean",
    ]
    chart_df = sensitivity_df.set_index("value_percent")[[column for column in chart_columns if column in sensitivity_df]]
    st.write("Average outcomes across parameter values")
    st.line_chart(chart_df)

    st.subheader("Sensitivity-stability summary")
    st.write(
        "Higher stability means the outcome changes little across the swept parameter range "
        "(less sensitive); lower stability means the parameter strongly drives that outcome."
    )
    stability_df = sensitivity_stability_summary(sensitivity_df)
    st.dataframe(stability_df, width="stretch")

    st.subheader("Export sensitivity results")
    export_columns = st.columns(2)
    export_columns[0].download_button(
        label="Sensitivity sweep (CSV)",
        data=sensitivity_df.to_csv(index=False),
        file_name=f"sensitivity_{parameter_name}.csv",
        mime="text/csv",
    )
    export_columns[1].download_button(
        label="Stability summary (CSV)",
        data=stability_df.to_csv(index=False),
        file_name=f"sensitivity_stability_{parameter_name}.csv",
        mime="text/csv",
    )


def render_assumptions_tab() -> None:
    st.subheader("Model assumptions")
    st.markdown(
        """
        These are **transparent simulation assumptions**, not empirical effect sizes
        estimated from Scrum datasets. The model integrates two literatures:
        Riedl et al. (2021) for predictor items and Kommol, Riedl & Woolley (2025) for
        organizing them into collective memory, attention, and reasoning.
        """
    )

    st.markdown("#### Process assumptions vs attribute assumptions")
    st.table(
        pd.DataFrame(
            [
                {
                    "Kind": "Process assumption",
                    "Examples": "Effort-related process, knowledge/skills process, strategy updating process, sprint phases",
                    "Interpretation": "Team behaviors / ways of working that can be coached and improved.",
                },
                {
                    "Kind": "Attribute assumption",
                    "Examples": "Individual skill, social sensitivity, age, gender composition",
                    "Interpretation": "Relatively stable member characteristics aggregated to the team.",
                },
                {
                    "Kind": "Emergent state",
                    "Examples": "Collective memory/attention/reasoning, team engagement, viability, sustainability",
                    "Interpretation": "States that evolve sprint-to-sprint via the feedback loop.",
                },
            ]
        )
    )

    st.markdown("#### Female proportion as a proxy")
    st.info(
        "Female proportion is modeled **only as a proxy pathway through social perceptiveness** "
        "when social perceptiveness is not directly measured (Woolley et al., 2010). It is not a "
        "biological causal claim. If social perceptiveness is measured directly, prefer that input."
    )

    st.markdown("#### Externalized weights")
    st.write(
        f"Model version **{MODEL_VERSION}**. CI weights, the age-diversity penalty, and the "
        "team-effectiveness layer are loaded from `config/weights.yaml`, so they can be tuned "
        "without editing the Python source."
    )

    st.markdown("#### Roles (Week 4)")
    st.write(
        "Roles act as small behavioral modifiers: a Product Owner sharpens strategy and shared "
        "purpose, a Scrum Master improves coordination/participation and relieves blockers, "
        "Testers raise in-review defect detection, and Developers add a small delivery nudge."
    )


def render_sidebar() -> None:
    with st.sidebar:
        st.header("Preset scenarios")
        preset_choice = st.selectbox("Choose a preset", options=list(PRESET_SCENARIOS.keys()))
        if st.button("Apply preset"):
            apply_preset(preset_choice)
            st.rerun()

        st.header("Simulation Parameters")
        st.session_state["team_size"] = st.slider("Team size", 3, 12, st.session_state["team_size"])
        st.session_state["number_of_sprints"] = st.slider("Number of sprints", 1, 20, st.session_state["number_of_sprints"])
        st.session_state["number_of_tasks"] = st.slider("Number of tasks", 10, 200, st.session_state["number_of_tasks"], step=5)

        with st.expander("Backlog mix (Week 2)", expanded=True):
            st.caption("Set the relative proportion of each task type. Values are normalized to 100%.")
            st.session_state["mix_feature"] = st.slider("Feature %", 0, 100, st.session_state["mix_feature"])
            st.session_state["mix_bug"] = st.slider("Bug %", 0, 100, st.session_state["mix_bug"])
            st.session_state["mix_refactor"] = st.slider("Refactor %", 0, 100, st.session_state["mix_refactor"])
            st.session_state["mix_spike"] = st.slider("Spike %", 0, 100, st.session_state["mix_spike"])
            mix_total = (
                st.session_state["mix_feature"]
                + st.session_state["mix_bug"]
                + st.session_state["mix_refactor"]
                + st.session_state["mix_spike"]
            )
            if mix_total == 100:
                st.success(f"Mix total: {mix_total}%")
            elif mix_total == 0:
                st.warning("Mix total is 0%; defaulting to 100% features.")
            else:
                normalized = normalize_task_mix(current_task_mix())
                st.info(
                    f"Mix total is {mix_total}%. It will be normalized to 100%: "
                    + ", ".join(f"{k} {round(v * 100)}%" for k, v in normalized.items())
                )

        with st.expander("Workflow realism (Week 3)", expanded=False):
            st.session_state["dependency_density"] = st.slider(
                "Dependency density (%)",
                0,
                100,
                st.session_state["dependency_density"],
                help="Share of tasks that depend on an upstream task and can be blocked.",
            )
            st.session_state["enable_rework"] = st.toggle(
                "Defect rework spillover",
                value=st.session_state["enable_rework"],
                help="Shipped defects create follow-up fix tasks that appear in later sprints.",
            )
            st.session_state["enable_sprint_phases"] = st.toggle(
                "Sprint-phase modifiers",
                value=st.session_state["enable_sprint_phases"],
                help="Planning affects strategy, review catches defects, retrospective scales learning.",
            )

        task_type_options = list(TASK_TYPE_PROFILES.keys())
        if st.session_state["task_type"] not in task_type_options:
            st.session_state["task_type"] = "feature"
        st.session_state["task_type"] = st.selectbox(
            "Primary task type (single-type fallback)",
            options=task_type_options,
            index=task_type_options.index(st.session_state["task_type"]),
            format_func=lambda key: str(TASK_TYPE_PROFILES[key]["label"]),
        )
        st.session_state["ai_support_level"] = st.slider("AI support level", 0, 100, st.session_state["ai_support_level"])
        st.session_state["trust_in_ai"] = st.slider("Trust in AI", 0, 100, st.session_state["trust_in_ai"])
        st.session_state["ai_reliability"] = st.slider("AI reliability", 0, 100, st.session_state["ai_reliability"])
        st.session_state["task_complexity"] = st.slider("Task complexity", 0, 100, st.session_state["task_complexity"])
        st.session_state["dashboard_quality"] = st.slider("Dashboard quality", 0, 100, st.session_state["dashboard_quality"])
        with st.expander("Team & Process", expanded=False):
            st.session_state["effort_management"] = st.slider(
                "Effort-related process",
                0,
                100,
                st.session_state["effort_management"],
                help="Riedl/Hackman process measure: how the team sustains and allocates effort during work.",
            )
            st.session_state["skills_knowledge_coordination"] = st.slider(
                "Knowledge / skills process",
                0,
                100,
                st.session_state["skills_knowledge_coordination"],
                help=(
                    "Team process for matching knowledge and skills to task contributions. "
                    "This is distinct from individual member skill levels."
                ),
            )
            st.session_state["task_strategy"] = st.slider(
                "Strategy updating process",
                0,
                100,
                st.session_state["task_strategy"],
                help="Team process for managing and updating the work strategy, not a static strategy attribute.",
            )
            st.session_state["female_proportion"] = st.slider(
                "Female proportion",
                0,
                100,
                st.session_state["female_proportion"],
                help=(
                    "Modeled as a proxy pathway through social perceptiveness when social perceptiveness "
                    "is not directly measured; not a biological causal claim."
                ),
            )
            st.session_state["team_engagement_baseline"] = st.slider(
                "Initial team engagement",
                0,
                100,
                st.session_state["team_engagement_baseline"],
                help="Team-level engagement, not individual engagement.",
            )
            st.session_state["consequentiality"] = st.slider(
                "Consequentiality / shared purpose",
                0,
                100,
                st.session_state["consequentiality"],
                help="Hackman/Wageman-style driver: the work feels consequential and creates shared purpose.",
            )
            st.caption(
                "CI systems follow the memory-attention-reasoning framing. "
                "Collective/shared memory is the baseline store of team knowledge; "
                "transactive memory is the computed mechanism for who knows what."
            )
            st.session_state["collective_memory"] = st.slider(
                "Collective / shared memory",
                0,
                100,
                st.session_state["collective_memory"],
                help=(
                    "Baseline retained team knowledge. In the model it is operationalized "
                    "through transactive memory: who knows what, specialization, and skills/knowledge coordination."
                ),
            )
            st.session_state["collective_attention"] = st.slider(
                "Collective focus of attention",
                0,
                100,
                st.session_state["collective_attention"],
                help="Shared focus on sprint goals, effort allocation, and visible coordination demands.",
            )
            st.session_state["collective_reasoning"] = st.slider(
                "Collective reasoning",
                0,
                100,
                st.session_state["collective_reasoning"],
                help="Joint interpretation, task strategy, problem solving, and decision quality.",
            )
        st.session_state["random_seed"] = st.number_input(
            "Random seed",
            min_value=0,
            max_value=999999,
            value=st.session_state["random_seed"],
            step=1,
        )


st.set_page_config(page_title="Agile AI Simulator", layout="wide")

st.title("Agile AI Simulator")
st.caption(f"Model version {MODEL_VERSION}")
st.write(
    """
    This academic prototype simulates an agile team working across multiple sprints
    and compares outcomes with and without AI support. Collective Intelligence is
    modeled through collective/shared memory, shared attention, shared reasoning,
    social sensitivity, participation balance, team engagement, diversity, and trust calibration.
    """
)

defaults = {
    "team_size": 6,
    "number_of_sprints": 8,
    "number_of_tasks": 60,
    "task_type": "feature",
    "mix_feature": 50,
    "mix_bug": 25,
    "mix_refactor": 15,
    "mix_spike": 10,
    "ai_support_level": 70,
    "trust_in_ai": 65,
    "ai_reliability": 78,
    "effort_management": 65,
    "skills_knowledge_coordination": 65,
    "task_strategy": 65,
    "female_proportion": 50,
    "team_engagement_baseline": 65,
    "consequentiality": 65,
    "task_complexity": 58,
    "dashboard_quality": 70,
    "collective_memory": 62,
    "collective_attention": 60,
    "collective_reasoning": 64,
    "dependency_density": 25,
    "enable_rework": True,
    "enable_sprint_phases": True,
    "random_seed": 42,
}
for key, value in defaults.items():
    st.session_state.setdefault(key, value)

render_sidebar()

config = build_config_from_sidebar()
config_dict = asdict(config)

with_ai = cached_run_simulation(config_dict, use_ai=True)
without_ai = cached_run_simulation(config_dict, use_ai=False)

single_run_tab, experiments_tab, sensitivity_tab, assumptions_tab = st.tabs(
    ["Single Run", "Monte Carlo Experiments", "Sensitivity Analysis", "Assumptions"]
)

with single_run_tab:
    render_single_run_tab(with_ai, without_ai)

with experiments_tab:
    render_experiments_tab(config)

with sensitivity_tab:
    render_sensitivity_tab(config)

with assumptions_tab:
    render_assumptions_tab()
