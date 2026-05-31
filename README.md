The Black Sea Coastal-Barrier Jet (BCBJ)
This repository contains the numerical tools and configuration files for identifying and analyzing the Black Sea Coastal-Barrier Jet (BCBJ).

Overview
The BCBJ is characterized as a warm-season low-level jet (LLJ) primarily driven by orographic blocking against the Küre Mountains. This system operates as a hydraulically supercritical phenomenon, significantly influencing regional moisture transport and air-sea interactions in the western Black Sea.

Contents
LLJ_classification: A Python implementation of the two-step vertical wind-structure algorithm used to identify jet maxima within the 1000–700 hPa layer. It includes classification based on Bonner (1968) and ASJ criteria.
namelist.input: WRF V4.4.1 Control configuration for Case 1 (two-domain nest, d01 = 5 km / 200×160, d02 = 1 km / 400×350, 49 eta levels). Thompson microphysics (mp_physics=8), YSU PBL (bl_pbl_physics=1), Noah LSM, RRTMG radiation, sst_update=1.
namelist.wps: Matching WPS configuration used to produce the geogrid for the Control run.
no_terrain_experiment/: Geogrid modification script, Control and No-Terrain geo_em files, and terrain comparison figures for the Kure-Mountains-flattened sensitivity run.

Citation
**Öztürk, R., and M. Kadıoğlu, 2026: The Black Sea Coastal-Barrier Jet: Identification of a New Low-Level Wind System. Monthly Weather Review.# The-Black-Sea-Coastal-Barrier-Jet
** not published