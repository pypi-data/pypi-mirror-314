import rioxarray as rxr
import requests, os
from utils.dataset import makeSafe_rio
from utils.get_features import get_features_with_z_values
from damage_assessment.nsi_assessment import get_nsi_damages_generic

BASEDIR = "damage_assessment_usvi/USVI_data/flooding/USGS_USVI/"
OUTPUTS = "/app/data/USGS_USVI/block/"
POINTS = os.path.join(OUTPUTS, "pre-aev")

def main():
    for i in os.listdir(BASEDIR):
        flooding = rxr.open_rasterio(
            os.path.join(BASEDIR, i)
        ).isel(band=0)
        print(flooding)
        flooding = makeSafe_rio(flooding)
        flooddepths = get_features_with_z_values(flooding, ISO3="USA")
        damages = get_nsi_damages_generic(flooddepths)
        damages.drop(columns=['polygon'], inplace=True)
        if not os.path.exists(POINTS):  
            os.makedirs(POINTS)
        damages.to_file(os.path.join(POINTS, f'{i.split(".")[0]}.gpkg'))
        
if __name__ == "__main__":
    main()