# Inv-Enh (Inversion-Enhanced) WRF sensitivity experiment

Companion code for the Inversion-Enhanced (Inv-Enh) sensitivity run
referenced in **The Black Sea Coastal-Barrier Jet** (MWR submission,
Ozturk et al.).

## What this is

A controlled experiment that **sharpens the capping elevated inversion**
above the western Black Sea during the spin-up of Case 1, so the
sensitivity of the BCBJ to a stronger lid can be quantified directly.

The perturbation is applied to the `TT` (air-temperature profile) field
of the WPS intermediate files at the four lead-in lateral-boundary times
(15 Sep 18 UTC, 16 Sep 00, 06, 12 UTC). At four target pressure
levels the temperature is raised by a fixed boost:

| Pressure level | Boost |
|---:|---:|
| 1000 hPa | +2.0 K |
|  975 hPa | +5.0 K |
|  950 hPa | +5.0 K |
|  925 hPa | +2.5 K |

The 950-975 hPa double-peak sets the lid; the 1000 hPa and 925 hPa
shoulders avoid a delta-function profile that would be smoothed away in
the first vertical-interpolation step of `real.exe`.

### Domain handling

| Domain | How the boost is applied |
|---|---|
| **d01** (5 km outer) | Inside a 40.5-45.0 deg N, 27.5-35.5 deg E bounding box at full strength, with a 10-grid linear taper outside the box (Euclidean distance transform) so the perturbation decays smoothly to zero at the lateral boundaries. |
| **d02** (1 km inner) | The inner nest sits fully inside the bounding box, so the boost is applied uniformly at the four pressure levels. |

Other met_em variables (`SST`, `SKINTEMP`, `LANDMASK`, soil moisture,
etc.) are passed through untouched.

`NETCDF4_CLASSIC` is used for the output so that every global attribute
and dimension that `real.exe` needs survives the rewrite (this is the
most common reason hand-edited met_em files crash WRF).

## Files

| File | What it is |
|---|---|
| `make_inv_enh_metem.py` | Script that writes modified met_em files for d01 (with spatial taper) and d02 (uniform). Reads from `input_dir`, writes to `output_dir`. |

## How to reproduce the Inv-Enh run

1. Run WPS through `metgrid.exe` as usual to produce the Control
   `met_em.d0*.nc` files. Keep a clean copy under
   `<case>/1d/org/`.
2. Edit `input_dir` / `output_dir` at the top of
   `make_inv_enh_metem.py` and run:
   ```bash
   python make_inv_enh_metem.py
   ```
   The four required time-stamps for d01 and d02 are written under
   `output_dir`.
3. Move (or symlink) the modified met_em files into the WRF run
   directory and re-run `real.exe` and `wrf.exe`. Only the lateral
   boundary update times need the perturbed files; the rest of the run
   evolves freely.

## Dependencies

- Python >= 3.9
- `numpy`, `scipy`, `netCDF4`

## Reference

Please cite the BCBJ paper when using this code. A DOI will be added
once the manuscript is accepted.
