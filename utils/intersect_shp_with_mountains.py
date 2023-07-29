import geopandas as gpd

def create_intersection_shapefile(shapefile1_path, shapefile2_path, output_shapefile_path):
    # Read the input shapefiles
    gdf1 = gpd.read_file(shapefile1_path)
    gdf2 = gpd.read_file(shapefile2_path)

    # Compute the intersection between the two GeoDataFrames
    intersection_gdf = gpd.overlay(gdf1, gdf2, how='intersection', keep_geom_type=False)

    # Write the intersection GeoDataFrame to a new shapefile
    intersection_gdf.to_file(output_shapefile_path)

# Example usage:
shapefile1_path = "../data/K3Binary/k3binary.shp"
shapefile2_path = "../data/HydroRIVERS_v10_shp/reduced_HydroRIVERS_v10.shp"
output_shapefile_path = "../output/dis_mountain.shp"

create_intersection_shapefile(shapefile1_path, shapefile2_path, output_shapefile_path)
