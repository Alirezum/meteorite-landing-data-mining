"""Figure builders, one module per output PNG in ``figures/``.

Figures 01-03 predate the repository (kept as ``figures/01``-``03``); the
modules below regenerate figures 04-11 from the raw dataset.
"""

from . import (
    fig04_recovery_regions,
    fig05_mass_concentration,
    fig06_class_families,
    fig07_family_chronology,
    fig08_coordinate_coverage,
    fig09_mass_by_decade,
    fig10_family_regions,
    fig11_records_vs_mass,
)

MODULES = (
    fig04_recovery_regions,
    fig05_mass_concentration,
    fig06_class_families,
    fig07_family_chronology,
    fig08_coordinate_coverage,
    fig09_mass_by_decade,
    fig10_family_regions,
    fig11_records_vs_mass,
)

__all__ = ["MODULES"]
