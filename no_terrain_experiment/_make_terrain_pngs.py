"""
Generate side-by-side terrain PNGs (Control vs No-Terrain) for the
BCBJ No-Terrain WRF sensitivity experiment.
Reads pre-built geo_em.d02.nc (control) and geo_em.d02_no_terrain.nc.
"""
import os
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import netCDF4 as nc

GEO_FILES = {
    'd02': (r"D:\Verisetleri\BCBJ\WRF\TEST1_348\geo_em.d02.nc",
            r"D:\Verisetleri\BCBJ\WRF\TEST1_348\geo_em.d02_no_terrain.nc",
            [26, 38, 38, 45]),     # extent: lon_min, lon_max, lat_min, lat_max
    'd01': (r"D:\Verisetleri\BCBJ\WRF\TEST1_348\geo_em.d01.nc",
            r"D:\Verisetleri\BCBJ\WRF\TEST1_348\geo_em.d01_no_terrain.nc",
            [22, 42, 36, 48]),
}
OUT_DIR  = r"D:\Verisetleri\BCBJ\code_release\no_terrain_experiment"
os.makedirs(OUT_DIR, exist_ok=True)

# Modification region (Kure Mts.) used in make_no_terrain_geo.py
LAT_MIN, LAT_MAX = 39.5, 43.0
LON_MIN, LON_MAX = 28.5, 36.0


def load_geo(path):
    ds = nc.Dataset(path)
    lat  = ds.variables['XLAT_M'][0, :, :]
    lon  = ds.variables['XLONG_M'][0, :, :]
    hgt  = ds.variables['HGT_M'][0, :, :]
    mask = ds.variables['LANDMASK'][0, :, :]
    ds.close()
    return lat, lon, hgt, mask


def draw_panel(ax, lon, lat, hgt, title, panel, extent):
    ax.add_feature(cfeature.COASTLINE, linewidth=1.4, edgecolor='black', zorder=5)
    mesh = ax.pcolormesh(lon, lat, hgt, cmap='terrain',
                         vmin=0, vmax=2000, shading='auto',
                         transform=ccrs.PlateCarree())
    box_lon = [LON_MIN, LON_MAX, LON_MAX, LON_MIN, LON_MIN]
    box_lat = [LAT_MIN, LAT_MIN, LAT_MAX, LAT_MAX, LAT_MIN]
    ax.plot(box_lon, box_lat, color='red', linewidth=1.6, linestyle='--',
            transform=ccrs.PlateCarree(), label='Modification region')
    ax.set_extent(extent, crs=ccrs.PlateCarree())
    gl = ax.gridlines(draw_labels=True, linewidth=0.6, color='gray',
                      alpha=0.5, linestyle=':')
    gl.top_labels = False
    gl.right_labels = False
    gl.xlabel_style = {'size': 11}
    gl.ylabel_style = {'size': 11}
    ax.set_title(title, fontsize=13, fontweight='bold', pad=10)
    ax.text(0.018, 0.965, panel, transform=ax.transAxes,
            fontsize=13, fontweight='bold', va='top', ha='left',
            bbox=dict(boxstyle='round,pad=0.30', facecolor='white',
                      edgecolor='black', linewidth=0.8, alpha=0.92))
    return mesh


def make_two_panel(geo_ctrl, geo_nter, extent, suffix):
    lat_c, lon_c, hgt_c, _ = load_geo(geo_ctrl)
    lat_n, lon_n, hgt_n, _ = load_geo(geo_nter)

    plt.rcParams.update({'font.family': 'serif', 'font.size': 11})
    fig, axs = plt.subplots(1, 2, figsize=(13, 5.8),
                            subplot_kw={'projection': ccrs.PlateCarree()})
    plt.subplots_adjust(wspace=0.08, right=0.90)

    m1 = draw_panel(axs[0], lon_c, lat_c, hgt_c,
                    "Control (WPS default terrain)", "(a)", extent)
    draw_panel(axs[1], lon_n, lat_n, hgt_n,
               "No-Terrain (Kure Mts. flattened to 10 m)", "(b)", extent)
    axs[0].legend(loc='lower right', fontsize=9, frameon=True,
                  fancybox=False, edgecolor='black')

    cax = fig.add_axes([0.915, 0.16, 0.012, 0.70])
    cb = fig.colorbar(m1, cax=cax)
    cb.set_label('Terrain height (m)', fontsize=12, fontweight='bold',
                 rotation=270, labelpad=18)
    cb.ax.tick_params(labelsize=10)

    fig.suptitle(f"WRF {suffix} terrain  -  Control vs No-Terrain sensitivity run",
                 fontsize=14, fontweight='bold', y=0.99)

    out = os.path.join(OUT_DIR, f"terrain_control_vs_noterrain_{suffix}.png")
    plt.savefig(out, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {out}")


def make_single(path, label, panel_title, fname, extent):
    lat, lon, hgt, _ = load_geo(path)
    plt.rcParams.update({'font.family': 'serif', 'font.size': 11})
    fig = plt.figure(figsize=(7.2, 5.8))
    ax = plt.axes(projection=ccrs.PlateCarree())
    mesh = draw_panel(ax, lon, lat, hgt, panel_title, label, extent)
    ax.legend(loc='lower right', fontsize=9, frameon=True,
              fancybox=False, edgecolor='black')
    cax = fig.add_axes([0.91, 0.13, 0.022, 0.74])
    cb = fig.colorbar(mesh, cax=cax)
    cb.set_label('Terrain height (m)', fontsize=12, fontweight='bold',
                 rotation=270, labelpad=18)
    cb.ax.tick_params(labelsize=10)
    out = os.path.join(OUT_DIR, fname)
    plt.savefig(out, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {out}")


if __name__ == "__main__":
    for dom, (ctrl, nter, extent) in GEO_FILES.items():
        make_single(ctrl, "(a)", f"Control - {dom} (WPS default terrain)",
                    f"terrain_control_{dom}.png", extent)
        make_single(nter, "(b)", f"No-Terrain - {dom} (Kure Mts. flattened to 10 m)",
                    f"terrain_noterrain_{dom}.png", extent)
        make_two_panel(ctrl, nter, extent, dom)
    print("Done.")
