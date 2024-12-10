from damage_assessment_usvi.damages_usvi import main as damage_assessment_usvi
from damage_assessment_usvi.aev_usvi import main as aev_usvi


import pytest

@pytest.mark.skip(reason="Disabling this test temporarily")
def test_damages_usvi():
    # This is intermediate processing to deal with non-rectilinear grids
    damage_assessment_usvi()
    aev_usvi()