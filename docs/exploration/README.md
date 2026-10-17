# Exploratory screenshots

Early, quick-look exploration of the dataset, produced before the repository was created
and kept here as a record of what has **already been visualised** — new figures should not
duplicate these views. The files were renamed from camera-roll/chat filenames
(`IMG_20261018_*` and `photo_2026-10-18_*`) to descriptive names for readability.

| File | Original name | Contents |
| --- | --- | --- |
| 01_yearly_record_counts_1900_2013.jpg | IMG_20261018_152505.jpg | Records per year, 1900–2013 (peak 2003) |
| 02_class_histograms_H3_H4.jpg | IMG_20261018_152507.jpg | Boxplots + log10_mass histograms for classes H3/H4 |
| 03_mixed_type_dissimilarity_heatmap.jpg | IMG_20261018_152510.jpg | Mixed-type dissimilarity (year, mass level, class, fall) |
| 04_year_interval_frequencies.jpg | IMG_20261018_152512.jpg | Records per year interval + grouped median year |
| 05_mass_density_fell_vs_found.jpg | IMG_20261018_152515.jpg | log10_mass and year densities, Fell vs Found |
| 06_descriptive_statistics_table.jpg | IMG_20261018_152525.jpg | Descriptive statistics of numeric features |
| 07_top_classes_fall_nametype_counts.jpg | IMG_20261018_152531.jpg | Top-15 classes, fall and nametype counts |
| 08_pixel_oriented_records.jpg | IMG_20261018_152534.jpg | Pixel-oriented view (records sorted by mass) |
| 09_mass_boxplots_by_fall_and_class.jpg | IMG_20261018_152536.jpg | log10_mass boxplots: fall type and top-10 classes |
| 10_log10_mass_normal_fit.jpg | IMG_20261018_152539.jpg | Normal distribution fitted to log10_mass |
| 11_quantile_plots.jpg | IMG_20261018_152601.jpg | Quantile plots of log10_mass and year |
| 12_class_treemap.jpg | IMG_20261018_152604.jpg | Treemap of the 25 most common classes |
| 13_missing_values_map.jpg | IMG_20261018_152606.jpg | Missing values per column and their pattern |
| 14_numeric_feature_boxplots.jpg | IMG_20261018_152608.jpg | Boxplots: log10_mass, year, reclat, reclong |
| 15_nominal_attributes_dissimilarity.jpg | IMG_20261018_152610.jpg | Nominal attributes + simple matching dissimilarity |
| 16_binary_attributes_jaccard.jpg | IMG_20261018_152618.jpg | Binary attributes + Jaccard similarity |
| 17_mass_qq_plots.jpg | IMG_20261018_152620.jpg | Q–Q plots: Fell vs Found, log10_mass vs normal |
| 18_pearson_correlation_matrix.jpg | IMG_20261018_152627.jpg | Pearson correlation matrix of numeric features |
| 19_euclidean_dissimilarity.jpg | IMG_20261018_152629.jpg | Data matrix + Euclidean dissimilarity (min–max) |
| 20_skewness_density_plots.jpg | IMG_20261018_152631.jpg | Densities of mass, log10_mass, year with skewness |
| 21_distance_metrics_comparison.jpg | IMG_20261018_152638.jpg | L1/L2/L∞ distance matrices compared |
| 22_feature_histograms.jpg | IMG_20261018_152640.jpg | Histograms of the numerical features |
| 23_scatter_correlation_examples.jpg | IMG_20261018_152642.jpg | Three scatters with Pearson r values |
| 24_class_cosine_similarity.jpg | IMG_20261018_152645.jpg | Cosine similarity between class mass distributions |
| 25_geographic_and_temporal_scatter.jpg | IMG_20261018_152650.jpg | World lat/long scatter + year vs mass |
| 26_scatterplot_matrix.jpg | IMG_20261018_152654.jpg | Scatterplot matrix coloured by fall |
| 27_circle_segments.jpg | IMG_20261018_152656.jpg | Circle segments (sorted by log10_mass) |
| 28_fell_vs_found_temporal_trends_fa.jpg | photo_2026-10-18_16-45-55.jpg | Persian-language composite: Fell vs Found trends (line, rolling mean, per-decade bars) |

Topics already covered here — mass distributions and tests, class-level comparisons,
latitude bias, time trends, correlations, dissimilarity/clustering views, missing values —
are intentionally **not** repeated in the new figures (04–07). See `docs/analysis.md`.
