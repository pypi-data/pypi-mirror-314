import torch
import math
import sys
import os
import numpy as np
import time

try:
    import postProcessing as post
    import preProcessing as pre
    from SWE import Godunov
except ImportError:
    from . import postProcessing as post
    from . import preProcessing as pre
    from .SWE import Godunov

def run(inputs):
    # ===============================================
    # Make output folder
    # ===============================================
    output_path = inputs.case_info['output_folder']
    if not os.path.isdir(output_path):
        os.mkdir(output_path)

    # ===============================================
    # set the device
    # ===============================================
    torch.cuda.set_device(inputs.model_params['GPU_device_ID'])
    device = torch.device("cuda", inputs.model_params['GPU_device_ID'])
 
    # ===============================================
    # preprocessing data
    # ===============================================   
    dem, mask, mask_boundary, demMeta, dx, dem_path = pre.import_DEM(inputs.case_info['DEM_path'], inputs.model_params['projected_coordinate'], device)
    end_time = inputs.model_params['end_time']

    dem, mask, given_h, given_Q, given_wl = pre.set_boundary(inputs.boundary, mask, mask_boundary, dem, demMeta, end_time, dx, device)
    gauge_index = pre.set_gauges(inputs.gauges['position'], mask, demMeta, device)
    
    # initial condition
    h0, qx0, qy0 = pre.set_initial_condition(inputs.initial_condition, dem, device)
    
    # rainfall
    rainfall_station_Mask, rainfallMatrix = pre.set_rain_station_mask(inputs.rainfall, dem, end_time, device)
    
    # land use and related parameters
    landuse, landIndex = pre.set_landuse(inputs.landuse, dem, device)
    manning = pre.set_manning(inputs.manning, landIndex)
    if inputs._soil:
        hydraulic_conductivity, capillary_head, water_content_diff = pre.set_infiltration_by_soil(inputs.soil, landIndex)
    else:
        hydraulic_conductivity, capillary_head, water_content_diff = pre.set_infiltration(inputs.infiltration, landIndex)
    sewer_sink = pre.set_sewer_sink(inputs.sewer, landIndex)
    # ===================== end of preprocessing ==========================
    
    # ===============================================
    # numerical tensors initializing
    # ===============================================
    print('Initializing data ...')
    numerical = Godunov(inputs.case_info, inputs.model_params, dx, 0, device)
    del inputs
    
    # initial tensors
    numerical.init__fluidField_tensor(mask, dem, h0, qx0, qy0, device)
    numerical.init__gauges_tensor(gauge_index)
    numerical.init__grid_tensor(landuse, rainfall_station_Mask, mask, device)
    numerical.init__time_series_tensor(given_h, given_Q, given_wl, rainfallMatrix, device)
    numerical.init__parameters_tensor(manning, # friction
                                      hydraulic_conductivity, capillary_head, water_content_diff, # infiltration
                                      sewer_sink,device)   

    # memory release to reduce memory 
    del mask, dem, h0, qx0, qy0, landuse, rainfall_station_Mask
    del manning, hydraulic_conductivity, capillary_head, water_content_diff, sewer_sink
    torch.cuda.empty_cache()  
    
    # ===============================================
    # simulation start!
    # ===============================================
    simulation_start = time.time()
    
    while numerical.t.item() < end_time:
        numerical.add__flux()
        numerical.add__precipitation_source(rainfallMatrix, device)
        numerical.add__infiltration_and_sewer_source()
        numerical.add__friction_source()
        numerical.update__time(device)
        numerical.update__observe_gauges()          
        print("{:.3f}".format(numerical.t.item()))
    
    simulation_end = time.time()
    tot_time = simulation_end - simulation_start
    print(tot_time)
    # simulation end!
    
    # ===============================================
    # Post processing data!
    # =============================================== 
    numerical.write__observe_gauges_and_time()
    post.exportRaster_tiff(dem_path, output_path, archive_pt=False)
    
   


