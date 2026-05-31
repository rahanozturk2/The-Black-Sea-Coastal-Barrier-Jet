The Black Sea Coastal-Barrier Jet (BCBJ)
This repository contains the numerical tools and configuration files for identifying and analyzing the Black Sea Coastal-Barrier Jet (BCBJ).

Overview
The BCBJ is characterized as a warm-season low-level jet (LLJ) primarily driven by orographic blocking against the Küre Mountains. This system operates as a hydraulically supercritical phenomenon, significantly influencing regional moisture transport and air-sea interactions in the western Black Sea.

Contents
LLJ_classification: A Python implementation of the two-step vertical wind-structure algorithm used to identify jet maxima within the 1000–700 hPa layer. It includes classification based on Bonner (1968) and ASJ criteria.
namelist.input: WRF V4.4.1 Control configuration for Case 1 (two-domain nest, d01 = 5 km / 200×160, d02 = 1 km / 400×350, 48 vertical layers defined by 49 eta interface levels). Thompson microphysics (mp_physics=8), YSU PBL (bl_pbl_physics=1), Noah LSM, RRTMG radiation, sst_update=1.
namelist.wps: Matching WPS configuration used to produce the geogrid for the Control run.
no_terrain_experiment/: Geogrid modification script (entire d01 flattened to land 10 m / sea 0 m), Control and No-Terrain geo_em files, and terrain comparison figures.
sst_cold_experiment/: met_em modification script that imposes a uniform -5 K SST/SKINTEMP anomaly over all sea points of d01 and d02 for the SST-Cold run.
inv_enh_experiment/: met_em modification script that sharpens the elevated capping inversion (+2.0 / +5.0 / +5.0 / +2.5 K at 1000 / 975 / 950 / 925 hPa) at the four lead-in lateral-boundary times, with a spatial taper on d01 and a uniform boost on d02.

Citation
**Öztürk, R., and M. Kadıoğlu, 2026: The Black Sea Coastal-Barrier Jet: Identification of a New Low-Level Wind System. Monthly Weather Review.# The-Black-Sea-Coastal-Barrier-Jet
** not published