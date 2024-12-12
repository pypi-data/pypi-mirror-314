import os
from my_.files.handy import create_dirs, check_file_exists
from glob import glob
import xarray as xr
import numpy as np


all_EUCORDEX_daily = {
    'name': 'BGC_EU3',
    'version': (1, 0, 6),
    'path': '/p/scratch/cjibg31/jibg3105/data/ERA5L/all/',
    'type_file': 'netcdf',
    'year_start': 1979,
    'month_start': 1,
    'year_end': 2022,
    'month_end': 12,
    'resolution_time': 'D',
    'grid': 'ERA5L_EUCORDEX',
    'variables': ['P',
                  'ET',
                  'PET',
                  'Runoff',
                  'SM'],
    'variable_names': {'P': 'tp',
                       'ET': 'e',
                       'PET': 'pev',
                       'Runoff': 'ro',
                       'SM': ['swvl1', 'swvl2', 'swvl3', 'swvl4']},
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
    'mask_value': -32767,
}


def create_yearly_files(path_rawdata: os.PathLike,
                        path_out: os.PathLike):
    
    """
    Input directory should only contain the ERA5L rawdata files...
    """

    print('\nConvert ERA5L files to yearly...\n')
    
    create_dirs(path_out)

    files = sorted(glob(f'{path_rawdata}/*.nc'))

    for f in files:

        file_year = f.split('/')[-1]

        if check_file_exists(f'{path_out}/{file_year}'): continue

        data_raw = xr.open_dataset(f)

        data_raw['e'] = data_raw['e'] * -1
        data_raw['pev'] = data_raw['pev'] * -1

        print(f'Create yearly file for file {f}...\n')

        data_raw.to_netcdf(f'{path_out}/{file_year}',
                         format = 'NETCDF4_CLASSIC', 
                         unlimited_dims = ['time'])
        

def merge_files(paths_rawdata: os.PathLike,
                path_out: os.PathLike):
    
    """
    Input directory should only contain the ERA5L rawdata files...
    """

    print('\nMerge ERA5L files...\n')
    
    create_dirs(path_out)
    
    files = []

    for p in paths_rawdata:
    
        pp = sorted(glob(f'{p}/*.nc'))

        files.extend(pp)

    data_raw = xr.open_mfdataset(files)

    years = np.unique(data_raw.time.dt.year.values)

    for y in years:

        print(f'Create yearly file for year {y}...\n')

        if check_file_exists(f'{path_out}/{y}.nc'): continue

        data_y = data_raw.sel(time = data_raw.time.dt.year.isin([y]))

        data_y.to_netcdf(f'{path_out}/{y}.nc',
                         format = 'NETCDF4_CLASSIC', 
                         unlimited_dims = ['time'])