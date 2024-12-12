

def src_var_apply_nc(name: str = '', sources: list = [], variables: list = [], 
                    array_sel_4d = None, method_sel = 'argmax', axis_sel: int = 0, 
                    axis_sel_shrink: int = 0, method_agg_4d: str = 'mean',
                    method_agg_time: str ='mean'):

    """
    Make an array 4d tesseract ("cube")
    assuming axis -2 and -1 are lat lon
    aggregated by method keywords 
    over time and e.g. pfts or soil layers
    """

    import xarray as xr

    from my_files.netcdf import open_netcdf
    from my_files.handy import check_file_exists
    from my_resources.sources import query_variables
    from my_resources.units import transform
    from my_files.netcdf import netcdf_variable_to_array
    from my_gridded.aggregate import select_o_apply_d


    file_out                    = f"out/nc/{name}_*{'+'.join(sources)}*_{'+'.join(variables)}_{method_agg_time}.nc"

    print(file_out)

    if check_file_exists(file_out): return

    print('File does not exists')

    data_out                    = xr.Dataset({})
    
    for src in sources:

        path                    = query_variables(src = src, key = 'path')
        data_src                = open_netcdf(f'{path}*.nc')

        for var in variables:

            print(f'Processing {src} - {var}')
            
            var_src                     = query_variables(src = src,  key = 'var_names')[var]
            var_array                   = netcdf_variable_to_array(data_src, var_src, dtype = 'float32')

            var_array_ux                = transform(var_array, src, var)
            
            var_array_2d                = select_o_apply_d(var_array_ux, array_sel_4d = array_sel_4d,
                                                           method_sel = method_sel, axis_sel = axis_sel,
                                                           axis_sel_shrink = axis_sel_shrink, 
                                                           method_agg_4d = method_agg_4d, 
                                                           method_agg_time = method_agg_time)
            
            data_out[f'{src}_{var}_{method_agg_time}'] = (['latitude', 'longitude'], var_array_2d)

    print(f'Succesfully created tesseract for sources and variables!\n')

    data_out.to_netcdf(f'{file_out}', mode='w', format='NETCDF4_CLASSIC')