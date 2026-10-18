"""Figure 06: coarse meteorite families - record counts and observed-fall share."""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from ..common import (
    BLUE,
    INK,
    MUTED,
    ORANGE,
    TEAL,
    add_titles,
    clean_axis,
    save_figure,
    use_style,
)

FIGURE = "06_class_families.png"


def build(df: pd.DataFrame) -> plt.Figure:
    stats = df.groupby("family").agg(n=("name", "size"), fell=("is_fell", "sum"))
    stats["fell_pct"] = stats["fell"] / stats["n"] * 100
    stats = stats.sort_values("n", ascending=True)  # largest plotted at the top
    overall = df["is_fell"].mean() * 100

    y = np.arange(len(stats))
    labels = [f"{name}  (n={n:,})" for name, n in zip(stats.index, stats["n"], strict=True)]

    fig = plt.figure(figsize=(13.6, 8.4))
    ax_a = fig.add_axes((0.205, 0.115, 0.27, 0.675))
    ax_b = fig.add_axes((0.565, 0.115, 0.39, 0.675))

    # --- panel A: record counts per family -----------------------------------
    colors = [ORANGE if name == "Iron meteorites" else BLUE for name in stats.index]
    ax_a.barh(y, stats["n"], height=0.68, color=colors)
    ax_a.set_yticks(y, labels, fontsize=10)
    ax_a.tick_params(axis="y", length=0)
    ax_a.set_xscale("log")
    ax_a.set_xlim(stats["n"].min() * 0.55, stats["n"].max() * 2.6)
    clean_axis(ax_a, grid="x")
    ax_a.set_title("Records per family", pad=12)

    # --- panel B: share observed falling --------------------------------------
    ax_b.scatter(stats["fell_pct"], y, s=64, color=TEAL, zorder=5)
    ax_b.axvline(overall, color=MUTED, linewidth=1, linestyle=(0, (4, 3)))
    label_offset = stats["fell_pct"].max() * 0.02
    for yi, pct, n in zip(y, stats["fell_pct"], stats["n"], strict=True):
        suffix = f"  (n={n:,})" if pct > 10 else ""
        ax_b.text(pct + label_offset, yi, f"{pct:.1f}%{suffix}", va="center", ha="left",
                  fontsize=9.5, color=INK)
    ax_b.set_xlim(0, stats["fell_pct"].max() * 1.14)
    ax_b.set_ylim(-0.6, len(stats) - 0.25)
    ax_b.tick_params(axis="y", left=False, labelleft=False)
    ax_b.text(overall, len(stats) - 0.35, f"  overall {overall:.1f}%", color=MUTED, fontsize=9.5, va="center")
    clean_axis(ax_b, grid="x")
    ax_b.set_title("Share of records observed falling (same order as left)", pad=12)
    ax_b.set_xlabel("Observed falling (Fell) share of the family's records (%)")

    add_titles(
        fig,
        "Finds dominate every family \u2014 but the balance differs systematically",
        f"All {len(df):,} records grouped into coarse families \u2022 fell share = records observed falling \u00f7 all family records",
        "Families reduce the 466 raw recclass values to 13 groups (mapping in src/meteorite_landing_data_mining/common.py). "
        "Families with a low fell share are mainly recovered by chance in Antarctica and hot deserts, where collection bias is strongest.",
    )
    return fig


def main(df: pd.DataFrame | None = None) -> str:
    use_style()
    if df is None:
        from ..common import load_landings

        df = load_landings()
    return str(save_figure(build(df), FIGURE))
