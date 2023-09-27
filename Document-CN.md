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

#### 原型

```python
def LonCoords(start, end, resolution)
```

#### 功能

给定开始和结束的纬度，以及分辨率，返回对应纬度序列

#### 使用例子

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

#### 原型

```python
def FromLatLonGetAreaMat(latlst, lonlst)
```

#### 功能

给定经纬度序列，返回由经纬度序列组成矩阵的对应的网格面积，通常用于面积加权相关的计算。

#### 使用例子

```python
# import 
from HYDRO_Plot.GlobalGridInfo import FromLatLonGetAreaMat

Sij = FromLatLonGetAreaMat(latList, lonList)
```

## FromLatLonGetLandOrSea

#### 原型

```python
def FromLatLonGetLandOrSea(latlst, lonlst, booType=True)
```

#### 功能

给定经纬度序列，返回由经纬度序列组成矩阵的陆地海洋属性。

- 当boolType为True(默认)时，返回的矩阵中，True代表陆地，False代表海洋
- 当boolType为False时，返回的矩阵中，1代表陆地，NaN代表海洋，方便用于直接乘法计算。

#### 使用例子

```python
# import 
from HYDRO_Plot.GlobalGridInfo import FromLatLonGetLandOrSea

isLand = FromLatLonGetLandOrSea(latList, lonList)
```

## RemoveSeaAsNan

#### 原型

```python
def RemoveSeaAsNan(arr, latlst, lonlst)
```

#### 功能

给定2D或3D的numpy数组，以及对应的经纬度序列，将移出海洋部分数值，设置为NaN。

#### 使用例子

```python
# import 
from HYDRO_Plot.Mask import RemoveSeaAsNan

arr = RemoveSeaAsNan(arr, latList, lonList)
```

## RemoveLandAsNan

类似`RemoveSeaAsNan`，移出陆地部分为NaN。



---

# HYDRO_Plot

