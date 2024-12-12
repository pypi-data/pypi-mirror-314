import numpy as np
import xarray as xr

regions = {'BI': [(50, -10), (50, 2), (59, 2), (59, -10)],
           'IP': [(36, -10), (36, 3), (44, 3), (44, -10)],
           'FR': [(44, -5), (44, 5), (50, 5), (50, -5)],
           'ME': [(48, 2), (48, 16), (55, 16), (55, 2)],
           'SC': [(55, 5), (55, 30), (70, 30), (70, 5)],
           'AL': [(44, 5), (44, 15), (48, 15), (48, 5)],
           'MD': [(36, 3), (36, 25), (44, 25), (44, 3)],
           'EA': [(44, 16), (44, 30), (55, 30), (55, 16)],}


def mask_prudence(array: np.ndarray | xr.DataArray,
                  lat: np.ndarray | xr.DataArray,
                  lon: np.ndarray | xr.DataArray,
                  sel_regions: str | list[str] | None):

    if sel_regions is None: return array

    shape = array.shape[-2:]

    mask = np.zeros(shape)

    for r in sel_regions:

        lat_max = regions[r][2][0]
        lat_min = regions[r][0][0]
        lon_max = regions[r][2][1]
        lon_min = regions[r][0][1]

        mask = np.where(((lat <= lat_max) & 
                        (lat >= lat_min) &
                        (lon <= lon_max) &
                        (lon >= lon_min)), 1, mask)
        
    if isinstance(array, xr.DataArray): 

        array_out = array.where(mask)

    return array_out