
import numpy as np
from my_.series.convert import tab_to_array


def rmse(obs, sim, decimals=2):

    """
    Root mean square error 
    Use this to compare model to observation series
    """    

    obs = tab_to_array(obs)
    sim = tab_to_array(sim)
    
    error = sim - obs

    if np.all(np.isnan(error)): return np.nan

    squared_error = error**2

    sum_squared_error = np.nansum(squared_error)

    n = np.count_nonzero(~np.isnan(error))

    mean_squared_error = sum_squared_error / n

    rmse = mean_squared_error**0.5

    rmse_rounded = np.around(rmse, decimals)
    
    return rmse_rounded


def pbias(obs, sim, decimals: int = 2):

    obs = tab_to_array(obs)
    sim = tab_to_array(sim)

    bias = sim - obs

    if np.all(np.isnan(bias)): return np.nan

    sum_bias = np.nansum(bias)

    sum_obs = np.nansum(obs)

    rel_bias = sum_bias / sum_obs
    
    percent_bias = rel_bias * 100

    percent_bias_rounded = np.around(percent_bias, decimals)

    return percent_bias_rounded


def r(obs, sim, decimals: int = 2):

    from scipy.stats.stats import pearsonr

    obs = tab_to_array(obs)
    sim = tab_to_array(sim)

    mask = ~np.isnan(obs) & ~np.isnan(sim)
    
    if np.count_nonzero(mask) <= 5: return np.nan

    obs_masked = obs[mask]
    sim_masked = sim[mask]

    r, p = pearsonr(obs_masked, sim_masked)

    r_rounded, p_rounded = np.around(r, decimals), np.around(p, decimals)

    return r_rounded