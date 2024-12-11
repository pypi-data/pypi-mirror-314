import pandas as pd
    
def multi_columns(groups: list = [], names: list = []):

    import pandas as pd

    multi_columns           = pd.MultiIndex.from_product(groups, names = names)

    return multi_columns


def src_var_lc_station_index(sources, variables, landcover, stations):

    import pandas as pd

    columns                 = multi_columns(groups = [sources, variables, stations], names = ['Source', 'Variable', 'Station'])

    df_columns              = columns.to_frame()

    df_columns.insert(2, 'Landcover', landcover)

    new_columns             = pd.MultiIndex.from_frame(df_columns)

    new_columns_sorted      = new_columns.sort_values()

    return new_columns_sorted


def single_src_var_X_index(array, src, var, lc, name_station):

    if array.ndim == 3: 

        column          = single_src_var_lc_station_index(src, var, lc, name_station)

    elif array.ndim == 4:

        n_layers                = array.shape[1]

        column          = single_src_var_lc_station_layer_index(src, var, lc, name_station, n_layers = n_layers)

    return column


def single_src_var_lc_station_index(src, var, lc, station):
    
    import pandas as pd

    names                   = ['Source', 'Variable', 'Landcover', 'Station']

    tuple_index             = (src, var, lc, station)

    index                   = pd.MultiIndex.from_tuples([tuple_index], names = names)

    return index


def single_multiindex(dictionary: dict):
    
    import pandas as pd

    names = list(dictionary.keys())

    indices = list(dictionary.values())

    if any([isinstance(i, list) for i in indices]):

        indices = [[i] if not isinstance(i, list)
                   else i
                   for i in indices]

        index = pd.MultiIndex.from_product(indices, names = names)

    else:
        
        index = pd.MultiIndex.from_tuples([indices], names = names)

    return index


def single_src_var_lc_station_layer_index(src, var, lc, station, n_layers):
    
    import pandas as pd
    import numpy as np

    if n_layers > 0:

        layers              = np.arange(n_layers).astype(str).tolist()

    elif n_layers < 0:

        layers              = [n_layers]

    names                   = ['Source', 'Variable', 'Landcover', 'Station', 'Layer']

    tuple_index             = [[src], [var], [lc], [station], layers]

    index                   = pd.MultiIndex.from_product(tuple_index, names = names)

    return index


def add_level_to_multi_columns(df, level: int, name_level: str, level_values, sort = False):

    import pandas as pd

    # Convert index to dataframe
    old_idx             = df.columns.to_frame()

    # Insert new level at specified location

    if level == -1:

        new_level       = pd.Series(level_values, name = name_level, index = old_idx.index)

        old_idx         = old_idx.join(new_level)

    else: 
        
        old_idx.insert(level, name_level, level_values)

    # Convert back to MultiIndex
    new_index           = pd.MultiIndex.from_frame(old_idx)

    df_new              = df.copy()
    df_new.columns      = new_index

    if sort: df_new == df_new.sort_index(axis = 1)

    return df_new


def layer_level_to_int(df):

    level_names         = df.columns.names

    if 'Layer' not in level_names: return df
    
    i_level             = level_names.index('Layer')

    level_int           = df.columns.levels[i_level].astype(int)
    
    df.columns          = df.columns.set_levels(level_int, level = i_level)

    return df


def select_multi_index(df: pd.DataFrame, 
                       levels: list, 
                       keys: list, 
                       axis = 1) -> pd.DataFrame:

    if isinstance(levels, str): levels = [levels]
    if isinstance(keys, str): keys = [keys]
    if isinstance(df, pd.Series): df = df.to_frame()

    axx = df.columns if axis == 1 else df.index

    n_levels = axx.nlevels

    names_levels = axx.names

    index_level = [names_levels.index(level) for level in levels]

    list_index = [slice(None)] * n_levels

    for i_indxs, indxs in enumerate(index_level):
        
        kk = keys[i_indxs]

        if isinstance(kk, str): kk = [kk]

        iikeys = [k for k in kk
                  if k in axx.get_level_values(indxs)]

        list_index[indxs] = iikeys
    
    if axis == 1:
        df_sel = df.loc[:, tuple(list_index)]

    else: 
        df_sel = df.loc[tuple(list_index), :]

    return df_sel


def nona_level(df: pd.DataFrame, 
               level: str | list[str], 
               axis: int = 1, 
               how: str = 'all'):

    if axis == 1 : df = df.T

    df_level_groups = df.groupby(sort = False, 
                                 level = level)
    
    df_nona = df_level_groups.apply(pd.DataFrame.dropna,
                                    axis = 1,
                                    how = how)
    
    if axis == 1: return df_nona.T

    return df_nona 
