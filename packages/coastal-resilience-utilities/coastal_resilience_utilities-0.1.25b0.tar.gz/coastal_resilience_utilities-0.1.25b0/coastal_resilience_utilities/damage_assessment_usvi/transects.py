import geopandas as gpd
from damage_assessment_usvi.aev_usvi import POINTS_MERGED
from damage_assessment_usvi.damages_usvi import OUTPUTS
from summary_stats.summary_stats import summary_stats_nearest
import os
import numpy as np

TRANSECTS = os.path.join(OUTPUTS, "transects")
if not os.path.exists(TRANSECTS):
    os.makedirs(TRANSECTS)

transects = {
    "StCroix": "/cccr-lab/001_projects/005_USGS_USVI/old_15c_USGS_USVI/01_DATA/Transects/Transects_USVI_StCroix_PAEK5000_100mspacing_500smooth_3000on6000offlength_mod.shp", 
    "StThomas": "/cccr-lab/001_projects/005_USGS_USVI/old_15c_USGS_USVI/01_DATA/Transects/Transects_USVI_StThom_PAEK5000_100mspacing_500smooth_2000on6000offlength.shp", 
    "StJohn": "/cccr-lab/001_projects/005_USGS_USVI/old_15c_USGS_USVI/01_DATA/Transects/Transects_USVI_StJohn_PAEK5000_100mspacing_500smooth_2000onMultipleofflength.shp"
}

for island in ("StCroix", "StThomas", "StJohn"):
    OUTPATH = os.path.join(TRANSECTS, island)
    if not os.path.exists(OUTPATH):
        os.makedirs(OUTPATH)
        
    x = gpd.read_file(os.path.join(POINTS_MERGED, f'{island}.gpkg'))
    t = gpd.read_file(transects[island])
    ss = summary_stats_nearest(
        x, 
        t, 
        "TransOrder", 
        [c for c in x.columns if np.any([i in c for i in ("damages", "flooding")])],
        ["sum"]
    )
    ss.to_file(os.path.join(OUTPATH, f"{island}_transects_with_damage_totals_alltransects.gpkg"))
    
    ss = summary_stats_nearest(
        x, 
        t[t["CoralCover"] == 1], 
        "TransOrder", 
        [c for c in x.columns if np.any([i in c for i in ("damages", "flooding")])],
        ["sum"]
    )
    ss.to_file(os.path.join(OUTPATH, f"{island}_transects_with_damage_totals_onlycoraltransects.gpkg"))
    print(ss)
