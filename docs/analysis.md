# Analysis of the new figures (04–07)

The repository already contained three summary figures and ~28 exploratory screenshots
(archived under `docs/exploration/`). Those cover mass distributions, class-level mass
comparisons, latitude bias, correlations, dissimilarity matrices and general EDA.

The four figures below were built to **complement** them with angles that were not yet
visualised: *where* meteorites are recovered (not just at which latitude), *how* the total
mass concentrates, a *coarse family* view instead of raw classes, and the *change of the
family mix over time*. All numbers are reproducible with
`uv run python -m meteorite_landing_data_mining`.

---

## 04 — Recovery regions (`figures/04_recovery_regions.png`)

**What it shows.** Records with coordinates (31,962 of 45,716, i.e. 69.9 %) grouped into
coarse recovery environments, and how the dominant environments change per decade.

**Key numbers**

| Region | Records |
| --- | ---: |
| Antarctica | 22,099 (69.1 % of geolocated) |
| Arabia & Middle East (Oman!) | 3,177 |
| Sahara & N. Africa | 2,454 |
| North America | 1,823 |
| Australia / Europe / Asia / Atacama | 643 / 535 / 452 / 424 |
| everything else (incl. 60 offshore) | 355 |

- The top three environments hold **86.8 %** of all geolocated records.
- Antarctica absorbs **92.8 %** of 1970s and **93.5 %** of 1980s records, then falls to
  74.5 % (1990s) → 55.1 % (2000s) → **11.2 %** (2010s).
- The 2010s geolocated records are led by **Arabia & Middle East (42.1 %)** and the
  **Atacama (32.4 %)**: the hot-desert era has replaced the Antarctic era.

**Interpretation.** This is a map of *collection effort*, not of how often meteorites fall.
Antarctic ice-sheet concentration plus systematic desert searches (Oman, Sahara, Atacama)
produce the peaks. Anything inferred about "where meteorites land" from this dataset is
dominated by those programmes. This extends figure 03 (latitude bands) by naming the
environments and adding the time dimension.

**Caveats.** The regions are deliberately coarse lat/lon boxes (e.g. "Arabia & Middle East"
includes Iran), and 30.1 % of records have no coordinates at all.

---

## 05 — Mass concentration (`figures/05_mass_concentration.png`)

**What it shows.** Cumulative share of the catalogued mass when records are ranked by mass
(Pareto / Lorenz view), plus the 15 heaviest records.

**Key numbers** (records with mass > 0; 19 records with mass ≤ 0 excluded)

- Total catalogued mass: **605 t**.
- **Hoba alone (60 t) = 9.9 %** of everything ever catalogued.
- Top **10 records = 57.1 %**, top **100 = 86.2 %**, top **1,000 = 96.7 %**.
- **9 records carry 50 %** of the mass; 193 records carry 90 %.
- All 15 heaviest are iron meteorites; the only *observed fall* among them is
  **Sikhote-Alin** (23 t, fell 1947 — the 9th heaviest record overall).

**Interpretation.** Summary statistics like "mean mass 13.2 kg" are meaningless here: the
mass distribution is a power law dominated by a handful of giant irons that survive entry
and are easy to stumble upon. For mass-based conclusions, the median or rank-based
statistics (the approach of figures 01 and 02) are the honest choice.

**Caveats.** Catalogued masses are individual recovered fragments, not necessarily single
objects (e.g. Campo del Cielo), and famous irons dominate the top of the list.

---

## 06 — Meteorite families (`figures/06_class_families.png`)

**What it shows.** The 466 raw `recclass` values reduced to 13 families: record counts and
the share of each family that was *observed falling* (Fell) rather than found.

**Key numbers**

- **Ordinary chondrites = 39,874 records (87.2 %)**; next: carbonaceous 1,603, HED
  achondrites 1,186, irons 1,069, enstatite 526.
- Rarest families in the catalogue: pallasites (94), Martian (119), other/ungrouped (114).
- Fell share per family: ordinary chondrites 2.1 %, carbonaceous 2.7 %, enstatite 3.2 %,
  other achondrites 3.5 %, mesosiderites 3.7 %, pallasites 4.3 %, **iron 4.6 %,
  HED 5.1 %** — versus an overall rate of 2.4 %.
- Conversely, **77.2 % of all 1,107 observed falls are ordinary chondrites** (855 records):
  they dominate the sky, but are diluted in the catalogue by desert/ice finds.

**Interpretation.** Every family is dominated by finds, but the degree differs
systematically. Families whose members are visually distinctive or metal-rich (irons, HED,
pallasites) show relatively more observed falls, because a fall of such a rock is noticed —
while an ordinary chondrite is usually recovered only through systematic collecting.
"Other / ungrouped" (37.7 %, n=114) is a small-n artefact of unclassified stones.

**Caveats.** Family mapping is a hand-written reduction of the raw classes (see
`src/meteorite_landing_data_mining/common.py`); "other/ungrouped" mixes heterogeneous
records.

---

## 07 — Family chronology (`figures/07_family_chronology.png`)

**What it shows.** For each decade from the 1900s to the 2010s: the number of records added
(top bar) and the family composition of those records (heatmap, % per decade).

**Key numbers**

- Records per decade: ~140–400 before 1970 → 4,969 (1970s) → 6,822 (1980s) →
  11,619 (1990s) → **17,757 (2000s)** → 1,963 (2010–2013).
- Iron meteorites: **41.7 %** of 1900s records → 26 % (1950s) → 15 % (1960s) →
  **< 1 % from the 1990s onward**.
- Ordinary chondrites: 45 % (1900s) → **92 % (1990s)** → 80 % (2010s).
- Carbonaceous chondrites: ~1–2 % early on → **4–5 % in the 2000s/2010s**.
- HED achondrites: 2–3 % historically → **7.5 % (2010s)**, their strongest decade.

**Interpretation.** The "composition of meteorites" changed dramatically — but not in the
sky. Before systematic collections, most records were chance finds, and chance finds are
biased towards big iron masses (42 % of 1900s records!). When Antarctic and desert
programmes took over from the 1970s, the composition snapped to the true dominant class
(ordinary chondrites) and then began to reflect the collectors' targets: carbonaceous
chondrites and rare achondrites (HED, Martian, Lunar) rise in the most recent decades.
Any time-series analysis of this dataset must account for this collection-regime break
around 1970.

**Caveats.** Pre-1900 (n=728) and undated records (n=292) are excluded; the 2010s only
covers 2010–2013, and cell values are rounded to whole percent.

---

## Takeaway

1. The catalogue is a **collection-effort record**, not a sample of what falls: Antarctica
   and three hot deserts contribute 86.8 % of geolocated records.
2. **Mass lives in a few irons** (top 10 records = 57 % of 605 t) while **numbers live in
   ordinary chondrites** (87 % of records).
3. Fell-share (2–5 % per family) is a **bias dial**: it is lowest exactly where systematic
   collecting is strongest.
4. The **1970s are a regime break** in every per-decade view: record counts, composition
   and geography all shift at once.

All four figures can be regenerated with one command:

```bash
uv sync
uv run python -m meteorite_landing_data_mining
```
