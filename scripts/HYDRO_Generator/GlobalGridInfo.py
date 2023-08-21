import numpy as np
from global_land_mask import globe


def FromLatLonGetAreaMat(latlst, lonlst):
    """
    Given list of lat, lon, return the area matrix.
    """
    R = 6371.4e3
    lat_j_rad = np.deg2rad(latlst)
    cos_j = np.cos(lat_j_rad)
    Sj = 2 * np.pi**2 * cos_j * R**2 / (180 * 360)
    Sij = np.repeat(Sj.reshape(-1, 1), len(lonlst), axis=1)
    return Sij


def FromLatLonGetLandOrSea(latlst, lonlst, boolType=True):
    """
    Given list of lat, lon, return the land or sea matrix .
    If boolType is True, return bool matrix, else return 1 for land and nan for sea (easy for multiply).
    """
    lat_mesh, lon_mesh = np.meshgrid(latlst, lonlst)
    land_mask = globe.is_land(lat_mesh, lon_mesh).T
    if boolType:
        return land_mask
    else:
        return np.where(land_mask, 1, np.nan)

    