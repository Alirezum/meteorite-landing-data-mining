"""Figure 04: where meteorites are recovered (recovery-region breakdown)."""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from ..common import (
    BLUE,
    INK,
    ORANGE,
    PALE,
    SALMON,
    TEAL,
    add_titles,
    clean_axis,
    save_figure,
    use_style,
)

FIGURE = "04_recovery_regions.png"

# Highlight the three dominant "collection environments"; everything else is blue.
REGION_COLORS = {
    "Antarctica": ORANGE,
    "Sahara & N. Africa": SALMON,
    "Arabia & Middle East": TEAL,
}
OTHER_COLOR = "#c8d2dc"
STACK_REGIONS = [
    "Antarctica",
    "Sahara & N. Africa",
    "Arabia & Middle East",
    "North America",
    "Australia",
]


def build(df: pd.DataFrame) -> plt.Figure:
    geo = df[df["region"].notna()].copy()
    counts = geo["region"].value_counts()

    fig = plt.figure(figsize=(13.6, 8.6))
    ax_a = fig.add_axes((0.135, 0.125, 0.26, 0.665))
    ax_b = fig.add_axes((0.475, 0.125, 0.50, 0.665))

    # --- panel A: counts per region -----------------------------------------
    ax_a.barh(
        counts.index[::-1],
        counts.values[::-1],
        color=[REGION_COLORS.get(r, OTHER_COLOR if r == "Ocean & other" else BLUE) for r in counts.index[::-1]],
        height=0.72,
    )
    ax_a.set_xscale("log")
    ax_a.set_xlim(counts.min() * 0.55, counts.max() * 3.4)
    for y, (_, n) in enumerate(counts[::-1].items()):
        ax_a.text(n * 1.18, y, f"{n:,}", va="center", ha="left", fontsize=10, color=INK)
    clean_axis(ax_a, grid="x")
    ax_a.tick_params(axis="y", length=0)
    ax_a.set_title("Geolocated records per recovery region", pad=12)

    # --- panel B: stacked composition by decade ------------------------------
    geo_dec = geo[geo["decade"] >= 1900]
    decades = sorted(geo_dec["decade"].dropna().unique())
    x = np.arange(len(decades))
    stacks = STACK_REGIONS + ["Other regions"]
    bottom = np.zeros(len(decades))
    for region in stacks:
        if region == "Other regions":
            mask = ~geo_dec["region"].isin(STACK_REGIONS)
        else:
            mask = geo_dec["region"] == region
        values = geo_dec[mask].groupby("decade").size().reindex(decades, fill_value=0).to_numpy()
        color = REGION_COLORS.get(region, BLUE if region == "North America" else PALE)
        if region == "Other regions":
            color = OTHER_COLOR
        ax_b.bar(x, values, bottom=bottom, width=0.76, color=color, label=region)
        bottom += values

    ax_b.set_xticks(x)
    ax_b.set_xticklabels([f"{d}s" for d in decades], rotation=45, ha="right", fontsize=9.5)
    for xi, total in zip(x, bottom, strict=True):
        ax_b.text(xi, total * 1.06, f"{total / 1000:.1f}k" if total >= 1000 else f"{total:.0f}",
                  ha="center", va="bottom", fontsize=9, color="#607898")
    ax_b.set_ylim(0, bottom.max() * 1.16)
    clean_axis(ax_b)
    ax_b.legend(loc="upper left", fontsize=10, handlelength=1.2, labelspacing=0.35)
    ax_b.set_title("Records per decade by region", pad=12)

    add_titles(
        fig,
        "Recovery is concentrated in Antarctica and the North-African deserts",
        "Geolocated records grouped into approximate recovery regions \u2022 colour highlights the dominant collection environments",
        "Recovery regions are coarse lat/lon bounding boxes, not exact borders. Only the 31,962 geolocated records are classified "
        "(13,754 records lack coordinates). The 2010s covers 2010-2013.",
    )
    return fig


def main(df: pd.DataFrame | None = None) -> str:
    use_style()
    if df is None:
        from ..common import load_landings

        df = load_landings()
    return str(save_figure(build(df), FIGURE))
