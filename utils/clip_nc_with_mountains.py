import xarray as xr
import geopandas as gpd
from shapely.geometry import box

# Read the NetCDF file
nc_file = '../data/wettasmin_W5E5v2.0_2019.nc'
dataset = xr.open_dataset(nc_file)

# Read the shapefile used for clipping
clip_shapefile = gpd.read_file("../data/K3Binary/k3binary.shp")

# Get the bounding box (envelope) of the shapefile
clip_extent = clip_shapefile.total_bounds

# Create a bounding box geometry from the shapefile extent
bbox = box(*clip_extent)

# Subset the NetCDF data using the bounding box
clipped_data = dataset.sel(lat=slice(clip_extent[1], clip_extent[3]), lon=slice(clip_extent[0], clip_extent[2]))

# Save the clipped data to a new NetCDF file
output_nc_file = "../data/clip_wettasmin_W5E5v2.0_2019.nc"
clipped_data.to_netcdf(output_nc_file)
