import pandas as pd
import numpy as np


def cell_to_df(cell: np.ndarray, 
               columns: pd.Index | pd.MultiIndex | pd.Series, 
               index: pd.Index | pd.MultiIndex | pd.Series, 
               dtype: str | None):

    """
    for 1d or 2d cell data
    """

    if dtype is None: dtype = cell.dtype

    df                      = pd.DataFrame(cell, columns = columns, index = index, dtype = dtype)
    
    return df


def tile_array_to_list(array, n_times):

    list_df                 = list(array)

    list_tiled              = list_df * n_times

    return list_tiled


def tab_to_array(tabular):

    import pandas as pd

    if isinstance(tabular, pd.Series): 
        
        tabular =  tabular.values
    
    if isinstance(tabular, pd.DataFrame): 
            
        tabular =  tabular.values

        tabular = tabular.flatten()

    return tabular


