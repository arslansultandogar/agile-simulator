"""Generate thesis figures from the real simulation results in results/."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

OUT = Path("figures"); OUT.mkdir(exist_ok=True)
R = Path("results")
plt.rcParams.update({"font.size": 9, "figure.dpi": 200,
                     "axes.spines.top": False, "axes.spines.right": False})
INK, ACC, WARN = "#333333", "#4C72B0", "#C44E52"

# --- Fig 1: CI levels -------------------------------------------------------
d = pd.read_csv(R / "exp1_ci_levels.csv")
fig, ax = plt.subplots(1, 3, figsize=(8.2, 2.7))
x = range(len(d))
labels = ["Low\n(40%)", "Default\n(62/60/64%)", "High\n(80%)"]
for a, (col, sd, ttl) in zip(ax, [
        ("Completion", "Completion SD", "Task completion rate (%)"),
        ("Defect rate", "Defect SD", "Defect rate (%)"),
        ("Effectiveness", "Effectiveness SD", "Team effectiveness")]):
    a.bar(x, d[col], yerr=d[sd], capsize=3, color=ACC, width=.6, alpha=.85)
    a.set_xticks(list(x)); a.set_xticklabels(labels, fontsize=7.5)
    a.set_title(ttl, fontsize=9)
    a.set_ylim(0, max(d[col]) * 1.35)
fig.suptitle("Experiment 1: outcomes by collective-intelligence baseline (N=200)", fontsize=10)
fig.tight_layout(); fig.savefig(OUT / "fig_exp1_ci_levels.png", bbox_inches="tight"); plt.close(fig)

# --- Fig 2: backlog composition --------------------------------------------
d = pd.read_csv(R / "exp3_task_types.csv")
short = ["Feature", "Bug fix", "Refactor", "Spike", "Default mix"]
fig, ax = plt.subplots(1, 3, figsize=(8.2, 2.7))
for a, (col, ttl) in zip(ax, [("Completion", "Completion rate (%)"),
                              ("Carry-over rate", "Carry-over rate (%)"),
                              ("Effectiveness", "Team effectiveness")]):
    cols = [WARN if s == "Spike" else ACC for s in short]
    a.bar(range(len(d)), d[col], color=cols, width=.62, alpha=.85)
    a.set_xticks(range(len(d))); a.set_xticklabels(short, rotation=35, ha="right", fontsize=7.5)
    a.set_title(ttl, fontsize=9)
    lo, hi = d[col].min(), d[col].max()
    a.set_ylim(lo - (hi - lo) * .8, hi + (hi - lo) * .35)
fig.suptitle("Experiment 3: outcomes by backlog composition (N=200)", fontsize=10)
fig.tight_layout(); fig.savefig(OUT / "fig_exp3_backlog.png", bbox_inches="tight"); plt.close(fig)

# --- Fig 3: process vs AI ---------------------------------------------------
d = pd.read_csv(R / "exp4_process_vs_ai.csv")
names = ["Default", "S3: strong process\nweak AI", "S4: weak process\nstrong AI"]
fig, ax = plt.subplots(1, 4, figsize=(8.6, 2.8))
for a, (col, sd, ttl) in zip(ax, [
        ("CI score", "CI SD", "Collective intelligence"),
        ("Decision quality", "DQ SD", "Decision quality"),
        ("Effectiveness", "Eff SD", "Team effectiveness"),
        ("Sustainability", "Sustain SD", "Member sustainability")]):
    a.bar(range(3), d[col], yerr=d[sd], capsize=3,
          color=["#999999", ACC, WARN], width=.6, alpha=.85)
    a.set_xticks(range(3)); a.set_xticklabels(names, fontsize=7, rotation=20, ha="right")
    a.set_title(ttl, fontsize=9)
    lo, hi = d[col].min(), d[col].max()
    a.set_ylim(lo - (hi - lo) * 1.2, hi + (hi - lo) * .5)
fig.suptitle("Experiment 4: strong process vs strong AI (N=200)", fontsize=10)
fig.tight_layout(); fig.savefig(OUT / "fig_exp4_process_vs_ai.png", bbox_inches="tight"); plt.close(fig)

# --- Fig 4: sensitivity importance ranking ---------------------------------
d = pd.read_csv(R / "sensitivity_importance_ranking.csv").sort_values("Range")
pretty = {"effort_management": "Effort-related process",
          "dashboard_quality": "Dashboard quality",
          "task_strategy": "Strategy-updating process",
          "skills_knowledge_coordination": "Knowledge/skills process",
          "collective_reasoning": "Collective reasoning",
          "trust_in_ai": "Trust in AI",
          "ai_reliability": "AI reliability",
          "dependency_density": "Dependency density"}
fig, a = plt.subplots(figsize=(5.6, 3.0))
cols = [WARN if p in ("ai_reliability", "trust_in_ai", "dashboard_quality") else ACC
        for p in d["Parameter"]]
a.barh([pretty[p] for p in d["Parameter"]], d["Range"], color=cols, alpha=.85)
a.set_xlabel("Swing in mean team effectiveness across sweep (20%–90%)")
a.set_title("Parameter importance: team process dominates AI parameters", fontsize=9.5)
for i, v in enumerate(d["Range"]):
    a.text(v + .06, i, f"{v:.2f}", va="center", fontsize=7.5)
a.set_xlim(0, d["Range"].max() * 1.18)
fig.tight_layout(); fig.savefig(OUT / "fig_sensitivity_ranking.png", bbox_inches="tight"); plt.close(fig)

# --- Fig 5: AI benefit vs reliability (the crossing point) -----------------
d = pd.read_csv(R / "ai_reliability_crossing.csv")
v20 = pd.read_csv(Path("results_v20") / "ai_reliability_crossing.csv")
fig, (a1, a2) = plt.subplots(1, 2, figsize=(8.0, 2.9))
a1.plot(d["ai_reliability"] * 100, d["eff_delta"], "o-", color=ACC, ms=3.5, label="model v2.1")
a1.fill_between(d["ai_reliability"] * 100, d["ci_low"], d["ci_high"], color=ACC, alpha=.18)
a1.plot(v20["ai_reliability"] * 100, v20["eff_delta"], "s--", color="#999999", ms=3,
        lw=1, label="model v2.0 (inert)")
a1.axhline(0, color=WARN, ls="--", lw=1)
a1.set_xlabel("Actual AI reliability (%)")
a1.set_ylabel("With-AI minus without-AI\neffectiveness")
a1.set_title("AI benefit crosses zero at ~48% reliability", fontsize=9.5)
a1.legend(fontsize=7, frameon=False)
a2.plot(d["ai_reliability"] * 100, d["trust_calibration"], "o-", color=ACC, ms=3.5,
        label="model v2.1")
a2.plot(v20["ai_reliability"] * 100, v20["trust_calibration"], "s--", color="#999999",
        ms=3, lw=1, label="model v2.0 (flat)")
a2.set_xlabel("Actual AI reliability (%)")
a2.set_ylabel("Trust calibration (%)")
a2.set_title("Calibration now tracks reliability", fontsize=9.5)
a2.legend(fontsize=7, frameon=False, loc="lower right")
fig.suptitle("Trust calibration and AI benefit under fixed high trust (85%)", fontsize=10)
fig.tight_layout(); fig.savefig(OUT / "fig_ai_reliability_crossing.png", bbox_inches="tight")
plt.close(fig)

# --- Fig 6: paired AI benefit distributions, S1 vs S2 ----------------------
s1 = pd.read_csv(R / "exp2_paired_S1_high_trust_high_reliability.csv")
s2 = pd.read_csv(R / "exp2_paired_S2_over_trust_low_reliability.csv")
fig, a = plt.subplots(figsize=(5.6, 3.0))
bins = 30
a.hist(s1["eff_delta"], bins=bins, alpha=.65, color=ACC, label="S1: calibrated trust, reliable AI")
a.hist(s2["eff_delta"], bins=bins, alpha=.65, color=WARN, label="S2: over-trust, unreliable AI")
a.axvline(0, color=INK, ls="--", lw=1)
a.axvline(s1["eff_delta"].mean(), color=ACC, lw=2)
a.axvline(s2["eff_delta"].mean(), color=WARN, lw=2)
a.set_xlabel("Paired AI benefit (with-AI minus without-AI effectiveness)")
a.set_ylabel("Runs")
a.set_title("Experiment 2: over-trust turns AI benefit negative (N=200)", fontsize=9.5)
a.legend(fontsize=7.5, frameon=False)
fig.tight_layout(); fig.savefig(OUT / "fig_exp2_paired_benefit.png", bbox_inches="tight")
plt.close(fig)

print("figures written:", sorted(p.name for p in OUT.glob("*.png")))
