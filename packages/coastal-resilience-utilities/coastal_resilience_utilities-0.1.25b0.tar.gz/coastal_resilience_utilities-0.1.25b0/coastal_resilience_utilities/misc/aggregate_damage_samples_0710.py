import geopandas as gpd
import pandas as pd
from glob import glob
import os
import re
import numpy as np

INDIR="/cccr-lab/001_projects/002_nbs-adapt/006_models/SFINCS_PROPAGATIONS/JAM/04_Raster_outputs/JAM-CompareBoundaryResults"
# INDIR="/cccr-lab/001_projects/002_nbs-adapt/006_models/SFINCS_PROPAGATIONS/DOM_01/04_Raster_outputs/DOM-CompareBoundaryResults"
DEFAULT_COLUMNS=["GID", "NAME"]

pattern = re.compile(r'^Damages.*SummaryStats.*\.gpkg$')

files = [f for f in glob(os.path.join(INDIR, '*')) if pattern.search(os.path.basename(f))]
print(files)

buff = []
for idx, f in enumerate(files):
    print(f)
    fname = f.split('/')[-1].split('.')[0]
    scenario = fname.split('_')[2]
    prev_new = fname.split('_')[4]
    gdf = gpd.read_file(f)
    gdf = gdf.rename(columns={c: f'{c}_{scenario}_{prev_new}' for c in gdf.columns})
    gdf = gdf.drop(columns=[c for c in gdf.columns if "geometry" in c])
    if idx == 0:
        columns_to_rename = [c for c in gdf.columns if np.any([i in c for i in DEFAULT_COLUMNS])]
        gdf = gdf.rename(columns={c: '_'.join(c.split('_')[0:2]) for c in columns_to_rename})
    if idx > 0:
        columns_to_drop = [c for c in gdf.columns if np.any([i in c for i in DEFAULT_COLUMNS])]
        gdf = gdf.drop(columns=columns_to_drop)
    buff.append(gdf)
    
gdf = pd.concat(buff, axis=1)
print(gdf.columns)
gdf.to_csv(os.path.join(INDIR, "summary_results_0709.csv"))