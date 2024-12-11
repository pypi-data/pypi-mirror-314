
"""
A python script to extract netcdf grid-cell data from any grid
Stations information in csv file
The out put time series can be in parquet or csv
"""
import numpy as np
import pandas as pd


def closest_cells(coords_points: np.ndarray, 
                  coords_cells: np.ndarray, 
                  shape: tuple[int]) -> np.ndarray:

    cells = [closest_cell(coords_points[i], 
                          coords_cells, 
                          shape)[0] 
                          for i in range(len(coords_points))]

    return np.array(cells)


def closest_cell(coords_point: np.ndarray, 
                 coords_cells: np.ndarray, 
                 shape: tuple[int]) -> tuple[np.ndarray, np.ndarray]:
    
    """
    Find the closest coordinate point.
    Given a point in 2d coordinates,
    and a list of points find the node.
    """

    if not isinstance(coords_point, np.ndarray): np.array(coords_point)
   
    deltas          = np.subtract(coords_cells, coords_point)

    dist            = np.einsum('ij,ij->i', deltas, deltas)

    closest_i       = np.nanargmin(dist)

    closest_coords  = coords_cells[closest_i, :]

    closest_cell    = np.unravel_index(closest_i, shape)

    return closest_cell, closest_coords


def grid_to_cell_df(array: np.ndarray, 
                    points: np.ndarray, 
                    shape: tuple[int], 
                    column: pd.Index | pd.MultiIndex, 
                    latitude: float, 
                    longitude: float,
                    index: pd.Index | pd.Series,
                    dtype = str) -> tuple[np.ndarray, np.ndarray, pd.Series]:

    """
    Get data from 3d or 4d array
    for one cell along time dimension
    Grid contains the lat lon points 
    lat lon are dims -2 and -1
    time is dim 0
    """

    from my_.series.convert import cell_to_df


    coords_point                = (latitude, longitude)

    indices_cell, coords_cell   = closest_cell(coords_point, points, shape)

    y_cell, x_cell              = [*indices_cell]

    array_cell                  = cell(array, y_cell, x_cell)

    timeseries_cell             = cell_to_df(array_cell, 
                                             column, 
                                             index,
                                             dtype).astype('float') 

    return indices_cell, coords_cell, timeseries_cell


def cell(array: np.ndarray, 
         y: int, 
         x: int, 
         y_dim: int = -2, 
         x_dim: int = -1) -> np.ndarray:

    """
    Get data from 3d or 4d array
    for one cell along time dimension
    Grid contains the lat lon points 
    lat lon are dims -2 and -1
    time is dim 0
    """
    
    #ndim                        = array.ndim
    #print(ndim)
    #
    #indx                        = [slice(None)] * ndim
    #indx[y_dim]                 = slice(y)
    #indx[x_dim]                 = slice(x)

    cell                        = array[..., y, x]
    
    return cell
        

def cells(array: np.ndarray, 
          ys: list[float] | np.ndarray, 
          xs: list[float] | np.ndarray, 
          y_dim: int = -2, 
          x_dim: int = -1):

    cells                       = [cell(array, ys[i], xs[i]) for i in range(len(ys))]

    return cells


def sites(source: str,
          variables: list[str],
          sites: pd.DataFrame,
          year_start: int,
          year_end: int,
          file_out: str | None = None,
          type_out: str = 'csv') -> pd.DataFrame:
    
    from my_.data.templates import gridded_data, grid, check_data_module
    from my_.series.group import single_multiindex
    from my_.series.aggregate import concat
    from my_.files.handy import save_df, check_file_exists
    from itertools import product

    if file_out is None: file_out = f'out'

    if check_file_exists(f'{file_out}.{type_out}'): return

    data_module = check_data_module('my_.data',
                                    source)
    if not data_module: return

    data = gridded_data(**data_module)
    
    data_variables = data.get_values(variables,
                                     y0 = year_start,
                                     y1 = year_end)
    
    grid_module = check_data_module(f'my_.data', 'grids')
    grid_attributes = getattr(grid_module, data.grid)

    data_grid = grid(**grid_attributes)
    points = data_grid.points()
    shape = data_grid.shape()
    index_time = data.index_time(year_start,
                                 year_end)

    list_ts = []

    n_sites = len(sites['name'])

    print(f'\nBegin loop over {n_sites} sites...\n')
    
    sites_out = sites.copy()

    for site, var in product(sites.index, variables):

        print(f'Get {var} data from location of site {site}...\n')
        
        site_latitude = sites['latitude'][site]
        site_longitude = sites['longitude'][site]
        site_name = sites['name'][site]
        site_type = sites['ecosystem_type'][site]

        units = data.variable_units[var]

        var_array = data_variables[var]

        if var_array.ndim == 3:
        
            indices = {'Variable': var_array, 
                       'Source': source, 
                       'Variable': var,
                       'Unit': units, 
                       'Ecosystem type': site_type, 
                       'Site': site_name}
            
        elif var_array.ndim == 4:
                       
            layers = np.arange(var_array.shape[1]).astype(str).tolist()
        
            indices = {'Variable': var_array, 
                       'Source': source, 
                       'Variable': var,
                       'Unit': units, 
                       'Ecosystem type': site_type, 
                       'Site': site_name,
                       'Layer': layers}


        column = single_multiindex(indices)
                        
        idxs, coords, ts = grid_to_cell_df(data_variables[var], 
                                           points, 
                                           shape, 
                                           column, 
                                           site_latitude, 
                                           site_longitude,
                                           index_time)

        list_ts.append(ts)
                    
        sites_out.loc[site, 'i_lat'] = idxs[0]
        sites_out.loc[site, 'i_lon'] = idxs[1]
        sites_out.loc[site, 'cell_lat'] = coords[0]
        sites_out.loc[site, 'cell_lon'] = coords[1]
    
    df_out = concat(list_ts, 
                    sort = False)

    save_df(sites_out,
            f'deims/sites_out_{source}.csv')
    
    save_df(df_out, 
            f'{file_out}.{type_out}', 
            type_out)


    
    
