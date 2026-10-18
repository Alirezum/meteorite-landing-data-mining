"""Figure 09: how the mass of recorded meteorites changed over time (finds vs falls)."""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from ..common import (
    GRID,
    INK,
    LAKE,
    MUTED,
    ORANGE,
    SALMON,
    TEAL,
    add_titles,
    clean_axis,
    save_figure,
    use_style,
)

FIGURE = "09_mass_by_decade.png"


def build(df: pd.DataFrame) -> plt.Figure:
    dated = df[(df["decade"] >= 1900) & df["decade"].notna() & (df["mass"] > 0)].copy()
    decades = sorted(dated["decade"].unique())
    x = np.arange(len(decades))

    def by_decade(sub: pd.DataFrame) -> pd.DataFrame:
        g = sub.groupby("decade")["mass"]
        return pd.DataFrame(
            {
                "q25": g.quantile(0.25).reindex(decades).to_numpy(),
                "med": g.median().reindex(decades).to_numpy(),
                "q75": g.quantile(0.75).reindex(decades).to_numpy(),
                "n": g.size().reindex(decades).to_numpy(),
                "small": sub["mass"].lt(100).groupby(sub["decade"]).mean().reindex(decades).to_numpy() * 100,
            }
        )

    found = by_decade(dated[~dated["is_fell"]])
    fell = by_decade(dated[dated["is_fell"]])

    fig = plt.figure(figsize=(13.6, 8.4))
    ax_a = fig.add_axes((0.065, 0.125, 0.575, 0.665))
    ax_b = fig.add_axes((0.725, 0.125, 0.235, 0.665))

    # --- panel A: median mass per decade with quartile bands -----------------
    ax_a.fill_between(x, found["q25"], found["q75"], color=SALMON, alpha=0.22, linewidth=0)
    ax_a.fill_between(x, fell["q25"], fell["q75"], color=LAKE, alpha=0.30, linewidth=0)
    ax_a.plot(x, found["med"], color=ORANGE, linewidth=2.4, marker="o", markersize=5, label="Found \u2014 median")
    ax_a.plot(x, fell["med"], color=TEAL, linewidth=2.4, marker="o", markersize=5, label="Fell \u2014 median")
    ax_a.set_yscale("log")
    ax_a.set_ylim(1.2, 2.2e5)
    ax_a.set_yticks([1e1, 1e2, 1e3, 1e4, 1e5], ["10 g", "100 g", "1 kg", "10 kg", "100 kg"])
    ax_a.set_xticks(x, [f"{d}s" for d in decades], rotation=45, ha="right", fontsize=9.5)
    ax_a.set_ylabel("Record mass (logarithmic scale)")
    ax_a.annotate(
        "median find: 13.0 kg",
        xy=(0, found["med"][0]),
        xytext=(0.0, 1.1e5),
        fontsize=10,
        color=INK,
        arrowprops=dict(arrowstyle="->", color=MUTED, linewidth=1),
    )
    ax_a.annotate(
        "10 g",
        xy=(7, found["med"][7]),
        xytext=(7.6, 4.5),
        fontsize=10,
        color=INK,
        arrowprops=dict(arrowstyle="->", color=MUTED, linewidth=1),
    )
    ax_a.annotate(
        "observed falls: 1.2\u20134.4 kg in every decade",
        xy=(9, fell["med"][9]),
        xytext=(4.1, 5e4),
        fontsize=10,
        color=TEAL,
        arrowprops=dict(arrowstyle="->", color=TEAL, linewidth=1),
    )
    ax_a.text(
        3.55,
        1.8,
        "systematic collecting starts",
        fontsize=9.5,
        color=MUTED,
        ha="center",
    )
    ax_a.axvline(6.5, color=GRID, linewidth=1, linestyle=(0, (4, 3)))
    ax_a.legend(loc="lower left", fontsize=10, handlelength=1.6)
    clean_axis(ax_a)
    ax_a.set_title("Median mass per record, by decade", pad=12)

    # --- panel B: share of records under 100 g -------------------------------
    ax_b.bar(x, found["small"], width=0.72, color=ORANGE, label="Found")
    ax_b.plot(x, fell["small"], color=TEAL, linewidth=2.2, marker="o", markersize=4.5, label="Fell")
    for xi, value in zip(x, found["small"], strict=True):
        ax_b.text(xi, value + 2.5, f"{value:.0f}", ha="center", va="bottom", fontsize=8.5, color=INK)
    ax_b.set_xticks(x, [f"{d}s" for d in decades], rotation=45, ha="right", fontsize=9.5)
    ax_b.set_ylim(0, 102)
    ax_b.set_yticks([0, 25, 50, 75, 100], ["0", "25", "50", "75", "100"])
    ax_b.set_ylabel("Share of the decade's records (%)")
    ax_b.legend(loc="center left", fontsize=10, handlelength=1.2)
    clean_axis(ax_b)
    ax_b.set_title("Records under 100 g", pad=12)

    add_titles(
        fig,
        "The modern flood of records is small stones \u2014 observed falls never changed",
        "Dated records 1900s\u20132010s with mass > 0 g, finds vs observed falls \u2022 left: median mass with interquartile band \u2022 right: share of records under 100 g",
        "Masses are individual recovered fragments, not single objects; 19 records with mass \u2264 0 g are excluded. The median find crashed from 13.0 kg (1900s) "
        "to 10 g (1970s) \u2014 a factor of ~1,300 \u2014 as systematic searching replaced chance finds, while the median observed fall stayed between 1.2 and 4.4 kg.",
    )
    return fig


def main(df: pd.DataFrame | None = None) -> str:
    use_style()
    if df is None:
        from ..common import load_landings

        df = load_landings()
    return str(save_figure(build(df), FIGURE))
