import xarray as xr
import numpy as np
import json

def return_max_coords(xarraydata):
    max = xarraydata.where(xarraydata==xarraydata.max(), drop=True).squeeze()
    return [float(max.lat.values), float(max.lon.values)]

# Load the netCDF file
dataset = xr.open_dataset('../output/mt+dis+temp+cndd.nc')

# Define lat and lon ranges for each region
north_america_lat_range = (20, 90)
north_america_lon_range = (-170, -30)

south_america_lat_range = (-60, 20)
south_america_lon_range = (-90, -30)

central_asia_lat_range = (30, 70)
central_asia_lon_range = (40, 100)

europe_lat_range = (35, 70)
europe_lon_range = (-25, 45)

# Define masks for each region based on lat and lon ranges
north_america_mask = (
    (dataset['lat'] >= north_america_lat_range[0])
    & (dataset['lat'] <= north_america_lat_range[1])
    & (dataset['lon'] >= north_america_lon_range[0])
    & (dataset['lon'] <= north_america_lon_range[1])
)

south_america_mask = (
    (dataset['lat'] >= south_america_lat_range[0])
    & (dataset['lat'] <= south_america_lat_range[1])
    & (dataset['lon'] >= south_america_lon_range[0])
    & (dataset['lon'] <= south_america_lon_range[1])
)

central_asia_mask = (
    (dataset['lat'] >= central_asia_lat_range[0])
    & (dataset['lat'] <= central_asia_lat_range[1])
    & (dataset['lon'] >= central_asia_lon_range[0])
    & (dataset['lon'] <= central_asia_lon_range[1])
)

europe_mask = (
    (dataset['lat'] >= europe_lat_range[0])
    & (dataset['lat'] <= europe_lat_range[1])
    & (dataset['lon'] >= europe_lon_range[0])
    & (dataset['lon'] <= europe_lon_range[1])
)

# Apply the masks and find the maximum index coordinate for each region
max_index_north_america = return_max_coords(dataset.where(north_america_mask)['normalized_cndd'])
max_index_south_america = return_max_coords(dataset.where(south_america_mask)['normalized_cndd'])
max_index_central_asia = return_max_coords(dataset.where(central_asia_mask)['normalized_cndd'])
max_index_europe = return_max_coords(dataset.where(europe_mask)['normalized_cndd'])

# Print the results
print("Max index in North America:", max_index_north_america, dataset.sel(lat = max_index_north_america[0], lon=
                                                                          max_index_north_america[1], method
                                                                          ='nearest').normalized_cndd.values)
print("Max index in South America:", max_index_south_america, dataset.sel(lat = max_index_south_america[0], lon=
                                                                          max_index_south_america[1], method
                                                                          ='nearest').normalized_cndd.values)
print("Max index in Central Asia:", max_index_central_asia, dataset.sel(lat = max_index_central_asia[0], lon=
                                                                          max_index_central_asia[1], method
                                                                          ='nearest').normalized_cndd.values)
print("Max index in Europe:", max_index_europe, dataset.sel(lat = max_index_europe[0], lon=
                                                                          max_index_europe[1], method
                                                                          ='nearest').normalized_cndd.values)
north_america_region =str(max_index_north_america[0] - 0.05) + "/" + str(max_index_north_america[1] - 0.05) +"/"+str(max_index_north_america[0] + 0.05) + "/" + str(max_index_north_america[1] + 0.05)
print(north_america_region)

coords = {'north_america' : max_index_north_america, 'south_america': max_index_south_america, 'central_asia':
          max_index_central_asia, 'europe':max_index_europe}
for key, value in coords.items():
    print(key, value)
    print(str(value[0] - 0.05) + "/" + str(value[1] - 0.05) +"/"+str(value[0] + 0.05) + "/" +str(value[1] +0.05))

regions = { 'south_america': max_index_south_america, 'central_asia':
          max_index_central_asia, 'europe':max_index_europe}

with open("../output/max_region_coords.json", "w") as outfile:
    json.dump(coords, outfile)
