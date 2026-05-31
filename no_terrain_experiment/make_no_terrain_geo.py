"""
make_no_terrain_geo.py
======================

Builds the modified WPS geogrid file (`geo_em.d01_no_terrain.nc`) used
in the No-Terrain sensitivity run of the Black Sea Coastal-Barrier Jet
(BCBJ) WRF experiment.

Method (BCJ.ipynb, Cell 15)
---------------------------
Every grid point is rewritten as a function of LANDMASK:

    HGT_M = 10.0  where LANDMASK == 1  (all land flattened to 10 m)
    HGT_M =  0.0  where LANDMASK == 0  (all sea pinned to 0 m)

There is no bounding box and no buffer-smoothing -- the whole d01
domain is flattened. This is the simplest possible "remove all
orographic forcing" experiment, designed to isolate the role of the
Kure Mountains (and the wider Anatolian relief) in maintaining the
BCBJ. Compared with the Control run, all other WPS / namelist
settings are identical.

Usage
-----
    python make_no_terrain_geo.py

Input (edit `input_file` if needed):
    D:\\geo_em.d01.nc

Output (written next to the input):
    D:\\geo_em.d01_no_terrain.nc
"""

import os
import shutil
import netCDF4 as nc

# ---------------------------------------------------------------------------
# Settings
# ---------------------------------------------------------------------------
input_file  = r"D:\geo_em.d01.nc"
output_file = r"D:\geo_em.d01_no_terrain.nc"

land_height = 10.0   # m, applied wherever LANDMASK == 1
sea_height  = 0.0    # m, applied wherever LANDMASK == 0


# ---------------------------------------------------------------------------
def flatten_terrain(in_path, out_path):
    print(f"Processing: {in_path}")
    shutil.copy(in_path, out_path)

    ds = nc.Dataset(out_path, 'r+')
    hgt = ds.variables['HGT_M']
    landmask = ds.variables['LANDMASK']

    hgt_data = hgt[:]
    land = landmask[:]
    hgt_data[land == 0] = sea_height
    hgt_data[land == 1] = land_height
    hgt[:] = hgt_data

    ds.close()
    print(f"  OK -> {out_path}")
    print(f"  LANDMASK == 1 -> HGT_M = {land_height} m")
    print(f"  LANDMASK == 0 -> HGT_M = {sea_height} m")


# ---------------------------------------------------------------------------
if __name__ == "__main__":
    if not os.path.exists(input_file):
        print(f"MISSING: {input_file}")
    else:
        flatten_terrain(input_file, output_file)
        print("\nNo-Terrain modification complete.")
