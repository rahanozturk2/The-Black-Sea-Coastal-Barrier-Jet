# No-Terrain WRF sensitivity experiment

Companion code and figures for the No-Terrain sensitivity run referenced
in **The Black Sea Coastal-Barrier Jet** (MWR submission, Ozturk et al.).

## What this is

A controlled experiment that isolates the role of the Kure Mountains
(northern Anatolia) in maintaining the Black Sea Coastal-Barrier Jet
(BCBJ). The terrain inside a fixed box (39.5-43.0 deg N, 28.5-36.0 deg E)
is reduced to **10 m** over land while the original coastline and all
ocean points are preserved. A 20-grid-cell cosine-tapered buffer blends
the flattened core back to the surrounding orography so no artificial
step is introduced.

All other WPS / namelist settings are identical to the Control run.

## Files

| File | What it is |
|---|---|
| `make_no_terrain_geo.py` | The exact script used to modify the WPS geogrid files (`geo_em.d01.nc`, `geo_em.d02.nc`) -> `*_no_terrain.nc`. Loops over both nested domains. |
| `terrain_control_d01.png` | d01 (5 km outer domain) terrain, Control (default WPS geogrid). |
| `terrain_noterrain_d01.png` | d01 terrain after No-Terrain modification. |
| `terrain_control_vs_noterrain_d01.png` | d01 side-by-side comparison; modification box drawn in red. |
| `terrain_control_d02.png` | d02 (1 km nested domain) terrain, Control. |
| `terrain_noterrain_d02.png` | d02 terrain after No-Terrain modification. |
| `terrain_control_vs_noterrain_d02.png` | d02 side-by-side comparison. |
| `_make_terrain_pngs.py` | Plotting script used to produce the PNGs above (loops over d01 and d02). |

## How to reproduce the No-Terrain run

1. Run WPS as usual to produce `geo_em.d01.nc` and `geo_em.d02.nc`.
2. Edit the input paths at the top of `make_no_terrain_geo.py` to point
   to your geogrid files, then run:
   ```bash
   python make_no_terrain_geo.py
   ```
   This writes `geo_em.d01_no_terrain.nc` and `geo_em.d02_no_terrain.nc`
   next to the originals.
3. In your WPS work directory, rename the modified files back to
   `geo_em.d0X.nc` (or symlink) and re-run `real.exe` and `wrf.exe`.

## Dependencies

- Python >= 3.9
- `numpy`, `netCDF4` (script)
- `matplotlib`, `cartopy` (plotting)

## Reference

Please cite the BCBJ paper when using this code. A DOI will be added
once the manuscript is accepted.
