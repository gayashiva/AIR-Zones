# import rasterio
# from rasterio.mask import mask
# from rasterio.windows import Window
# import numpy as np

# def clip_raster_by_mask(raster_path, mask_path, mask_value, output_path, no_data_value=None, block_size=256):
#     with rasterio.open(raster_path) as src:
#         with rasterio.open(mask_path) as mask_src:
#             profile = src.profile.copy()
#             profile.update(count=1, dtype=rasterio.float32)

#             block_windows = [Window(col_off=col, row_off=row, width=block_size, height=block_size)
#                              for col in range(0, src.width, block_size)
#                              for row in range(0, src.height, block_size)]

#             with rasterio.open(output_path, 'w', **profile) as dst:
#                 for window in block_windows:
#                     src_data = src.read(1, window=window)

#                     # Clip the data using the mask
#                     mountain_data = mask_src.read(1, window=window)
#                     mask = mountain_data == mask_value
#                     clipped_data = src_data * mask

#                     # Set areas outside the mountains to a specific NoData value (optional)
#                     if no_data_value is not None:
#                         clipped_data[~mask] = no_data_value

#                     # Convert the clipped_data to the data type of the output raster
#                     clipped_data = clipped_data.astype(profile['dtype'], copy=False)

#                     dst.write(clipped_data, window=window)

# # Example usage:
# discharge_raster_path = "../data/HydroRIVERS_v10_shp/raster/reduced_HydroRIVERS_v10.tif"
# mountain_raster_path = "../data/GlobalMountainsK3Binary/k3binary.tif"
# output_clipped_raster_path = "../data/clipped_raster.tif"

# mask_value = 1  # Set the mask value based on which you want to clip the discharge raster
# no_data_value = -9999  # Set the desired NoData value (optional, set to None if not needed)

# clip_raster_by_mask(discharge_raster_path, mountain_raster_path, mask_value, output_clipped_raster_path, no_data_value)

import rasterio
from rasterio.mask import mask
import dask.array as da

def clip_raster_by_geometry_dask(raster_to_clip_path, raster_with_geometry_path, output_clipped_raster_path, block_size=512):
    # Read the raster data to clip
    with rasterio.open(raster_to_clip_path) as src_to_clip:
        raster_profile = src_to_clip.profile
        nodata_value = src_to_clip.nodata
        raster_to_clip_data = src_to_clip.read(1)

    # Read the raster data with the geometry to use for clipping
    with rasterio.open(raster_with_geometry_path) as src_with_geometry:
        raster_geometry = src_with_geometry.bounds

    # Perform the clip operation using dask.array
    raster_dask = da.from_array(raster_to_clip_data, chunks=(block_size, block_size))
    clipped_data_dask = mask(dataset=raster_dask, shapes=[raster_geometry], crop=True)[0]

    # Convert dask.array to numpy array
    clipped_data = clipped_data_dask.compute()

    # Update the metadata for the clipped raster
    clipped_meta = raster_profile.copy()
    clipped_meta.update({
        "height": clipped_data.shape[0],
        "width": clipped_data.shape[1],
        "transform": src_to_clip.window(*raster_geometry).transform(),  # Update the transform based on the clipped extent
        "nodata": nodata_value  # Set the nodata value for the clipped raster
    })

    # Write the clipped raster to a new file
    with rasterio.open(output_clipped_raster_path, "w", **clipped_meta) as dest:
        dest.write(clipped_data, 1)

# Example usage:
discharge_raster_path = "../data/HydroRIVERS_v10_shp/raster/reduced_HydroRIVERS_v10.tif"
mountain_raster_path = "../data/GlobalMountainsK3Binary/k3binary.tif"
output_clipped_raster_path = "../data/clipped_raster.tif"

clip_raster_by_geometry(discharge_raster_path, mountain_raster_path, output_clipped_raster_path)
