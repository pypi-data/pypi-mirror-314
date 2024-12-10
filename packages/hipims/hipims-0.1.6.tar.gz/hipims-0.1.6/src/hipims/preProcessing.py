import os
import torch
import numpy as np
from shapely.geometry import box
import rasterio as rio
import scipy.ndimage as ndi

import pandas as pd
from rasterio.features import geometry_mask

def import_DEM(DEM_path, projected_coordinate, device):
    # import DEM data
    with rio.open(DEM_path) as src:
        demMasked = src.read(1, masked=True)
        demMeta = src.meta
        nodata=src.nodata
    # process DEM data
    dem = np.ma.filled(demMasked, fill_value=-9999.)
    mask = demMasked.mask
    # mask = (dem == nodata) | np.isnan(dem)
    
    mask = torch.from_numpy(mask)  

    # project data if needed
    dx = _degreeToMeter(projected_coordinate, demMeta['transform'][0])

    # Create a padded mask to add a border
    mask = torch.nn.functional.pad(mask, (1, 1, 1, 1), mode='constant', value=True)
    
    # generate_boundary_mask
    oppo_direction = np.array([[-1, 1], [1, 0], [1, 1], [-1, 0]])
    maskID = mask.to(torch.int32)
    mask_boundary = torch.zeros_like(mask, dtype=torch.int32)
    for i in range(4):
        mask_boundary = mask_boundary + maskID.roll(int(oppo_direction[i][0]),
                                                    int(oppo_direction[i][1]))
    mask_boundary[mask] = 0
    mask_boundary = mask_boundary[1:-1,1:-1].to(torch.bool)
    
    mask = ~mask
    # set nan value area as False
    mask = mask[1:-1,1:-1]

    # boundary slope adjustment to ensure that the water flow calculations do not diverge or lead to unphysical results
    distance = ndi.distance_transform_edt(mask)
    slope_factor = 0.01
    target_area = (distance > 0) & (distance <= 3)
    dem[target_area] -= (3 - distance[target_area]) * slope_factor * dx

    # dem from torch to numpy
    dem = torch.from_numpy(dem).to(device=device)
    
    mask = mask.to(torch.int32)
    
    return dem, mask, mask_boundary, demMeta, dx, DEM_path


def _degreeToMeter(projected_coordinate, Unit):
    if projected_coordinate:
        Unit = Unit * (2. * np.math.pi * 6371004.) / 360.
    return Unit
    
def set_gauges(gauges_position, mask, demMeta, device):
    gauge_index_1D = torch.tensor([])
    if gauges_position.size > 0:
        mask_gauge = mask.clone()  # here make a copy of mask values
        rows, cols = rio.transform.rowcol(demMeta['transform'],
                                          gauges_position[:, 0],
                                          gauges_position[:, 1])
        mask_gauge[rows, cols] = 100
        gauge_index_1D = torch.flatten(
            (mask_gauge[mask_gauge > 0] >= 99).nonzero()).type(torch.int64)

        rows = np.array(rows)
        cols = np.array(cols)
        array = rows * mask.size()[1] + cols

        order = array.argsort()
        ranks = order.argsort()

        gauge_index_1D = gauge_index_1D[ranks]
    gauge_index_1D.to(device)
    return gauge_index_1D

def set_boundary(boundary, mask, mask_boundary, dem, demMeta, end_time, dx, device):
    # 7 boundary types
    bc_dict = {'RIGID': 3, 
               'WALL_SLIP': 4, 
               'OPEN': 5, 
               'H_GIVEN': 6, 
               'Q_GIVEN': 7,
               'WL_GIVEN': 8,
               'FALL': 9}
    
    source_list = {'H_GIVEN': [], 
               'Q_GIVEN': [],
               'WL_GIVEN': []}
      
    # set default boundary
    default_BC = boundary['outline_boundary']
    if isinstance(default_BC, str):
        if default_BC in bc_dict:
            default_BC = bc_dict[default_BC]
        else:
            raise ValueError("The default_BC should be one of: " + ", ".join(bc_dict.keys()))
    mask[mask_boundary] = default_BC * 10
    
    # the boundary index will start with 0
    bc_count = [-1] * len(bc_dict)
    bc_count[list(bc_dict.values()).index(int(str(default_BC)[0]))] += 1

    # set index for each boundary
    if boundary['num_boundary'] > 0:  
        mask_box = torch.zeros_like(mask, dtype=torch.bool)
        for bound in boundary['bound_list']: 
            mask_box[:] = 0
            
            # set boundary type
            bc_type = bound['type'] 
            try:
                BC_TYPE = bc_dict[bc_type] 
            except KeyError:
                print("The keys should be: RIGID, WALL_SLIP, OPEN, H_GIVEN, Q_GIVEN, WL_GIVEN")
        
            # set boundary grid cells
            # set boundary box
            extent = bound['extent']
            boundary_box = box(extent[0], extent[2], extent[1], extent[3])
            mask_box = geometry_mask([boundary_box], transform=demMeta['transform'], invert=True, out_shape=mask.shape)       

            # set boundary index
            bc_count[list(bc_dict.values()).index(BC_TYPE)] += 1
            # set boundary grid index as 'type & index'
            bound_loc = (mask_boundary & mask_box).bool()

            mask[bound_loc] = int(
                str(BC_TYPE) +
                str(bc_count[list(bc_dict.values()).index(BC_TYPE)]))

            # read corresponding source file for h and hU
            if bc_type in ['Q_GIVEN', 'H_GIVEN', 'WL_GIVEN']:
                source = _set_time_series(bound['source'], end_time)
                if bc_type == 'Q_GIVEN' and source.shape[1]==2:
                    source = _convert_flow2velocity(source, bound_loc, mask, dx)
                
                source_list[bc_type].append(source)         

    # update mask with boundary
    mask_GPU = mask.to(device=device)
    
    # interpolate boundary source
    source_dict = _interpolate_source(source_list)

    # # # lower open boundary dem to avoid divergence of the solution
    # dem[mask_GPU==50] -= 0.01 * dx
    return dem, mask_GPU, source_dict['H_GIVEN'], source_dict['Q_GIVEN'], source_dict['WL_GIVEN']

def  _convert_flow2velocity(source, bound_loc, mask, dx):
    rows, cols = torch.where(bound_loc)
    rows = rows.numpy()
    cols = cols.numpy()

    if len(rows)==0 or len(cols)==0:
        raise KeyError
    theta = _get_bound_normal(cols, rows, mask)

    width = (np.max(cols) - np.min(cols) + 1) * dx
    hight = (np.max(rows) - np.min(rows) + 1) * dx
    
    ux = source[:,1] * np.cos(theta) / hight
    uy = source[:,1] * np.sin(theta) / width 

    source = np.c_[source[:,0], ux, uy]

    return source
    

def _get_bound_normal(cols, rows, mask):
    """get the normal vector of the bound line
    """
    if np.unique(cols).size==1: # vertical bound line
        theta = 0
    elif np.unique(rows).size==1: # horizontal bound line
        theta = np.pi*0.5
    else:
        boundary_slope = np.polyfit(rows, cols, 1)
        theta = np.arctan(boundary_slope[0])

    # check the direction of noraml vector
    test_direction_point = np.array([(rows[0] + rows[-1])/2 - np.sin(theta)*2, 
                                 (cols[0] + cols[-1])/2 + np.cos(theta)*2])
    r_test = int(round(test_direction_point[0]))
    c_test = int(round(test_direction_point[1]))
    
    r, c = mask.shape
    if not (0 <= r_test < r and 0 <= c_test < c) or not(mask[r_test, c_test]):
        theta = theta + np.pi
    
    return theta

def _interpolate_source(source_list):
    result_dict = {}
    for key, array_list in source_list.items():
        if not array_list:
            result_dict[key] = np.array([[0, 0], [60, 0]])
            continue
        
        all_times = np.unique(np.concatenate([array[:, 0] for array in array_list]))
        interpolated_values = []
        for array in array_list:
            times = array[:, 0]
            values = array[:, 1:]
            interpolated = [np.interp(all_times, times, values[:, i]) for i in range(values.shape[1])]
            interpolated_values.append(np.vstack(interpolated).T)

        if interpolated_values:
            continuous_array = np.ascontiguousarray(np.hstack(interpolated_values))
            result_dict[key] = np.hstack((all_times.reshape(-1, 1), continuous_array))
            
    return result_dict 

# internal funcs
def __import_tif_file(file_path, device):
    with rio.open(file_path) as src:
        file_data_masked = src.read(1, masked=True)
    file_data = np.ma.filled(file_data_masked, fill_value=-9999.)
    file_data = np.nan_to_num(file_data, nan=0)
    file_data = torch.from_numpy(file_data).to(device=device)
    return file_data

# grid data
# dem, land use, rainfall mask
def _set_grid_data(data, z, device):
    if isinstance(data, str):
        data_value = __import_tif_file(data, device)
    elif np.isscalar(data):
        data_value = torch.zeros_like(z, device=device) + data
    else: # array
        data_value = torch.tensor(data, device=device)
    return data_value
 
# time series data
# boundary source, rainfall source  
def _set_time_series(data, end_time):
    if isinstance(data, list):
        file_path, sheet_name = data[0], data[1]  
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        data = df.to_numpy()
    elif isinstance(data, str):
        _, file_ext = os.path.splitext(data)
    
        if file_ext in ['.xls', '.xlsx']:
            df = pd.read_excel(data, engine='openpyxl')
        elif file_ext in ['.txt', '.csv']:
            df = pd.read_csv(data, sep='\t')

        data = df.to_numpy()
    elif np.isscalar(data):
        data = np.array([[0, data], [end_time, data]])
    return data   

# land use based data
# sewer, infiltration, manning
def _set_landuse_based_data(data, landuse_uniq):
    if np.isscalar(data):
        data_array = np.zeros(len(landuse_uniq)) + data
    else:
        data_array = np.zeros(len(landuse_uniq)) + data['default_value']
        ind = np.isin(landuse_uniq, data['special_land_type_value'])
        data_array[ind] = data['special_param_value']
    return data_array

def set_initial_condition(initial_condition, z, device):
    h0 = _set_grid_data(initial_condition['h0'], z, device)
    hU0x = _set_grid_data(initial_condition['hU0x'], z, device)
    hU0y = _set_grid_data(initial_condition['hU0y'], z, device)
    return h0, hU0x, hU0y
    
def set_landuse(landuse, z, device):
    landuse = _set_grid_data(landuse['landuse_mask'], z, 'cpu')
    landuse = landuse.numpy()
    landuse_uniq = np.unique(landuse[landuse != -9999]) # remove nan value data
    # normalize landuse mask
    value_to_index = {value: i for i, value in enumerate(landuse_uniq)}
    for value in landuse_uniq:
        landuse[landuse==value] = value_to_index[value.item()]
    landuse[landuse==-9999] = 0

    landuse = torch.tensor(landuse, device=device)
    return landuse, landuse_uniq

def set_rain_station_mask(rain, z, end_time, device):
    rain_mask = _set_grid_data(rain['rain_mask'], z, device)
    rain_source = _set_time_series(rain['rain_source'], end_time)
    rain_source[:,1:] = rain_source[:,1:] / 1000./ 3600.
    return rain_mask, rain_source
 
# land use based data       
def set_manning(manning, landuse_uniq):
    manning = _set_landuse_based_data(manning['manning'], landuse_uniq)
    return manning

def set_infiltration(infiltration, landuse_uniq):
    hydraulic_conductivity = _set_landuse_based_data(infiltration['hydraulic_conductivity'], landuse_uniq)
    capillary_head = _set_landuse_based_data(infiltration['capillary_head'], landuse_uniq)
    water_content_diff = _set_landuse_based_data(infiltration['water_content_diff'], landuse_uniq)
    return hydraulic_conductivity, capillary_head, water_content_diff

def set_infiltration_by_soil(soil, landuse_uniq):
    try:
        hydraulic_conductivity, capillary_head, water_content_diff = _select_parameters_from_soil(soil['soil_type'])
    except ValueError as e:
        print(e)
    
    hydraulic_conductivity = _set_landuse_based_data(hydraulic_conductivity, landuse_uniq)
    capillary_head = _set_landuse_based_data(capillary_head, landuse_uniq)
    water_content_diff = _set_landuse_based_data(water_content_diff, landuse_uniq)
    return hydraulic_conductivity, capillary_head, water_content_diff
    
def _select_parameters_from_soil(soil_types):
    soil_type = soil_types['special_soil_type']
    land_value = soil_types['special_land_type_value']
    default_type = soil_types['default_soil_type']
    
    # soil parameter table
    # Suction (mm) -> capillary_head
    # Hydraulic Conductivity (mm/hr)
    # Porosity (Fraction) -> water_content_diff = saturated Soil Moisture Content (θs) - Initial Soil Moisture Content (θi) 
    soil_parameters = pd.DataFrame({
        'USDA Soil Type': [
            'Clay', 'Silty Clay', 'Sandy Clay', 'Clay Loam', 'Silty Clay Loam', 'Sandy Clay Loam',
            'Silt Loam', 'Loam', 'Sandy Loam', 'Loamy Sand', 'Sand', 'Impervious Surface', 'Water'
        ],
        'capillary_head': [
            316.3, 292.2, 239, 208.8, 273, 218.5, 166.8, 88.9, 110.1, 61.3, 49.5, 0.0, 0.0
        ],
        'hydraulic_conductivity': [
            0.3, 0.5, 0.6, 1, 1, 1.5, 3.4, 7.6, 10.9, 29.9, 117.8, 0.0, 0.0
        ],
        'water_content_diff': [
            0.385, 0.423, 0.321, 0.309, 0.432, 0.33, 0.486, 0.434, 0.412, 0.401, 0.417, 0.0, 0.0
        ]
    })
    # end of table

    default_para_df = soil_parameters[soil_parameters['USDA Soil Type'] == default_type].iloc[0]

    if land_value is None:
        hydraulic_conductivity = default_para_df['hydraulic_conductivity'] / 1000./ 3600.
        capillary_head = default_para_df['capillary_head'] / 1000. 
        water_content_diff = default_para_df['water_content_diff']
    else:
        # check if the input soil type is correct
        valid_soil_types = soil_parameters['USDA Soil Type'].values
        missing_soil_types = [st for st in soil_type if st not in valid_soil_types]
        if default_type not in valid_soil_types:
            missing_soil_types.append(default_type)     
        if missing_soil_types:
            raise ValueError(
                f"Error: The following soil types are not in the soil parameter table: {', '.join(missing_soil_types)}.\n"
                f"Valid soil types are: {', '.join(valid_soil_types)}"
            )
        # check end
            
        soil_para_df = soil_parameters[soil_parameters['USDA Soil Type'].isin(soil_type)]
        
        hydraulic_conductivity = {
            'default_value': np.array([default_para_df['hydraulic_conductivity']]) / 1000.,
            'special_land_type_value': land_value,
            'special_param_value': np.array(soil_para_df['hydraulic_conductivity']) / 1000.}
        
        capillary_head = {
            'default_value': np.array([default_para_df['capillary_head']]) / 1000. / 3600.,
            'special_land_type_value': land_value,
            'special_param_value': np.array(soil_para_df['capillary_head']) / 1000. / 3600.}
        
        water_content_diff = {
            'default_value': np.array([default_para_df['water_content_diff']]),
            'special_land_type_value': land_value,
            'special_param_value': np.array(soil_para_df['water_content_diff'])}
        
    return hydraulic_conductivity, capillary_head, water_content_diff
    
def set_sewer_sink(sewer, landuse_uniq):
    sewer_sink = _set_landuse_based_data(sewer['sewer_sink'], landuse_uniq)
    return sewer_sink
  