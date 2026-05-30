"""
make_no_terrain_geo.py
======================

Generates the modified WPS geogrid file (`geo_em.d01_no_terrain.nc`)
used in the No-Terrain sensitivity run of the Black Sea Coastal-Barrier
Jet (BCBJ) WRF experiment.

Method
------
Inside a fixed lat/lon box covering the Kure Mountains
(39.5-43.0 deg N, 28.5-36.0 deg E) the HGT_M field is reduced to
`target_hgt = 10 m` over land. A 20-grid cosine-tapered buffer
(S-curve, weight = 0.5 * (1 - cos(pi * d/buffer))) blends the flattened
core back to the original orography to avoid an artificial step.
Ocean grid points (LANDMASK == 0) are left at their original height
so the coastline is preserved. All HGT_* fields in the file are
overwritten with the modified field.

Usage
-----
    python make_no_terrain_geo.py

Input (edit `input_files` if needed):
    D:\\geo_em.d01.nc

Output (written next to the input):
    D:\\geo_em.d01_no_terrain.nc

Drop the *_no_terrain.nc file into your WPS workdir (renaming it back
to `geo_em.d01.nc`), then run `real.exe` and `wrf.exe` as usual.
"""

import os
import shutil
import numpy as np
import netCDF4 as nc

# ---------------------------------------------------------------------------
# Settings
# ---------------------------------------------------------------------------
input_files = [r"D:\geo_em.d01.nc"]

target_hgt       = 10.0   # flattened core height [m] over land
smooth_grid_dist = 20     # buffer width [grid cells]

# Modification box (Kure Mts.)
lat_min, lat_max = 39.5, 43.0
lon_min, lon_max = 28.5, 36.0


# ---------------------------------------------------------------------------
def apply_advanced_smoothing(file_path):
    output_path = file_path.replace(".nc", "_no_terrain.nc")
    print(f"\nProcessing: {file_path}")

    shutil.copy2(file_path, output_path)
    ds = nc.Dataset(output_path, "r+")

    lats = ds.variables['XLAT_M'][0, :, :]
    lons = ds.variables['XLONG_M'][0, :, :]
    hgt = ds.variables['HGT_M'][0, :, :].copy()
    original_hgt = hgt.copy()
    landmask = ds.variables['LANDMASK'][0, :, :]

    # Signed distance to the box edges (>=0 outside, 0 inside).
    d_lat = np.maximum(lat_min - lats, lats - lat_max)
    d_lon = np.maximum(lon_min - lons, lons - lon_max)
    dist_map = np.sqrt(np.maximum(d_lat, 0) ** 2 +
                       np.maximum(d_lon, 0) ** 2)

    # Convert "grid cells" to degrees for this domain.
    deg_per_grid = np.abs(lats[1, 0] - lats[0, 0])
    buffer_deg = smooth_grid_dist * deg_per_grid

    # Cosine S-curve: 0 inside box, 1 fully outside buffer.
    weights = np.clip(dist_map / buffer_deg, 0, 1)
    weights = 0.5 * (1 - np.cos(weights * np.pi))

    # Blend on land; preserve original height over sea.
    new_hgt = (original_hgt * weights) + (target_hgt * (1 - weights))
    final_hgt = np.where(landmask == 1, new_hgt, original_hgt)

    # Overwrite all HGT_* variables (HGT_M, HGT_U, HGT_V, ...).
    hgt_vars = [v for v in ds.variables if 'HGT' in v]
    for vname in hgt_vars:
        ds.variables[vname][0, :, :] = final_hgt

    ds.sync()
    ds.close()
    print(f"  OK -> {output_path}")
    print(f"  vars overwritten: {hgt_vars}")


# ---------------------------------------------------------------------------
if __name__ == "__main__":
    for f in input_files:
        if os.path.exists(f):
            apply_advanced_smoothing(f)
        else:
            print(f"  MISSING: {f}  (skipped)")
    print("\nNo-Terrain gradient smoothing complete.")
