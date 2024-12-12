
import numpy as np
import xarray as xr

def vpd_allen_2000(temp_max: np.ndarray | xr.DataArray,
                   temp_min: np.ndarray | xr.DataArray,
                   temp: np.ndarray | xr.DataArray,
                   rh: np.ndarray | xr.DataArray,
                   ) -> np.ndarray | xr.DataArray:
    
    # Temperature in ° Celsius    

    assert (temp_max.shape == \
            temp_min.shape == \
            temp.shape == \
            rh.shape)
    
    print(f'\nCalculating VPD [kPa] from Temperature and RH...\n')

    # doi: 10.1175/BAMS-86-2-225
    temp_dew = temp - ((100 - rh) / 5) 

    # ISBN: 978-92-5-104219-9 
    es_tmin = 0.6108 * np.exp((17.27 * temp_min) / (temp_min + 237.3))
    es_tmax = 0.6108 * np.exp((17.27 * temp_max) / (temp_max + 237.3))

    es = (es_tmax + es_tmin) / 2

    ea = 0.6108 * np.exp((17.27 * temp_dew) / (temp_dew + 237.3))

    # kPa
    vpd = es - ea

    if isinstance(vpd, xr.DataArray): vpd.rename('VPD')

    return vpd