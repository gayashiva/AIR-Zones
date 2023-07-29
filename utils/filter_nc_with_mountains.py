import xarray as xr
import geopandas as gpd
from shapely.geometry import Point

# Load the NetCDF file
nc_file = '../data/wettasmin_W5E5v2.0_2019.nc'
ds = xr.open_dataset(nc_file)

# Load the mountain regions shapefile
mountain_regions = gpd.read_file('../data/K3Binary/k3binary.shp')

# Function to check if a point lies within any of the mountain regions
def is_point_within_mountains(lon, lat, mountain_regions):
    point = Point(lon, lat)
    for index, row in mountain_regions.iterrows():
        if point.within(row['geometry']):
            return True
    return False

# Spatially subset the NetCDF data
lon_values = ds['lon'].values
lat_values = ds['lat'].values
selected_indices = []
for i in range(len(lon_values)):
    for j in range(len(lat_values)):
        if is_point_within_mountains(lon_values[i], lat_values[j], mountain_regions):
            selected_indices.append((j, i))

# Create a new subset of the NetCDF data
subset_ds = ds.isel(lat=slice(min(selected_indices)[0], max(selected_indices)[0]+1),
                    lon=slice(min(selected_indices)[1], max(selected_indices)[1]+1))

# Save the subset as a new NetCDF file
subset_ds.to_netcdf('../data/filtered_wettasmin_W5E5v2.0_2019.nc')

# Close the original NetCDF dataset
ds.close()
