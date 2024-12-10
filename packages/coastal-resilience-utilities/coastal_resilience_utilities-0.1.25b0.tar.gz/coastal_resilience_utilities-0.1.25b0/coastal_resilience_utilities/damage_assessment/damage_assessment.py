import rioxarray as rxr
import xarray as xr
import pandas as pd
from rasterio.errors import NotGeoreferencedWarning
import warnings
from utils.dataset import get_resolution, degrees_to_meters
from utils.damages import apply_ddf
from utils.geo import clip_dataarray_by_geometries
import rasterio
from rasterio.features import rasterize

import numpy as np
import math
import copy

import geopandas as gpd
import logging

import os
import gc

from dataconf import BUILDING_AREA, GADM, POPULATION

from dask.diagnostics import ProgressBar  # Import ProgressBar



DDF = os.path.join(os.path.dirname(__file__), 'supporting_data', 'damage_curves_and_values', 'DDF_Global.csv')
MAXDAMAGE = os.path.join(os.path.dirname(__file__), 'supporting_data', 'damage_curves_and_values', 'MaxDamage_per_m2.csv')
CROSSWALK = os.path.join(os.path.dirname(__file__), 'supporting_data', 'damage_curves_and_values', 'crosswalk_econ_gadm.csv')

def damages_dollar_equivalent(flooding: xr.Dataset | xr.DataArray, buildings: xr.Dataset | xr.DataArray, window=0, population_min=5):
    with warnings.catch_warnings():
        damage_percents = apply_ddf(flooding)
        if window:
            population = rxr.open_rasterio(
                POPULATION,
                chunks=True
            ).isel(band=0)
            minx, miny, maxx, maxy = flooding.rio.reproject("EPSG:4326").rio.bounds()
            population = population.rio.clip_box(
                minx=minx, miny=miny, maxx=maxx, maxy=maxy, auto_expand=True
            )
            population_res = get_resolution(population)
            population_res = degrees_to_meters(population_res[0], population.rio.bounds()[3])
            window_size = math.ceil(window / population_res)
            population = population.rolling(x=window_size, y=window_size, center=True).sum()
            population = xr.where(population > population_min, 1, 0).rio.write_crs("EPSG:4326").rio.reproject(flooding.rio.crs)
            population = population.reindex_like(damage_percents, method="nearest")
            damage_percents = damage_percents * population
            del population
            gc.collect()

        return (damage_percents * buildings)

def exposure(flooding: xr.Dataset | xr.DataArray):
    init_crs = flooding.rio.crs
    buildings = rxr.open_rasterio(
        BUILDING_AREA
    ).isel(band=0)
    with warnings.catch_warnings():
        warnings.filterwarnings(
            "ignore",
            category=NotGeoreferencedWarning,
            module="rasterio",
        )
        flooding_reproj = flooding.rio.reproject("EPSG:4326")
        minx, miny, maxx, maxy = flooding_reproj.rio.bounds()
        buildings = buildings.rio.clip_box(
            minx=minx, miny=miny, maxx=maxx, maxy=maxy, auto_expand=True
        ).rio.reproject(init_crs)
        del flooding_reproj
        gc.collect()

        flooding = xr.where(flooding == flooding.rio.nodata, 0, flooding).rio.write_crs(init_crs)
        buildings = xr.where(buildings == buildings.rio.nodata, 0, buildings).rio.write_crs(init_crs)

        flooding_res = get_resolution(flooding)
        buildings_res = get_resolution(buildings)

        res_modifier = (
            (flooding_res[0] * flooding_res[1]) /
            (buildings_res[0] * buildings_res[1])
        )
        
        buildings = buildings.reindex_like(flooding, method="nearest")
        buildings = buildings * res_modifier

        floodmask = xr.where(flooding > 0, 1, 0).rio.write_crs(init_crs)
        exposure = buildings * floodmask
        del floodmask, buildings
        gc.collect()

        return exposure


def AEV_geodataframe(gdf: gpd.GeoDataFrame, columns, rps, year_of_zero_damage=1.):
    rps      = np.array(rps)
    values  = np.array(np.nan_to_num(gdf[columns].to_numpy()))

    probability = 1.0 / rps
        
    #add rp = 1
    probability_of_zero_damage = 1/year_of_zero_damage
    if not any(probability==probability_of_zero_damage): 
        x = probability.tolist()
        x.append(probability_of_zero_damage)
        y = values.tolist()
        y = np.hstack((y, np.zeros((values.shape[0], 1)))).T # loss 0 for annual flood 
        
        
        probability = np.array(x) 
        values      = np.array(y)

    ind = np.argsort(probability)
    ind[::-1]
    probability = probability[ind[::-1]]
    values      = values[ind[::-1]]

    DX  = probability[0:-1] - probability[1:]
    upper = sum((DX * values[1:].T).T)
    lower = sum((DX * values[0:-1].T).T)
    aev = (upper + lower) / 2
    return aev


def AEV(ds: xr.Dataset | xr.DataArray, rps, keys, id, year_of_zero_damage=1.):
    values = np.nan_to_num(
        np.array([
            ds[k].to_numpy() for k in keys
        ])
    )

    rps      = np.array(rps)
    values  = np.array(values)

    probability = 1.0 / rps
        
    #add rp = 1
    probability_of_zero_damage = 1/year_of_zero_damage
    if not any(probability==probability_of_zero_damage): 
        x = probability.tolist()
        x.append(probability_of_zero_damage)
        y = values.tolist()
        y.append(np.zeros(ds[keys[0]].shape)) # loss 0 for annual flood 
        
        probability = np.array(x) 
        values      = np.array(y)

    ind = np.argsort(probability)
    ind[::-1]
    probability = probability[ind[::-1]]
    values      = values[ind[::-1]]

    DX  = probability[0:-1] - probability[1:]
    upper = sum((DX * values[1:].T).T)
    lower = sum((DX * values[0:-1].T).T)
    aev = (upper + lower) / 2
    to_return = xr.where(
        ds[keys[0]].fillna(1),
        aev,
        aev,
        keep_attrs=True
    ).rename(id)
    return to_return



def apply_dollar_weights(ds):
    ds_init = copy.deepcopy(ds)
    ds = copy.deepcopy(ds)
    init_crs = ds.rio.crs
    maxdamage = pd.read_csv(MAXDAMAGE)
    crosswalk = pd.read_csv(CROSSWALK)
    maxdamage = maxdamage.merge(crosswalk, left_on='Country', right_on="Econ",  how='left', suffixes=('', '_new'))
    maxdamage['Country'] = maxdamage['Boundaries'].combine_first(maxdamage['Country'])
    logging.info(GADM)
    
    gadm = gpd.read_parquet(GADM).set_crs(4326, allow_override=True)
    logging.info(gadm)
    ds = xr.where(ds == ds.rio.nodata, 0, ds).rio.write_crs(ds.rio.crs)
    ds.rio.write_nodata(0, inplace=True)
    ds = ds.rio.reproject("EPSG:4326")
    logging.info(ds)
    
    bounds = ds.rio.bounds()
    minx, miny, maxx, maxy = bounds
    
    # Clip the GeoDataFrame using the .cx accessor
    gadm = gadm.cx[minx:maxx, miny:maxy]
    gadm = pd.merge(gadm, maxdamage, left_on="NAME_0", right_on="Country", how="left")
    
    # Create an empty canvas with the same dimensions as the raster
    transform = rasterio.transform.from_bounds(*ds.rio.bounds(), ds.rio.width, ds.rio.height)
    out_shape = (ds.rio.height, ds.rio.width)
        

    # Rasterize the zones GeoDataFrame
    shapes = ((geom, value) for geom, value in zip(gadm.geometry, gadm['Total']))
    zone_raster = ds.copy()
    try:
        zones = rasterize(shapes=shapes, out_shape=out_shape, transform=transform, fill=np.nan, dtype='float32')
    except ValueError:
        zone_raster.data = np.full(out_shape, np.nan, dtype='float32')
        zone_raster = zone_raster.rio.reproject(init_crs).reindex_like(ds_init, method="nearest")
        return zone_raster
    
    zone_raster.data = zones
    zone_raster = zone_raster.rio.reproject(init_crs).reindex_like(ds_init, method="nearest")
    to_return = (ds_init * zone_raster)
    return to_return
            