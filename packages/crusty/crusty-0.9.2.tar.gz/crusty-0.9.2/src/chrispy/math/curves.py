
import pandas as pd
import numpy as np

def peaks(data: pd.Series | np.ndarray, 
          sigma: int = 6,
          distance: int = 46):

    from scipy.signal import find_peaks
    from scipy.ndimage import gaussian_filter1d

    smoo_ = gaussian_filter1d(data, sigma = sigma)

    peaks_ = find_peaks(smoo_, distance = distance)

    if isinstance(peaks_[0], np.ndarray):
        return peaks_[0]
    elif not peaks_[0]: 
        return np.nan
    elif isinstance(data, pd.Series):
        return peaks_[0][0]
    elif isinstance(data, np.ndarray):
        return peaks_[0]


def inflictions(df: pd.Series,
                sigma: int = 6):
    
    from scipy.ndimage import gaussian_filter1d

    smoo = gaussian_filter1d(df, sigma = sigma)

    d2 = np.gradient(np.gradient(smoo))

    infl = np.nonzero(np.diff(np.sign(d2)))[0]

    df_out = df.copy().drop(df.index)

    if (len(infl) == 0) or (len(infl) >= len(df.index) / 2): 
        
        infl = [np.nan]

    for i in range(len(infl)):

        df_out[i] = infl[i]

    return df_out
