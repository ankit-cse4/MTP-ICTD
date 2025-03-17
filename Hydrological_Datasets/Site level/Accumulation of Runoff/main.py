# initialise the qgis application
# TODO - please add the path to your qgis installation and then run this script

# import statements
import processing
import os

# TODO - import the runoff script, currently not added because it is in review

'''
This script is used to calculate the accumulation of runoff in the watershed. The script uses the r.watershed algorithm
The input parameters are:
1. input_dem: The depressionless DEM file
2. input_runoff_raster: The runoff raster file
3. output_dir: The output directory path to store the temporary and final outputs

* These inputs are results of the runoff script.

The output of the script is the accumulation of runoff in the given ROI

'''

# Define the input/output paths
input_dem = ''   # Depressionless DEM file
input_runoff_raster = ''  # Runoff raster file
output_dir = ''  # Output directory path to store the temporary and final outputs

# Ensure output directory exists
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

accumulation_output = os.path.join(output_dir, 'runoff_accumulation.tif')

processing.run("grass7:r.watershed", {'elevation':input_dem,
                                      'depression':None,
                                      'flow':input_runoff_raster,
                                      'disturbed_land':None,
                                      'blocking':None,
                                      'threshold':100000,
                                      'max_slope_length':None,
                                      'convergence':5,
                                      'memory':300,
                                      '-s':False,
                                      '-m':False,
                                      '-4':False,
                                      '-a':True,
                                      '-b':False,
                                      'accumulation':accumulation_output,
                                      'drainage':'TEMPORARY_OUTPUT',
                                      'basin':'TEMPORARY_OUTPUT',
                                      'stream':'TEMPORARY_OUTPUT',
                                      'half_basin':'TEMPORARY_OUTPUT',
                                      'length_slope':'TEMPORARY_OUTPUT',
                                      'slope_steepness':'TEMPORARY_OUTPUT',
                                      'tci':'TEMPORARY_OUTPUT',
                                      'spi':'TEMPORARY_OUTPUT',
                                      'GRASS_REGION_PARAMETER':None,
                                      'GRASS_REGION_CELLSIZE_PARAMETER':0,
                                      'GRASS_RASTER_FORMAT_OPT':'',
                                      'GRASS_RASTER_FORMAT_META':''})

print('Runoff accumulation completed successfully')