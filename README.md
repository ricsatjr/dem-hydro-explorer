# 🏔️ dem-hydro-explorer

> Interactive Google Colab notebook for SRTM DEM retrieval, terrain analysis, and hydrologic processing — featuring an interactive basemap, points of interest management, stream network extraction, and click-based watershed delineation. No API key required.

[![View Notebook](https://img.shields.io/badge/View-Notebook-orange?logo=jupyter)](https://nbviewer.org/github/ricsatjr/dem-hydro-explorer/blob/main/dem-hydro-explorer.ipynb)
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ricsatjr/dem-hydro-explorer/blob/main/dem-hydro-explorer.ipynb)
[![Copy to Drive](https://img.shields.io/badge/Copy%20to-Google%20Drive-blue?logo=googledrive)](https://colab.research.google.com/github/ricsatjr/dem-hydro-explorer/blob/main/dem-hydro-explorer.ipynb)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Data: SRTM](https://img.shields.io/badge/Data-SRTM%2030m-blue.svg)](https://www.earthdata.nasa.gov/sensors/srtm)
[![Open Source](https://img.shields.io/badge/Open%20Source-%E2%9C%93-brightgreen.svg)]()

---

## What It Does

**dem-hydro-explorer** is a self-contained Google Colab notebook that takes a user from an interactive web map all the way through to exported watershed boundaries — entirely in the browser, with no GIS software installation required.

Starting from a simple pan-and-zoom map interface, the user selects an area of interest, downloads elevation data automatically, and runs a standard hydrologic processing chain to extract stream networks and delineate upstream catchments. All outputs are exported in formats ready for use in QGIS, GRASS-GIS, or directly in QField on a mobile device.

Key capabilities:

- **No API key, no account** — elevation data is fetched from a public AWS S3 bucket
- **Fully interactive** — basemap navigation, point-of-interest management, click-to-delineate watershed tool, and adjustable stream threshold slider, all inside Colab
- **Standard hydrologic pipeline** — mirrors the processing steps used in QGIS, SAGA GIS, and GRASS-GIS (`r.watershed`, `r.fill.dir`)
- **QField-ready outputs** — all vector layers bundled into a single GeoPackage for direct import on Android/iOS

---

## Workflow

The notebook is organised into numbered steps that run sequentially top to bottom.

```
Step 0  →  Install dependencies (one-shot, ~60 seconds)
Step 1  →  Imports and configuration (location, DEM source, stream threshold)
Step 1.5→  Load Points of Interest (manual entry / paste GeoJSON / upload file)
Step 2  →  Browse interactive basemap (OSM, Satellite, Topo, CartoDB)
             └─ Capture bounding box of study area
Step 3  →  Download SRTM 30 m DEM for captured extent
Step 4  →  Compute elevation statistics + 4-panel terrain figure
             (shaded relief, elevation, slope, hypsometric curve)
Step 5  →  Hydrologic processing pipeline
             └─ Fill pits → Fill depressions → Resolve flats
             └─ D8 flow direction → Flow accumulation
             └─ Stream extraction → Vectorisation
Step 6  →  Interactive stream threshold tuning (slider widget)
Step 7  →  Watershed delineation
             └─ Click on map OR type coordinates
             └─ Auto-snap to highest-accumulation stream cell within search radius
             └─ Flow accumulation overlay for drainage intensity reference
             └─ Delineate upstream catchment + statistics + figure
Step 8  →  Export all results (GeoJSON + GeoPackage + GeoTIFF + PNG)
```

### Points of Interest

POIs can be loaded three ways:

| Method | How |
|--------|-----|
| Manual entry | Type name, latitude, longitude, and colour |
| Paste GeoJSON | Paste a raw GeoJSON FeatureCollection into a text area |
| Upload file | Upload a `.geojson` or zipped Shapefile (`.zip`) |

POIs are overlaid on the basemap and all output figures, and exported as a dedicated layer in the GeoPackage.

### Watershed Delineation

The pour point can be set in two ways:

- **Click on the map** — enable Click Mode, click anywhere inside or on the stream network; the tool snaps automatically to the highest-accumulation cell within a fixed pixel search radius, favouring the main channel over minor tributaries
- **Type coordinates** — enter latitude/longitude directly into the input boxes

The snapped point reports the D8 flow accumulation value and corresponding upstream drainage area in km². The delineated catchment boundary is then vectorised and statistics are computed (area, perimeter, elevation distribution, relief).

### Outputs

| File | Format | Description |
|------|--------|-------------|
| `dem.tif` | GeoTIFF | Downloaded SRTM 30 m DEM, clipped to study extent |
| `streams.geojson` | GeoJSON | Extracted stream network (line features) |
| `watershed.geojson` | GeoJSON | Delineated catchment boundary (polygon) |
| `points_of_interest.geojson` | GeoJSON | User-defined POIs (point features) |
| `dem_analysis.gpkg` | GeoPackage | All vector layers in one file — direct QField import |
| `terrain_analysis.png` | PNG | 4-panel terrain figure |
| `hydrology_analysis.png` | PNG | Flow accumulation + stream network figure |
| `watershed.png` | PNG | Catchment boundary + elevation histogram |

---

## Datasets

All datasets used are **open data** with no registration or API key required.

### SRTM 30 m (Primary DEM source)

| Property | Detail |
|----------|--------|
| Full name | Shuttle Radar Topography Mission (SRTM) 1 Arc-Second Global |
| Resolution | ~30 metres |
| Coverage | 60°N – 56°S |
| Provider | NASA / USGS |
| Access | AWS public S3 bucket (`elevation-tiles-prod/skadi/`) |
| Format | HGT binary tiles, gzip-compressed |
| License | Public domain |
| Citation | Farr, T. G., et al. (2007). The Shuttle Radar Topography Mission. *Reviews of Geophysics*, 45(2). https://doi.org/10.1029/2005RG000183 |

Tiles are fetched directly from:
```
https://s3.amazonaws.com/elevation-tiles-prod/skadi/{LAT}/{TILE}.hgt.gz
```
No AWS account, no credentials, no rate limits for standard use.

### Optional Alternative DEM Sources

If higher accuracy or different coverage is needed, the notebook supports [OpenTopography](https://opentopography.org/developers) with a free API key. Available datasets include:

| Dataset | Resolution | Coverage | Notes |
|---------|-----------|---------|-------|
| COP30 (Copernicus DEM) | ~30 m | Global | Based on TanDEM-X, excellent quality |
| NASADEM | ~30 m | 60°N – 56°S | Reprocessed SRTM with improved voids |
| AW3D30 (ALOS) | ~30 m | Global | JAXA product, good in vegetated areas |

Switch by setting `DEM_SOURCE = 'opentopography'` in the config cell.

### Basemap Tile Layers

The interactive map offers four tile layer options, all free and openly accessible:

| Layer | Provider | License |
|-------|----------|---------|
| OpenStreetMap | OpenStreetMap contributors | ODbL |
| Satellite imagery | Esri World Imagery | Esri basemap terms |
| Topographic | OpenTopoMap | CC-BY-SA |
| CartoDB Light | Carto | CC-BY |

---

## Key Libraries

All libraries used are **free and open source**.

### Geospatial Processing

| Library | Role | License |
|---------|------|---------|
| [pysheds](https://github.com/mdbartos/pysheds) | Core hydrologic engine — pit filling, flow direction, flow accumulation, stream extraction, watershed delineation | MIT |
| [rasterio](https://github.com/rasterio/rasterio) | GeoTIFF read/write, raster clipping, coordinate transforms, feature extraction | BSD |
| [GeoPandas](https://geopandas.org) | Vector data handling, GeoJSON/GeoPackage export, coordinate reference systems | BSD |
| [Shapely](https://shapely.readthedocs.io) | Geometry operations — union, centroid, boundary extraction | BSD |
| [Fiona](https://github.com/Toblerity/Fiona) | Vector file I/O backend (GeoJSON, GeoPackage) | BSD |
| [scipy](https://scipy.org) | Morphological raster operations (`binary_erosion`) | BSD |
| [NumPy](https://numpy.org) | Array operations throughout | BSD |

### Visualisation & Mapping

| Library | Role | License |
|---------|------|---------|
| [ipyleaflet](https://github.com/jupyter-widgets/ipyleaflet) | Interactive web map inside Colab (pan, zoom, click events, layer control) | MIT |
| [Matplotlib](https://matplotlib.org) | All static figures (terrain, hydrology, watershed) | PSF/BSD |
| [Pillow](https://python-pillow.org) | PNG encoding of flow accumulation overlay for ipyleaflet ImageOverlay | HPND |
| [ipywidgets](https://github.com/jupyter-widgets/ipywidgets) | UI controls — sliders, buttons, text inputs, file upload | BSD |

### Data Retrieval

| Library | Role | License |
|---------|------|---------|
| [requests](https://docs.python-requests.org) | HTTP download of SRTM tiles from AWS S3 | Apache 2.0 |
| [gzip](https://docs.python.org/3/library/gzip.html) | Decompression of `.hgt.gz` tile files | Python standard library |

---

## Dependencies

All packages are installed automatically in **Step 0** and imported in **Step 1** of the notebook. Tested on Google Colab (Python 3.12.13) with the following versions:

| Package | Version | Role |
|---------|---------|------|
| pysheds | 0.5 | Hydrologic processing |
| rasterio | 1.5.0 | Raster I/O and clipping |
| geopandas | 1.1.3 | Vector data and export |
| shapely | 2.1.2 | Geometry operations |
| fiona | 1.10.1 | Vector file I/O backend |
| ipyleaflet | 0.20.0 | Interactive web map |
| ipywidgets | 7.7.1 | UI controls and widgets |
| numpy | 2.0.2 | Array operations |
| matplotlib | 3.10.0 | Figures and visualisation |
| pillow | *(confirm version)* | Flow accumulation overlay encoding |
| scipy | 1.16.3 | Morphological raster operations |
| requests | 2.32.4 | SRTM tile download |
| traitlets | 5.7.1 | Widget trait validation |

> These versions reflect the Google Colab environment as of 7 April 2026. Colab updates its base environment periodically — if you encounter issues after a Colab update, pin the versions using `requirements.txt` (see below).

### Running locally (outside Colab)

A `requirements.txt` and `environment.yml` are provided in the repository root for users who want to run the notebook in a local Jupyter environment.

```bash
# pip
pip install -r requirements.txt

# conda
conda env create -f environment.yml
conda activate dem-hydro-explorer
```

---

## Usage

1. Open the notebook in Google Colab
2. Run **Step 0** to install dependencies (once per session)
3. Run **Step 1** — adjust the config block if needed (default location: Banaue Rice Terraces, Philippines)
4. Run all cells top to bottom
5. In **Step 7**, enable Click Mode on the map and click a point to delineate a watershed
6. Run **Step 8** to export all results

> **Tip:** After export, download `dem_analysis.gpkg` and open it directly in QField on your phone or tablet — all layers (streams, watershed, POIs) load at once without needing QGIS desktop.

---

## Compatibility

| Environment | Status |
|-------------|--------|
| Google Colab (recommended) | ✅ Tested |
| Jupyter Lab (local) | ✅ Should work |
| Jupyter Notebook classic | ⚠️ Widget rendering may vary |
| VS Code Jupyter | ⚠️ ipyleaflet support limited |

Python 3.10+ required.

---

## Acknowledgements

- NASA and USGS for the SRTM dataset
- AWS for hosting the elevation tiles as a public dataset
- Matt Bartos for [pysheds](https://github.com/mdbartos/pysheds), the hydrologic processing backbone of this notebook
- The OpenStreetMap, OpenTopoMap, and CartoDB communities for open basemap tiles

---

## License

This project is licensed under the **GNU General Public License v3.0** — see [LICENSE](LICENSE) for details.

All dependencies are licensed under MIT, BSD, PSF, Apache 2.0, or HPND terms, which are compatible with GPLv3.
