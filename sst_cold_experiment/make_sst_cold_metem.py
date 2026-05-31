"""
make_sst_cold_metem.py
======================

Builds the modified WPS met_em files used in the SST-Cold sensitivity
run of the Black Sea Coastal-Barrier Jet (BCBJ) WRF experiment.

Method (BCJ.ipynb, Cells 3 and 7)
---------------------------------
For every `met_em.d0*.nc` file in `folder_path`:

  1. Copy the original to `mod_met_em.d0*.nc` (full byte-for-byte copy
     so all global attributes and dimensions survive).
  2. Subtract `delta_t = 5.0` K from `SST` and `SKINTEMP` everywhere
     `LANDMASK == 0` (i.e. all sea points). Land values are untouched.
  3. Air-temperature profile (`TT`) is NOT modified -- only the surface
     boundary condition is perturbed; the boundary layer is allowed to
     re-equilibrate inside WRF.

A second pass (`activate_modified_files`) backs up the original
met_em files into `backup_originals/` and renames the `mod_met_em.*`
files to their canonical `met_em.*` names so that `real.exe` picks
them up unchanged.

Usage
-----
    python make_sst_cold_metem.py

Edit `folder_path` at the top to point at your case directory.

The SST-Cold run in the paper used `folder_path =
.../TEST1_348/1c/met_em`.
"""

import glob
import os
import shutil
import sys

import numpy as np
from netCDF4 import Dataset

# ---------------------------------------------------------------------------
# Settings
# ---------------------------------------------------------------------------
folder_path = r"C:\Rahan\ITU\DR_TEZ\BCJ\WRF\TEST1_348\1c\met_em"
delta_t     = 5.0   # K  -- subtracted from SST and SKINTEMP over sea


# ---------------------------------------------------------------------------
def cool_sst_over_sea(folder):
    """Write mod_met_em.* copies with SST - delta_t, SKINTEMP - delta_t."""
    files = sorted(glob.glob(os.path.join(folder, "met_em.d0*.nc")))
    if not files:
        print(f"No met_em files in {folder}")
        return

    print(f"--- SST-Cold modification: SST - {delta_t:.1f} K over sea ---")
    print(f"  files     : {len(files)}")
    print(f"  target    : LANDMASK == 0  (all sea points)\n")

    for idx, f_path in enumerate(files):
        base_name = os.path.basename(f_path)
        new_f_path = os.path.join(os.path.dirname(f_path), "mod_" + base_name)

        shutil.copy2(f_path, new_f_path)
        ds = Dataset(new_f_path, 'r+')

        landmask = ds.variables['LANDMASK'][0, :, :]
        sea_mask = (landmask == 0)

        sst_array  = ds.variables['SST'][0, :, :]
        skin_array = ds.variables['SKINTEMP'][0, :, :]

        old_avg = np.mean(sst_array[sea_mask]) - 273.15
        sst_array[sea_mask]  -= delta_t
        skin_array[sea_mask] -= delta_t
        new_avg = np.mean(sst_array[sea_mask]) - 273.15

        ds.variables['SST'][0, :, :]      = sst_array
        ds.variables['SKINTEMP'][0, :, :] = skin_array
        ds.close()

        sys.stdout.write(
            f"\r[{idx + 1}/{len(files)}] {base_name}  "
            f"sea-mean SST  {old_avg:6.2f}C -> {new_avg:6.2f}C"
        )
        sys.stdout.flush()
    print("\n  done.\n")


# ---------------------------------------------------------------------------
def activate_modified_files(folder):
    """Move originals to backup/ and rename mod_met_em.* -> met_em.*."""
    backup_folder = os.path.join(folder, "backup_originals")
    os.makedirs(backup_folder, exist_ok=True)
    print(f"--- Activating modified files (backup -> {backup_folder}) ---")

    for filename in os.listdir(folder):
        if not filename.endswith(".nc"):
            continue
        old_path = os.path.join(folder, filename)
        if not filename.startswith("mod_"):
            shutil.move(old_path, os.path.join(backup_folder, filename))
        else:
            new_name = filename.replace("mod_", "", 1)
            os.rename(old_path, os.path.join(folder, new_name))
    print("  WRF is ready to ingest the SST-Cold met_em files.\n")


# ---------------------------------------------------------------------------
if __name__ == "__main__":
    cool_sst_over_sea(folder_path)
    activate_modified_files(folder_path)
    print("SST-Cold modification complete.")
