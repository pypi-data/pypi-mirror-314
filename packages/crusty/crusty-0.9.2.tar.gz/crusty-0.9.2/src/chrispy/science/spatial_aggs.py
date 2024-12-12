

def landcover_spatial_moments(name_case: str, sources = [], variables = [], year_start: int = 1995, year_end: int = 2018,
                    moments = ['mean', 'variance']):

    print(f'\nIterate over gridded source data:\n{*sources,}\n')

    from my_resources.sources import query_variables, available_variables
    from my_files.handy import yearly_or_monthly_files, save_df
    from my_files.netcdf import open_netcdf, netcdf_variables_to_array
    from my_resources.units import transform
    from my_gridded.dimensions import select
    from my_math.stats import mean, variance
    from user_in.options_analyses import selected_landcover


    for src in sources:
     
        path                    = query_variables(src, 'path')
        freq_files              = query_variables(src, 'freq_files')

        vars_avail, vars_src    = available_variables(src, variables)

        files                   = yearly_or_monthly_files(freq_files, path, year_start, year_end)

        print('Load data...\n')

        data                    = open_netcdf(files)
        arrays_list             = netcdf_variables_to_array(data, vars_src, 'float32')

        for i_var, var in enumerate(vars_avail):

            array               = arrays_list[i_var]

            array_ux            = transform(array, src, var)

            for lc in selected_landcover:

                print(lc)

                indices_lc      = query_variables(src, 'sel_agg_layer_PFT')[lc]

                array_pft       = select(array_ux, indices_lc,  1)

                array_lc        = mean(array_pft, axes = 0)

                array_mean      = mean(array_lc, axes = (0, -2, -1))

                array_var       = variance(array_lc, axes = (0, -2, -1))

                print(array_mean, array_var)

                








landcover_spatial_moments('cool', sources = ['CLM5-EU3-pft'], variables = ['GPP'])




