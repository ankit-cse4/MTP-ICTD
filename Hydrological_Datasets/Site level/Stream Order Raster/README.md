# Stream Order Raster Dataset

## Overview
This dataset contains raster files representing stream orders for various sites. Stream order is a measure of the hierarchy of streams within a watershed, with higher orders indicating larger and more significant streams.

## Directory Structure
```
/Stream Order Raster/
├── Site1/
│   ├── stream_order.tif
│   └── metadata.json
├── Site2/
│   ├── stream_order.tif
│   └── metadata.json
└── README.md
```

## File Descriptions
- **stream_order.tif**: GeoTIFF file containing the stream order raster data for the site.
- **metadata.json**: JSON file containing metadata about the raster data, including coordinate reference system, resolution, and data source.

## Metadata Fields
- **site_name**: Name of the site.
- **crs**: Coordinate reference system used.
- **resolution**: Spatial resolution of the raster data.
- **data_source**: Source of the data.
- **date_collected**: Date when the data was collected.

## Usage
To use the stream order raster data, you can load the GeoTIFF files into GIS software such as QGIS or ArcGIS. The metadata files provide additional information necessary for proper interpretation and analysis of the data.

## License
This dataset is licensed under the [MIT License](LICENSE).

## Contact
For any questions or further information, please contact [ankitcse4@gmail.com].
