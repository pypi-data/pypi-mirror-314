# Coastal Resilience Utilities
This repository contains utilities for coastal resilience analysis and design.

## Contents
- `damage_assessment`: damage assessments based on earth observation data and National Structure Inventory.
- `damage_assessment_usvi`: damage assessments based on low-res NSI grids + OpenBuildings 
- `mosaic`: Mosaicking datasets.
- `summary_stats`: Summarize raster datasets using vector points and polygons.
- `utils`: A variety of functionality for doing geospatial analysis.  Rasterize, vectorize, fetch features from OSM/OpenBuildings/ArcOnline, extract values from rasters.

## Installation
The recommended way to install this repo is to use the provided `Makefile` to build a Docker image.

For example:
```bash
EXTRA_DOCKER_ARGS="-v <YOUR DATA DIRECTORY>:/data -v /cccr-lab:/cccr-lab" make bash-terminal
```

There are two env files:
- `.env`, which at this moment just contains GCP credentials
- `.data.env`, which maps files necessary for damage assessment

Note that it's a little tricky to guarantee out-of-the-box until we get more developers actively using this repo, but I do attempt to deploy this on multiple computers and make sure things work.  If you have trouble let's work it out!

## Examples
Check out the testing directory for examples on running analysis.

There are two other relevant repos in Gitlab:
- Datacube, which basically scales raster analyses
- GeospatialServices, which runs a variety of servers such as:
  - Jupyter for an analysis env
  - Prefect for reproducibility
  - Tile servers for app development

You don't need either to run, but the examples in GeospatialServices/Jupyter/notebooks are useful to understand using damage assessment.

## Schematic
The Figjam schematic can be found [here](https://git.ucsc.edu/chlowrie/coastal-resilience-utilities/-/blob/main/coastal_resilience_utilities/damage_assessment/damage_assessment.py?ref_type=heads)