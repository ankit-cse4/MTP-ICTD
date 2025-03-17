import numpy as np
import rasterio
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, LineString
import ast  # To parse string representation of tuples

# Define flow direction offsets
flow_direction_offsets = {
    1: (-1, 1),   # NE
    2: (-1, 0),   # N
    3: (-1, -1),  # NW
    4: (0, -1),   # W
    5: (1, -1),   # SW
    6: (1, 0),    # S
    7: (1, 1),    # SE
    8: (0, 1)     # E
}

def load_raster(file_path):
    """Load raster file and return array, transform, and nodata value."""
    with rasterio.open(file_path) as src:
        return src.read(1), src.transform, src.nodata  

def get_max_accumulation_pixel(mask, accumulation):
    """Find the pixel (row, col) with max accumulation inside the given mask."""
    max_idx = np.argmax(accumulation * mask)  # Get flattened index
    return np.unravel_index(max_idx, accumulation.shape)  # Convert to (row, col)

def get_downstream_mw_id(max_row, max_col, flow_direction, micro_watershed, nodata_value):
    """Find the downstream micro-watershed ID based on flow direction."""
    flow_value = flow_direction[max_row, max_col]

    if flow_value in flow_direction_offsets:
        d_row, d_col = flow_direction_offsets[flow_value]
        new_row, new_col = max_row + d_row, max_col + d_col

        # Check if new pixel is within bounds
        if 0 <= new_row < micro_watershed.shape[0] and 0 <= new_col < micro_watershed.shape[1]:
            new_mw_id = micro_watershed[new_row, new_col]
            return None if new_mw_id == nodata_value else new_mw_id
    return None

def compute_mw_connections(accumulation, flow_direction, micro_watershed, nodata_value):
    """Compute the edges representing micro-watershed connections."""
    unique_watersheds = np.unique(micro_watershed)
    unique_watersheds = unique_watersheds[unique_watersheds > 0]  # Exclude background (0 or NoData)
    
    edges = []
    
    for mw_id in unique_watersheds:
        mask = (micro_watershed == mw_id)
        max_row, max_col = get_max_accumulation_pixel(mask, accumulation)
        new_mw_id = get_downstream_mw_id(max_row, max_col, flow_direction, micro_watershed, nodata_value)
        
        if new_mw_id is not None and new_mw_id != mw_id:
            edges.append((mw_id, new_mw_id))
    
    return edges

def parse_centroid(centroid_str):
    """Parse centroid from string representation (if stored as text)."""
    try:
        centroid_tuple = ast.literal_eval(centroid_str)  # Convert string to tuple
        return Point(centroid_tuple)
    except (SyntaxError, ValueError):
        return None  # Return None if parsing fails

def update_micro_watershed_shapefile(mw_shapefile, edges):
    """Update the micro watershed shapefile with downstream_mws column."""
    gdf = gpd.read_file(mw_shapefile)
    edges_dict = dict(edges)  # Convert list of tuples to dictionary
    gdf["downstream_mws"] = gdf["mws_id"].map(edges_dict)
    updated_shapefile = mw_shapefile.replace(".shp", "_updated.shp")
    gdf.to_file(updated_shapefile)
    print(f"Updated micro watershed shapefile saved to: {updated_shapefile}")
    return gdf

def create_flow_line_shapefile(mw_shapefile, edges, output_shapefile):
    """Create a new line shapefile for micro watershed flow connections."""
    gdf = gpd.read_file(mw_shapefile)

    # Extract centroid points from the 'centroid' column
    gdf["centroid"] = gdf["centroid"].apply(parse_centroid)
    centroid_dict = {row["mws_id"]: row["centroid"] for _, row in gdf.iterrows() if row["centroid"]}

    line_geometries = []
    for mw_id, new_mw_id in edges:
        if mw_id in centroid_dict and new_mw_id in centroid_dict:
            line = LineString([centroid_dict[mw_id], centroid_dict[new_mw_id]])
            line_geometries.append({"mws_id": mw_id, "new_mws_id": new_mw_id, "geometry": line})

    line_gdf = gpd.GeoDataFrame(line_geometries, geometry="geometry", crs=gdf.crs)
    line_gdf.to_file(output_shapefile)
    print(f"Flow line shapefile saved to: {output_shapefile}")

def save_edges_to_csv(edges, output_file="micro_watershed_edges.csv"):
    """Save micro-watershed edges to a CSV file."""
    df = pd.DataFrame(edges, columns=["mw_id", "new_mw_id"])
    df.to_csv(output_file, index=False)
    print(f"Edges saved to {output_file}")


if __name__ == "__main__":
    # File paths (update these as needed)
    accumulation_raster = "accumulation.tif"
    flow_direction_raster = "flow_direction.tif"
    micro_watershed_raster = "micro_watershed.tif"
    mw_shapefile = "micro_watershed.shp"  # Vector shapefile with centroid column

    accumulation, _, _ = load_raster(accumulation_raster)
    flow_direction, _, _ = load_raster(flow_direction_raster)
    micro_watershed, _, nodata_value = load_raster(micro_watershed_raster)

    edges = compute_mw_connections(accumulation, flow_direction, micro_watershed, nodata_value)
    
    # Save edges as CSV
    save_edges_to_csv(edges)

    # Update micro watershed shapefile
    updated_gdf = update_micro_watershed_shapefile(mw_shapefile, edges)

    # Create flow line shapefile
    flow_line_shapefile = mw_shapefile.replace(".shp", "_flow_lines.shp")
    create_flow_line_shapefile(updated_gdf, edges, flow_line_shapefile)