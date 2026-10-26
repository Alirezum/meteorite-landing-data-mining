"""Figure 11: records vs catalogued mass per recovery region (the Antarctic trade-off)."""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from ..common import (
    BLUE,
    INK,
    MUTED,
    ORANGE,
    add_titles,
    clean_axis,
    human_mass,
    save_figure,
    use_style,
)

FIGURE = "11_records_vs_mass.png"


def build(df: pd.DataFrame) -> plt.Figure:
    geo = df[df["region"].notna()].copy()
    led = geo.groupby("region").agg(
        n=("name", "size"),
        mass=("mass", lambda s: s.clip(lower=0).sum()),
        med=("mass", "median"),
    )
    led["pct_rec"] = led["n"] / led["n"].sum() * 100
    led["pct_mass"] = led["mass"] / led["mass"].sum() * 100
    led = led.sort_values("pct_rec")
    total_t = led["mass"].sum() / 1e6

    y = np.arange(len(led))
    fig = plt.figure(figsize=(13.6, 8.4))
    ax_a = fig.add_axes((0.155, 0.115, 0.46, 0.675))
    ax_b = fig.add_axes((0.705, 0.115, 0.25, 0.675))

    # --- panel A: dumbbell - share of records vs share of mass ---------------
    for yi, (rec, mass) in enumerate(zip(led["pct_rec"], led["pct_mass"], strict=True)):
        ax_a.plot([rec, mass], [yi, yi], color="#c8d2dc", linewidth=2.2, zorder=2)
    ax_a.scatter(led["pct_rec"], y, s=62, color=BLUE, zorder=5, label="Share of geolocated records")
    ax_a.scatter(led["pct_mass"], y, s=62, color=ORANGE, zorder=5, label="Share of catalogued mass")
    for yi, (rec, mass) in enumerate(zip(led["pct_rec"], led["pct_mass"], strict=True)):
        label = (lambda v: f"{v:.1f}%" if v >= 10 else f"{v:.2f}%")
        if rec < 0.05 and mass < 0.05:  # both dots at the axis edge: stack the labels
            ax_a.annotate(f"{rec:.2f}%", (rec, yi), textcoords="offset points", xytext=(6, 5),
                          ha="left", va="bottom", fontsize=9, color=INK)
            ax_a.annotate(f"{mass:.2f}%", (mass, yi), textcoords="offset points", xytext=(6, -7),
                          ha="left", va="top", fontsize=9, color=INK)
            continue
        rec_right = rec >= mass
        ax_a.annotate(
            label(rec),
            (rec, yi),
            textcoords="offset points",
            xytext=(7 if rec_right else -7, 0),
            ha="left" if rec_right else "right",
            va="center",
            fontsize=9,
            color=INK,
        )
        ax_a.annotate(
            label(mass),
            (mass, yi),
            textcoords="offset points",
            xytext=(7 if not rec_right else -7, 0),
            ha="left" if not rec_right else "right",
            va="center",
            fontsize=9,
            color=INK,
        )
    ax_a.set_xscale("log")
    ax_a.set_xlim(0.015, 400)
    ax_a.set_xticks([0.1, 1, 10, 100], ["0.1%", "1%", "10%", "100%"])
    ax_a.set_yticks(y, led.index, fontsize=10.5)
    ax_a.tick_params(axis="y", length=0)
    ax_a.legend(loc="lower right", fontsize=10, handletextpad=0.4)
    ax_a.set_xlabel("Share of the geolocated catalogue (logarithmic scale)")
    clean_axis(ax_a, grid="x")
    ax_a.set_title("Share of records vs share of catalogued mass", pad=12)

    # --- panel B: median mass per record -------------------------------------
    ax_b.scatter(led["med"], y, s=62, color=INK, zorder=5)
    for yi, med in zip(y, led["med"], strict=True):
        ax_b.text(med * 1.35, yi, human_mass(med), va="center", ha="left", fontsize=9.5, color=MUTED)
    ax_b.set_xscale("log")
    ax_b.set_xlim(6, 5e4)
    ax_b.set_xticks([1e1, 1e2, 1e3, 1e4], ["10 g", "100 g", "1 kg", "10 kg"])
    ax_b.set_ylim(-0.6, len(led) - 0.4)
    ax_b.tick_params(axis="y", left=False, labelleft=False)
    ax_b.set_xlabel("Median mass (logarithmic scale)")
    clean_axis(ax_b, grid="x")
    ax_b.set_title("Median mass per record", pad=12)

    add_titles(
        fig,
        "Antarctica yields 69% of the records and 0.7% of the mass",
        f"Geolocated records only (31,962 / 45,716; {total_t:,.1f} t of the 605.3 t catalogue) \u2022 regions ranked by record count",
        "Mass shares are dominated by a handful of giant irons recovered in populated regions (Hoba, Cape York, Campo del Cielo \u2014 figure 05): the median "
        "Antarctic record is 13 g against 10.5 kg in the rest of South America. Coarse lat/lon regions as in figure 04.",
    )
    return fig


def main(df: pd.DataFrame | None = None) -> str:
    use_style()
    if df is None:
        from ..common import load_landings

        df = load_landings()
    return str(save_figure(build(df), FIGURE))
