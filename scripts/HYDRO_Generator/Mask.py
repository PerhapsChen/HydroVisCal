import numpy as np
from HYDRO_Generator.GlobalGridInfo import FromLatLonGetLandOrSea

def RemoveSeaAsNan(arr, latlst, lonlst):
    """
    Given a 2D/3D array, remove the sea area as nan.
    """
    assert len(arr.shape) in [2, 3], "Shape of data must be 2 or 3."
    landMask = FromLatLonGetLandOrSea(latlst, lonlst, boolType=False)
    if len(arr.shape)==2:
        arr = arr * landMask
    else:
        arr = arr * landMask[np.newaxis, :, :]
    
    return arr
    
def RemoveLandAsNan(arr, latlst, lonlst):
    """
    Given a 2D/3D array, remove the land area as nan.
    """
    assert len(arr.shape) in [2, 3], "Shape of data must be 2 or 3."
    seaMask = FromLatLonGetLandOrSea(latlst, lonlst, boolType=False)
    seaMask = np.where(seaMask==1, np.nan, 1)
    
    if len(arr.shape)==2:
        arr = arr * seaMask
    else:
        arr = arr * seaMask[np.newaxis, :, :]
    
    return arr
        
    
    