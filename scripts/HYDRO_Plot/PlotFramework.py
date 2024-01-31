import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from HYDRO_Plot.GeoAxesPlot import genGeoAxesJson, GeoAxesPlot

class PlotFramework:
    def __init__(self,dpi=200):
        self.fig = plt.figure(dpi=dpi)
        self.axs = []

    def addMainAxes(self, isGeo=False, proj=ccrs.PlateCarree(), **kwargs):
        '''
        isGeo: 主图是否为地理坐标系
        proj: 地图投影方式
        '''
        if isGeo:
            self.main_ax = self.fig.add_axes([0,0,1,1], projection=proj, **kwargs)
            self.main_ax.set_extent([-180,180,90,-90])

        else:
            self.main_ax = self.fig.add_axes([0,0,1,1], **kwargs)
        self.axs.append(self.main_ax)
        self.proj = proj
        self.updateMainAxesInfo()
        
        return self.main_ax
    
    def updateMainAxesInfo(self, ax=None):
        '''
        更新 main axes 信息
        '''
        if ax != None:
            self.main_ax = ax
        self.mainPos = self.main_ax.get_position()
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
        更改主图
        '''
        self.main_ax = ax
        self.updateMainAxesInfo()
    
    def addDeputyPlot(self, loc, pad, xlen, ylen, start, project=None):
        self.updateMainAxesInfo()
        # 副图在主图左边，间隔pad, 宽度为xlen, 高度为ylen，起始位置为ystart（通常为0）
        if loc == 'Left': 
            self.axs.append(self.fig.add_axes([self.mLB[0] - pad*self.mXL - xlen*self.mXL,
                                         self.mLB[1] + start*self.mYL, 
                                         self.mXL * xlen, 
                                         self.mYL * ylen], projection=project))
        # 副图在主图右边，间隔pad, 宽度为xlen, 高度为ylen，起始位置为ystart（通常为0）
        elif loc == 'Right':
            self.axs.append(self.fig.add_axes([self.mRT[0] + pad*self.mXL, 
                                         self.mLB[1] + start*self.mYL, 
                                         self.mXL * xlen, 
                                         self.mYL * ylen], projection=project))
        # 副图在主图上边，间隔pad, 宽度为xlen, 高度为ylen，起始位置为xstart（通常为0）
        elif loc == 'Top':
            self.axs.append(self.fig.add_axes([self.mLB[0] + start*self.mXL, 
                                         self.mLT[1] + pad*self.mYL, 
                                         self.mXL * xlen, 
                                         self.mYL * ylen], projection=project))
        # 副图在主图下边，间隔pad, 宽度为xlen, 高度为ylen，起始位置为xstart（通常为0）
        elif loc == 'Bottom':
            self.axs.append(self.fig.add_axes([self.mLB[0] + start*self.mXL, 
                                         self.mLB[1] - pad*self.mYL - ylen*self.mYL, 
                                         self.mXL * xlen, 
                                         self.mYL * ylen], projection=project))
        # 副图在主图内部，起始位置为xstart, ystart, 宽度为xlen, 高度为ylen
        elif loc == 'Inside':
            self.axs.append(self.fig.add_axes([self.mLB[0] + start[0]*self.mXL, 
                                         self.mLB[1] + start[1]*self.mYL, 
                                         self.mXL * xlen, 
                                         self.mYL * ylen], projection=project))
        else:
            print("Wrong loc parameter, please check")
        
        return self.axs[-1]
    
    def addDeputyPlot_Geo(self, loc, pad, xlen, ylen, start):
        self.updateMainAxesInfo()
        # 副图在主图左边，间隔pad, 宽度为xlen, 高度为ylen，起始位置为ystart（通常为0）
        if loc == 'Left': 
            self.axs.append(self.fig.add_axes([self.mLB[0] - pad*self.mXL - xlen*self.mXL,
                                         self.mLB[1] + start*self.mYL, 
                                         self.mXL * xlen, 
                                         self.mYL * ylen], projection=self.proj))
        # 副图在主图右边，间隔pad, 宽度为xlen, 高度为ylen，起始位置为ystart（通常为0）
        elif loc == 'Right':
            self.axs.append(self.fig.add_axes([self.mRT[0] + pad*self.mXL, 
                                         self.mLB[1] + start*self.mYL, 
                                         self.mXL * xlen, 
                                         self.mYL * ylen], projection=self.proj))
        # 副图在主图上边，间隔pad, 宽度为xlen, 高度为ylen，起始位置为xstart（通常为0）
        elif loc == 'Top':
            self.axs.append(self.fig.add_axes([self.mLB[0] + start*self.mXL, 
                                         self.mLT[1] + pad*self.mYL, 
                                         self.mXL * xlen, 
                                         self.mYL * ylen], projection=self.proj))
        # 副图在主图下边，间隔pad, 宽度为xlen, 高度为ylen，起始位置为xstart（通常为0）
        elif loc == 'Bottom':
            self.axs.append(self.fig.add_axes([self.mLB[0] + start*self.mXL, 
                                         self.mLB[1] - pad*self.mYL - ylen*self.mYL, 
                                         self.mXL * xlen, 
                                         self.mYL * ylen], projection=self.proj))
        # 副图在主图内部，起始位置为xstart, ystart, 宽度为xlen, 高度为ylen
        elif loc == 'Inside':
            self.axs.append(self.fig.add_axes([self.mLB[0] + start[0]*self.mXL, 
                                         self.mLB[1] + start[1]*self.mYL, 
                                         self.mXL * xlen, 
                                         self.mYL * ylen], projection=self.proj))
        else:
            print("Wrong loc parameter, please check")
        
        return self.axs[-1]
    
    
    def quick_map(self, lat, lon, data, cmap='hot_r', cmappcs=10, vmin=None, vmax=None, unit='Unit ($unit$)', **kwargs):
        '''
        快速绘制地图
        '''
        import os
        import numpy as np
        
        ax = self.addMainAxes(isGeo=True, **kwargs)
        
        if not os.path.exists('hydroJson/quick_map.json'):
            genGeoAxesJson('hydroJson/quick_map.json')
        
        if vmin == None and vmax == None:
            vmin = np.nanpercentile(data, 1)
            vmax = np.nanpercentile(data, 99)
            
        gp = GeoAxesPlot(ax, 'hydroJson/quick_map.json')
        
        gp.baseMap()
        gp.stackImage(data, lat, lon, cmap, cmappcs, vmin, vmax)
        
        cax = self.addDeputyPlot('Right', 0.01, 0.03, 1.0, 0.0)
        gp.addColorBar(cax, cmappcs+1, 'neither', unit, cbarLabelSize=9, **kwargs)
        
                