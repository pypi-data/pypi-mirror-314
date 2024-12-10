import argparse
import geopandas as gpd
import rioxarray as rxr
from summary_stats.summary_stats import summary_stats
import logging

def main():
    parser = argparse.ArgumentParser(description="Run summary statistics on flooding data and geographies.")
    parser.add_argument('-f', '--flooding', type=str, required=True, help="Path to the flooding data file.")
    parser.add_argument('-g', '--geographies', type=str, required=True, help="Path to the geographies data file.")
    parser.add_argument('-i', '--id', type=str, required=True, help="Path to the geographies data file.")
    parser.add_argument('-o', '--output', type=str, required=True, help="Path to the output file.")
    
    args = parser.parse_args()
    
    # Open flooding data with rioxarray
    flooding = rxr.open_rasterio(args.flooding).isel(band=0).to_dataset(name=args.id)
    
    # Open geographies data with geopandas
    gdf = gpd.read_file(args.geographies)
    
    CRS = flooding.rio.crs
    gdf = gdf.to_crs(CRS)
    
    # Run summary_stats
    result = summary_stats(gdf, flooding)
    logging.info(result)
    
    # Write the output to a file
    result.to_file(args.output, driver='GPKG')

if __name__ == "__main__":
    main()
