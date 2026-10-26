"""Figure 08: coordinate coverage over time - the modern catalogue loses its geography."""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from ..common import (
    INK,
    MUTED,
    ORANGE,
    TEAL,
    add_titles,
    clean_axis,
    save_figure,
    use_style,
)

FIGURE = "08_coordinate_coverage.png"
MISSING_COLOR = "#c8d2dc"  # records without coordinates


def build(df: pd.DataFrame) -> plt.Figure:
    dated = df[(df["decade"] >= 1900) & df["decade"].notna()].copy()
    dated["located"] = dated["region"].notna()
    decades = sorted(dated["decade"].unique())
    x = np.arange(len(decades))

    per = dated.groupby("decade").agg(n=("name", "size"), located=("located", "sum"))
    per["pct"] = per["located"] / per["n"] * 100

    by_status = (
        dated.groupby(["decade", "is_fell"])
        .agg(n=("name", "size"), located=("located", "sum"))
        .reset_index()
    )
    fell = by_status[by_status["is_fell"]].set_index("decade").reindex(decades)
    found = by_status[~by_status["is_fell"]].set_index("decade").reindex(decades)
    fell_pct = fell["located"] / fell["n"] * 100
    found_pct = found["located"] / found["n"] * 100

    fig = plt.figure(figsize=(13.6, 8.6))
    ax_a = fig.add_axes((0.075, 0.125, 0.52, 0.665))
    ax_b = fig.add_axes((0.665, 0.125, 0.29, 0.665))

    # --- panel A: stacked counts per decade ----------------------------------
    fell_located = fell["located"].to_numpy()
    found_located = found["located"].to_numpy()
    missing = (per["n"] - per["located"]).to_numpy()
    ax_a.bar(x, fell_located, width=0.74, color=TEAL, label="Located \u2014 Fell")
    ax_a.bar(x, found_located, bottom=fell_located, width=0.74, color=ORANGE, label="Located \u2014 Found")
    ax_a.bar(
        x,
        missing,
        bottom=fell_located + found_located,
        width=0.74,
        color=MISSING_COLOR,
        label="No coordinates",
    )
    totals = per["n"].to_numpy()
    for xi, pct, total in zip(x, per["pct"], totals, strict=True):
        ax_a.text(xi, total * 1.02, f"{pct:.0f}%", ha="center", va="bottom", fontsize=9, color=INK)
    ax_a.set_xticks(x, [f"{d}s" for d in decades], rotation=45, ha="right", fontsize=9.5)
    ax_a.set_ylim(0, totals.max() * 1.14)
    ax_a.set_yticks([0, 5000, 10000, 15000], ["0", "5k", "10k", "15k"])
    ax_a.set_ylabel("Records per decade")
    clean_axis(ax_a)
    ax_a.legend(loc="upper left", fontsize=10, handlelength=1.2, labelspacing=0.35)
    ax_a.set_title("Records per decade, by fall status and coordinate availability", pad=12)

    # --- panel B: coverage share by fall status ------------------------------
    ax_b.plot(x, fell_pct.to_numpy(), color=TEAL, linewidth=2.2, marker="o", markersize=4.5)
    ax_b.plot(x, found_pct.to_numpy(), color=ORANGE, linewidth=2.2, marker="o", markersize=4.5)
    ax_b.text(0.1, 103.5, "Fell", color=TEAL, fontsize=11, fontweight="bold", va="bottom")
    ax_b.text(len(decades) - 1, found_pct.iloc[-1] - 12, "Found", color=ORANGE, fontsize=11,
              fontweight="bold", ha="right")
    ax_b.annotate(
        f"{found_pct.iloc[-1]:.0f}%",
        (len(decades) - 1, found_pct.iloc[-1]),
        textcoords="offset points",
        xytext=(-6, -14),
        ha="right",
        fontsize=9.5,
        color=INK,
    )
    ax_b.set_xticks(x, [f"{d}s" for d in decades], rotation=45, ha="right", fontsize=9.5)
    ax_b.set_ylim(0, 108)
    ax_b.set_yticks([0, 25, 50, 75, 100], ["0", "25", "50", "75", "100"])
    clean_axis(ax_b)
    ax_b.set_title("Share of records with coordinates", pad=12)

    add_titles(
        fig,
        "Coordinate coverage is crumbling for finds \u2014 not for observed falls",
        "Dated records 1900s\u20132010s \u2022 left: counts split by fall status and whether coordinates exist \u2022 right: located share by fall status",
        "All 13,754 records without coordinates are \u201cFound\u201d; only 12 of 1,107 observed falls lack them. Geographic figures (03, 04, 10, 11) describe "
        "the 31,962 located records only \u2014 69.9% of the catalogue, but just 45.6% of the 2000s and 42.1% of the 2010s (2010\u20132013).",
    )
    return fig


def main(df: pd.DataFrame | None = None) -> str:
    use_style()
    if df is None:
        from ..common import load_landings

        df = load_landings()
    return str(save_figure(build(df), FIGURE))
