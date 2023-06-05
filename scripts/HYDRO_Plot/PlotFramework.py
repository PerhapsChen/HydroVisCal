import os
import json
import copy

import numpy as np
import xarray as xr
import matplotlib as mpl
import matplotlib.pyplot as plt

import cartopy.crs as ccrs
import cartopy.feature as cfeature

class PlotFramework:
    def __init__(self, isGeo=False, proj=ccrs.PlateCarree()):
        '''
        isGeo: 主图是否为地理坐标系
        proj: 地图投影方式
        '''
        self.fig = plt.figure(dpi=100, figsize=(8, 4))
        self.axs = []
        if isGeo:
            self.main_ax = self.fig.add_axes([0,0,1,1], projection=proj)
        else:
            #self.main_ax = self.fig.add_axes([0, 0, 1, 1])
            self.main_ax = self.fig.add_axes([0,0,1,1])
        self.axs.append(self.main_ax)
        self.proj = proj

    def updateMainAxesInfo(self):
        '''
        更新 main axes 信息
        '''
        self.mainPos = self.main_ax.get_position(True)
        self.mainXLen = self.mainPos.x1 - self.mainPos.x0
        self.mainYLen = self.mainPos.y1 - self.mainPos.y0
        self.mLB = (self.mainPos.x0, self.mainPos.y0)
        self.mRT = (self.mainPos.x1, self.mainPos.y1)
        self.mLT = (self.mainPos.x0, self.mainPos.y1)
        self.mRB = (self.mainPos.x1, self.mainPos.y0)
        self.mXL = self.mainXLen
        self.mYL = self.mainYLen 
        
    def changeMainAxes(self, ax):
        '''
        改变 main axes
        '''
        self.main_ax = ax
        self.updateMainAxesInfo()
        
        
    def addDeputyPlot(self, loc, pad, xlen, ylen, start):
        
        self.updateMainAxesInfo()

        # 副图在主图左边，间隔pad, 宽度为xlen, 高度为ylen，起始位置为ystart（通常为0）
        if loc == 'Left': 
            self.axs.append(self.fig.add_axes([self.mLB[0] - pad*self.mXL - xlen*self.mXL,
                                         self.mLB[1] + start*self.mYL, 
                                         self.mXL * xlen, 
                                         self.mYL * ylen]))
        # 副图在主图右边，间隔pad, 宽度为xlen, 高度为ylen，起始位置为ystart（通常为0）
        elif loc == 'Right':
            self.axs.append(self.fig.add_axes([self.mRT[0] + pad*self.mXL, 
                                         self.mLB[1] + start*self.mYL, 
                                         self.mXL * xlen, 
                                         self.mYL * ylen]))
        # 副图在主图上边，间隔pad, 宽度为xlen, 高度为ylen，起始位置为xstart（通常为0）
        elif loc == 'Top':
            self.axs.append(self.fig.add_axes([self.mLB[0] + start*self.mXL, 
                                         self.mLT[1] + pad*self.mYL, 
                                         self.mXL * xlen, 
                                         self.mYL * ylen]))
        # 副图在主图下边，间隔pad, 宽度为xlen, 高度为ylen，起始位置为xstart（通常为0）
        elif loc == 'Bottom':
            self.axs.append(self.fig.add_axes([self.mLB[0] + start*self.mXL, 
                                         self.mLB[1] - pad*self.mYL - ylen*self.mYL, 
                                         self.mXL * xlen, 
                                         self.mYL * ylen]))
        # 副图在主图内部，起始位置为xstart, ystart, 宽度为xlen, 高度为ylen
        elif loc == 'inside':
            self.axs.append(self.fig.add_axes([self.mLB[0] + start[0]*self.mXL, 
                                         self.mLB[1] + start[1]*self.mYL, 
                                         self.mXL * xlen, 
                                         self.mYL * ylen]))
        else:
            print("Wrong loc parameter, please check")


##! example
# from HYDRO_Plot import PlotFramework

# pf = PlotFramework(isGeo=True)
# pf.addDeputyPlot(loc='Left',pad=0.03, xlen=0.2,ylen=1.0,start=0)
# pf.axs[1].plot([1,2,3],[1,2,3])
# pf.addDeputyPlot(loc='Right',pad=0.03, xlen=0.2,ylen=1.0,start=0)
# pf.axs[2].plot([1,2,3],[1,2,3])
# pf.addDeputyPlot(loc='Top',pad=0.05, xlen=1, ylen=0.2,start=0)
# pf.axs[3].plot([1,2,3],[1,2,3])
# pf.addDeputyPlot(loc='Bottom',pad=0.05, xlen=1, ylen=0.2,start=0)
# pf.axs[4].plot([1,2,3],[1,2,3])
# pf.changeMainAxes(fw.axs[4])
# pf.addDeputyPlot(loc='Right', pad=0.03, xlen=0.2, ylen=1.0,start=0)
# pf.axs[5].scatter([1,2,3],[1,2,3])