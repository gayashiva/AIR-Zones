import geopandas as gpd
from shapely.geometry import Point, LineString
from tqdm import tqdm  # Import tqdm for the progress bar

# Load the mountain regions shapefile
mountain_regions = gpd.read_file('../data/K3Binary/k3binary.shp')

# Define the chunk size
chunk_size = 15000  # You can adjust this value based on your memory capacity and data size

# Specify the river discharge shapefile path
river_discharge_file_path = '../data/HydroRIVERS_v10_shp/reduced_HydroRIVERS_v10.shp'

# Load the river discharge shapefile
river_discharge_data = gpd.read_file(river_discharge_file_path)
print("Files loaded")

# Function to check if any part of a LineString intersects with any of the mountain regions
def is_linestring_within_mountains(linestring, mountain_regions):
    for geom in mountain_regions['geometry']:
        if linestring.intersects(geom):
            return True
    return False

# Filter the river discharge data points that intersect with the mountains
num_chunks = len(river_discharge_data) // chunk_size + 1  # Calculate the number of chunks
result_gdf = gpd.GeoDataFrame()  # Initialize an empty GeoDataFrame to store the combined data

for i in tqdm(range(num_chunks), total=num_chunks, desc="Processing chunks"):
    start_idx = i * chunk_size
    end_idx = (i + 1) * chunk_size
    river_discharge_chunk = river_discharge_data.iloc[start_idx:end_idx]
    
    # Filter the river discharge data points that intersect with the mountains for each chunk
    discharge_within_mountains = []
    for idx, row in river_discharge_chunk.iterrows():
        geometry = row['geometry']
        if isinstance(geometry, LineString):
            if is_linestring_within_mountains(geometry, mountain_regions):
                discharge_within_mountains.append(row)
    
    # Create a new GeoDataFrame with the filtered data for each chunk
    chunk_gdf = gpd.GeoDataFrame(discharge_within_mountains)

    # Append the chunk data to the result GeoDataFrame
    result_gdf = result_gdf.append(chunk_gdf, ignore_index=True)

# Save the combined GeoDataFrame to a single shapefile
result_gdf.to_file('../data/HydroRIVERS_v10_shp/filtered_HydroRIVERS_v10_shp/filtered_HydroRIVERS_v10.shp', index=False)
