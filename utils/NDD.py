import xarray as xr
import numpy as np

# Load the netCDF file
dataset = xr.open_dataset('../output/mt+dis+temp.nc')
var = 'wet_temperature'

# Compute negative degree days for the entire dataset
negativepart = np.less(dataset[var], 0) * dataset[var]
ndd = np.sum(negativepart, axis=0)  # Sum along the time dimension (assuming the first dimension is time)

# Add the computed NDD values as a new variable to the dataset
dataset['negative_degree_days'] = ndd

leh_coords = (34.163079280645604, 77.58554381044664)
leh_ds = dataset.sel(lat=leh_coords[0], lon=leh_coords[1], method='nearest')

dataset['normalized_ndd'] = ndd/leh_ds['negative_degree_days']

# Count NDD values greater than one
# ndd_count = np.sum(dataset['normalized_ndd']>1)

print(dataset['negative_degree_days'].max(), dataset['negative_degree_days'].min())
print(dataset['normalized_ndd'].max(), dataset['normalized_ndd'].min())
print(dataset)

# Save the updated dataset with the new variable
output_filename = '../output/mt+dis+temp+ndd.nc'
dataset.to_netcdf(output_filename)
