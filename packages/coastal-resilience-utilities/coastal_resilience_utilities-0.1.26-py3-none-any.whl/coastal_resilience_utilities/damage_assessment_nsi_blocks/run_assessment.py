import rioxarray as rxr
import requests, os
from coastal_resilience_utilities.utils.dataset import makeSafe_rio
from coastal_resilience_utilities.utils.get_features import get_features_with_z_values
from coastal_resilience_utilities.damage_assessment.nsi_assessment import get_nsi_damages_generic
from glob import glob
from typing import Callable
import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd
from typing import List

from coastal_resilience_utilities.damage_assessment.damage_assessment import AEV_geodataframe
from glob import glob
from tqdm import tqdm

import warnings

DEFAULT_REGIONS_PATH = "/cccr-lab/000_data-repository/037_NSI_Blockgroup_AggregateCurvesAndValues/OccupancyWeightedValue_MP.gpkg"

def main(flooding, regions_path=DEFAULT_REGIONS_PATH, features_from="OSM", ISO3="USA"):
    init_crs = flooding.rio.crs
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        flooding = flooding.rio.reproject("EPSG:4326")
        flooddepths = get_features_with_z_values(flooding, ISO3=ISO3, features_from=features_from)
        
        damages = get_nsi_damages_generic(
            flooddepths, 
            regions=gpd.read_file(regions_path)
        ).reset_index(drop=True)
        
    # spatial join nearest is occassionally returning duplicates.
    # Here we remove these, taking the maximum damage value if there are multiple.
    nonunique_ids = damages[damages.duplicated(subset=['id'], keep=False)]['id']
    damages_nonunique = damages[damages.id.isin(nonunique_ids)]
    damages_idxmax = damages_nonunique.groupby('id')['damages'].idxmax()
    damages_nonunique_max = damages_nonunique.loc[damages_idxmax]
    damages = pd.concat([damages[~damages.id.isin(nonunique_ids)], damages_nonunique_max])
    
    return damages.to_crs(init_crs)


def combine_damages_and_run_AEV(path: str, file_type: str = ".gpkg", rp_index: int = 3, separator: str = '_', RPS=["010", "050", "100", "500"]):
    data = glob(os.path.join(path, f"*{file_type}"))
    distinct_scenarios = list(set([
        separator.join(i.split('/')[-1].split('.')[0].split(separator)[0:rp_index]) 
        for i in data
    ]))

    all_aev_df = pd.DataFrame({"id": []})
    geometry_df = pd.DataFrame({"id": []})

    crs = None

    for scen in tqdm(distinct_scenarios):
        print(scen)
        buff = []
        columns = []
        
        for rp in RPS:
            fid = f"{scen}_RP{rp}"
            gdf = gpd.read_file(f"{path}/{fid}.gpkg")
            crs = gdf.crs
            buff.append(gdf[["id", "damages"]].rename(columns=dict(damages=fid)))
            columns.append(fid)
            geometry_df = pd.merge(geometry_df, gdf[["id", "geometry"]], left_on="id", right_on="id", how="outer", suffixes=['', f"{scen}_{rp}"])

        geometry_columns = [col for col in geometry_df.columns if col.startswith("geometry")]
        geometry_df["geometry"] = geometry_df[geometry_columns].bfill(axis=1).iloc[:, 0]
        geometry_df = geometry_df[["id", "geometry"]]
        
        df = pd.DataFrame({"id": []})
        for b in buff:
            df = pd.merge(df, b, left_on="id", right_on="id", how="outer")
            
        df[f"AEV_{scen}"] = AEV_geodataframe(df, columns, [int(i) for i in RPS])
        all_aev_df = pd.merge(all_aev_df, df[['id', f"AEV_{scen}"]], left_on="id", right_on="id", how="outer")
        
    
    geometry_columns = [col for col in geometry_df.columns if col.startswith("geometry")]
    geometry_df["geometry"] = geometry_df[geometry_columns].bfill(axis=1).iloc[:, 0]
    geometry_df = geometry_df[["id", "geometry"]]
        
    return gpd.GeoDataFrame(pd.merge(all_aev_df, geometry_df, left_on="id", right_on="id", how="outer"), geometry="geometry", crs=crs)


