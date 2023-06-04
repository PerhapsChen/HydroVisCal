import os
import json
import copy

import numpy as np
import xarray as xr
import matplotlib as mpl
import matplotlib.pyplot as plt

import cartopy.crs as ccrs
import cartopy.feature as cfeature

from HYDRO_Plot import ColorBarFromFig, genGlobalMapJson, GlobalMapPlot
    
class DeputyPlot:
    def __init__(self, fig, main_ax, jsonPath='./hydroJson/DeputyPlot.json'):
        self._main_ax = main_ax # 主图的axes引用对象
        self._fig = fig # 主图的figure引用对象
        
        self.mainPos = main_ax.get_position()
        self.mainXLen = self.mainPos.x1 - self.mainPos.x0
        self.mainYLen = self.mainPos.y1 - self.mainPos.y0
        self.mLB = (self.mainPos.x0, self.mainPos.y0)
        self.mRT = (self.mainPos.x1, self.mainPos.y1)
        self.mLT = (self.mainPos.x0, self.mainPos.y1)
        self.mRB = (self.mainPos.x1, self.mainPos.y0)

        # 如果json文件不存在，则生成默认的json文件，否则读取json文件
        if not os.path.exists(jsonPath):
            self.genDeputyPlotJson(jsonPath)
        else:
            self.jsonPath = jsonPath
            self.reloadJson()
    
    def genDeputyPlotJson(self, outputJsonPath='./hydroJson/DeputyPlot.json', returnDict=False):
        '''
        Generate json file for deputy plot
        '''
        PARAMETERS = {
            'box_lw': 0.5,
            'face_color': 'none',
            'loc': 'Left',
            'xpad': 0.05,
            'ypad': 0,
            'xlen': 0.2,
            'ylen': 1.0,
            'xstart': 0,
            'ystart': 0,
            
            'has_left': True,
            'has_right': True,
            'has_top': True,
            'has_bottom': True,
            
            'has_xtick': True,
            'has_ytick': True,
            
            'xtick_loc': 'bottom',
            'ytick_loc': 'left',
            
            'xtick_direction': 'in',
            'ytick_direction': 'in',
            
            'xtick_labelsize': 8,
            'ytick_labelsize': 8,
            
            'xtick_rotation': 0,
            'ytick_rotation': 0,
            
        } 
        # 大部分参数都是相对于主图的比例
        # 副图位置参数不可以通过regularAxes()函数调整
        
        if not os.path.exists(os.path.dirname(outputJsonPath)):
            os.mkdir(os.path.dirname(outputJsonPath))
            
        with open(outputJsonPath, "w", encoding='utf-8') as f:
            json.dump(PARAMETERS, f, indent=2)  
        
        print("Json file of parameters has written to [{}]".format(outputJsonPath))
        self.jsonPath = outputJsonPath
        self.paraDict = PARAMETERS
        if returnDict:
            return PARAMETERS 
        
    def reloadJson(self):
        with open(self.jsonPath) as f:
            self.paraDict = json.load(f)  
    
    def genDefaultJson(self):
        """
        go back to default json
        """
        genGlobalMapJson(self.jsonPath)
        
    def saveCurrentJson(self, outputJsonPath='./hydroJson/currentFromGlobalMap.json'):
        if not os.path.exists(os.path.dirname(outputJsonPath)):
            os.mkdir(os.path.dirname(outputJsonPath))
            
        with open(outputJsonPath, "w", encoding='utf-8') as f:
            json.dump(self.paraDict, f, indent=2)  
        
        print("Current parameters has written to [{}]".format(outputJsonPath)) 
        
    
    def genAxes(self):
        '''
        Generate axes for deputy plot
        '''
        self.reloadJson()
        self.fig = copy.deepcopy(self._fig) # 主图的figure对象
        P = self.paraDict
        loc = P['loc']
        mXL = self.mainXLen
        mYL = self.mainYLen 
        # 副图在主图左边，间隔pad, 宽度为xlen, 高度为ylen，起始位置为ystart（通常为0）
        if loc == 'Left': 
            self.ax = self.fig.add_axes([self.mLB[0] - P['xpad']*mXL - P['xlen']*mXL,
                                         self.mLB[1] + P['ystart']*mYL, 
                                         mXL * P['xlen'], 
                                         mYL * P['ylen']])
        elif loc == 'Right':
            self.ax = self.fig.add_axes([self.mRT[0] + P['xpad']*mXL, 
                                         self.mLB[1] + P['ystart']*mYL, 
                                         mXL * P['xlen'], 
                                         mYL * P['ylen']])
        elif loc == 'Top':
            self.ax = self.fig.add_axes([self.mLB[0] + P['xstart']*mXL, 
                                         self.mLT[1] + P['ypad']*mYL, 
                                         mXL * P['xlen'], 
                                         mYL * P['ylen']])
        elif loc == 'Bottom':
            self.ax = self.fig.add_axes([self.mLB[0] + P['xstart']*mXL, 
                                         self.mLB[1] - P['ypad']*mYL - P['ylen']*mYL, 
                                         mXL * P['xlen'], 
                                         mYL * P['ylen']])
        else:
            print("Wrong loc parameter, please check")
    
    def regularAxes(self):
        '''
        Regular axes for deputy plot
        '''
        self.reloadJson()
        P = self.paraDict
        self.ax.spines['top'].set_visible(P['has_top'])
        self.ax.spines['bottom'].set_visible(P['has_bottom'])
        self.ax.spines['left'].set_visible(P['has_left'])
        self.ax.spines['right'].set_visible(P['has_right'])
        
        self.ax.tick_params(axis='x', which='both', direction=P['xtick_direction'], 
                            labelsize=P['xtick_labelsize'], rotation=P['xtick_rotation'])
        self.ax.tick_params(axis='y', which='both', direction=P['ytick_direction'], 
                            labelsize=P['ytick_labelsize'], rotation=P['ytick_rotation'])
        
        self.ax.xaxis.set_ticks_position(P['xtick_loc'])
        self.ax.yaxis.set_ticks_position(P['ytick_loc'])
        
        self.ax.set_facecolor(P['face_color'])
        self.ax.spines['top'].set_linewidth(P['box_lw'])
        self.ax.spines['bottom'].set_linewidth(P['box_lw'])
        self.ax.spines['left'].set_linewidth(P['box_lw'])
        self.ax.spines['right'].set_linewidth(P['box_lw'])
        
        if not P['has_xtick']:
            self.ax.set_xticks([])
        if not P['has_ytick']:
            self.ax.set_yticks([])
    
    def get_fig(self):

        return self.fig
    
    def get_ax(self):
            
        return self.ax
                
        
        