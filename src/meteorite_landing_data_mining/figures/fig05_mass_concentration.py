"""Figure 05: how concentrated the total catalogued mass is (Pareto view)."""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from ..common import (
    BLUE,
    GRID,
    INK,
    MUTED,
    ORANGE,
    PALE,
    TEAL,
    add_titles,
    clean_axis,
    human_mass,
    save_figure,
    use_style,
)

FIGURE = "05_mass_concentration.png"


def build(df: pd.DataFrame) -> plt.Figure:
    pos = df[df["mass"] > 0].sort_values("mass", ascending=False).reset_index(drop=True)
    cumulative = pos["mass"].cumsum() / pos["mass"].sum() * 100
    ranks = np.arange(1, len(pos) + 1)
    n_50 = int((cumulative < 50).sum() + 1)
    total_t = pos["mass"].sum() / 1e6

    fig = plt.figure(figsize=(13.6, 8.2))
    ax_a = fig.add_axes((0.065, 0.125, 0.505, 0.665))
    ax_b = fig.add_axes((0.71, 0.125, 0.265, 0.665))

    # --- panel A: cumulative mass share vs rank ------------------------------
    ax_a.fill_between(ranks, cumulative, color=PALE, alpha=0.35, linewidth=0)
    ax_a.plot(ranks, cumulative, color=BLUE, linewidth=2.2)
    ax_a.axhline(50, color=MUTED, linewidth=1, linestyle=(0, (4, 3)))
    ax_a.set_xscale("log")
    ax_a.set_xlim(1, len(pos))
    ax_a.set_ylim(0, 102)
    ax_a.set_xlabel("Record rank (by mass, logarithmic scale)")
    ax_a.set_ylabel(f"Cumulative share of the {total_t:,.0f} t catalogued mass (%)")

    for rank in (1, 10, 100, 1000, 10000):
        share = cumulative.iloc[rank - 1]
        ax_a.plot([rank], [share], marker="o", markersize=6, color=ORANGE, zorder=5)
        ax_a.annotate(
            f"{share:.1f}%",
            (rank, share),
            textcoords="offset points",
            xytext=(6, -15 if rank < 100 else 6),
            fontsize=10,
            color=INK,
        )
    ax_a.annotate(
        f"{n_50} records carry half\nof the catalogued mass",
        xy=(n_50, 50),
        xytext=(3.5, 27),
        fontsize=10,
        color=INK,
        arrowprops=dict(arrowstyle="->", color=MUTED, linewidth=1),
    )
    ax_a.text(
        0.03,
        0.965,
        f"Top 1   \u2022 Hoba, 60.0 t  \u2022  {cumulative.iloc[0]:.1f}%\n"
        f"Top 10  \u2022  {cumulative.iloc[9]:.1f}%\n"
        f"Top 100  \u2022  {cumulative.iloc[99]:.1f}%",
        transform=ax_a.transAxes,
        va="top",
        ha="left",
        fontsize=10,
        color=INK,
        linespacing=1.55,
        bbox=dict(facecolor="white", edgecolor=GRID, boxstyle="round,pad=0.45", alpha=0.95),
    )
    clean_axis(ax_a)
    ax_a.set_title("Cumulative share of catalogued mass", pad=12)

    # --- panel B: the 15 heaviest records ------------------------------------
    top = pos.head(15).iloc[::-1]
    y = np.arange(len(top))
    colors = [TEAL if fell else ORANGE for fell in top["is_fell"]]
    ax_b.scatter(top["mass"], y, s=52, color=colors, zorder=5)
    ax_b.set_xscale("log")
    ax_b.set_xlim(top["mass"].min() * 0.7, top["mass"].max() * 6.5)
    ax_b.set_yticks(y, top["name"], fontsize=10)
    for yi, mass in zip(y, top["mass"], strict=True):
        ax_b.text(mass * 1.35, yi, human_mass(mass), va="center", ha="left", fontsize=9.5, color=MUTED)
    ax_b.set_xticks([1e4, 1e5, 1e6, 1e7, 1e8], ["10 kg", "100 kg", "1 t", "10 t", "100 t"])
    ax_b.set_xlabel("Mass (logarithmic scale)")
    ax_b.legend(
        handles=[
            plt.Line2D([], [], marker="o", linestyle="", color=ORANGE, label="Found"),
            plt.Line2D([], [], marker="o", linestyle="", color=TEAL, label="Fell"),
        ],
        loc="upper left",
        fontsize=10,
    )
    clean_axis(ax_b, grid="x")
    ax_b.tick_params(axis="y", length=0)
    ax_b.set_title("The 15 heaviest records", pad=12)

    add_titles(
        fig,
        "A handful of iron meteorites dominate the catalogued mass",
        f"Records ranked by mass \u2022 {len(pos):,} records with mass > 0 g \u2022 cumulative share of the {total_t:,.0f} t total",
        "The 19 records with mass \u2264 0 g are excluded. Sikhote-Alin (9th heaviest) is the only observed fall among the giants; "
        "large irons survive atmospheric entry and are easy to recover.",
    )
    return fig


def main(df: pd.DataFrame | None = None) -> str:
    use_style()
    if df is None:
        from ..common import load_landings

        df = load_landings()
    return str(save_figure(build(df), FIGURE))
