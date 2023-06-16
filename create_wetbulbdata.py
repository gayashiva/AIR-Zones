import xarray as xr
import numpy as np
import pandas as pd

# Define the wet bulb temperature calculation function
def calculate_Tw(T, RH):
    term1 = T * np.arctan(0.151977 * np.sqrt(RH + 8.313659))
    term2 = np.arctan(T + RH)
    term3 = np.arctan(RH - 1.676331)
    term4 = 0.00391838 * np.power(RH, 1.5) * np.arctan(0.023101 * RH)

    Tw = term1 + term2 - term3 + term4 - 4.686035
    return Tw

# df = pd.read_csv('data/guttannen22_aws.csv')
# print(df.head())

# # Extract the temperature and humidity data variables for the year 2001
# temperature = df['temp']
# humidity = df['RH']


# # Apply the wet bulb temperature calculation to the temperature and humidity data variables
# wet_temperature = calculate_Tw(temperature, humidity)
# print(wet_temperature)

# Load the temperature and humidity datasets
temperature_ds = xr.open_dataset('data/tasmin_W5E5v2.0_20110101-20191231.nc')
humidity_ds = xr.open_dataset('data/hurs_W5E5v2.0_20110101-20191231.nc')

# Extract the temperature and humidity data variables for the year 2001
temperature = temperature_ds['tasmin'].sel(time='2019') - 273.15
humidity = humidity_ds['hurs'].sel(time='2019')


# Apply the wet bulb temperature calculation to the temperature and humidity data variables
wet_temperature = calculate_Tw(temperature, humidity)

# Create a new DataArray with the wet bulb temperature data
wet_temperature_da = xr.DataArray(wet_temperature, coords=temperature.coords, dims=temperature.dims, name='wet_temperature')

# Create a new Dataset with the wet bulb temperature DataArray
wet_temperature_ds = xr.Dataset({'wet_temperature': wet_temperature_da})

# Save the new dataset to a NetCDF file
wet_temperature_ds.to_netcdf('data/wettasmin_W5E5v2.0_2019.nc')

