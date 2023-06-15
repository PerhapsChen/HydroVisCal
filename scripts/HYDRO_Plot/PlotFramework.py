import matplotlib.pyplot as plt
import cartopy.crs as ccrs

class PlotFramework:
    def __init__(self,dpi=200):
        self.fig = plt.figure(dpi=dpi)
        self.axs = []

    def addMainAxes(self, isGeo=False, proj=ccrs.PlateCarree()):
        '''
        isGeo: 主图是否为地理坐标系
        proj: 地图投影方式
        '''
        if isGeo:
            self.main_ax = self.fig.add_axes([0,0,1,1], projection=proj)
            self.main_ax.set_extent([-180,180,90,-90])

        else:
            self.main_ax = self.fig.add_axes([0,0,1,1])
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
        elif loc == 'Inside':
            self.axs.append(self.fig.add_axes([self.mLB[0] + start[0]*self.mXL, 
                                         self.mLB[1] + start[1]*self.mYL, 
                                         self.mXL * xlen, 
                                         self.mYL * ylen]))
        else:
            print("Wrong loc parameter, please check")
        
        return self.axs[-1]