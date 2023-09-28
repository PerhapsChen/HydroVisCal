import os
import json

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

import cartopy.crs as ccrs
import cartopy.feature as cfeature

from HYDRO_Plot.ColorBarFromFig import ColorBarFromFig


def genGeoAxesJson(outputJsonPath='./hydroJson/DefaultGeoAxes.json', returnDict=False):
    PARAMETERS = {
        'box_lw'            : 1,  
        'facecolor'         : 'none',
        'set_global'        : True,
        'has_stock_img'     : False,
        'has_coastlines'    : True,
        'coast_line_width'  : 0.5,
        'has_land'          : False,
        'has_ocean'         : False,
        'extent'            : [-180.001, 180.001, -90.0, 90.0],
        'stack_Image'          :
            {
                'remap'             : False,
            },
    }
    
    if not os.path.exists(os.path.dirname(outputJsonPath)):
        os.mkdir(os.path.dirname(outputJsonPath))
        
    with open(outputJsonPath, "w", encoding='utf-8') as f:
        json.dump(PARAMETERS, f, indent=2)  
    
    print("Json file of parameters has written to [{}]".format(outputJsonPath))
    
    if returnDict:
        return PARAMETERS
    
class GeoAxesPlot:
    def __init__(self, ax, jsonPath='./hydroJson/DefaultGeoAxes.json'):
        assert os.path.isfile(jsonPath), "Json file doesn't exist! "
        assert ax.__class__.__name__ == 'GeoAxes', \
            "Input ax must be GeoAxes, but given {}".format(ax.__class__.__name__)
        self.jsonPath = jsonPath
        self.ax = ax
        with open(jsonPath) as f:
            self.paraDict = json.load(f)
            
    def reloadJson(self):
        with open(self.jsonPath) as f:
            self.paraDict = json.load(f)  
    
    def genDefaultJson(self):
        """
        go back to default json
        """
        genGeoAxesJson(self.jsonPath)
        
    def saveCurrentJson(self, outputJsonPath='./hydroJson/currentGeoAxesMap.json'):
        if not os.path.exists(os.path.dirname(outputJsonPath)):
            os.mkdir(os.path.dirname(outputJsonPath))
            
        with open(outputJsonPath, "w", encoding='utf-8') as f:
            json.dump(self.paraDict, f, indent=2)  
        
        print("Current parameters has written to [{}]".format(outputJsonPath)) 
        
    def listChinaExtent(self):
        return [70, 140, 15, 55]
        
    def baseMap(self):
        self.reloadJson()
        PARAS = self.paraDict
        
        if PARAS['set_global']:
            self.ax.set_global()     
        if PARAS['has_stock_img']:
            self.ax.stock_img()
        if PARAS['has_coastlines']:
            self.ax.coastlines(lw=PARAS['coast_line_width'])
        if PARAS['has_land']:
            self.ax.add_feature(cfeature.LAND)
        if PARAS['has_ocean']:
            self.ax.add_feature(cfeature.OCEAN)
        self.ax.set_extent(tuple(PARAS['extent']), crs=ccrs.PlateCarree())
        plt.setp(self.ax.spines.values(), linewidth=PARAS['box_lw'])
    
    def addLonLatTicks(self, lon_ticks=None, lat_ticks=None, 
                       lon_grids=None, lat_grids=None,
                       lat_pos='bottom', lon_pos='left',
                       **kwargs):
        from cartopy.mpl.gridliner import LongitudeFormatter, LatitudeFormatter
        if lon_ticks is not None:
            self.ax.set_xticks(lon_ticks, crs=ccrs.PlateCarree())
        if lat_ticks is not None:
            self.ax.set_yticks(lat_ticks, crs=ccrs.PlateCarree())

        if lat_pos=='bottom':
            self.ax.xaxis.set_ticks_position('bottom')
        elif lat_pos=='top':
            self.ax.xaxis.set_ticks_position('top')
        else:
            raise ValueError("lat_pos must be 'bottom' or 'top', but given {}".format(lat_pos))
        
        if lon_pos=='left':
            self.ax.yaxis.set_ticks_position('left')
        elif lon_pos=='right':
            self.ax.yaxis.set_ticks_position('right')
        else:
            raise ValueError("lon_pos must be 'left' or 'right', but given {}".format(lon_pos))
        
        lon_formatter = LongitudeFormatter(zero_direction_label=True)
        lat_formatter = LatitudeFormatter()
        
        self.ax.xaxis.set_major_formatter(lon_formatter)
        self.ax.yaxis.set_major_formatter(lat_formatter)
        self.ax.gridlines(xlocs=lon_grids, ylocs=lat_grids, **kwargs)
    
    def stackImage(self, data, lat, lon, cmap='viridis', cmappcs=None, vmin=None, vmax=None):
        assert all(np.diff(lat) < 0), "Latitude is not descending!"
        assert len(data.shape)==2, "Only support 2D data, but given {}D".format(len(data.shape))
        assert data.shape[0]==len(lat) and data.shape[1]==len(lon),\
            "Shape of lat [{}], lon[{}], data[{}] are not matched.".format(len(lat),len(lon),data.shape)
        
        self.reloadJson()
        PARAS = self.paraDict['stack_Image'] # 使用stackImg的参数
        
        if type(cmap) == str:
            if '.' in cmap:
                cbff = ColorBarFromFig(cmap, piece=cmappcs, reverse=False, inputPcs=cmappcs)
                cmap = cbff.getColorBar()
            else:
                cmap = plt.get_cmap(cmap, cmappcs)
        
        dx = np.diff(lon).mean() / 2
        dy = np.diff(lat).mean() / 2
        extent = [max(np.min(lon) - dx, -179.99), 
                  min(np.max(lon) + dx, 179.99), 
                  max(np.min(lat) + dy, -89.99),
                  min(np.max(lat) - dy, 89.99)]
        
        if PARAS['remap']:
            self.ax.set_extent(extent,crs=ccrs.PlateCarree())
        
        im = self.ax.imshow(data, extent=extent, transform=ccrs.PlateCarree(), cmap=cmap)

        if vmin==None or vmax==None:
            vmin = np.nanmin(data)
            vmax = np.nanmax(data)
            
        im.set_clim(vmin=vmin, vmax=vmax)
        
        self.vmax = vmax
        self.vmin = vmin
        self.cmap = cmap
        self.cmap_pcs = cmappcs
        
    def addColorBar(self, cax, tickNums=None, 
                    cbarExtend='both', 
                    cbarUnit='Unit ($unit$)', 
                    cbarShrinkTicks=False,
                    cbarOrientation='V',
                    cbarLabelSize=12,
                    ):
        if tickNums==None:
            ticks = list(np.linspace(self.vmin, self.vmax, 6))
        elif type(tickNums)==int:
            ticks = list(np.linspace(self.vmin, self.vmax, tickNums))
        else:
            ticks = tickNums
        
        # 避免colobar两边ticks过于靠边
        if cbarShrinkTicks:
            self.vmin = self.vmin - (ticks[1] - ticks[0]) / 2
            self.vmax = self.vmax + (ticks[1] - ticks[0]) / 2

        norm = mpl.colors.Normalize(vmin=self.vmin, vmax=self.vmax)
        # pos = self.ax.get_position()
        # orientation = PARAS['cbar_orientation']
        assert cbarOrientation in ['V', 'H'],\
            "Orientation of colorbar only support 'V'(vertical) and 'H'(horizontal)."
            
        if cbarOrientation == 'V': # vertical
            cbar = mpl.colorbar.ColorbarBase(cax, cmap=self.cmap, norm=norm, 
                                             extend=cbarExtend, orientation='vertical')
            cbar.ax.set_ylabel(cbarUnit)
            
        elif cbarOrientation == 'H': # horizontal
            cbar = mpl.colorbar.ColorbarBase(cax, cmap=self.cmap, norm=norm, 
                                             extend=cbarExtend, orientation='horizontal')
            cbar.ax.set_xlabel(cbarUnit, fontsize=cbarLabelSize)
        
        cbar.set_ticks(ticks)
        cbar.ax.tick_params(labelsize=cbarLabelSize)
            
    # def stackScatter(self, data, lat, lon, zorder=0):
    
    #     data = np.array(data)
    #     assert len(data.shape)==1, "Only support 1D data, but given {}D".format(len(data.shape))
    #     assert len(lat)==len(lon)==len(data), "Length of data, lon and lat is not equal!" 
        
    #     PARAS = self.paraDict['stackSct']
        
    #     if PARAS['cmap_path']:
    #         pieces = PARAS['cmap_pcs']
    #         reverse = PARAS['cmap_reverse']
    #         input_pieces = PARAS['cmap_input_pieces']
    #         acbar = ColorBarFromFig(PARAS['cmap_path'], pieces, reverse, input_pieces)
    #         cmap = acbar.getColorBar()
    #     else:
    #         if PARAS['cmap_pcs'] == -1:
    #             cmap = plt.get_cmap(PARAS['cmap_string'])
    #         else:
    #             cmap = plt.get_cmap(PARAS['cmap_string'], PARAS['cmap_pcs']) 
        
    #     dx = PARAS['extent_pad']
    #     dy = PARAS['extent_pad']
    #     extent = [max(np.min(lon) - dx, -179.99), 
    #               min(np.max(lon) + dx, 179.99), 
    #               max(np.min(lat) + dy, -89.99),
    #               min(np.max(lat) - dy, 89.99)]
    #     if PARAS['remap']:
    #         self.ax.set_extent(extent,crs=ccrs.PlateCarree())
        
    #     sct = self.ax.scatter(lon, lat, c=data, s=PARAS['marker_size'], marker=PARAS['marker_style'], 
    #                           lw=PARAS['marker_lw'], edgecolor=PARAS['marker_edgecolor'],
    #                           transform=ccrs.PlateCarree(), cmap=cmap, zorder=zorder)

    #     # 确定绘图所用数据的范围
    #     cbarLimit = PARAS['cmap_limit']
    #     if cbarLimit:
    #         vmin = cbarLimit[0]
    #         vmax = cbarLimit[1]
    #     else:
    #         vmin = np.nanmin(data)
    #         vmax = np.nanmax(data)
            
    #     sct.set_clim(vmin=vmin, vmax=vmax)
        
    #     # 如果需要绘制colorbar
    #     if PARAS['has_colorbar']:
    #         # 根据 cbar_ticks_params 参数确定colorbar的tick and label.
    #         cbarTicksParams = PARAS['cbar_ticks_params']
    #         assert (len(cbarTicksParams) in [0, 1, 2, 3]),\
    #             "cbarTicksParams only support 0/1/2/3 paras input."
    #         if not cbarTicksParams:
    #             ticks = list(np.linspace(vmin, vmax, 6))
    #         elif len(cbarTicksParams)==1:
    #             ticks = list(np.linspace(vmin, vmax, cbarTicksParams[0]))
    #         elif len(cbarTicksParams)==2:
    #             ticks = list(np.linspace(cbarTicksParams[0], cbarTicksParams[1], 6))
    #         else:
    #             ticks = list(np.linspace(cbarTicksParams[0], cbarTicksParams[1], int(cbarTicksParams[2])))
            
    #         # 避免colobar两边ticks过于靠边
    #         if PARAS['cbar_shrink_ticks']:
    #             vmin = vmin - (ticks[1] - ticks[0]) / 2
    #             vmax = vmax + (ticks[1] - ticks[0]) / 2

    #         norm = mpl.colors.Normalize(vmin=vmin, vmax=vmax)
    #         pos = self.ax.get_position()
    #         orientation = PARAS['cbar_orientation']
    #         assert orientation in ['V', 'H'],\
    #             "Orientation of colorbar only support 'V'(vertical) and 'H'(horizontal)."
                
    #         if orientation == 'V': # vertical
    #             pad = PARAS['vertical_paras']['pad']
    #             width = PARAS['vertical_paras']['width']
    #             clen = PARAS['vertical_paras']['len']
    #             cax = self.fig.add_axes([pos.xmax + pad, pos.ymin, width, (pos.ymax - pos.ymin)])
    #             cbar_extend = PARAS['cbar_extend']
    #             cbar = mpl.colorbar.ColorbarBase(cax, cmap=cmap, norm=norm, extend=cbar_extend, orientation='vertical')
    #             cbar.ax.set_ylabel(PARAS['cbar_unit'])
                
    #         elif orientation == 'H': # horizontal
    #             pad = PARAS['horizontal_paras']['pad']
    #             width = PARAS['horizontal_paras']['width']
    #             clen = PARAS['horizontal_paras']['len']
    #             cax = self.fig.add_axes([pos.xmin + (pos.xmax - pos.xmin) * (1 - clen) / 2,
    #                                      pos.ymin - pad - width, 
    #                                      (pos.xmax - pos.xmin) * clen, 
    #                                      width])
    #             cbar_extend = PARAS['cbar_extend']
    #             cbar = mpl.colorbar.ColorbarBase(cax, cmap=cmap, norm=norm, extend=cbar_extend, orientation='horizontal')
    #             cbar.ax.get_xaxis().labelpad = 8
    #             cbar.ax.set_xlabel(PARAS['cbar_unit'])
            
    #         cbar.set_ticks(ticks)