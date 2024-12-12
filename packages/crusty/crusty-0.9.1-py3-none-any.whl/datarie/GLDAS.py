import os
from datarie.handy import create_dirs, check_file_exists
from glob import glob
import xarray as xr
import numpy as np
import pandas as pd

NOAH025_all_EUROCORDEX_monthly = {
    'name': 'GLDAS_NOAH025_M',
    'version': (1, 0, 6),
    'path': '/p/scratch/cjibg31/jibg3105/data/GLDAS/NOAH025_M/',
    'type_file': 'netcdf',
    'year_start': 1980,
    'month_start': 1,
    'year_end': 2014,
    'month_end': 12,
    'resolution_time': 'MS',
    'grid': 'GLDAS',
    'variables': ['P',
                  'ET',
                  'PET',
                  'Runoff',
                  'SM'],
    'variable_names': {'P': 'Rainf_f_tavg',
                       'ET': 'Evap_tavg',
                       'PET': 'PotEvap_tavg',
                       'Runoff': 'ro',
                       'SM': 'RootMoist_inst'},
    'variable_dimensions': {'P': ['time', 'lat', 'lon'], 
                            'ET': ['time', 'lat', 'lon'],
                            'PET': ['time', 'lat', 'lon'],
                            'Runoff': ['time', 'lat', 'lon'],
                            'SM': ['time', 'layer', 'lat', 'lon']}, 
    'variable_units': {'P': 'm/day',
                       'ET': 'm/day',
                       'PET': 'm/day',
                       'Runoff': 'm/day',
                       'SM': 'm^3/m^3'},
    'mask_value': None,
    'leapday': True,}


def create_yearly_files(path_rawdata: str,
                        path_out: str):
    
    """
    Input directory should only contain the GLEAM rawdata files...
    """

    print('\nConvert GLDAS files to yearly...\n')
    
    create_dirs(path_out)

    files = glob(f'{path_rawdata}/*')

    data_raw = xr.open_mfdataset(files).load()
    
    years = np.unique(data_raw.time.dt.year.values)

    for y in years:

        print(f'Create yearly file for year {y}...\n')

        if check_file_exists(f'{path_out}/{y}.nc'): continue

        data_y = data_raw.sel(time = data_raw.time.dt.year.isin([y]))

        data_y.to_netcdf(f'{path_out}/{y}.nc',
                         format = 'NETCDF4_CLASSIC', 
                         unlimited_dims = ['time'])