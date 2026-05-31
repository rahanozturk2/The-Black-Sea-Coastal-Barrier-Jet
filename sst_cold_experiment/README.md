# SST-Cold WRF sensitivity experiment

Companion code for the SST-Cold sensitivity run referenced in **The Black
Sea Coastal-Barrier Jet** (MWR submission, Ozturk et al.).

## What this is

A controlled experiment that imposes a uniform **-5 K** Sea Surface
Temperature anomaly over the entire Black Sea to test the response of
the BCBJ to a colder marine surface (an exaggerated upwelling /
cold-tongue analog).

The perturbation is applied directly to the WPS intermediate files
(`met_em.d0*.nc`) so it propagates cleanly through `real.exe` and is
imposed throughout the WRF simulation (with `sst_update = 1`).

| Field | Action |
|---|---|
| `SST`      | -5 K everywhere `LANDMASK == 0` |
| `SKINTEMP` | -5 K everywhere `LANDMASK == 0` |
| `TT` (air temperature profile) | **unchanged** -- the lower atmosphere is allowed to re-equilibrate inside WRF |
| Land surface fields | **unchanged** |

Both the outer (d01) and inner (d02) domains are modified together via
a single glob `met_em.d0*.nc`.

## Files

| File | What it is |
|---|---|
| `make_sst_cold_metem.py` | Script that copies the original met_em files to `mod_met_em.*`, applies the SST anomaly, then renames the modified files in place so `real.exe` ingests them. Originals are moved to a `backup_originals/` sibling folder. |

## How to reproduce the SST-Cold run

1. Run WPS through `metgrid.exe` as usual to produce the
   `met_em.d0*.nc` files for the Control run.
2. Edit `folder_path` at the top of `make_sst_cold_metem.py` to point
   at the directory containing those met_em files, then run:
   ```bash
   python make_sst_cold_metem.py
   ```
   This writes `mod_met_em.*` copies, then activates them (originals
   are saved under `backup_originals/`).
3. Run `real.exe` and `wrf.exe` against the modified met_em files.

## Dependencies

- Python >= 3.9
- `numpy`, `netCDF4`

## Reference

Please cite the BCBJ paper when using this code. A DOI will be added
once the manuscript is accepted.
