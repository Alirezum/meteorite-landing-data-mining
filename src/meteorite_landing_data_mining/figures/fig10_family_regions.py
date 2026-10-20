"""Figure 10: which recovery environment delivers which meteorite family."""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap, PowerNorm

from ..common import INK, MUTED, add_titles, save_figure, use_style

FIGURE = "10_family_regions.png"

SHARE_CMAP = LinearSegmentedColormap.from_list(
    "share", ["#ffffff", "#eef4f9", "#c5d8e8", "#7fa8cc", "#3f7cb0", "#1c4a76"]
)


def build(df: pd.DataFrame) -> plt.Figure:
    geo = df[df["region"].notna()]
    row_order = df["family"].value_counts().index.tolist()
    col_order = geo["region"].value_counts().index.tolist()
    counts = pd.crosstab(geo["family"], geo["region"]).reindex(index=row_order, columns=col_order)
    shares = counts.div(counts.sum(axis=1), axis=0) * 100
    row_totals = counts.sum(axis=1)

    fig = plt.figure(figsize=(13.6, 8.8))
    ax = fig.add_axes((0.185, 0.185, 0.70, 0.60))

    im = ax.imshow(
        shares.to_numpy(),
        aspect="auto",
        cmap=SHARE_CMAP,
        norm=PowerNorm(0.5, vmin=0, vmax=100),
        interpolation="nearest",
    )
    ax.set_xticks(np.arange(len(col_order)), col_order, rotation=40, ha="right", fontsize=9.5)
    ax.set_yticks(
        np.arange(len(row_order)),
        [f"{name}  (n={n:,})" for name, n in zip(row_order, row_totals, strict=True)],
        fontsize=10,
    )
    ax.tick_params(length=0)
    ax.set_xticks(np.arange(-0.5, len(col_order), 1), minor=True)
    ax.set_yticks(np.arange(-0.5, len(row_order), 1), minor=True)
    ax.grid(which="minor", color="white", linewidth=1.6)
    ax.tick_params(which="minor", length=0)
    ax.grid(which="major", visible=False)
    for side in ax.spines.values():
        side.set_visible(False)

    for row_i, row_name in enumerate(row_order):
        for col_i, col_name in enumerate(col_order):
            value = shares.loc[row_name, col_name]
            if value >= 1:
                ax.text(
                    col_i,
                    row_i,
                    f"{value:.0f}",
                    ha="center",
                    va="center",
                    fontsize=9,
                    color="white" if value > 55 else INK,
                )

    cbar = fig.colorbar(im, ax=ax, fraction=0.024, pad=0.012)
    cbar.set_label("Share of the family's geolocated records (%)", fontsize=9.5, color=MUTED)
    cbar.set_ticks([0, 25, 50, 75, 100])
    cbar.ax.tick_params(labelsize=9, color=MUTED)
    cbar.outline.set_visible(False)

    add_titles(
        fig,
        "Every recovery environment has its own family signature",
        "Share of each family's geolocated records by recovery region (%) \u2022 rows sum to 100 \u2022 n = geolocated records \u2022 values below 1% are left blank",
        "Lunar meteorites are 62% Arabian finds (mostly Oman); enstatite (88%) and carbonaceous chondrites (68%) are overwhelmingly Antarctic; iron meteorites "
        "and pallasites skew to historic North-American collections (44% and 42%). Regions are the coarse lat/lon boxes of figure 04; 31,962 geolocated records.",
        title_y=0.965,
        subtitle_y=0.912,
        note_y=0.015,
    )
    return fig


def main(df: pd.DataFrame | None = None) -> str:
    use_style()
    if df is None:
        from ..common import load_landings

        df = load_landings()
    return str(save_figure(build(df), FIGURE))
