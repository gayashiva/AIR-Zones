import geopandas as gpd
import fiona
from tqdm import tqdm

def reduce_shapefile(original_shapefile, reduced_shapefile, chunk_size):
    # Open the original shapefile in a read-only mode
    with fiona.open(original_shapefile, 'r') as src:
        # Get the metadata of the shapefile
        meta = src.meta

        # Get the total number of features in the shapefile
        total_features = len(src)

        # Create an empty list to store the reduced data
        reduced_data = []

        # Initialize the progress bar
        progress_bar = tqdm(total=total_features, unit='feature')

        # Create a new shapefile for the reduced data
        with fiona.open(reduced_shapefile, 'w', **meta) as dst:
            # Iterate over the shapefile records in chunks
            for i, feature in enumerate(src):
                # Process the feature and filter rows where ORD_FLOW equals 10
                if feature['properties']['ORD_FLOW'] == 10:
                    reduced_data.append(feature)

                # Check if the chunk size has been reached
                if i > 0 and (i + 1) % chunk_size == 0:
                    # Write the reduced data to the new shapefile
                    dst.writerecords(reduced_data)

                    # Clear the reduced data list for the next chunk
                    reduced_data = []

                # Update the progress bar
                progress_bar.update(1)

            # Write any remaining data to the new shapefile
            if reduced_data:
                dst.writerecords(reduced_data)

                # Update the progress bar
                progress_bar.update(len(reduced_data))

        # Close the progress bar
        progress_bar.close()

# Set the paths for the original and reduced shapefiles
original_shapefile = 'data/HydroRIVERS_v10_shp/HydroRIVERS_v10_shp/HydroRIVERS_v10.shp'
reduced_shapefile = 'data/HydroRIVERS_v10_shp/reduced_HydroRIVERS_v10.shp'

# Set the chunk size (adjust this based on your available memory)
chunk_size = 10000

# Call the function to reduce the shapefile in chunks
reduce_shapefile(original_shapefile, reduced_shapefile, chunk_size)

# import geopandas as gpd

# # def reduce_shapefile(original_shapefile, reduced_shapefile):
# #     # Read the original shapefile
# #     data = gpd.read_file(original_shapefile)
# #     
# #     # Select the desired columns (geometry and ORD_FLOW)
# #     columns_to_keep = ['ORD_FLOW', 'DIS_AV_CMS', 'geometry']
# #     reduced_data = data[columns_to_keep]
# #     
# #     # Save the reduced data to a new shapefile
# #     reduced_data.to_file(reduced_shapefile)

# def reduce_shapefile(original_shapefile, reduced_shapefile):
#     # Read the original shapefile
#     data = gpd.read_file(original_shapefile)

#     # Select the desired columns (geometry and ORD_FLOW)
#     columns_to_keep = ['ORD_FLOW', 'DIS_AV_CMS', 'geometry']
#     reduced_data = data[columns_to_keep]
#     
#     # Filter rows where ORD_FLOW equals 10
#     reduced_data = reduced_data[reduced_data['ORD_FLOW'] == 10]
#     
#     # Save the reduced data to a new shapefile
#     reduced_data.to_file(reduced_shapefile)

# # Set the paths for the original and reduced shapefiles
# original_shapefile = 'data/HydroRIVERS_v10_shp/HydroRIVERS_v10_shp/HydroRIVERS_v10.shp'
# reduced_shapefile = 'data/HydroRIVERS_v10_shp/reduced_HydroRIVERS_v10.shp'

# # Call the function to reduce the shapefile
# reduce_shapefile(original_shapefile, reduced_shapefile)
