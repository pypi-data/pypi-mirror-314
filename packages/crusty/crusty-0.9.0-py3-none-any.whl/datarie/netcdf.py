
import netCDF4 as nc
import numpy as np
import psutil
from typing import Literal

def nc_open(str_files: str | list,
            **kwargs):

    from glob import glob
    
    if isinstance(str_files, str):

        files = glob(str_files)

        n_files = len(files)

        if n_files == 1: return nc.Dataset(files[0], **kwargs)

        data = nc.MFDataset(sorted(files), **kwargs)

    elif isinstance(str_files, list):

        data = nc.MFDataset(sorted(str_files), **kwargs)
        
    return data


def variable_to_array(data: nc.Dataset, 
                      variable: str, 
                      stack_axis: int = 1,
                      dtype: str = 'float32',
                      mask_value: None | float | int = None):

    print(f'\nLoad netcdf variable {variable} to memory.')
    print(f'Available memory [GB]: {psutil.virtual_memory()[4] / 10**9}...\n')

    if isinstance(variable, list):

        arrays = [data.variables[v][:] 
                  for v in variable]

        array = np.stack(arrays, 
                         axis = stack_axis)
              
    elif isinstance(variable, str):

        netcdf_variable = data.variables[variable]

        array = netcdf_variable[:]

    np_dtype = getattr(np, dtype)
    
    array_out = array.astype(np_dtype)

    if mask_value is not None:

        array_out = np.ma.masked_values(array_out, mask_value)

    if isinstance(array_out, np.ma.masked_array): return array_out.filled(np.nan)
    else: return array_out
    

def variables_to_array(data: nc.Dataset, 
                       variables: list[str],
                       stack_axis: int = 1, 
                       dtype: str = 'float64',
                       mask_value: None | float | int = None):
    
    arrays_dtype = [variable_to_array(data, 
                                      v, 
                                      stack_axis,
                                      dtype,
                                      mask_value) for v in variables]

    return arrays_dtype


def variables_to_dict(data: nc.Dataset, 
                       variables: list[str],
                       stack_axis: int = 1, 
                       dtype: str = 'float64',
                       mask_value: None | float | int = None):
    
    if isinstance(variables, str): 
        variables = [variables]
    
    arrays_dtype = {v: variable_to_array(data, 
                                         v, 
                                         stack_axis,
                                         dtype,
                                         mask_value) for v in variables}

    return arrays_dtype

    
def netcdf_time(data: nc.Dataset,
                name_time: str = 'time',
                only_use_python_datetimes: bool = False,
                **kwargs):
    
    ## BAUSTELLE

    var = data.variables[name_time]
    units = var.units
    calendar = var.calendar

    dtime = nc.num2date(var[:], 
                        units = units, 
                        calendar = calendar,
                        only_use_python_datetimes = only_use_python_datetimes,
                        **kwargs)

    return dtime


def nc_out(fname: str,
           dimensions: dict,
           variables: dict,
           attributes: dict = {}, 
           format: Literal['NETCDF4_CLASSIC', 
                           'NETCDF3_CLASSIC'] = 'NETCDF4_CLASSIC',
           ) -> nc.Dataset:


    # dims = {'lat': {'dtype': np.float64, 'dims': [lat, lon], 'size': 16, 'attrs': {'units': 'degrees east'}}}
    # vars = {'temp: {'dtype': np.float64, 'dims':  [lat, lon], 'attrs': {'units': 'degrees east'}}}

    print(f'\nCreating netCDF output to: {fname}...\n')

    nc_out = nc.Dataset(fname, 
                        mode = 'w',
                        format = format)
    
    for k, v in attributes.items():

        nc_out.setncattr(k, v)
    
    for dim, dimc in dimensions.items():

        dim_nc = nc_out.createDimension(dim, dimc['size'])

        dim_var = nc_out.createVariable(dim, dimc['dtype'], dimc['dims'])

        for k, v in dimc['attrs'].items():
        
            dim_var.setncattr(k, v)
    
    for var, varc in variables.items():
        
        var_nc = nc_out.createVariable(var, varc['dtype'], varc['dims'])

        for k, v in varc['attrs'].items():
        
            var_nc.setncattr(k, v)

    return nc_out