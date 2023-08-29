import xarray as xr
import numpy as np
import math

def longest_consecutive_sum(lst):
    max_length = 0
    current_length = 0
    current_sum = 0
    max_sum = 0

    for num in lst:
        if not math.isnan(num):
            current_length += 1
            current_sum += num
            if current_length > max_length:
                max_length = current_length
                max_sum = current_sum
            if (current_length == max_length) & ( current_sum < max_sum):
                max_length = current_length
                max_sum = current_sum
        else:
            current_length = 0
            current_sum = 0

    return max_sum, max_length

def consecutive_negative_days(arr):
    mask = arr < 0
    masked = xr.where(mask, arr, np.nan)  # Mask non-negative temperatures
    cndd, cd = longest_consecutive_sum(masked)  # Calculate cumulative sum along time axis
    return cndd, cd

# Load the netCDF file
ds = xr.open_dataset('../output/mt+dis+temp.nc')
var = 'wet_temperature'

# Create an empty array to store new values
new_data1 = np.empty(ds['lat'].shape + ds['lon'].shape)
new_data2 = np.empty(ds['lat'].shape + ds['lon'].shape)

# Loop over latitude and longitude coordinates
for lat_idx, lat in enumerate(ds['lat']):
    for lon_idx, lon in enumerate(ds['lon']):
        if ds.sel(lat=lat, lon = lon)[var].mean(dim='time') != np.nan:
            CNDD, CD = consecutive_negative_days(ds.sel(lat=lat, lon = lon)[var].values)  # Replace retrieve_data with your actual data retrieval logic
            new_data1[lat_idx,lon_idx] = CNDD
            new_data2[lat_idx,lon_idx] = CD
            print(lat.values, lon.values, CD, CNDD)
        else:
            new_data1[lat_idx,lon_idx] = np.nan
            new_data2[lat_idx,lon_idx] = np.nan

# Compute negative degree days for the entire dataset
negativepart = np.less(ds[var], 0) * ds[var]
ndd = np.sum(negativepart, axis=0)  # Sum along the time dimension (assuming the first dimension is time)

# Add the computed NDD values as a new variable to the dataset
ds['negative_degree_days'] = ndd


# Create a new data variable using the calculated values
new_data_var1 = xr.DataArray(new_data1, coords=[ds['lat'], ds['lon']], dims=['lat', 'lon'])
new_data_var2 = xr.DataArray(new_data2, coords=[ds['lat'], ds['lon']], dims=['lat', 'lon'])

# Add the new data variable to the existing dataset
ds['CNDD'] = new_data_var1
ds['CD'] = new_data_var2

leh_coords = (34.163079280645604, 77.58554381044664)
leh_ds = ds.sel(lat=leh_coords[0], lon=leh_coords[1], method='nearest')
ds['normalized_cndd'] = ds['CNDD']/leh_ds['CNDD']

# print(ds['negative_degree_days'].values.max(), ds['negative_degree_days'].values.min())
# print(ds['normalized_ndd'].values.max(), ds['normalized_ndd'].values.min())

# Save the updated dataset with the new variable
output_filename = '../output/mt+dis+temp+cndd.nc'
ds.to_netcdf(output_filename)
