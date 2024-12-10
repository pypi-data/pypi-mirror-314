import os
import numpy as np
from datetime import datetime

class InputHipims:
    """ Summary information of a flood case
        Attributes:
            grid_attr:
            model_attr:
            boundary_attr:
            rain_attr:
            params_attr:
            initial_attr:
            
    """
    # default parameters
    case_info = {'case_folder': None, # string'
                 'input_folder': 'input',
                 'output_folder': 'output',
                 'DEM_path': None}
    
    model_params = {'num_GPU':1,
                    'start_time':0,
                    'GPU_device_ID':0,
                    'end_time':3600,
                    'output_interval':600,
                    'num_gauges': 0,
                    'second_order': False,
                    'projected_coordinate': False} 
    
    rainfall = {'rain_mask': 0,
            'rain_source': 0}
    
    initial_condition = {'h0':0, 
                         'hU0x':0, 
                         'hU0y':0}                        
    
    boundary = {'num_boundary':0,
                'bound_list': None,
                'outline_boundary':'FALL'}
    
    landuse = {'landuse_mask': 0}
    
    manning = {'manning':0} 
    
    infiltration = {'cumulative_depth':0, 
                    'hydraulic_conductivity':0,
                    'capillary_head':0, 
                    'water_content_diff':0}
    soil = {'soil_type': 0}
    
    sewer = {'sewer_sink': 0}
    
    gauges = {'num_gauge': 0,
                  'position': np.array([[]])}
     
    def __init__(self, 
                 case_folder,
                 dem_path,
                 output_folder,
                 rainfall_source):
        
        self._case_folder = os.path.join(os.environ['HOME'], case_folder)
        self._case_folder_input = os.path.join(self._case_folder,'input')

        self.case_info['case_folder'] = self._case_folder
        self.case_info['input_folder'] = self._case_folder_input
        self.case_info['output_folder'] = os.path.join(self._case_folder,output_folder)
        self.case_info['DEM_path'] = os.path.join(self._case_folder_input, dem_path)
        
        self.rainfall['rain_source'] = rainfall_source
        self._soil = False
        # self.num_of_sections = num_of_sections
        # self.device_no = device_no
    
    def set_model_parameters(self, 
                             device_id = 0,
                             start_time = 0,
                             end_time = 3600,
                             second_order = False,
                             output_interval = 600,
                             projected_coordinate = False):
        
        self.model_params['GPU_device_ID'] = device_id
        self.model_params['start_time'] = start_time
        self.model_params['end_time'] = end_time
        self.model_params['second_order'] = second_order
        self.model_params['output_interval'] = output_interval
        self.model_params['projected_coordinate'] = projected_coordinate
    
    def set_output_path(self, output_path):
        os.path.join(self._case_folder, output_path)
        
    def _get_path_or_value(self, param):
        if isinstance(param, str):
            full_path = os.path.join(self._case_folder_input, param)
            if not os.path.exists(full_path):
                raise FileNotFoundError(f"The file {full_path} does not exist.")
            return full_path
        else:
            return param
    
    def set_rainfall(self, rain_mask=0, rain_source=0.0):       
        self.rainfall['rain_mask'] = self._get_path_or_value(rain_mask)
        self.rainfall['rain_source'] = self._get_path_or_value(rain_source)
    
    def set_initial_condition(self, 
                              h0=0.0,
                              hU0x=0.0,
                              hU0y=0.0):
        self.initial_condition['h0'] = self._get_path_or_value(h0)
        self.initial_condition['hU0x'] = self._get_path_or_value(hU0x)
        self.initial_condition['hU0y'] = self._get_path_or_value(hU0y)
    
    def set_gauges_position(self, position=np.array([])):
        self.gauges['position'] = self._get_path_or_value(position)
    
    def set_boundary_condition(self, bound_list = None,
                                outline_boundary = 'OPEN'):
        self.boundary['num_boundary'] = len(bound_list)
        for bound in bound_list:
            if isinstance(bound['source'], list): 
                bound['source'][0] = self._get_path_or_value(bound['source'][0])
            elif isinstance(bound['source'], str): 
                bound['source'] = self._get_path_or_value(bound['source'])

        self.boundary['bound_list'] = bound_list
        self.boundary['outline_boundary']  = outline_boundary

    def set_landuse(self, landuse_mask=0):
        self.landuse['landuse_mask'] = self._get_path_or_value(landuse_mask)
            
    def set_manning(self, manning=0.035):
        # 1 耕地；0.035
        # 2 林地；0.1
        # 3 草地；0.035
        # 4 水域； 0.04
        # 5 建设用地；0.15
        # 6 未利用地 0.03
        self.manning['manning'] = manning
    
    
    def set_infiltration(self,
                        cumulative_depth = 0.0,
                        hydraulic_conductivity = 0.0,
                        capillary_head = 0.0,
                        water_content_diff = 0.0):
        self.infiltration['cumulative_depth'] = cumulative_depth
        self.infiltration['hydraulic_conductivity'] = hydraulic_conductivity
        self.infiltration['capillary_head'] = capillary_head
        self.infiltration['water_content_diff'] = water_content_diff 
    
    def set_soil_type(self, soil_type):
        self._soil = True
        self.soil['soil_type'] = soil_type
        
    def set_sewer_sink(self, sewer_rate=0.0):
        self.sewer['sewer_sink'] = sewer_rate
    
    ## info of simulation case      
    def __str__(self):
        """
        To show object summary information when it is called in console
        """
        self.display_info()
        time_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return  self.__class__.__name__+' object created on '+ time_str
    
    def display_info(self):
        def print_dict(one_dict):
            for key, value in one_dict.items():
                if isinstance(value, (list, tuple)):
                    print(f"{key}: ", end="\n")
                    print(*value, sep="\n")
                else:
                    print(f"{key}: {value}")
                    
        def display_module(module_name, model_attr, module_fuction, http_path):
            """ display summary information
            """  
            print(f'---------------------- {module_name} ---------------------')
            print(f"* To change paramaeters, use the '{module_fuction}' function. For details, visit {http_path}")
            print_dict(model_attr)
            print('\n')

        display_module('Case Information', self.case_info, 'set_case_info', 'http_path')        
        display_module('Model Parameters', self.model_params, 'set_model_parameters', 'http_path')
        display_module('Initial Condition', self.initial_condition, 'set_initial_condition', 'http_path')
        display_module('Boundary Condition', self.boundary, 'set_boundary_condition', 'http_path')
        display_module('Rainfall', self.rainfall, 'set_rainfall', 'http_path')
        
        display_module('Land Use', self.landuse, 'set_landuse', 'http_path')
        display_module('Friction Parameter', self.manning, 'set_manning', 'http_path')
        display_module('Sewer Sink', self.sewer, 'set_sewer_sink', 'http_path')
        
        if self._soil:
            display_module('Set infiltration parameters by soil type', self.soil, 'set_soil_type', 'http_path')
            # print("* To customize parameters, use the 'set_infiltration' function")
        else:
            display_module('Infiltration parameters', self.infiltration, 'set_inflitration', 'http_path')
            # print("* To set paramaeters by soil, use the 'set_soil_type' function")