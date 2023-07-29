import geopandas as gpd
import rasterio
from rasterio import features
from rasterio.transform import from_origin
import numpy as np

def shapefile_to_raster(shapefile_path, output_raster_path, pixel_size=0.1):
    # Step 2: Read the shapefile using geopandas
    gdf = gpd.read_file(shapefile_path)
    
    # Step 3: Determine the extent and resolution for the raster
    xmin, ymin, xmax, ymax = gdf.total_bounds
    cols = int((xmax - xmin) / pixel_size)
    rows = int((ymax - ymin) / pixel_size)
    
    # Step 4: Create an empty raster array
    raster_array = np.zeros((rows, cols), dtype=np.uint64)
    
    # Step 5: Create a transformation matrix to map coordinates to raster pixels
    transform = from_origin(xmin, ymax, pixel_size, pixel_size)
    
    # Step 6: Rasterize the shapefile on the empty raster array
    shapes = ((geom, 1) for geom in gdf.geometry)
    rasterized = features.rasterize(shapes=shapes, fill=0, out=raster_array, transform=transform)
    
    # Step 7: Write the raster to a new file
    with rasterio.open(output_raster_path, 'w', driver='GTiff', height=rows, width=cols, count=1, dtype=raster_array.dtype, crs=gdf.crs, transform=transform) as dst:
        dst.write(rasterized, 1)

# Example usage:
shapefile_path = "../data/HydroRIVERS_v10_shp/reduced_HydroRIVERS_v10.shp"
output_raster_path = "../data/HydroRIVERS_v10_shp/raster/reduced_HydroRIVERS_v10.tiff"
shapefile_to_raster(shapefile_path, output_raster_path)
