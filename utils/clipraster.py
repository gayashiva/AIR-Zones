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
