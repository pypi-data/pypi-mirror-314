from coastal_resilience_utilities.damage_assessment_nsi_blocks.prep_blocks import get_data_record, main as prep_blocks
from coastal_resilience_utilities.damage_assessment_nsi_blocks.run_assessment import main as run_assessment, combine_damages_and_run_AEV
import logging
import rioxarray as rxr
import os
from glob import glob
from pathlib import Path

import pytest

@pytest.mark.skip(reason="Skipping this test")
def test_prep_blocks(StateAbbr="MP"):
    record = get_data_record(StateAbbr=StateAbbr)
    geogs = prep_blocks(record)
    assert geogs.shape[0] > 0
    

@pytest.mark.skip(reason="Skipping this test")
def test_run_assessment():
    test_path = "/cccr-lab/001_projects/013_USGS_DOI_OIA/100_CNMI/124_SFINCS_SIMULATIONS/saipan/004_V4/S0_BASE_HH000_RP010/results/CNMI_saipan_S0_BASE_HH000_RP010_hmax_masked.tif"
    flooding = rxr.open_rasterio(test_path).isel(band=0)
    damages = run_assessment(flooding=flooding)
    logging.info(damages)
    

@pytest.mark.skip(reason="Skipping this test")
def test_combine_damages_and_run_AEV():
    test_path = "/cccr-lab/001_projects/013_USGS_DOI_OIA/100_CNMI/170_DAMAGES_CALCULATION/saipan/004_V4/pre-aev"
    damages = combine_damages_and_run_AEV(path=test_path)
    logging.info(damages.columns)
    

@pytest.mark.skip(reason="Skipping this test")
def test_path():
    logging.info(f"Current file path: {__file__}")
    return __file__
