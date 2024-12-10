import geopandas as gpd
import pandas as pd

from string import Template
import os
from damage_assessment_usvi.damages_usvi import OUTPUTS as BASEDIR, POINTS as INPUTS
from damage_assessment_usvi.helpers import parse_scenarios, compute_cartesian_product
from damage_assessment.damage_assessment import AEV_geodataframe
from utils.geo import merge_geodataframes
from summary_stats.summary_stats import summary_stats_nearest

from functools import partial

import logging

logging.basicConfig()
logging.root.setLevel(logging.INFO)

# Constants
AEVDIR = os.path.join(BASEDIR, "points")
POINTS_MERGED = os.path.join(BASEDIR, "points_merged")
BANDSDIR = os.path.join(BASEDIR, "bands")
LINESDIR = os.path.join(BASEDIR, "lines")
if not os.path.exists(BANDSDIR):
    os.makedirs(BANDSDIR)
if not os.path.exists(POINTS_MERGED):
    os.makedirs(POINTS_MERGED)
if not os.path.exists(LINESDIR):
    os.makedirs(LINESDIR)
    
id_prefix = "AEV-Econ"
rps = (10, 50, 100, 500)
template = "${island}_FZ_rp{rp}_${scen}_flood_depth"
_template = Template(template)


def process_scenario(scenario, basedir, rps, template):
    def pathgen(rp, formatter):
        return os.path.join(basedir, formatter.format(rp=rp)+'.gpkg')
    
    formatter = template.safe_substitute(scenario)
    gdf = merge_geodataframes(
        partial(pathgen, formatter=formatter),
        inputs=rps,
        input_formatter=lambda rp: f'rp{rp}'
    )
    aev = AEV_geodataframe(gdf, [f'damages_rp{rp}' for rp in rps], rps)
    gdf['damages_AEV'] = aev
    return gdf


# Main Execution
def main():
    if not os.path.exists(AEVDIR):
        os.makedirs(AEVDIR)
        
    # Compute AEV
    scenarios = parse_scenarios(template, INPUTS)
    scenarios = compute_cartesian_product(scenarios)
    for scenario in scenarios:
        gdf = process_scenario(scenario, INPUTS, rps, _template)
        gdf.to_file(os.path.join(AEVDIR, "_".join(scenario.values())+".gpkg"))

    islands = list(set([i['island'] for i in scenarios]))
    scens = list(set([i['scen'] for i in scenarios]))
    sample_columns = [i for i in gdf.columns if i != "geometry"]
    
    # Merge across scenarios into one file per island
    data = dict()
    for island in islands:
        pathgen = lambda x: os.path.join(AEVDIR, f"{island}_{x}.gpkg")
        merged_gdf = merge_geodataframes(pathgen, scens, sample_columns, ["OccupancyWeightedValue"])
        merged_gdf.to_file(os.path.join(POINTS_MERGED, f"{island}.gpkg"))
        data[island] = merged_gdf

    # Aggregate into lines
    lines_base = 'damage_assessment_usvi/USVI_data/CoastalSegments_ForBorja'
    for island, gdf in data.items():
        append = ''
        if island == "StThomas":
            append = "_Merge"
            
        lines = gpd.read_file(os.path.join(lines_base, f'{island}_Coastline_Intersect_SummaryPts_TransOrder{append}.shp'))
        lines = lines.dissolve(by='TransOrder').reset_index()
        summarized = summary_stats_nearest(gdf, lines, "TransOrder", [c for c in gdf.columns if "damages" in c], ["mean", "max", "sum"])
        s1 = gdf['damages_AEV_structural125'].sum()
        s2 = summarized['damages_AEV_structural125_sum'].sum()
        tol = 0.00001
        assert abs(s1 - s2) < tol, f"Sum should match, {s1} and {s2}"
        summarized.to_file(os.path.join(LINESDIR, f"{island}_shoreline.gpkg"))
          
    # Aggregate into bands
    bands_path = 'damage_assessment_usvi/USVI_data/USVI_Band_Shells.zip'
    bands = gpd.read_file(bands_path)
    gdf = pd.concat(data.values())
    summarized = summary_stats_nearest(gdf, bands, "OBJECTID", [c for c in gdf.columns if "damages" in c], ["mean", "max", "sum"])
    s1 = gdf['damages_AEV_structural125'].sum()
    s2 = summarized['damages_AEV_structural125_sum'].sum()
    assert abs(s1 - s2) < tol, f"Sum should match, {s1} and {s2}"
    summarized.to_file(os.path.join(BANDSDIR, f"summary_bands.gpkg"))
   
if __name__ == "__main__": 
    main()