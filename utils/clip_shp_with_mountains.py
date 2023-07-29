import geopandas as gpd
from shapely.geometry import box

# Load the shapefile to be clipped
mountains_gdf = gpd.read_file("../data/K3Binary/k3binary.shp")

# Load the shapefile used to define the clip extent
other_gdf= gpd.read_file("../data/HydroRIVERS_v10_shp/reduced_HydroRIVERS_v10.shp")

# Clip the other shapefile using the mountain regions
clipped_gdf = gpd.clip(other_gdf, mountains_gdf)

# Optionally, save the clipped shapefile to a new file
output_clipped_shapefile_path = "../data/HydroRIVERS_v10_shp/clip_HydroRIVERS_v10/clip_HydroRIVERS_v10.shp"
clipped_gdf.to_file(output_clipped_shapefile_path)
