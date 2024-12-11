
import pandas as pd
import xarray as xr
    
def resample(df: pd.DataFrame | pd.Series | xr.Dataset | xr.DataArray,
            offset_str: str, 
            method: str = 'mean',
            yearly_agg: bool = True,
            **kwargs) -> pd.DataFrame | pd.Series | xr.Dataset | xr.DataArray:
    
    print(f'\nResampling dataframe by {method} to {offset_str} time frequency...\n')

    if isinstance(df, xr.Dataset) | isinstance(df, xr.DataArray):

        func_ = getattr(xr.DataArray, method)
    
        index = 'time.year'
        
        offset_str_ = {'time': offset_str}
        
        df_resampler = df.resample(indexer = offset_str_)

        df_resampled = func_(df_resampler, **kwargs)

    elif isinstance(df, pd.DataFrame) | isinstance(df, pd.Series):
    
        index = df.index.year

        if yearly_agg: df = df.groupby(index, group_keys = False)

        df_resampler = df.resample(offset_str)

        df_resampled = df_resampler.agg(method)

    else: NotImplementedError('')

    return df_resampled


def reindex(df, timeseries, method =  None):

    df_new_time = df.reindex(timeseries, method = method)

    return df_new_time

    