from summary_stats.summary_stats import summary_stats, summary_stats_nearest
import geopandas as gpd
import rioxarray as rxr
from coastal_resilience_utilities import get_project_root
from pathlib import Path

import logging

logging.basicConfig()
logging.root.setLevel(logging.INFO)

PACKAGE_ROOT = get_project_root()

FLOODING = Path(PACKAGE_ROOT) / "test/data/JAM_WaterDepth_Historic_S1_Tr50.tif"
GEOGRAPHIES = Path(PACKAGE_ROOT) / "test/data/gadm_jamaica.gpkg"

def test_summary_stats():
    gdf = gpd.read_file(GEOGRAPHIES)
    flooding = rxr.open_rasterio(FLOODING).isel(band=0).to_dataset(name='flooding')
    summary_stats(gdf, flooding)
    

def test_summary_stats_nearest():
    PTS = gpd.read_file("test/data/openbuildings/StCroix_FZ_rp100_base_damages_openbuildings.gpkg")
    LINES = gpd.read_file("damage_assessment_usvi/USVI_data/CoastalSegments_ForBorja/StCroix_Coastline_Intersect_SummaryPts_TransOrder.shp")
    LINES = LINES.dissolve(by='TransOrder').reset_index()
    summary_stats_nearest(PTS, LINES, "TransOrder", ["damages"], ["mean", "max", "sum"])
    
def test_aggregate_points_to_dataarray():
    PTS = gpd.read_file("test/data/openbuildings/StCroix_FZ_rp100_base_damages_openbuildings.gpkg")
    GRID = rxr.open_rasterio("test/data/openbuildings/StCroix_FZ_rp100_base_flood_depth.tif")
    # logging.info(PTS)
    # return
    # aggregate_points_to_dataarray(GRID, PTS, "damages")
    