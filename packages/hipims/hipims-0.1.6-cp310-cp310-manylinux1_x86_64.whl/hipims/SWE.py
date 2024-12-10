# encoding: utf-8
# # High-Performance Integrated hydrodynamic Modelling System ***hybrid***
# @author: Jiaheng Zhao, Xue Tong
# @license: (C) Copyright 2020-2025. 2025~ Apache Licence 2.0
# @contact: x.tong2@lboro.ac.uk
# @software: hipims_hybrid
# @time: 21.07.2024
# This is an open source code used for high-performance flooding simulation.
# Feel free to use and extend.

"""
@author: Jiaheng Zhao, Xue Tong
@license: (C) Copyright 2020-2025. 2025~ Apache Licence 2.0
@contact: j.zhao@lboro.ac.uk, x.tong2@lboro.ac.uk
@software: hipims_torch
@file: swe.py
@time: 21.07.2024
@desc:
"""

import sys
import os
from numpy.lib.scimath import sqrt
import rasterio as rio
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import sys
import time
import math

from hipims import timeControl
from hipims import infiltration_sewer
from hipims import stationPrecipitation
from hipims import frictionImplicit_andUpdate
from hipims import fluxMask
from hipims import fluxCal_1stOrder
from hipims import fluxCal_2ndOrder

class Godunov:
    # ===================================================================
    #                       Initializing Funcs
    # ===================================================================
    def __init__(self, case_info, model_params, dx, export_n, device):
        super().__init__()

         # default parameters.
        self._tensorType = torch.float64  
        self.dt = torch.tensor(1.0e-6, dtype=self._tensorType, device=device)
        self._maxTimeStep = torch.tensor([60.], dtype=self._tensorType, device=device)
        self._rainfall_station_time_index = 0

        # model parameters. Can be revised by users.
        self.t = torch.tensor([model_params['start_time']], dtype=self._tensorType, device=device)
        self._secondOrder = model_params['second_order']
        self.cfl = torch.tensor(1.0 if self._secondOrder else 0.5, dtype=self._tensorType, device=device)
        self.dx = torch.tensor([dx], dtype=self._tensorType, device=device)
        self.export_timeStep = model_params['output_interval']
        self._export_n = export_n
        
        self._outpath = case_info['output_folder']

        # archive dt and t for debuging
        self.dt_list = []
        self.t_list = []
        
        
    def init__gauges_tensor(self, gauge_index):
        self._gauge_index = torch. as_tensor(gauge_index)
        self._write_gauges = len(gauge_index) > 0
        
        # gauges archive list
        self._t_gauges = []
        self._h_gauges = []
        self._qx_gauges = []
        self._qy_gauges = []
        
        self._gauge_output_time = 0
                 
    def init__fluidField_tensor(self, mask, z, h0, hU0x, hU0y, device):
        valid_mask = mask > 0
        
        # initial condition
        self._z_internal = torch.as_tensor(z[valid_mask].type(self._tensorType),
                                           device=device)
                                           
        self._h_internal = torch.as_tensor(h0[valid_mask].type(self._tensorType),
                                           device=device)
        
        self._qx_internal = torch.as_tensor(hU0x[valid_mask].type(self._tensorType),
                                            device=device)
        self._qy_internal = torch.as_tensor(hU0y[valid_mask].type(self._tensorType),
                                            device=device)
        
        # Assign initial water depth to dry grid cells that have inflows
        def starts_with_678(nums): # detect if numbers start with 7
            # Calculate the log base 10 and use torch.div for truncating to the nearest lower integer
            log_vals = torch.div(nums.float().log10(), 1, rounding_mode='trunc')
            divisor = 10 ** log_vals.int()
            divisor[nums == 0] = 1  # Avoid log10 of 0 by setting the divisor for 0 values to 1
            first_digits = torch.div(nums, divisor, rounding_mode='trunc')  # Find the most significant digit
            return torch.isin(first_digits, torch.tensor([6, 7, 8], device=device))
        
        mask_wet = starts_with_678(mask[valid_mask])
        self._h_internal = torch.where(mask_wet & (self._h_internal == 0), torch.full_like(self._h_internal, 0.001), self._h_internal)

        # init internal variables
        self._h_max = torch.as_tensor(h0[valid_mask].type(self._tensorType),
                                      device=device)

        self._h_update = torch.zeros_like(self._h_internal,
                                          dtype=self._tensorType,
                                          device=device)
        self._qx_update = torch.zeros_like(self._qx_internal,
                                           dtype=self._tensorType,
                                           device=device)
        self._qy_update = torch.zeros_like(self._qy_internal,
                                           dtype=self._tensorType,
                                           device=device)
        self._z_update = torch.zeros_like(self._z_internal,
                                          dtype=self._tensorType,
                                          device=device)
        self._wetMask = torch.flatten(
            (self._h_internal > 1.0e-6).nonzero()).type(torch.int32)

        del h0, hU0x, hU0y, z
        torch.cuda.empty_cache()
        
        # generate index mask
        """
        The direction of matrix
                                     [1,1] |1-1|+1 = 1
                                     |
                                     |
        |-1-1|+0 = 2 [-1, 0] <------ c ------->[1, 0] |1-1|+0 = 0
                                     |
                                     |
                                     [-1,1] |-1-1|+1 = 3

        index of direction = |dimension[0]-1|+dimension[1]

        Returns:
            [type] -- [description]
        """
        # add a border to current mask to avoid no -9999 exists in DEM
        mask = torch.nn.functional.pad(mask, (1, 1, 1, 1), 'constant', -1)
        # end of adding border

        index_mask = torch.zeros_like(mask, dtype=torch.int32,
                                      device=device) - 1 # now index are all -1
        
        index_mask[mask > 0] = torch.tensor(
            [i for i in range((mask[mask > 0]).size()[0])],
            dtype=torch.int32,
            device=device,
        )
        # 从 index_mask 中获取对应的索引
        oppo_direction = torch.tensor([[-1, 1], [1, 0], [1, 1], [-1, 0]],
                                      device=device)
        self._normal = torch.tensor(
            [[1.0, 0.0], [0.0, 1.0], [-1.0, 0.0], [0.0, -1.0]],
            dtype=self._tensorType,
            device=device)

        self._index = torch.zeros(size=(5, self._h_internal.shape[0]),
                                  dtype=torch.int32,
                                  device=device)
        self._index[0] = mask[mask > 0]
        for i in range(4):
            self._index[i + 1] = (index_mask.roll(
                oppo_direction[i][0].item(),
                oppo_direction[i][1].item()))[mask > 0]

        self._index = torch.flatten(self._index)

        del index_mask, oppo_direction, mask
        torch.cuda.empty_cache()

    
    
    def init__grid_tensor(self, landuseMask, rainfall_station_Mask, mask, device):
        self._landuseMask = torch.as_tensor(landuseMask[mask > 0],
                                             dtype=torch.uint8,
                                             device=device)
        self._rainfall_station_Mask = torch.as_tensor(rainfall_station_Mask[mask > 0], 
                                             dtype=torch.int16, device=device)
    
    def init__time_series_tensor(self, given_h, given_Q, given_wl, rainfallMatrix, device):
        self._given_depth = torch.as_tensor(given_h,
                                         dtype=self._tensorType,
                                         device=device)
        self._given_discharge = torch.as_tensor(given_Q,
                                             dtype=self._tensorType,
                                             device=device)
        self._given_wl = torch.as_tensor(given_wl,
                                         dtype=self._tensorType,
                                         device=device)
        self._rainfallMatrix = torch.as_tensor(rainfallMatrix,
                                         dtype=self._tensorType,
                                         device=device)
    
    def init__parameters_tensor(self, 
                                manning, 
                                hydraulic_conductivity,
                                capillary_head, 
                                water_content_diff, 
                                sewer_sink,
                                device):   
        # friction parameters
        self._manning = torch.as_tensor(manning,
                                     dtype=self._tensorType,
                                     device=device)
        # infiltration parameters
        self._cumulativeWaterDepth = torch.zeros_like(self._h_internal,
                                                      device=device)
        self._hydraulic_conductivity = torch.as_tensor(hydraulic_conductivity,
                                     dtype=self._tensorType,
                                     device=device)
        self._capillary_head = torch.as_tensor(capillary_head,
                                     dtype=self._tensorType,
                                     device=device)
        self._water_content_diff = torch.as_tensor(water_content_diff,
                                     dtype=self._tensorType,
                                     device=device)

        # sewer sink
        self._sewer_sink = torch.as_tensor(sewer_sink,
                                     dtype=self._tensorType,
                                     device=device)
     
    # =================== End of Initializing Funcs =====================
    
       
    # ===================================================================
    #                       Godunov Funcs
    # ===================================================================  
    
    def add__flux(self):  
        self._wetMask = torch.zeros_like(self._h_internal, dtype=torch.bool)
        fluxMask.update(self._wetMask, self._h_internal, self._index, self.t)
        self._wetMask = torch.flatten(self._wetMask.nonzero().type(torch.int32))  

        if self._secondOrder:                  
            fluxCal_2ndOrder.addFlux(
                self._wetMask,
                self._h_update,
                self._qx_update,
                self._qy_update,
                self._h_internal,
                self._z_internal,
                self._qx_internal,
                self._qy_internal,
                self._index,
                self._normal,
                self._given_depth,
                self._given_wl,
                self._given_discharge,
                self.dx,
                self.t,
                self.dt,
            )
        else:   
            # print('add flux\n')
            fluxCal_1stOrder.addFlux(                
                    self._wetMask,
                    self._h_update,
                    self._qx_update,
                    self._qy_update,
                    self._h_internal,
                    self._z_internal,
                    self._qx_internal,
                    self._qy_internal,
                    self._index,
                    self._normal,
                    self._given_depth,
                    self._given_wl,
                    self._given_discharge,
                    self.dx,
                    self.t,
                    self.dt,
                )

        torch.cuda.empty_cache()
    
    def __interpolate_rainfall(self, rainfall_ndarray_data, device):
        if self.t.item() < rainfall_ndarray_data[-1, 0]:
            if self.t.item() < rainfall_ndarray_data[
                    self._rainfall_station_time_index + 1, 0]:
                per = (
                    self.t.item() -
                    rainfall_ndarray_data[self._rainfall_station_time_index, 0]
                ) / (rainfall_ndarray_data[self._rainfall_station_time_index +
                                           1, 0] -
                     rainfall_ndarray_data[self._rainfall_station_time_index,
                                           0])
                self._rainStationData = torch.from_numpy(
                    rainfall_ndarray_data[self._rainfall_station_time_index,
                                          1:] + per *
                    (rainfall_ndarray_data[self._rainfall_station_time_index +
                                           1, 1:] -
                     rainfall_ndarray_data[self._rainfall_station_time_index,
                                           1:])).to(device=device)
            else:
                self._rainfall_station_time_index += 1
                self.__interpolate_rainfall(rainfall_ndarray_data,
                                                    device)
        else:
            self._rainStationData -= self._rainStationData
    
    def add__precipitation_source(self, rainfall_ndarray_data, device):
        self.__interpolate_rainfall(rainfall_ndarray_data, device)
        
        stationPrecipitation.addStation_Precipitation(
            self._h_update, self._rainfall_station_Mask, self._rainStationData,
            self.dt)
        
    def add__infiltration_and_sewer_source(self):
        infiltration_sewer.addInfiltrationAndSewer(
            self._wetMask, self._h_update, self._landuseMask, self._h_internal,
            self._hydraulic_conductivity, self._capillary_head,
            self._water_content_diff, self._cumulativeWaterDepth, 
            self._sewer_sink, self.dt)

    def add__friction_source(self):
        self._wetMask = torch.flatten(
            ((self._h_update.abs() > 0.0) +
             (self._h_internal >= 0.0)).nonzero()).type(torch.int32)
        
        frictionImplicit_andUpdate.addFriction_eulerUpdate(
            self._wetMask, self._h_update, self._qx_update, self._qy_update,
            self._z_update, self._landuseMask, self._h_internal,
            self._qx_internal, self._qy_internal,
            self._z_internal, self._manning, self.dt)

    def update__time(self, device):
        # reset dh, dqx, dqy, dz after all flux and sources updated
        self._h_update[:] = 0.
        self._qx_update[:] = 0.
        self._qy_update[:] = 0.
        self._z_update[:] = 0. 

        # update dt (2 parts)
        # part 1: control dt by CFL
        self._accelerator_dt = torch.full(self._wetMask.size(),
                                          self._maxTimeStep.item(),
                                          dtype=self._tensorType,
                                          device=device)
        timeControl.updateTimestep(
            self._wetMask,
            self._accelerator_dt,
            self._h_max,
            self._h_internal,
            self._qx_internal,
            self._qy_internal,
            self.dx,
            self.cfl,
            self.t,
            self.dt,
        )

        if self._accelerator_dt.size(0) != 0:
            self.dt = torch.min(self._accelerator_dt)
        else:
            # do nothing, keep the last time step
            pass
        
        # limit the time step not bigger than the five times of the older time step
        UPPER = 10.
        time_upper = self.dt * UPPER     
        self.dt = min(self.dt, time_upper)
        
        # part2: control dt by output interval, and export flow field if needed
        if (self.dt + self.t).item() >= float(self._export_n +
                                              1) * self.export_timeStep:
            self.dt = (self._export_n + 1) * self.export_timeStep - self.t
            self.__exportField()
            self._export_n += 1
            print("Saving outputs ...")
        self.t += self.dt
    
    # =================== End of Godunov Funcs =====================
    
    
    
    # ===================================================================
    #                     Archive/Export data Funcs
    # ===================================================================  
    def __exportField(self):
        # save the data to pt files 
        # the .pt file will be processed by numpy later at the postprocessing

        torch.save(
            self._h_internal,
            self._outpath + "/h_" + str(self.t + self.dt) + ".pt",
        )
        torch.save(
            self._qx_internal,
            self._outpath + "/qx_" + str(self.t + self.dt) + ".pt",
        )
        torch.save(
            self._qy_internal,
            self._outpath + "/qy_" + str(self.t + self.dt) + ".pt",
        )
        torch.save(
            self._h_max,
            self._outpath + "/h_max_" + str(self.t + self.dt) + ".pt",
        )

    def update__observe_gauges(self):
        if self._write_gauges:
            if self.t.item() - self._gauge_output_time > 10.0: 
                self._t_gauges.append(self.t.item())
                self._h_gauges.append(self._h_internal[self._gauge_index].cpu().numpy())
                self._qx_gauges.append(self._qx_internal[self._gauge_index].cpu().numpy())
                self._qy_gauges.append(self._qy_internal[self._gauge_index].cpu().numpy())
            
                self._gauge_output_time = self.t.item()
    
    def write__observe_gauges_and_time(self):
        self.__write_data(self._t_gauges, self._h_gauges, '/gauges_h.txt')
        self.__write_data(self._t_gauges, self._qx_gauges, '/gauges_qx.txt')
        self.__write_data(self._t_gauges, self._qy_gauges, '/gauges_qy.txt')
        self.__write_data(self.dt_list, self.t_list, '/t.txt')
    
    def __write_data(self, list1, list2, file_name):
        array1 = np.array(list1)
        array2 = np.array(list2) 
        T = np.column_stack((array1, array2))
        np.savetxt(self._outpath + file_name, T)