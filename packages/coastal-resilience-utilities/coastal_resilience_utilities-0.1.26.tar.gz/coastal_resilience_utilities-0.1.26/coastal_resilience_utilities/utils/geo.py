import rasterio
from shapely.geometry import shape
import geopandas as gpd
import pandas as pd
import xarray as xr
import numpy as np
from rasterio.sample import sample_gen
from utils.cache import memoize_geospatial_with_persistence
from utils.dataset import meters_to_degrees

from typing import Callable

import pyproj
import shapely
from shapely.geometry import Point
from shapely.ops import transform
from rasterio.features import rasterize

import copy
import logging
from tqdm import tqdm
import gc
import odc.geo.xr



# @memoize_geospatial_with_persistence('/tmp/extract_points.pkl')
def extract_z_values(ds, gdf, column_name, offset_column=None, offset_units=None) -> gpd.GeoDataFrame:
    # note the extra 'z' dimension that our results will be organized along
    da_x = xr.DataArray(gdf.geometry.x.values, dims=['z'])
    da_y = xr.DataArray(gdf.geometry.y.values, dims=['z'])
    logging.info(da_x)
    results = ds.sel(x=da_x, y=da_y, method='nearest')
    gdf[column_name] = results.values
    gdf[column_name][gdf[column_name] == ds.rio.nodata] = 0
    gdf[column_name][gdf[column_name].isna()] = 0
    if offset_units == "ft":
        offset = gdf[offset_column] * 0.3048
        gdf[column_name] = gdf[column_name] - offset
    if offset_units == "m":
        offset = gdf[offset_column]
        gdf[column_name] = gdf[column_name] - offset
    return gdf

# Convert GeoJSON to GeoDataFrame
def geojson_to_geodataframe(geojson):
    features = geojson["features"]
    geometries = [shape(feature["geometry"]) for feature in features]
    properties = [feature["properties"] for feature in features]
    gdf = gpd.GeoDataFrame(properties, geometry=geometries)
    return gdf


def transform_point(x, y, crs, out_crs="EPSG:4326"):
    pt = Point(x, y)
    init_crs = pyproj.CRS(crs)
    wgs84 = pyproj.CRS(out_crs)
    project = pyproj.Transformer.from_crs(init_crs, wgs84, always_xy=True).transform
    return transform(project, pt)


def rescale_raster(ds):
    print(ds.attrs)
    ds = copy.deepcopy(ds)
    ds = ds.where(ds != ds.attrs['_FillValue'], 0)
    # rxr doesn't respect integer scaling when running selects, so we need to do it manually.
    # Might be nice to wrap this into our own rxr import
    ds = ds * ds.attrs['scale_factor'] + ds.attrs['add_offset']
    return ds


def clip_dataarray_by_geometries(ds, gdf, nodata=np.nan):
    """
    Clips a rioxarray DataArray by each geometry in a GeoDataFrame.

    Parameters:
    dataarray (rioxarray.DataArray): The input dataarray to be clipped.
    geodf (geopandas.GeoDataFrame): The geodataframe containing the geometries for clipping.

    Returns:
    list: A list of clipped rioxarray DataArrays.
    """
    clipped_arrays = dict()
    gdf = gdf.to_crs(ds.rio.crs)

    for idx, row in tqdm(gdf.iterrows()):
        geometry = row['geometry']
        try: 
            minx, miny, maxx, maxy = geometry.bounds
            clipped_array = ds.rio.clip_box(minx=minx, miny=miny, maxx=maxx, maxy=maxy)
            clipped_array = clipped_array.rio.clip([geometry], ds.rio.crs, all_touched=True, drop=False, invert=False)
            print(clipped_array)
            print(clipped_array.sum())
            # clipped_array = xr.where(~np.isnan(clipped_array), 1, 0).rio.write_crs(ds.rio.crs)
            if clipped_array.max() > 0:
                clipped_arrays[idx] = clipped_array
                yield (idx, clipped_array)
        except:
            gc.collect()
            continue
        gc.collect()

    return clipped_arrays


def xr_vectorize(
    da,
    coarsen_by=50,
    attribute_col=None,
    crs=None,
    dtype="float32",
    output_path=None,
    verbose=True,
    filter_to_positive=False,
    **rasterio_kwargs,
) -> gpd.GeoDataFrame:
    """
    Vectorises a raster ``xarray.DataArray`` into a vector
    ``geopandas.GeoDataFrame``.

    Parameters
    ----------
    da : xarray.DataArray
        The input ``xarray.DataArray`` data to vectorise.
    attribute_col : str, optional
        Name of the attribute column in the resulting
        ``geopandas.GeoDataFrame``. Values from ``da`` converted
        to polygons will be assigned to this column. If None,
        the column name will default to 'attribute'.
    crs : str or CRS object, optional
        If ``da``'s coordinate reference system (CRS) cannot be
        determined, provide a CRS using this parameter.
        (e.g. 'EPSG:3577').
    dtype : str, optional
         Data type  of  must be one of int16, int32, uint8, uint16,
         or float32
    output_path : string, optional
        Provide an optional string file path to export the vectorised
        data to file. Supports any vector file formats supported by
        ``geopandas.GeoDataFrame.to_file()``.
    verbose : bool, optional
        Print debugging messages. Default True.
    **rasterio_kwargs :
        A set of keyword arguments to ``rasterio.features.shapes``.
        Can include `mask` and `connectivity`.

    Returns
    -------
    gdf : geopandas.GeoDataFrame

    """

    # Add GeoBox and odc.* accessor to array using `odc-geo`
    da = add_geobox(da, crs)
    if filter_to_positive:
        da = xr.where(da > 0, 1, 0)
    da = da.coarsen(x=coarsen_by, y=coarsen_by, boundary='pad').max()

    # Run the vectorizing function
    vectors = list(rasterio.features.shapes(
        source=da.data.astype(dtype), transform=da.odc.transform, **rasterio_kwargs
    ))

    # Extract the polygon coordinates and values from the list
    polygons = [polygon for polygon, value in vectors]
    values = [value for polygon, value in vectors]

    # Convert polygon coordinates into polygon shapes
    polygons = [shape(polygon) for polygon in polygons]

    # Create a geopandas dataframe populated with the polygon shapes
    attribute_name = attribute_col if attribute_col is not None else "attribute"
    gdf = gpd.GeoDataFrame(
        data={attribute_name: values}, geometry=polygons, crs=da.odc.crs
    )

    # If a file path is supplied, export to file
    if output_path is not None:
        if verbose:
            print(f"Exporting vector data to {output_path}")
        gdf.to_file(output_path)

    gdf.sindex
    if filter_to_positive:
        return gdf[gdf["attribute"] == 1.0]
    else:
        return gdf


def add_geobox(ds, crs=None):
    """
    Ensure that an xarray DataArray has a GeoBox and .odc.* accessor
    using `odc.geo`.

    If `ds` is missing a Coordinate Reference System (CRS), this can be
    supplied using the `crs` param.

    Parameters
    ----------
    ds : xarray.Dataset or xarray.DataArray
        Input xarray object that needs to be checked for spatial
        information.
    crs : str, optional
        Coordinate Reference System (CRS) information for the input `ds`
        array. If `ds` already has a CRS, then `crs` is not required.
        Default is None.

    Returns
    -------
    xarray.Dataset or xarray.DataArray
        The input xarray object with added `.odc.x` attributes to access
        spatial information.

    """
    # If a CRS is not found, use custom provided CRS
    if ds.odc.crs is None and crs is not None:
        ds = ds.odc.assign_crs(crs)
    elif ds.odc.crs is None and crs is None:
        raise ValueError(
            "Unable to determine `ds`'s coordinate "
            "reference system (CRS). Please provide a "
            "CRS using the `crs` parameter "
            "(e.g. `crs='EPSG:3577'`)."
        )

    return ds


def merge_geodataframes(path_generator: Callable, inputs: list, fields_to_keep=["flooding", "damages", "OccupancyWeightedValue"], keep_one=['OccupancyWeightedValue'], input_formatter: Callable = lambda x: x):
    
    buff = []
    for i in inputs:
        path = path_generator(i)
        gdf = gpd.read_file(path)
        gdf = gdf[fields_to_keep + ['geometry']].rename(columns={c: f'{c}_{input_formatter(i)}' for c in fields_to_keep})
        buff.append(gdf)
      
    merged_gdf = buff[0]
    for gdf in buff[1:]:
        merged_gdf = merged_gdf.merge(gdf, on='geometry', how='outer')
        
    for keep in keep_one:
        cols = [col for col in merged_gdf.columns if keep in col]
        merged_gdf[keep] = merged_gdf[cols].bfill(axis=1).iloc[:, 0] 
        merged_gdf = merged_gdf.drop(columns=cols)

    return merged_gdf


def rasterize_line(da: xr.DataArray, gdf: gpd.GeoDataFrame, buff = 0.0000001):
    gdf = gdf.to_crs(da.rio.crs)
    gdf.geometry = gdf.geometry.buffer(buff)
    # Create an empty canvas with the same dimensions as the raster
    transform = rasterio.transform.from_bounds(*da.rio.bounds(), da.rio.width, da.rio.height)
    out_shape = (da.rio.height, da.rio.width)
        

    # Rasterize the zones GeoDataFrame
    shapes = ((geom, 1) for geom, value in zip(gdf.geometry, gdf.index))
    zones = rasterize(
        shapes=shapes, 
        out_shape=out_shape, 
        transform=transform, 
        fill=0,
        all_touched=True,
        dtype='float32')
    zone_raster = da.copy()
    zone_raster.data = zones
    return zone_raster


def rasterize_zones(gdf, ds, field="index"):
    init_crs = ds.rio.crs
    gdf = gdf.to_crs(init_crs)
    # Rasterize the zones GeoDataFrame
    transform = rasterio.transform.from_bounds(*ds.rio.bounds(), ds.rio.width, ds.rio.height)
    out_shape = (ds.rio.height, ds.rio.width)
    
    if field == "index" and "index" not in gdf.columns:
        gdf = gdf.reset_index()
    shapes = ((geom, value) for geom, value in zip(gdf.geometry, gdf[field]))
    zone_raster = ds.copy()
    try:
        zones = rasterize(shapes=shapes, out_shape=out_shape, transform=transform, fill=np.nan, dtype='float32')
    except ValueError:
        zone_raster.data = np.full(out_shape, np.nan, dtype='float32')
        zone_raster = zone_raster.rio.reproject(init_crs).reindex_like(ds_init, method="nearest")
        return zone_raster
    
    zone_raster.data = zones
    return zone_raster

def test():
    print("test")