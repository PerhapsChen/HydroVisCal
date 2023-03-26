"""_summary_
[CLASS]
"""

import numpy as np
import xarray as xr
import matplotlib.pyplot as plt


class GenerateDataset:
    def SaveAsNetCDF(self, path):
        bias = 1e-5
        lon = np.arange(-179.5, 180, 1)
        lat = np.arange(-89.5, 90, 1)
        time = np.arange(1, 13)
        #print(time.shape[0], lat.shape[0], lon.shape[0])
        data = np.random.randn(time.shape[0], lat.shape[0], lon.shape[0])

        ds = xr.Dataset(data_vars={'vvvv': (['time', 'lat', 'lon'], data)},
                        coords={'time': time,
                                'lat': (['lat'], lat),
                                'lon': (['lon'], lon)})

        ds.to_netcdf(path)
