"""Figure 07: how the family mix of newly recorded meteorites changed over time."""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap, PowerNorm

from ..common import BLUE, INK, MUTED, add_titles, save_figure, use_style

FIGURE = "07_family_chronology.png"
TOP_FAMILIES = 7
OTHER_LABEL = "Other families"

SHARE_CMAP = LinearSegmentedColormap.from_list(
    "share", ["#ffffff", "#eef4f9", "#c5d8e8", "#7fa8cc", "#3f7cb0", "#1c4a76"]
)


def build(df: pd.DataFrame) -> plt.Figure:
    dated = df[(df["decade"] >= 1900) & df["decade"].notna()].copy()
    decades = sorted(dated["decade"].unique())
    total_counts = dated["family"].value_counts()
    top = list(total_counts.index[:TOP_FAMILIES])

    dated["family_row"] = np.where(dated["family"].isin(top), dated["family"], OTHER_LABEL)
    rows = top + [OTHER_LABEL]

    shares = (
        pd.crosstab(dated["family_row"], dated["decade"], normalize="columns")
        .reindex(index=rows, columns=decades)
        * 100
    )
    counts = dated.groupby("decade").size().reindex(decades)

    fig = plt.figure(figsize=(13.6, 8.8))
    grid = fig.add_gridspec(
        2, 1, height_ratios=[1, 4.8], hspace=0.12, left=0.175, right=0.955, top=0.775, bottom=0.145
    )
    ax_top = fig.add_subplot(grid[0])
    ax_heat = fig.add_subplot(grid[1])

    # --- marginal: records per decade ----------------------------------------
    x = np.arange(len(decades))
    ax_top.bar(x, counts.to_numpy(), width=0.7, color=BLUE)
    for xi, n in zip(x, counts.to_numpy(), strict=True):
        ax_top.text(xi, n * 1.03, f"{n / 1000:.1f}k" if n >= 1000 else f"{n:.0f}",
                    ha="center", va="bottom", fontsize=8.5, color=MUTED)
    ax_top.set_ylim(0, counts.max() * 1.22)
    ax_top.set_xlim(-0.6, len(decades) - 0.4)
    ax_top.set_xticks([])
    ax_top.set_yticks([0], ["0"])
    for side in ("top", "right"):
        ax_top.spines[side].set_visible(False)
    ax_top.grid(axis="x", visible=False)
    ax_top.set_title("Records added per decade", fontsize=10.5, color=MUTED, fontweight="normal", pad=6)
    ax_top.tick_params(axis="y", labelsize=9)

    # --- heatmap: family share per decade ------------------------------------
    im = ax_heat.imshow(
        shares.to_numpy(),
        aspect="auto",
        cmap=SHARE_CMAP,
        norm=PowerNorm(0.5, vmin=0, vmax=100),
        interpolation="nearest",
    )
    ax_heat.set_xticks(x, [f"{d}s" for d in decades], rotation=45, ha="right", fontsize=9.5)
    ax_heat.set_yticks(np.arange(len(rows)), rows, fontsize=10)
    ax_heat.tick_params(length=0)
    ax_heat.set_xticks(np.arange(-0.5, len(decades), 1), minor=True)
    ax_heat.set_yticks(np.arange(-0.5, len(rows), 1), minor=True)
    ax_heat.grid(which="minor", color="white", linewidth=1.4)
    ax_heat.tick_params(which="minor", length=0)
    ax_heat.grid(which="major", visible=False)
    for side in ax_heat.spines.values():
        side.set_visible(False)

    for row, yi in zip(rows, np.arange(len(rows)), strict=True):
        for decade, xi in zip(decades, x, strict=True):
            value = shares.loc[row, decade]
            ax_heat.text(
                xi, yi, f"{value:.0f}", ha="center", va="center", fontsize=9,
                color="white" if value > 55 else INK,
            )

    cbar = fig.colorbar(im, ax=ax_heat, fraction=0.028, pad=0.012)
    cbar.set_label("Share of the decade's records (%)", fontsize=9.5, color=MUTED)
    cbar.set_ticks([0, 25, 50, 75, 100])
    cbar.ax.tick_params(labelsize=9, color=MUTED)
    cbar.outline.set_visible(False)

    im.set_clim(0, 100)
    add_titles(
        fig,
        "The family mix of newly recorded meteorites shifted after the 1960s",
        "Share of each decade's records by meteorite family (%) \u2022 cell values in percent of that decade's records",
        "Pre-1900 (n=728) and undated (n=292) records are excluded; the 2010s covers 2010-2013 and cell values are rounded to whole "
        "percent. Iron meteorites drop from ~42% of 1900s records to <1% after 1990, while carbonaceous and achondrite families grow "
        "as Antarctic and hot-desert collections expand.",
        title_y=0.962,
        subtitle_y=0.915,
        note_y=0.015,
    )
    return fig


def main(df: pd.DataFrame | None = None) -> str:
    use_style()
    if df is None:
        from ..common import load_landings

        df = load_landings()
    return str(save_figure(build(df), FIGURE))
