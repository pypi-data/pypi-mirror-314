import os
import pkg_resources

def get_sample_data():    
    case_folder = pkg_resources.resource_filename(__name__, 'sample')
    dem_file = 'DEM.tif'
    output_folder = 'output'
    rainfall_source = 0
    return case_folder, dem_file, output_folder, rainfall_source

def get_sample_outline():
   return 'outline.shp'