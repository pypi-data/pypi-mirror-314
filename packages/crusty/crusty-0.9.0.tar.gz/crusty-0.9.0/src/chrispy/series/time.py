

import pandas as pd
import re

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

    if t_res_comp[0].isdigit(): t_res_num = t_res_comp[0]
    else: t_res_num = None

    t_res_str = t_res_comp[-1]

    time_raw = pd.date_range(y0_time, 
                             y1_time, 
                             freq = t_res_str,
                             **range_kwargs).to_series()

    # Make yearly groups for resample
    time_groups = time_raw.groupby(time_raw.index.year, 
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

    mask                        = [False if (s.month == 2 and s.day == 29) else True for s in series.index]

    series_out                  = series[mask]

    return series_out


def FLX_to_datetime(frequencies: list = []):

    translate                   = { 'Y': 'Y',
                                    'M': 'M',
                                    'D': 'D',
                                    'H': 'H'
                                   }
    
    freqs_translated            = [translate[freq] for freq in frequencies]
    
    return freqs_translated


def lowest_frequency(frequencies: list = []):

    """
    pandas date time offset strings

    """

    import numpy as np

    scores                      = {'Y': 0, 'M': 1, 'D': 2, 'H': 3}
    scores_rev                  = {v: k for k, v in scores.items()}

    freq_scores                 = [scores[freq] for freq in frequencies]

    freq_scores_array           = np.array(freq_scores)

    lowest_freq_score           = np.min(freq_scores_array)

    lowest_freq                 = scores_rev[lowest_freq_score]

    return lowest_freq


def index_to_datetime(df: pd.DataFrame, 
                      format: str | None = None):

    import pandas as pd

    df.index                    = pd.to_datetime(df.index, format = format)

    return df