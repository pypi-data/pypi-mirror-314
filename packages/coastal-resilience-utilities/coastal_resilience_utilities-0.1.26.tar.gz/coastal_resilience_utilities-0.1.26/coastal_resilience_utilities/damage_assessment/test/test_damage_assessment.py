from coastal_resilience_utilities.damage_assessment.damage_assessment import exposure, damages_dollar_equivalent, apply_dollar_weights
from coastal_resilience_utilities.damage_assessment.damage_assessment import AEV, apply_dollar_weights, AEV_geodataframe
from coastal_resilience_utilities.damage_assessment.population_assessment import main as population_assessment
from coastal_resilience_utilities.damage_assessment.nsi_assessment import get_nsi_damages, get_nsi
from coastal_resilience_utilities import get_project_root
import subprocess
import xarray as xr
import rioxarray as rxr
import uuid
import os
import logging
import geopandas as gpd
import pytest
import cProfile
from pathlib import Path
from coastal_resilience_utilities.dataconf import NSI


PACKAGE_ROOT = get_project_root()

BELIZE = Path(PACKAGE_ROOT) / "test/data/belize_test_flooding.tif"
MIAMI = Path(PACKAGE_ROOT) / "test/data/CWON_Miami_sample.tif"


def test_get_project_root():
    logging.info(get_project_root())
    
    
def non_rectilinear_grid(path):
    tmp_cog = f'/tmp/{str(uuid.uuid4())}.tiff'
    bashCommand = f"gdalwarp {BELIZE} {tmp_cog} -of COG"
    process = subprocess.Popen(bashCommand.split(' '), stdout=subprocess.PIPE)
    while True:
        line = process.stdout.readline()
        if not line: break
        print(line, flush=True)
    return tmp_cog


def test_damages_no_filters():
    ds = rxr.open_rasterio(non_rectilinear_grid(BELIZE)).isel(band=0)
    exp = exposure(ds)
    logging.info("exposure done")
    dde = damages_dollar_equivalent(ds, exp)
    logging.info("dde done")
    damages = apply_dollar_weights(dde)
    logging.info("damages done")
    logging.info(damages)
    

def test_population():
    import uuid
    ds = rxr.open_rasterio(non_rectilinear_grid(BELIZE)).isel(band=0)
    pop = population_assessment(ds, 0.5)
    logging.info(pop)
        
        
def test_AEV():
    tmp_dir = "/tmp"
    import zipfile
    import os
    from utils.dataset import open_as_ds

    zip_path = Path(PACKAGE_ROOT) / "test/data/TEST.zip"
    extract_path = Path(tmp_dir) / "test_data"
    os.makedirs(extract_path, exist_ok=True)

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)
        
    ds = open_as_ds(extract_path)
    rps = [10, 25, 50, 100]
    keys = [
        f"WaterDepth_Future2050_S1_Tr{rp}_t33" for rp in (10, 25, 50, 100)
    ]
    id = "AEV-Econ_Future2050_S1"
    aev = AEV(ds, rps, keys, id)
    assert aev.shape == ds[keys[0]].shape
    
    
def test_AEV_geodataframe():
    datapath = Path(PACKAGE_ROOT) / "test/data/openbuildings"
    rps = [10, 50, 100, 500]
    columns = ['flooding', 'damages']
    
    buff = []
    for rp in rps:
        gdf = gpd.read_file(datapath / f"StCroix_FZ_rp{rp}_base_flood_depth.gpkg")
        gdf = gdf[['geometry'] + columns]
        gdf = gdf.rename(columns={c: f'{c}_{rp}' for c in columns})
        buff.append(gdf)
        
    merged_gdf = buff[0]
    for gdf in buff[1:]:
        merged_gdf = merged_gdf.merge(gdf, on='geometry', how='outer')
        
    for c in columns:
        aev = AEV_geodataframe(merged_gdf, [f'{c}_{rp}' for rp in rps], rps)
        merged_gdf[f'{c}_AEV'] = aev
    logging.info(merged_gdf)
    

# @pytest.mark.skip(reason="Disabling this test temporarily")
def test_NSI():
    flooding = rxr.open_rasterio(
        MIAMI
    ).isel(band=0)
    left, bottom, right, top = flooding.rio.bounds()
    print(left, bottom, right, top)
    nsi = get_nsi(left=left, bottom=bottom, right=right, top=top, state="florida", crs=flooding.rio.crs)
    damages = get_nsi_damages(flooding, nsi)
    logging.info(damages)

if __name__ == "__main__":
    # cProfile.run("test_damages_no_filters()", "profile_results")
    test_damages_no_filters()