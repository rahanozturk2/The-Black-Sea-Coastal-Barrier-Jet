# No-Terrain WRF sensitivity experiment

Companion code, geogrid files, and figures for the No-Terrain sensitivity
run referenced in **The Black Sea Coastal-Barrier Jet** (MWR submission,
Ozturk et al.).

## What this is

A controlled experiment that removes all orographic forcing from the
WRF outer domain (d01, 5 km) to isolate the role of the Kure Mountains
and the wider Anatolian relief in maintaining the Black Sea
Coastal-Barrier Jet (BCBJ).

Every grid point in `geo_em.d01.nc` is rewritten as a function of the
WPS LANDMASK field:

| Where | HGT_M is set to |
|---|---|
| LANDMASK == 1 (land) | **10 m** |
| LANDMASK == 0 (sea)  | **0 m** |

No bounding box, no buffer smoothing -- the whole d01 domain becomes a
flat plate. All other WPS / namelist settings are identical to the
Control run.

## Files

| File | What it is |
|---|---|
| `make_no_terrain_geo.py` | Script that rewrites the WPS geogrid (`geo_em.d01.nc` -> `geo_em.d01_no_terrain.nc`). |
| `geo_em.d01.nc` | Original WPS geogrid (Control). |
| `geo_em.d01_no_terrain.nc` | Flattened geogrid used by the No-Terrain WRF run. |
| `terrain_control.png` | Terrain map, Control (default WPS geogrid). |
| `terrain_noterrain.png` | Terrain map after No-Terrain modification. |
| `terrain_control_vs_noterrain.png` | Side-by-side comparison. |
| `_make_terrain_pngs.py` | Plotting script used to produce the PNGs above. |

## How to reproduce the No-Terrain run

The exact geogrid we used is shipped here as `geo_em.d01_no_terrain.nc`.
To regenerate it yourself from a fresh WPS run:

1. Run WPS as usual to produce `geo_em.d01.nc`.
2. Edit the input path at the top of `make_no_terrain_geo.py` to point
   to your geogrid file, then run:
   ```bash
   python make_no_terrain_geo.py
   ```
3. In your WPS work directory, rename the modified file back to
   `geo_em.d01.nc` (or symlink) and re-run `real.exe` and `wrf.exe`.

## Dependencies

- Python >= 3.9
- `numpy`, `netCDF4` (script)
- `matplotlib`, `cartopy` (plotting)

## Reference

Please cite the BCBJ paper when using this code. A DOI will be added
once the manuscript is accepted.
