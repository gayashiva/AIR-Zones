import rasterio
import geopandas as gpd
from rasterio.features import shapes

def geotiff_to_shapefile(geotiff_path, shapefile_path):
    # Read the GeoTIFF file using rasterio
    with rasterio.open(geotiff_path) as src:
        # Get the raster data and affine transformation
        image = src.read(1)
        transform = src.transform

        # Convert the raster data to vector shapes
        shapes = list(rasterio.features.shapes(image, transform=transform))

    # Check if shapes list is empty or contains only NoData values
    if not shapes or all(value == 0 for shape, value in shapes):
        print("No valid data found in the GeoTIFF.")
        return

    # Filter out NoData values from the shapes list
    valid_shapes = [shape for shape, value in shapes if value != 0]

    # Create a GeoDataFrame from the valid vector shapes
    gdf = gpd.GeoDataFrame({'geometry': valid_shapes})

    # Save the GeoDataFrame as a shapefile
    gdf.to_file(shapefile_path)

if __name__ == "__main__":
    # Replace 'input_geotiff.tif' with the path to your GeoTIFF file
    input_geotiff = "/home/bsurya/Projects/AIR-Zones/data/GlobalMountainsK3Binary/k3binary.tif"

    # Replace 'output_shapefile.shp' with the desired output shapefile path
    output_shapefile = "/home/bsurya/Projects/AIR-Zones/data/GlobalMountainsK3Binary/k3binary.shp"

    geotiff_to_shapefile(input_geotiff, output_shapefile)
