import numpy as np
import xarray as xr

def GenXarrayDS(data, name, time, lat, lon):
    """
    Given a 2D or 3D numpy array and its coordinate information, return the xarray dataset.
    """
    
    assert len(data.shape) in [2, 3],\
        "Shape of data must be 2 or 3."
        
    if len(data.shape)==2:
        assert data.shape == (len(lat), len(lon)),\
            "Shape for data, lat, lon are not matched."
            
        ds = xr.Dataset( data_vars={ name: (['lat', 'lon'], data) },
                         coords={ 'lat': (['lat'], lat),  'lon': (['lon'], lon)} ) 
    elif len(data.shape)==3:
        assert data.shape == (len(time), len(lat), len(lon)),\
            "Shape for data, time, lat, lon are not matched."
        ds = xr.Dataset(data_vars={ name: (['time', 'lat', 'lon'], data) },
                        coords={'time': time,
                                'lat': (['lat'], lat),
                                'lon': (['lon'], lon)})
    return ds
   