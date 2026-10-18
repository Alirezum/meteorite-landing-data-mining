"""Shared helpers: paths, figure style, data loading and feature engineering.

The colour palette below was sampled from the pre-existing summary figures
(``figures/01``-``03``) so new figures share the same visual language.
"""

from __future__ import annotations

import re
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_CSV = PROJECT_ROOT / "data" / "raw" / "Meteorite_Landings_cleaned.csv"
FIGURES_DIR = PROJECT_ROOT / "figures"

# --- palette (sampled from figures/01-03) -----------------------------------
INK = "#102840"  # titles and primary text
MUTED = "#607898"  # subtitles, notes and tick labels
GRID = "#d8e0e8"
BLUE = "#3870a8"
ORANGE = "#e06850"
TEAL = "#289888"
SALMON = "#e8806a"
LAKE = "#68b8b0"  # light teal fill
SAND = "#e89880"  # light salmon fill
PALE = "#b8c8d8"  # light blue fill


def use_style() -> None:
    """Apply the shared matplotlib style."""
    mpl.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 11.5,
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "axes.edgecolor": GRID,
            "axes.linewidth": 0.9,
            "axes.labelcolor": MUTED,
            "axes.labelsize": 12,
            "axes.titlesize": 14,
            "axes.titlecolor": INK,
            "axes.titleweight": "bold",
            "axes.titlelocation": "left",
            "axes.grid": True,
            "grid.color": GRID,
            "grid.linewidth": 0.8,
            "xtick.color": MUTED,
            "ytick.color": MUTED,
            "xtick.labelsize": 10.5,
            "ytick.labelsize": 10.5,
            "legend.frameon": False,
        }
    )


def clean_axis(ax, *, grid: str = "y") -> None:
    """Drop the top/right spines and keep grid lines only on the given axis."""
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    other = "x" if grid == "y" else "y"
    ax.grid(axis=other, visible=False)
    ax.grid(axis=grid, visible=True)


def add_titles(
    fig,
    title: str,
    subtitle: str | None = None,
    note: str | None = None,
    *,
    title_y: float = 0.965,
    subtitle_y: float = 0.918,
    note_y: float = 0.018,
) -> None:
    """Add the figure-level title, subtitle and footnote used across figures."""
    fig.text(0.045, title_y, title, fontsize=16.5, fontweight="bold", color=INK, va="top")
    if subtitle:
        fig.text(0.045, subtitle_y, subtitle, fontsize=12, color=MUTED, va="top")
    if note:
        fig.text(0.045, note_y, note, fontsize=9.5, color=MUTED, va="bottom")


def human_mass(grams: float) -> str:
    """Format a mass in grams as a compact human-readable string."""
    if grams >= 1e6:
        return f"{grams / 1e6:,.1f} t"
    if grams >= 1e3:
        return f"{grams / 1e3:,.1f} kg"
    return f"{grams:,.0f} g"


# --- geography ---------------------------------------------------------------

# Approximate lat/lon bounding boxes, evaluated in order (first match wins).
# Deliberately coarse: they identify broad recovery environments, not borders.
REGION_BOXES: list[tuple[str, float, float, float, float]] = [
    ("Antarctica", -90.0, -60.0, -180.0, 180.0),
    ("Atacama region", -32.0, -17.0, -73.0, -63.0),
    ("Australia", -44.0, -10.0, 112.0, 154.0),
    ("New Zealand", -48.0, -33.0, 165.0, 180.0),
    ("North America", 13.0, 90.0, -180.0, -52.0),
    ("South America (rest)", -60.0, 13.0, -82.0, -34.0),
    ("Sahara & N. Africa", 15.0, 36.0, -17.0, 35.0),
    ("Arabia & Middle East", 12.0, 40.0, 34.0, 60.0),
    ("Europe", 36.0, 72.0, -25.0, 40.0),
    ("Africa (rest)", -35.0, 37.0, -20.0, 52.0),
    ("Asia", -10.0, 80.0, 60.0, 180.0),
]
REGION_OTHER = "Ocean & other"


def classify_region(lat: float | None, lon: float | None) -> str | None:
    """Map coordinates to a coarse recovery region (``None`` if not geolocated)."""
    if pd.isna(lat) or pd.isna(lon):
        return None
    for name, lat_min, lat_max, lon_min, lon_max in REGION_BOXES:
        if lat_min <= lat <= lat_max and lon_min <= lon <= lon_max:
            return name
    return REGION_OTHER


# --- meteorite families ------------------------------------------------------

_ORDINARY = re.compile(r"^(?:H|L|LL)\d|^(?:H|L|LL)$|^(?:H/L|L/LL|LL/L|H/LL)\d|^(?:H|L|LL)-")
_ENSTATITE = re.compile(r"^E(?:\d|H|L|$)")

_FAMILY_PREFIXES: list[tuple[tuple[str, ...], str]] = [
    (("Howardite", "Eucrite", "Diogenite", "HED"), "HED achondrites"),
    (("Aubrite", "Ureilite", "Angrite", "Achondrite"), "Other achondrites"),
    (("Acapulcoite", "Lodranite", "Winonaite", "Brachinite"), "Primitive achondrites"),
    (("Iron",), "Iron meteorites"),
    (("Pallasite",), "Pallasites"),
    (("Mesosiderite",), "Mesosiderites"),
]


def class_family(recclass: str) -> str:
    """Reduce one of the 466 raw ``recclass`` values to a coarse family."""
    rc = str(recclass).strip()
    if rc.startswith("Martian") or rc.startswith("SNC"):
        return "Martian meteorites"
    if rc.startswith("Lunar"):
        return "Lunar meteorites"
    rc_clean = rc.replace("~", "")  # the cleaned dataset contains "H~5" style typos
    if _ORDINARY.match(rc_clean):
        return "Ordinary chondrites"
    if rc_clean.startswith("C"):  # CM, CO, CV, CK, CR, CH, CB, CI, C-ung, ...
        return "Carbonaceous chondrites"
    if _ENSTATITE.match(rc_clean):  # EH, EL, E3-E6, E-ung
        return "Enstatite chondrites"
    if re.match(r"^[RK]\d", rc_clean):  # Rumuruti and Kakangari chondrites
        return "Other chondrites"
    if rc_clean.startswith(("OC", "Relict OC")):  # "OC" = ordinary chondrite shorthand
        return "Ordinary chondrites"
    for prefixes, family in _FAMILY_PREFIXES:
        if rc_clean.startswith(prefixes):
            return family
    if "chondrite" in rc_clean.lower():  # e.g. "Chondrite-ung"
        return "Other chondrites"
    return "Other / ungrouped"


# --- loading -----------------------------------------------------------------


def load_landings() -> pd.DataFrame:
    """Load the cleaned dataset and add the derived analysis columns."""
    df = pd.read_csv(DATA_CSV)
    df = df.rename(columns={"mass (g)": "mass", "reclat": "lat", "reclong": "lon"})
    df["is_fell"] = df["fall"].eq("Fell")
    df["family"] = df["recclass"].map(class_family)
    df["region"] = [classify_region(a, b) for a, b in zip(df["lat"], df["lon"], strict=True)]
    df["decade"] = (df["year"] // 10 * 10).astype("Int64")
    return df


def save_figure(fig, filename: str) -> Path:
    """Save a figure into ``figures/`` and report the path."""
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    path = FIGURES_DIR / filename
    fig.savefig(path, dpi=170, facecolor="white", bbox_inches="tight")
    plt.close(fig)
    return path
