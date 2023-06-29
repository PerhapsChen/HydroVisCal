# HydroVisCal
项目地址 https://github.com/PerhapsChen/HydroVisCal

?> `HydroVisCal` (**Hydro**logy **Vis**ualization & **Cal**culation) is a `Python` package maintained by CHEN Penghan based on `numpy`, `pandas`, `xarray`, `matplotlib`, `cartopy`, etc. 

在科研计算中，经常会需要编写大量的计算和可视化的代码以达到我们期望的效果。例如，当我们想要画一幅折线图，需要调整各种绘图细节参数，这些参数可能分布在不同行的代码中，尤其是参数较多的时候并不是特别方便。更加泛用的代码能更显著提高我们的工作效率。基于因此痛点，编写了一系列类和函数，方便更高效的进行科研的计算和可视化，目前仍处在初步开发阶段。它们大部分采用数据和逻辑分离的方式，使用`json`管理参数，进而让我们的工程代码文件更加简洁，逻辑更加清晰。把更多的时间留给科学问题的思考，而不是繁琐的代码参数调整。在某些情况下，这些代码能够数倍提高工作效率。[Wait for translating]

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

**原型及功能：**

```python
def LonCoords(start, end, resolution)
```

给定开始和结束的纬度，以及分辨率，返回对应纬度序列

**例子：**

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

**原型及功能：**

```python
def FromLatLonGetAreaMat(lat, lon)
```

给定lat和lon序列，返回网格面积矩阵。

**例子：**

```python
# import 
from HYDRO_Plot.GridArea import FromLatLonGetAreaMat
from 

Sij = FromLatLonGetAreaMat(lat, lon)
```



