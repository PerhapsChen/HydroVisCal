import numpy as np
import pandas as pd

def LonCoords(start, end, resolution):
    """
    Given (start, end, resolution) to generate the latitude,
    
    e.g. given (40,50,0.1) can get [40.05, .... 49.85, 49.95] for a total of 100.
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
    Given (start, end, resolution) to generate the latitude,
    
    e.g. given (30,20,0.1) can get [29.95, 29.85, ..., 20.15, 20.05] for a total of 100.
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
    Not recommend now.
    """
    #TODO: This function could be better.
    
    return pd.date_range(start=start, end=end, freq=resolution)