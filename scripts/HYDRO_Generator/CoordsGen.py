import numpy as np
import pandas as pd

def LonCoords(start, end, resolution):
    """
    给定起始和结束以及分辨率生成纬度，例如给了40,50,0.1,
    则生成[40.05, .... 49.85, 49.95]共100个。
    """
    assert resolution>0, "resolution must be positive."
    if start > end:
        print("[Warning] Bad for longitude: start > end.")
        S = start - resolution/2
        E = end + resolution/2 - 1e-5
        R = -resolution
    else:
        S = start + resolution/2
        E = end - resolution/2 + 1e-5
        R = resolution
    return np.arange(S, E, R)

def LatCoords(start, end, resolution):
    """
    给定起始和结束以及分辨率生成经度，例如给了30,20,0.1,
    则生成[29.95, 29.85, ..., 20.15, 20.05]共100个。
    """
    assert resolution>0, "resolution must be positive."
    if start > end:
        S = start - resolution/2
        E = end + resolution/2 - 1e-5
        R = -resolution
    else:
        print("[Warning] Bad for latitude: start < end.")
        S = start + resolution/2
        E = end - resolution/2 + 1e-5
        R = resolution
    return np.arange(S, E, R)

def TimeCoords(start, end, resolution):
    """
    Not Recommend.
    """
    return pd.date_range(start=start, end=end, freq=resolution)