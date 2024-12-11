from my_.files.handy import create_dirs, check_file_exists
import os
from glob import glob
import xarray as xr
import numpy as np

v381_yearly = {
    'name': 'GLEAM_v3.8a_yearly',
    'version': (3, 8, 1),
    'path': '/p/scratch/cjibg31/jibg3105/data/GLEAM/3.8a/yearly/',
    'type_file': 'netcdf',
    'year_start': 1980,
    'month_start': 1,
    'year_end': 2022,
    'month_end': 12,
    'resolution_time': 'YE',
    'grid': 'GLEAM',
    'variables': ['ET', 
                  'PET',
                  'SM',],
    'variable_names': {'ET': 'E',
                       'PET': 'Ep',
                       'SM': ['SMsurf', 'SMroot'],
                       },
    'variable_dimensions': {'ET': ['time', 'lat', 'lon'],
                            'PET': ['time', 'lat', 'lon'],
                            'SM': ['time', 'layer', 'lat', 'lon'],},
    'variable_units': {'ET': 'mm/year',
                       'PET': 'mm/year',
                       'SM': 'm^3/m^3'},
    'mask_value': None
}


def create_yearly_files(path_rawdata: os.PathLike,
                        path_out: os.PathLike):
    
    """
    Input directory should only contain the GLEAM rawdata files...
    """

    print('\nConvert GLEAM files to yearly...\n')
    
    create_dirs(path_out)

    files = glob(f'{path_rawdata}/*GLEAM*.nc')

    data_raw = xr.open_mfdataset(files)

    years = np.unique(data_raw.time.dt.year.values)

    for y in years:

        print(f'Create yearly file for year {y}...\n')

        if check_file_exists(f'{path_out}/{y}.nc'): continue

        data_y = data_raw.sel(time = data_raw.time.dt.year.isin([y]))

        data_y.to_netcdf(f'{path_out}/{y}.nc',
                         format = 'NETCDF4_CLASSIC', 
                         unlimited_dims = ['time'])
