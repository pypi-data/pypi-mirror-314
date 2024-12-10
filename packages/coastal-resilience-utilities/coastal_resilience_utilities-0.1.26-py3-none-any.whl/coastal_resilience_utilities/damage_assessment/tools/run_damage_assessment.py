from damage_assessment.damage_assessment import main as damage_assessment
from damage_assessment.damage_assessment import AEV, apply_dollar_weights
from damage_assessment.population_assessment import main as population_assessment
from damage_assessment.nsi_assessment import get_nsi_damages, get_nsi
import subprocess
import xarray as xr
import rioxarray as rxr
import uuid
import os
import logging
import argparse

from utils.dataset import compressRaster

logging.basicConfig()
logging.root.setLevel(logging.INFO)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Trigger remote damages or population")
    parser.add_argument("-f", "--flooding", type=str, help="Path to Input Flooding")
    parser.add_argument("-o", "--output", type=str, help="Path to Input Flooding")
    args = parser.parse_args()
    
    ds = rxr.open_rasterio(args.flooding).isel(band=0)
    damages = damage_assessment(ds)
    compressRaster(damages, args.output.split('.')[0] + '_unscaled.tif')
    damages = apply_dollar_weights(damages)
    
    compressRaster(damages, args.output)
    # damages.
    