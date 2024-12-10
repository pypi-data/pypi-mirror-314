import os
import geopandas as gpd
import pandas as pd
from damage_assessment.population_assessment import main as population_assessment
from damage_assessment.damage_assessment import main as damage_assessment, apply_dollar_weights, AEV

import rioxarray as rxr
import logging

from damage_assessment_usvi.damages_usvi import OUTPUTS as BASEDIR
from damage_assessment_usvi.helpers import parse_scenarios, compute_cartesian_product
from utils.dataset import compressRaster, open_as_ds
import copy

from string import Template

logging.basicConfig()
logging.root.setLevel(logging.INFO)

base = "/app/csir_damages"
islands = ["StCroix", "StThomas", "StJohn"]
scenarios = ["base", "ecological", "NoReef", "PostStorm", "structural125", "structural125w5"]
rps = [10, 50, 100, 500]

POPDIR = os.path.join(BASEDIR, "population")
if not os.path.exists(POPDIR):
    os.makedirs(POPDIR)


def get_merged_summary_points(scenario):
    data = dict()
    if scenario == "structural125w5":
        _scenario = "structural_125_w5"
    
    elif scenario == "structural125":
        _scenario = "structural_125"
    
    else:
        _scenario = scenario
        
    for island in islands:
        path = os.path.join(base, f"{island}_results_corrected")
        gdfs = [
            gpd.read_file(file) for file in 
                [os.path.join(path, f"{island}_FZ_rp{rp}_{_scenario}_summary_points.shp") for rp in rps]
        ]
        merged_gdf = gdfs[0]
        merged_gdf = merged_gdf.rename(columns = {c: f"{c}_rp{rps[0]}" for c in merged_gdf.columns if c != "geometry"})
        for gdf, rp in zip(gdfs[1:], rps[1:]):
            gdf = gdf.rename(columns = {c: f"{c}_rp{rp}" for c in gdf.columns if c != "geometry"})
            merged_gdf = merged_gdf.merge(gdf, how="outer", on="geometry")
        data[island] = merged_gdf
    return data


def validate_counts_and_damages(scenario):
    data = get_merged_summary_points(scenario)
        
    # Get building counts and total damages for previous method
    previous_values = dict()
    for island, gdf in data.items():
        print(island)
        all_b_cols = [c for c in gdf.columns if "ALL_B" in c]
        for all_b in all_b_cols:
            series = gdf[all_b][gdf[all_b] > 0]
            previous_values[f'{island}_{scenario}_count_{all_b.split("_")[2]}'] = series.sum()
        all_d_cols = [c for c in gdf.columns if "ALL_D" in c]
        for all_d in all_d_cols:
            series = gdf[all_d][gdf[all_d] > 0]
            previous_values[f'{island}_{scenario}_damages_{all_d.split("_")[2]}'] = series.sum()
        
    # Get counts and damages for new buildings
    new_values = dict()
    new_path = "/app/data/USGS_USVI/block/points_merged"
    for island in islands:
        comparison = os.path.join(new_path, f"{island}.gpkg")
        gdf = gpd.read_file(comparison)
        logging.info(gdf)
        for rp in rps:
            field = f'damages_rp{rp}_{scenario}'
            new_values[f"{island}_{scenario}_count_rp{rp}"] = gdf[field].count()
            new_values[f"{island}_{scenario}_damages_rp{rp}"] = gdf[field].sum()
    
    # Combine both series into a dataframe
    combined_df = pd.concat([pd.Series(previous_values), pd.Series(new_values)], axis=1)
    combined_df.columns = ['Old Method', 'Updated Method']
    return combined_df


def pop_aev():
    import copy
    rps = (10, 50, 100, 500)
    template = "${island}_rp{rp}_${scen}"
    _scenarios = parse_scenarios(template, POPDIR, ext=".tif")
    _scenarios = compute_cartesian_product(_scenarios)
    _template = Template(template)
    
    # for scenario in scenarios:
    #     print(scenario)
    #     validate_pop(scenario)
    
    buff = dict()
    for s in _scenarios:
        print(s)
        ds = open_as_ds(POPDIR, search=f"{s['island']}_*")
        print(ds)
        formatter = _template.safe_substitute(s)
        id = '_'.join(s.values())
        aev = AEV(
            copy.deepcopy(ds), 
            rps, 
            keys=[formatter.format(rp=rp) for rp in rps], 
            id=id
        )
        
        output_file = os.path.join(POPDIR, f'AEV_{id}.tif')
        compressRaster(aev, output_file)
    

def validate_pop(scenario):
    previous_data = get_merged_summary_points(scenario)
    
    # Get building counts and total damages for previous method
    previous_values = dict()
    for island, gdf in previous_data.items():
        print(island)
        pop_cols = [c for c in gdf.columns if "POP" in c]
        for pop in pop_cols:
            series = gdf[pop][gdf[pop] > 0]
            previous_values[f'{island}_{scenario}_population_{pop.split("_")[1]}'] = series.sum()
            
    # Get counts and damages for new buildings
    new_values = dict()
    flooding_path = "damage_assessment_usvi/USVI_data/flooding/USGS_USVI"
    for island in islands:
        for rp in rps:
            flooding = os.path.join(flooding_path, f"{island}_FZ_rp{rp}_{scenario}_flood_depth.tif")
            ds = rxr.open_rasterio(flooding).isel(band=0)
            pop = population_assessment(ds, threshold=0.1)
            
            compressRaster(pop, os.path.join(POPDIR, f'{island}_rp{rp}_{scenario}.tif'))
            new_values[f"{island}_{scenario}_population_rp{rp}"] = float(pop.sum().values)
    
    # Combine both series into a dataframe
    combined_df = pd.concat([pd.Series(previous_values), pd.Series(new_values)], axis=1)
    combined_df.columns = ['Old Method', 'Updated Method']
    return combined_df
    
    
    

def validate_damages_against_eo(scenario):
    # Get counts and damages for new buildings
    new_values = dict()
    flooding_path = "damage_assessment_usvi/USVI_data/flooding/USGS_USVI"
    for island in islands:
        for rp in rps:
            flooding = os.path.join(flooding_path, f"{island}_FZ_rp{rp}_{scenario}_flood_depth.tif")
            ds = rxr.open_rasterio(flooding).isel(band=0)
            dmg = damage_assessment(ds)
            dmg = apply_dollar_weights(dmg)
            new_values[f"{island}_{scenario}_damageEO_rp{rp}"] = float(dmg.sum().values)
    
    # Combine both series into a dataframe
    combined_df = pd.Series(new_values).rename("Old Method")
    return combined_df


def main():
    dfs = []
    for scenario in scenarios:
        dfs.append(pd.concat([validate_pop(scenario), validate_counts_and_damages(scenario), validate_damages_against_eo(scenario)]))
    df = pd.concat(dfs)
    df = df.reset_index()
    df[['Island', 'Scenario', 'Type', 'ReturnPeriod']] = df['index'].str.split('_', expand=True)
    df = df.drop(columns=['index'])

    csv_buff = []
    for scen in df.Scenario.unique():
        for t in df.Type.unique():
            _df = df[df.Scenario == scen]
            _df = _df[_df.Type == t]
            _df = _df.drop(columns=['Type', 'Scenario'])
            df_pivot = _df.pivot_table(index=['Island'], columns=['ReturnPeriod'], values=['Old Method', 'Updated Method'])
                    
            print(sorted(df_pivot.columns))
            df_pivot = df_pivot.reindex(
                [
                    ('Updated Method', 'rp10'), ('Updated Method', 'rp50'), ('Updated Method', 'rp100'), ('Updated Method', 'rp500'), 
                    ('Old Method', 'rp10'), ('Old Method', 'rp50'), ('Old Method', 'rp100'), ('Old Method', 'rp500')
                ], 
                axis=1
            )
            csv_path = f'/tmp/{scen}_{t}.csv'
            df_pivot.to_csv(csv_path)
            csv_buff.append(csv_path)
            
    import csv

    # Initialize a list to hold all rows
    all_rows = []

    # Iterate over each CSV file in csv_buff
    for csv_file in csv_buff:
        with open(csv_file, 'r') as f:
            reader = csv.reader(f)
            # Read all rows from the current CSV file
            rows = list(reader)
            # Append the rows to all_rows
            all_rows.append([csv_file.split('/')[-1].split('.')[0]] + ['' for r in rows[0][1:]])
            all_rows.extend(rows)
            # Append a gap row (empty row) to all_rows
            all_rows.append(['' for r in rows[0]])
            all_rows.append(['' for r in rows[0]])

    # Write the concatenated rows to a new CSV file
    with open('damage_assessment_usvi/validations/validation.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(all_rows)
        
    # Write the concatenated rows to a new CSV file
    with open(os.path.join(BASEDIR, "validations.csv"), 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(all_rows)


# main()
pop_aev()

    


# validate_counts_and_damages().to_csv('/app/data/USGS_USVI/comparison_validation_data.csv')
