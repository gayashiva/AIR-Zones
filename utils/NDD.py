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
    print(masked)
    cndd, cd = longest_consecutive_sum(masked)  # Calculate cumulative sum along time axis
    return cndd, cd

# Load the netCDF file
dataset = xr.open_dataset('../output/mt+dis+temp.nc')
var = 'wet_temperature'

# # Iterate over latitudes and longitudes
# for lats in dataset.coords['lat'].values:
#     for lons in dataset.coords['lon'].values:
#         if dataset.sel(lat=lats, lon = lons)[var].mean(dim='time') != np.nan:
#             CNDD, CD = consecutive_negative_days(dataset.sel(lat=lats, lon = lons)[var].values)  # Replace retrieve_data with your actual data retrieval logic
#             dataset.sel(lat=lats, lon = lons)['CNDD'] = CNDD
#             dataset.sel(lat=lats, lon = lons)['CD'] = CD
#             print(lats, lons, CD, CNDD)
#         else:
#             dataset.sel(lat=lats, lon = lons)['CNDD'] = np.nan
#             dataset.sel(lat=lats, lon = lons)['CD'] = np.nan

# # Compute negative degree days for the entire dataset
# negativepart = np.less(dataset[var], 0) * dataset[var]
# ndd = np.sum(negativepart, axis=0)  # Sum along the time dimension (assuming the first dimension is time)

# # Add the computed NDD values as a new variable to the dataset
# dataset['negative_degree_days'] = ndd

leh_coords = (34.163079280645604, 77.58554381044664)
leh_ds = dataset.sel(lat=leh_coords[0], lon=leh_coords[1], method='nearest')

south_america = (-29.75, -69.75)
sa_ds = dataset.sel(lat=south_america[0], lon=south_america[1], method='nearest')
# print(leh_ds['negative_degree_days'].values, leh_ds['CNDD'].values)

lats, lons = leh_coords[0], leh_coords[1]

# if leh_ds[var].mean(dim='time') != np.nan:
#     CNDD, CD = consecutive_negative_days(leh_ds[var].values)  # Replace retrieve_data with your actual data retrieval logic
#     leh_ds['CNDD'] = CNDD
#     leh_ds['CD'] = CD
#     print("Leh",CD, CNDD)

if sa_ds[var].mean(dim='time') != np.nan:
    CNDD, CD = consecutive_negative_days(sa_ds[var].values)  # Replace retrieve_data with your actual data retrieval logic
    sa_ds['CNDD'] = CNDD
    sa_ds['CD'] = CD
    print("SA", CD, CNDD)


# dataset['normalized_ndd'] = ndd/leh_ds['negative_degree_days']

# print(dataset['negative_degree_days'].values.max(), dataset['negative_degree_days'].values.min())
# print(dataset['normalized_ndd'].values.max(), dataset['normalized_ndd'].values.min())

# # Save the updated dataset with the new variable
# output_filename = '../output/mt+dis+temp+ndd.nc'
# dataset.to_netcdf(output_filename)
