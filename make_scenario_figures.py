"""Generate demonstration-scenario figures from results_scenarios/.

Follows make_figures.py conventions (Agg backend, dpi 200, palette). Reads only
results_scenarios/ and writes only results_scenarios/figures/ - thesis outputs
in results/, results_v20/ and figures/ are never touched.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm
import numpy as np
import pandas as pd
from pathlib import Path

R = Path("results_scenarios")
OUT = R / "figures"; OUT.mkdir(exist_ok=True)
plt.rcParams.update({"font.size": 9, "figure.dpi": 200,
                     "axes.spines.top": False, "axes.spines.right": False})
INK, ACC, WARN = "#333333", "#4C72B0", "#C44E52"

summary = pd.read_csv(R / "paired_summary.csv")
n_paired = int(summary["n"].iloc[0])
A_KEY, B_KEY = "A_safety_critical_embedded", "B_large_scale_enterprise"
op_rel = 0.78  # Scenario A operating point (AI arm)
op_trust = 0.65

# --- Fig 1: paired AI benefit, Scenario A vs B ------------------------------
a = pd.read_csv(R / f"paired_{A_KEY}.csv")
b = pd.read_csv(R / f"paired_{B_KEY}.csv")
fig, ax = plt.subplots(figsize=(5.8, 3.1))
bins = np.linspace(min(a["eff_delta"].min(), b["eff_delta"].min()),
                   max(a["eff_delta"].max(), b["eff_delta"].max()), 31)
ax.hist(a["eff_delta"], bins=bins, alpha=.65, color=ACC, label="Scenario A: safety-critical embedded")
ax.hist(b["eff_delta"], bins=bins, alpha=.65, color=WARN, label="Scenario B: large-scale enterprise")
ax.axvline(0, color=INK, ls="--", lw=1)
ax.axvline(a["eff_delta"].mean(), color=ACC, lw=2)
ax.axvline(b["eff_delta"].mean(), color=WARN, lw=2)
ax.set_xlabel("Paired AI benefit (with-AI minus without-AI team effectiveness)")
ax.set_ylabel("Runs")
ax.set_title(f"Paired AI benefit by scenario (N={n_paired}, identical seeds)", fontsize=9.5)
ax.legend(fontsize=7.5, frameon=False)
fig.tight_layout(); fig.savefig(OUT / "fig_scenarios_paired_benefit.png", bbox_inches="tight"); plt.close(fig)

# --- Fig 2: Scenario A reliability sweep with zero crossing -----------------
cross = pd.read_csv(R / "sweep_zero_crossing_A.csv")
sweeps = {t: pd.read_csv(R / f"sweep_reliability_A_trust{int(round(t*100)):03d}.csv")
          for t in cross["trust_in_ai"]}
colors = {0.65: ACC, 0.85: WARN}
fig, (a1, a2) = plt.subplots(1, 2, figsize=(8.2, 3.0))
title_bits = []
for t, d in sweeps.items():
    c = colors.get(t, INK)
    x = d["ai_reliability"] * 100
    a1.plot(x, d["eff_delta"], "o-", color=c, ms=3.5, label=f"trust = {t:.2f}")
    a1.fill_between(x, d["ci_low"], d["ci_high"], color=c, alpha=.18)
    a2.plot(x, d["trust_calibration_with"], "o-", color=c, ms=3.5, label=f"trust = {t:.2f}")
    row = cross[cross["trust_in_ai"] == t].iloc[0]
    if row["n_crossings"] >= 1 and pd.notna(row["first_crossing_reliability"]):
        xc = float(row["first_crossing_reliability"]) * 100
        a1.axvline(xc, color=c, ls=":", lw=1.2)
        a1.annotate(f"crosses 0 at {xc:.1f}%", xy=(xc, 0), xytext=(xc + 2, a1.get_ylim()[0] * 0.15 if a1.get_ylim()[0] < 0 else 0.3),
                    fontsize=7, color=c)
        title_bits.append(f"t={t:.2f}: crosses at {xc:.0f}%")
    else:
        title_bits.append(f"t={t:.2f}: none")
a1.axhline(0, color=INK, ls="--", lw=1)
a1.axvline(op_rel * 100, color="#999999", lw=.8, ls="-.")
a1.set_xlabel("Actual AI reliability (%)")
a1.set_ylabel("Paired AI benefit\n(with-AI minus without-AI effectiveness)")
a1.set_title("Zero crossing - " + "; ".join(title_bits), fontsize=8.5)
a1.legend(fontsize=7, frameon=False)
a2.set_xlabel("Actual AI reliability (%)")
a2.set_ylabel("Trust calibration, with-AI arm (%)")
a2.set_title("Trust calibration vs. reliability", fontsize=9)
a2.legend(fontsize=7, frameon=False, loc="lower right")
fig.suptitle(f"Scenario A: AI benefit and calibration vs. reliability (N={int(next(iter(sweeps.values()))['n'].iloc[0])} paired per point)",
             fontsize=10)
fig.tight_layout(); fig.savefig(OUT / "fig_scenarios_reliability_sweep_A.png", bbox_inches="tight"); plt.close(fig)

# --- Fig 3: trust x reliability heat maps -----------------------------------
g = pd.read_csv(R / "grid_trust_x_reliability_A.csv")
n_cell = int(g["n"].iloc[0])
ben = g.pivot(index="trust_in_ai", columns="ai_reliability", values="eff_delta_mean").sort_index()
cal = g.pivot(index="trust_in_ai", columns="ai_reliability", values="trust_calibration_mean").sort_index()
xs = ben.columns.values * 100; ys = ben.index.values * 100
ext = [xs.min() - 2.5, xs.max() + 2.5, ys.min() - 2.5, ys.max() + 2.5]
vmax = float(np.nanmax(np.abs(ben.values)))
fig, (h1, h2) = plt.subplots(1, 2, figsize=(8.6, 3.5))
im1 = h1.imshow(ben.values, origin="lower", extent=ext, aspect="auto", cmap="RdBu",
                norm=TwoSlopeNorm(vmin=-vmax, vcenter=0.0, vmax=vmax))
XX, YY = np.meshgrid(xs, ys)
try:
    cs = h1.contour(XX, YY, ben.values, levels=[0.0], colors=INK, linewidths=1.2, linestyles="--")
    h1.clabel(cs, fmt={0.0: "benefit = 0"}, fontsize=7)
except Exception:
    pass
h1.plot([xs.min(), xs.max()], [xs.min(), xs.max()], color="#777777", lw=.8, ls=":")  # calibrated diagonal
h1.plot(op_rel * 100, op_trust * 100, marker="*", ms=10, color="#111111", mec="white", label="Scenario A operating point")
h1.set_xlabel("Actual AI reliability (%)"); h1.set_ylabel("Trust in AI (%)")
h1.set_title(f"Paired AI benefit (N={n_cell}/cell, common random numbers)", fontsize=8.5)
h1.legend(fontsize=6.5, frameon=False, loc="upper left")
fig.colorbar(im1, ax=h1, fraction=.046, pad=.03, label="with-AI minus without-AI effectiveness")
im2 = h2.imshow(cal.values, origin="lower", extent=ext, aspect="auto", cmap="viridis")
h2.plot([xs.min(), xs.max()], [xs.min(), xs.max()], color="white", lw=.8, ls=":")
h2.plot(op_rel * 100, op_trust * 100, marker="*", ms=10, color="white", mec="black")
h2.set_xlabel("Actual AI reliability (%)"); h2.set_ylabel("Trust in AI (%)")
h2.set_title("Trust calibration, with-AI arm (%)", fontsize=8.5)
fig.colorbar(im2, ax=h2, fraction=.046, pad=.03, label="trust calibration (%)")
fig.suptitle("Scenario A: trust x reliability surface (dotted diagonal = perfectly calibrated)", fontsize=10)
fig.tight_layout(); fig.savefig(OUT / "fig_scenarios_trust_x_reliability_A.png", bbox_inches="tight"); plt.close(fig)


# --- Fig 4: supplementary - support 0.70 vs 0.80, does a crossing re-emerge? --
sup_cross = R / "sweep_zero_crossing_A_support080.csv"
if sup_cross.exists():
    c70 = pd.read_csv(R / "sweep_zero_crossing_A.csv").set_index("trust_in_ai")
    c80 = pd.read_csv(sup_cross).set_index("trust_in_ai")
    dp_cross = R / "sweep_zero_crossing_A_support080_defproc.csv"
    cdp = pd.read_csv(dp_cross).set_index("trust_in_ai") if dp_cross.exists() else None
    GRN = "#55A868"
    def _status(c, t):
        r = c.loc[t]
        return f"crosses at {float(r['first_crossing_reliability'])*100:.0f}%" if r["n_crossings"] >= 1 else "none"
    fig, axes = plt.subplots(1, 2, figsize=(8.2, 3.0), sharey=True)
    for ax, t in zip(axes, (0.65, 0.85)):
        ttag = f"trust{int(round(t*100)):03d}"
        d70 = pd.read_csv(R / f"sweep_reliability_A_{ttag}.csv")
        d80 = pd.read_csv(R / f"sweep_reliability_A_support080_{ttag}.csv")
        curves = [(d70, ACC, "support 0.70 (main run)"), (d80, WARN, "support 0.80")]
        if cdp is not None:
            curves.append((pd.read_csv(R / f"sweep_reliability_A_support080_defproc_{ttag}.csv"), GRN, "support 0.80 + default process"))
        for d, c, lab in curves:
            x = d["ai_reliability"] * 100
            ax.plot(x, d["eff_delta"], "o-", color=c, ms=3.5, label=lab)
            ax.fill_between(x, d["ci_low"], d["ci_high"], color=c, alpha=.18)
        ax.axhline(0, color=INK, ls="--", lw=1)
        ax.set_xlabel("Actual AI reliability (%)")
        statuses = [("0.70", _status(c70, t)), ("0.80", _status(c80, t))] + \
                   ([("0.80+default process", _status(cdp, t))] if cdp is not None else [])
        st = ("no zero crossing in any variant" if all(v == "none" for _, v in statuses)
              else "; ".join(f"{k} {v}" for k, v in statuses))
        ax.set_title(f"trust = {t:.2f}  |  {st}", fontsize=8.5)
        ax.legend(fontsize=7, frameon=False, loc="lower right")
    axes[0].set_ylabel("Paired AI benefit\n(with-AI minus without-AI effectiveness)")
    n80 = int(d80["n"].iloc[0])
    what = "neither support level nor process profile creates" if cdp is not None else "AI support level does not create"
    fig.suptitle(f"Scenario A: {what} a negative-benefit region (N={n80} paired per point)", fontsize=10)
    fig.tight_layout(); fig.savefig(OUT / "fig_scenarios_reliability_sweep_A_support_compare.png", bbox_inches="tight"); plt.close(fig)

print("figures written:", sorted(p.name for p in OUT.glob("*.png")))
