import os

BUILDING_AREA = os.getenv("BUILDING_AREA", "gs://supporting-data2/WSF3d_v02_BuildingArea.tif")
GADM = os.getenv("GADM", "gs://supporting-data2/gadm_country_bounds.parquet")
POPULATION = os.getenv("POPULATION", 'gs://supporting-data2/GHS_POP_E2020.tif')
OPEN_BUILDINGS = os.getenv("OPEN_BUILDINGS", "gs://supporting-data2/google-microsoft-open-buildings.parquet")
NSI = os.getenv("NSI", "gs://geopmaker-output-staging/nsi.geoparquet/")