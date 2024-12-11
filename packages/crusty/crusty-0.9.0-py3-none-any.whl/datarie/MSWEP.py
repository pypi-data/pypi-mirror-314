import os

from glob import glob
import xarray as xr
import numpy as np
import pandas as pd
import netCDF4 as nc
import timeit

from datarie.templates import gridded_data
from datarie.handy import create_dirs, check_file_exists

past_global_daily = {
    'name': 'MSWEP_past_global_daily',
    'version': (1, 0, 6),
    'path': '/p/scratch/cjibg31/jibg3105/data/GLEAM/MSWEP/yearly/',
    'type_file': 'netcdf',
    'year_start': 1979,
    'month_start': 1,
    'year_end': 2020,
    'month_end': 12,
    'resolution_time': 'D',
    'grid': 'MSWEP',
    'variables': ['P'],
    'variable_names': {'P': 'precipitation'},
    'variable_dimensions': {'P': ['time', 'lat', 'lon']}, 
    'variable_units': {'P': 'mm/day'},
    'mask_value': None,
    'leapday': True,}


def create_yearly_files(path_rawdata: os.PathLike[str]):
    
    print('\nConvert MSWEP files to yearly...\n')

    data_ = gridded_data(**past_global_daily)

    create_dirs(data_.path)

    time = data_.index_time()
    
    years = np.unique(time.dt.year.to_numpy())

    for y in years:

        start_time = timeit.default_timer()

        files = sorted(glob(f'{path_rawdata}/{y}*.nc'))

        data_y = xr.open_mfdataset(files, 
                                   combine = 'by_coords',
                                   chunks = {'time': len(files), 
                                             'lat': 32, 
                                             'lon': 32},
                                    engine = 'netcdf4').load()
        
        print(f'Create yearly file for year {y}...\n')

        if check_file_exists(f'{data_.path}/{y}.nc'): continue

        data_y.to_netcdf(f'{data_.path}/{y}.nc',
                         format = 'NETCDF4_CLASSIC', 
                         unlimited_dims = ['time'])
        
        data_y.close()

        print('Time for processing:')
        print(timeit.default_timer() - start_time)  
        print('Continue...')