
import pandas as pd

def single_site_model_benchmarks(name, df, variable: str, obs: str, df_static, sel_landcover):

    print('Calculate model benchmarks based on single sites and observations\n')

    from my_.series.group import select_multi_index, nona_level
    from my_.series.aggregate import single_axis_wise
    from my_.math.stats import rmse, pbias, r
    from my_.files.handy import save_df

    df_nona                     = nona_level(df, 
                                             ['Variable', 'Station'],
                                             axis = 1,
                                             how = 'any')

    df_n                        = select_multi_index(df_nona, ['Variable', 'Landcover'],
                                                      keys = [variable, sel_landcover])
    
    df_n.columns = df_n.columns.droplevel(level = [-1, -3])

    df_groups                   = df_n.groupby(axis = 1, level = ['Station'], group_keys = False)

    df_rmse                     = df_groups.apply(single_axis_wise, 
                                                  level = 'Source', 
                                                  key = obs, 
                                                  ffunc = rmse)
    
    df_pbias                    = df_groups.apply(single_axis_wise, level = 'Source', key = obs, ffunc = pbias)
    df_r                        = df_groups.apply(single_axis_wise, level = 'Source', key = obs, ffunc = r)

    names                       = df_static['name']
    lc                          = df_static['landcover']
    vars                        = [variable] * len(lc)

    df_count                    = df_n.count()#.droplevel(['Variable', 'Landcover']).unstack().T.reindex(names)
    
    df_lc_count                 = df_n.groupby(axis = 1, level = ['Source', 'Landcover']).count().sum().T

    new_cols                    = pd.MultiIndex.from_arrays([vars, lc, names])

    df_rmse_sort                = df_rmse.reindex(new_cols, axis = 0)
    df_pbias_sort               = df_pbias.reindex(new_cols, axis = 1).T
    df_r_sort                   = df_r.reindex(new_cols, axis = 1).T

    save_df(df_rmse, f'out/{name}/csv/stations_rmse_{variable}.csv')
    save_df(df_pbias, f'out/{name}/csv/stations_pbias_{variable}.csv')
    save_df(df_r, f'out/{name}/csv/stations_r_{variable}.csv')
    save_df(df_count, f'out/{name}/csv/stations_count_{variable}.csv')
    #save_df(df_lc_count, f'out/{name}/csv/landcover_count_{variable}.csv')
    


def landcover_model_benchmarks(name: str, 
                               df: pd.DataFrame, 
                               variable: str, 
                               obs: str, 
                               sel_landcover: list[str]):

    print('Calculate model benchmarks based on landcover and observations\n')
    
    from my_.series.group import select_multi_index, nona_level
    from my_.series.aggregate import single_level_wise, count_nonzero
    from my_.math.stats import rmse, pbias, r
    from my_.files.handy import save_df

    stations_uq = df.columns.unique(level = 'Station')
    
    stations_count = df.columns\
                       .get_level_values('Station')\
                       .value_counts()
    
    for s in stations_uq:
        
        if stations_count[s] == 1:

            df = df.drop(s, axis = 1, level = 'Station')

    df_nona = nona_level(df, 
                         ['Variable', 'Station'],
                         axis = 1,
                         how = 'any')

    #df_nona = df_nona.dropna(axis = 1, 
    #                         how = 'all')

    df_n = select_multi_index(df_nona, 
                              ['Variable', 'Landcover'],
                              keys = [variable, sel_landcover],
                              axis = 1)
    
    df_groups = df_n.T.groupby(level = ['Landcover'])

    df_groups_rmse = df_groups.apply(single_level_wise, 
                                     level = 'Source', 
                                     key = obs, 
                                     ffunc = rmse,
                                     axis = 0)

    
    df_groups_pbias = df_groups.apply(single_level_wise, 
                                      level = 'Source', 
                                      key = obs, 
                                      ffunc = pbias,
                                      axis = 0)
    
    df_groups_r  = df_groups.apply(single_level_wise, 
                                   level = 'Source', 
                                   key = obs, 
                                   ffunc = r,
                                   axis = 0)

    df_lc_count = df_n.groupby(axis = 1, 
                               level = ['Source', 'Landcover'])\
                                .count()\
                                    .sum()
    
    df_groups_count = pd.DataFrame({'count': 
                                   df_lc_count})

    df_out = df_groups_pbias.join(df_groups_rmse)\
                            .join(df_groups_r)\
                                  .T\
                                  .swaplevel(axis = 1)

    
    save_df(df_groups_count, 
            f'out/{name}/csv/landcover_count_{variable}.csv')
    
    save_df(df_out, 
            f'out/{name}/csv/landcover_r_rmse_pbias_{variable}.csv')


    
