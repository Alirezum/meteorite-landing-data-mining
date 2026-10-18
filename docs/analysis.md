# Analysis of the new figures (04–11)

The repository already contained three summary figures and ~28 exploratory screenshots
(archived under `docs/exploration/`). Those cover mass distributions, class-level mass
comparisons, latitude bias, correlations, dissimilarity matrices and general EDA.

The four figures below (04–07) were built to **complement** them with angles that were not yet
visualised: *where* meteorites are recovered (not just at which latitude), *how* the total
mass concentrates, a *coarse family* view instead of raw classes, and the *change of the
family mix over time*. Figures 08–11 followed in a second wave, interrogating the
*reliability* of those views and the remaining cross-dimensions — see the
[second set](#second-set-figures-0811) at the end of this page. All numbers are reproducible with
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

## Takeaway — first set (04–07)

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

---

# Second set: figures 08–11

Where 04–07 described *what* the catalogue contains, 08–11 interrogate how much of it can be
trusted and how its dimensions interact: coordinate coverage over time (08), the size of
records through time (09), the family × environment cross (10), and the records-vs-mass
ledger across environments (11). None of these views exists in figures 01–03 or in the
`docs/exploration/` archive.

---

## 08 — Coordinate coverage (`figures/08_coordinate_coverage.png`)

**What it shows.** Dated records 1900s–2010s split by fall status and coordinate availability,
plus the located share per decade for finds and falls separately. This quantifies the hidden
caveat behind every geographic figure.

**Key numbers**

- Overall coverage: **31,962 of 45,716 records (69.9 %)** have coordinates.
- Observed falls: **98.9 % located** (only 12 of 1,107 lack coordinates). Finds: **69.2 %**.
- **All 13,754 unlocated records are finds, and 13,575 of them (98.7 %) date after 1970.**
- Coverage per decade: 96.7–99.8 % through the 1980s, then **78.3 % (1990s) → 45.6 % (2000s)
  → 42.1 % (2010s)** — 9,668 of the 2000s' 17,757 records have no coordinates at all.

**Interpretation.** The geography of the catalogue is not uniformly incomplete: it is
*complete for observed falls* (documented events) and *progressively missing for finds*, whose
location metadata stops arriving in the modern bulk of the dataset. This has a direct
consequence for figure 04: its "hot-desert 2010s" conclusion rests on 827 of 1,963 records,
and the 2000s' composition is computed on 46 % of the decade. Cross-sectional geographic
statements should always be read as statements about the *located* half of the modern
catalogue.

**Caveats.** The 2010s covers 2010–2013. We cannot tell whether the coordinates were never
recorded or lost in the cleaned export; the pattern (finds only, post-1970) suggests a
cataloguing/export artefact rather than a physical fact.

---

## 09 — Mass through time (`figures/09_mass_by_decade.png`)

**What it shows.** Median mass per decade with interquartile bands, finds vs observed falls
(left), and the share of records under 100 g (right). Figure 05 argued that mass statistics
need rank-based treatment; this figure shows the *time dimension* of the same problem.

**Key numbers** (dated records with mass > 0)

- Median find mass: **13.0 kg (1900s) → 10 g (1970s)** — a factor of **≈1,300** — then
  23 g (1980s) → 41.5 g (2000s) → 99.6 g (2010s).
- Median observed fall: **1.15–4.44 kg in every decade** from the 1900s to the 2010s.
- Share of finds under 100 g: 4.8 % (1900s) → **81.2 % (1970s)** → 50.2 % (2010s).
  For falls the same share stays at 3.6–16.1 %.

**Interpretation.** The recorded "typical meteorite" shrank by three orders of magnitude —
but only in the *found* population. The fall population, which is sampled by physics rather
than by searching, did not change size at all. The 1970s break is a change of the
**detection floor**: systematic ice/desert surveys and metal-detector hunting started
recovering stones of grams, while before 1970 a meteorite entered the record mostly by
being stumbled upon — which favours big, metal-rich masses (hence figure 07's iron-heavy
early decades). Any mass-based time series on this dataset conflates "what fell" with
"what collectors could find".

**Caveats.** Masses are individual recovered fragments; 19 records with mass ≤ 0 g are
excluded. The post-1970 rise from 10 g to ~100 g likely combines detector technology,
cataloguing practice, and the composition of the newest records.

---

## 10 — Family × region (`figures/10_family_regions.png`)

**What it shows.** The 13 coarse families against the 12 recovery regions: the share of each
family's geolocated records contributed by each environment (rows sum to 100 %).

**Key numbers** (geolocated records only)

- **Ordinary chondrites (n=28,413): 72 % Antarctic**, 10 % Arabia, 8 % Sahara.
- **Enstatite chondrites (n=394): 88 % Antarctic**; **carbonaceous chondrites (n=837):
  68 % Antarctic + 16 % Sahara**; HED achondrites: 69 % Antarctic.
- **Lunar meteorites (n=102): 62 % Arabian finds** (24 % Antarctic, 11 % Sahara);
  Martian: 34 % Arabia, 30 % Antarctic, 25 % Sahara.
- **Iron meteorites (n=961): 44 % North American** collections, 13 % Antarctic, 10 % Asia;
  pallasites: 42 % North America.
- Mesosiderites are the only family split evenly between two environments (37 % Antarctic,
  37 % Arabia).

**Interpretation.** Each environment is a sieve with a different mesh. Antarctica's
systematic blue-ice searches deliver the statistical bulk of chondrites — including rare
chondrite types (enstatite, carbonaceous) that are nearly absent elsewhere. The hot deserts
deliver *targeted* finds: Lunar and Martian stones are recognised valuables (Oman's finds
dominate), and the historic, populous North-American/European collections are where the
19th–20th century's big irons were accumulated. Figure 06's "found share" bias is thus not
uniform noise: it has a geographic fingerprint.

**Caveats.** Geolocated records only (31,962); "other/ungrouped" mixes heterogeneous small
classes; the smaller families (n < 150) move by a handful of records; regions are the coarse
boxes of figure 04.

---

## 11 — Records vs mass ledger (`figures/11_records_vs_mass.png`)

**What it shows.** For each recovery region: its share of geolocated records against its
share of the catalogue's mass, plus the median mass per record. Figure 04 counted records;
figure 05 counted mass; this figure crosses the two.

**Key numbers** (geolocated records, 593.9 t of the 605.3 t catalogued mass)

- **Antarctica: 69.1 % of records, 0.65 % of mass**; median record 13 g.
- The top-3 environments by records (Antarctica, Arabia, Sahara = 86.8 % of records) hold
  just **4.3 % of the mass**.
- The top-3 by mass — **North America (37.5 %), Africa-rest (18.0 %), Asia (14.9 %)** —
  hold 70.4 % of the tonnage from **7.6 % of the records**.
- Median mass per record: South America-rest 10.5 kg, New Zealand 7.3 kg (n=8), Asia 3.2 kg,
  Africa-rest 2.7 kg, Europe 2.0 kg, North America 1.9 kg ... Antarctica 13 g,
  Australia 128 g, Atacama 143 g.

**Interpretation.** The catalogue carries two different histories. *Counts* are the history
of the last 50 years: systematic collecting in Antarctica and two hot deserts. *Mass* is the
history of the 19th and early 20th century: a handful of giant irons (Hoba, Cape York,
Campo del Cielo — figure 05) recovered where people were. Antarctica yields **181× more
records than the rest of South America yet 19× less mass**. Any regional "importance"
depends entirely on whether it is measured in stones or in kilograms.

**Caveats.** Mass = individually catalogued fragments (Campo del Cielo is one crater field
counted as several records); New Zealand (n=8) and the other small regions are small-n
artefacts; 11.4 t of catalogued mass sits on unlocated records and is excluded here.

---

## Takeaway — second set (08–11)

1. **The blind spot is modern, not historic.** Coordinate coverage is ~100 % for observed
   falls but falls to 45.6 % among 2000s finds — geographic conclusions apply to a shrinking
   subset.
2. **The detection floor collapsed in the 1970s** (median find 13 kg → 10 g, ~1,300×), while
   observed falls kept their size — the record flood is a collecting signal, not a sky signal.
3. **Environment is an explanation, not just a location:** Antarctica supplies chondrites
   (including the rare ones), Arabia supplies Lunar/Martian stones, old North-American
   collections supply the giant irons.
4. **Records and mass live in different places** (69.1 % vs 0.65 % in Antarctica): measure
   the catalogue in stones or in kilograms and you'll tell two different stories.

The same command regenerates all eight figures (04–11).
