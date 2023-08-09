import rioxarray as rxr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import numpy as np
import xarray as xr

def print_raster(raster):
    print(
        f"shape: {raster.rio.shape}\n"
        f"resolution: {raster.rio.resolution()}\n"
        f"bounds: {raster.rio.bounds()}\n"
        f"sum: {raster.sum().item()}\n"
        f"CRS: {raster.rio.crs}\n"
    )

create_mt_dis = 0
create_mt_dis_temp =1

if create_mt_dis:

    mountain_path = "../data/GlobalMountainsK3Binary/k1binary.tif"
    mt_ds = rxr.open_rasterio(mountain_path)

    dis_path = "../data/HydroRIVERS_v10_shp/raster/global_reduced_HydroRIVERS_v10.tif"
    dis_ds = rxr.open_rasterio(dis_path)

    # Define the latitude threshold for the Antarctic region
    antarctic_lat_threshold = -60.0

    # Create a mask for the Antarctic region
    antarctic_mask = dis_ds['y'] < antarctic_lat_threshold

    # Replace values in the Antarctic region with zeros using the mask
    dis_ds = dis_ds.where(~antarctic_mask, 1)

    print("Original Raster:\n----------------\n")
    print_raster(mt_ds)
    print("Raster to Match:\n----------------\n")
    print_raster(dis_ds)

    mt_match =mt_ds.rio.reproject_match(dis_ds)

    print("Original Raster:\n----------------\n")
    print_raster(dis_ds)
    print("Raster to Match:\n----------------\n")
    print_raster(mt_match)

    dis_ds_invert = dis_ds - 1
    # Create a new raster array where the value is 1 for mountain regions with non-zero discharge
    mt_dis = np.logical_and(mt_match, dis_ds_invert)
    # Convert bool to int
    mt_dis = mt_dis * 1
    # Save the resampled dataset to a new NetCDF file
    mt_dis_ds = mt_dis.to_dataset(name="AGregions")
    mt_dis_ds = mt_dis_ds.rename({'x': 'lon','y': 'lat'})
    print(mt_dis_ds)
    mt_dis_ds = mt_dis_ds.squeeze("band")

    # Save the resampled dataset to a new NetCDF file
    mt_dis_ds.to_netcdf('../output/mt+dis.nc')

    print("Montain and discharge dataset saved with binary mask.")

if create_mt_dis_temp:
    mt_dis = xr.open_dataset('../output/mt+dis.nc')
    # Load the netCDF file
    temp = xr.open_dataset('../data/wettasmin_W5E5v2.0_2019.nc')
    # temp = temp['wet_temperature']
    print(temp)

    #interpolate into the higher resolution grid from IMERG
    interp_mt_dis = mt_dis.interp(lat=temp["lat"], lon=temp["lon"])

    print(interp_mt_dis)

    # Broadcast the mask along the time dimension
    interp_mt_dis= interp_mt_dis.expand_dims(time=temp['time'], axis=0)

    # Create a mask using the binary dataset values where the value is 1
    mask = interp_mt_dis['AGregions'] == 1

    # Ensure the mask's latitudes and longitudes match the data's latitudes and longitudes
    lat_dim = temp['lat'].values
    lon_dim = temp['lon'].values

    # # Broadcast the mask along the lat and lon dimensions
    # broadcasted_mask = mask.sel(lat=lat_dim, lon=lon_dim, method='nearest')

    # Print the dimensions of the mask and the data
    # print("Mask dimensions:", mask.shape)
    # print("Data dimensions:", temp.shape)

    # Apply the mask to the temperature dataset using boolean indexing
    reduced_temp = temp.where(mask, drop=True)

    print(reduced_temp)
    # Save the resampled dataset to a new NetCDF file
    reduced_temp.to_netcdf('../output/mt+dis+temp.nc')

    print("Temperature dataset masked and saved with binary mask.")
