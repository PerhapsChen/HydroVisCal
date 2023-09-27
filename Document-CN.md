# HydroVisCal
项目地址 https://github.com/PerhapsChen/HydroVisCal

## 项目简介

**HydroVisCal**是一个用于地球科学（主要是水文、气象）计算和可视化的Python库。

## 模块简介

- **HYDRO_Generator**:  用于从零生成数据，例如经纬度序列等
- **HYDRO_Plot**: 用于数据的可视化，包括常规图和地图等
- **HYDRO_Time**: 用于处理时间相关的数据
- **HYDRO_Format**: 用于处理格式问题，例如格式转换等
- **HYDRO_MP**: 用于提供一些并行的接口
- **HYDRO_AI**: 提供一些初级的机器学习、深度学习相关接口
- **HYDRO_Stats**：一些统计的方法

# HYDRO_Generator

## LonCoords

给定开始和结束的纬度，以及分辨率，返回对应纬度序列

```python
def LonCoords(start, end, resolution)
```

**示例**

```python
# import 
from HYDRO_Plot.CoordsGen import LonCoords

lons = LonCoords(40, 50, 0.1)

# output
>> [40.05, .... 49.85, 49.95]
```

## LatCoords

同 `LonCoords`。

## FromLatLonGetAreaMat

给定经纬度序列，返回由经纬度序列组成矩阵的对应的网格面积，通常用于面积加权相关的计算。

```python
def FromLatLonGetAreaMat(latlst, lonlst)
```

**使用例子**

```python
# import 
from HYDRO_Plot.GlobalGridInfo import FromLatLonGetAreaMat

Sij = FromLatLonGetAreaMat(latList, lonList)
```

## FromLatLonGetLandOrSea

给定经纬度序列，返回由经纬度序列组成矩阵的陆地海洋属性。

- 当boolType为True(默认)时，返回的矩阵中，True代表陆地，False代表海洋
- 当boolType为False时，返回的矩阵中，1代表陆地，NaN代表海洋，方便用于直接乘法计算。

```python
def FromLatLonGetLandOrSea(latlst, lonlst, boolType=True)
```

**使用例子**

```python
# import 
from HYDRO_Plot.GlobalGridInfo import FromLatLonGetLandOrSea

isLand = FromLatLonGetLandOrSea(latList, lonList)
```

## RemoveSeaAsNan

给定2D或3D的numpy数组，以及对应的经纬度序列，将移出海洋部分数值，设置为NaN。

```python
def RemoveSeaAsNan(arr, latlst, lonlst)
```

**使用例子**

```python
# import 
from HYDRO_Plot.Mask import RemoveSeaAsNan

arr = RemoveSeaAsNan(arr, latList, lonList)
```

## RemoveLandAsNan

类似`RemoveSeaAsNan`，移出陆地部分为NaN。

## GenXarrayDS

给定2D或3D数组以及变量名，time，lat，lon序列，生成xarray dataset

```python
def GenXarrayDS(data, name, time, lat, lon)
```

示例

```python
import numpy as np
import pandas as pd
from HYDRO_Generator.XarrayDsGen import GenXarrayDS
from HYDRO_Generator.CoordsGen import LatCoords, LonCoords

arr_prec = np.random.rand(366, 100, 100)
lats = LatCoords(50, 40, 0.1)
lons = LonCoords(10, 20, 0.1)
times = pd.date_range('2000-01-01', '2000-12-31', freq='D')
ds = GenXarrayDS(arr_prec, 'prec', times, lats, lons)
```

---

# HYDRO_Format

## From2DNumpyArrayToTiff

将2D的numpy array输出为tiff文件。需要安装gdal。

```py
def From2DNumpyArrayToTiff(data, lat, lon, tiff_path)
```

## FromTiffToNumpyArray

读取tiff文件为二维数组，用于读取单band的tiff.

- 当return_lat_lon为True，会返回data, lat, lon。否则只返回data

```python
def FromTiffToNumpyArray(tiff_path, return_lat_lon=False)
```

---

# HYDRO_Stats

## TrendDetector

用于趋势检验，可以用于1D序列的趋势检验以及3D数组(对每个网格)的趋势检验。返回变化量、均值、变化率、p-value，斜率，截距。

- method可选**linear**（较慢）以及**sen**（推荐）方法。

```python
from HYDRO_Stats.TrendDetector import TrendDetector

class TrendDetector:
    def __init__(self, method='linear')
    def trend1D(self, arr)
    def trend3D(self, arr):
```

---



# HYDRO_Plot

## ColorbarFromFig

给定一张图片的路径（可以是我们在网上找到的好看的colorbar），制作一个一样的colobar。

```py
from HYDRO_Plot.ColorBarFromFig import ColorBarFromFig

class ColorBarFromFig:
    def __init__(self, path, piece=None, reverse=False, inputPcs=None)
    def getColorBar(self)
    def getColorBarArray(self)
```

## TrendPlot

给定一个一维序列，绘制趋势图，包括原本的值以及拟合的直线，以及拟合直线的斜率及显著性。

- 如果只想快速看一下序列`x`的趋势，使用`quickTrendPlot(x)`即可

```python
def genTrendPlotJson(outputJsonPath='./hydroJson/TrendPlot.json', returnDict=False)

class TrendPlot:
    def __init__(self, ax, jsonPath='./hydroJson/TrendPlot.json')
    def reloadJson(self)
    def genDefaultJson(self)
    def saveCurrentJson(self, outputJsonPath='./hydroJson/currentFromTrendPlot.json')
    def plot(self, x, y)

def quickTrendPlot(x, y=None)
```

## PlotFrameWork

绘制高度定制的子图框架

- 其中xlen, ylen是相对于主图的大小， start是相对于主图的偏移。loc可选[inside, left, right, top, bottom]

```python
class PlotFrameWork:
    def __init__(self, dpi=200)
    def addMainAxes(self, isGeo=False, proj=ccrs.PlateCarree())
    def updateMainAxesInfo(self, ax=None)
    def changeMainAxes(self, ax)
    def addDeputyPlot(self, loc, pad, xlen, ylen, start)
    def addDeputyPlot_Geo(self, loc, pad, xlen, ylen, start)
```

**示例**

```python
pf = PlotFramework(dpi=300)
# 创建主图
ax = pf.addMainAxes()
# 在主图内部添加子图 作为colorbar
cax = pf.addDeputyPlot(loc='inside', pad=0, xlen=0.2, ylen=0.05, start=[0.52,0.25])
gp.addColorBar(cax,tickNums=3,cbarExtend='both',cbarUnit='Changes of Diurnal Index',cbarOrientation='H')
# 在主图左侧添加子图 绘制纬度平均值
axLeft = pf.addDeputyPlot(loc='Left', pad=0.015,xlen=0.15,ylen=1,start=0)
axLeft.plot(np.nanmean(data, axis=1), lat, lw=0.5, color='k')
```

## GeoAxesPlot

给定一个geo ax, 在上面绘制地图。

```python
def genGeoAxesJson(outputJsonPath='./hydroJson/DefaultGeoAxes.json', returnDict=False)

class GeoAxesPlot:
    def __init__(self, ax, jsonPath='./hydroJson/DefaultGeoAxes.json')
    def reloadJson(self)
    def genDefaultJson(self)
    def saveCurrentJson(self, outputJsonPath='./hydroJson/currentGeoAxesMap.json')
    def listChinaExtent(self)
    def baseMap(self)
    def addLonLatTicks(self, lon_ticks=None, lat_ticks=None, 
                       lon_grids=None, lat_grids=None,
                       lat_pos='bottom', lon_pos='left', **kwargs):
    def stackImage(self, data, lat, lon, cmap='viridis', cmappcs=None, vmin=None, vmax=None)
    def addColorBar(self, cax, tickNums=None, cbarExtend='both', cbarUnit='Unit ($unit$)', 
                    cbarShrinkTicks=False,cbarOrientation='V',cbarLabelSize=12,)
    
```

**示例**

待补充
