import pandas as pd
import re
import xarray as xr

def index(y0: int, 
          y1: int, 
          t_res: str,
          month0: int = 1,
          month1: int = 12, 
          day0: int = 1,
          day1: int = 31,
          leapday: bool = True,
          range_kwargs: dict = {},
          resample_kwargs: dict = {}) -> pd.Series:

    """
    Create time index from beginning of year 0
    to end of year 0;
    To use for pandas time series;
    """
    
    if t_res[-1] == 'H': end_time = str(24 - int(t_res[:-1]))
    else: end_time = '23:59:00'

    y0_time = f'{y0}-{month0:02}-{day0:02} 00:00:00'
    y1_time = f'{y1}-{month1:02}-{day1:02} {end_time}'

    t_res_comp = re.split('(\d+)', t_res)

    t_res_str = t_res_comp[-1]

    time_raw = pd.date_range(y0_time, 
                             y1_time, 
                             freq = t_res_str,
                             **range_kwargs).to_series()

    # Make yearly groups for resample
    time_groups = time_raw.groupby(time_raw.year, 
                                   group_keys=False)

    # Resample. Not always needed (but e.g. for multiples 
    # '8D' frequecies)
    time_resampled = time_groups.resample(t_res, 
                                          **resample_kwargs) \
                                          .asfreq()
    
    if leapday == False: 
        time_resampled = drop_leapday(time_resampled)

    return time_resampled


def drop_leapday(series):

    """
    Drop the leapday entries from any
    time series. I think there should be
    an easier way as long as index is 
    datetime.
    """

    mask = [False if (s.month == 2 and s.day == 29) else True for s in series.index]

    series_out = series[mask]

    return series_out


def xr_resample(df: xr.Dataset | xr.DataArray,
                offset_str: str, 
                method: str = 'mean',
                **kwargs) -> xr.Dataset | xr.DataArray:
    
    func_ = getattr(xr.DataArray, method)
        
    df_resampler = df.resample(time = offset_str)

    df_resampled = func_(df_resampler, **kwargs)

    return df_resampled


def pd_resample(df: pd.DataFrame | pd.Series,
                offset_str: str, 
                method: str = 'mean',
                yearly_agg: bool = True) -> pd.DataFrame | pd.Series:
    
    print(f'\nResampling dataframe by {method} to {offset_str} time frequency...\n')
    
    index = pd.to_datetime(df.index).year

    if yearly_agg: df_n = df.groupby(index, group_keys = False)

    df_resampler = df_n.resample(offset_str)

    df_resampled = df_resampler.agg(method)

    return df_resampled