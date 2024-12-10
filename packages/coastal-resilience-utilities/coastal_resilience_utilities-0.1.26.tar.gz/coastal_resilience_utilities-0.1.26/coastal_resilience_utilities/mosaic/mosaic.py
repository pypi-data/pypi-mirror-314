import numpy as np
import xarray as xr
import shapely
from shapely.geometry import Point, MultiLineString, LineString, MultiPolygon, Polygon
from utils.geo import xr_vectorize
from tqdm import tqdm
import copy
from shapely.ops import unary_union
import logging
import geopandas as gpd
from utils.dataset import compressRaster
from utils.timing import TimingContext
from utils.geo import rasterize_line
from xrspatial import proximity


from joblib import Parallel, delayed
import numba

import gc

import asyncio
import concurrent

logging.basicConfig()
logging.root.setLevel(logging.INFO)



def create_encompassing_grid(arr1, arr2, buff=200):

    def is_ascending(arr):
        return np.all(arr[:-1] <= arr[1:])
    # Determine the bounds of the new mosaic
    y_min = min(arr1.y.min().item(), arr2.y.min().item())-buff
    y_max = max(arr1.y.max().item(), arr2.y.max().item())+buff
    x_min = min(arr1.x.min().item(), arr2.x.min().item())-buff
    x_max = max(arr1.x.max().item(), arr2.x.max().item())+buff

    # Determine the common resolution (assume regular grids and identical resolutions)
    y_res = min(np.abs(arr1.y[1] - arr1.y[0]).item(), np.abs(arr2.y[1] - arr2.y[0]).item())
    x_res = min(np.abs(arr1.x[1] - arr1.x[0]).item(), np.abs(arr2.x[1] - arr2.x[0]).item())

    # Create new coordinates
    new_y = np.arange(y_min, y_max + y_res, y_res)
    if not is_ascending(arr1.y):
        new_y = new_y[::-1]
    new_x = np.arange(x_min, x_max + x_res, x_res)
    if not is_ascending(arr1.x):
        new_x = new_x[::-1]

    # Create a new DataArray with the expanded coordinates filled with NaNs
    new_shape = (len(new_y), len(new_x))
    new_data1 = np.full(new_shape, np.nan)

    new_arr = xr.DataArray(new_data1, coords=[new_y, new_x], dims=["y", "x"])
    return new_arr



def calculate_distances_to_edges(xr_obj, line_feature, boundary, op=np.max):
    """
    Calculate the distance from each pixel in an xarray object to the nearest polygon in a MultiPolygon,
    setting pixel values outside the polygons to NaN.
    
    Parameters:
    xr_obj (xarray.DataArray or xarray.Dataset): The input xarray object containing spatial data.
    multipolygon (shapely.geometry.MultiPolygon): The input MultiPolygon to measure distances from.
    
    Returns:
    xarray.DataArray: An xarray DataArray with the same shape as the input, containing distances to the nearest polygon,
                      with values outside the polygons set to NaN.
    """
    # Get the dimensions and coordinates
    ds = xr_obj.compute()

    # Clip
    ds_clipped = ds.rio.clip([boundary], all_touched=True)

    # Stack
    ds_stacked = ds_clipped.stack(pt=['x','y'])
    ds_dict = ds_stacked.to_dict()
    data = ds_dict['data']
    coords = ds_dict['coords']['pt']['data']

    def get_dist(line_feature, pt, d):
        if d == np.nan:
            return 0
        else:
            return line_feature.distance(pt)

    distances = []
    for idx, c in enumerate(coords):
        distances.append(
            get_dist(line_feature, Point(*c), data[idx]) 
        )
        
    # distances =  Parallel(n_jobs=10)(delayed(get_dist)(line_feature, Point(*c), data[idx]) for idx, c in enumerate(coords))

    data = np.reshape(distances, [ds_clipped.shape[1], ds_clipped.shape[0]])
    data_array = xr.DataArray(
        data, 
        coords={"y": ds_clipped.y, "x": ds_clipped.x}, 
        dims=["x", "y"],
        attrs={}
    ).transpose('y', 'x')

    data_array.rio.write_crs(xr_obj.rio.crs, inplace=True)
    return data_array


def idw_mosaic(
    arr1: xr.DataArray, 
    arr2: xr.DataArray, 
    CRS="EPSG:4326", BUFF=0.0, DEBUG=False):
    # arr1 = arr1.rio.reproject(CRS)
    # arr2 = arr2.rio.reproject(CRS)
    COORDS_EQUAL = np.array_equal(arr1.coords['x'], arr2.coords['x']) and np.array_equal(arr1.coords['y'], arr2.coords['y'])
    
    if DEBUG:
        compressRaster(arr1, "arr1.tif")
        compressRaster(arr2, "arr2.tif")

    if not COORDS_EQUAL:
        base_grid = create_encompassing_grid(arr1, arr2, buff=BUFF).rio.write_crs(CRS)
    else:
        base_grid = arr1.copy()
    d = np.zeros(base_grid.shape)
    base_grid.data = d
    
    arr1 = arr1.where(arr1 != arr1.rio.nodata, 0).rio.write_crs(CRS, inplace=True)
    arr2 = arr2.where(arr2 != arr2.rio.nodata, 0).rio.write_crs(CRS, inplace=True)
    
    arr1.rio.write_nodata(0, inplace=True)
    arr2.rio.write_nodata(0, inplace=True)
    
    if not COORDS_EQUAL:
        l1_grid = arr1.reindex_like(base_grid, method="nearest")
        l2_grid = arr2.reindex_like(base_grid, method="nearest")
    else:
        l1_grid = arr1.copy()
        l2_grid = arr2.copy()
        
    l1_grid.rio.write_crs(CRS, inplace=True)
    l2_grid.rio.write_crs(CRS, inplace=True)
    
    del arr1, arr2, base_grid
    gc.collect()
    
    if DEBUG:
        compressRaster(l1_grid, "l1_grid.tif")
        compressRaster(l2_grid, "l2_grid.tif")


    l1_mask = xr.where(l1_grid > 0, 1, 0).compute().rio.write_crs(CRS, inplace=True)
    l2_mask = xr.where(l2_grid > 0, 1, 0).compute().rio.write_crs(CRS, inplace=True)

    # return
    # Calculate Polygons
    p1 = xr_vectorize(l1_mask > 0, coarsen_by=1)
    p2 = xr_vectorize(l2_mask > 0, coarsen_by=1)
    p1 = unary_union(p1.geometry)
    p2 = unary_union(p2.geometry)

    def to_line(p):
        if isinstance(p, shapely.geometry.MultiPolygon):
            return MultiLineString([LineString(polygon.exterior.coords) for polygon in p.geoms])
        return MultiLineString([LineString(p.exterior.coords)])
    
    def exponential_weighting(d1, d2, lambd):
        w1 = np.exp(-lambd * d1)
        w2 = np.exp(-lambd * d2)
        sum_w = w1 + w2
        w1 /= sum_w
        w2 /= sum_w
        return w1, w2

    
    intersection_polygon=p1.intersection(p2)
    if intersection_polygon.geom_type == 'GeometryCollection':
        intersection_polygon = [geom for geom in intersection_polygon.geoms]
    if not isinstance(intersection_polygon, MultiPolygon) and not isinstance(intersection_polygon, Polygon):
        intersection_polygon = unary_union([i for i in intersection_polygon if isinstance(i, MultiPolygon) or isinstance(i, Polygon)])
    if intersection_polygon.is_empty:
        return l1_grid + l2_grid
    
    if DEBUG:
        intersection_gdf = gpd.GeoDataFrame(geometry=[intersection_polygon], crs=CRS)
        intersection_gdf.to_file('intersection_polygon.gpkg', driver='GPKG')
        
        p1_gdf = gpd.GeoDataFrame(geometry=[p1], crs=CRS)
        p1_gdf.to_file('p1_polygon.gpkg', driver='GPKG')
        
        p2_gdf = gpd.GeoDataFrame(geometry=[p2], crs=CRS)
        p2_gdf.to_file('p2_polygon.gpkg', driver='GPKG')
    
    l1 = to_line(p1).intersection(intersection_polygon)
    l2 = to_line(p2).intersection(intersection_polygon)

    # p2.to_file('p2.gpkg')
    dl1 = calculate_distances_to_edges(l1_grid, l1, intersection_polygon)
    dl2 = calculate_distances_to_edges(l2_grid, l2, intersection_polygon)

    dl1 = xr.where(dl1 > 0, dl1, np.nan)
    dl2 = xr.where(dl2 > 0, dl2, np.nan)

    lamb = 0.5
    METHOD="IDW"
    
    if METHOD == "IDW":
        denom = dl1 + dl2
        dl1 = dl1 / denom 
        dl2 = dl2 / denom 
        
    if METHOD == "EXPO":
        dl1, dl2 = exponential_weighting(dl1, dl2, lamb)

    l1_mask = dl1.combine_first(l1_mask)
    l2_mask = dl2.combine_first(l2_mask)
    
    to_return = l1_mask * l1_grid + l2_mask * l2_grid
    to_return.rio.write_crs(CRS, inplace=True)
    to_return.rio.write_nodata(0, inplace=True)
    
    del intersection_polygon, l1, l2, dl1, dl2, l1_mask, l2_mask
    gc.collect()
    return to_return


def idw_mosaic_slim(
    arr1: xr.DataArray, 
    arr2: xr.DataArray, 
    CRS="EPSG:4326", BUFF=0.0, DEBUG=False):
    # arr1 = arr1.rio.reproject(CRS)
    # arr2 = arr2.rio.reproject(CRS)
    COORDS_EQUAL = np.array_equal(arr1.coords['x'], arr2.coords['x']) and np.array_equal(arr1.coords['y'], arr2.coords['y'])
    assert COORDS_EQUAL
    assert arr1.rio.nodata == 0 and arr2.rio.nodata == 0
    assert arr1.rio.crs == CRS and arr2.rio.crs == CRS
    
    base_grid = arr1.copy()
    d = np.zeros(base_grid.shape)
    base_grid.data = d
    
    l1_grid = arr1.copy().rio.write_crs(CRS)
    l2_grid = arr2.copy().rio.write_crs(CRS)

    l1_mask = xr.where(l1_grid > 0, 1, 0).compute().rio.write_crs(CRS)
    l2_mask = xr.where(l2_grid > 0, 1, 0).compute().rio.write_crs(CRS)

    # return
    # Calculate Polygons
    p1 = xr_vectorize(l1_mask > 0, coarsen_by=1)
    p2 = xr_vectorize(l2_mask > 0, coarsen_by=1)
    p1 = unary_union(p1.geometry)
    p2 = unary_union(p2.geometry)

    def to_line(p):
        if isinstance(p, shapely.geometry.MultiPolygon):
            return MultiLineString([LineString(polygon.exterior.coords) for polygon in p.geoms])
        return MultiLineString([LineString(p.exterior.coords)])
    
    intersection_polygon=p1.intersection(p2)
    if intersection_polygon.geom_type == 'GeometryCollection':
        intersection_polygon = [geom for geom in intersection_polygon.geoms]
    if not isinstance(intersection_polygon, MultiPolygon) and not isinstance(intersection_polygon, Polygon):
        intersection_polygon = unary_union([i for i in intersection_polygon if isinstance(i, MultiPolygon) or isinstance(i, Polygon)])
    if intersection_polygon.is_empty:
        return l1_grid + l2_grid
    
    l1 = to_line(p1).intersection(intersection_polygon)
    l2 = to_line(p2).intersection(intersection_polygon)
    
    try:
        l1_as_array = rasterize_line(l1_grid, gpd.GeoDataFrame(geometry=[l1], crs=CRS))
        l2_as_array = rasterize_line(l2_grid, gpd.GeoDataFrame(geometry=[l2], crs=CRS))
        import uuid
        x = str(uuid.uuid4())
        dl1 = proximity(l1_as_array)
        dl2 = proximity(l2_as_array)
        
        # intersection_zone = rasterize_line(l1_grid, gpd.GeoDataFrame(geometry=[intersection_polygon], crs=CRS))
        dl1 = (dl1 + 0.0000001).rio.clip([intersection_polygon], all_touched=True)
        dl2 = (dl1 + 0.0000001).rio.clip([intersection_polygon], all_touched=True)
        
        # l1_as_array.rio.to_raster(f'test_rasterize_{x}.tif')
        # dl1.rio.to_raster(f'test_proximity_{x}.tif')
        # intersection_gdf = gpd.GeoDataFrame(geometry=[intersection_polygon], crs=CRS)
        # intersection_gdf.to_file(f'intersection_polygon-{x}.gpkg', driver='GPKG')
        
        # p1_gdf = gpd.GeoDataFrame(geometry=[p1], crs=CRS)
        # p1_gdf.to_file(f'p1_polygon-{x}.gpkg', driver='GPKG')
        
        # p2_gdf = gpd.GeoDataFrame(geometry=[p2], crs=CRS)
        # p2_gdf.to_file(f'p2_polygon-{x}.gpkg', driver='GPKG')
        # return
        
        dl1 = xr.where(dl1 > 0, dl1, np.nan)
        dl2 = xr.where(dl2 > 0, dl2, np.nan)

        denom = dl1 + dl2
        dl1 = dl1 / denom 
        dl2 = dl2 / denom 
            

        l1_mask = dl1.combine_first(l1_mask)
        l2_mask = dl2.combine_first(l2_mask)
        
        to_return = l1_mask * l1_grid + l2_mask * l2_grid
        to_return.rio.write_crs(CRS, inplace=True)
        to_return.rio.write_nodata(0, inplace=True)
    
    except:
        to_return = np.maximum(l1_grid, l2_grid)
        to_return.rio.write_crs(CRS, inplace=True)
        to_return.rio.write_nodata(0, inplace=True)
    
    return to_return
