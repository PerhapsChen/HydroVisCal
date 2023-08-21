import numpy as np

def FromLatLonGetAreaMat(lat, lon):
    R = 6371.4e3
    lat_j_rad = np.deg2rad(lat)
    cos_j = np.cos(lat_j_rad)
    Sj = 2 * np.pi**2 * cos_j * R**2 / (180 * 360)
    Sij = np.repeat(Sj.reshape(-1, 1), len(lon), axis=1)
    return Sij
