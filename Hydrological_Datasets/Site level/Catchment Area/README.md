# Catchment Area Raster Dataset

## Overview
This dataset contains raster data representing the catchment areas for various sites. The data is useful for hydrological analysis and environmental studies.

## Contents
- `catchment_area_1.tif`: Raster file for catchment area 1.
- `catchment_area_2.tif`: Raster file for catchment area 2.
- `catchment_area_3.tif`: Raster file for catchment area 3.
- `metadata/`: Directory containing metadata files for each raster.

## Metadata
Each raster file is accompanied by a metadata file in the `metadata/` directory. The metadata includes information such as:
- Coordinate reference system (CRS)
- Resolution
- Data source
- Date of creation

## Usage
To use the raster data, you can load it into GIS software such as QGIS or ArcGIS. Below is an example of how to load a raster file using Python and the `rasterio` library:

```python
import rasterio

# Open the raster file
with rasterio.open('catchment_area_1.tif') as src:
  catchment_area = src.read(1)

# Print the shape of the raster
print(catchment_area.shape)
```

## License
This dataset is licensed under the [MIT License](LICENSE).

## Contact
For any questions or further information, please contact [ankitcse4@gmail.com].
