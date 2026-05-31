"""
make_inv_enh_metem.py
=====================

Builds the modified WPS met_em files used in the Inversion-Enhanced
(Inv-Enh) sensitivity run of the Black Sea Coastal-Barrier Jet (BCBJ)
WRF experiment.

Method (BCJ.ipynb, Cells 10 and 11)
-----------------------------------
For each of the four lead-in lateral-boundary times
(15_18, 16_00, 16_06, 16_12 UTC) we sharpen the elevated capping
inversion by adding a positive temperature perturbation at four
pressure levels in the `TT` field of the met_em files:

| Pressure level | Boost |
|---:|---:|
| 1000 hPa | +2.0 K |
|  975 hPa | +5.0 K |
|  950 hPa | +5.0 K |
|  925 hPa | +2.5 K |

Domain handling
~~~~~~~~~~~~~~~

- **d01 (5 km outer domain)** -- the boost is applied inside a
  bounding box (40.5-45.0 deg N, 27.5-35.5 deg E) covering the
  jet-relevant western Black Sea, with a 10-grid linear taper outside
  the box (Euclidean distance transform) so the perturbation decays
  smoothly to zero at the lateral boundaries.

- **d02 (1 km nested domain)** -- the inner domain sits entirely
  inside the bounding box, so the boost is applied uniformly at the
  four pressure levels with no spatial weighting.

In both domains we copy the source file to `NETCDF4_CLASSIC` format
to preserve every global attribute and dimension that `real.exe`
requires (failing to do this is the most common reason modified
met_em files crash WRF).

Usage
-----
    python make_inv_enh_metem.py

Edit `input_dir` / `output_dir` at the top to point at your case
directories. The Inv-Enh run in the paper used `1d/org/` as input and
`1d/modified/` as output.
"""

import glob
import os

import numpy as np
from netCDF4 import Dataset
from scipy.ndimage import distance_transform_edt

# ---------------------------------------------------------------------------
# Settings
# ---------------------------------------------------------------------------
input_dir  = r"C:\Rahan\ITU\DR_TEZ\BCJ\WRF\TEST1_348\1d\org"
output_dir = r"C:\Rahan\ITU\DR_TEZ\BCJ\WRF\TEST1_348\1d\modified"

target_boosts  = {1000: 2.0, 975: 5.0, 950: 5.0, 925: 2.5}   # hPa -> Kelvin
target_times   = ["15_18", "16_00", "16_06", "16_12"]

# d01 spatial mask
lat_min, lat_max = 40.5, 45.0
lon_min, lon_max = 27.5, 35.5
buffer_grids     = 10


# ---------------------------------------------------------------------------
def _copy_skeleton(src, dst, skip_var):
    """Clone all global attrs / dims / vars from src into dst, leaving
    `skip_var` un-filled so the caller can write its own data."""
    dst.setncatts({k: src.getncattr(k) for k in src.ncattrs()})
    for name, dim in src.dimensions.items():
        dst.createDimension(name, len(dim) if not dim.isunlimited() else None)
    for name, var in src.variables.items():
        new = dst.createVariable(name, var.datatype, var.dimensions)
        new.setncatts(src[name].__dict__)
        if name != skip_var:
            new[:] = var[:]
    return dst.variables[skip_var]


def process_d01():
    files = sorted(glob.glob(os.path.join(input_dir, "met_em.d01*")))
    target_files = [f for f in files if any(t in f for t in target_times)]
    if not target_files:
        print("d01: no target files found")
        return

    for fpath in target_files:
        fname = os.path.basename(fpath)
        new_path = os.path.join(output_dir, fname)
        print(f"\nd01: {fname}")

        with Dataset(fpath, 'r') as src, \
             Dataset(new_path, 'w', format='NETCDF4_CLASSIC') as dst:

            tt_out = _copy_skeleton(src, dst, skip_var='TT')

            lats = src.variables['XLAT_M'][0, :, :]
            lons = src.variables['XLONG_M'][0, :, :]
            pres = src.variables['PRES'][0, :, :, :] / 100.0   # Pa -> hPa
            tt   = src.variables['TT'][0, :, :, :].copy()

            core_mask = ((lats >= lat_min) & (lats <= lat_max) &
                         (lons >= lon_min) & (lons <= lon_max))
            dist_mask = np.ones_like(core_mask)
            dist_mask[core_mask] = 0
            dist_to_core = distance_transform_edt(dist_mask)
            weight = np.where(
                core_mask, 1.0,
                np.maximum(0, (buffer_grids - dist_to_core) / buffer_grids),
            )

            mid_y, mid_x = tt.shape[1] // 2, tt.shape[2] // 2
            for p_lvl, boost in target_boosts.items():
                idx = np.argmin(np.abs(pres[:, mid_y, mid_x] - p_lvl))
                tt[idx, :, :] += (boost * weight)
                print(f"  level {p_lvl:>5} hPa (idx {idx:2d})  boost +{boost} K (weighted)")

            tt_out[0, :, :, :] = tt


def process_d02():
    files = sorted(glob.glob(os.path.join(input_dir, "met_em.d02*")))
    target_files = [f for f in files if any(t in f for t in target_times)]
    if not target_files:
        print("d02: no target files found")
        return

    for fpath in target_files:
        fname = os.path.basename(fpath)
        new_path = os.path.join(output_dir, fname)
        print(f"\nd02: {fname}")

        with Dataset(fpath, 'r') as src, \
             Dataset(new_path, 'w', format='NETCDF4_CLASSIC') as dst:

            tt_out = _copy_skeleton(src, dst, skip_var='TT')

            pres = src.variables['PRES'][0, :, :, :] / 100.0
            tt   = src.variables['TT'][0, :, :, :].copy()
            mid_y, mid_x = tt.shape[1] // 2, tt.shape[2] // 2

            for p_lvl, boost in target_boosts.items():
                idx = np.argmin(np.abs(pres[:, mid_y, mid_x] - p_lvl))
                tt[idx, :, :] += boost           # d02 is fully inside core
                print(f"  level {p_lvl:>5} hPa (idx {idx:2d})  boost +{boost} K (uniform)")

            tt_out[0, :, :, :] = tt


# ---------------------------------------------------------------------------
if __name__ == "__main__":
    os.makedirs(output_dir, exist_ok=True)
    process_d01()
    process_d02()
    print("\nInv-Enh modification complete.")
